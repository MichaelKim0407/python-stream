import time as _time
import typing as _typing
from threading import (
    Thread as _Thread,
)

from stream.typing import (
    T_co as _T_co,
)


class ThreadedPrefetchOneIterator(_typing.Iterator[_T_co]):
    """
    Prefetch one record via multi-threading.
    """

    def __init__(self, iterable):
        self.__iter = iter(iterable)

        self.__next = None
        self.__stop_iteration = False
        self.__thread: _Thread = None
        self.__prefetch()

    def __prefetch_task(self):
        try:
            self.__next = next(self.__iter)
        except StopIteration:
            self.__stop_iteration = True

    def __prefetch(self):
        self.__thread = _Thread(target=self.__prefetch_task)
        self.__thread.start()

    def __next__(self):
        self.__thread.join()
        if self.__stop_iteration:
            raise StopIteration
        try:
            return self.__next
        finally:
            self.__prefetch()


class ThreadedPrefetchAllIterator(_typing.Iterator[_T_co]):
    class Timeout(Exception):
        pass

    def __init__(
            self,
            iterable,
            *,
            sleep=None,
            timeout=None,
    ):
        self.__iter = iter(iterable)
        self.__sleep = sleep
        self.__timeout = timeout

        self.__results = []
        self.__stopped = False
        self.__prefetch()

    def __prefetch_task(self):
        for item in self.__iter:
            self.__results.append(item)
        self.__stopped = True

    def __prefetch(self):
        thread = _Thread(target=self.__prefetch_task)
        thread.start()

    def __check_timeout(self, start):
        if self.__timeout is None:
            return
        if _time.time() - start < self.__timeout:
            return
        raise self.Timeout

    def __wait(self):
        if self.__sleep is None:
            return
        _time.sleep(self.__sleep)

    def __next__(self):
        start_timeout = _time.time()
        while not self.__results:
            if self.__stopped:
                raise StopIteration
            self.__check_timeout(start_timeout)
            self.__wait()
        return self.__results.pop(0)
