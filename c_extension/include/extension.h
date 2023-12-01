#ifndef RAYTRACE_EXTENSION_H
#define RAYTRACE_EXTENSION_H

#include <cglm/cglm.h>
#include <stdint.h>

struct vertex_t {
  vec4 position;

  vec4 normal;

  vec2 textureCoord;

  vec2 padding2;
};

struct face_t {
  int32_t v_index;
  int32_t vt_index;
  int32_t vn_index;
};

struct bvh_t {
  vec4 corner1;
  vec4 corner2;
  int32_t hitIndex;
  int32_t missIndex;
  uint32_t numTris;
  uint32_t triIndices[4];
  int32_t padding0;
};

void* addOffset(void* ptr, uint64_t n, uint64_t size, int8_t sign);
void generateVerts(struct vertex_t** outVecBuf, float* v, float* vn, float* vt,
                   struct face_t* faces, uint32_t numFaces, uint32_t offset);

#ifdef __cplusplus
extern "C" {
#endif

struct bvh_t* constructBvh(uint32_t* numBvh, struct vertex_t* verts,
                           uint32_t numVerts);

int freeBvh(struct bvh_t* volumes);

#ifdef  __cplusplus
}
#endif


#endif
