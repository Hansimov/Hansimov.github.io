"""
Jump Select

(Original name: Select Loop)

MIT License
Copyright 2019 Christopher Montesano

Modified by Hansimov, 2020.03
"""

import c4d
from c4d.utils import Neighbor
from c4d import gui

def get_opposite_edge(poly, p1, p2):
    if (p1 == p2) or (poly.c == poly.d):
        return None

    points = (p1, p2)
    poly_abcd = [poly.a, poly.b, poly.c, poly.d]
    poly_oppo = []

    for ele in poly_abcd:
        if ele not in points:
            poly_oppo.append(ele)

    if poly_oppo != []:
        return poly_oppo[:2]
    else:
        return None

def get_shared_points(poly1, poly2):
    shared_points = set()
    for pta in (poly1.a, poly1.b, poly1.c, poly1.d):
        for ptb in (poly2.a, poly2.b, poly2.c, poly2.d):
            if pta == ptb:
                shared_points.add(pta)
    return list(shared_points)

def select_poly_loop(obj, sim=False):
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
        raise ValueError("Must select if and only if 2 Polygons!")

    nth = int(gui.InputDialog("Set nth (int) of polys:", "2"))

    offsets = get_offsets(nth)

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
        raise ValueError("Selected polygons must share an edge!")

    n = Neighbor()
    n.Init(obj)

    for poly_index in range(2):
        this_poly_index = selected_ids[poly_index]
        pt1 = shared_points[0]
        pt2 = shared_points[1]

        for i in range(cply):
            try:
                nply = n.GetNeighbor(pt1, pt2, this_poly_index)
            # This IndexError happens on `plane` object polygons
            except IndexError as err:
                gui.MessageDialog("IndexError of GetNeighbor!")
                break

            if nply in [None,-1]:
                break

            this_poly_index = nply
            bsel.Select(nply)
            if not i%nth in offsets:
                bsel.Toggle(nply)
            opposite_edge = get_opposite_edge(plys[this_poly_index], pt1, pt2)
            if opposite_edge is None:
                break
            pt1, pt2 = opposite_edge
            if pt1 == shared_points[0] and pt2 == shared_points[1]:
                break

    obj.Message(c4d.MSG_CHANGE)
    c4d.EventAdd()

def select_spline_point_loop(op):
    sel = op.GetPointS()
    sel.DeselectAll()
    cnt = op.GetPointCount()
    nth = int(gui.InputDialog("Set nth (int) of points:", "2"))
    offsets = get_offsets(nth)
    for i in range(cnt):
        if i%nth in offsets: sel.Select(i)
    c4d.EventAdd()

def get_offsets(nth):
    if nth == 1:
        return [0]
    offset_list = gui.InputDialog("Set offsets (int, 0-{}), use space to split several offsets".format(nth-1), "1")
    offset_list = offset_list.split()
    offsets = []
    for offset in offset_list:
        offsets.append(min(int(offset),nth-1))
    return offsets

def main():
    op = doc.GetActiveObject()
    if not op:
        gui.MessageDialog("No active object!", c4d.GEMB_ICONSTOP)
        return False
    if type(op) == c4d.PolygonObject:
        try:
            select_poly_loop(op)
        except ValueError as err:
            gui.MessageDialog(str(err), c4d.GEMB_ICONSTOP)
    elif type(op) == c4d.SplineObject:
        try:
            select_spline_point_loop(op)
        except ValueError as err:
            gui.MessageDialog(str(err), c4d.GEMB_ICONSTOP)
    else:
        return False

if __name__=='__main__':
    main()