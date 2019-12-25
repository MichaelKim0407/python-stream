import typing as _typing

from .typing import (
    Function as _Function,
    Call as _Call,
    T_co as _T_co,
    V_co as _V_co,
    V as _V,
)


class Stream(_typing.Iterator[_T_co]):
    def __next__(self) -> _T_co:
        raise NotImplementedError  # pragma: no cover

    def __or__(self, other: _Function[_T_co, _V_co]) -> 'Stream[_V_co]':
        """
        Override the `|` operator.
        :param other: An iterator function, see `functional` package.
        """
        result = other(self)
        if isinstance(result, Stream):
            return result
        else:
            return IterStream(result)

    def __gt__(self, other: _Call[_T_co, _V]) -> _V:
        """
        Override the `>` operator.
        Call `other(self)`.
        """
        return other(self)

    def __call__(self) -> None:
        """
        Go through the stream with a for loop without returning anything.
        """
        for item in self:
            pass


class BaseIterStream(Stream[_T_co]):
    def __init__(self):
        self.__iter: _typing.Iterator[_T_co] = None

    def _iterable(self) -> _typing.Iterable[_T_co]:
        raise NotImplementedError  # pragma: no cover

    def __next__(self) -> _T_co:
        if self.__iter is None:
            self.__iter = iter(self._iterable())
        return next(self.__iter)


class IterStream(BaseIterStream[_T_co]):
    def __init__(self, iterable: _typing.Iterable):
        super().__init__()
        self.__iterable = iterable

    def _iterable(self) -> _typing.Iterable[_T_co]:
        return self.__iterable
