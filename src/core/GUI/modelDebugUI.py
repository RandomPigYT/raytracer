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

def material(materialID, num):
    

    status, albedo = imgui.color_edit3("albedo " + str(num), *sm.currentScene.sceneRenderer.materials[materialID].albedo)
    if status:
        sm.currentScene.sceneRenderer.materials[materialID].albedo = (*albedo, 1)


    status, emission = imgui.color_edit3("emission " + str(num), *sm.currentScene.sceneRenderer.materials[materialID].emission)
    if status:
        sm.currentScene.sceneRenderer.materials[materialID].emission = (*emission, 1)


    status, intensity = imgui.drag_float3("intensity " + str(num),
                                          *(sm.currentScene.sceneRenderer.materials[materialID].intensity[:-1]),
                                          0.01, format="%0.2f")
    if status:
        sm.currentScene.sceneRenderer.materials[materialID].intensity = (*intensity, 1)
    

    status, ref = imgui.drag_float3("refractive index " + str(num), 
                                      *(sm.currentScene.sceneRenderer.materials[materialID].refractiveIndex[:-1]),
                                      0.001, format="%0.3f")
    if status:
        sm.currentScene.sceneRenderer.materials[materialID].refractiveIndex = ref


    status, roughness = imgui.drag_float2("roughness " + str(num), 
                                      *sm.currentScene.sceneRenderer.materials[materialID].roughness,
                                      0.001, format="%0.3f",
                                      min_value=0, max_value=1)
    if status:
        sm.currentScene.sceneRenderer.materials[materialID].roughness = roughness

    status, metallic = imgui.drag_float("metallic " + str(num),
                                           sm.currentScene.sceneRenderer.materials[materialID].metallic,
                                           0.001, format="%0.3f",
                                           min_value=0, max_value=1)
    if status:
        sm.currentScene.sceneRenderer.materials[materialID].metallic = metallic

    status, reflectance = imgui.drag_float("reflectance " + str(num),
                                           sm.currentScene.sceneRenderer.materials[materialID].reflectance,
                                           0.001, format="%0.3f",
                                           min_value=0, max_value=1)
    if status:
        sm.currentScene.sceneRenderer.materials[materialID].reflectance = reflectance
    sm.currentScene.resetFrame()


def meshPosition(mesh, meshNum):
    status, pos = imgui.drag_float3("Position" + str(meshNum),
                                                mesh.position[0], mesh.position[1], mesh.position[2], 
                                                0.01, format="%.2f")
    if status:
        mesh.position = (*pos, 0)
    sm.currentScene.resetFrame()



def drawModel(window):

    
    imgui.begin("Spheres")

    sphereIndex = 0
    for i in sm.currentScene.sceneRenderer.spheres:
        imgui.text("Sphere " + str(sphereIndex + 1))
        radius(i, sphereIndex + 1, window)
        position(i, sphereIndex + 1, window)
        material(i.materialID, sphereIndex + 1)
        
        sphereIndex += 1

    sm.currentScene.sendSpheresToShader()

    imgui.end()

    imgui.begin("Mesh")

    meshIndex = 0
    for i in sm.currentScene.sceneRenderer.meshes:
        imgui.text("Mesh " + str(meshIndex + 1))
        meshPosition(i, meshIndex + 1)
        material(i.materialID, meshIndex + 1)
        meshIndex += 1
    
    sm.currentScene.sendMeshes()
    sm.currentScene.sendMats()

        


    imgui.end()