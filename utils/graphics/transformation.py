import numpy
import unittest
import copy

# class Matrix:
# 	self.matrix = None


def identity_matrix(size = 4):
	"""Return an Identity matrix of 'size' size. Default is 4x4."""
	return numpy.identity(size)


def isSquare(input_mat):
	"""Return whether the matrix is square"""
	return all (len (row) == len (input_mat) for row in input_mat)

def convert_to_homogenous(input_mat):
	"""Return a homogenous coordinate transform from a nonhomogenous coordinate transform"""
	assert isSquare(input_mat)
	hom = numpy.zeros([len(input_mat)+1,len(input_mat)+1])
	hom[:-1,:-1] = copy.deepcopy(input_mat)
	hom[-1,-1] = 1
	return hom

def convert_to_non_homogenous(input_mat):
	"""Return a nonhomogenous coordinate transform from a homogenous coordinate transform"""
	assert isSquare(input_mat)
	for i in range(len(input_mat)-1):
		assert input_mat[-1,i] == 0
		assert input_mat[i,-1] == 0
	assert input_mat[-1,-1] == 1

	nonhom = copy.deepcopy(input_mat[:-1,:-1])
	assert isSquare(nonhom)
	#TODO: copy or not copy
	return nonhom

def translate(trans):
	"""Returns homogenous translation transform"""
	nonhom = identity_matrix(len(trans)+1)
	for i in range(len(trans)):
		nonhom[i,-1] = trans[i]
	return nonhom

def rotate2D(angle,unit = 'radian'):
	"""Returns 2D homogenous rotation transform for an angle in radian(default)"""
	assert (unit=='radian' or unit=='degree')
	if unit=='degree':
		angle = numpy.radians(angle)

	c = numpy.cos(angle)
	s = numpy.sin(angle)

	mat = numpy.zeros([2,2])
	mat[0,0] = c
	mat[0,1] = -s
	mat[1,0] = s
	mat[1,1] = c
	return convert_to_homogenous(mat)

def rotate_along_base_axis(angle,unit='radian',axis='X'):
	"""Returns 3D homogenous rotation transform for an angle in radian(default)"""
	assert (unit=='radian' or unit=='degree')
	assert (axis=='X' or axis=='Y' or axis=='Z')
	numerical_axis = 0
	if axis=='Y':
		numerical_axis = 1
	if axis=='Z':
		numerical_axis = 2

	if unit=='degree':
		angle = numpy.radians(angle)

	c = numpy.cos(angle)
	s = numpy.sin(angle)

	mat = numpy.identity(3)
	mat[(numerical_axis+1)%3,(numerical_axis+1)%3] = c
	mat[(numerical_axis+1)%3,(numerical_axis+2)%3] = -s
	mat[(numerical_axis+2)%3,(numerical_axis+1)%3] = s
	mat[(numerical_axis+2)%3,(numerical_axis+2)%3] = c
	return convert_to_homogenous(mat)


# def rotate3D(angles,unit='radian',order='xyz'):


def scale(scaling_factor):
	"""Returns homogenous scaling transform"""
	nonhom = identity_matrix(len(scaling_factor)+1)
	for i in range(len(scaling_factor)):
		nonhom[i,i] = scaling_factor[i]
	return nonhom

# def shear()

# def general

