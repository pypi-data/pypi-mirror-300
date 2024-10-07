#!/usr/bin/env python

# Edited by amiro and eterzic 21.02.2021
from __future__ import print_function, division

import sys, os, numpy as np

from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

with open('README.md') as f:
	readme = f.read()


## Read compilation options
options = {}
with open('options.cfg') as f:
	for line in f.readlines():
		if '#' in line or len(line) == 1: continue # Skip comment
		linep = line.split('=')
		options[linep[0].strip()] = linep[1].strip()
		if options[linep[0].strip()] == 'ON':  options[linep[0].strip()] = True
		if options[linep[0].strip()] == 'OFF': options[linep[0].strip()] = False


## Set up compiler options and flags
CC  = 'gcc'   if options['FORCE_GCC'] or not os.system('which icc > /dev/null') == 0 else 'icc'
CXX = 'g++'  if options['FORCE_GCC'] or not os.system('which icc > /dev/null') == 0 else 'icpc'
FC  = 'gfortran' if options['FORCE_GCC'] or not os.system('which icc > /dev/null') == 0 else 'ifort'

CFLAGS   = ''
CXXFLAGS = ' -std=c++11'
FFLAGS   = ''
DFLAGS   = ' -DNPY_NO_DEPRECATED_API'
if CC == 'gcc':
	# Using GCC as a compiler
	CFLAGS   += ' -O0 -g -rdynamic -fPIC' if options['DEBUGGING'] else ' -O%s -ffast-math -fPIC' % options['OPTL']
	CXXFLAGS += ' -O0 -g -rdynamic -fPIC' if options['DEBUGGING'] else ' -O%s -ffast-math -fPIC' % options['OPTL']
	FFLAGS   += ' -O0 -g -rdynamic -fPIC' if options['DEBUGGING'] else ' -O%s -ffast-math -fPIC' % options['OPTL']
	# Vectorization flags
	if options['VECTORIZATION']:
		CFLAGS   += ' -march=native -ftree-vectorize'
		CXXFLAGS += ' -march=native -ftree-vectorize'
		FFLAGS   += ' -march=native -ftree-vectorize'
	# OpenMP flag
	if options['OPENMP_PARALL']:
		CFLAGS   += ' -fopenmp'
		CXXFLAGS += ' -fopenmp'
		DFLAGS   += ' -DUSE_OMP'
else:
	# Using GCC as a compiler
	CFLAGS   += ' -O0 -g -traceback -fPIC' if options['DEBUGGING'] else ' -O%s -fPIC' % options['OPTL']
	CXXFLAGS += ' -O0 -g -traceback -fPIC' if options['DEBUGGING'] else ' -O%s -fPIC' % options['OPTL']
	FFLAGS   += ' -O0 -g -traceback -fPIC' if options['DEBUGGING'] else ' -O%s -fPIC' % options['OPTL']
	# Vectorization flags
	if options['VECTORIZATION']:
		CFLAGS   += ' -x%s -mtune=%s' % (options['HOST'],options['TUNE'])
		CXXFLAGS += ' -x%s -mtune=%s' % (options['HOST'],options['TUNE'])
		FFLAGS   += ' -x%s -mtune=%s' % (options['HOST'],options['TUNE'])
	# OpenMP flag
	if options['OPENMP_PARALL']:
		CFLAGS   += ' -qopenmp'
		CXXFLAGS += ' -qopenmp'
		DFLAGS   += ' -DUSE_OMP'


## Set up environment variables
os.environ['CC']       = CC
os.environ['CXX']      = CXX
os.environ['CFLAGS']   = CFLAGS + DFLAGS
os.environ['CXXFLAGS'] = CXXFLAGS + DFLAGS
os.environ['LDSHARED'] = CC + ' -shared'


## Libraries and includes
libraries     = ['m']

# OSX needs to also link with python for reasons...
if sys.platform == 'darwin': libraries += [f'python{sys.version_info[0]}.{sys.version_info[1]}']


## Compiled modules
Module_Basins = Extension('Basins.basic',
					sources      = ['Basins/basic.pyx','Basins/src/geometry.cpp'],
					language     = 'c++',
					include_dirs = ['Basins/src/',np.get_include()],
					libraries    = libraries,
)

modules_list = [Module_Basins] if options['USE_COMPILED'] else []


## Main setup
setup(
	name                 = "Basins",
	version              = "1.6.0",
	author               = 'Arnau Miro, Elena Terzić',
	author_email         = 'arnau.miro@upc.edu, elena.terzic@proton.me',
	maintainer           = 'Arnau Miro',
	maintainer_email     = 'arnau.miro@upc.edu',	
	ext_modules=cythonize(modules_list,
		language_level = str(sys.version_info[0]), # This is to specify python 3 synthax
		annotate       = False                     # This is to generate a report on the conversion to C code
	),
    long_description     = readme,
    url                  = 'https://github.com/ElenaTerzic/Basins.git',
    packages             = find_packages(exclude=('Examples','doc','ShapefileExtractor')),
	include_package_data = True,
	scripts              = ['bin/basins_info'],
	install_requires     = ['numpy','cython']
)