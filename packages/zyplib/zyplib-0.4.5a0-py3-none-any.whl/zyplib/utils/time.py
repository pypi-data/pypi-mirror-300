import time
from datetime import datetime, timedelta, timezone
from timeit import default_timer as timer


def cur_time(pat: str ='%m/%d %H:%M:%S'):
    ts = time.time()
    td = timedelta(hours=8)  # 我们在东八区
    tz = timezone(td)
    dt = datetime.fromtimestamp(ts, tz)
    dt = dt.strftime(pat)
    return dt


class TicToc:
    def __init__(self):
        self._tic = 0
        self._toc = 0
        self._elapsed = 0

    def tic(self):
        self._tic = timer()

    def toc(self):
        self._toc = timer()
        self._elapsed = self._toc - self._tic

    @property
    def elapsed(self):
        delta = timedelta(seconds=self._elapsed)
        return str(delta)[:-3]
