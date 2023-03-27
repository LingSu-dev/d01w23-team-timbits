"""
Acceptance Tests for Issue46941 accessors
"""

import pandas as pd
import numpy.random as npr

# Proposed Dataset by issue
n_obs = 20
eye_colors = ["blue", "brown"]
people = pd.DataFrame({
    "eye_color": npr.choice(eye_colors, size=n_obs),
    "age": npr.randint(20, 60, size=n_obs)
})
people["age_group"] = pd.cut(people["age"], [20, 30, 40, 50, 60], right=False)
people["eye_color"] = pd.Categorical(people["eye_color"], eye_colors)

def test_ordered():
    print("Test proposed functionality in issue:\n")
    
    print("Output of original way to extract ordered column:\n")
    categories = people.select_dtypes("category")
    orig_res = categories[[col for col in categories.columns if categories[col].cat.ordered]]
    print(orig_res)
    
    print("Updated extraction of ordered column:\n")
    print(people.cat.ordered)
    
def test_unordered():
    print("\n\nTest proposed functionality for unordered in issue:\n")
    
    print("Output of original way to extract unordered column:\n")
    categories = people.select_dtypes("category")
    orig_res = categories[[col for col in categories.columns if not categories[col].cat.ordered]]
    print(orig_res)
    
    print("Updated extraction of unordered column:\n")
    print(people.cat.unordered)
    
def test_all():
    print("\n\nTest functionality for all columns in issue:\n")
    
    print("Output of original way to extract categorical columns:\n")
    orig_res = people.select_dtypes("category")
    print(orig_res)
    
    print("Updated extraction of categorical column:\n")
    print(people.cat.all)
        
if __name__ == "__main__":
    test_ordered()
    test_unordered()
    test_all()