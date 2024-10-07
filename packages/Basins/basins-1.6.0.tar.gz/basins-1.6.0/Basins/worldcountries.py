#!/usr/bin/env python

# Edited by amiro and eterzic 25.01.2021

from __future__ import print_function, division

import os, numpy as np

from .entities import Basin, ComposedBasin

# Path to the shapes directory
SHAPESPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'shapes')

# World Countries shapefile
mne = Basin.from_npy('mne', 'Montenegro', os.path.join(SHAPESPATH,'Montenegro_WorldCountries.npy'),downsample=1)
spa = Basin.from_npy('spa', 'Spain'     , os.path.join(SHAPESPATH,'Spain_WorldCountries.npy'),downsample=4)

del print_function, division, os, np, Basin, ComposedBasin