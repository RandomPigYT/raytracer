import imgui
import sceneManager as sm
import numpy as np
from glfw.GLFW import *
import ctypes as ct

def radius(sphere, sphereNum, window):
    status, newRadius = imgui.drag_float("Radius " + str(sphereNum), sphere.radius, format="%f", change_speed=0.001)

    if status:
        sphere.radius = newRadius


def position(sphere, sphereNum, window):
    
    status, pos = imgui.drag_float3("Position" + str(sphereNum),
                                                sphere.position[0], sphere.position[1], sphere.position[2], 
                                                0.01, format="%f")
    if status:
        sphere.position = (*pos, 0)

def material(sphere, sphereNum):
    

    status, kd = imgui.color_edit3("kd " + str(sphereNum), *sm.currentScene.materials[sphere.materialID].kd)
    if status:
        sm.currentScene.materials[sphere.materialID].kd = (*kd, 1)

    status, ks = imgui.color_edit3("ks " + str(sphereNum), *sm.currentScene.materials[sphere.materialID].ks)
    if status:
        sm.currentScene.materials[sphere.materialID].ks = (*ks, 1)

    status, emission = imgui.color_edit3("emission " + str(sphereNum), *sm.currentScene.materials[sphere.materialID].emission)
    if status:
        sm.currentScene.materials[sphere.materialID].emission = (*emission, 1)


    status, intensity = imgui.drag_float3("intensity " + str(sphereNum),
                                          *(sm.currentScene.materials[sphere.materialID].intensity[:-1]),
                                          0.01, format="%0.2f")
    if status:
        sm.currentScene.materials[sphere.materialID].intensity = (*intensity, 1)
    
    status, alpha = imgui.drag_float2("alpha " + str(sphereNum), 
                                      *sm.currentScene.materials[sphere.materialID].alpha,
                                      0.001, format="%0.3f",
                                      min_value=0, max_value=1)
    if status:
        sm.currentScene.materials[sphere.materialID].alpha = alpha

    status, metallicity = imgui.drag_float("metallicity " + str(sphereNum),
                                           sm.currentScene.materials[sphere.materialID].metallicity,
                                           0.001, format="%0.3f",
                                           min_value=0, max_value=1)

    if status:
        sm.currentScene.materials[sphere.materialID].metallicity = metallicity
    pass



def drawSphereUI(window):

    
    imgui.begin("Spheres")

    sphereIndex = 0
    for i in sm.currentScene.spheres:
        imgui.text("Sphere " + str(sphereIndex + 1))
        radius(i, sphereIndex + 1, window)
        position(i, sphereIndex + 1, window)
        material(i, sphereIndex + 1)
        
        sphereIndex += 1


    imgui.end()

    sm.currentScene.sendSpheresToShader()