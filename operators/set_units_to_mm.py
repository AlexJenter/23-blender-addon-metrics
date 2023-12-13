from contextvars import Context
import typing
import bpy


class MTRX_OT_set_units_to_mm(bpy.types.Operator):
    """Helps with setting Scene for Millimeters"""
    bl_idname: typing.Union[str, typing.Any] = "metrics.setup_mm"
    bl_label: typing.Union[str, typing.Any] = "Setup for MM"

    def execute(self, context: 'Context') -> typing.Union[typing.Set[int], typing.Set[str]]:
        context.scene.unit_settings.length_unit = 'MILLIMETERS'
        context.scene.unit_settings.scale_length = 0.001
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                context.space_data.overlay.grid_scale = 0.001
                context.space_data.clip_start = 1
                context.space_data.clip_end = 10_000
        return {'FINISHED'}
