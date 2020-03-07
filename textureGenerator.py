import cv2
import numpy as np
import os
import shutil
from . nodeSetup import * 

class textureGenerator:

    g_BaseImage = None
    g_GrayImage = None
    g_DstFolder = None

    def image_invert(image):
        return cv2.bitwise_not(image)

    def gamma_correction(image, gamma = 1):
        inv_gamma = 1 / gamma
        table = np.array([((i / 255) ** inv_gamma) * 255 for i in range(0, 256)]).astype("uint8")
        return cv2.LUT(image, table)

    def bump(grayScale, b_props):
        grayScale = cv2.bitwise_not(grayScale)
        bumpImage = cv2.convertScaleAbs(grayScale, alpha = b_props[1], beta = b_props[2])
        bumpImage = textureGenerator.gamma_correction(bumpImage, b_props[3])
        if b_props[0] == True:
            bumpImage = textureGenerator.image_invert(bumpImage)
        return bumpImage

    def specular(grayScale, s_props):
        th1, specularImage = cv2.threshold(grayScale, s_props[4], 255, cv2.THRESH_TOZERO)
        specularImage = cv2.convertScaleAbs(specularImage, alpha = s_props[1], beta = s_props[2])
        specularImage = textureGenerator.gamma_correction(specularImage, s_props[3])
        if s_props[0] == True:
            specularImage = textureGenerator.image_invert(specularImage)
        return specularImage

    def roughness(grayScale, r_props):
        roughnessImage = cv2.bitwise_not(grayScale)
        roughnessImage = cv2.convertScaleAbs(grayScale, alpha = r_props[1], beta = r_props[2])
        roughnessImage = textureGenerator.gamma_correction(roughnessImage, r_props[3])
        if r_props[0] == True:
            roughnessImage = textureGenerator.image_invert(roughnessImage)
        return roughnessImage

    def ambient(grayScale, a_props):
        th2, aoImage = cv2.threshold(grayScale, a_props[4], 255, cv2.THRESH_TRUNC)
        aoImage = cv2.convertScaleAbs(aoImage, alpha = a_props[1], beta = a_props[2])
        aoImage = textureGenerator.gamma_correction(aoImage, a_props[3])
        if a_props[0] == True:
            aoImage = textureGenerator.image_invert(aoImage)
        return aoImage

    def main(directory, name, b_props, s_props, r_props, a_props):
        
        global g_BaseImage
        global g_GrayImage
        
        baseImage = cv2.imread(directory)
        grayScale = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)
        grayScale = cv2.equalizeHist(grayScale)

        bumpImage = textureGenerator.bump(grayScale, b_props)
        specularImage = textureGenerator.specular(grayScale, s_props)
        roughnessImage = textureGenerator.roughness(grayScale, r_props)
        aoImage = textureGenerator.ambient(grayScale, a_props)

        g_BaseImage = baseImage
        g_GrayImage = grayScale
        
        image = [baseImage, bumpImage, specularImage, roughnessImage, aoImage]
        imageType = ["Base", "Bump", "Specular", "Roughness", "AO"]

        textureGenerator.saving(image, imageType, directory, name)

    def saving(image, imageType, directory, name):
        
        global g_DstFolder

        parent = os.path.dirname(directory)
        dstFolder = parent + '\\' + name + '\\'

        g_DstFolder = dstFolder

        if os.path.exists(dstFolder):
            shutil.rmtree(dstFolder)
        os.makedirs(dstFolder)

        for i in range(len(image)):
            if os.path.exists(dstFolder + imageType[i] + ".png"):
                os.remove(imageType[i] + ".png")
            cv2.imwrite(dstFolder + imageType[i] + ".png", image[i])

        nodeSetup.main(dstFolder, name)

    def changes(props, type):
        
        name = None
        global g_DstFolder
        
        if type == 0:
            name = "AO"
            Image = textureGenerator.ambient(g_GrayImage, props)
        elif type == 1:
            name = "Specular"
            Image = textureGenerator.specular(g_GrayImage, props)
        elif type == 2:
            name = "Roughness"
            Image = textureGenerator.roughness(g_GrayImage, props)
        else:
            name = "Bump"
            Image = textureGenerator.bump(g_GrayImage, props)
        
        print(g_DstFolder + name + ".png")

        if os.path.exists(g_DstFolder + name + ".png"):
            os.remove(g_DstFolder + name + ".png")
        cv2.imwrite(g_DstFolder + name + ".png", Image)      

        nodeSetup.reload()
