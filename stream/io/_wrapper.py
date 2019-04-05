import typing as _typing

from . import (
    File as _File,
)

FileType = _typing.TypeVar('FileType', bound=_File)


def wrapper_class(
        file_class: _typing.Type[FileType],
        wrapped_class: _typing.Union[_typing.Type, _typing.Callable],
) -> _typing.Type[FileType]:
    class WrapperClass(file_class):
        def __init__(self, *args, **kwargs):
            self._wrapped = wrapped_class(*args, **kwargs)

        def __enter__(self) -> 'WrapperClass':
            self._wrapped.__enter__()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return self._wrapped.__exit__()

        def __next__(self):
            return next(self._wrapped)

        def __iter__(self):
            return iter(self._wrapped)

        def __getattribute__(self, name: str):
            """
            1. If in __dict__, return it;
            2. If defined in subclasses of file_class, use it;
            3. Try get attr of wrapped object;
            4. Use definition from file_class.
            """
            if name == '__dict__':
                return object.__getattribute__(self, name)
            if name in self.__dict__:
                # is a variable
                return object.__getattribute__(self, name)

            try:
                this_attr = object.__getattribute__(self, name)
            except (AttributeError, NotImplementedError) as e:
                return getattr(self._wrapped, name)

            if name in self.__dict__:
                # cached_property
                return this_attr

            try:
                super_attr = super(WrapperClass, self).__getattribute__(name)
            except (AttributeError, NotImplementedError):
                return this_attr

            if this_attr != super_attr:
                return this_attr

            try:
                return getattr(self._wrapped, name)
            except AttributeError:
                return this_attr

    return WrapperClass
