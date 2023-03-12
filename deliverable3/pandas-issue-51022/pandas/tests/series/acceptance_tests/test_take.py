import pytest

import pandas as pd
import pandas._testing as tm

def test_take_value_error(ax):
    s = pd.Series([1, 2, 3])
    indices = [0]
    except_msg = f"axis={ax} is not a valid parameter"
    with pytest.raises(ValueError, match=except_msg):
        s.take(indices, axis=ax)
    

def test_series_take():
    '''
    the issue was lacking of validate the parameter, axis in Series.take()

    Thers tests ensure that the issue was fixed
    '''

    #default axis value
    s = pd.Series([1, 2, 3, 4, 5])
    indices = [0, 2, 4]

    result = s.take(indices)
    except_result = pd.Series([1, 3, 5], index=indices)
    tm.assert_series_equal(result, except_result)

    #valid axis in Series.take()
    result = s.take(indices, axis=0)
    except_result = pd.Series([1, 3, 5], index=indices)
    tm.assert_series_equal(result, except_result)

    result = s.take(indices, axis="index")
    except_result = pd.Series([1, 3, 5], index=indices)
    tm.assert_series_equal(result, except_result)

    #invalid axis in Series.take(), but valid axis value
    test_take_value_error(1)
    test_take_value_error('columns')

    #invalid axis value
    test_take_value_error(-1)
    test_take_value_error('foo')

if __name__== "__main__":
    test_series_take()
    print ("All tests passed")