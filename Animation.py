#***************************************************************************
#*																		 *
#*   Copyright (c) 2014													*  
#*   <microelly2@freecadbuch.de>										   * 
#*																		 *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)	*
#*   as published by the Free Software Foundation; either version 2 of	 *
#*   the License, or (at your option) any later version.				   *
#*   for detail see the LICENCE text file.								 *
#*																		 *
#*   This program is distributed in the hope that it will be useful,	   *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of		*
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		 *
#*   GNU Library General Public License for more details.				  *
#*																		 *
#*   You should have received a copy of the GNU Library General Public	 *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA																   *
#*																		 *
#***************************************************************************

__title__="FreeCAD Animation Toolkit"
__author__ = "Thomas Gundermann"
__url__ = "http://www.freecadbuch.de"

import FreeCAD
if FreeCAD.GuiUp:
	import FreeCADGui
	FreeCADGui.updateLocale()



def say(s):
		FreeCAD.Console.PrintMessage(str(s)+"\n")


import Draft,PyQt4
from PyQt4 import QtGui,QtCore


def errorDialog(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Critical,u"Error Message",msg )
    diag.setWindowFlags(PyQt4.QtCore.Qt.WindowStaysOnTopHint)
    diag.exec_()


##import FreeCAD,Draft,ArchComponent, DraftVecUtils
from FreeCAD import Vector
import math
import Draft, Part, FreeCAD, math, PartGui, FreeCADGui, PyQt4
from math import sqrt, pi, sin, cos, asin
from FreeCAD import Base

if FreeCAD.GuiUp:
	import FreeCADGui
	from PySide import QtCore, QtGui
	from DraftTools import translate
else:
	def translate(ctxt,txt):
		return txt

#---------------------
def say(s):
		FreeCAD.Console.PrintMessage(str(s)+"\n")


#------------------------------------



class _Actor(object):

	def __init__(self,obj,start=10,end=20):
		say("71")
		say(obj)
		say(self.obj.Label)
		say("71a!")
		#self.obj.obj=self.obj.getObject(obj)
		say("got")
		#self.obj.start=start
		#self.obj.end=end
		#if self.obj.obj2:
		#	self.obj.initPlace=	self.obj.obj2.Placement


	def initPlacement(self,tp):
		self.obj.initPlace=tp
		self.obj.obj2.Placement=tp
	def getObject(self,name):
		if  isinstance(name,str):
#			obj=FreeCAD.ActiveDocument.getObject(name)
			objl=App.ActiveDocument.getObjectsByLabel(name)
			obj=objl[0]
			say('obj found')
		else:
			obj=name
		say(obj)
		return obj

	def toInitialPlacement(self):
		self.obj.obj2.Placement=self.obj.initPlace
	def setIntervall(self,s,e):
		self.obj.start=s
		self.obj.end=e
	def step(self,now):
		say("Step" + str(now))


#----------------------
def createMover(count=6,size_bottom = 4, height=10,name='My_Mover'):
	'''makePrism(baseobj,[facenr],[angle],[name]) : Makes a Prism based on a
	regular polygon with count(8) vertexes face and a name (default
	= Prism).'''
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	
#	obj.addProperty("App::PropertyPythonObject","step","zzz","step")
#	obj.addProperty("App::PropertyPythonObject","reverse","zzz","reverse")
#	obj.setEditorMode("reverse", 2)
#	obj.setEditorMode("step", 2)
	
	obj.addProperty("App::PropertyInteger","start","intervall","start").start=10
	obj.addProperty("App::PropertyInteger","end","intervall","end").end=40

	obj.addProperty("App::PropertyPlacement","initPlace","3D Param","initPlace")
	obj.addProperty("App::PropertyVector","motionVector","3D Param","motionVector").motionVector=FreeCAD.Vector(100,0,0)
	obj.addProperty("App::PropertyLink","obj2","3D Param","moving object ")
	obj.addProperty("App::PropertyString","obj2ro","3D Param","moving obj").obj2ro="undefined"
	obj.setEditorMode("obj2ro", 1)
#	obj.addProperty("App::PropertyString","obj2rw","3D Param","Tooltipp bew. Ob").obj2rw="HUGO rw"
#	obj.setEditorMode("obj2rw", 0)
	
	# hack ...
	# obj.obj2=FreeCAD.ActiveDocument.Box
	_Mover(obj)
	_ViewProviderMover(obj.ViewObject)
	return obj

class _CommandMover:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/mover.png', 'MenuText': 'Mover', 'ToolTip': 'Mover Dialog'} 


	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Mover")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createMover()")
			say("I create a mover")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Mover(_Actor):


		
	def __init__(self,obj,motion=FreeCAD.Vector(100,0,0) ,start=10,end=20):
		self.obj=obj
		obj.Proxy = self
		self.Type = "_Mover"
#		obj.step=self.step
#		obj.reverse=self.reverse
#		self.obj.motionVector=motion


	def step(self,now):
		say("step XX")
		say(self)
		if not self.obj.obj2:
			errorDialog("kein mover objekt zugeordnet")
			raise Exception(' self.obj2 nicht definiert')

		if self.obj.obj2:
			if now<self.obj.start or now>self.obj.end:
				pass
			else:
				relativ=1.00/(self.obj.end-self.obj.start)
				v=FreeCAD.Vector(self.obj.motionVector).multiply(relativ)
				Draft.move(self.obj.obj2,v,copy=False)
		else:
			say("kein Moveobjekt ausgewaehlt")
			
	def reverse(self):
		self.obj.motionVector.multiply(-1)

	def execute(self,obj):
		say("execute  _Mover")
		say(self)
		say(obj)
		
		say("execute ..2 ")
		if hasattr(self,'obj2'):
			self.initPlace=	self.obj2.Placements
		# anzeigewert neu berechnen
		# obj.obj2ro=obj.obj2rw
		if hasattr(obj,'obj2'):
			say(obj.obj2)
		try:
			obj.obj2ro=obj.obj2.Label
		except:
			say("kein obj2")
			

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None





class _ViewProviderMover(object):
	"A View Provider for the Mover object"

 
	def getIcon(self):
		return '/home/microelly2/animation_wb/icons/mover.png'
   
	def __init__(self,vobj):
		vobj.Proxy = self


	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None



if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Mover',_CommandMover())
	
	
#-------------------------------------


def createRotator(name='My_Rotator'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","intervall","start").start=10
	obj.addProperty("App::PropertyInteger","end","intervall","end").end=40

	obj.addProperty("App::PropertyPlacement","initPlace","3D Param","initPlace")
	obj.addProperty("App::PropertyVector","rotationCentre","3D Param","Rotationszentrum")
	obj.addProperty("App::PropertyVector","rotationAxis","3D Param","Rotationsachse")
	obj.addProperty("App::PropertyFloat","angle","intervall","Dreh Winkel").angle=270
	obj.addProperty("App::PropertyLink","obj2","3D Param","rotating object ")
	obj.addProperty("App::PropertyString","obj2ro","3D Param","moving obj").obj2ro="undefined"
	obj.setEditorMode("obj2ro", 1)

	_Rotator(obj)
	_ViewProviderRotator(obj.ViewObject)
	return obj

class _CommandRotator:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/rotator.png', 'MenuText': 'Rotator', 'ToolTip': 'Rotator Dialog'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Rotator")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createRotator()")
			say("I create a rotator")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Rotator:

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "_Rotator"
		self.obj2=obj
		
	def execute(self,obj):
		say("execute _Rotator")
		if hasattr(obj,'obj2'):
			say(obj.obj2)
		try:
			obj.obj2ro=obj.obj2.Label
		except:
			say("kein obj2")
			

		#self.positionVector=position
		#self.axisVector=axis
		#self.angle=angle



	def stepx(self,now):
		say("difgfdgd2rn")
		say(now)
		say("-----ffffff----------")
		say(self.obj2.start)
		say(self.end)
		say("ende")


	def step(self,now):
		say("di2rn")
		say(now)
		say(self.obj2.start)

		say("---------------")
		if now<self.obj2.start or now>self.obj2.end:
			say("ausserhalb")
			pass
		else:
			say(self.obj2.end-self.obj2.start)
			relativ=1.00/(self.obj2.end-self.obj2.start)
			say(relativ)
			angle2=self.obj2.angle*relativ
			say(angle2)
			say(self.obj2.rotationAxis)
			try:
				pass
				Draft.rotate([self.obj2.obj2],angle2,self.obj2.rotationCentre,axis=self.obj2.rotationAxis,copy=False)
			except:
				say("Fehler warum ...")
			finally:
				say("fertig")
		say("ende")

	def  setRot(self,dwireName):
		import math
		obj=self.getObject(dwireName)
#		t=App.ActiveDocument.DWire002
		t=obj
		a=t.Shape.Vertexes[0]
		b=t.Shape.Vertexes[1]
		c=t.Shape.Vertexes[2]
		v1=FreeCAD.Vector(a.X,a.Y,a.Z).sub(FreeCAD.Vector(b.X,b.Y,b.Z))
		
		v2=FreeCAD.Vector(c.X,c.Y,c.Z).sub(FreeCAD.Vector(b.X,b.Y,b.Z))
		
		print v1
		axis=v1.cross(v2)
		print axis
		
		
		print v1
		
		dot=v1.dot(v2)
		print dot
		
		cosAngle=dot/(v1.Length *v2.Length)
		
		print cosAngle
		angle=math.acos(cosAngle)/math.pi *180
		
		print angle
		self.axisVector=axis
		self.angle=angle
		self.positionVector=FreeCAD.Vector(b.X,b.Y,b.Z)
	def reverse(self):
		self.angle =- self.angle
	def reverse2(self):
		self.angle =  self.angle - 180
	def reverse3(self):
		self.angle =   self.angle -180




class _ViewProviderRotator(object):
	"A View Provider for the Mover object"

	def getIcon(self):
		return '/home/microelly2/animation_wb/icons/rotator.png'
   
	def __init__(self,vobj):
		vobj.Proxy = self

	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None


if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Rotator',_CommandRotator())

#---------------------------------------------------------------

	
#-------------------------------------


	
#-------------------------------------


def createPlugger(name='My_Plugger'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyLink","pin","3D Param","pin")
	obj.addProperty("App::PropertyLink","obj","3D Param","objekt")
	obj.addProperty("App::PropertyInteger","ix","nummer","index 1").ix=3
	obj.addProperty("App::PropertyEnumeration","detail","format","art").detail=["Placement.Base","Vertex.Point","unklarmp"]



	_Plugger(obj)
	_ViewProviderPlugger(obj.ViewObject)
	return obj

class _CommandPlugger:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/plugger.png', 'MenuText': 'Plugger', 'ToolTip': 'Plugger Dialog'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Plugger")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createPlugger()")
			say("I create a Plugger")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   


class _Plugger(_Actor):
	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Plugger"

		self.obj2 = obj 
		#super(type(self), self).__init__(obname,start,end)
#		obj.pin=FreeCAD.ActiveDocument.Box
#		obj.obj=FreeCAD.ActiveDocument.Cylinder
#		obj.detail="Placement.Base"

	def step(self,now):
		say("step--------------------")
		if not self.obj2.obj:
			errorDialog("kein ziel zugeordnet")
			raise Exception(' self.obj2.obj nicht definiert')
		if not self.obj2.pin:
			errorDialog("kein pin zugeordnet")
			raise Exception(' self.obj2.pin nicht definiert')
		say(self.obj2.ix)
		say(self.obj2.detail)

		if self.obj2.detail=="Placement.Base":
			say("Base")
			self.obj2.obj.Placement.Base=self.obj2.pin.Placement.Base
		elif self.obj2.detail=="Vertex.Point":
			say("tuwas")
			say(self.obj2.ix)
			say(self.obj2.pin.Shape.Vertexes[self.obj2.ix].Point)
			self.obj2.obj.Placement.Base=self.obj2.pin.Shape.Vertexes[self.obj2.ix].Point
		else:
			say("schl,echt")
			# raise Exception("unknown detail")
		#say("tuwas")
		#say(self.obj2.ix)
		#say(self.obj2.pin.Shape.Vertexes[self.obj2.ix].Point)
		#self.obj2.obj.Placement.Base=self.obj2.pin.Shape.Vertexes[self.obj2.ix].Point

	def setDetail(self,detailname,param1):
			self.obj2.detail=detailname
			self.obj2.param1=param1
	
	def execute(self,obj):
		say("execute _Plugger")

class _ViewProviderPlugger(object):
	"A View Provider for the Mover object"

	def getIcon(self):
		return '/home/microelly2/animation_wb/icons/plugger.png'
   
	def __init__(self,vobj):
		vobj.Proxy = self

	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None


if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Plugger',_CommandPlugger())

#---------------------------------------------------------------


	
#-------------------------------------


def createTranquillizer(name='My_Tranquillizer'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyFloat","time","params","time").time=0.02
	_Tranquillizer(obj)
	_ViewProviderTranquillizer(obj.ViewObject)
	return obj

class _CommandTranquillizer:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/tranq.png', 'MenuText': 'Tranquillizer', 'ToolTip': 'Tranquillizer Dialog'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Tranquillizer")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createTranquillizer()")
			say("I create a Tranquillizer")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return

import time
from time import sleep
	   
class _Tranquillizer:

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Tranquillizer"
		self.obj2 = obj 

	def execute(self,obj):
		say("execute _Tranquillizer")

	def step(self,now):
		say(self)
		FreeCAD.tt=self
		time.sleep(self.obj2.time)
	def  toInitialPlacement(self):
		pass
	
	
###############


class _ViewProviderTranquillizer(object):
	"A View Provider for the Mover object"

	def getIcon(self):
		return '/home/microelly2/animation_wb/icons/tranq.png'

	def __init__(self,vobj):
		vobj.Proxy = self


	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None


if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Tranquillizer',_CommandTranquillizer())

#---------------------------------------------------------------

	
#-------------------------------------


def createAdjuster(name='My_Adjuster'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","intervall","start").start=10
	obj.addProperty("App::PropertyInteger","end","intervall","end").end=40
	obj.addProperty("App::PropertyFloat","va","intervall","va").va=0
	obj.addProperty("App::PropertyFloat","ve","intervall","ve").ve=40
	obj.addProperty("App::PropertyLink","obj","3D Param","Sketch")
	obj.addProperty("App::PropertyInteger","nr","intervall","nummer Datum").nr=1


	obj.addProperty("App::PropertyString","unit","3D Param","einheit").unit=""

	_Adjuster(obj)
	_ViewProviderMover(obj.ViewObject)
	return obj

class _CommandAdjuster:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/adjuster.png', 'MenuText': 'Adjuster', 'ToolTip': 'Adjuster Dialog'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Adjuster")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createAdjuster()")
			say("I create a Adjuster")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Adjuster(_Actor):
	
	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Adjuster"
		self.obj2 = obj 

		
	def step(self,now):
		say("stepsdfdf!")

		if not self.obj2.obj:
			errorDialog("kein Sketch zugeordnet")
			raise Exception(' self.obj2.obj nicht definiert')
 
		FreeCADGui.ActiveDocument.setEdit(self.obj2.obj.Name)
		#say(self.ve)
		#say(self.va)
		if 1:
			v=self.obj2.va +  (self.obj2.ve - self.obj2.va)*(now-self.obj2.start)/(self.obj2.end-self.obj2.start)
			say(v)
		try:
			say("intern")	
			self.obj2.obj.setDatum(self.obj2.nr,FreeCAD.Units.Quantity(v))
			
		except:
			 say("ffehler") 
		say("sett")
		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.ActiveDocument.resetEdit()
		#FreeCADGui.updateGui() 

	def setValues(self,va,ve):
		self.obj2.va=va
		self.obj2.ve=ve



	def execute(self,obj):
		say("execute _Adjuster")




class _ViewProviderAdjuster(object):
	"A View Provider for the Mover object"

 
	def getIcon(self):
		return '/home/microelly2/animation_wb/icons/adjuster.png'

	def __init__(self,vobj):
		vobj.Proxy = self


	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None


if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Adjuster',_CommandAdjuster())

#---------------------------------------------------------------


	
#-------------------------------------


def createPhotographer(name='My_Photographer'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","intervall","start").start=10
	obj.addProperty("App::PropertyInteger","end","intervall","end").end=40
	obj.addProperty("App::PropertyInteger","size_x","format","start").size_x=480
	obj.addProperty("App::PropertyInteger","size_y","format","end").size_y=640
	obj.addProperty("App::PropertyPath","fn","zzz","outdir").fn="/tmp/fc_anim_"
	obj.addProperty("App::PropertyEnumeration","format","format","Bildformat").format=["png","jpg","bmp"]
	_Photographer(obj)
	_ViewProviderPhotographer(obj.ViewObject)
	return obj

class _CommandPhotographer:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/photographer.png', 'MenuText': 'Photographer', 'ToolTip': 'Photographer Dialog'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Photographer")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createPhotographer()")
			say("I create a Photographer")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Photographer(_Actor):

	def __init__(self,obj):
		self.obj2 = obj 
		obj.Proxy = self
		self.Type = "Photographer"

	def execute(self,obj):
		say("execute _Photographer")

	def step(self,now):
		if now<self.obj2.start or now>self.obj2.end:
			pass
		else:
			FreeCADGui.Selection.clearSelection()
			FreeCADGui.updateGui() 
			say("view")
			FreeCADGui.activeDocument().activeView().viewAxometric()
			kf= "%04.f"%now
			fn=self.obj2.fn+kf+'.png'
			fn=self.obj2.fn+kf+'.'+self.obj2.format 
			FreeCADGui.activeDocument().activeView().saveImage(fn,self.obj2.size_x,self.obj2.size_y,'Current')
	def  toInitialPlacement(self):
		pass


class _ViewProviderPhotographer(object):
	"A View Provider for the Mover object"

	
	def getIcon(self):
		return '/home/microelly2/animation_wb/icons/photographer.png'
   
	def __init__(self,vobj):
		vobj.Proxy = self

	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None

	def __init__(self,vobj):
		vobj.Proxy = self

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Photographer',_CommandPhotographer())

#---------------------------------------------------------------



	
#-------------------------------------


def createManager(name='My_Manager'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","intervall","params",
						"intervall")

	obj.addProperty("App::PropertyPythonObject","run","zzz",						"run")
	obj.addProperty("App::PropertyLinkList","targets","zzz",						"targets")
	obj.addProperty("App::PropertyString","text","params",						"text")
	_Manager(obj)
	_ViewProviderManager(obj.ViewObject)
	return obj

class _CommandManager:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/manager.png', 'MenuText': 'Manager', 'ToolTip': 'Manager Dialog'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Manager")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createManager()")
			say("I create a Manager")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Manager:

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "_Manager"
#		obj.targets=[]
#		obj.targets=[FreeCAD.ActiveDocument.Box]
#		obj.fn=''
#		obj.text='ausgabe erfolgt hier'
#		obj.intervall=20
#		obj.run=self.run
		self.obj2=obj



	def execute(self,obj):
		say("execute _Manager")
		#obj.run=self.run
		


	def register(self,obj):
		self.obj2.targets.append(obj)

	
	def runORIG(self,intervall):
		say("run " +str(intervall))
		for nw in range(intervall):	
			say("loop---");
			say(self)
		#	say(self.Name)
			if hasattr(self,'obj2'):
					t=FreeCAD.ActiveDocument.getObject(self.obj2.Name)
			
			
			say(nw)
			for ob in t.OutList:
					say(ob.Label)
					#try:
					say("step")
					ob.step(nw)
					#except:
					#say("fehler step")
					#	raise Exception(ob)
			try:
				pass
				#Draft.move(helper,sk,copy=False)
				FreeCADGui.Selection.clearSelection()
				FreeCADGui.updateGui() 
	#			self.genOutput(nw)
	###			self.showTime(nw)
			except:
				say ("schiefgegangen")

	def run(self,intervall):
		say("run " +str(intervall))
		for nw in range(intervall):	
			say("loop--" + str(nw));
			say(self)
		#	say(self.Name)
			if hasattr(self,'obj2'):
				t=FreeCAD.ActiveDocument.getObject(self.obj2.Name)
			else:
				raise Exception("obj2 not found --> reinit the file!")
			for ob in t.OutList:
					say(ob.Label)
					try:
						say("step xx")
						say(ob)
						say(ob.Proxy)
						say(ob.Proxy.step)
						ob.Proxy.step(nw)
					except:
						say("fehler step 2")
						raise Exception("step nicht ausfuerbar")
			try:
				pass
				#Draft.move(helper,sk,copy=False)
				FreeCADGui.Selection.clearSelection()
				FreeCADGui.updateGui() 
	#			self.genOutput(nw)
	###			self.showTime(nw)
			except:
				say ("schiefgegangen")


	def setShowTime(self,texter):
		self.obj.text=texter


	def showTime(self,nw1):
		if self.obj.text:
			kf= "%04.f"%nw1
			self.obj.text.LabelText = [unicode(str(kf), 'utf-8'),]

	def finalize(self,wait=5):
			for obj in self.obj.targets:
				obj.toInitialPlacement()
				FreeCADGui.updateGui() 
			time.sleep(wait)









class _ViewProviderManager(object):
	"A View Provider for the Mover object"

	
	def getIcon(self):
		return '/home/microelly2/animation_wb/icons/manager.png'
   
	def __init__(self,vobj):
		vobj.Proxy = self


	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None



if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Manager',_CommandManager())

#---------------------------------------------------------------




class _Starter:
	
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/icon1.svg', 'MenuText': 'Starte', 'ToolTip': 'Initialisier nach Dateiladen '} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		for ob in FreeCAD.ActiveDocument.Objects:
			if hasattr(ob,'Proxy'):
				ob.Proxy.__init__(ob)
				# ob.Proxy.obj2=ob
				print("init " +ob.Name)


if FreeCAD.GuiUp:
	FreeCADGui.addCommand('A_Starter',_Starter())

	

class _Runner:
	
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/animation.png', 'MenuText': 'Run Manager', 'ToolTip': 'Manager Run'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		try:
			pass
			# FreeCAD.getDocument("z7").getObject("My_Manager").Proxy.run(100)
		except:
			pass
		M = FreeCADGui.Selection.getSelectionEx()
		say(M)
		if len(M)==0:
			errorDialog("Manager auswahlen")
		elif M[0].Object.Proxy.Type <> '_Manager':
			errorDialog("Manager auswahlen")
		else:
			tt=M[0].Object
			say(tt)
			tt.Proxy.run(100)




if FreeCAD.GuiUp:
	FreeCADGui.addCommand('A_Runner',_Runner())

# fast Helpers
# define  Activated !!
	
class _B1:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/icon1.svg', 'MenuText': 'B1', 'ToolTip': 'B1'} 
	def IsActive(self):
		return True
	def Activated(self):
		say("runngi _B1")
		say(self)

class _B2:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/icon2.svg', 'MenuText': 'B2', 'ToolTip': 'B2'} 
	def IsActive(self):
		return True
	def Activated(self):
		say("runngi _B2")

class _B3:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/icon3.svg', 'MenuText': 'B3', 'ToolTip': 'B3'} 
	def IsActive(self):
		return True
	def Activated(self):
		say("runngi _B3")


if FreeCAD.GuiUp:
	FreeCADGui.addCommand('B1',_B1())
	FreeCADGui.addCommand('B2',_B2())
	FreeCADGui.addCommand('B3',_B3())





