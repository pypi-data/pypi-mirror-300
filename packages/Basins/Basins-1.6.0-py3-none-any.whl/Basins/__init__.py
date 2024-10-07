#!/usr/bin/env python

# Edited by amiro and eterzic 25.01.2021

__VERSION__ = '1.2.0'

from .basic    import Point, Ball, Polygon
from .entities import Basin, ComposedBasin, Line, SimpleRectangle, Rectangle, Plane, SimpleCube, Cube
from .         import generic, climate, hydrolakes, worldseas, worldcountries, adriatic, baltic, mediterranean

del basic, entities