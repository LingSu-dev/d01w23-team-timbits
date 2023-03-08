from copy import copy

from cython import Py_ssize_t

from libc.stdlib cimport free, malloc

import numpy as np

cimport numpy as cnp
from numpy cimport int64_t, ndarray

cnp.import_array()

from pandas._libs cimport util

from pandas._libs.lib import is_scalar, maybe_convert_objects


cdef _check_result_array(object obj, Py_ssize_t cnt):

    if (util.is_array(obj) or
            (isinstance(obj, list) and len(obj) == cnt) or
            getattr(obj, 'shape', None) == (cnt,)):
        raise ValueError('Function does not reduce')


cdef class _BaseGrouper:
    cdef _check_dummy(self, object dummy):
        # both values and index must be an ndarray!

        values = dummy.values
        # GH 23683: datetimetz types are equivalent to datetime types here
        if (dummy.dtype != self.arr.dtype
                and values.dtype != self.arr.dtype):
            raise ValueError('Dummy array must be same dtype')
        if util.is_array(values) and not values.flags.contiguous:
            # e.g. Categorical has no `flags` attribute
            values = values.copy()
        index = dummy.index.values
        if not index.flags.contiguous:
            index = index.copy()

        return values, index

    cdef inline _update_cached_objs(self, object cached_typ, object cached_ityp,
                                    Slider islider, Slider vslider):
        if cached_typ is None:
            cached_ityp = self.ityp(islider.buf)
            cached_typ = self.typ(
                vslider.buf, dtype=vslider.buf.dtype, index=cached_ityp, name=self.name
            )
        else:
            # See the comment in indexes/base.py about _index_data.
            # We need this for EA-backed indexes that have a reference
            # to a 1-d ndarray like datetime / timedelta / period.
            object.__setattr__(cached_ityp, '_index_data', islider.buf)
            cached_ityp._engine.clear_mapping()
            object.__setattr__(cached_typ._mgr._block, 'values', vslider.buf)
            object.__setattr__(cached_typ._mgr._block, 'mgr_locs',
                               slice(len(vslider.buf)))
            object.__setattr__(cached_typ, '_index', cached_ityp)
            object.__setattr__(cached_typ, 'name', self.name)

        return cached_typ, cached_ityp

    cdef inline object _apply_to_group(self,
                                       object cached_typ, object cached_ityp,
                                       bint initialized):
        """
        Call self.f on our new group, then update to the next group.
        """
        cdef:
            object res

        cached_ityp._engine.clear_mapping()
        res = self.f(cached_typ)
        res = _extract_result(res)
        if not initialized:
            # On the first pass, we check the output shape to see
            #  if this looks like a reduction.
            initialized = True
            _check_result_array(res, len(self.dummy_arr))

        return res, initialized


cdef class SeriesBinGrouper(_BaseGrouper):
    """
    Performs grouping operation according to bin edges, rather than labels
    """
    cdef:
        Py_ssize_t nresults, ngroups

    cdef public:
        ndarray arr, index, dummy_arr, dummy_index
        object values, f, bins, typ, ityp, name

    def __init__(self, object series, object f, object bins, object dummy):

        assert dummy is not None  # always obj[:0]
        assert len(bins) > 0  # otherwise we get IndexError in get_result

        self.bins = bins
        self.f = f

        values = series.values
        if util.is_array(values) and not values.flags.c_contiguous:
            # e.g. Categorical has no `flags` attribute
            values = values.copy('C')
        self.arr = values
        self.typ = series._constructor
        self.ityp = series.index._constructor
        self.index = series.index.values
        self.name = series.name

        self.dummy_arr, self.dummy_index = self._check_dummy(dummy)

        # kludge for #1688
        if len(bins) > 0 and bins[-1] == len(series):
            self.ngroups = len(bins)
        else:
            self.ngroups = len(bins) + 1

    def get_result(self):
        cdef:
            ndarray arr, result
            ndarray[int64_t] counts
            Py_ssize_t i, n, group_size, start, end
            object res
            bint initialized = 0
            Slider vslider, islider
            object cached_typ = None, cached_ityp = None

        counts = np.zeros(self.ngroups, dtype=np.int64)

        if self.ngroups > 0:
            counts[0] = self.bins[0]
            for i in range(1, self.ngroups):
                if i == self.ngroups - 1:
                    counts[i] = len(self.arr) - self.bins[i - 1]
                else:
                    counts[i] = self.bins[i] - self.bins[i - 1]

        group_size = 0
        n = len(self.arr)

        vslider = Slider(self.arr, self.dummy_arr)
        islider = Slider(self.index, self.dummy_index)

        result = np.empty(self.ngroups, dtype='O')

        start = 0
        try:
            for i in range(self.ngroups):
                group_size = counts[i]
                end = start + group_size

                islider.move(start, end)
                vslider.move(start, end)

                cached_typ, cached_ityp = self._update_cached_objs(
                    cached_typ, cached_ityp, islider, vslider)

                res, initialized = self._apply_to_group(cached_typ, cached_ityp,
                                                        initialized)
                start += group_size

                result[i] = res

        finally:
            # so we don't free the wrong memory
            islider.reset()
            vslider.reset()

        result = maybe_convert_objects(result)
        return result, counts


cdef class SeriesGrouper(_BaseGrouper):
    """
    Performs generic grouping operation while avoiding ndarray construction
    overhead
    """
    cdef:
        Py_ssize_t nresults, ngroups

    cdef public:
        ndarray arr, index, dummy_arr, dummy_index
        object f, labels, values, typ, ityp, name

    def __init__(self, object series, object f, object labels,
                 Py_ssize_t ngroups, object dummy):

        # in practice we always pass obj.iloc[:0] or equivalent
        assert dummy is not None

        if len(series) == 0:
            # get_result would never assign `result`
            raise ValueError("SeriesGrouper requires non-empty `series`")

        self.labels = labels
        self.f = f

        values = series.values
        if util.is_array(values) and not values.flags.c_contiguous:
            # e.g. Categorical has no `flags` attribute
            values = values.copy('C')
        self.arr = values
        self.typ = series._constructor
        self.ityp = series.index._constructor
        self.index = series.index.values
        self.name = series.name

        self.dummy_arr, self.dummy_index = self._check_dummy(dummy)
        self.ngroups = ngroups

    def get_result(self):
        cdef:
            # Define result to avoid UnboundLocalError
            ndarray arr, result = None
            ndarray[int64_t] labels, counts
            Py_ssize_t i, n, group_size, lab, start, end
            object res
            bint initialized = 0
            Slider vslider, islider
            object cached_typ = None, cached_ityp = None

        labels = self.labels
        counts = np.zeros(self.ngroups, dtype=np.int64)
        group_size = 0
        n = len(self.arr)

        vslider = Slider(self.arr, self.dummy_arr)
        islider = Slider(self.index, self.dummy_index)

        result = np.empty(self.ngroups, dtype='O')

        start = 0
        try:
            for i in range(n):
                group_size += 1

                lab = labels[i]

                if i == n - 1 or lab != labels[i + 1]:
                    if lab == -1:
                        start += group_size
                        group_size = 0
                        continue

                    end = start + group_size
                    islider.move(start, end)
                    vslider.move(start, end)

                    cached_typ, cached_ityp = self._update_cached_objs(
                        cached_typ, cached_ityp, islider, vslider)

                    res, initialized = self._apply_to_group(cached_typ, cached_ityp,
                                                            initialized)

                    start += group_size

                    result[lab] = res
                    counts[lab] = group_size
                    group_size = 0

        finally:
            # so we don't free the wrong memory
            islider.reset()
            vslider.reset()

        # We check for empty series in the constructor, so should always
        #  have result initialized by this point.
        assert initialized, "`result` has not been initialized."

        result = maybe_convert_objects(result)

        return result, counts


cdef inline _extract_result(object res, bint squeeze=True):
    """ extract the result object, it might be a 0-dim ndarray
        or a len-1 0-dim, or a scalar """
    if hasattr(res, 'values') and util.is_array(res.values):
        res = res.values
    if util.is_array(res):
        if res.ndim == 0:
            res = res.item()
        elif squeeze and res.ndim == 1 and len(res) == 1:
            res = res[0]
    return res


cdef class Slider:
    """
    Only handles contiguous data for now
    """
    cdef:
        ndarray values, buf
        Py_ssize_t stride, orig_len, orig_stride
        char *orig_data

    def __init__(self, ndarray values, ndarray buf):
        assert values.ndim == 1
        assert values.dtype == buf.dtype

        if not values.flags.contiguous:
            values = values.copy()

        self.values = values
        self.buf = buf
        self.stride = values.strides[0]

        self.orig_data = self.buf.data
        self.orig_len = self.buf.shape[0]
        self.orig_stride = self.buf.strides[0]

        self.buf.data = self.values.data
        self.buf.strides[0] = self.stride

    cdef move(self, int start, int end):
        """
        For slicing
        """
        self.buf.data = self.values.data + self.stride * start
        self.buf.shape[0] = end - start

    cdef reset(self):

        self.buf.shape[0] = self.orig_len
        self.buf.data = self.orig_data
        self.buf.strides[0] = self.orig_stride


class InvalidApply(Exception):
    pass


def apply_frame_axis0(object frame, object f, object names,
                      const int64_t[:] starts, const int64_t[:] ends):
    cdef:
        BlockSlider slider
        Py_ssize_t i, n = len(starts)
        list results
        object piece
        dict item_cache

    # We have already checked that we don't have a MultiIndex before calling
    assert frame.index.nlevels == 1

    results = []

    slider = BlockSlider(frame)

    mutated = False
    item_cache = slider.dummy._item_cache
    try:
        for i in range(n):
            slider.move(starts[i], ends[i])

            item_cache.clear()  # ugh
            chunk = slider.dummy
            object.__setattr__(chunk, 'name', names[i])

            try:
                piece = f(chunk)
            except Exception:
                # We can't be more specific without knowing something about `f`
                raise InvalidApply('Let this error raise above us')

            # Need to infer if low level index slider will cause segfaults
            require_slow_apply = i == 0 and piece is chunk
            try:
                if not piece.index is chunk.index:
                    mutated = True
            except AttributeError:
                # `piece` might not have an index, could be e.g. an int
                pass

            if not is_scalar(piece):
                # Need to copy data to avoid appending references
                try:
                    piece = piece.copy(deep="all")
                except (TypeError, AttributeError):
                    piece = copy(piece)

            results.append(piece)

            # If the data was modified inplace we need to
            # take the slow path to not risk segfaults
            # we have already computed the first piece
            if require_slow_apply:
                break
    finally:
        slider.reset()

    return results, mutated


cdef class BlockSlider:
    """
    Only capable of sliding on axis=0
    """

    cdef public:
        object frame, dummy, index
        int nblocks
        Slider idx_slider
        list blocks

    cdef:
        char **base_ptrs

    def __init__(self, object frame):
        cdef:
            Py_ssize_t i
            object b

        self.frame = frame
        self.dummy = frame[:0]
        self.index = self.dummy.index

        self.blocks = [b.values for b in self.dummy._mgr.blocks]

        for x in self.blocks:
            util.set_array_not_contiguous(x)

        self.nblocks = len(self.blocks)
        # See the comment in indexes/base.py about _index_data.
        # We need this for EA-backed indexes that have a reference to a 1-d
        # ndarray like datetime / timedelta / period.
        self.idx_slider = Slider(
            self.frame.index._index_data, self.dummy.index._index_data)

        self.base_ptrs = <char**>malloc(sizeof(char*) * len(self.blocks))
        for i, block in enumerate(self.blocks):
            self.base_ptrs[i] = (<ndarray>block).data

    def __dealloc__(self):
        free(self.base_ptrs)

    cdef move(self, int start, int end):
        cdef:
            ndarray arr
            Py_ssize_t i

        # move blocks
        for i in range(self.nblocks):
            arr = self.blocks[i]

            # axis=1 is the frame's axis=0
            arr.data = self.base_ptrs[i] + arr.strides[1] * start
            arr.shape[1] = end - start

        # move and set the index
        self.idx_slider.move(start, end)

        object.__setattr__(self.index, '_index_data', self.idx_slider.buf)
        self.index._engine.clear_mapping()

    cdef reset(self):
        cdef:
            ndarray arr
            Py_ssize_t i

        # reset blocks
        for i in range(self.nblocks):
            arr = self.blocks[i]

            # axis=1 is the frame's axis=0
            arr.data = self.base_ptrs[i]
            arr.shape[1] = 0
