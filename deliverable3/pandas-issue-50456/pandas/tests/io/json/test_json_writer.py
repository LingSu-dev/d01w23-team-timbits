from pandas import DataFrame
import pandas as pd
import pandas._testing as tm
from pandas.io.json._json import FrameWriter


def test_writejson_base_case():
    testdf = DataFrame()
    writer = FrameWriter(obj = testdf, date_format="iso", double_precision=2, ensure_ascii=False, date_unit="s", index=True, default_handler=None,indent=4,orient="split")
    tm.assert_frame_equal(testdf, writer.obj_to_write)


def test_writejson_normal_case():
    testdf = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    writer = FrameWriter(obj = testdf, date_format="iso", double_precision=2, ensure_ascii=False, date_unit="s", index=True, default_handler=None,indent=4,orient="split")
    tm.assert_frame_equal(testdf, writer.obj_to_write)

def test_writejson_normal_case2():
    df = DataFrame([[1]],columns=pd.MultiIndex.from_arrays([["2022"]]))
    writer = FrameWriter(obj = df, date_format="iso", double_precision=2, ensure_ascii=False, date_unit="s", index=True, default_handler=None,indent=4,orient="split") 
    tm.assert_frame_equal(df, writer.obj_to_write)

#this is the case mentioned in the issue
def test_writejson_issue_case():
    df = DataFrame([[1, 2], [3, 4]],columns=pd.MultiIndex.from_arrays([["2022", "2022"], ['JAN', 'FEB']]))
    trans_columns = DataFrame([[1, 2], [3, 4]],columns=pd.MultiIndex.from_arrays([["2022", "JAN"], ['2022', 'FEB']]))
    writer = FrameWriter(obj = df, date_format="iso", double_precision=2, ensure_ascii=False, date_unit="s", index=True, default_handler=None,indent=4,orient="split") 
    tm.assert_frame_equal(trans_columns, writer.obj_to_write)


def test_writejson_more_complex():
    df = DataFrame([[1, 2, 3], [3, 4, 5],[5, 6, 7]],columns=pd.MultiIndex.from_arrays([["2022", "2022", "2022"], ['JAN', 'FEB', 'MAR'],['A','B', 'C']]))
    trans_columns = DataFrame([[1, 2, 3], [3, 4, 5],[5, 6, 7]],columns=pd.MultiIndex.from_arrays([["2022", "JAN", "A"], ['2022', 'FEB', 'B'],['2022','MAR', 'C']]))
    writer = FrameWriter(obj = df, date_format="iso", double_precision=2, ensure_ascii=False, date_unit="s", index=True, default_handler=None,indent=4,orient="split")
    tm.assert_frame_equal(trans_columns, writer.obj_to_write)


def test_writejson_more_complex2():
    df = DataFrame([[1, 2, 3, 4], [3, 4, 5, 6], [5, 6, 7, 8],[9, 10, 11, 12]],columns=pd.MultiIndex.from_arrays([["2022", "2022","2023","2024"], ['JAN', 'FEB','MAR','APR'],['A','B','c', 'D'],["a","b","c","d"]]))
    trans_columns = DataFrame([[1, 2, 3, 4], [3, 4, 5, 6], [5, 6, 7, 8],[9,10,11,12]],columns=pd.MultiIndex.from_arrays([["2022", "JAN", "A","a"], ['2022', 'FEB', 'B','b'],['2023','MAR', 'c','c'],['2024','APR', 'D','d']]))
    writer = FrameWriter(obj = df, date_format="iso", double_precision=2, ensure_ascii=False, date_unit="s", index=True, default_handler=None,indent=4,orient="split")
    tm.assert_frame_equal(trans_columns, writer.obj_to_write)
    
    