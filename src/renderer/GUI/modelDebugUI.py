import imgui
import sceneManager as sm
import numpy as np
from glfw.GLFW import *
import ctypes as ct

def radius(sphere, sphereNum, window):
    status, newRadius = imgui.drag_float("Radius " + str(sphereNum), sphere.radius, format="%.2f", change_speed=0.01)
    if status:
        sphere.radius = newRadius

    sm.currentScene.resetFrame()


def position(sphere, sphereNum, window):
    
    status, pos = imgui.drag_float3("Position" + str(sphereNum),
                                                sphere.position[0], sphere.position[1], sphere.position[2], 
                                                0.01, format="%.2f")
    if status:
        sphere.position = (*pos, 0)
    sm.currentScene.resetFrame()

def material(materialID, sphereNum):
    

    status, albedo = imgui.color_edit3("albedo " + str(sphereNum), *sm.currentScene.materials[materialID].albedo)
    if status:
        sm.currentScene.materials[materialID].albedo = (*albedo, 1)


    status, emission = imgui.color_edit3("emission " + str(sphereNum), *sm.currentScene.materials[materialID].emission)
    if status:
        sm.currentScene.materials[materialID].emission = (*emission, 1)


    status, intensity = imgui.drag_float3("intensity " + str(sphereNum),
                                          *(sm.currentScene.materials[materialID].intensity[:-1]),
                                          0.01, format="%0.2f")
    if status:
        sm.currentScene.materials[materialID].intensity = (*intensity, 1)
    

    status, ref = imgui.drag_float3("refractive index " + str(sphereNum), 
                                      *(sm.currentScene.materials[materialID].refractiveIndex[:-1]),
                                      0.001, format="%0.3f")
    if status:
        sm.currentScene.materials[materialID].refractiveIndex = ref


    status, roughness = imgui.drag_float2("roughness " + str(sphereNum), 
                                      *sm.currentScene.materials[materialID].roughness,
                                      0.001, format="%0.3f",
                                      min_value=0, max_value=1)
    if status:
        sm.currentScene.materials[materialID].roughness = roughness

    status, metallic = imgui.drag_float("metallic " + str(sphereNum),
                                           sm.currentScene.materials[materialID].metallic,
                                           0.001, format="%0.3f",
                                           min_value=0, max_value=1)
    if status:
        sm.currentScene.materials[materialID].metallic = metallic

    status, reflectance = imgui.drag_float("reflectance " + str(sphereNum),
                                           sm.currentScene.materials[materialID].reflectance,
                                           0.001, format="%0.3f",
                                           min_value=0, max_value=1)
    if status:
        sm.currentScene.materials[materialID].reflectance = reflectance
    sm.currentScene.resetFrame()



def drawSphereUI(window):

    
    imgui.begin("Spheres")

    sphereIndex = 0
    for i in sm.currentScene.spheres:
        imgui.text("Sphere " + str(sphereIndex + 1))
        radius(i, sphereIndex + 1, window)
        position(i, sphereIndex + 1, window)
        material(i.materialID, sphereIndex + 1)
        
        sphereIndex += 1

    sm.currentScene.sendSpheresToShader()

    imgui.end()