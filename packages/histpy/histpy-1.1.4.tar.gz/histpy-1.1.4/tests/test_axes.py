from histpy import *

import numpy as np
from numpy import array_equal as arr_eq
from numpy import random

import pytest
from pytest import approx

from copy import deepcopy

nbinsx = 5
nbinsy = 4
nbinsz = 3

x = range(0,nbinsx+1)
y = list(np.linspace(10,20,nbinsy+1))
z = np.linspace(20,30,nbinsz+1)

def test_axes():
    '''
    Test Axes class for lines missed by general tests
    '''

    # Label override
    assert Axes(Axes(x, labels='axis'), 'axis2') == Axes(x, labels='axis2')

    axes = Axes([x,y], labels=['x','y'])
    assert (Axes(axes, labels=['x2','y2'])
            == Axes([x,y], labels=['x2','y2']))

    assert arr_eq(axes.labels, ['x','y'])
    assert axes.ndim == 2
    assert arr_eq(axes.nbins, [nbinsx, nbinsy])
    
    #Conversion to numpy array
    assert isinstance(axes.__array__(), np.ndarray)
    assert all([arr_eq(a,b) for a,b in zip(axes.__array__(),[x,y])])
