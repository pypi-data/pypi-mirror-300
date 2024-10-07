from typing import Union, Tuple, TypeVar

T = TypeVar("T")
ResultWithErr = Union[Tuple[T, None], Tuple[None, Exception]]
OK = lambda x: (x, None)
ERR = lambda err: (None, err)
