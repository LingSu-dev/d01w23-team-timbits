"""
Acceptance Tests for Issue50456
"""

import pandas as pd
import pandas._testing as tm

from pandas.io.json import read_json


def test_orient_split_issue_input():
    print("\n\nFirst Test:\n")
    df = pd.DataFrame([[1, 2], [3, 4]], columns=pd.MultiIndex.from_arrays([["2022", "2022"], ['JAN', 'FEB']]))
    print(read_json(df.to_json(orient="split"), orient="split"))
    

def test_orient_split_biggerDF():
    print("\nSecond Test:\n")
    df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=pd.MultiIndex.from_arrays([["2022", "2022", "2023"], ['JAN', 'FEB', "FEB"], ["28th", "27th", "28th"]]))
    print(read_json(df.to_json(orient="split"), orient="split"))


def test_orient_split_biggestDF():
    print("\nThird Test:\n")
    df = pd.DataFrame([['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['i', 'j', 'k','l'],['m', 'n', 'o', 'p']],
    columns=pd.MultiIndex.from_arrays([["A", "A", "B", "B"], ["2022", "2022", "2023", "2024"], ["JAN", "FEB", "FEB", "MAR"], ["28th", "27th", "28th", "29th"]]))
    print(read_json(df.to_json(orient="split"), orient="split"))