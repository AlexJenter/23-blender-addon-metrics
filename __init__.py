import bpy
import csv
import os
from .operators.apply_scale import MTRX_OT_apply_scale
from .operators.copy_to_clipboard import MTRX_OT_copy_to_clipboard
from .operators.set_units_to_mm import MTRX_OT_set_units_to_mm
from .panels.sidebar import MTRX_PT_sidebar
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


classes = [
    MTRX_OT_apply_scale,
    MTRX_OT_copy_to_clipboard,
    MTRX_OT_set_units_to_mm,
    MTRX_PT_sidebar,
]


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
