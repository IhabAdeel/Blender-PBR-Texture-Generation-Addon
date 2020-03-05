#-----------------------------------------------------------------------
#     Addon Information and imports
#-----------------------------------------------------------------------

bl_info = {
    "name": "PBR Texture Map Generator",
    "description": "Generate and assign PBR textures",
    "author": "Ihab Adeel",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "warning": "", 
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}


import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       PointerProperty,
                       )

from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )

from . nodeSetup import nodeSetup

from . textureGenerator import textureGenerator

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MyProperties(PropertyGroup):

    b_invert: BoolProperty(
        name="Invert Bump",
        description="Invert Bump",
        default = False
        )
    
    s_invert: BoolProperty(
        name="Invert Specular",
        description="Invert Specular",
        default = False
        )

    r_invert: BoolProperty(
        name="Invert Roughness",
        description="Invert Roughness",
        default = False
        )

    a_invert: BoolProperty(
        name="Invert AO",
        description="Invert AO",
        default = False
        )

    d_invert: BoolProperty(
        name="Invert Displacement",
        description="Invert Displacement",
        default = False
        )

    b_bright: IntProperty(
        name = "Bump Brightness",
        description="Bump Brightness",
        default = 0,
        min = -127,
        max = 127
        )
    
    s_bright: IntProperty(
        name = "Specular Brightness",
        description="Specular Brightness",
        default = -35,
        min = -127,
        max = 127
        )

    r_bright: IntProperty(
        name = "Roughness Brightness",
        description="Roughness Brightness",
        default = -50,
        min = -127,
        max = 127
        )

    a_bright: IntProperty(
        name = "AO Brightness",
        description="AO Brightness",
        default = 0,
        min = -127,
        max = 127
        )

    d_bright: IntProperty(
        name = "Displacement Brightness",
        description="Displacement Brightness",
        default = 0,
        min = -127,
        max = 127
        )

    b_gamma: FloatProperty(
        name = "Bump Gamma",
        description = "Bump Gamma",
        default = 1,
        min = 0,
        max = 5
        )

    s_gamma: FloatProperty(
        name = "Specular Gamma",
        description = "Specular Gamma",
        default = 1,
        min = 0,
        max = 5
        )

    r_gamma: FloatProperty(
        name = "Roughness Gamma",
        description = "Roughness Gamma",
        default = 1,
        min = 0,
        max = 5
        )

    a_gamma: FloatProperty(
        name = "AO Gamma",
        description = "AO Gamma",
        default = 1,
        min = 0,
        max = 5
        )

    d_gamma: FloatProperty(
        name = "Displacement Gamma",
        description = "Displacement Gamma",
        default = 1,
        min = 0,
        max = 5
        )

    b_sat: FloatProperty(
        name = "Bump Saturation",
        description = "Bump Saturation",
        default = 1,
        min = -5,
        max = 5
        )

    s_sat: FloatProperty(
        name = "Specular Saturation",
        description = "Specular Saturation",
        default = 1,
        min = -5,
        max = 5
        )

    r_sat: FloatProperty(
        name = "Roughness Saturation",
        description = "Roughness Saturation",
        default = 1,
        min = -5,
        max = 5
        )

    a_sat: FloatProperty(
        name = "AO Saturation",
        description = "AO Saturation",
        default = 2,
        min = -5,
        max = 5
        )

    d_sat: FloatProperty(
        name = "Displacement Saturation",
        description = "Displacement Saturation",
        default = 1.5,
        min = -5,
        max = 5
        )

    s_threshold: IntProperty(
        name = "Specular Threshold",
        description="Specular Threshold",
        default = 25,
        min = 0,
        max = 255
        )
    
    a_threshold: IntProperty(
        name = "AO Threshold",
        description="AO Threshold",
        default = 127,
        min = 0,
        max = 255
        )

    d_kernel: IntProperty(
        name = "Kernel Smooth",
        description="Kernel Smooth",
        default = 11,
        min = 5,
        max = 105
        )

    mat_name: StringProperty(
        name="",
        description="",
        default="default",
        maxlen=1024,
        )

    image_path: StringProperty(
        name = "",
        description="",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
        )

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------
class WM_OT_generateTextures(Operator):
    bl_label = "Generate Textures"
    bl_idname = "wm.generatetextures"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        b_props = [mytool.a_invert, mytool.a_sat, mytool.a_bright, mytool.a_gamma]
        s_props = [mytool.s_invert, mytool.s_sat, mytool.s_bright, mytool.s_gamma, mytool.s_threshold]
        r_props = [mytool.r_invert, mytool.r_sat, mytool.r_bright, mytool.r_gamma]
        a_props = [mytool.a_invert, mytool.a_sat, mytool.a_bright, mytool.a_gamma, mytool.a_threshold]
        d_props = [mytool.d_invert, mytool.d_sat, mytool.d_bright, mytool.d_gamma, mytool.d_kernel]

        textureGenerator.main(mytool.image_path, mytool.mat_name, b_props, s_props, r_props, a_props, d_props)

        return {'FINISHED'}

class WM_OT_purgeSelected(Operator):
    bl_label = "Purge Selected Unused"
    bl_idname = "wm.purgeselected"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        for image in bpy.data.images:
            if image.users or (image.users == 1 and image.use_fake_user):
                continue
            bpy.data.images.remove(image)

        selected = bpy.context.active_object.active_material.name[:-4]

        for material in bpy.data.materials:
            if material.name[:-4] == selected or (material.name == selected):
                if material.users or (material.users == 1 and material.use_fake_user):
                    continue
                bpy.data.materials.remove(material)
        
        return {'FINISHED'}

class WM_OT_purgeAll(Operator):
    bl_label = "Purge All Unused"
    bl_idname = "wm.purgeall"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        for image in bpy.data.images:
            if image.users or (image.users == 1 and image.use_fake_user):
                continue
            bpy.data.images.remove(image)

        for material in bpy.data.materials:
            if material.users or (material.users == 1 and material.use_fake_user):
                continue
            bpy.data.materials.remove(material)

        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tools"
    bl_context = "objectmode"   

class OBJECT_PT_MainPanel(OBJECT_PT_CustomPanel, Panel):
    bl_idname = "OBJECT_PT_mainpanel"
    bl_label = "PBR Texture Generator"

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.label(text = 'Enter Material name:')
        layout.prop(mytool, "mat_name")
        layout.label(text = 'Select Base/Albedo image')
        layout.prop(mytool, "image_path")
        layout.operator("wm.generatetextures")
        layout.operator("wm.purgeselected")
        layout.operator("wm.purgeall")
        layout.separator()

class OBJECT_PT_AO(OBJECT_PT_CustomPanel, Panel):
    bl_parent_id = "OBJECT_PT_mainpanel"
    bl_label = "AO Map"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "a_invert")
        layout.prop(mytool, "a_sat")
        layout.prop(mytool, "a_bright")
        layout.prop(mytool, "a_gamma")
        layout.prop(mytool, "a_threshold")

class OBJECT_PT_SPECULAR(OBJECT_PT_CustomPanel, Panel):
    bl_parent_id = "OBJECT_PT_mainpanel"
    bl_label = "Specular Map"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "s_invert")
        layout.prop(mytool, "s_sat")
        layout.prop(mytool, "s_bright")
        layout.prop(mytool, "s_gamma")
        layout.prop(mytool, "s_threshold")

class OBJECT_PT_ROUGHNESS(OBJECT_PT_CustomPanel, Panel):
    bl_parent_id = "OBJECT_PT_mainpanel"
    bl_label = "Roughness Map"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "r_invert")
        layout.prop(mytool, "r_sat")
        layout.prop(mytool, "r_bright")
        layout.prop(mytool, "r_gamma")

class OBJECT_PT_BUMP(OBJECT_PT_CustomPanel, Panel):
    bl_parent_id = "OBJECT_PT_mainpanel"
    bl_label = "Bump Map"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "b_invert")
        layout.prop(mytool, "b_sat")
        layout.prop(mytool, "b_bright")
        layout.prop(mytool, "b_gamma")

class OBJECT_PT_DISPLACEMENT(OBJECT_PT_CustomPanel, Panel):
    bl_parent_id = "OBJECT_PT_mainpanel"
    bl_label = "Displacement Map"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "d_invert")
        layout.prop(mytool, "d_sat")
        layout.prop(mytool, "d_bright")
        layout.prop(mytool, "d_gamma")
        layout.prop(mytool, "d_threshold")
        layout.prop(mytool, "d_kernel")

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MyProperties,
    WM_OT_generateTextures,
    WM_OT_purgeSelected,
    WM_OT_purgeAll,
    OBJECT_PT_MainPanel,
    OBJECT_PT_AO,
    OBJECT_PT_SPECULAR,
    OBJECT_PT_ROUGHNESS,
    OBJECT_PT_BUMP,
    OBJECT_PT_DISPLACEMENT
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()
    
