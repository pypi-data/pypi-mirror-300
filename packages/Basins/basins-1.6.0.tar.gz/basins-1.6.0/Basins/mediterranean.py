#!/usr/bin/env python

# Edited by amiro and eterzic 19.09.2024

from __future__ import print_function, division

import os, numpy as np

from .entities import Basin, ComposedBasin


# OGS Basins

alb  = Basin.from_array('alb'  , 'Alboran Sea'                      , np.array([[-5.5, 32.0, 0.],[-1.0, 32.0, 0.],[-1.0, 40.0, 0.],[-5.5, 40.0, 0.]]))
swm1 = Basin.from_array('swm1' , 'South Western Mediterranean west' , np.array([[-1.0, 32.0, 0.],[5.0 , 32.0, 0.], [5.0, 39.5, 0.],[-1.0, 39.5, 0.]]))
swm2 = Basin.from_array('swm2' , 'South Western Mediterranean east' , np.array([[  5., 32.0, 0.],[9.25, 32.0, 0,],[9.25, 39.5, 0,],[   5, 39.5, 0.]]))
nwm  = Basin.from_array('nwm'  , 'North Western Mediterranean'      , np.array([[-1.0, 39.5, 0.],[9.25, 39.5, 0.],[9.25, 46. , 0.],[-1.0, 46. , 0.]]))
tyr1 = Basin.from_array('tyr1' , 'Northern Tyrrhenian'              , np.array([[9.25, 41.25, 0.],[15.0, 41.25, 0.],[10.0, 46.0 , 0.],[9.25, 46.0 , 0.]]))
tyr2 = Basin.from_array('tyr2' , 'Southern Tyrrhenian'              , np.array([[9.25, 36.75, 0.],[15.0, 36.75, 0.],[15.0, 38.0 , 0.],[15.6, 38.2 , 0.],[16.1, 38.2 , 0.],[16.5, 39.5 , 0.],[15.0, 41.25, 0.],[9.25, 41.25, 0.]]))

ion1 = Basin.from_array('ion1' , 'Western Ionian'                   , np.array([[9.25, 32.0,  0.],[15.0, 32.0,  0.],[15.0, 36.75, 0.],[10.7, 36.75, 0.],[9.25, 35.0 , 0.]]))
ion2 = Basin.from_array('ion2' , 'Eastern Ionian'                   , np.array([[15.0 , 30.0 , 0.],[21.85, 30.0 , 0.],[21.85, 36.75, 0.],[15.0 , 36.75, 0.]]) )
ion3 = Basin.from_array('ion3' , 'Northern Ionian'                  , np.array([[15.0 , 36.75, 0.],[21.85, 36.75, 0.],[21.85, 40.0 , 0.],[18.5 , 40.0 , 0.],[17.0 , 41.0 , 0.],[16.1 , 40.0 , 0.],[16.5 , 39.5 , 0.],[16.1 , 38.2 , 0.],[15.6 , 38.2 , 0.],[15.0 , 38.0 , 0.]]))

adr1 = Basin.from_array('adr1' , 'Northern Adriatic'                , np.array([[10. , 46. , 0.],[13.0, 42.5, 0.],[20.0, 42.5, 0.],[15.0, 46.0, 0.]])) 
adr2 = Basin.from_array('adr2' , 'Southern Adriatic'                , np.array([[14.0, 42.5, 0.],[20.0, 42.5, 0.],[20.0, 40.0, 0.],[18.5, 40.0, 0.],[18.0, 40.5, 0.],[16.6, 41.0, 0.],[13.0, 42.5, 0.]]))

lev1 = Basin.from_array('lev1' , 'Western Levantine'                , np.array([[21.85, 30.0, 0.],[26.25, 30.0, 0.],[26.25, 35.1, 0.],[24.9 , 35.1, 0.],[24.0 , 35.3, 0.],[21.85, 35.3, 0.]]))
lev2 = Basin.from_array('lev2' , 'Northern Levantine'               , np.array([[26.25, 33.60, 0.],[33.00, 33.60, 0.],[33.00, 38.00, 0.],[28.00, 38.00, 0.],[28.00, 35.30, 0.],[26.30, 35.30, 0.],[26.25, 35.28, 0.]]))
lev3 = Basin.from_array('lev3' , 'Southern Levantine'               , np.array([[26.25, 30.00, 0.],[26.25, 33.60, 0.],[33.00, 33.60, 0.],[33.00, 30.00, 0.]]))
lev4 = Basin.from_array('lev4' , 'Eastern Levantine'                , np.array([[33.0, 30.0, 0.],[37.0, 30.0, 0.],[37.0, 38.0, 0.],[33.0, 38.0, 0.]]))

aeg  = Basin.from_array('aeg'  , 'Aegean Sea'                       , np.array([[21.85, 35.30, 0.],[24.00, 35.30, 0.],[24.90, 35.10, 0.],[26.25, 35.10, 0.],[26.25, 35.28, 0.],[26.30, 35.30, 0.],[28.00, 35.30, 0.],[28.00, 42.00, 0.],[21.85, 42.00, 0.]]) )


# Composed basins - 3 regions
wmed = ComposedBasin('wmed', 'Western Mediterranean', [alb , swm1, swm2, nwm, tyr1, tyr2])
emed = ComposedBasin('emed', 'Eastern Mediterranean', [lev1, lev2, lev3, lev4, aeg])
cmed = ComposedBasin('cmed', 'Central Mediterranean', [adr1, adr2, ion1, ion2, ion3])

# Regional
lev  = ComposedBasin('lev', 'Levantine Sea', [lev1, lev2, lev3, lev4])
ion  = ComposedBasin('ion', 'Ionian Sea'   , [ion1, ion2, ion3] )
adr  = ComposedBasin('adr', 'Adriatic Sea' , [adr1, adr2])
tyr  = ComposedBasin('tyr', 'Tyrrenian Sea' ,[tyr1, tyr2])
swm  = ComposedBasin('swm', 'South Western Mediterraneaan Sea',[swm1, swm2])


del print_function, division, os, np, Basin, ComposedBasin