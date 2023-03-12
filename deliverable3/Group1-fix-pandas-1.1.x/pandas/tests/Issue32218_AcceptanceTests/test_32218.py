"""
Acceptance Tests for Issue50456
"""

import pandas as pd
import numpy as np

# The acceptance test on issue mentioned in 32218
print("List initialization:")

df = pd.DataFrame(["1", "2", None], columns=["a"], dtype="str")
print(df)
print(type(df.loc[2].values[0]))

# Acceptance tests based on different usages.
print("\nMasked Array initialization:")

masked_data = np.ma.masked_array(np.array(["1", "2", None]), [False, True, False])
df = pd.DataFrame(masked_data, columns=["A"], dtype="str")
print(df)
print(type(df.loc[2].values[0]))

print("\nSeries initialization:")

df = pd.DataFrame(pd.Series(["1", "2", None]), columns=["A"], dtype="str")
print(df)
print(type(df.loc[2].values[0]))

print("\nIndex initialization:")

df = pd.DataFrame(pd.Index(["1", "2", None]), columns=["A"], dtype="str")
print(df)
print(type(df.loc[2].values[0]))