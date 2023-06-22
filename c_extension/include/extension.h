#ifndef RAYTRACE_EXTENSION_H
#define RAYTRACE_EXTENSION_H

#include <stdint.h>
#include <cglm/cglm.h>


struct vertex {
  vec3 position;
  float padding0;
  vec3 normal;
  float padding1;
  vec3 textureCoord;
  float padding2;
};

struct material {
  vec3 kd;
  float alpha_x;
  vec3 ks;
  float alpha_y;
  vec3 emission;
  float padding0;
};

struct mesh {
  uint64_t startingVertex;
  uint64_t numTriangles;
  uint64_t materialID;
  uint64_t objectID;
};

struct object {
  vec3 pos;
  uint32_t id;
};

struct argData_t {
  uint64_t numVertices;
  uint64_t numMaterials;
  uint64_t numMeshes;
  uint64_t numObjects;
};

#endif
