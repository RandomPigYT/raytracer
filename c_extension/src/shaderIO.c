#include "../include/extension.h"
#include <stdio.h>


void sendToShader(struct vertex* vertices, struct material* materials,
                  struct mesh* meshes, struct object* objects,
                  struct argData_t argData) {

	
	for (int i = 0; i < argData.numMeshes; i++){
		
		printf("%ld %ld %ld %ld\n", meshes[i].startingVertex, meshes[i].numTriangles, meshes[i].materialID, meshes[i].objectID);
	}

}





