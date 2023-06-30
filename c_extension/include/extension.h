#ifndef RAYTRACE_EXTENSION_H
#define RAYTRACE_EXTENSION_H

#include <cglm/cglm.h>
#include <stdint.h>


struct vertex_t {
  vec3 position;

  float padding0;

  vec3 normal;

  float padding1;

  vec2 textureCoord;

  vec2 padding2;
};

struct face_t {
	
	int32_t v_index;
	int32_t vt_index;
	int32_t vn_index;

};


void* addOffset(void* ptr, uint64_t n, uint64_t size, int8_t sign);
void generateVerts(struct vertex_t** outVecBuf, float* v, float* vn, float* vt, 
										struct face_t* faces, uint32_t numFaces, uint32_t offset);

#endif
