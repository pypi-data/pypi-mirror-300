import logging
logger = logging.getLogger(__name__)

import numpy as np
from numpy import log2

import operator

from copy import copy,deepcopy

import astropy.units as u

class Axis:
    """
    Bin edges. Optionally labeled

    You can select specific edges using the slice operator (:code:`[]`).
    The result is also another Axis object. 

    Args:
        edges (array-like): Bin edges. Can be a Quantity array, if you need units
        label (str): Label for axis. If edges is an Axis object, this will 
            override its label
        scale (str): Bin center mode e.g. `"linear"` or `"log"`. 
            See `axis_scale` property. If edges is an Axis 
            object, this will override its mode
    """

    def __init__(self, edges, label = None, scale = None):

        if isinstance(edges, Axis):
            self._edges = edges._edges

            #Override
            if label is None:
                self._label = edges._label
            else:
                self._label = label

            if scale is None:
                self._scale = edges._scale
            else:
                self._scale = scale

            self._unit = edges.unit
                
        else:

            if isinstance(edges, u.Quantity):
                self._unit = edges.unit
                edges = edges.value
            else:
                self._unit = None
            
            self._edges = self._sanitize_edges(edges)

            self._label = label

            if scale is None:
                self._scale = 'linear'
            else:
                self._scale = scale
                
    def _sanitize_edges(self, edges):

        edges = np.array(edges)

        if edges.ndim != 1:
            raise ValueError("Edges list must be a 1-dimensional array")
        
        if len(edges) < 2:
            raise ValueError("All edges need at least two edges")
    
        if any(np.diff(edges) <= 0):
            raise ValueError("All bin edges must be strictly monotonically"
                             " increasing")

        return edges

    @property
    def unit(self):
        """
        Return the astropy units of the axis. Or ``None`` is units where not declare. 
        """
        
        return self._unit

    def to(self, unit, equivalencies=[]):

        # Compute factor
        unit = u.Unit(unit)
        
        if self.unit is None:
            
            if unit is None or unit == u.dimensionless_unscaled:
                factor = 1
            else:
                TypeError("Axis without units")

        else:
            
            factor = self.unit.to(unit, equivalencies = equivalencies)

        # Make changes
        self._unit = unit
        self._edges *= factor
        
    @property
    def axis_scale(self):
        """
        Control what is considered the center of the bin. This affects
        `centers()` and interpolations.

        Modes:
            - linear (default): The center is the midpoint between the bin edges
            - symmetric: same as linear, except for the first center, which
              will correspond to the lower edge. This is, for example, useful 
              when the histogram is filled with the absolute value of a 
              variable.
            - log: The center is the logarithmic (or geometrical) midpoint between
              the bin edges.
        """

        return self._scale

    @axis_scale.setter
    def axis_scale(self, mode):
        
        if mode not in ['linear', 'symmetric', 'log']:
            raise ValueError("Bin center mode '{}' not supported".format(mode))

        if mode == 'log' and self.lo_lim <= 0:
            raise ArithmeticError("Bin center mode 'log' can only be assigned "
                                  "to axes starting at a positive number")

        self._scale = mode

    def __array__(self):
        return np.array(self._edges)

    def __len__(self):
        return len(self._edges)

    def __eq__(self, other):

        if self.unit is None or other.unit is None:
            if self.unit != other.unit:
                return False

        return (np.all(self.edges == other.edges)
                and
                self.axis_scale == other.axis_scale
                and
                self._label == other._label)

    def __getitem__(self, key):

        if isinstance(key, int):

            if key < 0:
                key += self.nbins
            
            key = slice(key, key+1)
            
        if isinstance(key, slice):

            start,stop,stride = key.indices(self.nbins+1)

            if stride != 1:
                raise ValueError("Step must be 1 when getting an axis slice.")

            if start > stop:
                raise ValueError("Axis slices cannot reverse the bin order.")

            if stop - start < 1:
                raise ValueError("Axis slice must have a least one bin")

            key = slice(start, stop+1)

        else:
            raise TypeError("Axis slice opertor only supports integers and slices")

        if key.start < 0 or key.stop > self.nbins+1:
            raise ValueError("Axis element out of bounds")

        new_edges = self._edges[key]

        if self.unit is not None:
            new_edges = new_edges*self.unit
        
        return Axis(new_edges,
                    label = self.label,
                    scale = self.axis_scale)

    def _strip_units(self, quantity):

        if isinstance(quantity, u.Quantity):

            if quantity.unit == u.dimensionless_unscaled:
                return quantity.value
            
            if self.unit is None:
                return u.UnitConversionError("Axis without units")

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
    
    def find_bin(self, value):
        """
        Return the bin `value` corresponds to. 

        Return:
            int: Bin number. -1 for underflow, `nbins` for overflow
        """

        value = self._strip_units(value)

        return np.digitize(value, self._edges)-1
    
    def interp_weights(self, value):
        """
        Get the two closest bins to `value`, together with the weights to 
        linearly interpolate between them. The bin contents are assigned to 
        the center of the bin.

        Values beyond the center of the first/last bin will 
        result in the contents of the first/last bint, accordingly.

        Return:
            [int, int]: Bins. Shaped (2,N)
            [float, float]: Weights. Shaped (2,N)
        """

        # Find bin and standarize
        bin0 = self.find_bin(value)

        value = self._strip_units(value)

        isscalar = np.isscalar(bin0)
        if isscalar:
            bin0 = np.array([bin0])

        # Use edge bins for our of bounds values
        bin0[bin0 < 0] = 0
        bin0[bin0 == self.nbins] -= 1
                
        # Linear interpolation with two closest bins
        center0 = self._strip_units(self.centers[bin0])

        bin1 = copy(bin0)

        bin1[value > center0] += 1
        bin1[value <= center0] -= 1
        
        # Handle histogram edges, beyond center of first/last pixel
        bin1 = np.minimum(self.nbins-1, np.maximum(0, bin1))

        # Sort
        reverse_mask = bin0 > bin1

        bin0_aux = copy(bin0)
        bin0[reverse_mask] = bin1[reverse_mask]
        bin1[reverse_mask] = bin0_aux[reverse_mask]
        
        # Weights
        center0 = self._strip_units(self.centers[bin0])
        center1 = self._strip_units(self.centers[bin1])

        if self._scale == 'log':
            center0 = log2(center0)
            center1 = log2(center1)
            value = log2(value)

        norm = center1 - center0
        
        w0 = (center1 - value)
        w1 = (value - center0)

        # No interpolation at the very edge
        is_edge = bin0 == bin1
        not_edge = np.logical_not(is_edge)
        
        w0[is_edge] = .5
        w1[is_edge] = .5

        w0[not_edge] /= norm[not_edge]
        w1[not_edge] /= norm[not_edge]

        # Squeeze if needed
        if isscalar:
            return (np.array([bin0[0],bin1[0]]), np.array([w0[0],w1[0]]))
        else:
            return (np.array([bin0,bin1]), np.array([w0,w1]))

    def _with_units(self, a):
        if self.unit is None:
            return a
        else:
            return a*self.unit
        
    @property
    def lower_bounds(self):
        '''
        Lower bound of each bin
        '''

        return self._with_units(self._edges[:-1])

    @property
    def upper_bounds(self):
        '''
        Upper bound of each bin
        '''

        return self._with_units(self._edges[1:])

    @property
    def bounds(self):
        '''
        Start of [lower_bound, upper_bound] values for each bin.
        '''

        return self._with_units(np.transpose([self.lower_bounds, self.upper_bounds]))

    @property
    def lo_lim(self):
        """
        Overall lower bound
        """

        return self._with_units(self._edges[0])

    @property
    def hi_lim(self):
        """
        Overall upper bound of histogram
        """

        return self._with_units(self._edges[-1])

    @property
    def edges(self):
        """
        Edges of each bin
        """

        return self._with_units(self._edges)

    @property
    def label(self):
        """
        Axis label
        """
        return self._label

    @label.setter
    def label(self, new_label):
        self._label = new_label

    @property
    def label_with_unit(self):
        """
        Axis 'label [units]'
        """
        label = ""
        
        if self.label is not None:
            label += f"{self.label}"
            
        if self.unit not in [None, u.dimensionless_unscaled]:
            label += f" [{self.unit}]"

        return label
                
    @property
    def centers(self):
        '''
        Center of each bin.
        '''

        if self._scale == 'linear':
            centers = (self._edges[1:] + self._edges[:-1])/2
        elif self._scale == 'symmetric':
            centers = (self._edges[1:] + self._edges[:-1])/2
            centers[0] = self.lo_lim
        elif self._scale == 'log':
            log2_edges = log2(self._edges)
            centers = 2**((log2_edges[1:] + log2_edges[:-1])/2)
        else:
            raise AssertionError("This shouldn't happen, "
                                 "tell maintainers to fix it")
        
        return self._with_units(centers)
        
    @property
    def widths(self):
        '''
        Width each bin.
        '''

        return self._with_units(np.diff(self._edges))

    @property
    def nbins(self):
        """
        Number of elements along each axis. Either an int (1D histogram) or an 
        array
        """
        
        return len(self._edges)-1

    def _enforce_unitless(self, value, error_message = None):

        if isinstance(value, u.UnitBase):
            unit = value
        elif isinstance(value, u.Quantity):
            unit = value.unit
        else: 
            unit = u.dimensionless_unscaled

        if unit != u.dimensionless_unscaled:
            raise TypeError(error_message)
            
    def _ioperation(self, other, operation):

        self._enforce_unitless(other,
                               "Operations with dimensional quantities "
                               "are not allowed")
        
        other = self._strip_units(other)

        self._edges = self._sanitize_edges(operation(self._edges, other))

        return self

    def _operation(self, other, operation):

        new_axis = deepcopy(self)
        new_axis = new_axis._ioperation(other, operation)
        return new_axis
    
    def __imul__(self, other):
        return self._ioperation(other, operator.imul)
        
    def __mul__(self, other):
        return self._operation(other, operator.mul)

    def __rmul__(self, other):
        self._enforce_unitless(other,
                               "Operations with dimensional quantities "
                               "are not allowed")
        
        other = self._strip_units(other)
        
        return self*other
    
    def __itruediv__(self, other):
        return self._ioperation(other, operator.itruediv)
        
    def __truediv__(self, other):
        return self._operation(other, operator.truediv)

    # No rtruediv nor rsub. Bins must be monotonically increasing
    
    def __iadd__(self, other):
        return self._ioperation(other, operator.iadd)
        
    def __add__(self, other):
        return self._operation(other, operator.add)

    def __radd__(self, other):
        self._enforce_unitless(other,
                               "Operations with dimensional quantities "
                               "are not allowed")
        
        other = self._strip_units(other)

        return self + other
    
    def __isub__(self, other):
        return self._ioperation(other, operator.isub)
        
    def __sub__(self, other):
        return self._operation(other, operator.sub)        

    def _write(self, axes_group, name):
        """
        Save all needed information to recreate Axis into 
        a HDF5 group
        """
        
        axis_set = axes_group.create_dataset(name,
                                             data = self.edges)

        axis_set.attrs['__class__'] = (self.__class__.__module__,
                                       self.__class__.__name__)

        axis_set.attrs['scale'] = self.axis_scale

        if self.label is not None:
            # HDF5 doesn't support unicode
            axis_set.attrs['label'] = str(self.label)

        if self.unit is not None:
            axis_set.attrs['unit'] = str(self.unit)              

    @classmethod
    def _open(cls, dataset):
        """
        Create Axis from HDF5 dataset
        """

        scale = dataset.attrs['scale']

        edges = np.array(dataset)

        if 'unit' in dataset.attrs:
            edges = edges*u.Unit(dataset.attrs['unit'])

        label = None
        if 'label' in dataset.attrs:
            label = dataset.attrs['label']

        return cls(edges = edges,
                   scale = scale,
                   label = label)

