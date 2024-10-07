#!/usr/bin/env python

# Edited by amiro and eterzic 22.12.2023

from __future__ import print_function, division

from .entities import Basin, ComposedBasin, SimpleRectangle


npolar     = Basin('npole',  'North Pole',      SimpleRectangle(-180, 180, 66.56, 90).points)   # between the North Pole and the  Arctic Cicle
ntemperate = Basin('ntemp',  'North Temperate', SimpleRectangle(-180, 180, 40, 66.56).points)   # between the Arctic Circle and 40 degrees
nsubtrop   = Basin('nstrop', 'North Subtropic', SimpleRectangle(-180, 180, 23.5, 40).points)    # between 40 degrees and the Tropic of Cancer
tropic     = Basin('trop',   'Tropic',          SimpleRectangle(-180, 180, -23.5, 23.5).points) # between the Tropic of Cancer and the Tropic of Capricorn
ssubtrop   = Basin('sstrop', 'South subtropic', SimpleRectangle(-180, 180, -40, -23.5).points)  # between -40 degrees and the Tropic of Capricorn
stemperate = Basin('stemp',  'South Temperate', SimpleRectangle(-180, 180, -60, -40).points)    # between Antarctic Cicle and -40 degrees
spolar     = Basin('spole',  'South Pole',      SimpleRectangle(-180, 180, -90, -66.56).points) # between the South Pole and Antarctic Cicle

subtropic  = ComposedBasin('strop', 'Subtropic', [nsubtrop,ssubtrop])
temperate  = ComposedBasin('temp',  'Temperate', [ntemperate,stemperate])
polar      = ComposedBasin('polar', 'Polar',     [npolar,spolar])


del print_function, division, Basin, ComposedBasin, SimpleRectangle