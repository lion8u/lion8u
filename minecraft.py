from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import numpy 
from perlin_noise import PerlinNoise
from numpy.core.shape_base import block
from numpy import abs
import time


app = Ursina()

window.color = color.rgb(0,0,255)
window.exit_button.visible = False

prevTime = time.time()

scene.fog_color = color.rgb(255,255,255)
scene.fog_density = 0.02

grassStrokeTex = load_texture('grass.png')
wireTex = load_texture('wireframe.png')
monoTex = load_texture('grass.png')
stoneTex = load_texture('grass_mono.png')

bte = Entity(model='cube',texture=wireTex)
class BTYPE:
	STONE = color.rgb(255,255,255)
	GRASS = color.rgb(0,255,0)
	SOIL = color.rgb(150,70,0)
	RUBY = color.rgb(255,0,0)

blockType = BTYPE.SOIL
buildMode = -1 # -1 is OFF, 1 is ON

def buildTool():
    if buildMode == -1:
    	bte.visible = False
    	return
    else: 
    	bte.visible = True
    bte.position = round(subject.position + 
    	            camera.forward * 3)
    bte.y += 2
    bte.y = round(bte.y)
    bte.x = round(bte.x)
    bte.z = round(bte.z)
    bte.color = blockType

def build():
	e = duplicate(bte)
	e.collider = 'cube'
	e.texture = stoneTex
	e.color = blockType


def input(key):
	global blockType
	global buildMode
	if key == 'q' or key == 'escape':
		quit()
	if key == 'g': generateSubset()
	
	if buildMode == 1 and key == 'left mouse down':
		e = mouse.hovered_entity
		build()
	elif buildMode == 1 and key == 'right mouse down':
		e = mouse.hovered_entity
		if e and e.visible==True:
			destroy(e)
	if key == 'f': buildMode *= -1

	if key == '1': blockType=BTYPE.SOIL
	if key == '2': blockType=BTYPE.GRASS
	if key == '3': blockType=BTYPE.STONE
	if key == '4': blockType=BTYPE.RUBY


def update():
    global prevZ, prevX, prevTime, amp
    if  abs(subject.z - prevZ) > 1 or \
        abs(subject.x - prevX) > 1:
        generateShell()
    if time.time() - prevTime > 0.5:
    	generateSubset()
    	#prevTime = time.time()
    if subject.y < -amp-1:
    	subject.y = subject.height + floor((noise([subject.x/freq,
    		                subject.z/freq]))*amp)
    	subject.land()

    buildTool()


noise = PerlinNoise(octaves=3,seed=2021)
amp = 6
freq = 100


terrain = Entity(model=None, collider=None)
terrainWidth = 100
subWidth = int(terrainWidth/1)
subsets = []
subCubes = []
sci = 0
currentSubset = 0

# Instantiate our 'ghost' subset cubes.
for i in range(subWidth):
	bud = Entity(model='cube')
	subCubes.append(bud)
# Instantiate our empty subsets.
for i in range(int((terrainWidth*terrainWidth)/subWidth)):
	bud = Entity(model=None)
	bud.parent = terrain
	subsets.append(bud)

def generateSubset():
	global sci, currentSubset, freq, amp
	if currentSubset >= len(subsets): 
		
		return
	for i in range(subWidth):
		x = subCubes[i].x = floor((i+sci)/terrainWidth)
		z = subCubes[i].z = floor((i+sci)%terrainWidth)
		y = subCubes[i].y = floor((noise([x/freq,z/freq]))*amp)
		subCubes[i].parent = subsets[currentSubset]
		
        # Set color of subCube 
		r = 0
		g = 0
		b = 0
		g = 255
		subCubes[i].color = color.rgb(r,g,b)
		subCubes[i].visible = False

	subsets[currentSubset].combine(auto_destroy=False)
	subsets[currentSubset].texture = grassStrokeTex   	
	sci += subWidth
	currentSubset += 1





#for i in range(terrainWidth*terrainWidth):
	#bud = Entity(model='cube',color=color.green)

	#bud.x = floor(i/terrainWidth)
	#bud.z = floor(i%terrainWidth)
	#bud.y = floor((noise([bud.x/freq,bud.z/freq]))*amp)
	#bud.parent = terrain

#terrain.combine()
#terrain.collider = 'mesh'
#terrain.texture = grassStrokeTex


shellies = []
shellWidth = 3
for i in range(shellWidth*shellWidth):
	bud = Entity(model='cube',collider='box')
	bud.visible = False
	shellies.append(bud)

def generateShell():
	global shellWidth, amp, freq
	for i in range(len(shellies)):
		x = shellies[i].x = floor((i/shellWidth) + 
			                subject.x - 0.5*shellWidth)
		z = shellies[i].z = floor((i%shellWidth) + 
			                subject.z - 0.5*shellWidth)
		shellies[i].y = floor((noise([x/freq,z/freq]))*amp)




subject = FirstPersonController()
subject.x = subject.z = 5
subject.y = 12
subject.gravity = 0.5
prevZ = subject.z
prevX = subject.x

generateShell()

app.run()
