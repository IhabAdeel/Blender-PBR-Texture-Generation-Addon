# Blender-PBR-Texture-Generation-Addon
A Blender Addon that generates PBR Textures (Albedo, AO, Specular, Roughness, Bump and Displacement maps) with OpenCV and assigns it directly to the object.

This addon only works on Blender 2.8 and beyond

                         ORIGINAL                                           GENERATED
## Installing

To run the addon in blender we need to install OpenCV for blender which can be installed by the following steps:

1. Locate the python terminal in you blender installation folder. For Windows, it can be found at
```
C:\Program Files\Blender Foundation\Blender 2.82\2.82\python\bin
```
2. Open the system terminal and execute the following commands
```
python.exe -m pip install --upgrade pip setuptools wheel --user
python.exe -m pip install opencv-python --user
```
3. Copy the addon folder to the Blender Addon Folder which can be found at
```
C:\Program Files\Blender Foundation\Blender 2.82\2.82\scripts\addons
```
4. Start blender and go to User Prefences and search for PBR Texture Map Generator addon
5. Enable and use
6. The Panel will be located in the 3D viewport, under the Tools Panel

## Using the Texture Generator
1. Enter Material Name: Enter the desired Material name 
2. Select Base/Albedo Image: Locate and open the base image for your texture
3. Generate Textures: This will generate all the required textures and save them in a new/existing folder in the image source location. This will also setup the nodes necessary and the object will be for rendering, all the changes will be seen immediately in the viewport 
4. Purge Selected Unused: This will delete all unused Materials of the same name as that as the one selected currently. This will help remove all the duplicates which may have been generated while editing the textures.
5. Purge All Unused: This will delete ALL materials which are not in use by the object.
      
1. Invert: Use this if you wish to invert the respective Texture Map (this can be done in the node editor as well)
2. Saturation: Use to control the saturation between the Black and White areas of the image for the respective map, min = -5 , max = +5
3. Brightness: Use to control the overall brightness of the respective map, min = -127 , max = +127
4. Gamma: Use for gamma correction(if required) of the respective map, min = 0 , max = +5
5. Threshold: Use to set the maximum threshold of the map, min = 0 , max = +255
6. Kernel: Use to smooth out the displacement map, min = 5 , max = 104
   
The addon has default values for all the above fields and will generate results immediately, these options are only for tweaking the textures if the result was unsatisfactory.

## The Node Setup
1. Mapping: Use to control how the texture is mapped onto the object
2. Invert: Invert the texture map
3. ColorRamp: Use for final touches to the texture maps
4. RGB Curve: Use for controlling the base texture
5. Bump: Use for adjusting the effect of the effect of the bump and displacement maps

## Examples
                        ORIGINAL                                     GENERATED
