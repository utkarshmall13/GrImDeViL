import sys
import numpy
from OpenGL.GLUT import *

class Controller:
	def __init__(self):
		self.lMButtonPressed = False
		self.rMButtonPressed = False
		self.initPressXY = numpy.array([0.0,0.0],dtype=float)
		self.cameraOrient = numpy.array([0.0,0.0,0.0],dtype=float)
		self.cameraPosition = numpy.array([0,0,0.0],dtype=float)
		self.cameraOrientation = numpy.array([0,0,0],dtype=float)

		return

	def keyPressed(self,cmd):
		# If escape is pressed, kill everything.
		key = cmd[0]
		if key.decode('utf-8') == '\x1b':
			sys.exit()
		elif key.decode('utf-8') == 'r':
			self.cameraPosition = numpy.array([0,0,0])
			self.cameraOrientation = numpy.array([0,0,0],dtype=float)

	def specialKeyPressed(self,cmd):
		key = cmd[0]
		if key == 100:			#left
			self.cameraPosition[0]-=0.1
		elif key == 102:			#right
			self.cameraPosition[0]+=0.1
		elif key == 101:			#up
			self.cameraPosition[1]-=0.1
		elif key == 103:			#down
			self.cameraPosition[1]+=0.1

	def mouseKeyPressed(self,cmd):
		key = cmd[0]
		if key == 3:			#in
			self.cameraPosition[2]+=0.1
		elif key == 4:			#out
			self.cameraPosition[2]-=0.1
		if key == 0:			#Pan
			self.lMButtonPressed = not self.lMButtonPressed
			self.initPressXY = numpy.array([cmd[2],cmd[3]])
			self.cameraOrient = numpy.copy(self.cameraOrientation)

	def activeMotion(self,cmd):
		if(self.lMButtonPressed):
			XY = numpy.array([cmd[0],cmd[1]])-self.initPressXY
			XY = XY/5
			self.cameraOrientation *= 0.0
			self.cameraOrientation += self.cameraOrient-(numpy.append(XY[::-1],0.0))
		return


def setKeyCallback(controller):
	glutIgnoreKeyRepeat(1)
	def keyPressed(*args):
		controller.keyPressed(args)
	glutKeyboardFunc(keyPressed)
	def specialKeyPressed(*args):
		controller.specialKeyPressed(args)
	glutSpecialFunc(specialKeyPressed)
	def mouseKeyPressed(*args):
		controller.mouseKeyPressed(args)
	glutMouseFunc(mouseKeyPressed)
	def activeMotion(*args):
		controller.activeMotion(args)
	glutMotionFunc(activeMotion)
