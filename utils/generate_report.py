from contextvars import Context
import bpy
from mathutils import Vector
from .bmesh_from_object_transformed import bmesh_from_object_transformed

v_unit_scale = Vector((1.0, 1.0, 1.0))


def generate_report(method: bpy.types.EnumProperty, context: 'Context'):
    SETTINGS: bpy.types.UnitSettings = bpy.context.scene.unit_settings
    SYSTEM: str | int = SETTINGS.system
    LENGTH: str | int = SETTINGS.length_unit
    SCALE: float = SETTINGS.scale_length

    F1: float = bpy.utils.units.to_value(SYSTEM, 'LENGTH', '1') * SCALE
    F2: float = F1 * F1
    F3: float = F2 * F1

    o: bpy.types.Object = bpy.context.active_object

    with bmesh_from_object_transformed(bpy.context.active_object) as bm:
        area: float = sum(face.calc_area() for face in bm.faces)
        if method == 'FULL':
            volume: float = bm.calc_volume()
        if method == 'WALLED':
            volume: float = area * context.scene.metrics_wall_thickness

    mass = float(context.scene.metrics_density) * volume

    def format_length(x: float) -> str:
        return bpy.utils.units.to_string('METRIC', 'LENGTH', x * F1, precision=4)

    def format_area(x: float) -> str:
        return bpy.utils.units.to_string('METRIC', 'AREA', x * F2, precision=4)

    def format_volume(x: float) -> str:
        return bpy.utils.units.to_string('METRIC', 'VOLUME', x * F3, precision=4)

    def format_mass(x: float) -> str:
        return bpy.utils.units.to_string('METRIC', 'MASS', x * F3, precision=4)

    report = [
        f"Object: {o.name}",
        f"Method: {method.title()}",
        f"Wall Thickness: {format_length(context.scene.metrics_wall_thickness)}" if method == 'WALLED' else None,
        f"Dimensions:",
        f"    X: {format_length(o.dimensions.x)}",
        f"    Y: {format_length(o.dimensions.y)}",
        f"    Z: {format_length(o.dimensions.z)}",
        f"Area: {format_area(area)}",
        f"Volume: {format_volume(volume)}",
        f"Weight: {format_mass(mass)}",
    ]
    
    return "\n".join([l for l in report if l])
