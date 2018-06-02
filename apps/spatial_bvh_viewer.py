import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys
sys.path.append("../graphics")
from controls.Controller import Controller,setKeyCallback

import numpy
import time

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input-file","-if",required=True)
parser.add_argument("--fps","-fps",default=120,type=int)
args = parser.parse_args()
input_file = args.input_file
fps = args.fps

import csv
data = []
with open(input_file,"r") as ifd:
	for row in csv.reader(ifd,delimiter=" "):
		data.append([float(tmp) for tmp in row])
data = numpy.array(data)

# PyOpenGL 3.0.1 introduces this convenience module...
from OpenGL.GL.shaders import *

program = None
# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):                # We call this right after our OpenGL window is created.
	glClearColor(1.0, 1.0, 1.0, 1.0)    # This Will Clear The Background Color To Black
	glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
	glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
	glEnable(GL_DEPTH_TEST)                # Enables Depth Testing
	glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()                    # Reset The Projection Matrix
										# Calculate The Aspect Ratio Of The Window
	gluPerspective(120.0, float(Width)/float(Height), 0.1, 100.0)

	glMatrixMode(GL_MODELVIEW)
 
	if not glUseProgram:
		print('Missing Shader Objects!')
		sys.exit(1)
	global program
	program = compileProgram(
		compileShader('''
			varying vec3 normal;

			void main() {
				normal = gl_NormalMatrix * gl_Normal;
				gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
			}
		''',GL_VERTEX_SHADER),
		compileShader('''
			varying vec3 normal;
			void main() {
				float intensity;
				vec4 color;
				vec3 n = normalize(normal);
				vec3 l = normalize(gl_LightSource[0].position).xyz;
			
				// quantize to 5 steps (0, .25, .5, .75 and 1)
				//intensity = (floor(dot(l, n) * 4.0) + 1.0)/4.0;
				intensity = dot(l, n);
				color = vec4(intensity*1.0, intensity*0.5, intensity*0.5,intensity*1.0);
				//color = vec4(0,0,0,0);
			
				gl_FragColor = color;
			}
	''',GL_FRAGMENT_SHADER),)

def create_frame(current_time,fps=120):
	global start_time
	exact = (current_time-start_time)*fps
	floor = int(exact)
	fraction = exact - int(exact)

	if(floor>=data.shape[0]):
		start_time = time.time()
		exact = 0
		floor = int(exact)
		fraction = exact - int(exact)

	row = data[floor]*(1-fraction) + data[floor+1]*fraction

	for i in range(0,row.shape[0]-1,3):
		glTranslatef(row[i],row[i+1],row[i+2])
		glutSolidSphere(0.5,10,10)
		glTranslatef(-row[i],-row[i+1],-row[i+2])

	glBegin(GL_POLYGON)
	glVertex3f(-50, 0,50.0)
	glVertex3f(50, 0,50.0)
	glVertex3f(50, 0,-50.0)
	glVertex3f(-50, 0,-50.0)
	glEnd()


start_time = time.time()

def DrawGLScene():
	cameraPosition = controller.cameraPosition
	# cameraPosition[1:] = -50
	cameraOrientation = controller.cameraOrientation

	# Clear The Screen And The Depth Buffer
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()                    # Reset The View 

	glTranslatef(cameraPosition[0],cameraPosition[1],cameraPosition[2])
	glRotatef(cameraOrientation[0],1,0,0)	#x
	glRotatef(cameraOrientation[1],0,1,0)	#y
	glRotatef(cameraOrientation[2],0,0,1)	#z
	# Move Left 1.5 units and into the screen 6.0 units.

	if program:
		glUseProgram(program)

	current_time = time.time()
	create_frame(current_time,fps)

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

def main():
	global window
	global controller

	glutInit()
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	
	# get a 640 x 480 window 
	glutInitWindowSize(1280,720)

	window = glutCreateWindow("Test window")

	controller = Controller()
	setKeyCallback(controller)

	glutIdleFunc(DrawGLScene)
	glutDisplayFunc(DrawGLScene)

	InitGL(1280,720)
	glutMainLoop()


if __name__ == "__main__":
	print("Hit ESC key to quit.")
	main()

