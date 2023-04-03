import pandas as pd
import numpy as np
from pandas import DataFrame
from pandas.core.framebuilder import dfBuilder
import pandas._testing as tm
import pytest

class TestdfBuilder:
    def test_asType(self):
        testBuilder = dfBuilder(columns=['a','b','c'])
        testBuilder.appendDict(row={'a':1,'b':2,'c':3})
        testBuilder.asType(dtype=["int","float","str"])
        expectedrows = [[1,2.0,"3"]]
        assert testBuilder.getrows() == expectedrows
    
    # test asType when there is dtypes and check if ValueError is raised
    def test_asType2(self):
        with pytest.raises(ValueError):
            testBuilder = dfBuilder(columns=['a','b'])
            testBuilder.asType(dtype=["int","float","str"])

    # test asType when there are rows with different data types
    def test_asType3(self):
        testBuilder = dfBuilder(columns=['a','b','c'])
        testBuilder.appendDict(row={'a':1,'b':2.0,'c':"3"})
        testBuilder.appendDict(row={'a':1,'b':2,'c':3})
        testBuilder.asType(dtype=["int","float","bool"])
        expectedrows = [[1,2.0,True],[1,2.0,True]]
        assert testBuilder.getrows() == expectedrows

    # test asType when putting asType in the middle of appendRow
    def test_asType4(self):
        testBuilder = dfBuilder(columns=['a','b','c'])
        testBuilder.appendRow([1,2,3])
        testBuilder.asType(dtype=["int","float","str"])
        testBuilder.appendDict(row={'a':1,'b':2.0,'c':"3"})
        expectedrows = [[1,2.0,"3"],[1,2.0,"3"]]
        assert testBuilder.getrows() == expectedrows

    # test build when there is no dtypes and no rows
    def test_build(self):
        testBuilder = dfBuilder(columns=['a','b','c'])
        expecteddf = DataFrame(columns=['a','b','c'])
        tm.assert_frame_equal(testBuilder.build(),expecteddf)

    # test build when there is dtypes
    def test_build2(self):
        testBuilder = dfBuilder(columns=['a','b','c'],dtypes=["int","float","str"])
        expecteddf = DataFrame(columns=['a', 'b', 'c'])
        expecteddf['a'] = expecteddf['a'].astype('int')
        expecteddf['b'] = expecteddf['b'].astype('float')
        expecteddf['c'] = expecteddf['c'].astype('str')
        tm.assert_frame_equal(testBuilder.build(),expecteddf)

    # test build when there is dtypes and rows
    def test_build3(self):
        testBuilder = dfBuilder(columns=['a','b','c'],dtypes=["int","float","str"])
        testBuilder.appendRow([1,2,3])
        expecteddf = DataFrame(columns=['a', 'b', 'c'])
        expecteddf['a'] = expecteddf['a'].astype('int')
        expecteddf['b'] = expecteddf['b'].astype('float')
        expecteddf['c'] = expecteddf['c'].astype('str')
        expecteddf.loc[0] = [1,2.0,"3"]
        tm.assert_frame_equal(testBuilder.build(),expecteddf,check_dtype=False)

    # test build when there is dtypes and rows with different data types
    def test_build4(self):
        testBuilder = dfBuilder(columns=['a','b','c'],dtypes=["int","float","str"])
        testBuilder.appendRow([1,2,3])
        testBuilder.appendDict(row={'a':1,'b':2.0,'c':"3"})
        expecteddf = DataFrame(columns=['a', 'b', 'c'])
        expecteddf['a'] = expecteddf['a'].astype('int')
        expecteddf['b'] = expecteddf['b'].astype('float')
        expecteddf['c'] = expecteddf['c'].astype('str')
        expecteddf.loc[0] = [1,2.0,"3"]
        expecteddf.loc[1] = [1,2.0,"3"]
        tm.assert_frame_equal(testBuilder.build(),expecteddf,check_dtype=False)

    # test build when there is dtypes and rows with different data types
    def test_build5(self):
        testBuilder = dfBuilder(columns=['a','b','c'],dtypes=["int","float","bool"])
        testBuilder.appendRow([1,2,0])
        testBuilder.appendDict(row={'a':1,'b':2.0,'c':"3"})
        testBuilder.asType(dtype=["int","float","bool"])
        expecteddf = DataFrame(columns=['a', 'b', 'c'])
        expecteddf['a'] = expecteddf['a'].astype('int')
        expecteddf['b'] = expecteddf['b'].astype('float')
        expecteddf['c'] = expecteddf['c'].astype('bool')
        expecteddf.loc[0] = [1,2.0,False]
        expecteddf.loc[1] = [1,2.0,True]
        tm.assert_frame_equal(testBuilder.build(),expecteddf,check_dtype=False)

    # test build when there isn't dtypes and rows with different data types
    def test_build6(self):
        testBuilder = dfBuilder(columns=['a','b','c'])
        testBuilder.appendRow([1,2,0])
        testBuilder.appendDict(row={'a':1,'b':2.0,'c':"3"})
        expecteddf = DataFrame(columns=['a', 'b', 'c'])
        expecteddf.loc[0] = [1,2,0]
        expecteddf.loc[1] = [1,2.0,"3"]
        tm.assert_frame_equal(testBuilder.build(),expecteddf,check_dtype=False)