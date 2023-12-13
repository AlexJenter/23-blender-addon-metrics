import bpy
import bmesh
from contextlib import contextmanager


@contextmanager
def bmesh_from_object_transformed(object: bpy.types.Object):
    """Creates a new bmesh from a blender object, applies its world matrix and subsequently frees the memory"""
    bm: bmesh.types.BMesh = bmesh.new()
    try:
        bm.from_mesh(object.data)
        matrix = object.matrix_world
        bmesh.ops.transform(bm, matrix=matrix, verts=bm.verts)
        yield bm
    finally:
        bm.free()
