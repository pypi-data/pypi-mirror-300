import logging
logger = logging.getLogger(__name__)

import numpy as np

from copy import copy,deepcopy

from .axis import Axis

from sparse import SparseArray

import astropy.units as u

class Axes:
    """
    Holds a list of axes. 

    The operator :code:`Axes[key]` return a subset of these. Key can be either the
    index or the label. If the key is a single index, a single Axis object
    will be returned

    Args:
        edges (array or list of arrays or Axis): Definition of bin edges.
        labels (array of str): Optionally label the axes for easier indexing.
            Will override the labels of edges, if they are Axis objects
        axis_scale (str or array): Bin center mode e.g. `"linear"` or `"log"`. 
            See Axis.axis_scale. If not an array, all axes will have this mode.

    """

    def __init__(self, edges, labels=None, axis_scale = None):

        # Standarize axes as list of Axis
        if isinstance(edges, Axes):
            # From another Axes object
            
            self._axes = copy(edges._axes)

        elif isinstance(edges, Axis):

            self._axes = [edges]
            
        elif np.isscalar(edges):

            if np.isscalar(edges):
                raise TypeError("'edges' can't be a scalar")

        else:

            # Either a list with edges (1D), or a list of lists of edges (ND)
            
            if all(np.ndim(a) == 0 for a in edges):
                #1D histogram
                self._axes = [Axis(edges)]
            else:
                #Multi-dimensional histogram.
                self._axes = [axis if isinstance(axis, Axis)
                              else Axis(axis)
                              for axis in edges]

        #Override labels if nedeed
        if labels is not None:
            
            if np.isscalar(labels):
                labels = [labels]

            if len(labels) != self.ndim:
                raise ValueError("Edges - labels size mismatch")

            for n,label in enumerate(labels):
                self._axes[n] = Axis(self._axes[n], label)

        self._update_labels_index()
                
        #Override scale if nedeed
        if axis_scale is not None:
            
            if np.isscalar(axis_scale):
                axis_scale = self.ndim*[axis_scale]

            if len(axis_scale) != self.ndim:
                raise ValueError("Edges - axis_scale size mismatch")

            for mode,ax in zip(axis_scale, self._axes):
                ax.axis_scale = mode

    def _update_labels_index(self):

        #Maps labels to axes indices. Only keep non-None
        labels = np.array([a.label for a in self._axes])

        non_none_labels = labels[labels != None]
        if len(np.unique(non_none_labels)) != len(non_none_labels):
                    raise ValueError("Labels can't repeat")

        self._labels = {}
        
        for n,label in enumerate(labels):
            if label is not None:
                self._labels[label] = n
        
                
    def __len__(self):
        return self.ndim

    def __iter__(self):
        return iter(self._axes)
            
    @property
    def ndim(self):
        """
        Number of axes
        """
        return len(self._axes)

    def label_to_index(self, key):
        """
        Turn a key or list of keys, either indices or labels, into indices

        Args:
            key (int or str): Index or label
        
        Return:
            int: Index
        """
        
        if isinstance(key, (int, np.integer)):
            return key
        if (isinstance(key, (np.ndarray, list, tuple, range))
            and
            not isinstance(key, str)):
            return tuple(self.label_to_index(k) for k in key)
        if isinstance(key, slice):
            return np.arange(*key.indices(self.ndim))
        else:
            #Label
            try:
                return self._labels[key]
            except KeyError:
                logger.error("Axis with label {} not found".format(key))
                raise

    def __getitem__(self, key):

        indices = self.label_to_index(key)

        if np.isscalar(indices):
            return self._axes[indices]
        else:
            return Axes([self._axes[i] for i in indices])

    def __setitem__(self, key, new):

        if not isinstance(new, Axis):
            new = Axis(new)

        key = self.label_to_index(key)

        if new.nbins != self._axes[key].nbins:
            raise ValueError("Can't assign new axis with different number of bins")

        self._axes[key] = new    
        
    def __eq__(self, other):
        return all([a1 == a2 for a1,a2 in zip(self._axes,other._axes)])

    def __array__(self):
        return np.array(self._axes)

    def find_bin(self, *values):
        """
        Return one or more indices corresponding to the bin this value or 
        set of values correspond to.

        You can pass either an array, or specified the values as different 
        arguments. i.e. :code:`h.find_bin(x,y,z)` = :code:`h.find_bin([x,y,z])`

        Multiple entries can be passed at once. e.g. 
        :code:`h.find_bin([x0, x1, x2])`, 
        :code:`h.find_bin([x0, x1],[y0, y1],[z0, z1])`,
        :code:`h.find_bin([[x0, x1],[y0, y1],[z0, z1]])`
        
        Args:
            values (float or array): Vaule or list of values. Either shape N or
               ndim x N, where N is the number of entries.

        Return:
            int or tuple: Bin index
        """
        
        # Handle 1D
        if self.ndim == 1:

            # 1D hist, any shape of values works. The output has the same shape
            
            if len(values) != 1:
                raise ValueError("Mismatch between values shape and number of axes")

            return self[0].find_bin(values[0])

        # >=2D case

        # Sanitize and standarize
        if len(values) == 1:
            # e.g. ([x,y]) or ([[x0,x1], [y0,y1]]), NOT (x,y,z), [[x0,x1], [y0,y1]]
            values = tuple(values[0])
            
        if len(values) != self.ndim:
            raise ValueError("Mismatch between values shape and number of axes")

        return tuple(axis.find_bin(val)
                     for val,axis in zip(values, self._axes))

    def interp_weights(self, *values):
        """
        Get the bins and weights to linearly interpolate between bins.
        The bin contents are assigned to the center of the bin.

        Args:
            values (float or array): Coordinates within the axes to interpolate.
        
        Returns:
            array of tuples of int, array of floats: Bins and weights to use. 
            Shaped (2^ndim, N). Bins is an array of tupples for multi-dimensional
            histograms.

        """

        # Handle 1D
        if self.ndim == 1:

            # 1D hist, any shape of values works. The output has the same shape
            
            if len(values) != 1:
                raise ValueError("Mismatch between values shape and number of axes")

            return self._axes[0].interp_weights(values[0])

        # >=2D case

        # Sanitize and standarize
        if len(values) == 1:
            # e.g. ([x,y]) or ([[x0,x1], [y0,y1]]), NOT (x,y,z), [[x0,x1], [y0,y1]]
            values = tuple(values[0])
            
        if len(values) != self.ndim:
            raise ValueError("Mismatch between values shape and number of axes")
        
        # Broadcast
        values = np.broadcast_arrays(*values, subok = True)
        values_shape = values[1].shape
        
        # Get the bin/weights for each individual axis
        dim_bins = np.empty(self.ndim, dtype = 'O')
        dim_weights = np.empty(self.ndim, dtype = 'O')
        
        for dim,value in enumerate(values):

            bins,weights = self._axes[dim].interp_weights(value)

            dim_bins[dim] = bins
            dim_weights[dim] = weights

        npoints = 2**self.ndim
        bins = np.empty(tuple([npoints]) + values_shape,
                        dtype = 'O')
        weights = np.empty(tuple([npoints]) + values_shape)

        # Combine them. e.g. for 2D this results in
        # weights = [dim_weights[0][0]*dim_weights[1][0],
        #            dim_weights[0][1]*dim_weights[1][0],
        #            dim_weights[0][0]*dim_weights[1][1],
        #            dim_weights[0][1]*dim_weights[1][1]]
        # bins = [(dim_bins[0][0], dim_bins[1][0]),
        #         (dim_bins[0][1], dim_bins[1][0]),
        #         (dim_bins[0][0], dim_bins[1][1]),
        #         (dim_bins[0][1], dim_bins[1][1])]
        # bit_masks = [0b001, 0b010, 0b100, ...]
        bit_masks = 2**np.array(range(self.ndim))
        for n in range(npoints):

            weight = 1
            bin_list = np.empty(tuple([self.ndim]) + values_shape,
                                dtype = int) 

            # Since there are two weights per axis, we use bit
            # masking to loop between them instead of recursion
            for dim,bit_mask in enumerate(bit_masks):

                index = int(bool(n & bit_mask)) # Either 0 or 1

                weight *= dim_weights[dim][index]
                bin_list[dim] = dim_bins[dim][index]

            # Rearrange as an array of tuples
            # It might seem like a simple reshape would do the job but this
            # was the only way I found to make an array of tuples, as opposed
            # to the tuples being converted onto an extra dimension
            bin_list = [z for z in zip(*[b.flatten() for b in bin_list])]
            bin_list_aux = np.empty(np.prod(values_shape, dtype = int),
                                    dtype = 'O')
            bin_list_aux[:] = bin_list
            
            if values_shape:
                bin_list_aux = np.reshape(bin_list_aux, values_shape)
                bins[n] = bin_list_aux
            else:
                bins[n] = bin_list_aux[0]

            weights[n] = weight
            
        return bins, weights
            
    def _get_axis_property(f):
        """
        Decorator to retrieve a property from all axes at once
        
        The methods need to be reclared as:
        @_get_axis_property
        def property_name(self):
            return 'property_name'
        """

        @property
        def wrapper(self):
            
            return np.array([getattr(axis, f(self)) for axis in self._axes])
            
        return wrapper

    @_get_axis_property
    def units(self):
        """
        Labels of all axes. 
        """
        return 'unit'

    @_get_axis_property
    def labels(self):
        """
        Labels of all axes. 
        """
        return 'label'

    @labels.setter
    def labels(self, new_labels):

        if len(new_labels) != self.ndim:
            raise ValueError("Number of labels do not correspond to the "
                             "number of dimensions.")

        for axis,label in zip(self,new_labels):
            axis.label = label

        self._update_labels_index()
            
    @_get_axis_property
    def lo_lims(self):
        """
        Overall lower bounds
        """
        return 'lo_lim'
        
    @_get_axis_property
    def hi_lims(self):
        """
        Overall upper bounds
        """
        return 'hi_lim'
        
    @_get_axis_property
    def nbins(self):
        """
        Number of elements along each axis.
        """
        return 'nbins'
        
    def expand_dims(self, a, axis):
        """
        Insert new axes into `a` as appropiate to allow broadcasting with
        a histogram having these axes 
        """

        # Standarize inputs
        if not isinstance(a, (np.ndarray, SparseArray)):
            a = np.array(a)

        axis = np.array(self.label_to_index(axis))

        if axis.ndim == 0:
            # Make scalars an array
            axis = axis[None]
        
        # Sanity checks
        if a.ndim != len(axis):
            raise ValueError("Number of input axes ({}) "
                             "does not match number of "
                             "dimensions ({}) of the "
                             "input array".format(len(axis),
                                                  a.ndim))

        if a.ndim > self.ndim:
            raise ValueError("Number of dimensions of the input array ({}) "
                             "cannot be greater than the "
                             "number of axes ({})".format(a.ndim, self.ndim))

        if any(axis >= self.ndim) or any(axis < 0):
            raise ValueError("One or more axes indices ({}) "
                             "out of bounds ({} axes)".format(axis, self.ndim))
        
        # Match number of axes
        orig_ndim = a.ndim
        a = a[tuple(slice(None) for _ in range(a.ndim)) + 
              tuple(None for _ in range(self.ndim - a.ndim))]

        # Reorganize axes
        a = np.moveaxis(a, np.arange(orig_ndim), axis)
        
        return a

    def broadcast(self, a, axis):
        """
        Expand the dimensions and broadcast an array for a given set of axes 
        such that it has the same dimensions as the histogram.

        Args:
            a (array): Array to broadcast
            axis (int or array): Histogram axes correspond to the array axes.
        """

        # Add singleton dims
        a = self.expand_dims(a, axis)

        # Account for under/overflow
        new_shape = self.nbins
        
        for i,(a_nbins,h_nbins) in enumerate(zip(a.shape, new_shape)):

            if a_nbins == h_nbins+2:
                new_shape[i] += 2

        output = np.broadcast_to(a, tuple(new_shape)) 

        if isinstance(a, u.Quantity):
            output = output*a.unit
        
        return output
    
    def expand_dict(self, axis_value, default = None):
        """
        Convert pairs of axis:value to a list of length `ndim`.

        Args:
            axis_value (dict): Dictionary with axis-value pairs (can be labels)
            default: Default filling value for unspecified axes

        Return:
            tuple
        """
        
        val_list = [default] * self.ndim
        
        for axis,value in axis_value.items():
        
            axis = self.label_to_index(axis)
            
            val_list[axis] = value

        return tuple(val_list)
        
