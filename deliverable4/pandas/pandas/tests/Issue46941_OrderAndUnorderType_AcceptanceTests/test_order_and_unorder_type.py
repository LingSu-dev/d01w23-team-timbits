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

series = pd.Series([0, 1, 2])
group_member = series.astype(group_member_cat)
age = series.astype(age_cat)

def test_is_ordered_categorical_dtype():
  print("Test is_ordered_categorical_dtype")
  if (is_ordered_categorical_dtype(age_cat)):
    print(age_cat)
  if (is_ordered_categorical_dtype(group_member)):
    print(age)

def test_is_unordered_categorical_dtype():
  print("Test is_unordered_categorical_dtype")
  if (is_unordered_categorical_dtype(group_member_cat)):
    print(group_member_cat)
  if (test_is_unordered_categorical_dtype(group_member)):
    print(group_member)


if __name__ == "__main__":
    test_is_ordered_categorical_dtype()
    test_is_unordered_categorical_dtype()
