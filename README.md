# Blender-PBR-Texture-Generation-Addon
A Blender Addon that generates PBR Textures (Albedo, AO, Specular, Roughness, Bump and Displacement maps) with OpenCV and assigns it directly to the object.

This addon only works on Blender 2.8 and beyond

                         ORIGINAL                                           GENERATED
[![Example](https://user-images.githubusercontent.com/43339338/76030875-95053d80-5f5c-11ea-8454-2cdbe3a5af7c.png)]()

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
[![Main Panel](https://user-images.githubusercontent.com/43339338/76028699-22df2980-5f59-11ea-9cf0-07e3c6a3660c.png)]()
1. Enter Material Name: Enter the desired Material name 
2. Select Base/Albedo Image: Locate and open the base image for your texture
3. Generate Textures: This will generate all the required textures and save them in a new/existing folder in the image source location. This will also setup the nodes necessary and the object will be for rendering, all the changes will be seen immediately in the viewport 
4. Purge Selected Unused: This will delete all unused Materials of the same name as that as the one selected currently. This will help remove all the duplicates which may have been generated while editing the textures.
5. Purge All Unused: This will delete ALL materials which are not in use by the object.
      
[![Sub Panel](https://user-images.githubusercontent.com/43339338/76028700-2377c000-5f59-11ea-94fe-bdf33caaed5d.png)]()
1. Invert: Use this if you wish to invert the respective Texture Map (this can be done in the node editor as well)
2. Saturation: Use to control the saturation between the Black and White areas of the image for the respective map, min = -5 , max = +5
3. Brightness: Use to control the overall brightness of the respective map, min = -127 , max = +127
4. Gamma: Use for gamma correction(if required) of the respective map, min = 0 , max = +5
5. Threshold: Use to set the maximum threshold of the map, min = 0 , max = +255
6. Kernel: Use to smooth out the displacement map, min = 5 , max = 104
   
The addon has default values for all the above fields and will generate results immediately, these options are only for tweaking the textures if the result was unsatisfactory.

## The Node Setup
[![Node Setup](https://user-images.githubusercontent.com/43339338/76031591-fed21700-5f5d-11ea-8f5e-247ba95136a7.png)]()
1. Mapping: Use to control how the texture is mapped onto the object
2. Invert: Invert the texture map
3. ColorRamp: Use for final touches to the texture maps
4. RGB Curve: Use for controlling the base texture
5. Bump: Use for adjusting the effect of the effect of the bump and displacement maps

## Examples
                        ORIGINAL                                     GENERATED
[![eg1](https://user-images.githubusercontent.com/43339338/76033459-55d9eb00-5f62-11ea-9233-568771b7779e.png)]()
[![eg2](https://user-images.githubusercontent.com/43339338/76033466-596d7200-5f62-11ea-9976-188be6b91264.png)]()
[![eg3](https://user-images.githubusercontent.com/43339338/76033470-5d00f900-5f62-11ea-9e04-caf2e61020d3.png)]()
[![eg4](https://user-images.githubusercontent.com/43339338/76033474-5f635300-5f62-11ea-962f-1835555ad2e7.png)]()
[![eg5](https://user-images.githubusercontent.com/43339338/76033488-62f6da00-5f62-11ea-9f85-989a112729ba.png)]()
