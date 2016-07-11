import shutil
import bpy
import os
import json
import nodes_pipeline
from bpy.types import Menu, Panel, UIList
from bpy.props import *

def cb_scene_update(context):
    edit_obj = bpy.context.edit_object
    if edit_obj is not None and edit_obj.is_updated_data is True:
        edit_obj.geometry_cached = False

def initProperties():
    # For project
    bpy.types.World.CGVersion = StringProperty(name = "CGVersion", default="")
    bpy.types.World.CGProjectTarget = EnumProperty(
        items = [('HTML5', 'HTML5', 'HTML5'), 
                 ('Windows', 'Windows', 'Windows'), 
                 ('OSX', 'OSX', 'OSX'),
                 ('Linux', 'Linux', 'Linux'), 
                 ('iOS', 'iOS', 'iOS'),
                 ('Android', 'Android', 'Android')],
        name = "Target", default='HTML5')
    bpy.types.World.CGProjectName = StringProperty(name = "Name", default="ArmoryGame")
    bpy.types.World.CGProjectPackage = StringProperty(name = "Package", default="game")
    bpy.types.World.CGProjectWidth = IntProperty(name = "Width", default=800)
    bpy.types.World.CGProjectHeight = IntProperty(name = "Height", default=600)
    bpy.types.World.CGProjectScene = StringProperty(name = "Scene")
    bpy.types.World.CGProjectSamplesPerPixel = IntProperty(name = "Samples per pixel", default=1)
    bpy.types.World.CGPhysics = EnumProperty(
        items = [('Disabled', 'Disabled', 'Disabled'), 
                 ('Bullet', 'Bullet', 'Bullet')],
        name = "Physics", default='Bullet')
    bpy.types.World.CGKhafileConfig = StringProperty(name = "Config")
    bpy.types.World.CGMinimize = BoolProperty(name="Minimize Data", default=True)
    bpy.types.World.CGOptimizeGeometry = BoolProperty(name="Optimize Geometry", default=False)
    bpy.types.World.CGCacheShaders = BoolProperty(name="Cache Shaders", default=True)
    bpy.types.World.CGPlayViewportCamera = BoolProperty(name="Viewport Camera", default=False)
    bpy.types.World.CGPlayConsole = BoolProperty(name="Debug Console", default=False)
    bpy.types.World.CGPlayDeveloperTools = BoolProperty(name="Developer Tools", default=False)

    # For object
    bpy.types.Object.geometry_cached = bpy.props.BoolProperty(name="Geometry Cached", default=False) # TODO: move to mesh type
    bpy.types.Object.instanced_children = bpy.props.BoolProperty(name="Instanced Children", default=False)
    bpy.types.Object.custom_material = bpy.props.BoolProperty(name="Custom Material", default=False)
    bpy.types.Object.custom_material_name = bpy.props.StringProperty(name="Name", default="")
    bpy.types.Object.game_export = bpy.props.BoolProperty(name="Game Export", default=True)
    # For geometry
    bpy.types.Mesh.static_usage = bpy.props.BoolProperty(name="Static Usage", default=True)
    # For camera
    bpy.types.Camera.frustum_culling = bpy.props.BoolProperty(name="Frustum Culling", default=False)
    bpy.types.Camera.sort_front_to_back = bpy.props.BoolProperty(name="Sort Front to Back", default=False)
    bpy.types.Camera.pipeline_path = bpy.props.StringProperty(name="Pipeline Path", default="deferred_pipeline")
    bpy.types.Camera.pipeline_id = bpy.props.StringProperty(name="Pipeline ID", default="deferred")
	# TODO: Specify multiple material ids, merge ids from multiple cameras 
    bpy.types.Camera.geometry_context = bpy.props.StringProperty(name="Geometry", default="deferred")
    bpy.types.Camera.shadows_context = bpy.props.StringProperty(name="Shadows", default="shadowmap")
    bpy.types.Camera.translucent_context = bpy.props.StringProperty(name="Translucent", default="translucent")
    bpy.types.Camera.is_probe = bpy.props.BoolProperty(name="Probe", default=False)
    bpy.types.Camera.probe_generate_radiance = bpy.props.BoolProperty(name="Generate Radiance", default=False)
    bpy.types.Camera.probe_texture = bpy.props.StringProperty(name="Texture", default="")
    bpy.types.Camera.probe_num_mips = bpy.props.IntProperty(name="Number of mips", default=0)
    bpy.types.Camera.probe_volume = bpy.props.StringProperty(name="Volume", default="")
    bpy.types.Camera.probe_strength = bpy.props.FloatProperty(name="Strength", default=1.0)
    bpy.types.Camera.probe_blending = bpy.props.FloatProperty(name="Blending", default=0.0)
	# TODO: move to world
    bpy.types.Camera.world_envtex_name = bpy.props.StringProperty(name="Environment Texture", default='')
    bpy.types.Camera.world_envtex_num_mips = bpy.props.IntProperty(name="Number of mips", default=0)
    bpy.types.Camera.world_envtex_color = bpy.props.FloatVectorProperty(name="Environment Color", size=4, default=[0,0,0,1])
    bpy.types.Camera.world_envtex_strength = bpy.props.FloatProperty(name="Environment Strength", default=1.0)
    bpy.types.Camera.world_envtex_sun_direction = bpy.props.FloatVectorProperty(name="Sun Direction", size=3, default=[0,0,0])
    bpy.types.Camera.world_envtex_turbidity = bpy.props.FloatProperty(name="Turbidity", default=1.0)
    bpy.types.Camera.world_envtex_ground_albedo = bpy.props.FloatProperty(name="Ground Albedo", default=0.0)
    bpy.types.Camera.last_decal_context = bpy.props.StringProperty(name="Decal Context", default='')
    bpy.types.World.world_defs = bpy.props.StringProperty(name="World Shader Defs", default='')
    bpy.types.World.generate_radiance = bpy.props.BoolProperty(name="Generate Radiance", default=True)
    bpy.types.World.generate_clouds = bpy.props.BoolProperty(name="Generate Clouds", default=False)
    bpy.types.World.generate_clouds_density = bpy.props.FloatProperty(name="Density", default=0.2, min=0.0, max=10.0)
    bpy.types.World.generate_clouds_size = bpy.props.FloatProperty(name="Size", default=1.0, min=0.0, max=10.0)
    bpy.types.World.generate_clouds_lower = bpy.props.FloatProperty(name="Lower", default=2.0, min=1.0, max=10.0)
    bpy.types.World.generate_clouds_upper = bpy.props.FloatProperty(name="Upper", default=3.5, min=1.0, max=10.0)
    bpy.types.World.generate_clouds_wind = bpy.props.FloatVectorProperty(name="Wind", default=[0.2, 0.06], size=2)
    bpy.types.World.generate_clouds_secondary = bpy.props.FloatProperty(name="Secondary", default=0.0, min=0.0, max=10.0)
    bpy.types.World.generate_clouds_precipitation = bpy.props.FloatProperty(name="Precipitation", default=1.0, min=0.0, max=2.0)
    bpy.types.World.generate_clouds_eccentricity = bpy.props.FloatProperty(name="Eccentricity", default=0.6, min=0.0, max=1.0)
    bpy.types.World.shadowmap_size = bpy.props.IntProperty(name="Shadowmap Size", default=0)
    bpy.types.World.scripts_list = bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    bpy.types.World.bundled_scripts_list = bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    # For material
    bpy.types.Material.receive_shadow = bpy.props.BoolProperty(name="Receive Shadow", default=True)
    bpy.types.Material.custom_shader = bpy.props.BoolProperty(name="Custom Shader", default=False)
    bpy.types.Material.custom_shader_name = bpy.props.StringProperty(name="Name", default='')
    bpy.types.Material.stencil_mask = bpy.props.IntProperty(name="Stencil Mask", default=0)
    bpy.types.Material.export_tangents = bpy.props.BoolProperty(name="Export Tangents", default=False)
    bpy.types.Material.skip_context = bpy.props.StringProperty(name="Skip Context", default='')
    # For scene
    bpy.types.Scene.game_export = bpy.props.BoolProperty(name="Game Export", default=True)

# Menu in object region
class ObjectPropsPanel(bpy.types.Panel):
    bl_label = "Armory Props"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
 
    def draw(self, context):
        layout = self.layout
        obj = bpy.context.object

        layout.prop(obj, 'game_export')

        if obj.type == 'MESH':
            layout.prop(obj, 'instanced_children')
            layout.prop(obj, 'custom_material')
            if obj.custom_material:
                layout.prop(obj, 'custom_material_name')

# Menu in data region
class DataPropsPanel(bpy.types.Panel):
    bl_label = "Armory Props"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
 
    def draw(self, context):
        layout = self.layout
        obj = bpy.context.object

        if obj.type == 'CAMERA':
            layout.prop(obj.data, 'is_probe')
            if obj.data.is_probe == True:
                layout.prop(obj.data, 'probe_texture')
                layout.prop_search(obj.data, "probe_volume", bpy.data, "objects")
                layout.prop(obj.data, 'probe_strength')
                layout.prop(obj.data, 'probe_blending')
            layout.prop(obj.data, 'frustum_culling')
            layout.prop(obj.data, 'sort_front_to_back')
            layout.prop_search(obj.data, "pipeline_path", bpy.data, "node_groups")
            layout.operator("cg.reset_pipelines")
        elif obj.type == 'MESH':
            layout.prop(obj.data, 'static_usage')
            layout.operator("cg.invalidate_cache")

class ScenePropsPanel(bpy.types.Panel):
    bl_label = "Armory Props"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
 
    def draw(self, context):
        layout = self.layout
        obj = bpy.context.scene
        layout.prop(obj, 'game_export')

class OBJECT_OT_RESETPIPELINESButton(bpy.types.Operator):
    bl_idname = "cg.reset_pipelines"
    bl_label = "Reset Pipelines"
 
    def execute(self, context):
        nodes_pipeline.reset_pipelines()
        return{'FINISHED'}

class OBJECT_OT_INVALIDATECACHEButton(bpy.types.Operator):
    bl_idname = "cg.invalidate_cache"
    bl_label = "Invalidate Cache"
 
    def execute(self, context):
        context.object.geometry_cached = False
        return{'FINISHED'}

# Menu in materials region
class MatsPropsPanel(bpy.types.Panel):
    bl_label = "Armory Props"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
 
    def draw(self, context):
        layout = self.layout
        mat = bpy.context.material

        layout.prop(mat, 'receive_shadow')
        layout.prop(mat, 'custom_shader')
        if mat.custom_shader:
            layout.prop(mat, 'custom_shader_name')
        layout.prop(mat, 'stencil_mask')
        layout.prop(mat, 'skip_context')

# Menu in world region
class WorldPropsPanel(bpy.types.Panel):
    bl_label = "Armory Props"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "world"
 
    def draw(self, context):
        layout = self.layout
        wrd = bpy.context.world
        layout.prop(wrd, 'generate_radiance')
        layout.prop(wrd, 'generate_clouds')
        if wrd.generate_clouds:
            layout.prop(wrd, 'generate_clouds_density')
            layout.prop(wrd, 'generate_clouds_size')
            layout.prop(wrd, 'generate_clouds_lower')
            layout.prop(wrd, 'generate_clouds_upper')
            layout.prop(wrd, 'generate_clouds_wind')
            layout.prop(wrd, 'generate_clouds_secondary')
            layout.prop(wrd, 'generate_clouds_precipitation')
            layout.prop(wrd, 'generate_clouds_eccentricity')

# Registration
def register():
    bpy.utils.register_module(__name__)
    initProperties()
    bpy.app.handlers.scene_update_post.append(cb_scene_update)

def unregister():
    bpy.app.handlers.scene_update_post.remove(cb_scene_update)
    bpy.utils.unregister_module(__name__)
