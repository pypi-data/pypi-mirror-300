from histpy import *

import numpy as np
from numpy import array_equal as arr_eq
from numpy import random

import pytest
from pytest import approx

from copy import deepcopy

from sparse import DOK, SparseArray
import sparse

nbinsx = 5
nbinsy = 4
nbinsz = 3

x = range(0,nbinsx+1)
y = list(np.linspace(10,20,nbinsy+1))
z = np.linspace(20,30,nbinsz+1)

def test_histogram_init():
    '''
    Check the various ways a histogram can be initialized
    '''
    
    # 1D from range
    h = Histogram(x)
    assert h.ndim == 1
    assert arr_eq(h.axis.edges, np.array(x))
    assert arr_eq(h.axis.widths, np.ones(nbinsx))
    assert arr_eq(h.axis.centers, np.arange(0,nbinsx)+.5)
    assert arr_eq(h[...], np.zeros(nbinsx+2))
    assert arr_eq(h[:], np.zeros(nbinsx))
    assert h.axis.nbins == nbinsx
    assert h.find_bin(0) == 0
    assert h.find_bin(.5) == 0
    assert arr_eq(h.find_bin([0,1]), [0,1])
    
    # 1D from list
    h = Histogram(y)
    assert h.ndim == 1
    assert arr_eq(h.axis.edges, np.array(y))

    # 1D from array
    h = Histogram(z)
    assert h.ndim == 1
    assert arr_eq(h.axis.edges, np.array(z))

    # 1D from list of list
    h = Histogram([y])
    assert h.ndim == 1
    assert arr_eq(h.axis.edges, np.array(y))

    # 1D from sparse array
    h = Histogram(x, sparse = True)
    assert isinstance(h.full_contents, SparseArray)

    h = Histogram(x, contents = DOK(len(x)-1))
    assert h.is_sparse
    
    # Multi-D from list of lists
    h = Histogram([y,y,y])
    assert h.ndim == 3
    assert all(arr_eq(axis1,axis2) for axis1,axis2 in zip(h.axes,[np.array(y),np.array(y),np.array(y)]))

    # Multi-D from list of arrays
    h = Histogram([z,z,z])
    assert h.ndim == 3
    assert all(arr_eq(axis1,axis2) for axis1,axis2 in zip(h.axes,[np.array(z),np.array(z),np.array(z)]))

    # Multi-D from list of arrays and lists
    h = Histogram(Axes([x,y,z], labels=['x','y','z']))
    assert h.ndim == 3
    assert all(arr_eq(axis1,axis2) for axis1,axis2 in zip(h.axes,[np.array(x),np.array(y),np.array(z)]))
    assert all(arr_eq(a.centers,axis2) for a,axis2 in zip(h.axes,[x[:-1]+np.diff(x)/2,y[:-1]+np.diff(y)/2,z[:-1]+np.diff(z)/2])) 
    assert all(arr_eq(a.widths,axis2) for a,axis2 in zip(h.axes,[np.diff(x),np.diff(y),np.diff(z)])) 
    assert arr_eq(h[:], np.zeros([nbinsx, nbinsy, nbinsz]))
    assert arr_eq(h[...], np.zeros([nbinsx+2, nbinsy+2, nbinsz+2]))
    assert arr_eq(h.nbins, [nbinsx, nbinsy, nbinsz])

    assert arr_eq(h.find_bin(0.5, 13, 27), [0,1,2])
    
    # Multi-D from array
    h = Histogram(np.reshape(np.linspace(0,100,30),[3,10]))
    assert h.ndim == 3
    assert all(arr_eq(axis1,axis2) for axis1,axis2 in zip(h.axes,list(np.reshape(np.linspace(0,100,30),[3,10]))))

    # 1D from sparse array
    h = Histogram((x,y,z), sparse = True)
    assert isinstance(h.full_contents, SparseArray)

    h = Histogram((x,y,z), contents = DOK((len(x)-1, len(y)-1, len(z)-1)))
    assert h.is_sparse

    
def test_histogram_fill_and_index():
    """
    Check the fill() method

    Also check slicing by the [] operator. Not that this is different than
    the slice() method, which returns a histogram rather than just the contents.
    """
    
    # Check 1D filling and indexing
    h = Histogram(x)

    for i in range(-1,nbinsx+1):
        h.fill(i+0.5, weight = i)

    assert arr_eq(h[-1:h.end+1], h[-1:nbinsx+1])
    assert arr_eq(h[-1:nbinsx+1], range(-1,nbinsx+1))
    assert arr_eq(h[-1:h.end], h[-1:nbinsx])
    assert arr_eq(h[-1:h.end-1], h[-1:nbinsx-1])
    assert h[h.end] == nbinsx
    
    assert arr_eq(h[:], range(0,nbinsx))
    assert arr_eq(h[-1:5], range(-1,5))
    assert arr_eq(h[:5], range(0,5))
    assert arr_eq(h[[0,2,3]], [0,2,3])

    # Chek 3D filling and indexing
    h = Histogram(Axes([x,y,z], labels = ['x','y','z']), sumw2 = True)

    for ix,vx in enumerate(x[:-1]):
        for iy,vy in enumerate(y[:-1]):
            for iz,vz in enumerate(z[:-1]):

                h.fill(vx,vy,vz, weight = (ix*nbinsy + iy)*nbinsz + iz)

    assert arr_eq(h[:], np.reshape(range(0, nbinsx*nbinsy*nbinsz), (nbinsx,nbinsy,nbinsz)))
    first_xbin = np.zeros((nbinsy+2,nbinsz+2))
    first_xbin[1:-1,1:-1] = np.reshape(range(0, nbinsy*nbinsz), (nbinsy,nbinsz))
    assert arr_eq(h[0,...], first_xbin)
    assert arr_eq(h.sumw2[:], np.reshape(range(0, nbinsx*nbinsy*nbinsz), (nbinsx,nbinsy,nbinsz))**2)
    assert arr_eq(h[0,0,-1:h.end+1], [0] + list(range(0,nbinsz)) + [0])
    h.fill(x[0],y[0],z[nbinsz], weight = 10)
    assert arr_eq(h[0,0,-1:h.end+1], [0] + list(range(0,nbinsz)) + [10])

    assert np.sum(h[:]) == np.sum(range(0,nbinsx*nbinsy*nbinsz))
    assert np.sum(h[...]) == np.sum(h[:]) + 10
    
    h2 = Histogram(h.axes, h[...], h.sumw2[...])
    assert h == h2

    # Clear
    h.clear()
    assert h == Histogram(Axes([x,y,z], labels = ['x','y','z']), sumw2 = True)

    # Sparse
    # Note: arr_eq only works with dense
    h = Histogram(x, sparse = True)

    for i in range(-1,nbinsx+1):
        h.fill(i+0.5, weight = i)

    assert arr_eq(h[-1:h.end+1].todense(), h[-1:nbinsx+1].todense())
    assert arr_eq(h[-1:nbinsx+1].todense(), range(-1,nbinsx+1))
    assert arr_eq(h[-1:h.end].todense(), h[-1:nbinsx].todense())
    assert arr_eq(h[-1:h.end-1].todense(), h[-1:nbinsx-1].todense())
    assert h[h.end] == nbinsx
    
    assert arr_eq(h[:].todense(), range(0,nbinsx))
    assert arr_eq(h[-1:5].todense(), range(-1,5))
    assert arr_eq(h[:5].todense(), range(0,5))
    assert arr_eq(h[[0,2,3]].todense(), [0,2,3])
    
def test_concatenate():

    h1 = Histogram([x,y], labels=['x','y'],
                   contents = random.rand(nbinsx, nbinsy))
    h2 = Histogram([x,y], labels=['x','y'],
                   contents = random.rand(nbinsx+2, nbinsy+2),
                   sumw2 = random.rand(nbinsx+2, nbinsy+2))


    # Without under/overflow
    hc = Histogram.concatenate(z, [h2,h2,h1], label = 'z')

    hc_contents = np.zeros([nbinsz+2, nbinsx+2, nbinsy+2])
    hc_contents[1] = h2[...]
    hc_contents[2] = h2[...]
    hc_contents[3] = h1[...]

    hc_check = Histogram([z,x,y], labels=['z','x','y'],
                         contents = hc_contents)

    assert hc == hc_check

    # With under/overflow
    hc = Histogram.concatenate(z, [h1,h2,h2,h1,h2], label = 'z')

    hc_contents = np.zeros([nbinsz+2, nbinsx+2, nbinsy+2])
    hc_contents[0] = h1[...]
    hc_contents[1] = h2[...]
    hc_contents[2] = h2[...]
    hc_contents[3] = h1[...]
    hc_contents[4] = h2[...]

    hc_check = Histogram([z,x,y], labels=['z','x','y'],
                         contents = hc_contents)

    assert hc == hc_check

    # With sumw2
    hc = Histogram.concatenate(z, [h2,h2,h2], label = 'z')

    hc_contents = np.zeros([nbinsz+2, nbinsx+2, nbinsy+2])
    hc_contents[1] = h2[...]
    hc_contents[2] = h2[...]
    hc_contents[3] = h2[...]

    hc_sumw2 = np.zeros([nbinsz+2, nbinsx+2, nbinsy+2])
    hc_sumw2[1] = h2.sumw2[...]
    hc_sumw2[2] = h2.sumw2[...]
    hc_sumw2[3] = h2.sumw2[...]

    hc_check = Histogram([z,x,y], labels=['z','x','y'],
                         contents = hc_contents,
                         sumw2 = hc_sumw2)
    
    assert hc == hc_check

    # Axes mismatch
    h3 = Histogram([y,x], labels=['y','x'],
                   contents = random.rand(nbinsy, nbinsx))

    with pytest.raises(ValueError):
        Histogram.concatenate(z, [h3,h3,h1], label = 'z')

    # Size mismatch
    with pytest.raises(ValueError):
        Histogram.concatenate(z, [h2,h1], label = 'z')

    # Sparse
    h2 = h2.to_sparse()
    
    hc = Histogram.concatenate(z, [h2,h2,h2], label = 'z')

    hc_contents = np.zeros([nbinsz+2, nbinsx+2, nbinsy+2])
    hc_contents[1] = h2[...].todense()
    hc_contents[2] = h2[...].todense()
    hc_contents[3] = h2[...].todense()

    hc_sumw2 = np.zeros([nbinsz+2, nbinsx+2, nbinsy+2])
    hc_sumw2[1] = h2.sumw2[...].todense()
    hc_sumw2[2] = h2.sumw2[...].todense()
    hc_sumw2[3] = h2.sumw2[...].todense()

    hc_check = Histogram([z,x,y], labels=['z','x','y'],
                         contents = hc_contents,
                         sumw2 = hc_sumw2)
    
    assert hc == hc_check

        
def test_histogram_project_slice():
    """
    Check the project and slice methods
    """
    
    # Project
    h = Histogram([x,y,z],
                  np.ones([nbinsx,nbinsy,nbinsz]), np.ones([nbinsx,nbinsy,nbinsz]),
                  labels=['x','y','z'])

    xproj = h.project('x')

    assert arr_eq(xproj[:], nbinsy*nbinsz*np.ones(nbinsx))
    assert arr_eq(h.axes['x'].edges, xproj.axis.edges)
    assert xproj != h
    
    xzproj = h.project('x','z')
    assert arr_eq(xzproj[:], nbinsy*np.ones([nbinsx,nbinsz]))
    assert arr_eq(xzproj.sumw2[:], nbinsy*np.ones([nbinsx,nbinsz]))
    assert all(arr_eq(axis1,axis2) for axis1,axis2 in zip(h.axes[['x','z']], xzproj.axes))

    #Project can be use to transpose
    yzx_transpose = h.project('y','z','x')
    assert arr_eq(yzx_transpose[:], np.ones([nbinsy, nbinsz, nbinsx]))
    assert all(arr_eq(axis1,axis2) for axis1,axis2 in
               zip(yzx_transpose.axes, [y,z,x]))

    
    #Slice
    hslice = h.slice[...]
    assert h == hslice

    hslice = h.slice[h.all, h.all, ...]
    assert h == hslice

    hslice = h.slice[h.all,h.all,1:2].slice[h.all, 0:1, ...].slice[3:4, ...]
    goodslice = np.pad([[[1]]], 1)
    assert arr_eq(hslice[...], goodslice)
    assert arr_eq(hslice.sumw2[...], goodslice)

    h = Histogram([x,y],
                  np.ones([nbinsx+2,nbinsy+2]), np.ones([nbinsx+2,nbinsy+2]),
                  labels=['x','y'])

    # Sparse project
    h = Histogram([x,y,z],
                  labels=['x','y','z'],
                  sparse = True,
                  sumw2 = True)

    h[:,0,:] = 1
    h.sumw2[:,0,:] = 1
    
    xproj = h.project('x')

    assert arr_eq(xproj[:].todense(), nbinsz*np.ones(nbinsx))
    
    xzproj = h.project('x','z')
    assert arr_eq(xzproj[:].todense(), np.ones([nbinsx,nbinsz]))
    assert arr_eq(xzproj.sumw2[:].todense(), np.ones([nbinsx,nbinsz]))

    # Sparse slice
    hslice = h.slice[...]
    assert h == hslice

    hslice = h.slice[h.all, h.all, ...]
    assert h == hslice

    hslice = h.slice[h.all,h.all,1:2].slice[h.all, 0:1, ...].slice[3:4, ...]
    goodslice = np.pad([[[1]]], 1)
    assert arr_eq(hslice[...].todense(), goodslice)
    assert arr_eq(hslice.sumw2[...].todense(), goodslice)
    
def test_histogram_operator():

    ones = np.ones([nbinsx+2, nbinsy+2])
    h0 = Histogram([x,y], ones, ones, labels = ['x','y'])

    h = deepcopy(h0)
    h *= 2

    assert h == Histogram([x,y], 2*ones, 4*ones, labels = ['x','y'])

    h = deepcopy(h0)
    h = h * 2

    assert h == Histogram([x,y], 2*ones, 4*ones, labels = ['x','y'])

    h = deepcopy(h0)
    h += h0

    assert h == Histogram([x,y], 2*ones, 2*ones, labels = ['x','y'])

    h -= h0

    # Errors grow since histograms are assumed independent
    assert h == Histogram([x,y], ones, 3*ones, labels = ['x','y'])
    
    h = h + h0
    assert h == Histogram([x,y], 2*ones, 4*ones, labels = ['x','y'])

    h = h - h0
    assert h == Histogram([x,y], ones, 5*ones, labels = ['x','y'])

    # Sparse
    h0 = Histogram(np.linspace(0,10,30), sparse = True)
    h1 = Histogram(np.linspace(0,10,30), sparse = True)

    h0.fill(np.random.uniform(0,10,1000))
    h1.fill(np.random.normal(5,1,1000))

    h = h0*h1

    assert Histogram(np.linspace(0,10,30),
                     h0.full_contents*h1.full_contents) == h
    
def test_histogram_interpolation():

    h = Histogram([np.linspace(-0.5,5.5,7),
                   np.linspace(-0.5,3.5,5)],
                  np.repeat([range(0,4)],6, axis=0))

    assert h.interp(5,2.6) == 2.6

    h = Histogram([np.linspace(-0.5,3.5,5),
                   np.linspace(-0.5,5.5,7)],
                  np.repeat(np.transpose([range(0,4)]), 6, axis=1))

    assert h.interp(2.6, 5) == 2.6

    h = Histogram([np.linspace(-0.5,3.5,5),
                   np.linspace(-0.5,5.5,7)],
                  (np.repeat(np.transpose([range(0,4)]), 6, axis=1)
                   * np.repeat([range(0,6)],4, axis=0)))

    assert h.interp(2,3) == 6
    assert h.interp(2,2.5) == 5
    assert h.interp(1.5,2.5) == 3.75

    h = Histogram([10**np.linspace(-0.5,3.5,5),
                   10**np.linspace(-0.5,5.5,7)],
                  (np.repeat(np.transpose([range(0,4)]), 6, axis=1)
                   * np.repeat([range(0,6)],4, axis=0)),
                  axis_scale = 'log')

    assert h.interp(10**2, 10**3) == approx(6)
    assert h.interp(10**2, 10**2.5) == approx(5)
    assert h.interp(10**1.5, 10**2.5) == approx(3.75)

    c = np.linspace(.5,9.5,10)
    c[0] = 0
    h = Histogram(np.linspace(0,10,11), c)
    h.axes[0].axis_scale = 'symmetric'
    
    assert h.interp(.5) == 0.5
    
def test_histogram_sanity_checks():
    """
    Check expected exceptions
    """
    
    # Bad axes shape
    with pytest.raises(Exception):
        Histogram(edges = np.array([[[1,2,3,4],[1,2,3,4]]]))

    with pytest.raises(Exception):
        Histogram(edges = 5)

    with pytest.raises(Exception):
        Histogram(edges = [])

    with pytest.raises(Exception):
        Histogram(edges = [5])

    with pytest.raises(Exception):
        Histogram(edges = [[5,6],[5]])

    # Bad labels
    with pytest.raises(Exception):
        Axes([1,2,3,4], labels=['x','y'])
        
    with pytest.raises(Exception):
        Axes([range(10), range(20)], labels=['x','x'])

    # Axes - contents size mistmatch
    with pytest.raises(Exception):
        Histogram(edges = [0,1,2,3], contents = [0,0])

    # Not strictly monotically increasing axes
    with pytest.raises(Exception):
        Histogram(edges = [0,1,2,3,3,4,5])
        
    with pytest.raises(Exception):
        Histogram(edges = [0,1,2,3,4,3,5])
        
    # Out of bounds
    h = Histogram(edges = [0,1,2,3], labels=['x'])
    with pytest.raises(Exception):
        h[-2]

    with pytest.raises(Exception):
        h[h]

    with pytest.raises(Exception):
        h[h.end+2]

    with pytest.raises(Exception):
        h[-2:h.end+2]

    with pytest.raises(Exception):
        h[:h.end+2]

    with pytest.raises(Exception):
        h[[-2,-1,1]]

    with pytest.raises(Exception):
        h[[-1,1,6]]

    with pytest.raises(Exception):
        h.axes[1]

    with pytest.raises(Exception):
        h.axes['y']

    # Filling and find bin dimensions
    h = Histogram(edges = [0,1,2,3])
    with pytest.raises(Exception):
        h.find_bin(1,2) # 2 inputs, 1 dim

    h.fill(1, weight = 2) # Correst, weight by key
    with pytest.raises(Exception):
        h.fill(1,2) # 2 inputs, 1 dim.

    # Project
    h = Histogram(edges = [0,1,2,3])
    with pytest.raises(Exception):
        h.project(0) #Can't project 1D histogram 

    h = Histogram(edges = [range(0,10), range(0,20)])
    with pytest.raises(Exception):
        h.project([0,0]) #Axes repeat

    h = Histogram(edges = [range(0,10), range(0,20)])
    with pytest.raises(Exception):
        h.project(2) # Axis out of bounds

    # Slicing
    h = Histogram(edges = [range(0,10+1), range(0,20+1)])
    
    h.slice[0, 0] # Slices can't be just the underflow
    with pytest.raises(Exception):
        h.slice[-1] # Out of bounds

    h.slice[9] # Slices cant's be just the overflow
    with pytest.raises(Exception):
        h.slice[10] # Out of bounds

    with pytest.raises(Exception):
        h.slice[6:3] # Backward slice not supported

    # Operators
    h = Histogram(edges = [range(0,10+1), range(0,20+1)])
    h2 = Histogram(edges = [range(0,10), range(0,20)])

    with pytest.raises(Exception):
        h *= [1,2]

    with pytest.raises(Exception):
        h += h2

    with pytest.raises(Exception):
        h -= h2
