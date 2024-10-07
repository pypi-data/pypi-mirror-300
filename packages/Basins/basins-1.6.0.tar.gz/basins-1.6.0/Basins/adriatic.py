#!/usr/bin/env python

# Edited by amiro and eterzic 13.01.2022

from __future__ import print_function, division

import os, numpy as np

from .entities import Basin, ComposedBasin

# Path to the shapes directory
SHAPESPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'shapes')

north = Basin.from_npy('nadr', 'North Adriatic', os.path.join(SHAPESPATH,'North_Adriatic.npy'),downsample=4)
mid   = Basin.from_npy('madr', 'Mid Adriatic',   os.path.join(SHAPESPATH,'Mid_Adriatic.npy'),  downsample=4)
south = Basin.from_npy('sadr', 'South Adriatic', os.path.join(SHAPESPATH,'South_Adriatic.npy'),downsample=4)

# Composed basins
all   = ComposedBasin('adr', 'Adriatic', [north,mid,south])

del print_function, division, os, np, Basin, ComposedBasin