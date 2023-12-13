import bpy
from mathutils import Vector
from ..utils.bmesh_from_mesh import bmesh_from_mesh

v_unit_scale = Vector((1.0, 1.0, 1.0))


def generate_report(method, context):
    SETTINGS = bpy.context.scene.unit_settings
    SYSTEM = SETTINGS.system
    LENGTH = SETTINGS.length_unit
    SCALE = SETTINGS.scale_length

    F1 = bpy.utils.units.to_value(SYSTEM, 'LENGTH', '1') * SCALE
    F2 = F1 * F1
    F3 = F2 * F1

    o = bpy.context.active_object

    with bmesh_from_mesh(bpy.context.active_object) as bm:
        area = sum(face.calc_area() for face in bm.faces)
        if method == 'FULL':
            volume = float(bm.calc_volume())
        if method == 'WALLED':
            volume = area * context.scene.metrics_wall_thickness

    mass = float(context.scene.metrics_density) * volume

    def format_length(x):
        return bpy.utils.units.to_string('METRIC', 'LENGTH', x * F1, precision=4)

    def format_area(x):
        return bpy.utils.units.to_string('METRIC', 'AREA', x * F2, precision=4)

    def format_volume(x):
        return bpy.utils.units.to_string('METRIC', 'VOLUME', x * F3, precision=4)

    def format_mass(x):
        return bpy.utils.units.to_string('METRIC', 'MASS', x * F3, precision=4)

    return [
        f"Object: {o.name}",
        f"Method: {method.title()}",
        f"Wall Thickness: {format_length(context.scene.metrics_wall_thickness)}" if method == 'WALLED' else None,
        f"Dimensions:",
        f"    X: {format_length(o.dimensions.x)}",
        f"    Y: {format_length(o.dimensions.y)}",
        f"    Z: {format_length(o.dimensions.z)}",
        f"Area: {format_area(area)}" if o.scale == v_unit_scale else None,
        f"Volume: {format_volume(volume)}" if o.scale == v_unit_scale else None,
        f"Weight: {format_mass(mass)}" if o.scale == v_unit_scale else None,
    ]
