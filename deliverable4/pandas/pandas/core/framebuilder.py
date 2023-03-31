# class builder for DataFrames class

import typing as tp
import pandas as pd
import numpy as np
from pandas._typing import (
    Dtype,
    Axes,
)
from pandas import DataFrame


class dfBuilder:
    __rows = []

    def __init__(
        self,
        columns: list,
        dtypes: list, 
    ):
        self.columns = columns
        if dtypes is not None:
            self.dtypes = list(dtypes)
            if len(columns) != len(dtypes):
                raise ValueError()
            """
            self.dtypes = {}
            for i in range(len(self.columns)):
                self.dtypes[self.columns[i]] = np.dtype(dtypes[i])
            """

        else:
            dtypes = None
        


    def appendRow(self, row: list):
        if len(row) != len(self.columns):
            raise ValueError("length error")

        new_row = []
        for i in range(len(self.columns)):
            r = np.array([row[i]], dtype=np.dtype(self.dtypes[i]))
            new_row.append(r[0])
        """ 
            #if np.dtype(type(row[i])) != np.dtype(self.dtypes[i]):
            print(eval(np.dtype(self.dtypes[i])))
            if isinstance(row[i], eval(np.dtype(self.dtypes[i]))):
                    print(np.dtype(type(row[i])))
                    print(np.dtype(self.dtypes[i]))
                    raise ValueError("type error")
                
        """
        self.__rows.append(new_row)
    
    def build(self):
        """
        dtype_dict = {}
        for i in range(len(self.columns)):
            dtype_dict[self.columns[i]] = self.dtypes[i]
        
        df = DataFrame(self.__rows, columns=self.columns, dtype=dtype_dict)
        return df
        """
        df = DataFrame(self.__rows, columns=self.columns)
        return df