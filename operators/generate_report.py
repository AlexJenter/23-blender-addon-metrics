import bpy
from ..utils.generate_report import generate_report


class MTRX_OT_generate_report(bpy.types.Operator):
    bl_label = "Generate Report"
    bl_idname = "metrics.generate_report"

    def execute(self, context):
        context.scene.metrics_report = generate_report(
            context.scene.metrics_production_method, context)
        return {'FINISHED'}
