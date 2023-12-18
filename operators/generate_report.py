import bpy

class MTRX_OT_generate_report(bpy.types.Operator):
    bl_label = "Generate Report"
    bl_idname = "metrics.generate_report"
    def execute(self, context):
        context.scene.metrics_report = "hjello"
        print("hjell")
        return {'FINISHED'}