import numpy as np
import pytest

from pandas import (
    CategoricalDtype,
    Series,
    DataFrame,
    concat,
)
import pandas._testing as tm

class CatFrameAccessorBase:
    @pytest.fixture(autouse=True)
    def empty_df(self):
        self.empty = DataFrame()
        yield self.empty
    
    @pytest.fixture(autouse=True) 
    def ordered_df(self):
        bool_cat = CategoricalDtype(categories=[0, 1], ordered=True)
        
        self.ordered = DataFrame(columns=['a', 'b'])
        self.ordered = self.ordered.astype(bool_cat)
        yield self.ordered
    
    @pytest.fixture(autouse=True) 
    def unordered_df(self):
        unordered_bool_cat = CategoricalDtype(categories=[0, 1], ordered=False)
        
        self.unordered = DataFrame(columns=['c', 'd'])
        self.unordered = self.unordered.astype(unordered_bool_cat)
        yield self.unordered
        
    @pytest.fixture(autouse=True)
    def nocat_df(self):
        self.nocat = DataFrame(columns=[1,2])
        yield self.nocat

    @pytest.fixture(autouse=True)
    def mixcontent_df(self, unordered_df, ordered_df, nocat_df):
        self.mixed = concat([unordered_df, ordered_df, nocat_df], axis=1, join='inner')
        id = np.identity(6,dtype=np.int64)
        for c, i in zip(self.mixed.columns, range(6)):
            self.mixed[c] = Series(data=id[i]).astype(self.mixed[c].dtype)
            
        yield self.mixed

class TestCatFrameAccessor(CatFrameAccessorBase):
    
    def test_null_column_cat_accessor_get_properties(self, empty_df):
        """
        Empty DataFrames on .cat.* should an empty DataFrame
        """
        tm.assert_frame_equal(empty_df, empty_df.cat.all)
        tm.assert_frame_equal(empty_df, empty_df.cat.ordered)
        tm.assert_frame_equal(empty_df, empty_df.cat.unordered)
    
    def test_no_cat_cat_accessor_get_properties(self, nocat_df, empty_df):
        """
        DataFrames without any categorical indexes on .cat.* should an empty DataFrame
        """
        tm.assert_frame_equal(empty_df, nocat_df.cat.all, check_column_type=False)
        tm.assert_frame_equal(empty_df, nocat_df.cat.ordered, check_column_type=False)
        tm.assert_frame_equal(empty_df, nocat_df.cat.unordered, check_column_type=False)
    
    def test_only_ordered_cat_accessor_get_properties(self, ordered_df, empty_df):
        """
        DataFrames with only ordered categorical indexes on .cat.all/ordered should an empty DataFrame,
        o.w. should return nothing
        """
        tm.assert_frame_equal(ordered_df, ordered_df.cat.all, check_column_type=False)
        tm.assert_frame_equal(ordered_df, ordered_df.cat.ordered, check_column_type=False)
        tm.assert_frame_equal(empty_df, ordered_df.cat.unordered, check_column_type=False)
    
    def test_only_unordered_cat_accessor_get_properties(self, unordered_df, empty_df):
        """
        DataFrames with only unordered categorical indexes on .cat.all/unordered should an empty DataFrame,
        o.w. should return nothing
        """
        tm.assert_frame_equal(unordered_df, unordered_df.cat.all, check_column_type=False)
        tm.assert_frame_equal(empty_df, unordered_df.cat.ordered, check_column_type=False)
        tm.assert_frame_equal(unordered_df, unordered_df.cat.unordered, check_column_type=False)
    
    def test_both_order_cat_accessor_get_properties(self, unordered_df, ordered_df):
        """
        DataFrames with both ordering should display the corresponding columns on each .cat.* method.
        """
        all_cat = concat([unordered_df, ordered_df], axis=1, join='inner')
        tm.assert_frame_equal(all_cat, all_cat.cat.all, check_column_type=False)
        tm.assert_frame_equal(ordered_df, all_cat.cat.ordered, check_column_type=False)
        tm.assert_frame_equal(unordered_df, all_cat.cat.unordered, check_column_type=False)
    
    def test_multiple_mixed_cat_accessor_get_properties(self, unordered_df, ordered_df, nocat_df):
        """
        DataFrames with mixed categorical indexes should ignore non categorical indexes and display the corresponding
        columns on each .cat.* method.
        """
        mixed = concat([unordered_df, ordered_df, nocat_df], axis=1, join='inner')
        all_cat = concat([unordered_df, ordered_df], axis=1, join='inner')
        tm.assert_frame_equal(all_cat, mixed.cat.all, check_column_type=False)
        tm.assert_frame_equal(ordered_df, mixed.cat.ordered, check_column_type=False)
        tm.assert_frame_equal(unordered_df, mixed.cat.unordered, check_column_type=False)
    
    def test_preserve_row_cat_accessor_get_properties(self, unordered_df, ordered_df, mixcontent_df):
        """
        DataFrame columns should contain the same data after the segregation.
        """  
        ordered_columns = mixcontent_df[ordered_df.columns]
        unordered_columns = mixcontent_df[unordered_df.columns]
        all_cat_columns = concat([unordered_columns, ordered_columns], axis=1, join='inner')
        
        tm.assert_frame_equal(all_cat_columns, mixcontent_df.cat.all, check_column_type=False)
        tm.assert_frame_equal(ordered_columns, mixcontent_df.cat.ordered, check_column_type=False)
        tm.assert_frame_equal(unordered_columns, mixcontent_df.cat.unordered, check_column_type=False)
        
    def test_delegate_no_cat(self, empty_df, nocat_df):
        """
        DataFrame without columns or no categorical columns should return empty DataFrame
        """
        tm.assert_frame_equal(empty_df, empty_df.cat.as_ordered(), check_column_type=False)
        tm.assert_frame_equal(empty_df, nocat_df.cat.as_ordered(), check_column_type=False)
        
    def test_delegate_no_cat_type_error(self, empty_df):
        """
        DataFrame without columns or no categorical columns should give error when input to
        delegate is invalid
        """
        try:
            empty_df.cat.reorder_categories()
            pytest.xfail("Expected: TypeError; Actual: No error")
        except Exception as ex:
            if (not isinstance(ex, TypeError)):
                pytest.xfail("Expected: TypeError; Actual: " + ex.__class__.__name__)
                
        try:
            empty_df.cat.reorder_categories(1)
            pytest.xfail("Expected: TypeError; Actual: No error")
        except Exception as ex:
            if (not isinstance(ex, TypeError)):
                pytest.xfail("Expected: TypeError; Actual: " + ex.__class__.__name__)
                
    def test_delegate_no_cat_attr_error(self, empty_df):
        """
        DataFrame without columns or no categorical columns should give error when input to
        delegate is invalid
        """
        try:
            empty_df.cat.dummy
            pytest.xfail("Expected: AttributeError; Actual: No error")
        except Exception as ex:
            if (not isinstance(ex, AttributeError)):
                pytest.xfail("Expected: AttributeError; Actual: " + ex.__class__.__name__)
                
        try:
            empty_df.cat.dummy()
            pytest.xfail("Expected: AttributeError; Actual: No error")
        except Exception as ex:
            if (not isinstance(ex, AttributeError)):
                pytest.xfail("Expected: AttributeError; Actual: " + ex.__class__.__name__)
                
    def test_delegate_no_param(self, ordered_df, unordered_df):
        """
        DataFrame operation should be applied on all categorical. We use remove_unused_categories.
        """
        mixed = concat([unordered_df, ordered_df], axis=1, join='inner')
        clean_df = mixed.cat.remove_unused_categories()
        for col in clean_df.cat.all:
            assert(clean_df[col].cat.categories.array.size == 0)
            
    def test_delegate_non_empty_param(self, ordered_df, unordered_df, nocat_df):
        """
        DataFrame operation with a parameter should be applied on all categorical without error.
        We use remove_categories. This furthur tests categories from non categoricals are not
        returned.
        """
        mixed = concat([unordered_df, ordered_df, nocat_df], axis=1, join='inner')
        clean_df = mixed.cat.remove_categories([0])
        for col in clean_df.cat.all:
            assert(clean_df[col].cat.categories.array.size == 1)
        
    
        
    