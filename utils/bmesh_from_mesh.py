import bmesh
from contextlib import contextmanager


@contextmanager
def bmesh_from_mesh(object):
    bm = bmesh.new()
    try:
        bm.from_mesh(object.data)
        yield bm
    finally:
        bm.free()
