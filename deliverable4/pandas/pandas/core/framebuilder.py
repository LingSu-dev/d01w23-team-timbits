# class dfBuilder

import pandas as pd
import numpy as np
from pandas import DataFrame


class dfBuilder:
    __rows = []

    def __init__(
        self,
        columns: list,
        dtypes: list = None, 
    ):
        self.columns = columns
        if dtypes is not None:
            self.dtypes = list(dtypes)
            if len(columns) != len(dtypes):
                raise ValueError("columns and type length do not match")
        else:
            self.dtypes = None
        


    def appendRow(self, row: list):
        if len(row) != len(self.columns):
            raise ValueError("Given row length not match with columns length")

        if self.dtypes is not None: 
            new_row = []
            for i in range(len(self.columns)):
                r = np.array([row[i]], dtype=np.dtype(self.dtypes[i]))
                new_row.append(r[0])
            self.__rows.append(new_row)
        
        else:
            self.__rows.append(row)
            
        """ 
            #if np.dtype(type(row[i])) != np.dtype(self.dtypes[i]):
            print(eval(np.dtype(self.dtypes[i])))
            if isinstance(row[i], eval(np.dtype(self.dtypes[i]))):
                    print(np.dtype(type(row[i])))
                    print(np.dtype(self.dtypes[i]))
                    raise ValueError("type error")
                
        """

    

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
