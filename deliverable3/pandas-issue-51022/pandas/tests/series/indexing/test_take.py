import pytest

import pandas as pd
from pandas import Series
import pandas._testing as tm


def test_take():
    ser = Series([-1, 5, 6, 2, 4])

    actual = ser.take([1, 3, 4])
    expected = Series([5, 2, 4], index=[1, 3, 4])
    tm.assert_series_equal(actual, expected)

    actual = ser.take([-1, 3, 4])
    expected = Series([4, 2, 4], index=[4, 3, 4])
    tm.assert_series_equal(actual, expected)

    msg = lambda x: f"index {x} is out of bounds for( axis 0 with)? size 5"
    with pytest.raises(IndexError, match=msg(10)):
        ser.take([1, 10])
    with pytest.raises(IndexError, match=msg(5)):
        ser.take([2, 5])


def test_take_categorical():
    # https://github.com/pandas-dev/pandas/issues/20664
    ser = Series(pd.Categorical(["a", "b", "c"]))
    result = ser.take([-2, -2, 0])
    expected = Series(
        pd.Categorical(["b", "b", "a"], categories=["a", "b", "c"]), index=[1, 1, 0]
    )
    tm.assert_series_equal(result, expected)

def test_take_wrong_axis():
    # https://github.com/pandas-dev/pandas/issues/51022
    ser = Series([1,2,3])
    
    msg = lambda x: f"axis={x} is not a valid parameter"
    with pytest.raises(ValueError, match=msg("foo")):
        ser.take([1], axis="foo")
    with pytest.raises(ValueError, match=msg(1)):
        ser.take([1], axis=1)