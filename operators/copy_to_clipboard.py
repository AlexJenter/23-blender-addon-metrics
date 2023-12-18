import bpy
from ..utils.generate_report import generate_report
from ..types import operator


class MTRX_OT_copy_to_clipboard(bpy.types.Operator):
    """Copy report to system clipboard"""
    bl_idname = "metrics.copy_to_clipboard"
    bl_label = "Copy report"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(self: bpy.types.Operator, context: bpy.types.Context) -> bool:
        return context.mode == "OBJECT"

    def execute(self: bpy.types.Operator, context: bpy.types.Context) -> operator.executeReturn:
        bpy.context.window_manager.clipboard = context.scene.metrics_report

        self.report({'INFO'}, f"Metrics: Report has been copied to clipboard")
        return {'FINISHED'}