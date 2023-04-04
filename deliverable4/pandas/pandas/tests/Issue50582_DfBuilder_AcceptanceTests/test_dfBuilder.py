"""
Acceptance Tests for Issue50582 DataFrameBuilder
"""

import pytest
import pandas as pd
import pandas._testing as tm
from pandas.core.framebuilder import dfBuilder

# Test dfBuilder with single row
def test_dfBuilder_single_row_no_dtype():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'])
    expected = builder.appendRow(['John', 30, 'M']).build()

    # Create actual DataFrame using DataFrame constructor
    data = [['John', 30, 'M']]
    actual = pd.DataFrame(data, columns=['name', 'age', 'gender'])

    tm.assert_equal(actual, expected)

def test_dfBuilder_single_dict_no_dtype():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'])
    expected = builder \
                .appendDict({"name": "John", "age": 30, "gender": "M"}) \
                .build()

    # Create actual DataFrame using DataFrame constructor
    data = [['John', 30, 'M']]
    actual = pd.DataFrame(data, columns=['name', 'age', 'gender'])

    tm.assert_equal(actual, expected)

def test_dfBuilder_multiple_rows_no_dtype():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'])
    expected = builder \
                .appendRow(['John', 30, 'M']) \
                .appendRow(['Mary', 25, 'F']) \
                .appendRow(['Bob', 40, 'M']) \
                .build()

    # Create actual DataFrame using DataFrame constructor
    data = [['John', 30, 'M'], ['Mary', 25, 'F'], ['Bob', 40, 'M']]
    actual = pd.DataFrame(data, columns=['name', 'age', 'gender'])

    tm.assert_equal(actual, expected)

def test_dfBuilder_multiple_rows_dict_no_dtype():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'])
    expected = builder \
                .appendDict({"name": "John", "age": 30, "gender": "M"}) \
                .appendDict({"name": "Mary", "age": 25, "gender": "F"}) \
                .appendDict({"name": "Bob", "age": 40, "gender": "M"}) \
                .build()

    # Create actual DataFrame using DataFrame constructor
    data = [['John', 30, 'M'], ['Mary', 25, 'F'], ['Bob', 40, 'M']]
    actual = pd.DataFrame(data, columns=['name', 'age', 'gender'])

    tm.assert_equal(actual, expected)

def test_dfBuilder_single_row_with_dtype_consistency():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['str', 'int', 'str'])
    expected = builder.appendRow(['John', 30, 'M']).build()

    # Create actual DataFrame using DataFrame constructor
    data = [['John', 30, 'M']]
    actual = pd.DataFrame(data, columns=['name', 'age', 'gender'])

    tm.assert_equal(actual, expected)

def test_dfBuilder_multiple_rows_with_dtype_consistency():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['str', 'int', 'str'])
    expected = builder \
                .appendRow(['John', 30, 'M']) \
                .appendRow(['Mary', 25, 'F']) \
                .appendRow(['Bob', 40, 'M']) \
                .build()

    # Create actual DataFrame using DataFrame constructor
    data = [['John', 30, 'M'], ['Mary', 25, 'F'], ['Bob', 40, 'M']]
    actual = pd.DataFrame(data, columns=['name', 'age', 'gender'])

    tm.assert_equal(actual, expected)

def test_dfBuilder_multiple_rows_dict_with_dtype_consistency():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['str', 'int', 'str'])
    expected = builder \
                .appendDict({"name": "John", "age": 30, "gender": "M"}) \
                .appendDict({"name": "Mary", "age": 25, "gender": "F"}) \
                .appendDict({"name": "Bob", "age": 40, "gender": "M"}) \
                .build()

    # Create actual DataFrame using DataFrame constructor
    data = [['John', 30, 'M'], ['Mary', 25, 'F'], ['Bob', 40, 'M']]
    actual = pd.DataFrame(data, columns=['name', 'age', 'gender'])

    tm.assert_equal(actual, expected)

def test_dfBuilder_single_rows_with_mismatch_dtype():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['int', 'int', 'str'])

    with pytest.raises(ValueError):
        builder.appendRow(['John', 30, 'M']).build()

def test_dfBuilder_multiple_rows_with_mismatch_dtype():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['int', 'int', 'str'])

    with pytest.raises(ValueError):
        builder.appendRow([1, 30, 'M']) \
               .appendRow([2, 25, 'F']) \
               .appendRow(['Bob', 40, 'M']) \
               .build()

def test_dfBuilder_multiple_rows_dict_with_mismatch_dtype():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['int', 'int', 'str'])
    
    with pytest.raises(ValueError):
        builder.appendDict({"name": 1, "age": 30, "gender": "M"}) \
               .appendDict({"name": 2, "age": 25, "gender": "F"}) \
               .appendDict({"name": "Kevin", "age": 40, "gender": "M"}) \
               .build()

def test_dfBuilder_single_row_with_dtype_downcast():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['str', 'int', 'bool'])
    expected = builder.appendRow(['John', 30, 'M']).build()
    
    # Create actual DataFrame using DataFrame constructor
    columns = ["name", "age", "gender"]
    dfs = []
    dfs.append(pd.DataFrame([['John', 30, 'M']], columns=columns, dtype=object))
    df_tmp = pd.concat(dfs, ignore_index=True)
    actual = df_tmp.astype({"name": "str", "age": "int", "gender": bool}, copy=False)
    
    tm.assert_equal(actual, expected)

def test_dfBuilder_multiple_rows_with_dtype_downcast():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['str', 'int', 'bool'])
    expected = builder \
                .appendRow(['John', 30, 'M']) \
                .appendRow(['Mary', 25, 'F']) \
                .appendRow(['Bob', 40, 'M']) \
                .build()
    
    # Create actual DataFrame using DataFrame constructor
    columns = ["name", "age", "gender"]
    dfs = []
    dfs.append(pd.DataFrame([['John', 30, 'M']], columns=columns, dtype=object))
    dfs.append(pd.DataFrame([['Mary', 25, 'F']], columns=columns, dtype=object))
    dfs.append(pd.DataFrame([['Bob', 40, 'M']], columns=columns, dtype=object))
    df_tmp = pd.concat(dfs, ignore_index=True)
    actual = df_tmp.astype({"name": "str", "age": "int", "gender": bool}, copy=False)
    
    tm.assert_equal(actual, expected)

def test_dfBuilder_multiple_rows_dict_with_dtype_downcast():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['str', 'int', 'bool'])
    expected = builder \
                .appendDict({"name": "John", "age": 30, "gender": "M"}) \
                .appendDict({"name": "Mary", "age": 25, "gender": "F"}) \
                .appendDict({"name": "Bob", "age": 40, "gender": "M"}) \
                .build()
    
    # Create actual DataFrame using DataFrame constructor
    columns = ["name", "age", "gender"]
    dfs = []
    dfs.append(pd.DataFrame([['John', 30, 'M']], columns=columns, dtype=object))
    dfs.append(pd.DataFrame([['Mary', 25, 'F']], columns=columns, dtype=object))
    dfs.append(pd.DataFrame([['Bob', 40, 'M']], columns=columns, dtype=object))
    df_tmp = pd.concat(dfs, ignore_index=True)
    actual = df_tmp.astype({"name": "str", "age": "int", "gender": bool}, copy=False)
    
    tm.assert_equal(actual, expected)

def test_dfBuilder_column_dtype_mismatch_len():
    # Create expected DataFrame using DataFrameBuilder
    msg = "Given columns and dtypes length do not match"
    with pytest.raises(ValueError, match=msg):
        builder = dfBuilder(columns=['name', 'age'], dtypes=['str', 'int', 'bool'])

def test_dfBuilder_column_rows_mismatch_len():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age'], dtypes=['str', 'int'])

    msg = "Given row length not match with columns length"
    with pytest.raises(ValueError, match=msg):
        builder.appendRow(['John', 30, 'M'])

def test_dfBuilder_single_row_as_type_valid():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age'], dtypes=['str', 'int'])
    expected = builder.appendRow(['John', 30]) \
                        .asType(dtype = ['str', 'bool']) \
                        .build()

    # Create actual DataFrame using DataFrame constructor
    columns = ["name", "age"]
    dfs = []
    dfs.append(pd.DataFrame([['John', 30]], columns=columns, dtype=object))
    df_tmp = pd.concat(dfs, ignore_index=True)
    actual = df_tmp.astype({"name": "str", "age": bool}, copy=False)

    tm.assert_equal(actual, expected)

def test_dfBuilder_multiple_rows_as_type_valid():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['str', 'int', 'bool'])
    expected = builder \
                .appendRow(['John', 30, 'M']) \
                .appendRow(['Mary', 25, 'F']) \
                .appendRow(['Bob', 40, 'M']) \
                .asType(dtype = ['str', 'str', 'bool']) \
                .build()

    # Create actual DataFrame using DataFrame constructor
    columns = ['name', 'age', 'gender']
    dfs = []
    dfs.append(pd.DataFrame([['John', 30, 'M']], columns=columns, dtype=object))
    dfs.append(pd.DataFrame([['Mary', 25, 'F']], columns=columns, dtype=object))
    dfs.append(pd.DataFrame([['Bob', 40, 'M']], columns=columns, dtype=object))
    df_tmp = pd.concat(dfs, ignore_index=True)
    actual = df_tmp.astype({"name": "str", "age": "str", "gender": bool}, copy=False)

    tm.assert_equal(actual, expected)
  
def test_dfBuilder_multiple_rows_dict_as_type_valid():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['str', 'int', 'bool'])
    expected = builder \
                .appendDict({"name": "John", "age": 30, "gender": "M"}) \
                .appendDict({"name": "Mary", "age": 25, "gender": "F"}) \
                .appendDict({"name": "Bob", "age": 40, "gender": "M"}) \
                .asType(dtype = ['str', 'str', 'bool']) \
                .build()

    # Create actual DataFrame using DataFrame constructor
    columns = ['name', 'age', 'gender']
    dfs = []
    dfs.append(pd.DataFrame([['John', 30, 'M']], columns=columns, dtype=object))
    dfs.append(pd.DataFrame([['Mary', 25, 'F']], columns=columns, dtype=object))
    dfs.append(pd.DataFrame([['Bob', 40, 'M']], columns=columns, dtype=object))
    df_tmp = pd.concat(dfs, ignore_index=True)
    actual = df_tmp.astype({"name": "str", "age": "str", "gender": bool}, copy=False)

    tm.assert_equal(actual, expected)

def test_dfBuilder_single_row_as_mismatch_type_str_to_int():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age'], dtypes=['str', 'int'])

    with pytest.raises(ValueError):
        builder.appendRow(['John', 30]).asType(dtype = ['int', 'int']).build()

def test_dfBuilder_single_row_as_mismatch_type_str_to_float():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age'], dtypes=['str', 'int'])

    with pytest.raises(ValueError):
        builder.appendRow(['John', 30]).asType(dtype = ['float', 'int']).build()

def test_dfBuilder_multiple_rows_as_mismatch_type():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['str', 'int', 'str'])
    
    with pytest.raises(ValueError):
        builder \
        .appendRow(['BigGuy', 30, 'M']) \
        .appendRow(['Mary', 25, 'F']) \
        .appendRow(['Bob', 40, 'M']) \
        .asType(dtype = ['int', 'int', 'str']) \
        .build()

def test_dfBuilder_single_row_as_type_mismatch_len():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age'], dtypes=['str', 'int'])

    msg = "Given dtypes length do not match with columns length"
    with pytest.raises(ValueError, match=msg):
        builder.appendRow(['John', 30]).asType(dtype = ['int', 'int', 'int']).build()

def test_dfBuilder_multiple_rows_as_type_mismatch_len():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['str', 'int', 'str'])
    
    msg = "Given dtypes length do not match with columns length"
    with pytest.raises(ValueError, match=msg):
        builder \
        .appendRow(['John', 30, 'M']) \
        .appendRow(['Mary', 25, 'F']) \
        .appendRow(['Bob', 40, 'M']) \
        .asType(dtype = ['int', 'int']) \
        .build()

def test_dfBuilder_appendDict_missing_data_1():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['str', 'int', 'str'])

    msg = "Missing data of column name"
    with pytest.raises(ValueError, match=msg):
        builder \
            .appendDict({"missing": "John", "age": 30, "gender": "M"}) \
            .appendDict({"name": "Mary", "age": 25, "gender": "F"}) \
            .appendDict({"name": "Bob", "age": 40, "gender": "M"}) \
            .asType(dtype = ['str', 'str', 'bool']) \
            .build()

def test_dfBuilder_appendDict_missing_data_2():
    # Create expected DataFrame using DataFrameBuilder
    builder = dfBuilder(columns=['name', 'age', 'gender'], dtypes=['str', 'int', 'str'])

    msg = "Missing data of column gender"
    with pytest.raises(ValueError, match=msg):
        builder \
            .appendDict({"name": "John", "age": 30, "gender": "M"}) \
            .appendDict({"name": "Mary", "age": 25, "gender": "F"}) \
            .appendDict({"name": "Bob", "age": 40, "missing": "M"}) \
            .asType(dtype = ['str', 'str', 'bool']) \
            .build()