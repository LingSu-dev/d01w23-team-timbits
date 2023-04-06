"""
Acceptance Tests for Issue 46941 is_ordered_categorical_dtype
and is_unordered_categorical_dtype.
"""
import pandas as pd
from pandas.core.dtypes.common import (
  is_ordered_categorical_dtype,
  is_unordered_categorical_dtype,
  CategoricalDtype,
)


group_member_cat = CategoricalDtype(categories=['Ben', 'John', 'Alan'], ordered=False)
age_cat = CategoricalDtype(categories=[15, 18, 19], ordered=True)

array = [0, 1, 2]
series = ['a', 'b', 'c']
group_member = pd.Series(array, dtype=group_member_cat)
group_member.astype(group_member_cat)
age = pd.Series(array, dtype=age_cat)


def test_categorical_dtype():

  print("Testing categorical dtype")

  if (is_ordered_categorical_dtype(age_cat) and
      not is_unordered_categorical_dtype(age_cat)):
      print("pass order category")
  else:
      print("fail order category")

  if (is_ordered_categorical_dtype(age) and
      not is_unordered_categorical_dtype(age)):
      print("pass order series")
  else:
      print("fail order series")

  if (is_unordered_categorical_dtype(group_member_cat) and
      not is_ordered_categorical_dtype(group_member_cat)):
      print("pass unorder category")
  else:
      print("fail unorder category")

  if (is_unordered_categorical_dtype(group_member) and 
      not is_ordered_categorical_dtype(group_member)):
      print("pass unorder series")
  else:
      print("fail unorder series")


def test_non_categorical_type():

  print("Testing non categorical dtype")

  if (not is_unordered_categorical_dtype(series) and 
      not is_ordered_categorical_dtype(series)):
      print("pass serie")
  else:
      print("fail series")

  if (not is_unordered_categorical_dtype(array) and 
      not is_ordered_categorical_dtype(array)):
      print("pass array")
  else:
      print("fail array")
  
  if (not is_unordered_categorical_dtype(1) and 
      not is_ordered_categorical_dtype(1)):
      print("pass int")
  else:
      print("fail int")

  if (not is_unordered_categorical_dtype('a') and 
      not is_ordered_categorical_dtype('a')):
      print("pass str")
  else:
      print("fail str")

  if (not is_unordered_categorical_dtype(None) and 
      not is_ordered_categorical_dtype(None)):
      print("pass None")
  else:
      print("fail None")

  print("Test finished")


if __name__ == "__main__":
    test_categorical_dtype()
    test_non_categorical_type()
