import bpy
from ..utils import generate_report

class MTRX_OT_copy_to_clipboard(bpy.types.Operator):
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