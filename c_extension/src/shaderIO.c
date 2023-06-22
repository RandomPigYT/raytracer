#include <stdio.h>

#include "../include/extension.h"

void sendToShader(struct SceneData scene, struct argData args) {

    printf("cameraPos %f %f %f\ncameraDir %f %f %f\n", scene.cameraPos[0], scene.cameraPos[1],
           scene.cameraPos[2], scene.cameraDir[0], scene.cameraDir[1],
           scene.cameraDir[2]);
    printf("program - %d\n", scene.shaderProgram);
  for (int i = 0; i < args.numMeshes; i++) {

    printf("%ld %ld %ld %ld\n", scene.meshes[i].startingVertex,
           scene.meshes[i].numTriangles, scene.meshes[i].materialID,
           scene.meshes[i].objectID);

  }
}
