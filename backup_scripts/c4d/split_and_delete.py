"""
Name-US: split and delete
Description-US: split and delete polygons
"""
import c4d

def main():
    c4d.CallCommand(14046, 0) # Split
    c4d.CallCommand(12109, 0) # Delete
    doc.SetActiveObject(doc.GetActiveObject().GetNext())

if __name__=='__main__':
    main()