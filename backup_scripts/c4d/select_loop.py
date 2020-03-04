"""
MIT License
Copyright 2019 Christopher Montesano
"""

import c4d
from c4d.utils import Neighbor
from c4d import gui

def get_opposite_edge(poly, p1, p2):

    if (p1 == p2):
        return None

    if (poly.c == poly.d):  # triangle
        return None

    points = (p1, p2)

    if poly.a in points and poly.b in points:
        return poly.c, poly.d

    if poly.b in points and poly.c in points:
        return poly.a, poly.d

    if poly.c in points and poly.d in points:
        return poly.a, poly.b

    if poly.d in points and poly.a in points:
        return poly.b, poly.c

    return None


def get_shared_points(poly1, poly2):
    shared_points = set()
    for pta in (poly1.a, poly1.b, poly1.c, poly1.d):
        for ptb in  (poly2.a, poly2.b, poly2.c, poly2.d):
            if pta == ptb:
                shared_points.add(pta)
    return list(shared_points)


def select_poly_loop(obj, nth=1, sim=False):
    if obj is None:
        raise ValueError("No object selected")

    if not isinstance(obj, c4d.PolygonObject):
        raise ValueError("Not a polygon object")

    cply = obj.GetPolygonCount()
    cpnt = obj.GetPointCount()
    bsel = obj.GetPolygonS()

    if cply == 0:
        raise ValueError("No polygons found")
    if bsel.GetCount() != 2:
        raise ValueError("Exactly two polygons must be selected")

    plys = obj.GetAllPolygons()

    selected_ids = []
    for index, selected in enumerate(bsel.GetAll(cply)):
        if not selected:
            continue
        selected_ids.append(index)

    assert(len(selected_ids) == 2)

    poly1 = plys[selected_ids[0]]
    poly2 = plys[selected_ids[1]]

    shared_points = get_shared_points(poly1, poly2)
    if len(shared_points) != 2:
        raise ValueError("Selected polygons must share an edge")

    n = Neighbor()
    n.Init(obj)

    for poly_index in range(2):
        this_poly_index = selected_ids[poly_index]
        pt1 = shared_points[0]
        pt2 = shared_points[1]

        for i in range(cply):
            nply = n.GetNeighbor(pt1, pt2, this_poly_index)
            if nply is None:
                break
            this_poly_index = nply
            bsel.Select(nply)
            if i % nth != 0:
                bsel.Toggle(nply)
            opposite_edge = get_opposite_edge(plys[this_poly_index], pt1, pt2)
            if opposite_edge is None:
                break
            pt1, pt2 = opposite_edge
            if pt1 == shared_points[0] and pt2 == shared_points[1]:
                break

    obj.Message(c4d.MSG_CHANGE)
    c4d.EventAdd()

def select_spline_point_loop(op,nth):
    sel = op.GetPointS()
    sel.DeselectAll()

    # Set the index of first selected point 
    offset = int(gui.InputDialog("Set offset (0-{}) (int)".format(nth-1), "0"))
    cnt = op.GetPointCount()
    for i in range(cnt):
        if i%nth == offset: sel.Select(i)
    c4d.EventAdd() #Update the scene

def main():
    op = doc.GetActiveObject()
    if not op: 
        #gui.MessageDialog("No object active!")
        return False
    
    nth = int(gui.InputDialog("Set every nth polygon:", "2"))

    # Check whether the object is spline type
    if type(op) != c4d.Ospline:
        select_spline_point_loop(op,nth)
    else:
        try:
            select_poly_loop(op, nth)
        except ValueError as err:
            gui.MessageDialog(str(err))

if __name__=='__main__':
    main()