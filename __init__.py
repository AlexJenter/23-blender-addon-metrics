from distutils import dir_util
import bpy
import csv
import bmesh
import os
from mathutils import Vector
from .operators.set_units_to_mm import MTRX_OT_set_units_to_mm
from .operators.apply_scale import MTRX_OT_apply_scale
from .utils.generate_report import generate_report

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


class MTRX_OT_copy_operator(bpy.types.Operator):
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


class MTRX_PT_sidebar(bpy.types.Panel):
    """Display Producion Metrics"""
    bl_label = "Production Metrics"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    @classmethod
    def poll(cls, context):

        return len(context.selectable_objects)

    def execute(self, context):
        pass

    def draw(self, context):
        col = self.layout.column(align=True)
        col.operator("metrics.setup_mm", icon="FIXED_SIZE")
        col.separator()
        col.prop(context.scene, "metrics_production_method")
        col.separator()
        col.prop(context.scene, "metrics_density")

        if (context.scene.metrics_production_method == 'WALLED'):
            col = self.layout.column(align=True)
            col.prop(context.scene, "metrics_wall_thickness")

        report = generate_report(
            context.scene.metrics_production_method, context)

        box = self.layout.box()
        col = box.column(align=True)
        [col.label(text=line) for line in report if line]

        col = self.layout.column(align=False)

        col.operator(MTRX_OT_apply_scale.bl_idname,
                     text=MTRX_OT_apply_scale.bl_label,
                     icon='CON_SIZELIMIT')

        col.operator(MTRX_OT_copy_operator.bl_idname,
                     text=MTRX_OT_copy_operator.bl_label,
                     icon='COPYDOWN')


classes = [MTRX_OT_set_units_to_mm,
           MTRX_OT_copy_operator,
           MTRX_OT_apply_scale,
           MTRX_PT_sidebar, ]


csv_path = os.path.join(os.path.dirname(__file__), "density.csv")
# https://www.scheideanstalt.de/metallglossar/metallglossar/
with open(csv_path, newline='') as csvfile:
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

    bpy.types.Scene.metrics_report = bpy.props.StringProperty(
        name='Report',
        description='Stores the Report as String',
        default=''
    )


def unregister():
    [bpy.utils.unregister_class(c) for c in classes]

    del bpy.types.Scene.metrics_density
    del bpy.types.Scene.metrics_production_method
    del bpy.types.Scene.metrics_wall_thickness


if __name__ == '__main__':
    register()
