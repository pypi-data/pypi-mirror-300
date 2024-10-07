#!/usr/bin/env python

# Edited by amiro and eterzic 25.01.2021

from __future__ import print_function, division

import numpy as np

from .basic import Point, Ball, Polygon


class Basin(Polygon):
	'''
	A region defined by a polygon.
	'''
	def __init__(self,abbrev,name,points):
		super(Basin, self).__init__(points)
		self._abbrev = abbrev
		self._name   = name

	def __str__(self):
		retstr = 'Basin %s (%s) with %d points:\n' % (self.name,self.abbrev,self.npoints)
		retstr += super(Basin, self).__str__()
		return retstr

	def to_file(self,filename):
		'''
		Dump the x and y coordinates 
		'''
		x, y = self.x, self.y
		file = open(filename,'w')
		for ip in range(self.npoints):
			file.write('%f %f\n'%(x[ip],y[ip]))
		file.close()

	@classmethod
	def from_array(cls,abbrev,name,xyz):
		'''
		Build a basin from an array of points
		of shape (npoints,3).
		'''
		pointList = np.array([Point.from_array(p) for p in xyz],dtype=Point)
		return cls(abbrev,name,pointList)

	@classmethod
	def from_npy(cls,abbrev,name,fname,downsample=1):
		'''
		Build a basin from an array of points
		obtained by reading an npy file.
		'''
		xyz = np.load(fname)
		pointList = np.array([Point.from_array(p) for p in xyz[::downsample,:]],dtype=Point)
		return cls(abbrev,name,pointList)

	@property
	def abbrev(self):
		return self._abbrev

	@property
	def name(self):
		return self._name

	@property
	def box(self):
		return [np.max(self.x),np.min(self.x),np.max(self.y),np.min(self.y)]


class ComposedBasin(object):
	'''
	A region composed by an array of basins
	'''
	def __init__(self,abbrev,name,basins):
		self._abbrev = abbrev
		self._name   = name
		self._list   = basins

	def __str__(self):
		retstr = 'Composed Basin of %d basins:\n' % (len(self.basins))
		for basin in self.basins:
			retstr += basin.__str__()
		return retstr

	# Operators
	def __getitem__(self,i):
		'''
		Polygon[i]
		'''
		return self._list[i]

	def __setitem__(self,i,value):
		'''
		Polygon[i] = value
		'''
		self._list[i] = value

	def __iter__(self):
		return self._list.__iter__()

	def __gt__(self, other):
		'''
		self.isinside(other)
		'''
		if isinstance(other,Point):
			return self.isinside(other) # Return true if Point inside Polygon
		else: # Assume numpy array
			return self.areinside(other)

	def __lt__(self,other):
		'''
		not self.isinside(other)
		'''
		if isinstance(other,Point):
			return not self.isinside(other)
		else:
			return np.logical_not(self.areinside(other))
		
	# Functions
	def isempty(self):
		return len(self.basins) == 0

	def isinside(self,point):
		'''
		Returns True if the point is inside the polygon, else False.
		'''
		for basin in self.basins:
			if basin.isinside(point): return True
		return False

	def isinbasin(self,point):
		'''
		Returns the basin where the point is inside
		'''
		for basin in self.basins:
			if basin.isinside(point): return basin
		return Basin('none','Not Found',np.array([Point(0.,0.,0.)]))

	def areinside(self,xyz):
		'''
		Returns True if the points are inside the polygon, else False.
		'''
		out = np.zeros((xyz.shape[0],len(self.basins)),dtype=bool)
		for ii,basin in enumerate(self.basins):
			out[:,ii] = basin.areinside(xyz)
		return np.logical_or.reduce(out,axis=1)

	def areinbasin(self,xyz):
		'''
		Returns a list with the basins that the points are inside 
		'''		
		out = np.array([Basin('none','Not Found',np.array([Point(0.,0.,0.)]))]*xyz.shape[0],object)
		for ii,basin in enumerate(self.basins):
			mask = basin.areinside(xyz)
			out[mask] = basin
		return out

	def compute_centroid(self):
		'''
		Returns the centroid.
		'''
		out = np.array([0.,0.,0.])
		for basin in self.basins:
			out += basin.compute_centroid().xyz
		out /= len(self.basins)
		return Point.from_array(out)

	@property
	def abbrev(self):
		return self._abbrev

	@property
	def name(self):
		return self._name

	@property
	def basins(self):
		return self._list

	@property
	def centroid(self):
		return self.compute_centroid()

	@property
	def box(self):
		x,y = np.array([],np.double),np.array([],np.double)
		for basin in self.basins:
			x = np.concatenate((x,basin.x))
			y = np.concatenate((y,basin.y))
		return [np.max(x),np.min(x),np.max(y),np.min(y)]


class Line(object):
	'''
	A 2D line defined by 2 points and discretized by a number
	of points inside that line.
	'''
	def __init__(self, p1, p2, npoints=100):
		d = p2 - p1 # vector pointing in the direction of the line
		f = np.linspace(0.,1.,npoints)
		# Preallocate
		self._points = [Point(p1.x,p1.y,p1.z) for p in range(npoints)]
		self._bbox   = [Ball() for p in range(npoints)]
		for ip in range(1,npoints):
			# Build the point list
			self._points[ip].xyz = p1.xyz + f[ip]*d.xyz
			# For each point compute a ball centered on the point with
			# a radius of half the distance to the last point
			vec = self._points[ip] - self._points[ip-1]
			self._bbox[ip] = Ball(self._points[ip],vec.norm())
		# Add the ball for the first point
		vec = self._points[1] - self._points[0]
		self._bbox[0] = Ball(self._points[0],vec.norm())
		if not self._points[-1] == p2: raiseError('Last point does not match!!')
		self._dist = np.array([])

	def isempty(self):
		return self.npoints == 0

	def isinside(self,point,algorithm=None):
		'''
		Returns True if the point is inside (close to) the line, else False.
		'''
		for b in self._bbox:
			if b.isinside(point): return True # Point is inside the bounding box
		return False

	def areinside(self,xyz,algorithm=None):
		'''
		Returns True if the points are inside (close to) the polygon, else False.
		'''
		out = np.zeros((xyz.shape[0],),dtype=bool)
		# Loop on the point boxes and compute the points that are inside the box
		for b in self._bbox:
			idx      = b.areinside(xyz) # Points are inside the bounding box
			out[idx] = True
		return out

	def interpolate(self,xyz,var):
		'''
		Interpolates a variable value to the points of the line.
		Assume xyz and var as masked points.
		'''
		if len(self._dist) == 0:
			self._dist = np.zeros((self.npoints,xyz.shape[0]),dtype=np.double)
			# Loop on the point boxes and compute the points that are inside the box
			for ip,b in enumerate(self._bbox):
				idx = b.areinside(xyz) # Points are inside the bounding box
				if len(idx) > 0:
					vec = xyz[idx] - np.tile(b.center.xyz,(xyz[idx].shape[0],1))
					self._dist[ip,idx] = np.sqrt(np.sum(vec*vec,axis=1))
					# If there is a point matching exactly our point then
					# the distance will be 0, so when we invert the distances
					# the weight should be infinite
					id0 = self._dist[ip,idx] == 0.
					self._dist[ip,idx]      = 1./self._dist[ip,idx]
					self._dist[ip,idx][id0] = 1.e20
		# Compute interpolated variable	
		out = np.zeros((len(self._bbox),var.shape[1]) if len(var.shape) > 1 else (len(self._bbox),) ,dtype=var.dtype)
		sum_dist = np.sum(self._dist,axis=1) # length of npoints on the line
		# Compute the averaged for the field
		if len(var.shape) > 1: 
			# Vectorial array
			for idim in range(var.shape[1]):
				out[:,idim] = np.matmul(self._dist,var[:,idim])/sum_dist
		else:
			# Scalar array
			out[:] = np.matmul(self._dist,var)/sum_dist
		return out

	@property
	def npoints(self):
		return len(self._points)
	@property
	def points(self):
		return self._points
	@points.setter
	def points(self,value):
		self._points = value


class SimpleRectangle(Polygon):
	'''
	2D rectangle. Assumes z = 0 and the points aligned with the axis.
	For any other shape please use Rectangle or Polygon.

	4-------3
	|		|
	|		|
	1-------2
	'''
	def __init__(self,xmin,xmax,ymin,ymax):
		self._abbrev = 'sr'
		self._name   = 'Simple Rectangle'
		pointList = np.array([
			Point(xmin,ymin,0.), # 1
			Point(xmax,ymin,0.), # 2
			Point(xmax,ymax,0.), # 3
			Point(xmin,ymax,0.), # 4
		])
		super(SimpleRectangle, self).__init__(pointList)

	def isinside(self,point,algorithm=None):
		'''
		A fast algorithm for simple rectangles.
		'''
		x_inside = point[0] >= self.points[0][0] and point[0] <= self.points[1][0]
		y_inside = point[1] >= self.points[0][1] and point[0] <= self.points[3][1]
		return x_inside and y_inside

	def areinside(self,xyz,algorithm=None):
		'''
		A fast algorithm for simple rectangles.
		'''
		x_inside = np.logical_and(xyz[:,0] >= self.points[0][0],xyz[:,0] <= self.points[1][0])
		y_inside = np.logical_and(xyz[:,1] >= self.points[0][1],xyz[:,1] <= self.points[3][1])
		return np.logical_and(x_inside,y_inside)

	@classmethod
	def from_array(cls,xyz):
		'''
		Build a square from an array of points
		of shape (npoints,3).
		'''
		npoints   = xyz.shape[0]
		if not npoints == 5: raiseError('Invalid number of points for Rectangle %d' % npoints)
		return super(SimpleRectangle, cls).from_array(xyz)
	
	@property
	def abbrev(self):
		return self._abbrev

	@property
	def name(self):
		return self._name

	@property
	def box(self):
		return [np.max(self.x),np.min(self.x),np.max(self.y),np.min(self.y)]


class Rectangle(Polygon):
	'''
	2D rectangle. Assumes z = 0.

	4-------3
	|		|
	|		|
	1-------2
	'''
	def __init__(self,points):
		if not len(points) == 4: raiseError('Invalid Rectangle!')
		self._abbrev = 'r'
		self._name   = 'Rectangle'
		self._center = Point.from_array(0.25*(points[0].xyz+points[1].xyz+points[2].xyz+points[3].xyz))
		super(Rectangle, self).__init__(points)

	def normal(self):
		'''
		Returns the unitary normal that defines the plane
		of the Rectangle.
		'''
		# Code_Saturne algorithm
		u = self.points[1] - self._center
		v = self.points[0] - self._center
		n = u.cross(v)
		return n/n.norm()

	def project(self,point):
		'''
		Given a point outside the plane defined by the Rectangle, 
		it projects the point into the Rectangle plane.
		'''
		n = self.normal() # Normal to the plane
		if isinstance(point,Point): 
			# We are dealing with a single point
			vp   = point - self.points[0]
			dist = vp.dot(n)
		else:
			# We are dealing with a list of points
			npoints = point.shape[0]
			n       = np.tile(n.xyz,(npoints,)).reshape(npoints,3)
			vp      = point - np.tile(self.points[0].xyz,(npoints,)).reshape(npoints,3)
			dist    = np.tile(np.sum(vp*n,axis=1),(3,1)).T
		# Projected point in the Rectangle plane
		return point + n*dist, dist

	def inclusion3D(self,point):
		'''
		3D inclusion is easily determined by projecting the point and polygon into 2D. 
		To do this, one simply ignores one of the 3D coordinates and uses the other two.
		To optimally select the coordinate to ignore, compute a normal vector to the plane, 
		and select the coordinate with the largest absolute value [Snyder & Barr, 1987]. 
		This gives the projection of the polygon with maximum area, and results in robust computations.

		This function is for internal use inside the Cube method.
		'''
		n   = self.normal()       # Normal to the plane
		p,_ = self.project(point) # Projected point
		# Which is the biggest dimension?
		idmax = np.argmax(np.abs(n.xyz))
		# Convert to xy the smallest dimensions for Rectangle
		points = self.points
		for ip in range(self.npoints):
			points[ip].xyz = np.append(np.delete(self.points[ip].xyz,idmax),np.zeros((1,)))
		self.points = points
		# Redo the bounding box
		self.bbox = Ball.fastBall(self)
		# Do the same for the points
		if isinstance(point,Point):
			p.xyz =  np.append(np.delete(p.xyz,idmax),np.zeros((1,)))
		else:
			npoints = p.shape[0]
			p =  np.append(np.delete(p,idmax,axis=1),np.zeros((npoints,1)),axis=1)
		return p

	@classmethod
	def from_array(cls,xyz):
		'''
		Build a square from an array of points
		of shape (npoints,3).
		'''
		npoints = xyz.shape[0]
		if not npoints == 4: raiseError('Invalid number of points for Rectangle %d' % npoints)
		return super(Rectangle, cls).from_array(xyz)

	@property
	def abbrev(self):
		return self._abbrev

	@property
	def name(self):
		return self._name

	@property
	def box(self):
		return [np.max(self.x),np.min(self.x),np.max(self.y),np.min(self.y)]


class Plane(Rectangle):
	'''
	3D plane in rectangular form, useful for slices.

	4-------3
	|		|
	|		|
	1-------2
	'''
	def __init__(self,points,mindist=0.1):
		self._mindist = mindist
		if not len(points) == 4: raiseError('Invalid Plane!')
		self._abbrev = 'p'
		self._name   = 'Plane'
		super(Plane, self).__init__(points)

	def isinside(self,point,algorithm=None):
		'''
		Project the point to the plane defined by the 3D rectangle
		and obtain the inclusion.
		'''
		# Create an auxiliary rectangle
		points = np.array([self.points[0].xyz,
						   self.points[1].xyz,
						   self.points[2].xyz,
						   self.points[3].xyz
						  ]).copy()
		aux = Rectangle.from_array(points)
		# Obtain the distance of the point to the plane
		_,dist = aux.project(point)
		# Check if the projected point is inside the face
		inside = aux.isinside(aux.inclusion3D(point))
		# Appart from being inside the point has to fulfill the minimum distance
		return inside and dist <= self._mindist

	def areinside(self,xyz,algorithm=None):
		'''
		Project the points to the plane defined by the 3D rectangle
		and obtain the inclusion.
		'''
		# Create an auxiliary rectangle
		points = np.array([self.points[0].xyz,
						   self.points[1].xyz,
						   self.points[2].xyz,
						   self.points[3].xyz
						  ]).copy()
		aux = Rectangle.from_array(points)
		# Obtain the distance of the point to the plane
		_,dist = aux.project(xyz)
		# Check if the projected point is inside the face
		inside = aux.areinside(aux.inclusion3D(xyz))
		# Appart from being inside the point has to fulfill the minimum distance
		print(inside,dist)
		return np.logical_and(inside,np.abs(dist[:,0]) <= self._mindist)

	@property
	def abbrev(self):
		return self._abbrev

	@property
	def name(self):
		return self._name

	@property
	def box(self):
		return [np.max(self.x),np.min(self.x),np.max(self.y),np.min(self.y)]


class SimpleCube(Polygon):
	'''
	3D cube. Assumes the points to be aligned with the axis.
	For any other shape please use Cube or Polygon.

	  8-------7
	 /|      /|
	4-------3 |
	| 5-----|-6
	|/      |/
	1-------2
	'''
	def __init__(self,xmin,xmax,ymin,ymax,zmin,zmax):
		pointList = np.array([
			Point(xmin,ymin,zmin), # 1
			Point(xmax,ymin,zmin), # 2
			Point(xmax,ymax,zmin), # 3
			Point(xmin,ymax,zmin), # 4
			Point(xmin,ymin,zmax), # 5
			Point(xmax,ymin,zmax), # 6
			Point(xmax,ymax,zmax), # 7
			Point(xmin,ymax,zmax), # 8
		])
		super(SimpleCube, self).__init__(pointList)

	def isinside(self,point,algorithm=None):
		'''
		A fast algorithm for cubes.
		'''
		x_inside = point[0] >= self.points[0][0] and point[0] <= self.points[1][0]
		y_inside = point[1] >= self.points[0][1] and point[1] <= self.points[3][1]
		z_inside = point[2] >= self.points[0][2] and point[2] <= self.points[7][2]
		return x_inside and y_inside and z_inside

	def areinside(self,xyz,algorithm=None):
		'''
		A fast algorithm for cubes.
		'''
		x_inside = np.logical_and(xyz[:,0] >= self.points[0][0], xyz[:,0] <= self.points[1][0])
		y_inside = np.logical_and(xyz[:,1] >= self.points[0][1], xyz[:,1] <= self.points[3][1])
		z_inside = np.logical_and(xyz[:,2] >= self.points[0][2], xyz[:,2] <= self.points[7][2])
		return np.logical_and(np.logical_and(x_inside,y_inside),z_inside)

	@classmethod
	def from_array(cls,xyz):
		'''
		Build a cube from an array of points
		of shape (npoints,3).
		'''
		npoints   = xyz.shape[0]
		if not npoints == 8: raiseError('Invalid number of points for Cube %d' % npoints)
		return super(SimpleCube, cls).from_array(xyz)


class Cube(Polygon):
	'''
	3D cube.

	  8-------7
	 /|      /|
	4-------3 |
	| 5-----|-6
	|/      |/
	1-------2
	'''
	def __init__(self,points):
		if not len(points) == 8: raiseError('Invalid Cube!')
		super(Cube, self).__init__(points)
		# Generate the indices for each face
		self._face_ids = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(2,6,7,3),(0,3,7,4),(1,2,6,5)]

	def isinside(self,point,algorithm=None):
		'''
		Project the point to each of the faces of the cube and check
		if the point is inside or outside of the 2D geometry.
		Each face is a rectangle
		'''
		# Loop the faces
		for face_id in self._face_ids:
			face_points = np.array([self.points[face_id[0]].xyz,
							        self.points[face_id[1]].xyz,
							        self.points[face_id[2]].xyz,
							        self.points[face_id[3]].xyz
							      ]).copy()
			# Obtain each face as a Rectangle
			face = Rectangle.from_array(face_points)
			# Check if the projected point is inside the face
			inside = face.isinside(face.inclusion3D(point))
			# If the point is outside the face we can already stop
			if not inside: return False
		# If we reached here it means the point is inside all the faces
		return True

	def areinside(self,xyz,algorithm=None):
		'''
		Project the point to each of the faces of the cube and check
		if the point is inside or outside of the 2D geometry.
		Each face is a rectangle
		'''
		npoints = xyz.shape[0]
		out     = np.ones((npoints,),dtype=bool)
		# Loop the faces
		for face_id in self._face_ids:
			face_points = np.array([self.points[face_id[0]].xyz,
							        self.points[face_id[1]].xyz,
							        self.points[face_id[2]].xyz,
							        self.points[face_id[3]].xyz
							      ]).copy()
			# Obtain each face as a Rectangle
			face = Rectangle.from_array(face_points)
			# Check if the projected points are inside the face
			inside = face.areinside(face.inclusion3D(xyz))
			# Filter out the points that are outside (False)
			out = np.logical_and(out,inside)
		return out

	@classmethod
	def from_array(cls,xyz):
		'''
		Build a cube from an array of points
		of shape (npoints,3).
		'''
		npoints   = xyz.shape[0]
		if not npoints == 8: raiseError('Invalid number of points for Cube %d' % npoints)
		return super(Cube, cls).from_array(xyz)