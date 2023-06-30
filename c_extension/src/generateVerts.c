#include "../include/extension.h"
#include <stdlib.h>


void generateVerts(struct vertex_t** outVecBuf, float* v, float* vn, float* vt, 
										struct face_t* faces, uint32_t numFaces, uint32_t offset){

	for (uint32_t i = 0; i < numFaces; i++){

		(*outVecBuf)[i + offset].position[0] = v[faces[i].v_index * 3];
		(*outVecBuf)[i + offset].position[1] = v[(faces[i].v_index * 3) + 1];
		(*outVecBuf)[i + offset].position[2] = v[(faces[i].v_index * 3) + 2];
	
		if (faces[i].vt_index >= 0){
			(*outVecBuf)[i + offset].textureCoord[0] = vt[(faces[i].vt_index * 2)];
			(*outVecBuf)[i + offset].textureCoord[1] = vt[(faces[i].vt_index * 2) + 1];
		}
		
		if (faces[i].vn_index >= 0){
			(*outVecBuf)[i + offset].normal[0] = vn[(faces[i].vn_index * 3)];
			(*outVecBuf)[i + offset].normal[1] = vn[(faces[i].vn_index * 3) + 1];
			(*outVecBuf)[i + offset].normal[2] = vn[(faces[i].vn_index * 3) + 2];
		}

	}
	
}
