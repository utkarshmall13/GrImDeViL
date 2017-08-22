import unittest
import transformation
import numpy

class MyTest(unittest.TestCase):
	def test_convert_to_homogenous(self):
		hom = transformation.convert_to_homogenous(transformation.identity_matrix(2))
		self.assertEqual(len(hom), 3)
		self.assertEqual(len(hom[0]), 3)
		self.assertEqual(len(hom[1]), 3)
		self.assertEqual(len(hom[2]), 3)

	def test_convert_to_non_homogenous(self):
		hom = transformation.convert_to_homogenous(transformation.identity_matrix(2))
		nonhom = transformation.convert_to_non_homogenous(hom)

		self.assertEqual(len(nonhom[0]), 2)
		self.assertEqual(len(nonhom[1]), 2)
		self.assertEqual(nonhom[0,0],1)

	def test_translate(self):
		trans = transformation.translate([1,2,3])
		vector = numpy.array([1,2,3,1])
		result = trans.dot(vector)
		self.assertEqual(result[0], 2)
		self.assertEqual(result[1], 4)
		self.assertEqual(result[2], 6)

	def test_rotate2D(self):
		rot2d = transformation.rotate2D(45,unit = 'degree')
		vector = numpy.array([1,0,1])
		result = rot2d.dot(vector)
		print(result)
		self.assertAlmostEqual(result[0], 0.7071, places=4)
		self.assertAlmostEqual(result[1], 0.7071, places=4)
		self.assertAlmostEqual(result[2], 1, places=4)

	def test_rotate_along_base_axis(self):
		rot2d = transformation.rotate_along_base_axis(45,unit = 'degree')
		vector = numpy.array([1,0,1])
		result = rot2d.dot(vector)
		print(result)
		self.assertAlmostEqual(result[0], 0.7071, places=4)
		self.assertAlmostEqual(result[1], 0.7071, places=4)
		self.assertAlmostEqual(result[2], 1, places=4)

	def test_scale(self):
		scal = transformation.scale([0.5,2,3])
		vector = numpy.array([1,2,3,1])
		result = scal.dot(vector)
		self.assertEqual(result[0], 0.5)
		self.assertEqual(result[1], 4)
		self.assertEqual(result[2], 9)


	def run_all_tests(self):
		self.test_convert_to_homogenous()
		self.test_convert_to_non_homogenous()
		self.test_translate()
		self.test_scale()
		self.test_rotate2D()
		print("All test cases passed!")


myTest = MyTest()
myTest.run_all_tests()
