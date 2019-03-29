import gzip as _gzip
import typing as _typing

from stream.typing import (
    Function as _Function,
)
from stream.util.io import (
    BytesIterableAsIO as _BytesIO,
)
from .each import (
    apply_each as _apply_each,
)

decode: _Function[bytes, str] = _apply_each(bytes.decode, encoding='utf-8')


def un_gzip(iterable: _typing.Iterable[bytes]) -> _typing.Iterator[str]:
    """
    Unzip a gzip byte stream into str, and split by lines.
    """
    readable = _BytesIO(iterable)
    with _gzip.open(readable) as f:
        yield from f
