#!/usr/bin/env python

# Edited by amiro and eterzic 13.01.2022

from __future__ import print_function, division

import os, numpy as np

from .entities import Basin, ComposedBasin, SimpleRectangle

bornholm = Basin('born', 'Bornholm',       SimpleRectangle(15.0, 17.8, 54.5 ,  55.5).points)
gdansk   = Basin('gdan', 'Gdansk'  ,       SimpleRectangle(18.1,  20., 53.8 , 55.15).points)
gotland  = Basin('gotl', 'Gotland' ,       SimpleRectangle(17. ,   22, 55.15,  60.0).points)
kattegat = Basin('katt', 'Kattegat',       SimpleRectangle(10. , 12.8,   55.,  58.4).points) 
w_baltic = Basin('wbal', 'Western Baltic', SimpleRectangle(12.8,  15.,  53.7,  56.0).points)


del print_function, division, os, np, Basin, ComposedBasin, SimpleRectangle