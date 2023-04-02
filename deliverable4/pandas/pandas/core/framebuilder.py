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
        self.__rows=[]
        self.columns = columns
        if dtypes is not None:
            self.dtypes = list(dtypes)
            if len(columns) != len(dtypes):
                raise ValueError("Given columns and dtypes length do not match")
        else:
            self.dtypes = None


    def asType(self, dtype: list):
        if len(self.columns)!= len(dtype):
            raise ValueError("Given dtypes length do not match with columns length")

        if len(self.__rows) ==0:
            self.dtypes = list(dtype)
        else:
            for i in range(len(self.columns)):
                
                for j in range(len(self.__rows)):
                    
                    column_check=[(self.__rows[j][i])]
                    r = np.array(column_check, dtype=np.dtype(dtype[i]))
                    self.__rows[j][i] = r[0]
            self.dtypes=list(dtype)


    def appendDict(self, row: dict):
        new_row = []
        for i in range(len(self.columns)):
            if self.columns[i] not in row:
                raise ValueError("Missing data of column " + self.columns[i])
            
            if self.dtypes is not None:
                r = np.array([row[self.columns[i]]], dtype= np.dtype(self.dtypes[i]))
                new_row.append(r[0])
            else:
                new_row.append(row[self.columns[i]])

        self.__rows.append(new_row)



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


    

    def build(self):
        df = DataFrame(self.__rows, columns=self.columns)
        return df
