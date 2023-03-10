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
    ser = Series([1, 2, 3])

    msg = lambda x: f"axis={x} is not a valid parameter"
    with pytest.raises(ValueError, match=msg("foo")):
        ser.take([1], axis="foo")
    with pytest.raises(ValueError, match=msg(1)):
        ser.take([1], axis=1)


def test_take_non_default_axis():
    # https://github.com/pandas-dev/pandas/issues/51022
    msg = lambda x: f"axis={x} is not a valid parameter"
    with pytest.raises(ValueError, match=msg("aaa")):
        pd.Series([1, 4, 7]).take([2], axis="aaa")
    with pytest.raises(ValueError, match=msg("0")):
        pd.Series([1, 4, 7]).take([0, 1], axis="0")


def test_take_default_axis():
    # https://github.com/pandas-dev/pandas/issues/51022
    actual = pd.Series([1, 4, 7]).take([2])
    expected = pd.Series([7], index=[2])
    tm.assert_series_equal(actual, expected)

    actual = pd.Series([1, 4, 7]).take([0, 1], axis="index")
    expected = pd.Series([1, 4], index=[0, 1])
    tm.assert_series_equal(actual, expected)
