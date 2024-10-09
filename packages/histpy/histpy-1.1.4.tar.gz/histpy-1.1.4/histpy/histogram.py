import logging
logger = logging.getLogger(__name__)

import warnings

import numpy as np

import operator

import sys

from copy import copy,deepcopy

import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

from inspect import signature

import h5py as h5

from .axes import Axes,Axis
from .healpix_axis import HealpixAxis

from sparse import DOK, COO, GCXS, SparseArray

import astropy.units as u

from mhealpy import HealpixMap

class Histogram(object):
    """
    This is a wrapper of a numpy array with axes and a fill method. Sparse array from
    pydata's sparse package are also supported.
    
    Like an array, the histogram can have an arbitrary number of dimensions.

    Standard numpy array indexing is supported to get the contents 
    --i.e. :code:`h[:]`, :code:`h[4]`, :code:`h[[1,3,4]]`, :code:`h[:,5:50:2]]`,
    etc.--. However, the meaning of the :code:`-1` index is different. Instead of 
    counting from the end, :code:`-1` corresponds to the underflow bin. Similarly,
    an index equal to the number of bins corresponds to the overflow bin. 

    You can however give relative position with respect to :code:`h.end` 
    --e.g. :code:`h[0:h.end]` result in all regular bins, :code:`h[-1:h.end+1]` 
    includes also the underflow/overflow bins and :code:`h[h.end]` gives you the 
    contents of the overflow bin. The convenient aliases :code:`h.uf = -1`,
    :code:`h.of = e.end` and :code:`h.all = slice(-1,h.end+1)` --or 
    :code:`slice(0,h.end)` if the under/overflow are not tracked-- are provided.
    
    You can also use an :code:`Ellipsis` object (:code:`...`) at the end to specify that the
    contents from the rest of the dimension are to have the under and overflow
    bins included. e.g. for a 3D histogram :code:`h[1,-1:h.end+1,-1:h.end+1]
    = h[1,...]`. :code:`h[:]` returns all contents without under/overflow bins and
    h[...] returns everything, including those special bins.

    All axes track the under/overflow by default. You can specify that certain axes 
    will not with the :code:`track_overflow` flag. However, attempting to
    access an underflow/overflow bin when they are not tracked will result in 
    an IndexError.

    If :code:`sumw2` is not :code:`None`, then the histogram will keep track of 
    the sum of the weights squared --i.e. you better use this if you are using 
    weighted data and are concern about error bars--. You can access these with
    :code:`h.sumw2[item]`, where `item` is interpreted the same was a in :code:`h[item]`.
    :code:`h.bin_error[item]` return the :code:`sqrt(sumw2)` (or :code:`sqrt(contents)` is :code:`sumw2
    was not specified`).

    The operators :code:`+`, :code:`-`, :code:`*` and :code:`-` are available.
    Both other operand can be a histograms, a scalar or an array of appropiate size.
    Note that :code:`h += h0` is more efficient than 
    :code:`h = h + h0` since latter involves the instantiation of a new histogram.

    Args:
        edges (Axes or array): Definition of bin edges, Anything that can
            be processes by Axes. Lower edge value is included in the bin, 
            upper edge value is excluded.
        contents (array or SparseArray): Initialization of histogram contents. Might or might
            not include under/overflow bins. Initialize to 0 by default.
        sumw2 (None, bool or array): If True, it will keep track of the sum of
            the weights squared. You can also initialize them with an array
        labels (array of str): Optionally label the axes for easier indexing
        axis_scale (str or array): Bin center mode e.g. `"linear"` or `"log"`. 
            See ``Axis.axis_scale``.
        sparse (bool): Initialize an empty sparse histogram. Only relevant if no contents
            are provided.
        track_overflow (bool or array): Whether to allovate space to track the underflow and overflow bins.
            Provide a bool value for all axes, or an array of bool values for each axes. 
    """
            
    def __init__(self, edges, contents = None, sumw2 = None,
                 labels=None, axis_scale = None, sparse = None, unit = None, track_overflow = True):

        self._axes = Axes(edges, labels=labels, axis_scale = axis_scale)

        # Standarize track overflowe
        self._track_overflow = self._standarize_track_overflow(track_overflow)
        
        # Standarize contents (with under/overflow) or initialize them to zero.
        if contents is not None:

            # Deal with units
            if isinstance(contents, u.Quantity):

                if unit is None:
                    unit = contents._unit
                    contents = contents.value
                else:
                    contents = contents.to_value(unit)

            # Sparse
            self._sparse = isinstance(contents, SparseArray) 

            # Shape depending on overflow or not
            pads = []
            for n, (nbins, size, track_overflow) in enumerate(zip(self.axes.nbins, np.shape(contents), self.track_overflow())):
                if size == nbins == size:
                    if track_overflow:
                        pads += [(1,1)]
                    else:
                        pads += [(0,0)]
                elif size == nbins + 2:
                    if track_overflow:
                        pads += [(0,0)]
                    else:
                        raise ValueError(f"Axis {n} of contents has size {size} and {nbins} bins. It appears to have underflow and underflow contents, but the user specified those are not to be tracked for this axis.")
                else:
                    raise ValueError("Bins ({}) - contents {} size mismatch".format(self.axes.nbins,np.shape(contents)))

            self._contents = np.pad(contents, pads)
                        
        else:

            self._sparse = sparse

            contents_shape = [n+2*track_overflow for n,track_overflow in zip(self.axes.nbins, self.track_overflow())]

            if self.is_sparse:
                self._contents = DOK(contents_shape, fill_value = 0.)
            else:
                self._contents = np.zeros(contents_shape)


        # slice does not seems to work well with GCXS, force COO for now
        # Check https://github.com/pydata/sparse/issues/550
        if isinstance(self._contents, GCXS):
            self._contents = self._contents.asformat('coo')

        # Units
        if unit is not None:
            self._unit = u.Unit(unit)
        else:
            self._unit = None
        
        #Check if we'll keep track of the sum of the weights
        # Use same units as main histogram.
        w2units = None
        if self.unit is not None:
            w2units = self.unit*self.unit
        
        if sumw2 is None or sumw2 is False:
            self._sumw2 = None
        elif sumw2 is True:
            self._sumw2 = Histogram(self._axes,
                                    sparse = self.is_sparse,
                                    unit = w2units,
                                    track_overflow = self.track_overflow())
        elif isinstance(sumw2, Histogram):
            if self.axes != sumw2.axes and not np.array_equal(self.track_overflow(), sumw2.track_overflow()):
                raise ValueError("Is sumw2 is a Histogram is needs to have "
                                 "consistent axes and track_overflow parameter")

            self._sumw2 = sumw2
            
            self._sumw2.to(w2units)
        
        else:
            
            self._sumw2 = Histogram(self._axes, sumw2, unit = w2units, track_overflow = self.track_overflow())

        if self._sumw2 is not None and self.is_sparse != self._sumw2.is_sparse:
            raise ValueError("Both contents and sumw2 must be either "
                             "sparse or dense")

        # Special access methods
        self.sumw2 = None if self._sumw2 is None else self._get_sumw2(self)
        self.bin_error = self._get_bin_error(self)
        self.slice = self._slice(self)

    @property
    def unit(self):
        return self._unit

    def to(self, unit, equivalencies=[], update = True, copy = True):
        """
        Convert to other units.

        Args:
            unit (unit-like): Unit to convert to.
            equivalencies (list or tuple): A list of equivalence pairs to try if the units are not
                directly convertible.  
            update (bool): If ``update`` is ``False``, only the units will be changed without
                updating the contents accordingly
            copy (bool): If True (default), then the value is copied. Otherwise, a copy
                will only be made if necessary.
        """

        # Copy
        if copy:
            new = deepcopy(self)
        else:
            new = self
        
        # If no conversion is needed
        if not update:
            if unit is None:
                new._unit = None
            else:
                new._unit = u.Unit(unit)

            if new.sumw2 is not None:
                new._sumw2._unit = unit if unit is None else unit*unit
                
            return new

        # Compute factor
        if new.unit is None:
            
            if unit is None or unit == u.dimensionless_unscaled:
                factor = 1
            else:
                TypeError("Histogram without units")

        else:
            
            factor = new.unit.to(unit, equivalencies = equivalencies)

        # Update values
        new *= factor

        # Update units
        new._unit = unit

        if new._sumw2 is not None:
            new._sumw2._unit = unit*unit

        return new

    def _standarize_track_overflow(self, track_overflow):
        if isinstance(track_overflow, (bool, np.bool_)):
            track_overflow = np.full(self.ndim, track_overflow)
        elif isinstance(track_overflow, (np.ndarray, list, tuple)):
            track_overflow = np.array(track_overflow, ndmin = 1)
            if track_overflow.size != self.ndim:
                raise ValueError("track_overflow size doesn't match the number of dimensions")
        elif isinstance(track_overflow, dict):
            track_overflow = self.axes.expand_dict(track_overflow, default = True)
        else:
            raise TypeError("Track overflow can only be bool, an array or a dictionary.")

        return track_overflow

    def _match_track_overflow(self, old_track_overflow, new_track_overflow):
        """
        Compute slices and pads needed to go from one to the other
        """
    
        pads = []
        slices = []

        for old_track, new_track in zip(old_track_overflow, new_track_overflow):
            if old_track:

                if new_track:
                    slices += [slice(None)]
                else:
                    slices += [slice(1,-1)]

                pads += [(0,0)]

            else:
                slices += [slice(None)]

                if new_track:
                    pads += [(1,1)]
                else:
                    pads += [(0,0)]

        return tuple(slices), pads

    def track_overflow(self, track_overflow = None):
        """
        Obtain a list specifying wether each axis is tracking underflows and overflows.

        Args:
           track_overflow (bool, array or dict): Optional. Update whether or not the underflows and overflows
               are tracked.
        """
        if track_overflow is not None:
            # Update _contents shape appropiately
            old_track_overflow = self.track_overflow()
            new_track_overflow = self._standarize_track_overflow(track_overflow)

            slices, pads = self._match_track_overflow(old_track_overflow,
                                                      new_track_overflow)
            
            self._contents = self._contents[slices]

            if np.sum(pads) > 0:
                # Prevents new allocations
                self._contents = np.pad(self._contents, pads)
            
            self._track_overflow = new_track_overflow

            if self._sumw2 is not None:
                self._sumw2.track_overflow(new_track_overflow)

        return self._track_overflow
        
    
    @property
    def is_sparse(self):
        """
        Return True if the underlaying histogram contents are hold in a sparse array. False if it is a dense array.
        """
        return self._sparse

    def to_dense(self):
        """
        Return a dense representation of a sparse histogram
        """

        h_dense = deepcopy(self)
        
        if h_dense.is_sparse:
            h_dense._contents = self._contents.todense()

        if h_dense._sumw2 is not None:
            h_dense._sumw2 = h_dense._sumw2.to_dense()

        h_dense._sparse = False
            
        return h_dense

    # pydata sparse style
    todense = to_dense
    
    def to_sparse(self):
        """
        Return a sparse representation of a histogram.
        """

        h_sparse = deepcopy(self)
        
        if not h_sparse.is_sparse:
            h_sparse._contents = COO.from_numpy(self._contents)

        if h_sparse._sumw2 is not None:
            h_sparse._sumw2 = self._sumw2.to_sparse()

        h_sparse._sparse = True
            
        return h_sparse

    # pydata sparse style
    todense = to_dense

    @classmethod
    def concatenate(cls, edges, histograms, label = None, track_overflow = True):
        """
        Generate a Histogram from a list of histograms. The axes of all input
        histograms must be equal, and the new histogram will have one more
        dimension than the input. The new axis has index 0.

        Args:
            edges (Axes or array): Definition of bin edges of the new dimension
            histograms (list of Histogram): List of histogram to fill contents. 
                Might or might not include under/overflow bins.
            labels (str): Label the new dimension
            track_overflow (bool): Track underflow and overflow on the newly created axis.

        Return:
            Histogram
        """

        # Check all same axes
        old_axes = histograms[0].axes
        old_track_overflow = histograms[0].track_overflow()
        
        for hist in histograms:
            
            if hist.axes != old_axes:
                raise ValueError("The axes of all input histogram must equal")

            if not np.array_equal(hist.track_overflow(), old_track_overflow):
                raise ValueError("The track_overflow parameter of all input histograms must be equal")

        # Check new axis matches number of histograms,
        # with or without under/overflow
        new_axis = Axis(edges, label = label)

        if len(histograms) == new_axis.nbins:
            if track_overflow:
                padding = [(1,1)]+[(0,0)]*old_axes.ndim
            else:
                padding = [(0,0)]+[(0,0)]*old_axes.ndim
        elif len(histograms) == new_axis.nbins + 2:
            if track_overflow:
                padding = [(0,0)]+[(0,0)]*old_axes.ndim
            else:
                raise ValueError(f"I input histograms appear to have underflow and underflow contents, but the user specified those are not to be tracked for this axis.")
        else:
            raise ValueError("Mismatch between number of bins and "
                             "number of histograms")

        new_track_overflow = np.append(track_overflow, old_track_overflow)
        
        # Create new axes and new contents
        new_axes = Axes([new_axis] + [ax for ax in old_axes])

        # Check all sparse or all dense
        is_sparse = [h.is_sparse for h in histograms]

        if not np.all(is_sparse) and np.any(is_sparse):
            raise ValueError("Cannot concatenate a mix of sparse and dense histograms")

        # Unit conversion factor
        unit = histograms[0].unit

        if unit is None:
            # No factors, just check all histogram are the same
            
            for h in histograms[1:]:
                if h.unit is not None:
                    raise ValueError("Cannot concatenate maps with and without units.")
            
            unit_factor = 1
            
        else:

            unit_factor = [1]

            for h in histograms[1:]:
                if h.unit is None:
                    raise ValueError("Cannot concatenate maps with and without units.")
                else:
                    unit_factor += [h.unit.to(unit)]

            if np.all(unit_factor == 1):
                unit_factor = 1
            
        # Update contents, with padding and units if needed
        if unit_factor == 1:
            contents = np.concatenate([h._contents[None] for h in histograms])
        else:
            contents = np.concatenate([factor*h._contents[None]
                                       for factor,h in zip(unit_factor,histograms)])

        contents = np.pad(contents, padding)
        
        # New sumw2
        has_sumw2 = [h.sumw2 is not None for h in histograms] 
        if np.all(has_sumw2):

            if unit_factor == 1:
                sumw2 = np.concatenate([h._sumw2._contents[None] for h in histograms])
            else:
                sumw2 = np.concatenate([factor*factor*h.sumw2_._contents[None]
                                        for factor,h in zip(unit_factor,histograms)])
            
            sumw2 = np.pad(sumw2, padding)

        else:

            sumw2 = None

            if np.any(has_sumw2):
                # A mix. Drop and warn
                logger.warning("Not all input histogram have sum of weights "
                               "squared. sumw2 will be dropped")
        
        return Histogram(new_axes, contents, sumw2, unit = unit, track_overflow = new_track_overflow)
            
    @property
    def ndim(self):
        return self._axes.ndim
            
    def clear(self):
        """
        Set all counts to 0
        """

        if self.unit is None:
            self[...] = 0
        else:
            self[...] = 0*self.unit            

        if self._sumw2 is not None:
            self._sumw2.clear()
                    
    def __eq__(self, other):
        # Histogram is completely defined by axes and contents

        return (self._axes == other._axes
                and
                np.array_equal(self._track_overflow, other._track_overflow)
                and
                np.all(self._contents == other._contents)
                and
                self.unit == other.unit
                and
                self._sumw2 == other._sumw2)

    def __array__(self):

        return np.array(self.contents)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):

        if len(inputs) != 1 or inputs[0] is not self:
            raise NotImplementedError(
                "Only numpy functions with a single operand are supported "
                "e.g. np.sin(h), np.sum(h). Call h.contents explicitly to "
                "get the corresponding array e.g. np.add(h.contents, a)")
        
        return ufunc(self.contents, *inputs[1:], **kwargs)
        
    def __array_function__(self, func, types, args, kwargs):

        # Only support basic functions on a single operand like np.sum(h)

        if len(args) != 1 or args[0] is not self:
            raise NotImplementedError(
                "Only numpy functions with a single operand are supported "
                "e.g. np.sin(h), np.sum(h). Call h.contents explicitly to "
                "get the corresponding array e.g. np.add(h.contents, a)")
        
        return func(self.contents, *args[1:], **kwargs)

    class _NBINS():        
        '''
        Convenience class that will expand to the number of bins of a 
        given dimension. 

        The trick is to overload the -/+ operators such than 
        h.end +/- offset (h being an instance of Histogram and 'end' an 
        static instance of Histogram._NBINS) returns an instance of _NBINS 
        itself, which stores the offset. The [] operator can then detect that
        the input is an instance of _NBINS and convert it into an integer with
        respect to the size of the appropiate axis.
        '''
        
        def __init__(self, offset = 0):
            self.offset = offset
    
        def __add__(self, offset):
            return self.__class__(offset)
    
        def __sub__(self, offset):
            return self + (-offset)
        
    end = _NBINS()
    
    # Convenient aliases
    uf = -1
    of = end

    class _ALL():
        '''
        Expands to slice(-1, end+1) is the axis track under/overflow, 
        and slice(0, end) otherwise
        '''
    
    all = _ALL()
    
    def _prepare_indices(self, indices):
        '''
        Prepare indices for it use in __getitem__ and __setitem__ 
        --i.e. [] overloading --
        
        See class help.
        '''
        
        def _prepare_index(index, dim):
            '''
            Modify index for a single axis to account for under/overflow, 
            as well as to catch instances of _NBINS (see description above)
            This depend on the number of bins in the axis of a given 
            dimension (dim)
            '''

            overflow_offset = 1 if self._track_overflow[dim] else 0

            if isinstance(index,slice):

                # Both start and stop can be either None, an instance of
                # _NBINS or an integer
                index = slice(overflow_offset
                              if index.start is None
                              else
                              self.axes[dim].nbins + index.start.offset + overflow_offset
                              if isinstance(index.start, self._NBINS)
                              else
                              index.start + overflow_offset,
                              
                              self.axes[dim].nbins + overflow_offset
                              if index.stop is None
                              else
                              self.axes[dim].nbins + index.stop.offset + overflow_offset
                              if isinstance(index.stop, self._NBINS)
                              else
                              index.stop + overflow_offset,
                              
                              index.step)
                
                # Check bounds. Note index is the _contents index at this point
                if index.start < 0 or index.stop > self._contents.shape[dim]:
                    raise IndexError("Bin index out of bounds")
                
                return index
            
            elif isinstance(index, (np.integer, int)):

                index = index + overflow_offset
                
                # Check bounds. Note index is the _contents index at this point
                if index < 0 or index > self._contents.shape[dim]:
                    raise IndexError("Bin index out of bounds")

                return index

            elif isinstance(index, self._NBINS):

                # Referece with respect to nbins
                return _prepare_index(self.axes[dim].nbins + index.offset, dim)

            elif isinstance(index, self._ALL):

                # All bins. Adjust depending on whether under/overflow are tracked or not
                if self._track_overflow[dim]:
                    return _prepare_index(slice(-1, self.end+1), dim)
                else:
                    return _prepare_index(slice(0, self.end), dim)
            
            elif isinstance(index, (np.ndarray, list, tuple, range)):

                # Note: this will return a copy, not a view
                    
                # Handle references with respecto to nbins
                index = np.array(index)

                if index.dtype == bool:
                    # Mask. Pad under/overflow

                    return np.pad(index,
                                  tuple((1,1) if (track and size == nbins) else (0,0)
                                   for size,nbins,track in zip(index.shape, self.axes.nbins, self._track_overflow)),
                                  constant_values = False)
                    
                else:
                    # Indices

                    index_shape = index.shape

                    index = index.flatten()

                    index =  [self.axes[dim].nbins + i.offset + overflow_offset
                              if isinstance(i,self._NBINS) else
                              i + overflow_offset
                              for i in index]

                    index = np.reshape(index, index_shape)
                    
                    # Check bounds. Note index is the _contents index at this point/
                    if (np.any(index < 0) or
                         np.any(index > self._contents.shape[dim])):
                        raise IndexError("Bin index out of bounds")
                        
                    return index
                    
            else:
                raise TypeError("Index can only be an int, slice, list or array")
        
        if isinstance(indices, tuple):

            # Get the rest of the dimensions with under/overflow user used ...
            if indices[-1] is Ellipsis:
                extra_indices = tuple(slice(-int(self._track_overflow[dim]),
                                            self.axes[dim].nbins+int(self._track_overflow[dim]))
                                      for dim in range(len(indices)-1, self.ndim))

                indices = self._prepare_indices(indices[:-1] + extra_indices)

                return indices
            
            # Standard way. All other ways end up here after recursion
            indices = tuple(_prepare_index(index, dim)
                            for dim,index in enumerate(indices))

            # Remove under/overflow of the rest of the dimensions
            indices += tuple(_prepare_index(slice(None), dim) for dim in
                             range(len(indices), self.ndim))

            return indices

        elif isinstance(indices, dict):

            return self._prepare_indices(self.axes.expand_dict(indices, default = slice(None)))

        else:
            # Single axis
            return self._prepare_indices(tuple([indices]))

    # Access methods
    # DO NOT use _contents directly, all goes through here
    # to handle sparse arrays correctly. Specifically, do not
    # to operations on self._contents (*,+,slice, concatenate, etc.)
    # since DOK is very inneficient. Similarly, COO is readonly,
    # so trying to use __setitem__ on it will raise an error.
    # Assignments to _contents iteself are fine (e.g. self._contents = X)

    def __setitem__(self, indices, new_contents):

        # Make it mutable if needed
        if self.is_sparse:
            self._contents = self._contents.asformat('dok')

        indices = self._prepare_indices(indices)

        try:
            self._contents[indices] = self._strip_units(new_contents)
        except (IndexError, ValueError) as e:

            if self.is_sparse:
                # Check if advance indexing is being used
                for index in indices:
                    if isinstance(index, np.ndarray):
                        logger.warning(
                            "Advance indexing is not yet be fully supported "
                            "for sparse arrays. See "
                            "https://github.com/pydata/sparse/issues/1 and "
                            "https://github.com/pydata/sparse/issues/114")

                        break
            raise e

    @property
    def _getitem_units(self):
        # Usually, if the histogram has units, [] and interp would return units.
        # Unfortunatenly SparseMatrix is not compatible with Quantity, so in sparse
        # mode only the values is returned
        return not (self.unit is None or self.is_sparse)
        
    def __getitem__(self, indices):

        # Go back to efficient read-only if needed
        if self.is_sparse:
            self._contents = self._contents.asformat('coo')

        indices = self._prepare_indices(indices)

        try:
            if self._getitem_units:
                return self._contents[indices]*self.unit
            else:              
                return self._contents[indices]
        except IndexError as e:

            if self.is_sparse:
                # Check if advance indexing is being used
                for index in indices:
                    if isinstance(index, np.ndarray):
                        logger.warning(
                            "Advance indexing is not yet be fully supported "
                            "for sparse arrays. See "
                            "https://github.com/pydata/sparse/issues/1 and "
                            "https://github.com/pydata/sparse/issues/114")

                        break

            raise e

    class _special_getitem:
        """
        This allows to use regular indexing for special access methods. 
        e.g. h.sumw2[] and h.bin_error[]
        """
        
        def __init__(self, hist):
            self._hist = hist

        def __getitem__(self, item):
            raise NotImplmentedError

        def __array__(self):
            return self.contents

        @property
        def contents(self):
            return self[:]
    
        @property
        def full_contents(self):
            return self[...]
        
    class _get_sumw2(_special_getitem):
        """
        Return the sum fo the weights squares. If sumw2 is not stored, then
        it assumed all the weights of all entries equal 1.
        """
        
        def __getitem__(self, item):

            return self._hist._sumw2[item]
            
        def __setitem__(self, indices, new_sumw2):

            if self._hist._sumw2 is None:
                raise ValueError("Histogram does not have sumw2")

            self._hist._sumw2[indices] = new_sumw2
            
    class _get_bin_error(_special_getitem):
        """
        Return the sqrt of sumw2
        """
        
        def __getitem__(self, item):
            if self._hist._sumw2 is not None:
                return np.sqrt(self._hist._sumw2[item])
            else:

                if self._hist._getitem_units:
                    # Fake units
                    return np.sqrt(np.abs(self._hist[item].value))*self._hist.unit
                else:
                    return np.sqrt(np.abs(self._hist[item]))
                
                return np.sqrt(np.abs(self._hist[item]))
                        
        def __setitem__(self, indices, new_bin_error):

            if self._hist._sumw2 is None:
                raise ValueError("Histogram does not have sumw2")

            self._hist._sumw2[indices] = np.power(new_bin_error, 2)

    @property
    def contents(self):
        """
        Equivalent to :code:`h[:]`. Does not include under and overflow bins.
        """
        
        return self[:]
        
    @property
    def full_contents(self):
        """
        Equivalent to :code:`h[...]`. The size of each axis can be nbins or nbins+2, depending on
        the track_overflow parameters
        """
        return self[...]
    
    @property
    def axes(self):
        """
        Underlaying axes object
        """
        
        return self._axes

    @property
    def axis(self):
        """
        Equivalent to :code:`self.axes[0]`, but fails if :code:`ndim > 1`
        """

        if self.ndim > 1:
            raise ValueError("Property 'axis' can only be used with 1D "
                            "histograms. Use `axes` for multidimensional "
                            "histograms")

        return self.axes[0]

    @axis.setter
    def axis(self, new):

        self.axes[0] = new

        if self._sumw2 is not None:
            self._sumw2.axis = new
        
    @property
    def nbins(self):

        if self.ndim == 1:
            return self.axes[0].nbins
        else:
            return self.axes.nbins
            
    def interp(self, *values):
        """
        Get a linearly interpolated content for a given set of values
        along each axes. The bin contents are assigned to the center of the bin.
        
        Args:
            values (float or array): Coordinates within the axes to interpolate.
                 Must have the same size as `ndim`. Input values as
                 `(1,2,3)` or `([1,2,3])`

        Return:
            float
        """

        bins,weights = self._axes.interp_weights(*values)

        if bins.ndim == 1:
            # Single point case

            content = 0
            
            for bin,weight in zip(bins, weights):
                content += weight*self._strip_units(self[bin])

        else:

            # Multi

            content = np.zeros(shape = bins.shape[1:])
            
            for bin,weight in zip(bins, weights):

                # Each b can be a tuple
                bin = np.array(bin, ndmin = 1)

                bin_values = [self._strip_units(self[b]) for b in bin.flatten()]
                bin_values = np.reshape(bin_values, bin.shape)
                
                content += weight*bin_values

        if self.unit is not None:
            content = content * self.unit
                
        return content

    def find_bin(self, *args, **kwargs):
        return self.axes.find_bin(*args, **kwargs)

    def _strip_units(self, quantity):

        if isinstance(quantity, u.Quantity):

            if quantity.unit == u.dimensionless_unscaled:
                return quantity.value
            
            if self.unit is None:
                return u.UnitConversionError("Histogram without units")

            return quantity.to_value(self.unit)

        elif isinstance(quantity, u.UnitBase):

            if quantity == u.dimensionless_unscaled:
                # Do no crash is self.unit is None
                return 1

            return quantity.to(self.unit)
        
        else:

            if self.unit is not None:
                raise u.UnitConversionError("Specify units")
            
            return quantity

    def fill(self, *values, weight = None):
        '''
        And an entry to the histogram. Can be weighted.

        Follow same convention as find_bin()

        Args:
            values (float or array): Value of entry
            weight (float): Value weight in histogram. Defaults to 1 in whatever units
                the histogram has
        
        Note:
            Note that weight needs to be specified explicitely by key, otherwise
            it will be considered a value an a IndexError will be thrown.
        '''

        indices = self.find_bin(*values)

        # Standarize if single axis
        if not isinstance(indices, tuple):
            indices = (indices,)
        
        # Allow for some values with different shape but broadcastable
        indices = np.broadcast_arrays(*indices)

        # Convert units if needed
        if weight is None:
            weight = 1
        else:
            weight = self._strip_units(weight)
        
        # Flatten all
        indices = tuple([i.flatten() for i in indices])
        weight = np.array(weight).flatten()
        
        # Make it work with multiple entries at one
        new_axes = tuple(np.arange(np.ndim(indices), 2))
        indices = np.expand_dims(indices, new_axes).transpose()
        weight = np.broadcast_to(weight, indices.shape[0])

        # Work with _contents directly. More efficient. 
        # We don't need all the checks from self._prepare_indices
        # because these come from find_bin. This is faster.
        # We just need to adjust them based on whether tracking under/overflow or not...
        indices += self._track_overflow[None]
        # ...and to throw away those which are under/overflow, only for
        # those axes that do not track under/over (indices here are for _contents[])
        mask = np.all(np.logical_and(indices >= 0,
                                     indices <= np.array(self._contents.shape)[None]),
                      axis = 1)
        indices = indices[mask]
        weight = weight[mask] 
        
        if self.is_sparse:

            # Filling a dict directly. Sparse has a lot of overhead checking
            # that the indices are valid in the __setitem__ method, but I'm
            # already checking this with _prepare_indices
            # This is faster than doing self._contents[i] += w
            d_new_contents = {}

            for i,w in zip(indices, weight):
                # Add if already exists, otherwise create new entry
                try:
                    elem = d_new_contents[tuple(i)]
                    elem[0] += w
                    elem[1] += w*w
                except KeyError:
                    d_new_contents[tuple(i)] = [w, w*w]

            # Convert dict to sparse array
            coords = np.transpose(list(d_new_contents.keys()))
            data = np.array(list(d_new_contents.values()))
            
            new_contents = COO(coords = coords, data = data[:,0],
                               shape = self._contents.shape)

            # Add
            self._contents = self._contents.asformat('coo')

            self._contents += new_contents

            if self._sumw2 is not None:
                self._sumw2._contents = self._sumw2._contents.asformat('coo')

                new_contents_sqr = COO(coords = coords, data = data[:,1],
                               shape = self._contents.shape)
                    
                self._sumw2._contents += new_contents_sqr
            
        else:

            # Add directly for dense array
            for i,w in zip(indices, weight):
                self._contents[tuple(i)] += w

            if self._sumw2 is not None:
                for i,w in zip(indices, weight):
                    self._sumw2._contents[tuple(i)] += w*w

    def project(self, *axis):
        """
        Return a histogram consisting on a projection of the current one

        Args:
            axis (int or str or list): axis or axes onto which the
                histogram will be projected --i.e. will sum up over the
                other dimensiones--. The axes of the new histogram will
                have the same order --i.e. you can transpose axes--

        Return:
            Histogram: Projected histogram
        """
        if self.ndim == 1:
            raise ValueError("Can't project a 1D histogram. "
                             "Consider using np.sum(h) or np.sum(h.full_contents) (with under/overflow)")

        #Standarize
        if len(axis) == 1 and \
           isinstance(axis[0], (list, np.ndarray, range, tuple)):
            # Got a sequence
            axis = axis[0]
        
        axis = np.array(self._axes.label_to_index(axis))
        
        if len(np.unique(axis)) != len(axis):
            raise ValueError("An axis can't repeat")

        # Project
        sum_axes = tuple(dim for dim in range(0, self.ndim) if dim not in axis)

        if len(sum_axes) == 0:
            new_contents = deepcopy(self.full_contents)
        else:
            new_contents = self.full_contents.sum(axis = sum_axes)

        # Transpose the contents to match the order of the axis provided by the
        # the user, which are currently sorted
        new_contents = np.transpose(new_contents,
                                    axes = np.argsort(np.argsort(axis)))

        new_sumw2 = None
        if self._sumw2 is not None:
            new_sumw2 = self._sumw2.project(axis).full_contents

        return Histogram(edges = self._axes[axis],
                         contents = new_contents,
                         sumw2 = new_sumw2,
                         unit = self.unit,
                         track_overflow = self._track_overflow[axis])

    def clear_overflow(self, axes = None):
        """
        Set all overflow bins to 0, including sumw2

        Args:
            axes (None or array): Axes number or labels. All by default
        """
        if axes is None:
            axes = range(self.ndim)
        elif np.isscalar(axes):
            axes = [axes]
        
        axes = self._axes.label_to_index(axes)

        for n in axes:

            if self._track_overflow[n]:
                indices = self.expand_dict({n:self.of}, self.all)
                if self.unit is None:
                    self[indices] = 0
                else:
                    self[indices] = 0*self.unit

        if self._sumw2 is not None:
            self._sumw2.clear_overflow(axes)
        
    def clear_underflow(self, axes = None):
        """
        Set all overflow bins to 0, including sumw2

        Args:
            axes (None or array): Axes number or labels. All by default
        """
        if axes is None:
            axes = range(self.ndim)
        elif np.isscalar(axes):
            axes = [axes]

        axes = self._axes.label_to_index(axes)

        for n in axes:

            if self._track_overflow[n]:
                indices = self.expand_dict({n:self.uf}, self.all)
                if self.unit is None:
                    self[indices] = 0
                else:
                    self[indices] = 0*self.unit

        if self._sumw2 is not None:
            self._sumw2.clear_underflow(axes)        

    def clear_underflow_and_overflow(self, *args, **kwargs):
        """
        Set all underflow and overflow bins to 0, including sumw2

        Args:
            axes (None or array): Axes number or labels. All by default
        """

        self.clear_underflow(*args, **kwargs)
        self.clear_overflow(*args, **kwargs)        
            
    class _slice:
        """
        Return a histogram which is a slice of the current one
        """

        def __init__(self, hist):
            self._hist = hist

        def __getitem__(self, item):

            # Standarize indices into slices
            indices = self._hist._prepare_indices(item)
            indices = tuple(slice(i,i+1) if isinstance(i, (int, np.integer)) else i for i in indices)

            # Check indices and either pad or use under/overflor

            # If under/overflow are including, will use them instead of pads
            padding = np.array([[1,1] if tracked else [0,0]
                                for tracked in self._hist._track_overflow])

            axes_indices = np.empty(self._hist.ndim, dtype = 'O')
            new_nbins = np.empty(self._hist.ndim, dtype = int)
            
            for ndim,(index, axis) in enumerate(zip(indices,
                                                    self._hist.axes)):

                track_overflow = self._hist._track_overflow[ndim]
                overflow_offset = int(track_overflow)

                # Sanity checks
                if not isinstance(index, slice):

                    raise TypeError("Only slices and integers allowed in slice[]")
               
                start,stop,stride = index.indices(axis.nbins+2*overflow_offset)

                if stride != 1:
                    raise ValueError("Step must be 1 when getting a slice."
                                     "Alertnatively us rebin().")

                if start == stop:
                    raise ValueError("Slice must have a least one bin in "
                                     "all dimensions. Alternatively use project().")

                if start > stop:
                    raise ValueError("Slices cannot reverse the bin order.")

                # Handle under/overflow
                if track_overflow:
                    # Axes don't have under/overflow
                    axis_start = max(start - 1, 0)
                    axis_stop =  min(stop,      axis.nbins + 1)

                    if start == 0:

                        if stop-start == 1:
                            raise ValueError("The slice cannot contain only the "
                                             "underflow bin")

                        padding[ndim, 0] = 0

                    
                    if stop == axis.nbins + 2:

                        if stop-start == 1:
                            raise ValueError("The slice cannot contain only the "
                                             "overflow bin")
                        
                        padding[ndim, 1] = 0                        

                else:
                    axis_start = start
                    axis_stop = stop + 1
                    
                    
                axes_indices[ndim] = slice(axis_start, axis_stop)
                new_nbins[ndim] = stop-start
                
            axes_indices = tuple(axes_indices)
            # Get new contents. Pad is underflow/overflow are not included
            new_contents = self._hist.full_contents[indices]
            new_contents = np.pad(new_contents, padding)
            
            # New Axes
            new_axes = []

            for axis,index in zip(self._hist.axes,axes_indices):

                new_axis_kw =  {'edges': axis.edges[index],
                                'label': axis.label}
                
                if isinstance(axis, HealpixAxis):
                    new_axis_kw['nside'] = axis.nside
                    new_axis_kw['scheme'] = axis.scheme
                    new_axis_kw['coordsys'] = axis.coordsys
                else:
                    new_axis_kw['scale'] = axis.axis_scale

                new_axes += [axis.__class__(**new_axis_kw)]
                
            # Sum weights squared
            new_sumw2 = None
            if self._hist._sumw2 is not None:
                new_sumw2 = self._hist._sumw2.slice[item]

            # Create new histogram
            return Histogram(edges = new_axes,
                             contents = new_contents,
                             sumw2 = new_sumw2,
                             unit = self._hist.unit,
                             track_overflow = self._hist._track_overflow)

    def _unit_operation(self, other, operation):
        """
        Get the value part of the other operand and the new unit of the histogram
        """

        # Separate between value and unit
        if isinstance(other, Histogram):
            other_unit = other.unit
            other_value = other # It will be handled as a regular HealpixMap
        elif isinstance(other, u.Quantity):
            other_unit = other.unit
            other_value = other.value
        elif isinstance(other, u.UnitBase):
            other_unit = other
            other_value = 1
        else:
            # float, int, array, list
            other_unit = None
            other_value = np.array(other)

        if self.unit is None and other_unit is  None:
            # If neither operand have units, do nothing else
            return other_value, None

        # Adjust other_value and self.unit depending on the operand

        # Standarize dimensionless
        if other_unit is None:
            other_unit = u.dimensionless_unscaled

        old_unit = self.unit
        if old_unit is None:
            old_unit = u.dimensionless_unscaled
            
        # For * and / the conversion factor is stored in the unit itself
        # ** only accepts scalar dimensionaless quantities, it will crash anyway
        # The idencity operator (for the raterizer) doesn't use the other's units
        if operation in [operator.add, operator.iadd,
                         operator.sub, operator.isub]:
            
            # +, -
            # We need to correct the value by the conversion unit
            # No change in units
            other_value = other_value * other_unit.to(old_unit)
            new_unit = old_unit
            
        elif operation in [operator.mul, operator.imul,
                           operator.truediv, operator.itruediv,
                           operator.floordiv, operator.ifloordiv]:

            # *, /
            # The conversion factor is stored in the unit itself
            new_unit = operation(old_unit, other_unit)
                
        else: 

            raise ValueError("Operation not supported")
            
        return other_value, new_unit

    
    def _ioperation(self, other, operation):

        sum_operation = operation in [operator.isub, operator.iadd,
                                      operator.sub,  operator.add]

        product_operation = operation in [operator.imul, operator.itruediv,
                                          operator.mul, operator.truediv]

        # Get the value part of other and the new unit the result should have
        other, new_unit = self._unit_operation(other, operation) 

        # Temporarily disable units
        self.to(None, update = False, copy = False)
        
        if isinstance(other, Histogram):

            # Temporarily disable units
            other_unit = other._unit
            other.to(None, update = False, copy = False)
            
            # Another histogram, same axes
            if self.axes != other.axes:
                raise ValueError("Axes mismatch")

            # Match overflow/underflow
            other_contents = other.full_contents

            slices, pads = self._match_track_overflow(other._track_overflow,
                                                      self._track_overflow)

            other_contents = other_contents[slices]

            if np.sum(pads) > 0:
                # Prevents new allocations
                other_contents = np.pad(other_contents, pads)
            
            new_contents = operation(self.full_contents, other_contents)

            if self._sumw2 is not None or other._sumw2 is not None:

                if self._sumw2 is None or other._sumw2 is None:
                    logger.warning("Operation between histograms with and "
                                   "without sumw2. Using default.")

                # Match over/underflow
                other_sumw2_contents = other.sumw2.full_contents

                other_sumw2_contents = other_sumw2_contents[slices]
                
                if np.sum(pads) > 0:
                    # Prevents new allocations
                    other_sumw2_contents = np.pad(other_sumw2_contents, pads)
                    
                if sum_operation:

                    self._sumw2._contents = self.sumw2.full_contents + other_sumw2_contents

                elif product_operation:

                    # Error of either f = A*B or f = A/B is
                    # f_err^2 = f^2 * ((A_err/A)^2 + (B_err/B)^2)
                    
                    relvar = (self.sumw2.full_contents/
                              (self.full_contents*self.full_contents))

                    other_relvar = (other_sumw2_contents/
                                    (other_contents*other_contents))
                    
                    self._sumw2._contents = (new_contents*new_contents*
                                             (relvar + other_relvar))

                else:
                    
                    raise ValueError("Operation not supported")

            self._contents = new_contents
            
            # Restore units
            other.to(other_unit, update = False, copy = False)

        else:

            # By scalar or array. Can be broadcasted

            if np.ndim(other) != 0:

                # Array. With or without under/overflow bins
                if not isinstance(other, (np.ndarray, SparseArray)):
                    other = np.array(other)

                if other.ndim != self.ndim:
                    raise ValueError("Operand number of dimensions ({}) does not"
                                     "match number of axes ({})".format(other.ndim,
                                                                        self.ndim))
                
                pad = []

                for n,(length,nbins,track_overflow) in enumerate(zip(other.shape, self.axes.nbins,self._track_overflow)):

                    overflow_offset = int(track_overflow)
                    
                    if length == 1 or length == nbins+2*overflow_offset:
                        # Single element axis can be broadcasted as is
                        # OR array includes under/overflow
                        pad += [(0,)]
                    elif track_overflow and length == nbins:
                        # Missing under and overflow, but right shape.
                        pad += [(1,)]
                    else:
                        raise ValueError("Could not broadcast array of shape {} "
                                         "to histogram with nbins "
                                         "{}".format(other.shape,
                                                     self.axes.nbins))

                if np.sum(pad) > 0:
                    # Prevents new allocations
                    other = np.pad(other, pad)
                                    
            self._contents = operation(self.full_contents, other)

            if self._sumw2 is not None:

                if sum_operation:

                    # sumw2 remains constant if summing/substracting a constant
                    pass
                    
                elif product_operation:
                    
                    self._sumw2 = operation(operation(self._sumw2, other), other)
                    
                else:
                    
                    raise ValueError("Operation not supported")

        # Restore unit
        self.to(new_unit, update = False, copy = False)
        
        return self

    def _operation(self, other, operation):

        new = deepcopy(self)

        new._ioperation(other, operation)

        return new
    
    def __imul__(self, other):

        return self._ioperation(other, operator.imul)
                
    def __mul__(self, other):

        return self._operation(other, operator.mul)

    def __rmul__(self, other):

        return self*other

    def __itruediv__(self, other):

        return self._ioperation(other, operator.itruediv)

    def __truediv__(self, other):

        return self._operation(other, operator.truediv)

    def __rtruediv__(self, other):
        """
        Divide a scalar by the histogram
        """

        if not np.isscalar(other):
            raise ValueError("Inverse operation can only occur between "
                             "histograms or a histogram and a scalar")

        new = deepcopy(self)

        # Simple change of unit in this case. Other can't be Quantity or Unit
        new_unit = None
        new_w2unit = None
        
        if new.unit is not None:
            new_unit = (1/new.unit).unit
            new_w2unit = new_unit**2

        # Temporarily disable unit
        new.to(None, update = False, copy = False)
        
        # Error propagtion of f = b/A (where b is constant, no error) is:
        # f_err^2 = f^2 (A_err/A)^2

        if new._sumw2 is not None:
            new._sumw2._contents = (new._sumw2.full_contents * other*other /
                                    np.power(new.full_contents, 4))

        new._contents = other/new.full_contents

        # Set units
        new.to(new_unit, update = False, copy = False)
        
        return new
    
    def __iadd__(self, other):

        return self._ioperation(other, operator.iadd)
            
    def __add__(self, other):

        return self._operation(other, operator.add)

    def __radd__(self, other):

        return self + other

    def __neg__(self):

        new = deepcopy(self)

        new._contents = -1*new.full_contents

        # No change to sumw2 or units

        return new
    
    def __isub__(self, other):

        return self._ioperation(other, operator.isub)
            
    def __sub__(self, other):

        return self._operation(other, operator.sub)

    def __rsub__(self, other):

        return -self + other

    def _comparison_operator(self, other, operation):

        if not self._getitem_units:
            other = self._strip_units(other)

        return operation(self.contents, other)
    
    def __lt__(self, other):
        return self._comparison_operator(other, operator.lt)
    
    def __le__(self, other):
        return self._comparison_operator(other, operator.le)
    
    def __gt__(self, other):
        return self._comparison_operator(other, operator.gt)
    
    def __ge__(self, other):
        return self._comparison_operator(other, operator.ge)
    
    def expand_dims(self, *args, **kwargs):
        """
        Same as h.axes.expand_dims().
        """
        return self._axes.expand_dims(*args, **kwargs)
    
    def broadcast(self, *args, **kwargs):
        """
        Same as h.axes.broadcast().
        """
        return self._axes.broadcast(*args, **kwargs)
    
    def expand_dict(self, *args, **kwargs):
        """
        Same as h.axes.expand_dict().
        """
        return self._axes.expand_dict(*args, **kwargs)

    def rebin(self, *ngroup):

        """
        Rebin the histogram by grouping multiple bins into a single one.

        Args:
            ngroup (int or array): Number of bins that will be combined for each 
                bin of the output. Can be a single number or a different number
                per axis. A number <0 indicates that the bins will start to be
                combined starting from the last one.

        Return:
            Histogram
        """

        # === Contents ===

        # New number of bins.
        ngroup = np.squeeze(ngroup)
        ngroup_sign = np.broadcast_to(np.sign(ngroup), (self.ndim))
        ngroup = np.broadcast_to(np.abs(ngroup), (self.ndim))
        
        new_nbins = np.floor(self.axes.nbins / ngroup).astype(int)

        if any(ngroup == 0):
            raise ValueError("ngroup cannot be 0")
        
        # Add padding so under/overflow bins match ngroup including "leftover bins"
        padding =  [(ngroup_i - int(track_overflow_i),
                    ngroup_i - (int(track_overflow_i) + nbins_i - new_nbins_i * ngroup_i))
                    for ngroup_i, nbins_i, new_nbins_i, track_overflow_i
                    in zip(ngroup, self.axes.nbins, new_nbins, self._track_overflow)]

        # Rever direction if needed
        padding = [pad[::direction]
                   for pad,direction
                   in zip(padding,ngroup_sign)]
        
        new_contents = np.pad(self.full_contents, padding)

        # Sum every ngroup elements by reshaping first
        new_shape = np.empty(2*self.ndim, dtype = int)
        new_shape[0::2] = new_nbins+2
        new_shape[1::2] = ngroup
        new_shape = tuple(new_shape)
        sum_axis = tuple(np.arange(1,2*self.ndim,2))
        new_contents = np.sum(new_contents.reshape(new_shape), axis = sum_axis)

        # Remove under/overflow bins if not tracked
        new_contents = new_contents[tuple(slice(None)
                                          if tracked else
                                          slice(1,-1)
                                          for tracked in self._track_overflow)]
        
        # === Adjust edges ===
        new_axes = []
        for axis,ngroup_i,ngroup_sign_i in zip(self._axes, ngroup, ngroup_sign):

            # Very ngroup-th edge
            new_edges = axis.edges[::ngroup_i * ngroup_sign_i][::ngroup_sign_i]

            # New axis keeping properties
            new_axes += [Axis(new_edges,
                              label = axis.label,
                              scale = axis.axis_scale)]
            
        # === Sum weights square ===
        new_sumw2 = None
        
        if self._sumw2 is not None:
            new_sumw2 = self._sumw2.rebin(ngroup * ngroup_sign)

        # === New histogram ===
        return Histogram(new_axes,
                         new_contents,
                         new_sumw2,
                         unit = self.unit,
                         track_overflow = self._track_overflow)

    def plot(self, ax = None,
             errorbars = None,
             colorbar = True,
             label_axes = True,
             **kwargs):
        """
        Quick plot of the histogram contents. 

        Under/overflow bins are not included. Only 1D and 2D histograms 
        are supported.

        Histogram with a HealpixAxis will automatically be plotted 
        as a map, passing all kwargs to mhealpy's HealpixMap.plot()

        Args:
            ax (matplotlib.axes): Axes on where to draw the histogram. A new 
                one will be created by default.
            errorbars (bool or None): Include errorbar for 1D histograms. The default is to
                plot them if sumw2 is available
            colorbar (bool): Draw colorbar in 2D plots
            label_axes (bool): Label plots axes. Histogram axes must be labeled.
            **kwargs: Passed to `matplotlib.errorbar()` (1D) or 
                `matplotlib.pcolormesh` (2D)
        """

        # Matplotlib errorbar and pcolormesh need regular array
        contents = self.contents
        if self.is_sparse:
            contents = self.contents.todense()

        if self._getitem_units:
            contents = self._strip_units(contents)

        # Handle the special case of a healpix axis
        if self.ndim == 1 and isinstance(self.axis, HealpixAxis):

            # Pad in case it is partial map
            contents = np.pad(contents,
                              (self.axis.lo_lim,
                               self.axis.npix - self.axis.hi_lim))

            m = HealpixMap(data = contents, base = self.axis)

            args = ()
            if ax is not None:
                args = (ax,)
                
            plot, ax = m.plot(*args,
                              cbar = colorbar,
                              **kwargs)

            return ax, plot            
            
        # Default errorbars
        if errorbars is None:
            if self.sumw2 is None:
                errorbars = False
            else:
                errorbars = True
                
        # Create axes if needed (with labels)
        if ax is None:
            fig,ax = plt.subplots()

        # Plot, depending on number of dimensions
        if self.ndim == 1:

            # We have two points per bin (lower edge+center), and 2 extra
            # point for under/overflow (these currently don't have errorbar,
            # they looked bad)
            if self.axis.unit is None:
                xdata = np.empty(2*self.nbins + 2)
            else:
                xdata = np.empty(2*self.nbins + 2)*self.axis.unit
                
            xdata[0] = self.axis.edges[0] # For underflow, first edge
            xdata[1::2] = self.axis.edges # In between edges. Last edge for overflow
            xdata[2::2] = self.axis.centers # For markers

            underflow = self[-1] if self._track_overflow[0] else 0
            overflow = self[self.nbins] if self._track_overflow[0] else 0

            if self._getitem_units:
                underflow = self._strip_units(underflow)
                overflow = self._strip_units(overflow)
            
            ydata = np.concatenate(([underflow],
                                    np.repeat(contents, 2),
                                    [overflow]))

            # Style
            drawstyle = kwargs.pop('drawstyle', 'steps-post')

            # Error bars
            yerr = None

            if errorbars:

                errors = self.bin_error.contents
                if self.is_sparse:
                    # No auto densify
                    errors = errors.todense()

                yerr = np.empty(2*self.nbins + 2)
                yerr[2::2] = errors
                yerr[0] = None # No underflow errorbar, looked bad
                yerr[1::2] = None # No overflow errorbar, looked bad
                
            # Plot
            plot = ax.errorbar(u.Quantity(xdata).value,
                               ydata,
                               yerr = yerr,
                               drawstyle = drawstyle,
                               **kwargs)

            # Label axes
            if label_axes:
                ax.set_xlabel(self.axis.label_with_unit)                

                if self.unit not in [None, u.dimensionless_unscaled]:
                    ax.set_ylabel(f"[{self.unit}]")
                
        elif self.ndim == 2:

            # No under/overflow
            plot = ax.pcolormesh(u.Quantity(self.axes[0].edges).value,
                                 u.Quantity(self.axes[1].edges).value,
                                 np.transpose(contents),
                                 **kwargs)

            if label_axes:
                ax.set_xlabel(self.axes[0].label_with_unit)
                ax.set_ylabel(self.axes[1].label_with_unit)

            if colorbar:

                cax = ax.get_figure().colorbar(plot, ax = ax)

                if self.unit not in [None, u.dimensionless_unscaled]:
                    cax.set_label(f"[{self.unit}]")
                    
        else:

            raise ValueError("Plotting only available for 1D and 2D histograms")
            
        if self.axes[0].axis_scale == 'log':
                ax.set_xscale('log')

        if self.ndim > 1:
            if self.axes[1].axis_scale == 'log':
                ax.set_yscale('log')
                
        return ax,plot

    draw = plot
    
    def fit(self, f, lo_lim = None, hi_lim = None, **kwargs):
        """
        Fit histogram data using least squares.

        This is a convenient call to scipy.optimize.curve_fit. Sigma corresponds
        to the output of `h.bin_error`. Empty bins (e.g. error equals 0) are 
        ignored

        Args:
            f (callable): Function f(x),... that takes the independent variable 
                x as first argument, and followed by the parameters to be fitted.
                For a k-dimensional histogram is should handle arrays of shape 
                (k,) or (k,N). The inputs and outputs must be unitless.
            lo_lim (float or array): Low axis limit to fit. One value per axis.
            lo_lim (float or array): High axis limit to fit. One value per axis.
            **kwargs: Passed to scipy.optimize.curve_fit
        """
        
        # Sanity checks
        for axis,lo,hi in  zip(self.axes,
                          np.broadcast_to(lo_lim, self.ndim, subok = True),
                          np.broadcast_to(hi_lim, self.ndim, subok = True)):

            if ((lo is not None and lo < axis.lo_lim) or
                (hi is not None and hi >= axis.hi_lim)):
                raise ValueError("Fit limits out of bounds")

        # Get bins that correspond to the fit limits
        lim_bins = tuple([slice(None if lo is None else axis.find_bin(lo),
                                None if hi is None else axis.find_bin(hi))
                          for axis,lo,hi
                          in zip(self.axes,
                                 np.broadcast_to(lo_lim, self.ndim, subok = True),
                                 np.broadcast_to(hi_lim, self.ndim, subok = True))])

        # Get data to fit
        x = [axis.centers[bins].value
             if axis.unit is not None
             else axis.centers[bins]
             for axis,bins in zip(self.axes,lim_bins)]
        x = np.meshgrid(*x, indexing='ij') # For multi-dimensional histograms
        y = self[lim_bins]
        sigma = self.bin_error[lim_bins]

        # Units
        if self._getitem_units:
            y = y.value

        # Sparse
        if self.is_sparse:
            y = y.todense()
            sigma = sigma.todense()
        
        # Ignore empty bins
        non_empty = sigma != 0 
        x = [centers[non_empty] for centers in x]
        y = y[non_empty]
        sigma = sigma[non_empty]

        # Flat matrices
        if self.ndim > 1:
            x = [centers.flatten() for centers in x]
            y = y.flatten()
            sigma = sigma.flatten()
        else:
            x = x[0]
            
        # Sanity checks
        if len(x) < len(signature(f).parameters)-1:
            raise RuntimeError("Less bins within limits than parameters to fit.")

        # Actual fit with scipy
        return curve_fit(f, x, y, sigma = sigma, **kwargs)
    
    def write(self, filename, name = "hist", overwrite = False):
        """
        Write histogram to disk.

        It will be save as a group in a HDF5 file. Appended if the file already 
        exists.

        Args:
            filename (str): Path to file
            name (str): Name of group to save histogram (can be any HDF5 path)
            overwrite (str): Delete and overwrite group if already exists.
        """

        with h5.File(filename, 'a') as f:

            # Will fail on existing group by default
            if name in f:
                if overwrite:
                    del f[name]
                else:
                    raise ValueError("Unable to write histogram. Another group "
                                     "with the same name already exists. Choose "
                                     "a different name or use overwrite")

            # Contents
            hist_group = f.create_group(name)

            if self.unit is not None:
                hist_group.attrs['unit'] = str(self.unit)
                
            if self.is_sparse:

                hist_group.attrs['format'] = 'coo'

                contents_group = hist_group.create_group('contents')

                contents = self._contents.asformat('coo')
                
                contents_group.create_dataset('coords',
                                              data = contents.coords,
                                              compression = "gzip")
                contents_group.create_dataset('data',
                                              data = contents.data,
                                              compression = "gzip")
                contents_group.create_dataset('shape', data = contents.shape)
                contents_group.create_dataset('fill_value', data = contents.fill_value)

                if self._sumw2 is not None:

                    sumw2_group = hist_group.create_group('sumw2')

                    sumw2_contents = self._sumw2._contents.asformat('coo')
                    
                    sumw2_group.create_dataset('coords',
                                               data = sumw2_contents.coords,
                                               compression = "gzip")
                    sumw2_group.create_dataset('data',
                                               data = sumw2_contents.data,
                                               compression ="gzip")
                    sumw2_group.create_dataset('shape',
                                              data = sumw2_contents.shape)
                    sumw2_group.create_dataset('fill_value',
                                              data = sumw2_contents.fill_value)

            else:
                    
                hist_group.attrs['format'] = 'dense'

                hist_group.create_dataset('contents', data = self._contents)

                if self._sumw2 is not None:
                    hist_group.create_dataset('sumw2', data = self._sumw2._contents)

            # Axes. Each one is a data set with attributes
            axes_group = hist_group.create_group('axes', track_order = True)

            for i,axis in enumerate(self.axes):

                axis._write(axes_group, str(i))
                
    @classmethod
    def open(cls, filename, name = 'hist'):
        """
        Read histogram from disk.

        Args:
            filename (str): Path to file
            name (str): Name of group where the histogram was saved.
        """

        with h5.File(filename, 'r') as f:

            hist_group = f[name]

            unit = None
            if 'unit' in hist_group.attrs:
                unit = u.Unit(hist_group.attrs['unit'])
                
            # Contents
            # Backwards compatible before sparse was supported
            if ('format' not in hist_group.attrs or
                hist_group.attrs['format'] == 'dense'):
            
                contents = np.array(hist_group['contents'])

                sumw2 = None
                if 'sumw2' in hist_group:
                    sumw2 = np.array(hist_group['sumw2'])

            elif hist_group.attrs['format'] == 'gcxs':

                contents_group = hist_group['contents']

                compressed_axes = None
                if 'compressed_axes' in contents_group:
                    compressed_axes = np.array(contents_group['compressed_axes'])
                
                contents = GCXS((np.array(contents_group['data']),
                                 np.array(contents_group['indices']),
                                 np.array(contents_group['indptr'])),
                                compressed_axes = compressed_axes,
                                shape = tuple(contents_group['shape']),
                                fill_value = np.array(contents_group['fill_value']).item())

                sumw2 = None
                if 'sumw2' in hist_group:
                    sumw2_group = hist_group['sumw2']
                
                    compressed_axes = None
                    if 'compressed_axes' in sumw2_group:
                        compressed_axes = np.array(sumw2_group['compressed_axes'])
                        
                    sumw2 = GCXS((np.array(sumw2_group['data']),
                                  np.array(sumw2_group['indices']),
                                  np.array(sumw2_group['indptr'])),
                                 compressed_axes = compressed_axes,
                                 shape = tuple(sumw2_group['shape']),
                                 fill_value = np.array(sumw2_group['fill_value']).item())
                    
            elif hist_group.attrs['format'] == 'coo':

                contents_group = hist_group['contents']
                
                contents = COO(coords = np.array(contents_group['coords']),
                               data = np.array(contents_group['data']),
                               shape = tuple(contents_group['shape']),
                               fill_value = np.array(contents_group['fill_value']).item())

                sumw2 = None
                if 'sumw2' in hist_group:
                    sumw2_group = hist_group['sumw2']
                
                    sumw2 = COO(coords = np.array(sumw2_group['coords']),
                                data = np.array(sumw2_group['data']),
                                shape = tuple(sumw2_group['shape']),
                                fill_value = np.array(sumw2_group['fill_value']).item())

            else:
                raise IOError(f"Format {hist_group.attrs['format']} unknown.")
                    
            # Axes
            axes_group = hist_group['axes']

            axes = []
            for axis in axes_group.values():

                # Get class. Backwards compatible with version
                # with only Axis
                axis_cls = Axis

                if '__class__' in axis.attrs:
                    class_module, class_name = axis.attrs['__class__']
                    axis_cls = getattr(sys.modules[class_module], class_name)

                axes += [axis_cls._open(axis)]

            axes = Axes(axes)

        # Deduce track_overflow based on contents shape
        track_overflow = [size == nbins + 2
                          for size,nbins in zip(contents.shape, axes.nbins)]
                
        return Histogram(axes, contents = contents,
                         sumw2 = sumw2,
                         unit = unit,
                         track_overflow = track_overflow)
        
