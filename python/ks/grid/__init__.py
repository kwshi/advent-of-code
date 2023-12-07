from ..point import P2

import typing
import sys

class Grid[T]:
    _data: list[T]

    _offset: int
    _step0: int
    _step1: int

    _size0: int

    def __init__(self, data: list[T], size0: int, *,step0:int|None=None,step1:int|None=None):
        self._data=data
        if len(data)%size0:
            raise ValueError(f'Grid `size0` {size0} does not evenly divide data length {len(data)}')


    def _index(self, p: P2.Like):
        match p:
            case (i,j) | P2(i,j):
                if not (0 <= i < self.size0  and 0<=j<self.size1): raise IndexError(p)
                return self._offset + i*self._step0 + j*self._step1

    def _update_offset(self):
        self._offset = (self._step0<0) * (1-self.size0)*self._step0+(self._step1<0)*(1-self.size1)*self._step1

    def rot(self, n:int=1):
        """
        starting from upright row-major m×n grid:
        rot0 index:      0,  n,  1, m
        rot1 index:    n-1, -1,  n, n
        rot2 index:   mn-1, -n, -1, m
        rot3 index: (m-1)n,  1, -n, n

        note: mn-1 = (m-1)n + (n-1).
        """
        match n%4:
            case 1:
                self._size0 = self.size1
                self._step0, self._step1 = -self._step1, self._step0
                self._update_offset()
            case 2:
                self._step0, self._step1 = -self._step0, -self._step1
                self._update_offset()
            case 3:
                self._size0 = self.size1
                self._step0, self._step1 = self._step1, -self._step0
                self._update_offset()
            case _:
                pass
        return self

    def flip0(self):
        self._step0 = -self._step0
        self._update_offset()
        return self

    def flip1(self):
        self._step1 = -self._step1
        self._update_offset()
        return self

    def __getitem__(self, p: P2.Like):
        return self._data[self._index(p)]

    def __setitem__(self, p: P2.Like, value: T):
        self._data[self._index(p)] = value

    def transpose(self):
        self._step0, self._step1 = self._step1, self._step0
        self._size0 = self.size1
        return self

    def transpose_anti(self):
        self.transpose()
        return self.rot(2)

    @property
    def size0(self): return self._size0

    @property
    def size1(self): return len(self._data)//self._size0

    def display(self, sep: str='', file: typing.TextIO=sys.stdout):
        width = max(len(str(v)) for v in self._data)
        for i in range(self.size0):
            file.write(sep.join(str(self[i,j]).rjust(width) for j in range(self.size1)))
            file.write('\n')
        file.write('\n')
        file.flush()

    def iter0(self):
        return (self[i,j]for i in range(self.size0) for j in range(self.size1))

    def iter1(self):
        return (self[i,j] for j in range(self.size1)for i in range(self.size0) )

    @classmethod
    def read_chars(cls, stdin: typing.TextIO):
        for line in stdin:
            pass
