import bpy
from contextvars import Context
from ..operators.apply_scale import MTRX_OT_apply_scale
from ..operators.copy_to_clipboard import MTRX_OT_copy_to_clipboard
from ..utils.generate_report import generate_report


class MTRX_PT_sidebar(bpy.types.Panel):
    """Display Producion Metrics"""
    bl_label = "Production Metrics"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    @classmethod
    def poll(cls, context: 'Context'):
        return context.active_object is not None

    def draw(self, context: 'Context'):
        col = self.layout.column(align=True)
        col.operator("metrics.setup_mm", icon="FIXED_SIZE")
        col.separator()
        col.prop(context.scene, "metrics_production_method")
        col.separator()
        col.prop(context.scene, "metrics_density")

        if (context.scene.metrics_production_method == 'WALLED'):
            col = self.layout.column(align=True)
            col.prop(context.scene, "metrics_wall_thickness")

        box = self.layout.box()
        col = box.column(align=True)
        report = generate_report(
            context.scene.metrics_production_method, context)

        [col.label(text=line) for line in report if line]

        col = self.layout.column(align=False)

        col.operator(MTRX_OT_apply_scale.bl_idname,
                     text=MTRX_OT_apply_scale.bl_label,
                     icon='CON_SIZELIMIT')

        col.operator(MTRX_OT_copy_to_clipboard.bl_idname,
                     text=MTRX_OT_copy_to_clipboard.bl_label,
                     icon='COPYDOWN')
