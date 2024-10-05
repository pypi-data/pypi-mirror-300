from abc import ABC, abstractmethod
from pathlib import Path

from ..compat import Any, Callable, Self
from .source import Source
from .result import Result
from .utils import _to_bool


class Filler(ABC):
    @abstractmethod
    def fill(self, source: Source, val: Result) -> Result:
        return None


class DefaultFiller(Filler):
    def __init__(self, default: Any):
        self.default = default

    def fill(self, source: Source, val: Result) -> Result:
        if val.is_err():
            return val.then_ok(self.default)
        else:
            return val


class SourceFiller(Filler):
    def __init__(self, args, override = False):
        self.args = args
        self.override = override

    def fill(self, source: Source, val: Result) -> Result:
        for i, arg in enumerate(self.args):
            if not isinstance(arg, Filler):
                continue
            arg_val = arg.fill(source, val)
            if arg_val.is_err():
                return val.then(arg_val)
            else:
                self.args[i] = arg_val.get()

        if val.is_err():
            return val.then(source.get(self.args))
        if self.override:
            return val.then_try(source.get(self.args))
        else:
            return val


class ApplyFiller(Filler):
    def __init__(
        self,
        func: Callable[[Any],Any],
        name = None,
        must_apply = True,
        print_traceback = False
    ):
        self.func = func
        self.name = "" if name is None else name
        self.must_apply = must_apply
        self.print_traceback = print_traceback

    def _err_message(self, value: Result, extra = ""):
        return f"Cannot apply function \"{self.name}\" to \"{value}\"{extra}"

    def _exc_message(self, value: Result, exception: Exception):
        exc_str = f": {exception}"
        if self.print_traceback:
            exc_str = f":\n{traceback.format_exc()}"

        return self._err_message(value, extra = exc_str)

    def fill(self, source: Source, val: Result) -> Result:
        if val.is_err():
            return val.then_err(self._err_message(val))

        try:
            return val.then_ok(self.func(val.get()))
        except Exception as e:
            msg = self._exc_message(val, e)
            if self.must_apply:
                return val.then_err(msg)
            else:
                return val.then_benign_err(msg)


class Try(Filler):
    def __init__(self, fillers: list[Filler]):
        self._fillers = fillers

    def fill(self, source: Source, val: Result) -> Result:
        for filler in self._fillers:
            val = filler.fill(source, val)
        return val

    def append(self, filler: Filler) -> Self:
        self._fillers.append(filler)
        return self

    @classmethod
    def source(cls, *args, prefix = None) -> Self:
        if prefix is None:
            args = list(args)
        else:
            args = [prefix] + list(args)

        return Try([SourceFiller(args)])

    @classmethod
    def cfgmap(cls, *paths: str|Path) -> Self:
        return cls.source(*paths, prefix = "configmaps")

    @classmethod
    def secret(cls, *paths: str|Path) -> Self:
        return cls.source(*paths, prefix = "secrets")

    def or_source(self, *args, prefix = None) -> Self:
        return self.append(Try.source(*args, prefix = prefix))

    def or_cfgmap(self, *paths: str|Path) -> Self:
        return self.or_source(*paths, prefix = "configmaps")

    def or_secret(self, *paths: str|Path) -> Self:
        return self.or_source(*paths, prefix = "secrets")

    def default(self, default: Any) -> Self:
        return self.append(DefaultFiller(default))

    def apply(self, func: Callable[[Any],Any], *args, **kwargs) -> Self:
        return self.append(ApplyFiller(func, *args, **kwargs))

    def join(self, suffix: str, **kwargs) -> Self:
        return self.apply(
            func = lambda s: s + suffix,
            name = f"join with {suffix}",
            **kwargs
        )

    def to_int(self, **kwargs) -> Self:
        return self.apply(
            func = int,
            name = "convert to int",
            **kwargs
        )

    def to_path(self, **kwargs) -> Self:
        return self.apply(
            func = Path,
            name = "convert to pathlib.Path",
            **kwargs
        )

    def to_bool(self, **kwargs) -> Self:
        return self.apply(
            func = _to_bool,
            name = "convert to bool",
            **kwargs
        )
