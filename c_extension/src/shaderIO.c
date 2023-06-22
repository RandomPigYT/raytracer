#include <stdio.h>

#include "../include/extension.h"

void sendToShader(vec3 cameraPos, vec3 cameraDir, struct vertex *vertices,
                  struct material *materials, struct mesh *meshes,
                  struct object *objects, struct argData_t argData,
									GLuint shaderProgram) {

  for (int i = 0; i < argData.numMeshes; i++) {
	
		printf("%f %f %f\n%f %f %f\n", cameraPos[0], cameraPos[1], cameraPos[2], cameraDir[0], cameraDir[1], cameraDir[2]);

    printf("%ld %ld %ld %ld\n", meshes[i].startingVertex,
           meshes[i].numTriangles, meshes[i].materialID, meshes[i].objectID);

		printf("program - %d\n", shaderProgram);
  }
}
