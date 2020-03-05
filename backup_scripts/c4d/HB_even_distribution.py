"""
HB_EvenDistribution V1.0

Last Modified: 6/25/2015
Works with CINEMA 4D R16.050 and up.
Copyright: Holger Biebrach, www.c4dstuff.com

Name-US: HB_Even_Distribution
Description-US: Distributes Points along Edge selection evenly [CTRL: Input Influence Radius]

Video Tutorial:
https://youtu.be/Ki6I9sRdeUU?t=24m32s

Name-DE: HB_EvenDistribution
Description-DE: Verteilt Punkte gleichmäßig auf Kantenselektion[CTRL: Input Influence Radius]

ChangeLog:
6/11/2015 Release Version

"""

import c4d
from c4d import utils
from c4d import gui




def SetGlobalPosition(obj, pos):
    m = obj.GetMg()
    m.off = pos
    obj.SetMg(m)

def SetGlobalRotation(obj, rot):
    m = obj.GetMg()
    pos = m.off
    scale = c4d.Vector( m.v1.GetLength(),
                        m.v2.GetLength(),
                        m.v3.GetLength())

    m = utils.HPBToMatrix(rot)

    m.off = pos
    m.v1 = m.v1.GetNormalized() #* scale.x
    m.v2 = m.v2.GetNormalized() #* scale.y
    m.v3 = m.v3.GetNormalized() #* scale.z

    obj.SetMg(m)

def RemoveChildren(objlist):
    
    for obj in objlist:
        doc.AddUndo(c4d.UNDOTYPE_DELETE, obj)
        obj.Remove()
        
    
    c4d.EventAdd()    
    return

def InsertChildren(objlist,root):
    for obj in objlist:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        obj.InsertUnder(root)
        
    c4d.EventAdd()    
    return



def main():
    doc.StartUndo()
    obj=doc.GetActiveObject()
    objType=obj.GetType()
    ObjPos=obj.GetMg()
    ObjChildren = obj.GetChildren()
   
    RemoveChildren(ObjChildren)


    CTRL=False
    bc = c4d.BaseContainer()
    c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc)
       

    
    if bc[c4d.BFM_INPUT_QUALIFIER] ==2 :
        CTRL=True
        DeformerRadius = gui.InputDialog("Influence Radius")
        if not DeformerRadius: return
    
    
    
    settings = c4d.BaseContainer()                 # Settings Edge to Spline
    utils.SendModelingCommand(command = c4d.MCOMMAND_EDGE_TO_SPLINE,
                                list = [obj],
                                mode = c4d.MODELINGCOMMANDMODE_EDGESELECTION,
                                bc = settings,
                                doc = doc,
                                flags = c4d.MODELINGCOMMANDFLAGS_CREATEUNDO)
                                
               
    # Mospline
    OriginalSpline=obj.GetDown()

    SegmentCount=OriginalSpline.GetSegmentCount()
    PointCount=OriginalSpline.GetPointCount()/SegmentCount
  
    MoSpline=c4d.BaseObject(440000054)
    MoSpline[c4d.MGMOSPLINEOBJECT_MODE]=1
    MoSpline[c4d.MGMOSPLINEOBJECT_SOURCE_SPLINE]=OriginalSpline
    MoSpline[c4d.MGMOSPLINEOBJECT_SPLINE_MODE]=2
    MoSpline[c4d.MGMOSPLINEOBJECT_SPLINE_COUNT]=PointCount*10
    doc.AddUndo(c4d.UNDOTYPE_NEW, MoSpline)
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, MoSpline)  
    MoSpline.InsertBefore(OriginalSpline)
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, MoSpline)
    
    SetGlobalRotation(MoSpline,c4d.Vector(0,0,0))
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, MoSpline)
    SetGlobalPosition(MoSpline,c4d.Vector(0,0,0))
    

    # SplineDeformer
    SplineDeformer=c4d.BaseObject(1008982)
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, SplineDeformer)
    SplineDeformer[c4d.SPLINEDEFORMEROBJECT_RADIUS]=0.001
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, SplineDeformer)
    SplineDeformer[c4d.SPLINEDEFORMEROBJECT_USE_LENGTH]=False
    
    
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, SplineDeformer)
    SplineDeformer[c4d.SPLINEDEFORMEROBJECT_ORIGINAL_SPLINE]=OriginalSpline
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, SplineDeformer)
    SplineDeformer[c4d.SPLINEDEFORMEROBJECT_MODIFY_SPLINE]=MoSpline
    
    
    SplineDeformer.InsertAfter(OriginalSpline)
    doc.AddUndo(c4d.UNDOTYPE_NEW, SplineDeformer)
    
    
    if CTRL == True: 
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, SplineDeformer)
        SplineDeformer[c4d.SPLINEDEFORMEROBJECT_RADIUS]=float(DeformerRadius)
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, SplineDeformer)
        SplineDeformer[c4d.SPLINEDEFORMEROBJECT_USE_LENGTH]=False

        
    
    SplineDeformer.Message(c4d.MSG_DESCRIPTION_VALIDATE)
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, SplineDeformer)
    
    CSsettings = c4d.BaseContainer()                 
    NewObj=utils.SendModelingCommand(command = c4d.MCOMMAND_CURRENTSTATETOOBJECT,
                                list = [obj],
                                mode = c4d.MODELINGCOMMANDMODE_EDGESELECTION,
                                bc = CSsettings,
                                doc = doc,
                                )
   

    NewObj[0].InsertAfter(obj)
    doc.AddUndo(c4d.UNDOTYPE_NEW, NewObj[0])
    NewObj[0].SetMg(ObjPos)
   
    
    # New Root is a NULL Object
    if NewObj[0].GetType() == c4d.Onull:
        NewPolyObj=NewObj[0].GetDown()

        NewPolyObj.InsertAfter(obj)
        doc.AddUndo(c4d.UNDOTYPE_NEW, NewPolyObj)
        doc.AddUndo(c4d.UNDOTYPE_DELETE,NewObj[0])
        NewObj[0].Remove()
        doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, NewPolyObj)
        doc.SetSelection(NewPolyObj, c4d.SELECTION_ADD)

        InsertChildren(ObjChildren,NewPolyObj)
        NewPolyObj.SetMg(ObjPos)
        doc.AddUndo(c4d.UNDOTYPE_NEW, NewPolyObj)
        
    else:# New Root is a PolyObject
        
        NewObjChildren= NewObj[0].GetChildren()

        RemoveChildren(NewObjChildren)
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, NewObj[0])
        doc.SetSelection(NewObj[0], c4d.SELECTION_ADD)
  
        InsertChildren(ObjChildren,NewObj[0])
        NewObj[0].SetMg(ObjPos)
        doc.AddUndo(c4d.UNDOTYPE_NEW, NewObj[0])

    
    
    doc.AddUndo(c4d.UNDOTYPE_DELETE,obj)
    obj.Remove()
        
    
    c4d.EventAdd()
    doc.EndUndo()
    
    
if __name__=='__main__':
    main()
