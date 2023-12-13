import bpy
import bmesh
from contextlib import contextmanager


@contextmanager
def bmesh_from_object(object: bpy.types.Object):
    """Creates a new bmesh from a blender object and frees the memory after use"""
    bm: bmesh.types.BMesh = bmesh.new()
    try:
        bm.from_mesh(object.data)
        yield bm
    finally:
        bm.free()
