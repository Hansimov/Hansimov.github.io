"""
HB_SelectionToCircle V1.1

Last Modified: 1/1/2016
Works with CINEMA 4D R16.050 and up.
Copyright: Holger Biebrach, www.c4dstuff.com

Name-US: HB_Selection_To_Circle
Description-US: Makes current Selection Spherical/Radial

Select Points or Polygons and run the Script. The selection will be made Spherical.

Video Tutorial:
https://youtu.be/kQpLqrtGfBQ?t=21s

Name-DE: HB_SelectionToCircle
Description-DE: Macht Selektion Spherisch/Kreisförmig

ChangeLog:
1/1/2016 v1.0 Release Version

11/22/2016 v1.1 
-Fixed issue where selection was scaled down

"""

import c4d
from c4d import gui, documents, plugins, utils


def deletetags(obj): # Scan Tags on Object
    
    n       = 1 
    
    tags    = obj.GetTags()

    for tag in tags:
        if not tag: continue
        tagtype = tag.GetType()
   
        
        if tag.GetName()=="tempsel":
            doc.AddUndo(c4d.UNDOTYPE_DELETE, tag)
            tag.Remove()
            c4d.EventAdd()


def GetModelingAxis(op):
    sel = op.GetPointS()
    points = [(i, point)
          for i, point in enumerate(op.GetAllPoints())
          if sel.IsSelected(i)]

    if not points:
      return

    average = sum(point[1] for point in points) / float(len(points))
    return average

def GetSelectionSize(op):


    sel = op.GetPointS()
    points = [(i, point)
          for i, point in enumerate(op.GetAllPoints())
          if sel.IsSelected(i)]

    if not points:
      return

    selsizeminX = min(point[1].x for point in points)
    selsizemaxX = max(point[1].x for point in points)
    selsizeminY = min(point[1].y for point in points)
    selsizemaxY = max(point[1].y for point in points)
    selsizeminZ = min(point[1].z for point in points)
    selsizemaxZ = max(point[1].z for point in points)

    boundbox= c4d.Vector(selsizemaxX,selsizemaxY,selsizemaxZ)-c4d.Vector(selsizeminX,selsizeminY,selsizeminZ)
    selsize=boundbox.GetLength()
    return selsize

def RemoveChildren(objlist):
    
    for obj in objlist:
        doc.AddUndo(c4d.UNDOTYPE_DELETE, obj)
        obj.Remove()
        
        
    
    c4d.EventAdd()    
    return

def InsertChildren(objlist,root):
    
    
    for obj in objlist:
        
        obj.InsertUnder(root)
        doc.AddUndo(c4d.UNDOTYPE_NEW, obj)
        
        
    c4d.EventAdd()    
    return


def main():
    
    doc.StartUndo()
    
    selobj=doc.GetSelection()
    
    if len(selobj)>1 or len(selobj)==0 : #ERROR
        
        gui.MessageDialog("Select one Object!")
        return

    bc = c4d.BaseContainer()
    c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc) #Modifier Key pressed?
    
    if bc[c4d.BFM_INPUT_QUALIFIER] ==2:
       CTRL=True
       if len(selobj)==2:
           gui.MessageDialog("Select one Object!")
           return     
    else:
        CTRL=False




    mode=doc.GetMode()


    obj=selobj[0]
    objChildren = obj.GetChildren()
    if doc.GetMode()==7: # is Polymode active? Run selction Command

        c4d.utils.SendModelingCommand(command = c4d.MCOMMAND_SELECTPOLYTOPOINT,
                                    list = [obj],
                                    mode = c4d.MODELINGCOMMANDMODE_POLYGONSELECTION,
                                    bc = c4d.BaseContainer(),
                                    doc = doc)
                                    
    if doc.GetMode()==6: # is EdgeMode active? Run selction Command
 
        ConvertSettings = c4d.BaseContainer() 
 
        ConvertSettings[c4d.MDATA_CONVERTSELECTION_LEFT]=1
        ConvertSettings[c4d.MDATA_CONVERTSELECTION_RIGHT]=0    

        c4d.utils.SendModelingCommand(command = c4d.MCOMMAND_CONVERTSELECTION,
                                    list = [obj],
                                    mode = c4d.MODELINGCOMMANDMODE_EDGESELECTION,
                                    bc = ConvertSettings,
                                    doc = doc)

    doc.SetMode(5)#pointmode

    ObjPos=obj.GetMg()

    selAxisPos= GetModelingAxis(obj)
    
    newm    = obj.GetMg()

    newm.off = selAxisPos
       
    selsize = GetSelectionSize(obj)
    
    SphereDeformer=c4d.BaseObject(1001003)
    SphereDeformer[c4d.SPHERIFYOBJECT_STRENGTH]=1
    SphereDeformer[c4d.SPHERIFYOBJECT_RADIUS]= selsize/2
    
    
    SphereDeformer.SetMg(newm)
    c4d.CallCommand(12552) # Set Selection
    newseltag=doc.GetActiveTag()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL,newseltag)
    newseltag.SetName("tempsel")
    restag = c4d.BaseTag(5683)
    restag[c4d.RESTRICTIONTAG_NAME_01]="tempsel"
    SphereDeformer.InsertTag(restag)
    doc.AddUndo(c4d.UNDOTYPE_NEW, restag)
    
    SphereDeformer.InsertUnder(obj)
    doc.AddUndo(c4d.UNDOTYPE_NEW, SphereDeformer)
    
    CSsettings = c4d.BaseContainer()                 
    NewObj=utils.SendModelingCommand(command = c4d.MCOMMAND_CURRENTSTATETOOBJECT,
                                    list = [obj],
                                    mode = c4d.MODELINGCOMMANDMODE_EDGESELECTION,
                                    bc = CSsettings,
                                    doc = doc,
                                    )
       
    if NewObj[0].GetType()==c4d.Onull:
        NewObjChild=NewObj[0].GetDown()
    else:
        NewObjChild=NewObj[0]
        
        
    NewObjChild.InsertAfter(obj)
    doc.AddUndo(c4d.UNDOTYPE_NEW, NewObjChild)
    
    
    ObjChild=NewObj[0].GetDown()
    doc.AddUndo(c4d.UNDOTYPE_DELETE, ObjChild)
    ObjChild.Remove()
    doc.AddUndo(c4d.UNDOTYPE_DELETE, obj)
    obj.Remove()
    deletetags(NewObjChild)
    NewObjChildren=NewObjChild.GetChildren()
    
    RemoveChildren(NewObjChildren)
    InsertChildren(objChildren, NewObjChild)
    
    
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL,NewObjChild)
    NewObjChild.SetBit(c4d.BIT_ACTIVE)
    NewObjChild.SetMg(ObjPos)
    doc.SetMode(mode)#pointmode
    doc.EndUndo()
    c4d.EventAdd()
    

if __name__=='__main__':
    main()
