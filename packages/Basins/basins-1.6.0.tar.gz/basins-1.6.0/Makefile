# Compile Basins
#   Compile with g++ or Intel C++ Compiler
#   Compile with the most aggressive optimization setting (O3)
#   Use the most pedantic compiler settings: must compile with no warnings at all
#
# The user may override any desired internal variable by redefining it via command-line:
#   make CXX=g++ [...]
#   make OPTL=-O2 [...]
#   make FLAGS="-Wall -g" [...]
#
# Arnau Miro 2021

# Include user-defined build configuration file
include options.cfg

# Compilers
#
# Automatically detect if the intel compilers are installed and use
# them, otherwise default to the GNU compilers
ifeq ($(FORCE_GCC),ON) 
	# Forcing the use of GCC
	# C Compiler
	CC = gcc
	# C++ Compiler
	CXX = g++
	# Fortran Compiler
	FC = gfortran
else
	ifeq (,$(shell which icc))
		# C Compiler
		CC = gcc
		# C++ Compiler
		CXX = g++
		# Fortran Compiler
		FC = gfortran
	else
		# C Compiler
		CC = icc
		# C++ Compiler
		CXX = icpc
		# Fortran Compiler
		FC = ifort
	endif
endif

# Compiler flags
#
ifeq ($(CC),gcc)
	# Using GCC as a compiler
	ifeq ($(DEBUGGING),ON)
		# Debugging flags
		CFLAGS   += -O0 -g -rdynamic -fPIC
		CXXFLAGS += -O0 -g -rdynamic -fPIC
		FFLAGS   += -O0 -g -rdynamic -fPIC
	else
		CFLAGS   += -O$(OPTL) -ffast-math -fPIC
		CXXFLAGS += -O$(OPTL) -ffast-math -fPIC
		FFLAGS   += -O$(OPTL) -ffast-math -fPIC
	endif
	# Vectorization flags
	ifeq ($(VECTORIZATION),ON)
		CFLAGS   += -march=native -ftree-vectorize
		CXXFLAGS += -march=native -ftree-vectorize
		FFLAGS   += -march=native -ftree-vectorize
	endif
	# OpenMP flag
	ifeq ($(OPENMP_PARALL),ON)
		CFLAGS   += -fopenmp -DUSE_OMP
		CXXFLAGS += -fopenmp -DUSE_OMP
	endif
else
	# Using INTEL as a compiler
	ifeq ($(DEBUGGING),ON)
		# Debugging flags
		CFLAGS   += -O0 -g -traceback -fPIC
		CXXFLAGS += -O0 -g -traceback -fPIC
		FFLAGS   += -O0 -g -traceback -fPIC
	else
		CFLAGS   += -O$(OPTL) -fPIC
		CXXFLAGS += -O$(OPTL) -fPIC
		FFLAGS   += -O$(OPTL) -fPIC
	endif
	# Vectorization flags
	ifeq ($(VECTORIZATION),ON)
		CFLAGS   += -x$(HOST) -mtune=$(TUNE)
		CXXFLAGS += -x$(HOST) -mtune=$(TUNE)
		FFLAGS   += -x$(HOST) -mtune=$(TUNE)
	endif
	# OpenMP flag
	ifeq ($(OPENMP_PARALL),ON)
		CFLAGS   += -qopenmp -DUSE_OMP
		CXXFLAGS += -qopenmp -DUSE_OMP
	endif
endif
# C++ standard
CXXFLAGS += -std=c++11
# Header includes
CXXFLAGS += -I${INC_PATH}

# Defines
#
DFLAGS = -DNPY_NO_DEPRECATED_API

# One rule to compile them all, one rule to find them,
# One rule to bring them all and in the compiler link them.
all: requirements python install
	@echo ""
	@echo "Basins deployed successfully"


# Python
#
python: setup.py
	@CC="${CC}" CFLAGS="${CFLAGS} ${DFLAGS}" CXX="${CXX}" CXXFLAGS="${CXXFLAGS} ${DFLAGS}" LDSHARED="${CC} -shared" ${PYTHON} $< build_ext --inplace
	@echo "Python programs deployed successfully"

requirements: requirements.txt
	@${PIP} install -r $<

install: 
	@CC="${CC}" CFLAGS="${CFLAGS} ${DFLAGS}" CXX="${CXX}" CXXFLAGS="${CXXFLAGS} ${DFLAGS}" LDSHARED="${CC} -shared" ${PIP} install .

install_dev: 
	@CC="${CC}" CFLAGS="${CFLAGS} ${DFLAGS}" CXX="${CXX}" CXXFLAGS="${CXXFLAGS} ${DFLAGS}" LDSHARED="${CC} -shared" ${PIP} install -e .

package-build:
	@CFLAGS="${CFLAGS}" CXXFLAGS="${CXXFLAGS}" LDSHARED="${CC} -shared" ${PYTHON} -m build


# Generic object makers
#
%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $< $(DFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $< $(DFLAGS)

%.o: %.f
	$(FC) $(FFLAGS) -c -o $@ $< $(DFLAGS)

%.o: %.f90
	$(FC) $(FFLAGS) -c -o $@ $< $(DFLAGS)


# Clean
#
clean:
	-@cd Basins; rm -f *.o *.pyc *.c *.cpp *.html
	-@cd Basins; rm -rf __pycache__ 
	-@rm -rf  build

uninstall: clean
	-@cd Basins; rm *.so
	-@${PIP} uninstall Basins
	-@rm -rf Basins.egg-info
