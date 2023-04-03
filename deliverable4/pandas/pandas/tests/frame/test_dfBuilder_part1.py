import pandas as pd
import numpy as np
from pandas import DataFrame
from pandas.core.framebuilder import dfBuilder
import pandas._testing as tm
import pytest

class TestdfBuilder:

    # test when there is no dtypes
    def test_init(self):
        testforinit = dfBuilder(columns=['a','b','c'])
        expectedcolumns = ['a','b','c']
        expecteddtypes = None
        expectedrows = []
        assert testforinit.columns == expectedcolumns
        assert testforinit.dtypes == expecteddtypes
        assert testforinit.getrows() == expectedrows

    # test when there is dtypes
    def test_init2(self):
        testforinit = dfBuilder(columns=['a','b','c'],dtypes=["int","float","str"])
        expectedcolumns = ['a','b','c']
        expecteddtypes = ["int","float","str"]
        expectedrows = []
        assert testforinit.columns == expectedcolumns
        assert testforinit.dtypes == expecteddtypes
        assert testforinit.getrows() == expectedrows

    # test when there is dtypes and columns length is not equal to dtypes length and check if ValueError is raised
    def test_init3(self):
        with pytest.raises(ValueError):
            testforinit = dfBuilder(columns=['a','b','c'],dtypes=["int","float"])

    # test for appendDict
    def test_appendDict(self):
        testBuilder = dfBuilder(columns=['a','b','c'])
        testBuilder.appendDict(row={'a':1,'b':2,'c':3})
        expectedrows = [[1,2,3]]
        assert testBuilder.getrows() == expectedrows

    # test for appendDict when there is dtypes
    def test_appendDict2(self):
        testBuilder = dfBuilder(columns=['a','b','c'],dtypes=["int","float","str"])
        testBuilder.appendDict(row={'a':1,'b':2,'c':3})
        expectedrows = [[1,2.0,"3"]]
        assert testBuilder.getrows() == expectedrows

    # test for appendDict when there is dtypes and check if ValueError is raised
    def test_appendDict3(self):
        with pytest.raises(ValueError):
            testforinit = dfBuilder(columns=['a','b','c'],dtypes=["int","float","str"])
            testforinit.appendDict(row={'a':1,'b':2})

    # test for appendDict when there is no dtypes and check if we can add different data types
    def test_appendDict4(self):
        testBuilder = dfBuilder(columns=['a','b','c'])
        testBuilder.appendDict(row={'a':1,'b':2.0,'c':"3"})
        testBuilder.appendDict(row={'a':1,'b':2,'c':3})
        expectedrows = [[1,2.0,"3"],[1,2,3]]
        assert testBuilder.getrows() == expectedrows

    # test for appendRow
    def test_appendRow(self):
        testBuilder = dfBuilder(columns=['a','b','c'])
        testBuilder.appendRow(row=[1,2,3])
        expectedrows = [[1,2,3]]
        assert testBuilder.getrows() == expectedrows

    # test for appendRow when there is dtypes
    def test_appendRow2(self):
        testBuilder = dfBuilder(columns=['a','b','c'],dtypes=["int","float","str"])
        testBuilder.appendRow(row=[1,2,3])
        expectedrows = [[1,2.0,"3"]]
        assert testBuilder.getrows() == expectedrows

    # test for appendRow when there is dtypes and check if ValueError is raised
    def test_appendRow3(self):
        with pytest.raises(ValueError):
            testforinit = dfBuilder(columns=['a','b','c'],dtypes=["int","float","str"])
            testforinit.appendRow(row=[1,2])

    # test for appendRow when there is no dtypes and check if we can add different data types
    def test_appendRow4(self):
        testBuilder = dfBuilder(columns=['a','b','c'])
        testBuilder.appendRow(row=[1,2.0,"3"])
        testBuilder.appendRow(row=[1,2,3])
        expectedrows = [[1,2.0,"3"],[1,2,3]]
        assert testBuilder.getrows() == expectedrows

    # test for appendRow when one of the data types is not correct
    def test_appendRow5(self):
        testBuilder = dfBuilder(columns=['a','b','c'],dtypes=["int","float","bool"])
        testBuilder.appendRow(row=[1,2,"3"])
        expectedrows = [[1,2.0,True]]
        assert testBuilder.getrows() == expectedrows

    # test for appendRows when adding multiple rows
    def test_appendRows6(self):
        testBuilder = dfBuilder(columns=['a','b','c'])
        testBuilder.appendRow([1,2,True])
        testBuilder.appendRow(["4",5,6])
        expectedrows = [[1,2,True],["4",5,6]]
        assert testBuilder.getrows() == expectedrows



    

