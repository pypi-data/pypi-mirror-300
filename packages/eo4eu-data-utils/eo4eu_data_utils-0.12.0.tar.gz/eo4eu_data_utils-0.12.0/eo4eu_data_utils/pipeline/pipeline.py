from logging import Logger
from pathlib import Path

from ..compat import Self, Callable, Any
from .interface import Data, Action, ActionContext
from .drivers import Driver, LocalDriver
from .actions import (
    Log,
    Apply,
    Source,
    Filter,
    Switch,
    Branch,
    FileOp,
    Collect,
    StatefulAction,
    basic_dst_func,
    basic_put_func,
    move_put_func,
    unpack_put_func,
)


class Pipeline(Action):
    def __init__(
        self,
        logger: Logger|None = None,
        summary: Logger|None = None,
        selector: Callable[[Path],Any]|None = None,
        context: ActionContext|None = None,
    ):
        if all([
            context is None,
            logger is not None,
            summary is not None
        ]):
            context = ActionContext(
                logger = logger,
                summary = summary,
                selector = selector
            )

        self._context = context
        self._actions = []

    def execute(self, input: Data, context: ActionContext) -> Data:
        if self._context is None and context is not None:
            self._context = context

        result = input.copy()
        for action in self._actions:
            result = action.execute(result, self._context)
        return result

    def exec(self) -> Data:
        return self.execute(Data.empty(), self._context)

    def then(self, action: Action, context: ActionContext|None = None) -> Self:
        if context is None:
            self._actions.append(action)
        else:
            self._actions.append(StatefulAction(action, context))
        return self

    def apply(self, func: Callable[[Data],Data]) -> Self:
        return self.then(
            action = Apply(func = func),
            context = context
        )

    def source(
        self,
        driver: Driver,
        cwdir: str|Path = "",
        context: ActionContext|None = None
    ) -> Self:
        return self.then(
            action = Source(driver = driver, cwdir = Path(cwdir)),
            context = context
        )

    def filter(
        self,
        *predicates: Any,
        context: ActionContext|None = None
    ) -> Self:
        return self.then(
            action = Filter(predicates = list(predicates)),
            context = context
        )

    def switch(
        self,
        cases: dict[Any,Action]|list[tuple[Any,Action]],
        otherwise: Action|None = None,
        context: ActionContext|None = None
    ) -> Self:
        case_tuples = cases
        if isinstance(cases, dict):
            case_tuples = [
                (predicate, action) for predicate, action in cases.items()
            ]
        if otherwise is not None:
            case_tuples.append((lambda path: True, otherwise))

        return self.then(
            action = Switch(case_tuples),
            context = context
        )

    def branch(
        self,
        predicate: Any,
        action: Action,
        context: ActionContext|None = None
    ) -> Self:
        return self.then(
            action = Branch(predicate, action),
            context = context
        )

    def collect(
        self,
        name: str,
        consume: bool = False,
        context: ActionContext|None = None
    ) -> Self:
        return self.then(
            action = Collect(name = name, consume = consume),
            context = context
        )

    def consume(
        self,
        name: str,
        context: ActionContext|None = None
    ) -> Self:
        return self.collect(name = name, consume = True, context = context)

    def log(
        self,
        msg: str|Callable[[Logger,Data],None],
        summary: bool = False,
        context: ActionContext|None = None
    ):
        log_func = msg
        if isinstance(msg, str):
            log_func = lambda logger, data: logger.info(msg)
        return self.then(
            action = Log(log_func = log_func, summary = summary),
            context = context
        )

    def summarize(self,
        msg: str|Callable[[Logger,Data],None],
        context: ActionContext|None = None
    ) -> Self:
        return self.log(msg = msg, summary = True, context = context)

    def put(
        self,
        driver: Driver,
        outdir: str|Path = "",
        cd: bool = False,
        context: ActionContext|None = None
    ) -> Self:
        return self.then(
            action = FileOp(
                driver = driver,
                outdir = Path(outdir),
                names = ("Put", "Putting", "Put"),
                dst_func = basic_dst_func,
                put_func = basic_put_func,
                cd = cd
            ),
            context = context
        )

    def upload(
        self,
        driver: Driver,
        outdir: str|Path = "",
        cd: bool = False,
        context: ActionContext|None = None
    ) -> Self:
        return self.then(
            action = FileOp(
                driver = driver,
                outdir = Path(outdir),
                names = ("Upload", "Uploading", "Uploaded"),
                dst_func = basic_dst_func,
                put_func = basic_put_func,
                cd = cd
            ),
            context = context
        )

    def download(
        self,
        outdir: str|Path = "",
        cd: bool = False,
        context: ActionContext|None = None
    ) -> Self:
        return self.then(
            action = FileOp(
                driver = LocalDriver(Path.cwd()),
                outdir = Path(outdir),
                names = ("Download", "Downloading", "Downloaded"),
                dst_func = basic_dst_func,
                put_func = basic_put_func,
                cd = cd
            ),
            context = context
        )

    def move(
        self,
        outdir: str|Path = "",
        cd: bool = False,
        context: ActionContext|None = None
    ) -> Self:
        return self.then(
            action = FileOp(
                driver = None,
                outdir = Path(outdir),
                names = ("Move", "Moving", "Moved"),
                dst_func = basic_dst_func,
                put_func = move_put_func,
                cd = cd
            ),
            context = context
        )

    def unpack(
        self,
        outdir: str|Path = "",
        cd: bool = False,
        context: ActionContext|None = None
    ) -> Self:
        return self.then(
            action = FileOp(
                driver = None,
                outdir = Path(outdir),
                names = ("Unpack", "Unpacking", "Unpacked"),
                dst_func = basic_dst_func,
                put_func = unpack_put_func,
                cd = cd
            ),
            context = context
        )


def then() -> Pipeline:
    return Pipeline()
