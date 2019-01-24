bl_info = {
    "name": "Blender for Halo",
    "description": "A JMS Exporter for Blender.",
    "author": "Lone Starr",
    "version": (1, 0),
    "blender": (2, 71, 0),
    "location": "View3D > TOOLS > Blender for Halo",
    "category": "Import-Export"}

import bpy
from decimal import *
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

numMat = 0
currentIndex = 0
vCount = 0
pCount = 0
vertInRegion = 0
currentVertNum = 0
nodeList = []
orderedNodeList = []
objectsInScene = []
nodeChildIndex = []
nodeRotX = []
nodeRotY = []
nodeRotZ = []
nodeRotW = []
nodePosX = []
nodePosY = []
nodePosZ = []
markerRotW = []
markerRotX = []
markerRotY = []
markerRotZ = []
markerPosX = []
markerPosY = []
markerPosZ = []
markerScale = []
matNames = []
matPath = []
polyList = []
matIndex = []
vertList = []
objNodeIndex = []
vertPos = []
vertNormal = []
vertuv = []
polyMatIndex = []
markerList = []
markerNodeIndex = []
matIndex = {}
nodeIndex = {}
nodeChildList = {}
nodeSiblingIndex = {}


def GetNodeInfo():
	global objectsInScene
	global nodeList
	global orderedNodeList
	global nodeIndex
	global nodeChildList
	global nodeChildIndex
	global nodeSiblingIndex
	global nodeRotX
	global nodeRotY
	global nodeRotZ
	global nodeRotW
	global nodePosX
	global nodePosY
	global nodePosZ
	
	currentIndex = 0

	#Node Info
	for node in range(0, len(bpy.data.objects)):
		if 'frame' in bpy.data.objects[node].name:
			nodeList.append(bpy.data.objects[node])
		elif 'bip01' in bpy.data.objects[node].name:
			nodeList.append(bpy.data.objects[node])
		else:
			pass
	for node in range(0, len(nodeList)):
		if nodeList[node].parent not in nodeList:
			orderedNodeList.append(nodeList[node])
			parentNode = nodeList[node]
	for node in range(0, len(nodeList)):
		try:
			if parentNode == nodeList[node]:
				for child in range(0, len(parentNode.children)):
					if parentNode.children[child] in nodeList:
						orderedNodeList.append(parentNode.children[child])		
					else:
						if '#' not in parentNode.children[child].name:
							objectsInScene.append(parentNode.children[child])
						else:pass
			else:
				for child in range(0, len(nodeList[node].children)):
					if nodeList[node].children[child] in nodeList:
						orderedNodeList.append(nodeList[node].children[child])
					else:
						if '#' not in nodeList[node].children[child].name:
							objectsInScene.append(nodeList[node].children[child])
						else:
							pass
		except IndexError:
			pass
			
	sortedNodeList = []
	for node in range(1, len(nodeList)):
		currentNode = orderedNodeList[node]
		sortedNodeList.append(currentNode.name)
	sorted(sortedNodeList)
	parentNode = orderedNodeList[0]
	orderedNodeList = []
	orderedNodeList.append(parentNode)
	nodeIndex[parentNode] = currentIndex
	currentIndex = currentIndex + 1
	for node in range(0, len(sortedNodeList)):
		orderedNodeList.append(bpy.data.objects[sortedNodeList[node]])
		nodeIndex[bpy.data.objects[sortedNodeList[node]]] = currentIndex
		currentIndex = currentIndex + 1
	for node in range(0, len(nodeList)):
		currentNode = []
		for x in range(0, len(orderedNodeList[node].children)):
			if orderedNodeList[node].children[x] in nodeList:
				currentNode.append(orderedNodeList[node].children[x])
		nodeChildList[orderedNodeList[node]] = currentNode
	for node in range(0, len(nodeList)):
		try:
			nodeChildIndex.append(nodeIndex[nodeChildList[orderedNodeList[node]][0]])
		except IndexError:
			nodeChildIndex.append("-1")
	for node in range(0, len(nodeList)):
		if len(nodeChildList[orderedNodeList[node]]) > 1:
			for sibling in range(0, len(nodeChildList[orderedNodeList[node]])):
				try:
					nodeSiblingIndex[nodeChildList[orderedNodeList[node]][sibling]] = nodeIndex[nodeChildList[orderedNodeList[node]][sibling + 1]]
				except IndexError:
					pass
	for node in range(0, len(nodeList)):
		#rotation
		nodeRotW.append(str(Decimal(orderedNodeList[node].rotation_quaternion[0]).quantize(Decimal('0.000001'))))
		nodeRotX.append(str(Decimal(orderedNodeList[node].rotation_quaternion[1]).quantize(Decimal('0.000001'))))
		nodeRotY.append(str(Decimal(orderedNodeList[node].rotation_quaternion[2]).quantize(Decimal('0.000001'))))
		nodeRotZ.append(str(Decimal(orderedNodeList[node].rotation_quaternion[3]).quantize(Decimal('0.000001'))))
		
		#Location
		nodePosX.append(str(Decimal(orderedNodeList[node].location[0] * 100).quantize(Decimal('0.000001'))))
		nodePosY.append(str(Decimal(orderedNodeList[node].location[1] * 100).quantize(Decimal('0.000001'))))
		nodePosZ.append(str(Decimal(orderedNodeList[node].location[2] * 100).quantize(Decimal('0.000001'))))
		
def GetMaterialInfo(mesh):
	global numMat
	global matNames
	global matPath
	global matIndex
	global currentIndex
	global markerList
	
	#Material Info
	try:
		for mat in range(0, len(mesh.data.materials)):
			currentName = mesh.data.materials[mat].name
			currentMat = mesh.data.materials[mat]
			if currentName not in matNames:
				matNames.append(currentName)
				matIndex[currentName] = currentIndex
				currentIndex = currentIndex + 1
				try:
					currentPath = currentMat.texture_slots[0].texture.image.filepath
					matPath.append(currentPath)
				except AttributeError:
					matPath.append("<none>")
	
	#Number of materials
		numMat = len(matNames)
	except AttributeError:	
		print("Error: No materials.")
		
def GetMarkerInfo():
	global markerNodeIndex
	global markerRotW
	global markerRotX
	global markerRotY
	global markerRotZ
	global markerPosX
	global markerPosY
	global markerPosZ
	global markerScale
	for node in range(0, len(nodeList)):
		for marker in range(0, len(orderedNodeList[node].children)):
			if '#' in orderedNodeList[node].children[marker].name:
				markerList.append(orderedNodeList[node].children[marker])
				markerNodeIndex.append(nodeIndex[orderedNodeList[node]])
				markerRotW.append(str(Decimal(orderedNodeList[node].children[marker].rotation_quaternion[0]).quantize(Decimal('0.000001'))))
				markerRotX.append(str(Decimal(orderedNodeList[node].children[marker].rotation_quaternion[1]).quantize(Decimal('0.000001'))))
				markerRotY.append(str(Decimal(orderedNodeList[node].children[marker].rotation_quaternion[2]).quantize(Decimal('0.000001'))))
				markerRotZ.append(str(Decimal(orderedNodeList[node].children[marker].rotation_quaternion[3]).quantize(Decimal('0.000001'))))
				markerPosX.append(str(Decimal(orderedNodeList[node].children[marker].location[0] * 100).quantize(Decimal('0.000001'))))
				markerPosY.append(str(Decimal(orderedNodeList[node].children[marker].location[1] * 100).quantize(Decimal('0.000001'))))
				markerPosZ.append(str(Decimal(orderedNodeList[node].children[marker].location[2] * 100).quantize(Decimal('0.000001'))))
				markerScale.append(Decimal(orderedNodeList[node].children[marker].dimensions[0] * 100).quantize(Decimal('0.000001')))
	print(markerList)

def GetRegionInfo():
	global regionName
	
	regionName = []
	for region in range(0, len(bpy.data.groups)):
		regionName.append(bpy.data.groups[region].name)

def GetVertexInfo(mesh):
	global vertInRegion
	global currentVertNum
	global numPoly
	global polyList
	global vertList
	global vertPos
	global vertNormal
	global vertuv
	global polyMatIndex
	global vCount
	global objNodeIndex
	
	vertInRegion = vertInRegion + len(mesh.data.polygons) * 3
	wMatrix = mesh.matrix_world
	vertNum = []
	polyNum = []
	for poly in range(0, len(mesh.data.polygons)):
		currentIndex = mesh.data.polygons[poly].material_index
		currentMaterial = mesh.data.materials[currentIndex].name
		currentPoly = mesh.data.polygons[poly]
		polyList.append(currentPoly)
		polyNum.append(currentPoly)
		currentVert = polyNum[poly].vertices
		vertNum.append(currentVert)
		polyMatIndex.append(matIndex[currentMaterial])
	for poly in range(0, len(mesh.data.polygons)):
		vertList.append(mesh.data.vertices[vertNum[poly][0]])
		vertList.append(mesh.data.vertices[vertNum[poly][1]])
		vertList.append(mesh.data.vertices[vertNum[poly][2]])
		vertNormal.append(mesh.data.vertices[vertNum[poly][0]].normal)
		vertNormal.append(mesh.data.vertices[vertNum[poly][1]].normal)
		vertNormal.append(mesh.data.vertices[vertNum[poly][2]].normal)
		objNodeIndex.append(nodeIndex[mesh.parent])
		objNodeIndex.append(nodeIndex[mesh.parent])
		objNodeIndex.append(nodeIndex[mesh.parent])
	for v in range (vCount, len(vertList)):
		currentVert = vertList[v].co
		worldVert = wMatrix * currentVert
		vertPos.append(worldVert)
		vCount = len(vertList)
	for v in range (0, len(mesh.data.polygons) * 3):
		vertuv.append(mesh.data.vertices.data.uv_layers.active.data[v].uv)


def WriteToFile(context, filepath):
	global pCount
	
	f = open(filepath, 'w',)
	
	#Top of File
	f.write("8200\n")
	f.write("3251\n")
	
	#Node Info
	GetNodeInfo()
	f.write(str(len(nodeList)) + "\n")
	for node in range(0, len(nodeList)):
		f.write(orderedNodeList[node].name + "\n")
		currentIndex = int(nodeChildIndex[node])
		f.write(str(currentIndex) + "\n")
		try:
			currentIndex = int(nodeSiblingIndex[orderedNodeList[node]])
			f.write(str(currentIndex - 1) + "\n")
		except KeyError:
			f.write("-1\n")
		f.write(nodeRotX[node] + "\t")
		f.write(nodeRotY[node] + "\t")
		f.write(nodeRotZ[node] + "\t")
		f.write(nodeRotW[node] + "\n")
		f.write(nodePosX[node] + "\t")
		f.write(nodePosY[node] + "\t")
		f.write(nodePosZ[node] + "\n")
		
		
	#Material Info
	for obj in range(0, len(objectsInScene)):
		GetMaterialInfo(objectsInScene[obj])
	f.write(str(numMat) + "\n")
	for mat in range(0, numMat):
		f.write(matNames[mat] + "\n")
		correctFilePath = matPath[mat].replace('.tif', '')
		f.write(correctFilePath + "\n")
		
	#Marker Info
	GetMarkerInfo()
	f.write(str(len(markerList)) + "\n")
	for marker in range(0, len(markerList)):
		correctMarkerName = markerList[marker].name.replace('#', '')
		f.write(correctMarkerName + "\n")
		f.write("-1\n")
		f.write(str(markerNodeIndex[marker]) + "\n")
		f.write(markerRotX[marker] + "\t")
		f.write(markerRotY[marker] + "\t")
		f.write(markerRotZ[marker] + "\t")
		f.write(markerRotW[marker] + "\n")
		f.write(markerPosX[marker] + "\t")
		f.write(markerPosY[marker] + "\t")
		f.write(markerPosZ[marker] + "\n")
		f.write(str(markerScale[marker]) + "\n")
	#Region Info
	GetRegionInfo()
	f.write(str(len(regionName)) + "\n")
	for region in range(0, len(regionName)):
		f.write(regionName[region] + "\n")
		for obj in range(0, len(bpy.data.groups[region].objects)):
			GetVertexInfo(bpy.data.groups[region].objects[obj])
	#Vertex Info
			f.write(str(vertInRegion) + "\n")
			for vert in range(0, vertInRegion):
				f.write(str(objNodeIndex[vert]) + "\n")
				f.write(str(Decimal(vertPos[vert][0] * 100).quantize(Decimal('0.000001'))) + "\t" +
				str(Decimal(vertPos[vert][1] * 100).quantize(Decimal('0.000001'))) + "\t" + 
				str(Decimal(vertPos[vert][2] * 100).quantize(Decimal('0.000001'))) + "\n")
				f.write(str(Decimal(vertNormal[vert][0]).quantize(Decimal('0.000001'))) + "\t" +
				str(Decimal(vertNormal[vert][1]).quantize(Decimal('0.000001')))  + "\t" +
				str(Decimal(vertNormal[vert][2]).quantize(Decimal('0.000001'))) + "\n")
				f.write("-1\n")
				f.write("0\n")
				f.write(str(Decimal(vertuv[vert][0]).quantize(Decimal('0.000001'))) + "\n")
				f.write(str(Decimal(vertuv[vert][1]).quantize(Decimal('0.000001'))) + "\n")
				f.write("0\n")
	#Save File
	f.close()
	
	return {'FINISHED'}
	
class ExportToFile(Operator, ExportHelper):
	"""Export to File"""
	bl_idname = "jms.export"
	bl_label = "Export to File"
	
	filename_ext = ".jms"
	
	filter_glob = StringProperty(
		default="*.jms",
		options={'HIDDEN'},
		)
		
	def execute(self, context):
		return WriteToFile(context, self.filepath)
		
class BlenderForHalo(bpy.types.Panel):
	"""Tools panel for exporting to Halo Custom Edition"""
	bl_label = "Blender for Halo"
	bl_idname = "OBJECT_PT_BlenderForHalo"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	
	def draw(self, context):
		layout = self.layout
		
		row = layout.row()
		row.operator('jms.export', text="Export to .jms", icon='FILESEL')

def register():
	bpy.utils.register_class(BlenderForHalo)
	bpy.utils.register_class(ExportToFile)

def unregister():
	bpy.utils.unregister_class(BlenderForHalo)
	bpy.utils.unregister_class(ExportToFile)
	
if __name__ == "__main__":
	register()