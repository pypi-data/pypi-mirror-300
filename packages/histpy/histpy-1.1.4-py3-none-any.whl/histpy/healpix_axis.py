from .axis import Axis

from mhealpy import HealpixBase

import numpy as np

from astropy.coordinates import SkyCoord, BaseRepresentation, SphericalRepresentation
import astropy.units as u

class HealpixAxis(Axis, HealpixBase):
    """
    2D spherical axis using a HEALPix grid

    Args:
        nside (int): Alternatively, you can specify the edges for all pixels.
        scheme (str): Healpix scheme. Either 'RING', 'NESTED'.
        edges (array): List of bin edges in terms of HEALPix pixels. Must be integers. Default:
            all pixels, one pixel per bin.
        coordsys (BaseFrameRepresentation or str): Instrinsic coordinates of the map.
            Either ‘G’ (Galactic), ‘E’ (Ecliptic) , ‘C’ (Celestial = Equatorial) or any other 
            coordinate frame recognized by astropy.
    """
    
    def __init__(self,
                 nside = None,
                 scheme = 'ring',
                 edges = None,
                 coordsys = None,
                 label = None,
                 *args, **kwargs):

        if nside is None and edges is not None:

            npix = len(edges)-1

            if not np.array_equal(edges, np.arange(npix + 1)):
                raise ValueError("If you don't specify nside, edges must include all pixels. Use integers.")

            HealpixBase.__init__(self,
                                 npix = npix,
                                 scheme = scheme,
                                 coordsys = coordsys)

        else:

            if nside is None:
                raise ValueError("Specify either nside or edges")
            
            HealpixBase.__init__(self,
                                 nside = nside,
                                 scheme = scheme,
                                 coordsys = coordsys)

            if edges is None:
                # Default to full map
                edges = np.arange(self.npix + 1)
                
        super().__init__(edges,
                         label = label)
        
    def _sanitize_edges(self, edges):

        edges = super()._sanitize_edges(edges)

        # Check it corresponds to pixels
        if edges.dtype.kind not in 'ui':
            raise ValueError("HeapixAxis needs integer edges")

        if edges[0] < 0 or edges[-1] > self.npix+1:
            raise ValueError("Edges must be within 0 and the total number of pixels")

        return edges
        
    def __eq__(self, other):
        return self.conformable(other) and super().__eq__(other)

    def __getitem__(self, key):

        base_axis = super().__getitem__(key)

        return HealpixAxis(edges = base_axis,
                           nside = self.nside,
                           scheme = self.scheme,
                           coordsys = coordsys)

    def find_bin(self, value):
        """
        Find the bin number that corresponds to a given pixel or coordinate.

        Args:
            value (int, SkyCoord, BaseRepresentation): Pixel or coordinate

        Returns:
            int
        """
        
        if isinstance(value, (SkyCoord, BaseRepresentation)):
            # Transform first from coordinates to pixel
            value = self.ang2pix(value)

        return super().find_bin(value)

    def interp_weights(self, value):
        """
        Return the 4 closest pixels on the two rings above and below the 
        location and corresponding weights. Weights are provided for bilinear 
        interpolation along latitude and longitude

        Args:
            value (int, SkyCoord, BaseRepresentation): Coordinate to interpolate. When
                passing an integer, the center of the corresponding pixel will be used.

        Returns:
            bins (int array): Array of bins to be interpolated
            weights (float array): Corresponding weights.
        """

        if isinstance(value, (SkyCoord, BaseRepresentation)):

            pixels, weights = self.get_interp_weights(value)

            return self.find_bin(pixels), weights
        
        else:

            # Pixel. Get the center.

            if self.coordsys is None:

                lon,lat = self.pix2ang(value, lonlat = True)

                value = SphericalRepresentation(lon = lon*u.deg,
                                                lat = lat*u.deg,
                                                lonlat = True)
                
            else:

                value = self.pix2skycoord(value)
            
            return self.interp_weights(value)
    
    def _operation(self, key):
        raise AttributeError("HealpixAxis doesn't support operations")

    def _write_attrs(self, attrs):
        """
        Save all needed information to recreate Axis into 
        a HDF5 group

        Args:
            attrs (HDF5 attribute)
        """
        
        attrs['nside'] = self.nside

        if self.label is not None:
            # HDF5 doesn't support unicode
            attrs['label'] = str(axis.label)
            
        if self.coordsys is not None:
            attrs['coordsys'] = str(self.coordsys.name)

    def _write(self, axes_group, name):
        """
        Save all needed information to recreate Axis into 
        a HDF5 group
        """
        
        axis_set = axes_group.create_dataset(name,
                                             data = self.edges)

        axis_set.attrs['__class__'] = (self.__class__.__module__,
                                       self.__class__.__name__)

        axis_set.attrs['nside'] = self.nside
        axis_set.attrs['scheme'] = self.scheme

        if self.label is not None:
            # HDF5 doesn't support unicode
            axis_set.attrs['label'] = str(self.label)
            
        if self.coordsys is not None:
            axis_set.attrs['coordsys'] = str(self.coordsys.name)

    @classmethod
    def _open(cls, dataset):
        """
        Create Axis from HDF5 dataset
        """

        edges = np.array(dataset)

        nside = dataset.attrs['nside']
        scheme = dataset.attrs['scheme']
        
        label = None
        if 'label' in dataset.attrs:
            label = dataset.attrs['label']

        coordsys = None
        if 'coordsys' in dataset.attrs:
            coordsys = dataset.attrs['coordsys']

        return cls(edges = edges,
                   nside = nside,
                   scheme = scheme,
                   label = label,
                   coordsys = coordsys)

    



