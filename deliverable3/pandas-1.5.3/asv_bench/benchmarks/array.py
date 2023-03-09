import numpy as np

import pandas as pd

from .pandas_vb_common import tm


class BooleanArray:
    def setup(self):
        self.values_bool = np.array([True, False, True, False])
        self.values_float = np.array([1.0, 0.0, 1.0, 0.0])
        self.values_integer = np.array([1, 0, 1, 0])
        self.values_integer_like = [1, 0, 1, 0]
        self.data = np.array([True, False, True, False])
        self.mask = np.array([False, False, True, False])

    def time_constructor(self):
        pd.arrays.BooleanArray(self.data, self.mask)

    def time_from_bool_array(self):
        pd.array(self.values_bool, dtype="boolean")

    def time_from_integer_array(self):
        pd.array(self.values_integer, dtype="boolean")

    def time_from_integer_like(self):
        pd.array(self.values_integer_like, dtype="boolean")

    def time_from_float_array(self):
        pd.array(self.values_float, dtype="boolean")


class IntegerArray:
    def setup(self):
        self.values_integer = np.array([1, 0, 1, 0])
        self.data = np.array([1, 2, 3, 4], dtype="int64")
        self.mask = np.array([False, False, True, False])

    def time_constructor(self):
        pd.arrays.IntegerArray(self.data, self.mask)

    def time_from_integer_array(self):
        pd.array(self.values_integer, dtype="Int64")


class ArrowStringArray:

    params = [False, True]
    param_names = ["multiple_chunks"]

    def setup(self, multiple_chunks):
        try:
            import pyarrow as pa
        except ImportError:
            raise NotImplementedError
        strings = tm.rands_array(3, 10_000)
        if multiple_chunks:
            chunks = [strings[i : i + 100] for i in range(0, len(strings), 100)]
            self.array = pd.arrays.ArrowStringArray(pa.chunked_array(chunks))
        else:
            self.array = pd.arrays.ArrowStringArray(pa.array(strings))

    def time_setitem(self, multiple_chunks):
        for i in range(200):
            self.array[i] = "foo"

    def time_setitem_list(self, multiple_chunks):
        indexer = list(range(0, 50)) + list(range(-50, 0))
        self.array[indexer] = ["foo"] * len(indexer)

    def time_setitem_slice(self, multiple_chunks):
        self.array[::10] = "foo"
