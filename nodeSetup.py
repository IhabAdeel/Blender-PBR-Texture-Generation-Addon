import bpy

class nodeSetup:
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
        node.image = bpy.data.images.load(directory+'Specular.jpg')
        node.image.colorspace_settings.name = 'Non-Color'      
        node.location = -325, 200
    
        #Roughness    
        node = nodes.new('ShaderNodeTexImage')
        node.name = 'Roughness'
        node.image = bpy.data.images.load(directory+'Roughness.jpg')
        node.image.colorspace_settings.name = 'Non-Color'
        node.location = -325, -30

        #AO
        node = nodes.new('ShaderNodeTexImage')
        node.name = 'AO'
        node.image = bpy.data.images.load(directory+'AO.jpg')
        node.image.colorspace_settings.name = 'Non-Color'
        node.location = -325, 430

        #Bump
        node = nodes.new('ShaderNodeTexImage')
        node.name = 'Bump'
        node.image = bpy.data.images.load(directory+'Bump.jpg')
        node.image.colorspace_settings.name = 'Non-Color'
        node.location = -325, -260

        #Base
        node = nodes.new('ShaderNodeTexImage')
        node.name = 'Base'
        node.image = bpy.data.images.load(directory+'Base.jpg')
        node.location = -325, 660

        #Dispalcement
        node = nodes.new('ShaderNodeTexImage')
        node.name = 'Displacement'
        node.image = bpy.data.images.load(directory+'Displacement.jpg')
        node.image.colorspace_settings.name = 'Non-Color'
        node.location = -325, -490

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

        node = nodes.new('ShaderNodeInvert')
        node.name = 'Displacement_Invert'
        node.inputs[0].default_value = 0
        node.location = -25, -490

        node = nodes.new('ShaderNodeValToRGB')
        node.name = 'AO_ColorRamp'
        node.location = 250, 430

        node = nodes.new('ShaderNodeValToRGB')
        node.name = 'Specular_ColorRamp'
        node.location = 250, 200

        node = nodes.new('ShaderNodeValToRGB')
        node.name = 'Roughness_ColorRamp'
        node.location = 250, -30

        node = nodes.new('ShaderNodeValToRGB')
        node.name = 'Bump_ColorRamp'
        node.location = 250, -260

        node = nodes.new('ShaderNodeValToRGB')
        node.name = 'Displacement_ColorRamp'
        node.location = 250, -490

        #Mix RGB
        node = nodes.new('ShaderNodeMixRGB')
        node.name = 'MixRGB'
        node.blend_type = 'MULTIPLY'
        node.location = 530, 530

        node = nodes.new('ShaderNodeNormalMap')
        node.name = 'NormalMap'
        node.location = 530, -260

        #Bump
        node = nodes.new('ShaderNodeBump')
        node.name = 'BumpNode'
        node.inputs[0].default_value = 0.5
        node.location = 730, -400

        '''LINKING NODES'''

        node_source = ['TextCoordinate','Mapping','Mapping','Mapping','Mapping','Mapping','Mapping','Base','AO','Specular','Roughness','Displacement','Bump','RGBCurve','AO_Invert','Specular_Invert','Roughness_Invert','Bump_Invert','Displacement_Invert','AO_ColorRamp','Bump_ColorRamp','MixRGB','NormalMap','Specular_ColorRamp','Roughness_ColorRamp','BumpNode','Displacement_ColorRamp']
        node_dest = ['Mapping','Base','AO','Specular','Roughness','Bump','Displacement','RGBCurve','AO_Invert','Specular_Invert','Roughness_Invert','Displacement_Invert','Bump_Invert','MixRGB','AO_ColorRamp','Specular_ColorRamp','Roughness_ColorRamp','Bump_ColorRamp','Displacement_ColorRamp','MixRGB','NormalMap','Principled BSDF','BumpNode','Principled BSDF','Principled BSDF','Principled BSDF','BumpNode']
        output = ['UV','Vector','Vector','Vector','Vector','Vector','Vector','Color','Color','Color','Color','Color','Color','Color','Color','Color','Color','Color','Color','Color','Color','Color','Normal','Color','Color','Normal','Color']
        in_put = ['Vector','Vector','Vector','Vector','Vector','Vector','Vector','Color','Color','Color','Color','Color','Color','Color1',0,0,0,0,0,'Color2','Color','Base Color','Normal','Specular','Roughness','Normal','Height']

        for i in range(len(output)):
            mat.node_tree.links.new(nodes[node_source[i]].outputs[output[i]], nodes[node_dest[i]].inputs[in_put[i]])

        '''ASSIGNING MATERIAL TO ACTIVE OBJECT'''
        bpy.context.active_object.active_material = mat
