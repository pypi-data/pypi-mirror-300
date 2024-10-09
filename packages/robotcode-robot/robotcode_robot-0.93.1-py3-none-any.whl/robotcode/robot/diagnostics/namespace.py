import ast
import enum
import itertools
import time
import weakref
from collections import OrderedDict, defaultdict
from concurrent.futures import CancelledError
from itertools import chain
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
)

from robot.errors import VariableError
from robot.libraries import STDLIBS
from robot.parsing.lexer.tokens import Token
from robot.parsing.model.blocks import Keyword, SettingSection, TestCase, VariableSection
from robot.parsing.model.statements import Arguments, Setup, Statement, Timeout
from robot.parsing.model.statements import LibraryImport as RobotLibraryImport
from robot.parsing.model.statements import ResourceImport as RobotResourceImport
from robot.parsing.model.statements import (
    VariablesImport as RobotVariablesImport,
)
from robot.variables.search import (
    is_scalar_assign,
    is_variable,
    search_variable,
)
from robotcode.core.concurrent import RLock
from robotcode.core.event import event
from robotcode.core.lsp.types import (
    CodeDescription,
    Diagnostic,
    DiagnosticRelatedInformation,
    DiagnosticSeverity,
    DiagnosticTag,
    DocumentUri,
    Location,
    Position,
    Range,
)
from robotcode.core.text_document import TextDocument
from robotcode.core.uri import Uri
from robotcode.core.utils.logging import LoggingDescriptor

from ..utils import get_robot_version
from ..utils.ast import (
    range_from_node,
    range_from_token,
    strip_variable_token,
    tokenize_variables,
)
from ..utils.match import eq_namespace
from ..utils.stubs import Languages
from ..utils.variables import BUILTIN_VARIABLES
from ..utils.visitor import Visitor
from .entities import (
    ArgumentDefinition,
    BuiltInVariableDefinition,
    CommandLineVariableDefinition,
    EnvironmentVariableDefinition,
    GlobalVariableDefinition,
    Import,
    InvalidVariableError,
    LibraryEntry,
    LibraryImport,
    LocalVariableDefinition,
    ResourceEntry,
    ResourceImport,
    TestVariableDefinition,
    VariableDefinition,
    VariableMatcher,
    VariablesEntry,
    VariablesImport,
)
from .errors import DIAGNOSTICS_SOURCE_NAME, Error
from .imports_manager import ImportsManager
from .library_doc import (
    BUILTIN_LIBRARY_NAME,
    DEFAULT_LIBRARIES,
    KeywordDoc,
    KeywordError,
    KeywordMatcher,
    LibraryDoc,
    resolve_robot_variables,
)


class DiagnosticsError(Exception):
    pass


class DiagnosticsWarningError(DiagnosticsError):
    pass


class ImportError(DiagnosticsError):
    pass


class NameSpaceError(Exception):
    pass


class VariablesVisitor(Visitor):
    def get(self, source: str, model: ast.AST) -> List[VariableDefinition]:
        self._results: List[VariableDefinition] = []
        self.source = source
        self.visit(model)
        return self._results

    def visit_Section(self, node: ast.AST) -> None:  # noqa: N802
        if isinstance(node, VariableSection):
            self.generic_visit(node)

    def visit_Variable(self, node: Statement) -> None:  # noqa: N802
        name_token = node.get_token(Token.VARIABLE)
        if name_token is None:
            return

        name = name_token.value

        if name is not None:
            match = search_variable(name, ignore_errors=True)
            if not match.is_assign(allow_assign_mark=True):
                return

            if name.endswith("="):
                name = name[:-1].rstrip()

            values = node.get_values(Token.ARGUMENT)
            has_value = bool(values)
            value = tuple(
                s.replace(
                    "${CURDIR}",
                    str(Path(self.source).parent).replace("\\", "\\\\"),
                )
                for s in values
            )

            self._results.append(
                VariableDefinition(
                    name=name,
                    name_token=strip_variable_token(
                        Token(
                            name_token.type,
                            name,
                            name_token.lineno,
                            name_token.col_offset,
                            name_token.error,
                        )
                    ),
                    line_no=node.lineno,
                    col_offset=node.col_offset,
                    end_line_no=node.lineno,
                    end_col_offset=node.end_col_offset,
                    source=self.source,
                    has_value=has_value,
                    resolvable=True,
                    value=value,
                )
            )


class VariableVisitorBase(Visitor):
    def __init__(
        self,
        namespace: "Namespace",
        nodes: Optional[List[ast.AST]] = None,
        position: Optional[Position] = None,
        in_args: bool = True,
    ) -> None:
        super().__init__()
        self.namespace = namespace
        self.nodes = nodes
        self.position = position
        self.in_args = in_args

        self._results: Dict[str, VariableDefinition] = {}
        self.current_kw_doc: Optional[KeywordDoc] = None
        self.current_kw: Optional[Keyword] = None

    def get_variable_token(self, token: Token) -> Optional[Token]:
        return next(
            (
                v
                for v in itertools.dropwhile(
                    lambda t: t.type in Token.NON_DATA_TOKENS,
                    tokenize_variables(token, ignore_errors=True, extra_types={Token.VARIABLE}),
                )
                if v.type == Token.VARIABLE
            ),
            None,
        )


class ArgumentVisitor(VariableVisitorBase):
    def __init__(
        self,
        namespace: "Namespace",
        nodes: Optional[List[ast.AST]],
        position: Optional[Position],
        in_args: bool,
        current_kw_doc: Optional[KeywordDoc],
    ) -> None:
        super().__init__(namespace, nodes, position, in_args)

        self.current_kw_doc: Optional[KeywordDoc] = current_kw_doc

    def get(self, model: ast.AST) -> Dict[str, VariableDefinition]:
        self._results = {}

        self.visit(model)

        return self._results

    def visit_Arguments(self, node: Statement) -> None:  # noqa: N802
        args: List[str] = []

        arguments = node.get_tokens(Token.ARGUMENT)

        for argument_token in arguments:
            try:
                argument = self.get_variable_token(argument_token)

                if argument is not None and argument.value != "@{}":
                    if (
                        self.in_args
                        and self.position is not None
                        and self.position in range_from_token(argument_token)
                        and self.position > range_from_token(argument).end
                    ):
                        break

                    if argument.value not in args:
                        args.append(argument.value)
                        arg_def = ArgumentDefinition(
                            name=argument.value,
                            name_token=strip_variable_token(argument),
                            line_no=argument.lineno,
                            col_offset=argument.col_offset,
                            end_line_no=argument.lineno,
                            end_col_offset=argument.end_col_offset,
                            source=self.namespace.source,
                            keyword_doc=self.current_kw_doc,
                        )
                        self._results[argument.value] = arg_def

            except VariableError:
                pass


class OnlyArgumentsVisitor(VariableVisitorBase):
    def get(self, model: ast.AST) -> List[VariableDefinition]:
        self._results = {}

        self.visit(model)

        return list(self._results.values())

    def visit(self, node: ast.AST) -> None:
        if self.position is None or self.position >= range_from_node(node).start:
            super().visit(node)

    def visit_Keyword(self, node: ast.AST) -> None:  # noqa: N802
        self.current_kw = cast(Keyword, node)
        try:
            self.generic_visit(node)
        finally:
            self.current_kw = None
            self.current_kw_doc = None

    def visit_KeywordName(self, node: Statement) -> None:  # noqa: N802
        from .model_helper import ModelHelper

        name_token = node.get_token(Token.KEYWORD_NAME)

        if name_token is not None and name_token.value:
            keyword = ModelHelper.get_keyword_definition_at_token(self.namespace.get_library_doc(), name_token)
            self.current_kw_doc = keyword

            for variable_token in filter(
                lambda e: e.type == Token.VARIABLE,
                tokenize_variables(name_token, identifiers="$", ignore_errors=True),
            ):
                if variable_token.value:
                    match = search_variable(variable_token.value, "$", ignore_errors=True)
                    if match.base is None:
                        continue
                    name = match.base.split(":", 1)[0]
                    full_name = f"{match.identifier}{{{name}}}"
                    var_token = strip_variable_token(variable_token)
                    var_token.value = name
                    self._results[full_name] = ArgumentDefinition(
                        name=full_name,
                        name_token=var_token,
                        line_no=variable_token.lineno,
                        col_offset=variable_token.col_offset,
                        end_line_no=variable_token.lineno,
                        end_col_offset=variable_token.end_col_offset,
                        source=self.namespace.source,
                        keyword_doc=self.current_kw_doc,
                    )

            if self.current_kw is not None:
                args = ArgumentVisitor(
                    self.namespace, self.nodes, self.position, self.in_args, self.current_kw_doc
                ).get(self.current_kw)
                if args:
                    self._results.update(args)


class BlockVariableVisitor(OnlyArgumentsVisitor):

    def visit_ExceptHeader(self, node: Statement) -> None:  # noqa: N802
        variables = node.get_tokens(Token.VARIABLE)[:1]
        if variables and is_scalar_assign(variables[0].value):
            try:
                variable = self.get_variable_token(variables[0])

                if variable is not None:
                    self._results[variable.value] = LocalVariableDefinition(
                        name=variable.value,
                        name_token=strip_variable_token(variable),
                        line_no=variable.lineno,
                        col_offset=variable.col_offset,
                        end_line_no=variable.lineno,
                        end_col_offset=variable.end_col_offset,
                        source=self.namespace.source,
                    )

            except VariableError:
                pass

    def _get_var_name(self, original: str, position: Position, require_assign: bool = True) -> Optional[str]:
        robot_variables = resolve_robot_variables(
            str(self.namespace.imports_manager.root_folder),
            str(Path(self.namespace.source).parent) if self.namespace.source else ".",
            self.namespace.imports_manager.get_resolvable_command_line_variables(),
            variables=self.namespace.get_resolvable_variables(),
        )

        try:
            replaced = robot_variables.replace_string(original)
        except VariableError:
            replaced = original
        try:
            name = self._resolve_var_name(replaced, robot_variables)
        except ValueError:
            name = original
        match = search_variable(name, identifiers="$@&")
        match.resolve_base(robot_variables)
        valid = match.is_assign() if require_assign else match.is_variable()
        if not valid:
            return None
        return str(match)

    def _resolve_var_name(self, name: str, variables: Any) -> str:
        if name.startswith("\\"):
            name = name[1:]
        if len(name) < 2 or name[0] not in "$@&":
            raise ValueError
        if name[1] != "{":
            name = f"{name[0]}{{{name[1:]}}}"
        match = search_variable(name, identifiers="$@&", ignore_errors=True)
        match.resolve_base(variables)
        if not match.is_assign():
            raise ValueError
        return str(match)

    def visit_KeywordCall(self, node: Statement) -> None:  # noqa: N802
        # TODO  analyze "Set Local/Global/Suite Variable"

        for assign_token in node.get_tokens(Token.ASSIGN):
            variable_token = self.get_variable_token(assign_token)

            try:
                if variable_token is not None:
                    if (
                        self.position is not None
                        and self.position in range_from_node(node)
                        and self.position > range_from_token(variable_token).end
                    ):
                        continue

                    if variable_token.value not in self._results:
                        self._results[variable_token.value] = LocalVariableDefinition(
                            name=variable_token.value,
                            name_token=strip_variable_token(variable_token),
                            line_no=variable_token.lineno,
                            col_offset=variable_token.col_offset,
                            end_line_no=variable_token.lineno,
                            end_col_offset=variable_token.end_col_offset,
                            source=self.namespace.source,
                        )

            except VariableError:
                pass

        keyword_token = node.get_token(Token.KEYWORD)
        if keyword_token is None or not keyword_token.value:
            return

        keyword = self.namespace.find_keyword(keyword_token.value, raise_keyword_error=False)
        if keyword is None:
            return

        if keyword.libtype == "LIBRARY" and keyword.libname == "BuiltIn":
            var_type = None
            if keyword.name == "Set Suite Variable":
                var_type = VariableDefinition
            elif keyword.name == "Set Global Variable":
                var_type = GlobalVariableDefinition
            elif keyword.name == "Set Test Variable" or keyword.name == "Set Task Variable":
                var_type = TestVariableDefinition
            elif keyword.name == "Set Local Variable":
                var_type = LocalVariableDefinition
            else:
                return
            try:
                variable = node.get_token(Token.ARGUMENT)
                if variable is None:
                    return

                position = range_from_node(node).start
                position.character = 0
                var_name = self._get_var_name(variable.value, position)

                if var_name is None or not is_variable(var_name):
                    return

                var = var_type(
                    name=var_name,
                    name_token=strip_variable_token(variable),
                    line_no=variable.lineno,
                    col_offset=variable.col_offset,
                    end_line_no=variable.lineno,
                    end_col_offset=variable.end_col_offset,
                    source=self.namespace.source,
                )

                if var_name not in self._results or type(self._results[var_name]) is not type(var):
                    if isinstance(var, LocalVariableDefinition) or not any(
                        l for l in self.namespace.get_global_variables() if l.matcher == var.matcher
                    ):
                        self._results[var_name] = var
                    else:
                        self._results.pop(var_name, None)

            except VariableError:
                pass

    def visit_InlineIfHeader(self, node: Statement) -> None:  # noqa: N802
        for assign_token in node.get_tokens(Token.ASSIGN):
            variable_token = self.get_variable_token(assign_token)

            try:
                if variable_token is not None:
                    if (
                        self.position is not None
                        and self.position in range_from_node(node)
                        and self.position > range_from_token(variable_token).end
                    ):
                        continue

                    if variable_token.value not in self._results:
                        self._results[variable_token.value] = LocalVariableDefinition(
                            name=variable_token.value,
                            name_token=strip_variable_token(variable_token),
                            line_no=variable_token.lineno,
                            col_offset=variable_token.col_offset,
                            end_line_no=variable_token.lineno,
                            end_col_offset=variable_token.end_col_offset,
                            source=self.namespace.source,
                        )

            except VariableError:
                pass

    def visit_ForHeader(self, node: Statement) -> None:  # noqa: N802
        variables = node.get_tokens(Token.VARIABLE)
        for variable in variables:
            variable_token = self.get_variable_token(variable)
            if variable_token is not None and variable_token.value and variable_token.value not in self._results:
                self._results[variable_token.value] = LocalVariableDefinition(
                    name=variable_token.value,
                    name_token=strip_variable_token(variable_token),
                    line_no=variable_token.lineno,
                    col_offset=variable_token.col_offset,
                    end_line_no=variable_token.lineno,
                    end_col_offset=variable_token.end_col_offset,
                    source=self.namespace.source,
                )

    def visit_Var(self, node: Statement) -> None:  # noqa: N802
        from robot.parsing.model.statements import Var

        variable = node.get_token(Token.VARIABLE)
        if variable is None:
            return
        try:
            var_name = variable.value
            if var_name.endswith("="):
                var_name = var_name[:-1].rstrip()

            if not is_variable(var_name):
                return

            scope = cast(Var, node).scope

            if scope in ("SUITE",):
                var_type = VariableDefinition
            elif scope in ("TEST", "TASK"):
                var_type = TestVariableDefinition
            elif scope in ("GLOBAL",):
                var_type = GlobalVariableDefinition
            else:
                var_type = LocalVariableDefinition

            var = var_type(
                name=var_name,
                name_token=strip_variable_token(variable),
                line_no=variable.lineno,
                col_offset=variable.col_offset,
                end_line_no=variable.lineno,
                end_col_offset=variable.end_col_offset,
                source=self.namespace.source,
            )

            if var_name not in self._results or type(self._results[var_name]) is not type(var):
                if isinstance(var, LocalVariableDefinition) or not any(
                    l for l in self.namespace.get_global_variables() if l.matcher == var.matcher
                ):
                    self._results[var_name] = var
                else:
                    self._results.pop(var_name, None)

        except VariableError:
            pass


class ImportVisitor(Visitor):
    def get(self, source: str, model: ast.AST) -> List[Import]:
        self._results: List[Import] = []
        self.source = source
        self.visit(model)
        return self._results

    def visit_Section(self, node: ast.AST) -> None:  # noqa: N802
        if isinstance(node, SettingSection):
            self.generic_visit(node)

    def visit_LibraryImport(self, node: RobotLibraryImport) -> None:  # noqa: N802
        name = node.get_token(Token.NAME)

        separator = node.get_token(Token.WITH_NAME)
        alias_token = node.get_tokens(Token.NAME)[-1] if separator else None

        last_data_token = next(v for v in reversed(node.tokens) if v.type not in Token.NON_DATA_TOKENS)
        if node.name:
            self._results.append(
                LibraryImport(
                    name=node.name,
                    name_token=name if name is not None else None,
                    args=node.args,
                    alias=node.alias,
                    alias_token=alias_token,
                    line_no=node.lineno,
                    col_offset=node.col_offset,
                    end_line_no=(
                        last_data_token.lineno
                        if last_data_token is not None
                        else node.end_lineno if node.end_lineno is not None else -1
                    ),
                    end_col_offset=(
                        last_data_token.end_col_offset
                        if last_data_token is not None
                        else node.end_col_offset if node.end_col_offset is not None else -1
                    ),
                    source=self.source,
                )
            )

    def visit_ResourceImport(self, node: RobotResourceImport) -> None:  # noqa: N802
        name = node.get_token(Token.NAME)

        last_data_token = next(v for v in reversed(node.tokens) if v.type not in Token.NON_DATA_TOKENS)
        if node.name:
            self._results.append(
                ResourceImport(
                    name=node.name,
                    name_token=name if name is not None else None,
                    line_no=node.lineno,
                    col_offset=node.col_offset,
                    end_line_no=(
                        last_data_token.lineno
                        if last_data_token is not None
                        else node.end_lineno if node.end_lineno is not None else -1
                    ),
                    end_col_offset=(
                        last_data_token.end_col_offset
                        if last_data_token is not None
                        else node.end_col_offset if node.end_col_offset is not None else -1
                    ),
                    source=self.source,
                )
            )

    def visit_VariablesImport(self, node: RobotVariablesImport) -> None:  # noqa: N802
        name = node.get_token(Token.NAME)

        last_data_token = next(v for v in reversed(node.tokens) if v.type not in Token.NON_DATA_TOKENS)
        if node.name:
            self._results.append(
                VariablesImport(
                    name=node.name,
                    name_token=name if name is not None else None,
                    args=node.args,
                    line_no=node.lineno,
                    col_offset=node.col_offset,
                    end_line_no=(
                        last_data_token.lineno
                        if last_data_token is not None
                        else node.end_lineno if node.end_lineno is not None else -1
                    ),
                    end_col_offset=(
                        last_data_token.end_col_offset
                        if last_data_token is not None
                        else node.end_col_offset if node.end_col_offset is not None else -1
                    ),
                    source=self.source,
                )
            )


class DocumentType(enum.Enum):
    UNKNOWN = "unknown"
    GENERAL = "robot"
    RESOURCE = "resource"
    INIT = "init"


class Namespace:
    _logger = LoggingDescriptor()

    @_logger.call
    def __init__(
        self,
        imports_manager: ImportsManager,
        model: ast.AST,
        source: str,
        document: Optional[TextDocument] = None,
        document_type: Optional[DocumentType] = None,
        languages: Optional[Languages] = None,
        workspace_languages: Optional[Languages] = None,
    ) -> None:
        super().__init__()

        self.imports_manager = imports_manager

        self.model = model
        self.source = source
        self._document = weakref.ref(document) if document is not None else None
        self.document_type: Optional[DocumentType] = document_type
        self.languages = languages
        self.workspace_languages = workspace_languages

        self._libraries: Dict[str, LibraryEntry] = OrderedDict()
        self._namespaces: Optional[Dict[KeywordMatcher, List[LibraryEntry]]] = None
        self._libraries_matchers: Optional[Dict[KeywordMatcher, LibraryEntry]] = None
        self._resources: Dict[str, ResourceEntry] = OrderedDict()
        self._resources_matchers: Optional[Dict[KeywordMatcher, ResourceEntry]] = None
        self._variables: Dict[str, VariablesEntry] = OrderedDict()
        self._initialized = False
        self._invalid = False
        self._initialize_lock = RLock(default_timeout=120, name="Namespace.initialize")
        self._analyzed = False
        self._analyze_lock = RLock(default_timeout=120, name="Namespace.analyze")
        self._library_doc: Optional[LibraryDoc] = None
        self._library_doc_lock = RLock(default_timeout=120, name="Namespace.library_doc")
        self._imports: Optional[List[Import]] = None
        self._import_entries: Dict[Import, LibraryEntry] = OrderedDict()
        self._own_variables: Optional[List[VariableDefinition]] = None
        self._own_variables_lock = RLock(default_timeout=120, name="Namespace.own_variables")
        self._global_variables: Optional[List[VariableDefinition]] = None
        self._global_variables_dict: Optional[Dict[VariableMatcher, VariableDefinition]] = None
        self._global_variables_lock = RLock(default_timeout=120, name="Namespace.global_variables")
        self._global_variables_dict_lock = RLock(default_timeout=120, name="Namespace.global_variables_dict")

        self._global_resolvable_variables: Optional[Dict[str, Any]] = None
        self._global_resolvable_variables_lock = RLock(
            default_timeout=120, name="Namespace._global_resolvable_variables_lock"
        )

        self._suite_variables: Optional[Dict[str, Any]] = None
        self._suite_variables_lock = RLock(default_timeout=120, name="Namespace.global_variables")

        self._diagnostics: List[Diagnostic] = []
        self._keyword_references: Dict[KeywordDoc, Set[Location]] = {}
        self._variable_references: Dict[VariableDefinition, Set[Location]] = {}
        self._local_variable_assignments: Dict[VariableDefinition, Set[Range]] = {}
        self._namespace_references: Dict[LibraryEntry, Set[Location]] = {}

        self._imported_keywords: Optional[List[KeywordDoc]] = None
        self._imported_keywords_lock = RLock(default_timeout=120, name="Namespace.imported_keywords")
        self._keywords: Optional[List[KeywordDoc]] = None
        self._keywords_lock = RLock(default_timeout=120, name="Namespace.keywords")

        # TODO: how to get the search order from model
        self._search_order: Optional[Tuple[str, ...]] = None

        self._finder: Optional[KeywordFinder] = None

        self.imports_manager.imports_changed.add(self._on_imports_changed)
        self.imports_manager.libraries_changed.add(self._on_libraries_changed)
        self.imports_manager.resources_changed.add(self._on_resources_changed)
        self.imports_manager.variables_changed.add(self._on_variables_changed)

        self._in_initialize = False

        self._ignored_lines: Optional[List[int]] = None

    @event
    def has_invalidated(sender) -> None: ...

    @event
    def has_initialized(sender) -> None: ...

    @event
    def has_analysed(sender) -> None: ...

    @event
    def library_import_changed(sender) -> None: ...

    @event
    def resource_import_changed(sender) -> None: ...

    @event
    def variables_import_changed(sender) -> None: ...

    @property
    def document(self) -> Optional[TextDocument]:
        return self._document() if self._document is not None else None

    @property
    def search_order(self) -> Tuple[str, ...]:
        if self._search_order is None:
            return tuple(self.imports_manager.global_library_search_order)

        return self._search_order

    def _on_imports_changed(self, sender: Any, uri: DocumentUri) -> None:
        # TODO: optimise this by checking our imports
        self.invalidate()

    @_logger.call
    def _on_libraries_changed(self, sender: Any, libraries: List[LibraryDoc]) -> None:
        if not self.initialized or self.invalid:
            return

        invalidate = False

        for p in libraries:
            if any(e for e in self._libraries.values() if e.library_doc == p):
                invalidate = True
                break

        if invalidate:
            self.invalidate()

    @_logger.call
    def _on_resources_changed(self, sender: Any, resources: List[LibraryDoc]) -> None:
        if not self.initialized or self.invalid:
            return

        invalidate = False

        for p in resources:
            if any(e for e in self._resources.values() if e.library_doc.source == p.source):
                invalidate = True
                break

        if invalidate:
            self.invalidate()

    @_logger.call
    def _on_variables_changed(self, sender: Any, variables: List[LibraryDoc]) -> None:
        if not self.initialized or self.invalid:
            return

        invalidate = False

        for p in variables:
            if any(e for e in self._variables.values() if e.library_doc.source == p.source):
                invalidate = True
                break

        if invalidate:
            self.invalidate()

    def is_initialized(self) -> bool:
        with self._initialize_lock:
            return self._initialized

    def _invalidate(self) -> None:
        self._invalid = True
        self.imports_manager.imports_changed.remove(self._on_imports_changed)
        self.imports_manager.libraries_changed.remove(self._on_libraries_changed)
        self.imports_manager.resources_changed.remove(self._on_resources_changed)
        self.imports_manager.variables_changed.remove(self._on_variables_changed)

    @_logger.call
    def invalidate(self) -> bool:
        with self._initialize_lock:
            if self._invalid:
                return False

            self._invalidate()
        self.has_invalidated(self)
        return True

    @_logger.call
    def get_diagnostics(self) -> List[Diagnostic]:
        self.ensure_initialized()

        self.analyze()

        return self._diagnostics

    @_logger.call
    def get_keyword_references(self) -> Dict[KeywordDoc, Set[Location]]:
        self.ensure_initialized()

        self.analyze()

        return self._keyword_references

    def get_variable_references(
        self,
    ) -> Dict[VariableDefinition, Set[Location]]:
        self.ensure_initialized()

        self.analyze()

        return self._variable_references

    def get_local_variable_assignments(
        self,
    ) -> Dict[VariableDefinition, Set[Range]]:
        self.ensure_initialized()

        self.analyze()

        return self._local_variable_assignments

    def get_namespace_references(self) -> Dict[LibraryEntry, Set[Location]]:
        self.ensure_initialized()

        self.analyze()

        return self._namespace_references

    def get_import_entries(self) -> Dict[Import, LibraryEntry]:
        self.ensure_initialized()

        return self._import_entries

    def get_libraries(self) -> Dict[str, LibraryEntry]:
        self.ensure_initialized()

        return self._libraries

    def get_namespaces(self) -> Dict[KeywordMatcher, List[LibraryEntry]]:
        self.ensure_initialized()

        if self._namespaces is None:
            self._namespaces = defaultdict(list)

            for v in (self.get_libraries()).values():
                self._namespaces[KeywordMatcher(v.alias or v.name or v.import_name, is_namespace=True)].append(v)
            for v in (self.get_resources()).values():
                self._namespaces[KeywordMatcher(v.alias or v.name or v.import_name, is_namespace=True)].append(v)
        return self._namespaces

    def get_resources(self) -> Dict[str, ResourceEntry]:
        self.ensure_initialized()

        return self._resources

    def get_imported_variables(self) -> Dict[str, VariablesEntry]:
        self.ensure_initialized()

        return self._variables

    @_logger.call
    def get_library_doc(self) -> LibraryDoc:
        with self._library_doc_lock:
            if self._library_doc is None:
                self._library_doc = self.imports_manager.get_libdoc_from_model(
                    self.model,
                    self.source,
                    model_type="RESOURCE",
                    append_model_errors=self.document_type is not None and self.document_type == DocumentType.RESOURCE,
                )

            return self._library_doc

    class DataEntry(NamedTuple):
        libraries: Dict[str, LibraryEntry] = OrderedDict()
        resources: Dict[str, ResourceEntry] = OrderedDict()
        variables: Dict[str, VariablesEntry] = OrderedDict()
        diagnostics: List[Diagnostic] = []
        import_entries: Dict[Import, LibraryEntry] = OrderedDict()
        imported_keywords: Optional[List[KeywordDoc]] = None

    @_logger.call(condition=lambda self: not self._initialized)
    def ensure_initialized(self) -> bool:
        with self._initialize_lock:
            if not self._initialized:

                succeed = False
                try:
                    self._logger.debug(lambda: f"initialize {self.document}")

                    imports = self.get_imports()

                    variables = self.get_suite_variables()

                    self._import_default_libraries(variables)
                    self._import_imports(
                        imports,
                        str(Path(self.source).parent),
                        top_level=True,
                        variables=variables,
                    )

                    self._reset_global_variables()

                    self._initialized = True
                    succeed = True

                except BaseException:
                    if self.document is not None:
                        self.document.remove_data(Namespace)
                        self.document.remove_data(Namespace.DataEntry)

                    self._invalidate()
                    raise

                if succeed:
                    self.has_initialized(self)

        return self._initialized

    @property
    def initialized(self) -> bool:
        return self._initialized

    @property
    def invalid(self) -> bool:
        return self._invalid

    @_logger.call
    def get_imports(self) -> List[Import]:
        if self._imports is None:
            self._imports = ImportVisitor().get(self.source, self.model)

        return self._imports

    @_logger.call
    def get_own_variables(self) -> List[VariableDefinition]:
        with self._own_variables_lock:
            if self._own_variables is None:
                self._own_variables = VariablesVisitor().get(self.source, self.model)

            return self._own_variables

    _builtin_variables: Optional[List[BuiltInVariableDefinition]] = None

    @classmethod
    def get_builtin_variables(cls) -> List[BuiltInVariableDefinition]:
        if cls._builtin_variables is None:
            cls._builtin_variables = [BuiltInVariableDefinition(0, 0, 0, 0, "", n, None) for n in BUILTIN_VARIABLES]

        return cls._builtin_variables

    @_logger.call
    def get_command_line_variables(self) -> List[VariableDefinition]:
        return self.imports_manager.get_command_line_variables()

    def _reset_global_variables(self) -> None:
        with self._global_variables_lock, self._global_variables_dict_lock, self._suite_variables_lock:
            with self._global_resolvable_variables_lock:
                self._global_variables = None
                self._global_variables_dict = None
                self._suite_variables = None
                self._global_resolvable_variables = None

    def get_global_variables(self) -> List[VariableDefinition]:
        with self._global_variables_lock:
            if self._global_variables is None:
                self._global_variables = list(
                    itertools.chain(
                        self.get_command_line_variables(),
                        self.get_own_variables(),
                        *(e.variables for e in self._resources.values()),
                        *(e.variables for e in self._variables.values()),
                        self.get_builtin_variables(),
                    )
                )

            return self._global_variables

    def get_global_variables_dict(self) -> Dict[VariableMatcher, VariableDefinition]:
        with self._global_variables_dict_lock:
            if self._global_variables_dict is None:
                self._global_variables_dict = {m: v for m, v in self.yield_variables()}

            return self._global_variables_dict

    def yield_variables(
        self,
        nodes: Optional[List[ast.AST]] = None,
        position: Optional[Position] = None,
        skip_commandline_variables: bool = False,
        skip_local_variables: bool = False,
        skip_global_variables: bool = False,
    ) -> Iterator[Tuple[VariableMatcher, VariableDefinition]]:
        yielded: Dict[VariableMatcher, VariableDefinition] = {}

        test_or_keyword = None
        test_or_keyword_nodes = None

        if nodes:
            test_or_keyword_nodes = list(
                itertools.dropwhile(
                    lambda v: not isinstance(v, (TestCase, Keyword)),
                    nodes if nodes else [],
                )
            )
            test_or_keyword = test_or_keyword_nodes[0] if test_or_keyword_nodes else None

        in_args = isinstance(test_or_keyword_nodes[-1], Arguments) if test_or_keyword_nodes else False
        only_args = (
            isinstance(test_or_keyword_nodes[-1], (Arguments, Setup, Timeout)) if test_or_keyword_nodes else False
        )

        for var in chain(
            *[
                (
                    (
                        (OnlyArgumentsVisitor if only_args else BlockVariableVisitor)(
                            self,
                            nodes,
                            position,
                            in_args,
                        ).get(test_or_keyword)
                    )
                    if test_or_keyword is not None and not skip_local_variables
                    else []
                )
            ],
            self.get_global_variables() if not skip_global_variables else [],
        ):
            if var.matcher not in yielded:
                if skip_commandline_variables and isinstance(var, CommandLineVariableDefinition):
                    continue

                yielded[var.matcher] = var

                yield var.matcher, var

    def get_suite_variables(self) -> Dict[str, Any]:
        with self._suite_variables_lock:
            vars = {}

            def check_var(var: VariableDefinition) -> bool:
                if var.matcher in vars:
                    return False
                vars[var.matcher] = var

                return var.has_value

            self._suite_variables = {v.name: v.value for v in filter(check_var, self.get_global_variables())}

        return self._suite_variables

    def get_resolvable_variables(
        self,
        nodes: Optional[List[ast.AST]] = None,
        position: Optional[Position] = None,
    ) -> Dict[str, Any]:
        if nodes:
            return {
                v.name: v.value
                for k, v in self.yield_variables(nodes, position, skip_commandline_variables=True)
                if v.has_value
            }

        with self._global_resolvable_variables_lock:
            if self._global_resolvable_variables is None:
                self._global_resolvable_variables = {
                    v.name: v.value
                    for k, v in self.yield_variables(nodes, position, skip_commandline_variables=True)
                    if v.has_value
                }
            return self._global_resolvable_variables

    def get_variable_matchers(
        self,
        nodes: Optional[List[ast.AST]] = None,
        position: Optional[Position] = None,
    ) -> Dict[VariableMatcher, VariableDefinition]:
        self.ensure_initialized()

        return {m: v for m, v in self.yield_variables(nodes, position)}

    @_logger.call
    def find_variable(
        self,
        name: str,
        nodes: Optional[List[ast.AST]] = None,
        position: Optional[Position] = None,
        skip_commandline_variables: bool = False,
        skip_local_variables: bool = False,
        ignore_error: bool = False,
    ) -> Optional[VariableDefinition]:
        self.ensure_initialized()

        if name[:2] == "%{" and name[-1] == "}":
            var_name, _, default_value = name[2:-1].partition("=")
            return EnvironmentVariableDefinition(
                0,
                0,
                0,
                0,
                "",
                f"%{{{var_name}}}",
                None,
                default_value=default_value or None,
            )

        try:
            matcher = VariableMatcher(name)

            for m, v in self.yield_variables(
                nodes,
                position,
                skip_commandline_variables=skip_commandline_variables,
                skip_local_variables=skip_local_variables,
                skip_global_variables=True,
            ):
                if matcher == m:
                    return v

            result = self.get_global_variables_dict().get(matcher, None)
            if matcher is not None:
                return result

        except InvalidVariableError:
            if not ignore_error:
                raise

        return None

    def _import(
        self,
        value: Import,
        variables: Optional[Dict[str, Any]],
        base_dir: str,
        *,
        top_level: bool = False,
        source: Optional[str] = None,
        parent_import: Optional[Import] = None,
        parent_source: Optional[str] = None,
    ) -> Optional[LibraryEntry]:
        result: Optional[LibraryEntry] = None
        try:
            if isinstance(value, LibraryImport):
                if value.name is None:
                    raise NameSpaceError("Library setting requires value.")

                result = self._get_library_entry(
                    value.name,
                    value.args,
                    value.alias,
                    base_dir,
                    sentinel=self,
                    variables=variables,
                )
                result.import_range = value.range
                result.import_source = value.source
                result.alias_range = value.alias_range

                self._import_entries[value] = result

                if (
                    top_level
                    and result.library_doc.errors is None
                    and (len(result.library_doc.keywords) == 0 and not bool(result.library_doc.has_listener))
                ):
                    self.append_diagnostics(
                        range=value.range,
                        message=f"Imported library '{value.name}' contains no keywords.",
                        severity=DiagnosticSeverity.WARNING,
                        source=DIAGNOSTICS_SOURCE_NAME,
                        code=Error.LIBRARY_CONTAINS_NO_KEYWORDS,
                    )
            elif isinstance(value, ResourceImport):
                if value.name is None:
                    raise NameSpaceError("Resource setting requires value.")

                source = self.imports_manager.find_resource(value.name, base_dir, variables=variables)

                if self.source == source:
                    if parent_import:
                        self.append_diagnostics(
                            range=parent_import.range,
                            message="Possible circular import.",
                            severity=DiagnosticSeverity.INFORMATION,
                            source=DIAGNOSTICS_SOURCE_NAME,
                            related_information=(
                                [
                                    DiagnosticRelatedInformation(
                                        location=Location(
                                            str(Uri.from_path(value.source)),
                                            value.range,
                                        ),
                                        message=f"'{Path(self.source).name}' is also imported here.",
                                    )
                                ]
                                if value.source
                                else None
                            ),
                            code=Error.POSSIBLE_CIRCULAR_IMPORT,
                        )
                else:
                    result = self._get_resource_entry(
                        value.name,
                        base_dir,
                        variables=variables,
                    )
                    result.import_range = value.range
                    result.import_source = value.source

                    self._import_entries[value] = result

                    if top_level and (
                        not result.library_doc.errors
                        and top_level
                        and not result.imports
                        and not result.variables
                        and not result.library_doc.keywords
                    ):
                        self.append_diagnostics(
                            range=value.range,
                            message=f"Imported resource file '{value.name}' is empty.",
                            severity=DiagnosticSeverity.WARNING,
                            source=DIAGNOSTICS_SOURCE_NAME,
                            code=Error.RESOURCE_EMPTY,
                        )

            elif isinstance(value, VariablesImport):
                if value.name is None:
                    raise NameSpaceError("Variables setting requires value.")

                result = self._get_variables_entry(
                    value.name,
                    value.args,
                    base_dir,
                    variables=variables,
                )

                result.import_range = value.range
                result.import_source = value.source

                self._import_entries[value] = result
            else:
                raise DiagnosticsError("Unknown import type.")

            if top_level and result is not None:
                if result.library_doc.source is not None and result.library_doc.errors:
                    if any(err.source and Path(err.source).is_absolute() for err in result.library_doc.errors):
                        self.append_diagnostics(
                            range=value.range,
                            message="Import definition contains errors.",
                            severity=DiagnosticSeverity.ERROR,
                            source=DIAGNOSTICS_SOURCE_NAME,
                            related_information=[
                                DiagnosticRelatedInformation(
                                    location=Location(
                                        uri=str(Uri.from_path(err.source)),
                                        range=Range(
                                            start=Position(
                                                line=(
                                                    err.line_no - 1
                                                    if err.line_no is not None
                                                    else max(
                                                        result.library_doc.line_no,
                                                        0,
                                                    )
                                                ),
                                                character=0,
                                            ),
                                            end=Position(
                                                line=(
                                                    err.line_no - 1
                                                    if err.line_no is not None
                                                    else max(
                                                        result.library_doc.line_no,
                                                        0,
                                                    )
                                                ),
                                                character=0,
                                            ),
                                        ),
                                    ),
                                    message=err.message,
                                )
                                for err in result.library_doc.errors
                                if err.source is not None
                            ],
                            code=Error.IMPORT_CONTAINS_ERRORS,
                        )
                    for err in filter(
                        lambda e: e.source is None or not Path(e.source).is_absolute(),
                        result.library_doc.errors,
                    ):
                        self.append_diagnostics(
                            range=value.range,
                            message=err.message,
                            severity=DiagnosticSeverity.ERROR,
                            source=DIAGNOSTICS_SOURCE_NAME,
                            code=err.type_name,
                        )
                elif result.library_doc.errors is not None:
                    for err in result.library_doc.errors:
                        self.append_diagnostics(
                            range=value.range,
                            message=err.message,
                            severity=DiagnosticSeverity.ERROR,
                            source=DIAGNOSTICS_SOURCE_NAME,
                            code=err.type_name,
                        )

        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException as e:
            if top_level:
                self.append_diagnostics(
                    range=value.range,
                    message=str(e),
                    severity=DiagnosticSeverity.ERROR,
                    source=DIAGNOSTICS_SOURCE_NAME,
                    code=type(e).__qualname__,
                )
            elif parent_import is not None:
                self.append_diagnostics(
                    range=parent_import.range,
                    message="Import definition contains errors.",
                    severity=DiagnosticSeverity.ERROR,
                    source=DIAGNOSTICS_SOURCE_NAME,
                    code=Error.IMPORT_CONTAINS_ERRORS,
                    related_information=(
                        (
                            [
                                DiagnosticRelatedInformation(
                                    location=Location(str(Uri.from_path(parent_source)), value.range),
                                    message=str(e),
                                ),
                            ]
                        )
                        if parent_source
                        else None
                    ),
                )
        finally:
            self._reset_global_variables()

        return result

    def _import_imports(
        self,
        imports: Iterable[Import],
        base_dir: str,
        *,
        top_level: bool = False,
        variables: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        parent_import: Optional[Import] = None,
        parent_source: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:

        with self._logger.measure_time(
            lambda: f"loading imports for {self.source if top_level else source}",
            context_name="import",
        ):
            for imp in imports:
                if variables is None:
                    variables = self.get_suite_variables()

                entry = self._import(
                    imp,
                    variables=variables,
                    base_dir=base_dir,
                    top_level=top_level,
                    source=source,
                    parent_import=parent_import,
                    parent_source=parent_source if parent_source else source,
                )

                if entry is not None:
                    if isinstance(entry, ResourceEntry):
                        assert entry.library_doc.source is not None
                        already_imported_resources = next(
                            (e for e in self._resources.values() if e.library_doc.source == entry.library_doc.source),
                            None,
                        )

                        if already_imported_resources is None and entry.library_doc.source != self.source:
                            self._resources[entry.import_name] = entry
                            if entry.variables:
                                variables = self.get_suite_variables()

                            try:
                                variables = self._import_imports(
                                    entry.imports,
                                    str(Path(entry.library_doc.source).parent),
                                    top_level=False,
                                    variables=variables,
                                    source=entry.library_doc.source,
                                    parent_import=imp if top_level else parent_import,
                                    parent_source=parent_source if top_level else source,
                                )
                            except (SystemExit, KeyboardInterrupt):
                                raise
                            except BaseException as e:
                                if top_level:
                                    self.append_diagnostics(
                                        range=entry.import_range,
                                        message=str(e) or type(entry).__name__,
                                        severity=DiagnosticSeverity.ERROR,
                                        source=DIAGNOSTICS_SOURCE_NAME,
                                        code=type(e).__qualname__,
                                    )
                        elif top_level:
                            if entry.library_doc.source == self.source:
                                self.append_diagnostics(
                                    range=entry.import_range,
                                    message="Recursive resource import.",
                                    severity=DiagnosticSeverity.INFORMATION,
                                    source=DIAGNOSTICS_SOURCE_NAME,
                                    code=Error.RECURSIVE_IMPORT,
                                )
                            elif (
                                already_imported_resources is not None and already_imported_resources.library_doc.source
                            ):
                                self.append_diagnostics(
                                    range=entry.import_range,
                                    message=f"Resource {entry} already imported.",
                                    severity=DiagnosticSeverity.INFORMATION,
                                    source=DIAGNOSTICS_SOURCE_NAME,
                                    related_information=(
                                        [
                                            DiagnosticRelatedInformation(
                                                location=Location(
                                                    uri=str(Uri.from_path(already_imported_resources.import_source)),
                                                    range=already_imported_resources.import_range,
                                                ),
                                                message="",
                                            )
                                        ]
                                        if already_imported_resources.import_source
                                        else None
                                    ),
                                    code=Error.RESOURCE_ALREADY_IMPORTED,
                                )

                    elif isinstance(entry, VariablesEntry):
                        already_imported_variables = next(
                            (
                                e
                                for e in self._variables.values()
                                if e.library_doc.source == entry.library_doc.source
                                and e.alias == entry.alias
                                and e.args == entry.args
                            ),
                            None,
                        )
                        if (
                            already_imported_variables is None
                            and entry.library_doc is not None
                            and entry.library_doc.source_or_origin
                        ):
                            self._variables[entry.library_doc.source_or_origin] = entry
                            if entry.variables:
                                variables = self.get_suite_variables()
                        elif top_level and already_imported_variables and already_imported_variables.library_doc.source:
                            self.append_diagnostics(
                                range=entry.import_range,
                                message=f'Variables "{entry}" already imported.',
                                severity=DiagnosticSeverity.INFORMATION,
                                source=DIAGNOSTICS_SOURCE_NAME,
                                related_information=(
                                    [
                                        DiagnosticRelatedInformation(
                                            location=Location(
                                                uri=str(Uri.from_path(already_imported_variables.import_source)),
                                                range=already_imported_variables.import_range,
                                            ),
                                            message="",
                                        )
                                    ]
                                    if already_imported_variables.import_source
                                    else None
                                ),
                                code=Error.VARIABLES_ALREADY_IMPORTED,
                            )

                    elif isinstance(entry, LibraryEntry):
                        if top_level and entry.name == BUILTIN_LIBRARY_NAME and entry.alias is None:
                            self.append_diagnostics(
                                range=entry.import_range,
                                message=f'Library "{entry}" is not imported,'
                                ' because it would override the "BuiltIn" library.',
                                severity=DiagnosticSeverity.INFORMATION,
                                source=DIAGNOSTICS_SOURCE_NAME,
                                related_information=(
                                    [
                                        DiagnosticRelatedInformation(
                                            location=Location(
                                                uri=str(Uri.from_path(entry.import_source)),
                                                range=entry.import_range,
                                            ),
                                            message="",
                                        )
                                    ]
                                    if entry.import_source
                                    else None
                                ),
                                code=Error.LIBRARY_OVERRIDES_BUILTIN,
                            )
                            continue

                        already_imported_library = next(
                            (
                                e
                                for e in self._libraries.values()
                                if e.library_doc.source == entry.library_doc.source
                                and e.library_doc.member_name == entry.library_doc.member_name
                                and e.alias == entry.alias
                                and e.args == entry.args
                            ),
                            None,
                        )
                        if (
                            already_imported_library is None
                            and (entry.alias or entry.name or entry.import_name) not in self._libraries
                        ):
                            self._libraries[entry.alias or entry.name or entry.import_name] = entry
                        elif top_level and already_imported_library and already_imported_library.library_doc.source:
                            self.append_diagnostics(
                                range=entry.import_range,
                                message=f'Library "{entry}" already imported.',
                                severity=DiagnosticSeverity.INFORMATION,
                                source=DIAGNOSTICS_SOURCE_NAME,
                                related_information=(
                                    [
                                        DiagnosticRelatedInformation(
                                            location=Location(
                                                uri=str(Uri.from_path(already_imported_library.import_source)),
                                                range=already_imported_library.import_range,
                                            ),
                                            message="",
                                        )
                                    ]
                                    if already_imported_library.import_source
                                    else None
                                ),
                                code=Error.LIBRARY_ALREADY_IMPORTED,
                            )

        return variables

    def _import_lib(self, library: str, variables: Optional[Dict[str, Any]] = None) -> Optional[LibraryEntry]:
        try:
            return self._get_library_entry(
                library,
                (),
                None,
                str(Path(self.source).parent),
                is_default_library=True,
                variables=variables,
            )
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException as e:
            self.append_diagnostics(
                range=Range.zero(),
                message=f"Can't import default library '{library}': {str(e) or type(e).__name__}",
                severity=DiagnosticSeverity.ERROR,
                source="Robot",
                code=type(e).__qualname__,
            )
            return None

    def _import_default_libraries(self, variables: Optional[Dict[str, Any]] = None) -> None:

        with self._logger.measure_time(lambda: f"importing default libraries for {self.source}", context_name="import"):
            if variables is None:
                variables = self.get_suite_variables()

            for library in DEFAULT_LIBRARIES:
                e = self._import_lib(library, variables)
                if e is not None:
                    self._libraries[e.alias or e.name or e.import_name] = e

    @_logger.call
    def _get_library_entry(
        self,
        name: str,
        args: Tuple[Any, ...],
        alias: Optional[str],
        base_dir: str,
        *,
        is_default_library: bool = False,
        sentinel: Any = None,
        variables: Optional[Dict[str, Any]] = None,
    ) -> LibraryEntry:
        if variables is None:
            variables = self.get_suite_variables()

        library_doc = self.imports_manager.get_libdoc_for_library_import(
            name,
            args,
            base_dir=base_dir,
            sentinel=None if is_default_library else sentinel,
            variables=variables,
        )

        return LibraryEntry(
            name=library_doc.name,
            import_name=name,
            library_doc=library_doc,
            args=args,
            alias=alias,
        )

    @_logger.call
    def get_imported_library_libdoc(
        self, name: str, args: Tuple[str, ...] = (), alias: Optional[str] = None
    ) -> Optional[LibraryDoc]:
        self.ensure_initialized()

        return next(
            (
                v.library_doc
                for e, v in self._import_entries.items()
                if isinstance(e, LibraryImport) and v.import_name == name and v.args == args and v.alias == alias
            ),
            None,
        )

    @_logger.call
    def _get_resource_entry(
        self,
        name: str,
        base_dir: str,
        *,
        variables: Optional[Dict[str, Any]] = None,
    ) -> ResourceEntry:
        if variables is None:
            variables = self.get_suite_variables()

        (namespace, library_doc) = self.imports_manager.get_namespace_and_libdoc_for_resource_import(
            name, base_dir, sentinel=self, variables=variables
        )

        return ResourceEntry(
            name=library_doc.name,
            import_name=name,
            library_doc=library_doc,
            imports=namespace.get_imports(),
            variables=namespace.get_own_variables(),
        )

    @_logger.call
    def get_imported_resource_libdoc(self, name: str) -> Optional[LibraryDoc]:
        self.ensure_initialized()

        return next(
            (
                v.library_doc
                for e, v in self._import_entries.items()
                if isinstance(e, ResourceImport) and v.import_name == name
            ),
            None,
        )

    @_logger.call
    def _get_variables_entry(
        self,
        name: str,
        args: Tuple[Any, ...],
        base_dir: str,
        *,
        variables: Optional[Dict[str, Any]] = None,
    ) -> VariablesEntry:
        if variables is None:
            variables = self.get_suite_variables()

        library_doc = self.imports_manager.get_libdoc_for_variables_import(
            name,
            args,
            base_dir=base_dir,
            sentinel=self,
            variables=variables,
        )

        return VariablesEntry(
            name=library_doc.name,
            import_name=name,
            library_doc=library_doc,
            args=args,
            variables=library_doc.variables,
        )

    @_logger.call
    def get_imported_variables_libdoc(self, name: str, args: Tuple[str, ...] = ()) -> Optional[LibraryDoc]:
        self.ensure_initialized()

        return next(
            (
                v.library_doc
                for e, v in self._import_entries.items()
                if isinstance(e, VariablesImport) and v.import_name == name and v.args == args
            ),
            None,
        )

    def get_imported_keywords(self) -> List[KeywordDoc]:
        with self._imported_keywords_lock:
            if self._imported_keywords is None:
                self._imported_keywords = list(
                    itertools.chain(
                        *(e.library_doc.keywords for e in self._libraries.values()),
                        *(e.library_doc.keywords for e in self._resources.values()),
                    )
                )

            return self._imported_keywords

    @_logger.call
    def iter_all_keywords(self) -> Iterator[KeywordDoc]:
        import itertools

        libdoc = self.get_library_doc()

        for doc in itertools.chain(
            self.get_imported_keywords(),
            libdoc.keywords if libdoc is not None else [],
        ):
            yield doc

    @_logger.call
    def get_keywords(self) -> List[KeywordDoc]:
        with self._keywords_lock:
            if self._keywords is None:
                current_time = time.monotonic()
                self._logger.debug("start collecting keywords")
                try:
                    i = 0

                    self.ensure_initialized()

                    result: Dict[KeywordMatcher, KeywordDoc] = {}

                    for doc in self.iter_all_keywords():
                        i += 1
                        result[doc.matcher] = doc

                    self._keywords = list(result.values())
                except BaseException:
                    self._logger.debug("Canceled collecting keywords ")
                    raise
                else:
                    self._logger.debug(
                        lambda: f"end collecting {len(self._keywords) if self._keywords else 0}"
                        f" keywords in {time.monotonic() - current_time}s analyze {i} keywords"
                    )

            return self._keywords

    def append_diagnostics(
        self,
        range: Range,
        message: str,
        severity: Optional[DiagnosticSeverity] = None,
        code: Union[int, str, None] = None,
        code_description: Optional[CodeDescription] = None,
        source: Optional[str] = None,
        tags: Optional[List[DiagnosticTag]] = None,
        related_information: Optional[List[DiagnosticRelatedInformation]] = None,
        data: Optional[Any] = None,
    ) -> None:

        self._diagnostics.append(
            Diagnostic(
                range,
                message,
                severity,
                code,
                code_description,
                source,
                tags,
                related_information,
                data,
            )
        )

    def is_analyzed(self) -> bool:
        with self._analyze_lock:
            return self._analyzed

    @_logger.call(condition=lambda self: not self._analyzed)
    def analyze(self) -> None:
        from .namespace_analyzer import NamespaceAnalyzer

        with self._analyze_lock:
            if not self._analyzed:
                canceled = False

                self.ensure_initialized()

                with self._logger.measure_time(lambda: f"analyzing document {self.source}", context_name="analyze"):
                    try:
                        result = NamespaceAnalyzer(self.model, self, self.create_finder()).run()

                        self._diagnostics += result.diagnostics
                        self._keyword_references = result.keyword_references
                        self._variable_references = result.variable_references
                        self._local_variable_assignments = result.local_variable_assignments
                        self._namespace_references = result.namespace_references

                        lib_doc = self.get_library_doc()

                        if lib_doc.errors is not None:
                            for err in lib_doc.errors:
                                self.append_diagnostics(
                                    range=Range(
                                        start=Position(
                                            line=((err.line_no - 1) if err.line_no is not None else 0),
                                            character=0,
                                        ),
                                        end=Position(
                                            line=((err.line_no - 1) if err.line_no is not None else 0),
                                            character=0,
                                        ),
                                    ),
                                    message=err.message,
                                    severity=DiagnosticSeverity.ERROR,
                                    source=DIAGNOSTICS_SOURCE_NAME,
                                    code=err.type_name,
                                )
                    # TODO: implement CancelationToken
                    except CancelledError:
                        canceled = True
                        self._logger.debug("analyzing canceled")
                        raise
                    finally:
                        self._analyzed = not canceled

                self.has_analysed(self)

    def get_finder(self) -> "KeywordFinder":
        if self._finder is None:
            self._finder = self.create_finder()
        return self._finder

    def create_finder(self) -> "KeywordFinder":
        self.ensure_initialized()
        return KeywordFinder(self, self.get_library_doc())

    @_logger.call(condition=lambda self, name, **kwargs: self._finder is not None and name not in self._finder._cache)
    def find_keyword(
        self,
        name: Optional[str],
        *,
        raise_keyword_error: bool = True,
        handle_bdd_style: bool = True,
    ) -> Optional[KeywordDoc]:
        finder = self._finder if self._finder is not None else self.get_finder()

        return finder.find_keyword(
            name,
            raise_keyword_error=raise_keyword_error,
            handle_bdd_style=handle_bdd_style,
        )


class DiagnosticsEntry(NamedTuple):
    message: str
    severity: DiagnosticSeverity
    code: Optional[str] = None


class CancelSearchError(Exception):
    pass


DEFAULT_BDD_PREFIXES = {"Given ", "When ", "Then ", "And ", "But "}


class KeywordFinder:
    def __init__(self, namespace: Namespace, library_doc: LibraryDoc) -> None:
        self.namespace = namespace
        self.self_library_doc = library_doc

        self.diagnostics: List[DiagnosticsEntry] = []
        self.multiple_keywords_result: Optional[List[KeywordDoc]] = None
        self._cache: Dict[
            Tuple[Optional[str], bool],
            Tuple[
                Optional[KeywordDoc],
                List[DiagnosticsEntry],
                Optional[List[KeywordDoc]],
            ],
        ] = {}
        self.handle_bdd_style = True
        self._all_keywords: Optional[List[LibraryEntry]] = None
        self._resource_keywords: Optional[List[ResourceEntry]] = None
        self._library_keywords: Optional[List[LibraryEntry]] = None

    def reset_diagnostics(self) -> None:
        self.diagnostics = []
        self.multiple_keywords_result = None

    def find_keyword(
        self,
        name: Optional[str],
        *,
        raise_keyword_error: bool = False,
        handle_bdd_style: bool = True,
    ) -> Optional[KeywordDoc]:
        try:
            self.reset_diagnostics()

            self.handle_bdd_style = handle_bdd_style

            cached = self._cache.get((name, self.handle_bdd_style), None)

            if cached is not None:
                self.diagnostics = cached[1]
                self.multiple_keywords_result = cached[2]
                return cached[0]

            try:
                result = self._find_keyword(name)
                if result is None:
                    self.diagnostics.append(
                        DiagnosticsEntry(
                            f"No keyword with name '{name}' found.",
                            DiagnosticSeverity.ERROR,
                            Error.KEYWORD_NOT_FOUND,
                        )
                    )
            except KeywordError as e:
                if e.multiple_keywords:
                    self._add_to_multiple_keywords_result(e.multiple_keywords)

                if raise_keyword_error:
                    raise

                result = None
                self.diagnostics.append(DiagnosticsEntry(str(e), DiagnosticSeverity.ERROR, Error.KEYWORD_ERROR))

            self._cache[(name, self.handle_bdd_style)] = (
                result,
                self.diagnostics,
                self.multiple_keywords_result,
            )

            return result
        except CancelSearchError:
            return None

    def _find_keyword(self, name: Optional[str]) -> Optional[KeywordDoc]:
        if not name:
            self.diagnostics.append(
                DiagnosticsEntry(
                    "Keyword name cannot be empty.",
                    DiagnosticSeverity.ERROR,
                    Error.KEYWORD_ERROR,
                )
            )
            raise CancelSearchError
        if not isinstance(name, str):
            self.diagnostics.append(  # type: ignore
                DiagnosticsEntry(
                    "Keyword name must be a string.",
                    DiagnosticSeverity.ERROR,
                    Error.KEYWORD_ERROR,
                )
            )
            raise CancelSearchError

        result = self._get_keyword_from_self(name)
        if not result and "." in name:
            result = self._get_explicit_keyword(name)

        if not result:
            result = self._get_implicit_keyword(name)

        if not result and self.handle_bdd_style:
            return self._get_bdd_style_keyword(name)

        return result

    def _get_keyword_from_self(self, name: str) -> Optional[KeywordDoc]:
        if get_robot_version() >= (6, 0):
            found: List[Tuple[Optional[LibraryEntry], KeywordDoc]] = [
                (None, v) for v in self.self_library_doc.keywords.get_all(name)
            ]
            if len(found) > 1:
                found = self._select_best_matches(found)
                if len(found) > 1:
                    self.diagnostics.append(
                        DiagnosticsEntry(
                            self._create_multiple_keywords_found_message(name, found, implicit=False),
                            DiagnosticSeverity.ERROR,
                            Error.MULTIPLE_KEYWORDS,
                        )
                    )
                    raise CancelSearchError

            if len(found) == 1:
                # TODO warning if keyword found is defined in resource and suite
                return found[0][1]

            return None

        try:
            return self.self_library_doc.keywords.get(name, None)
        except KeywordError as e:
            self.diagnostics.append(DiagnosticsEntry(str(e), DiagnosticSeverity.ERROR, Error.KEYWORD_ERROR))
            raise CancelSearchError from e

    def _yield_owner_and_kw_names(self, full_name: str) -> Iterator[Tuple[str, ...]]:
        tokens = full_name.split(".")
        for i in range(1, len(tokens)):
            yield ".".join(tokens[:i]), ".".join(tokens[i:])

    def _get_explicit_keyword(self, name: str) -> Optional[KeywordDoc]:
        found: List[Tuple[Optional[LibraryEntry], KeywordDoc]] = []
        for owner_name, kw_name in self._yield_owner_and_kw_names(name):
            found.extend(self.find_keywords(owner_name, kw_name))

        if get_robot_version() >= (6, 0) and len(found) > 1:
            found = self._select_best_matches(found)

        if len(found) > 1:
            self.diagnostics.append(
                DiagnosticsEntry(
                    self._create_multiple_keywords_found_message(name, found, implicit=False),
                    DiagnosticSeverity.ERROR,
                    Error.MULTIPLE_KEYWORDS,
                )
            )
            raise CancelSearchError

        return found[0][1] if found else None

    def find_keywords(self, owner_name: str, name: str) -> List[Tuple[LibraryEntry, KeywordDoc]]:
        if self._all_keywords is None:
            self._all_keywords = list(
                chain(
                    self.namespace._libraries.values(),
                    self.namespace._resources.values(),
                )
            )

        if get_robot_version() >= (6, 0):
            result: List[Tuple[LibraryEntry, KeywordDoc]] = []
            for v in self._all_keywords:
                if eq_namespace(v.alias or v.name, owner_name):
                    result.extend((v, kw) for kw in v.library_doc.keywords.get_all(name))
            return result

        result = []
        for v in self._all_keywords:
            if eq_namespace(v.alias or v.name, owner_name):
                kw = v.library_doc.keywords.get(name, None)
                if kw is not None:
                    result.append((v, kw))
        return result

    def _add_to_multiple_keywords_result(self, kw: Iterable[KeywordDoc]) -> None:
        if self.multiple_keywords_result is None:
            self.multiple_keywords_result = list(kw)
        else:
            self.multiple_keywords_result.extend(kw)

    def _create_multiple_keywords_found_message(
        self,
        name: str,
        found: Sequence[Tuple[Optional[LibraryEntry], KeywordDoc]],
        implicit: bool = True,
    ) -> str:
        self._add_to_multiple_keywords_result([k for _, k in found])

        if any(e[1].is_embedded for e in found):
            error = f"Multiple keywords matching name '{name}' found"
        else:
            error = f"Multiple keywords with name '{name}' found"

            if implicit:
                error += ". Give the full name of the keyword you want to use"

        names = sorted(f"{e[1].name if e[0] is None else f'{e[0].alias or e[0].name}.{e[1].name}'}" for e in found)
        return "\n    ".join([f"{error}:", *names])

    def _get_implicit_keyword(self, name: str) -> Optional[KeywordDoc]:
        result = self._get_keyword_from_resource_files(name)
        if not result:
            return self._get_keyword_from_libraries(name)
        return result

    def _prioritize_same_file_or_public(
        self, entries: List[Tuple[Optional[LibraryEntry], KeywordDoc]]
    ) -> List[Tuple[Optional[LibraryEntry], KeywordDoc]]:
        matches = [h for h in entries if h[1].source == self.namespace.source]
        if matches:
            return matches

        matches = [handler for handler in entries if not handler[1].is_private()]

        return matches or entries

    def _select_best_matches(
        self, entries: List[Tuple[Optional[LibraryEntry], KeywordDoc]]
    ) -> List[Tuple[Optional[LibraryEntry], KeywordDoc]]:
        normal = [hand for hand in entries if not hand[1].is_embedded]
        if normal:
            return normal

        matches = [hand for hand in entries if not self._is_worse_match_than_others(hand, entries)]
        return matches or entries

    def _is_worse_match_than_others(
        self,
        candidate: Tuple[Optional[LibraryEntry], KeywordDoc],
        alternatives: List[Tuple[Optional[LibraryEntry], KeywordDoc]],
    ) -> bool:
        for other in alternatives:
            if (
                candidate[1] is not other[1]
                and self._is_better_match(other, candidate)
                and not self._is_better_match(candidate, other)
            ):
                return True
        return False

    def _is_better_match(
        self,
        candidate: Tuple[Optional[LibraryEntry], KeywordDoc],
        other: Tuple[Optional[LibraryEntry], KeywordDoc],
    ) -> bool:
        return (
            other[1].matcher.embedded_arguments.match(candidate[1].name) is not None
            and candidate[1].matcher.embedded_arguments.match(other[1].name) is None
        )

    def _get_keyword_from_resource_files(self, name: str) -> Optional[KeywordDoc]:
        if self._resource_keywords is None:
            self._resource_keywords = list(chain(self.namespace._resources.values()))

        if get_robot_version() >= (6, 0):
            found: List[Tuple[Optional[LibraryEntry], KeywordDoc]] = []
            for v in self._resource_keywords:
                r = v.library_doc.keywords.get_all(name)
                if r:
                    found.extend([(v, k) for k in r])
        else:
            found = []
            for k in self._resource_keywords:
                s = k.library_doc.keywords.get(name, None)
                if s is not None:
                    found.append((k, s))

        if not found:
            return None

        if get_robot_version() >= (6, 0):
            if len(found) > 1:
                found = self._prioritize_same_file_or_public(found)

                if len(found) > 1:
                    found = self._select_best_matches(found)

                    if len(found) > 1:
                        found = self._get_keyword_based_on_search_order(found)

        else:
            if len(found) > 1:
                found = self._get_keyword_based_on_search_order(found)

        if len(found) == 1:
            return found[0][1]

        self.diagnostics.append(
            DiagnosticsEntry(
                self._create_multiple_keywords_found_message(name, found),
                DiagnosticSeverity.ERROR,
                Error.MULTIPLE_KEYWORDS,
            )
        )
        raise CancelSearchError

    def _get_keyword_based_on_search_order(
        self, entries: List[Tuple[Optional[LibraryEntry], KeywordDoc]]
    ) -> List[Tuple[Optional[LibraryEntry], KeywordDoc]]:
        for libname in self.namespace.search_order:
            for e in entries:
                if e[0] is not None and eq_namespace(libname, e[0].alias or e[0].name):
                    return [e]

        return entries

    def _get_keyword_from_libraries(self, name: str) -> Optional[KeywordDoc]:
        if self._library_keywords is None:
            self._library_keywords = list(chain(self.namespace._libraries.values()))

        if get_robot_version() >= (6, 0):
            found: List[Tuple[Optional[LibraryEntry], KeywordDoc]] = []
            for v in self._library_keywords:
                r = v.library_doc.keywords.get_all(name)
                if r:
                    found.extend([(v, k) for k in r])
        else:
            found = []

            for k in self._library_keywords:
                s = k.library_doc.keywords.get(name, None)
                if s is not None:
                    found.append((k, s))

        if not found:
            return None

        if get_robot_version() >= (6, 0):
            if len(found) > 1:
                found = self._select_best_matches(found)
                if len(found) > 1:
                    found = self._get_keyword_based_on_search_order(found)
        else:
            if len(found) > 1:
                found = self._get_keyword_based_on_search_order(found)
            if len(found) == 2:
                found = self._filter_stdlib_runner(*found)

        if len(found) == 1:
            return found[0][1]

        self.diagnostics.append(
            DiagnosticsEntry(
                self._create_multiple_keywords_found_message(name, found),
                DiagnosticSeverity.ERROR,
                Error.MULTIPLE_KEYWORDS,
            )
        )
        raise CancelSearchError

    def _filter_stdlib_runner(
        self,
        entry1: Tuple[Optional[LibraryEntry], KeywordDoc],
        entry2: Tuple[Optional[LibraryEntry], KeywordDoc],
    ) -> List[Tuple[Optional[LibraryEntry], KeywordDoc]]:
        stdlibs_without_remote = STDLIBS - {"Remote"}
        if entry1[0] is not None and entry1[0].name in stdlibs_without_remote:
            standard, custom = entry1, entry2
        elif entry2[0] is not None and entry2[0].name in stdlibs_without_remote:
            standard, custom = entry2, entry1
        else:
            return [entry1, entry2]

        self.diagnostics.append(
            DiagnosticsEntry(
                self._create_custom_and_standard_keyword_conflict_warning_message(custom, standard),
                DiagnosticSeverity.WARNING,
                Error.CONFLICTING_LIBRARY_KEYWORDS,
            )
        )

        return [custom]

    def _create_custom_and_standard_keyword_conflict_warning_message(
        self,
        custom: Tuple[Optional[LibraryEntry], KeywordDoc],
        standard: Tuple[Optional[LibraryEntry], KeywordDoc],
    ) -> str:
        custom_with_name = standard_with_name = ""
        if custom[0] is not None and custom[0].alias is not None:
            custom_with_name = " imported as '%s'" % custom[0].alias
        if standard[0] is not None and standard[0].alias is not None:
            standard_with_name = " imported as '%s'" % standard[0].alias
        return (
            f"Keyword '{standard[1].name}' found both from a custom test library "
            f"'{'' if custom[0] is None else custom[0].name}'{custom_with_name} "
            f"and a standard library '{standard[1].name}'{standard_with_name}. "
            f"The custom keyword is used. To select explicitly, and to get "
            f"rid of this warning, use either "
            f"'{'' if custom[0] is None else custom[0].alias or custom[0].name}.{custom[1].name}' "
            f"or '{'' if standard[0] is None else standard[0].alias or standard[0].name}.{standard[1].name}'."
        )

    def _get_bdd_style_keyword(self, name: str) -> Optional[KeywordDoc]:
        if get_robot_version() < (6, 0):
            lower = name.lower()
            for prefix in ["given ", "when ", "then ", "and ", "but "]:
                if lower.startswith(prefix):
                    return self._find_keyword(name[len(prefix) :])
            return None

        parts = name.split()
        if len(parts) < 2:
            return None
        for index in range(1, len(parts)):
            prefix = " ".join(parts[:index]).title()
            if prefix.title() in (
                self.namespace.languages.bdd_prefixes if self.namespace.languages is not None else DEFAULT_BDD_PREFIXES
            ):
                return self._find_keyword(" ".join(parts[index:]))
        return None
