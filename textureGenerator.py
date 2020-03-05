import cv2
import numpy as np
import os
import shutil
from . nodeSetup import nodeSetup 

class textureGenerator:
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

    def displacement(grayScale, d_props):
        displaceImage = cv2.convertScaleAbs(grayScale, alpha = d_props[1], beta = d_props[2])
        displaceImage = cv2.bitwise_not(displaceImage)
        displaceImage = cv2.convertScaleAbs(displaceImage, alpha = d_props[1], beta = d_props[2])
        displaceImage = cv2.bitwise_not(displaceImage)
        displaceImage = cv2.bilateralFilter(displaceImage, d_props[4], 75, 75)
        displaceImage = textureGenerator.gamma_correction(displaceImage, d_props[3])
        if d_props[0] == True:
            displaceImage = textureGenerator.image_invert(displaceImage)
        return displaceImage

    def main(directory, name, b_props, s_props, r_props, a_props, d_props):
        baseImage = cv2.imread(directory)
        grayScale = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)
        grayScale = cv2.equalizeHist(grayScale)

        bumpImage = textureGenerator.bump(grayScale, b_props)
        specularImage = textureGenerator.specular(grayScale, s_props)
        roughnessImage = textureGenerator.roughness(grayScale, r_props)
        aoImage = textureGenerator.ambient(grayScale, a_props)
        displaceImage = textureGenerator.displacement(grayScale, d_props)
        
        image = [baseImage, grayScale, bumpImage, specularImage, roughnessImage, aoImage, displaceImage]
        imageType = ["Base", "GrayScale", "Bump", "Specular", "Roughness", "AO", "Displacement"]

        textureGenerator.saving(image, imageType, directory, name)

    def saving(image, imageType, directory, name):
        
        parent = os.path.dirname(directory)
        dstFolder = parent + '\\' + name + '\\'

        if os.path.exists(dstFolder):
            shutil.rmtree(dstFolder)
        os.makedirs(dstFolder)

        for i in range(len(image)):
            #cv2.imshow(imageType[i], cv2.resize(image[i], (300,300), image[i]))
            #print(directory+imageType[i])
            if os.path.exists(dstFolder + imageType[i] + ".jpg"):
                os.remove(imageType[i] + ".jpg")
            cv2.imwrite(dstFolder + imageType[i] + ".jpg", image[i])
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        nodeSetup.main(dstFolder, name)
