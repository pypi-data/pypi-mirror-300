import json
import logging
from pprint import pformat
from pathlib import Path

from ..compat import Self, Iterator, Any
from .source import (
    Source,
    EnvSource,
    DictSource,
    FileSource,
    CompoundSource,
)
from .filler import Filler
from .result import Result


class Config:
    def __init__(self, **kwargs):
        self._logger = logging.getLogger(__name__)
        self._sources = []
        self._attrs = {}
        for key, val in kwargs.items():
            if isinstance(val, dict):
                val = Config(**val)
            if isinstance(val, self.__class__):
                val.set_logger(self._logger)

            self._attrs[key] = val

    @classmethod
    def from_dict(cls, items: dict) -> Self:
        return Config(**items)

    @classmethod
    def from_json(cls, items: str) -> Self:
        return cls.from_dict(json.loads(items))

    def to_dict(self):
        return {
            key: val.to_dict() if isinstance(val, self.__class__) else val
            for key, val in self.items()
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __getattr__(self, key: str):
        if key[0] == "_":
            return super().__getattr__(key)
        return self._attrs[key]

    def __setattr__(self, key: str, val):
        if key[0] == "_":
            return super().__setattr__(key, val)
        self._attrs[key] = val

    def __getitem__(self, key: str):
        return self._attrs[key]

    def __setitem__(self, key: str, val):
        self._attrs[key] = val

    def __repr__(self) -> str:
        return pformat(self.to_dict())

    def items(self) -> Iterator[tuple[str,Any]]:
        return self._attrs.items()

    def set_logger(self, logger) -> Self:
        self._logger = logger
        return self

    def use_source(self, source: Source) -> Self:
        self._sources.append(source)
        return self

    def use_files(self, root: str|Path = "/") -> Self:
        return self.use_source(FileSource(root))

    def use_env(self) -> Self:
        return self.use_source(EnvSource())

    def use_dict(self, source: dict, **kwargs) -> Self:
        return self.use_source(DictSource(source, **kwargs))

    def use_json(self, source: str, **kwargs) -> Self:
        return self.use_dict(json.loads(source), **kwargs)

    def fill(
        self,
        sources: list[Source]|None = None,
        raise_on_err: bool = False,
        previous_keys: list[str]|None = None
    ) -> Self:
        if sources is None:
            sources = []
        if previous_keys is None:
            previous_keys = []

        all_sources = sources + self._sources
        source = CompoundSource(all_sources)
        for key, val in self.items():
            if isinstance(val, self.__class__):
                self._attrs[key] = val.fill(
                    sources = all_sources,
                    raise_on_err = raise_on_err,
                    previous_keys = previous_keys
                )
            if isinstance(val, Filler):
                filled_val = val.fill(source, Result.none()).log_warnings(self._logger)

                if filled_val.is_ok():
                    self._attrs[key] = filled_val.get()
                else:
                    msg = f"Could not fill {'/'.join(previous_keys + [key])}"
                    if raise_on_err:
                        raise ValueError(msg)
                    else:
                        self._logger.error(msg)
        return self
