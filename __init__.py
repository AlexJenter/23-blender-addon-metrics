import csv
import bpy
import bmesh
from bpy.types import Panel
from bpy.types import Operator
from mathutils import Vector

bl_info = {
    "name": "Production Metrics",
    "description": "addon",
    "author": "Alex Jenter",
    "version": (0, 0, 1),
    "blender": (4, 1, 0),
    "location": "View3D",
    "warning": "",
    "support": "COMMUNITY",
    "doc_url": "",
    "category": "3D View"
}


v_unit_scale = Vector((1.0, 1.0, 1.0))


def generate_report(method, ctx):
    SETTINGS = bpy.context.scene.unit_settings
    SYSTEM = SETTINGS.system
    LENGTH = SETTINGS.length_unit
    SCALE = SETTINGS.scale_length

    F1 = bpy.utils.units.to_value(SYSTEM, 'LENGTH', '1') * SCALE
    F2 = F1 * F1
    F3 = F2 * F1

    o = bpy.context.active_object

    bm = bmesh.new()
    bm.from_mesh(o.data)

    area = sum(face.calc_area() for face in bm.faces)

    if method == 'FULL':
        volume = float(bm.calc_volume())
    else:
        volume = area * ctx.scene.metrics_wall_thickness

    bm.free()

    mass = float(ctx.scene.metrics_density) * volume

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
        f"Wall Thickness: {format_length(ctx.scene.metrics_wall_thickness)}" if method == 'WALLED' else None,
        f"Dimensions:",
        f"    X: {format_length(o.dimensions.x)}",
        f"    Y: {format_length(o.dimensions.y)}",
        f"    Z: {format_length(o.dimensions.z)}",
        f"Area: {format_area(area)}" if o.scale == v_unit_scale else None,
        f"Volume: {format_volume(volume)}" if o.scale == v_unit_scale else None,
        f"Weight: {format_mass(mass)}" if o.scale == v_unit_scale else None,
    ]


class MTRX_OT_apply_scale_operator(Operator):
    """Apply scale in order to calculate accurate surface area and volume"""
    bl_idname = "metrics.apply_scale"
    bl_label = "Apply object scale"
    bl_description = "Please apply Scale in order to get area an volume metrics"

    @classmethod
    def poll(self, context):
        return context.object.scale != Vector((1, 1, 1))

    def execute(self, context):
        bpy.ops.object.transform_apply(location=False,
                                       rotation=False,
                                       scale=True,
                                       properties=True,
                                       isolate_users=False)
        self.report({'INFO'}, f"Metrics: Object scale has been applied")
        return {'FINISHED'}


class MTRX_OT_copy_operator(Operator):
    """Copy report to system clipboard"""
    bl_idname = "metrics.copy_to_clipboard"
    bl_label = "Copy report"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        report = generate_report(
            context.scene.metrics_production_method, context)
        bpy.context.window_manager.clipboard = "\n".join(filter(None, report))
        self.report({'INFO'}, f"Metrics: Report has been copied to clipboard")
        return {'FINISHED'}


class MTRX_PT_sidebar(Panel):
    """Display Producion Metrics"""
    bl_label = "Production Metrics"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw(self, context):
        # col = self.layout.column(align=True)

        col = self.layout.column(align=True)
        col.prop(context.scene, "metrics_production_method")
        col.prop(context.scene, "metrics_density")

        if (context.scene.metrics_production_method == 'WALLED'):
            col = self.layout.column(align=True)
            col.prop(context.scene, "metrics_wall_thickness")

        box = self.layout.box()

        report = generate_report(
            context.scene.metrics_production_method, context)

        col = box.column(align=True)
        [col.label(text=line) for line in report if line]

        col = self.layout.column(align=False)

        col.operator(MTRX_OT_apply_scale_operator.bl_idname,
                     text=MTRX_OT_apply_scale_operator.bl_label,
                     icon='CON_SIZELIMIT')

        col.operator(MTRX_OT_copy_operator.bl_idname,
                     text=MTRX_OT_copy_operator.bl_label,
                     icon='COPYDOWN')


classes = [MTRX_OT_copy_operator,
           MTRX_OT_apply_scale_operator,
           MTRX_PT_sidebar, ]


# https://www.scheideanstalt.de/metallglossar/metallglossar/

with open('./density.csv', newline='') as csvfile:
    table_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    mat_items = []
    for row in list(table_reader)[1:]:

        name, short_name, density, melting_point, comment = row

        mat_items.append((density,
                          name,
                          f"[{short_name:<2}] {name}\nDichte: {density:>7}kg/m³\n\n{comment}"))

def register():
    [bpy.utils.register_class(c) for c in classes]

    bpy.types.Scene.metrics_density = bpy.props.EnumProperty(
        name='Density',
        description='A material and an associated specific weight',
        default=None,
        items=mat_items
    )

    bpy.types.Scene.metrics_production_method = bpy.props.EnumProperty(
        name='Type',
        description='Production method',
        default='FULL',
        items=[('FULL', 'Full', ''),
               ('WALLED', 'Walled', '')]
    )

    bpy.types.Scene.metrics_wall_thickness = bpy.props.FloatProperty(
        name='Wall Thickness',
        description='Multiplier for calculating Volume based on Area',
        subtype='DISTANCE',
        default=4.0,
        soft_min=2,
        soft_max=6,
        min=0,
        max=30
    )


def unregister():
    [bpy.utils.unregister_class(c) for c in classes]

    del bpy.types.Scene.metrics_density
    del bpy.types.Scene.metrics_production_method
    del bpy.types.Scene.metrics_wall_thickness


if __name__ == '__main__':
    register()
