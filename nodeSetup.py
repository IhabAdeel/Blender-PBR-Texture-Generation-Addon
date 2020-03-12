import bpy
import os

class nodeSetup:
    def reload():
        for image in bpy.data.images:
            image.reload()

    def main(directory, name):    
        
        '''CREATING MATERIAL'''

        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
    
        '''NODE CREATION'''

        #Pricipled BSDF 
        node = nodes['Principled BSDF']
        node.location = 950, 330

        #Output Node    
        node = nodes['Material Output']
        node.location = 1250, 330

        #Texture Coordinate    
        node = nodes.new('ShaderNodeTexCoord')
        node.name = 'TextCoordinate'
        node.location = -900, 120
    
        #Mapping     
        node = nodes.new('ShaderNodeMapping')
        node.name = 'Mapping'    
        node.location = -700, 120

        #Specular Image    
        node = nodes.new('ShaderNodeTexImage')
        node.name = 'Specular'  
        print(directory)
        node.image = bpy.data.images.load(os.path.join(directory, 'Specular.png'))
        node.image.colorspace_settings.name = 'Non-Color'      
        node.location = -325, 200
    
        #Roughness    
        node = nodes.new('ShaderNodeTexImage')
        node.name = 'Roughness'
        node.image = bpy.data.images.load(os.path.join(directory, 'Roughness.png'))
        node.image.colorspace_settings.name = 'Non-Color'
        node.location = -325, -30

        #AO
        node = nodes.new('ShaderNodeTexImage')
        node.name = 'AO'
        node.image = bpy.data.images.load(os.path.join(directory, 'AO.png'))
        node.image.colorspace_settings.name = 'Non-Color'
        node.location = -325, 430

        #Bump
        node = nodes.new('ShaderNodeTexImage')
        node.name = 'Bump'
        node.image = bpy.data.images.load(os.path.join(directory, 'Bump.png'))
        node.image.colorspace_settings.name = 'Non-Color'
        node.location = -325, -260

        #Base
        node = nodes.new('ShaderNodeTexImage')
        node.name = 'Base'
        node.image = bpy.data.images.load(os.path.join(directory, 'Base.png'))
        node.location = -325, 660

        #RGB Curves
        node = nodes.new('ShaderNodeRGBCurve')
        node.name = 'RGBCurve'
        node.location = -25, 780

        node = nodes.new('ShaderNodeInvert')
        node.name = 'AO_Invert'
        node.inputs[0].default_value = 0
        node.location = -25, 430

        node = nodes.new('ShaderNodeInvert')
        node.name = 'Specular_Invert'
        node.inputs[0].default_value = 0
        node.location = -25, 200

        node = nodes.new('ShaderNodeInvert')
        node.name = 'Roughness_Invert'
        node.inputs[0].default_value = 0
        node.location = -25, -30

        node = nodes.new('ShaderNodeInvert')
        node.name = 'Bump_Invert'
        node.inputs[0].default_value = 0
        node.location = -25, -260

        node = nodes.new('ShaderNodeValToRGB')
        node.name = 'AO_ColorRamp'
        point = node.color_ramp.elements
        point[0].position = 0.8
        node.location = 250, 430

        node = nodes.new('ShaderNodeValToRGB')
        node.name = 'Specular_ColorRamp'
        point = node.color_ramp.elements
        point[0].position = 0.8
        node.location = 250, 200

        node = nodes.new('ShaderNodeValToRGB')
        node.name = 'Roughness_ColorRamp'
        point = node.color_ramp.elements
        point[0].position = 0.8
        node.location = 250, -30

        node = nodes.new('ShaderNodeValToRGB')
        node.name = 'Bump_ColorRamp'
        point = node.color_ramp.elements
        point[1].position = 1
        node.location = 250, -260

        #Mix RGB
        node = nodes.new('ShaderNodeMixRGB')
        node.name = 'MixRGB'
        node.blend_type = 'MULTIPLY'
        node.location = 530, 530

        node = nodes.new('ShaderNodeNormalMap')
        node.name = 'NormalMap'
        node.location = 1330, -260

        #Bump
        node = nodes.new('ShaderNodeBump')
        node.name = 'BumpNode'
        node.inputs[0].default_value = 1
        node.inputs[1].default_value = 0.05
        node.location = 530, -260

        #Value1
        node = nodes.new('ShaderNodeValue')
        node.name = 'Value1'
        node.outputs[0].default_value = 1
        node.location = 530, -460

        #Value2
        node = nodes.new('ShaderNodeValue')
        node.name = 'Value2'
        node.outputs[0].default_value = 0.5
        node.location = 730, -460

        #Add
        node = nodes.new('ShaderNodeMixRGB')
        node.name = 'Add'
        node.blend_type = 'ADD'
        node.inputs[0].default_value = 1
        node.location = 730, -260

        #Multiply
        node = nodes.new('ShaderNodeMixRGB')
        node.name = 'Multiply'
        node.blend_type = 'MULTIPLY'
        node.inputs[0].default_value = 1
        node.location = 930, -260

        #Gamma
        node = nodes.new('ShaderNodeGamma')
        node.name = 'Gamma'
        node.inputs[1].default_value = 2.2
        node.location = 1130, -260

        '''LINKING NODES'''

        node_source = ['TextCoordinate','Mapping','Mapping','Mapping', 'Mapping',  'Mapping','Base',    'AO',       'Specular',       'Roughness',       'Bump',       'RGBCurve','AO_Invert',   'Specular_Invert',   'Roughness_Invert',   'Bump_Invert',   'AO_ColorRamp','Bump_ColorRamp','MixRGB',         'Specular_ColorRamp','Roughness_ColorRamp','BumpNode','Value1', 'Value2',   'Add',     'Multiply','Gamma',    'NormalMap']
        node_dest =   ['Mapping',       'Base',   'AO',     'Specular','Roughness','Bump',   'RGBCurve','AO_Invert','Specular_Invert','Roughness_Invert','Bump_Invert','MixRGB',  'AO_ColorRamp','Specular_ColorRamp','Roughness_ColorRamp','Bump_ColorRamp','MixRGB',      'BumpNode',      'Principled BSDF','Principled BSDF',   'Principled BSDF',    'Add',     'Add',    'Multiply', 'Multiply','Gamma',   'NormalMap','Principled BSDF']
        output =      ['UV',            'Vector', 'Vector', 'Vector',  'Vector',   'Vector', 'Color',   'Color',    'Color',          'Color',           'Color',      'Color',   'Color',       'Color',             'Color',              'Color',         'Color',       'Color',         'Color',          'Color',             'Color',              'Normal',  'Value',  'Value',    'Color',   'Color',   'Color',    'Normal']
        in_put =      ['Vector',        'Vector', 'Vector', 'Vector',  'Vector',   'Vector', 'Color',   'Color',    'Color',          'Color',           'Color',      'Color1',  0,             0,                   0,                    0,               'Color2',      'Height',        'Base Color',     'Specular',          'Roughness',          'Color1',  'Color2', 'Color2',   'Color1',  'Color',   'Color',    'Normal']

        for i in range(len(output)):
            mat.node_tree.links.new(nodes[node_source[i]].outputs[output[i]], nodes[node_dest[i]].inputs[in_put[i]])

        '''ASSIGNING MATERIAL TO ACTIVE OBJECT'''
        bpy.context.active_object.active_material = mat
