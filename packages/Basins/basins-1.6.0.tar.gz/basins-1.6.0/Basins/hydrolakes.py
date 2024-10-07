#!/usr/bin/env python

# Edited by amiro and eterzic 25.01.2021

from __future__ import print_function, division

import os, numpy as np

from .entities import Basin

# Path to the shapes directory
SHAPESPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'shapes')

# Skadar lake, shapefile from HydroLAKES
skadar_lowres  = Basin.from_npy('skadar', 'Skadar Lake', os.path.join(SHAPESPATH,'Skadar_HydroLAKES.npy'),downsample=6)
skadar_midres  = Basin.from_npy('skadar', 'Skadar Lake', os.path.join(SHAPESPATH,'Skadar_HydroLAKES.npy'),downsample=4)
skadar_highres = Basin.from_npy('skadar', 'Skadar Lake', os.path.join(SHAPESPATH,'Skadar_HydroLAKES.npy'),downsample=1)

del print_function, division, os, np, Basin