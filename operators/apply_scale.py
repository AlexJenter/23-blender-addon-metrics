import bpy
from mathutils import Vector
 
class MTRX_OT_apply_scale(bpy.types.Operator):
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