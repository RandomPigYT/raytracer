#include <math.h>

#include "../include/extension.h"
#include "c-vector/vec.h"

#define NUM_BUCKETS 12

struct bvhNodeInfo_t {
  int64_t left;
  int64_t right;
  int64_t parent;
  uint32_t* triangles;  // Vector
};

struct sceneInfo_t {
  struct vertex_t* verts;
  uint32_t numVerts;
};

enum axis_e { X_AXIS = 0, Y_AXIS = 1, Z_AXIS = 2 };

vec4* calcCentroids(struct sceneInfo_t* s) {
  struct vertex_t* verts = s->verts;
  uint32_t numVerts = s->numVerts;

  uint32_t numTris = numVerts / 3;

  vec4* centroids = malloc(numTris * sizeof(vec4));

  for (uint32_t i = 0; i < numTris; i++) {
    vec4 c;

    // Adds the three position vectors of the triangle and stores the result in
    // 'c'
    glm_vec4_add(verts[3 * i].position, verts[(3 * i) + 1].position, c);
    glm_vec4_add(c, verts[(3 * i) + 2].position, c);

    // Divides the result in 'c' by 3 and stores the reasult in the ith index of
    // 'centroids'
    glm_vec4_divs(c, 3.0f, centroids[i]);
  }

  return centroids;
}

vec4* getCorners(struct vertex_t* verts, uint32_t* triangles) {
  vec4 minCorner;
  vec4 maxCorner;

  for (int i = 0; i < vector_size(triangles); i++) {
  }
}

vec4* constructVolumes(struct sceneInfo_t* s, vec4* centroids,
                       struct bvh_t* parentNode,
                       struct bvhNodeInfo_t* parentInfo, uint32_t bucketIndex,
                       float bucketWidth, enum axis_e axis) {
  uint32_t* left = vector_create();
  uint32_t* right = vector_create();

  for (int i = 0; i < vector_size(parentInfo->triangles); i++) {
    if (centroids[parentInfo->triangles[i]][axis] <=
        parentNode->corner1[axis] + ((bucketIndex + 1) * bucketWidth))
      vector_add(&left, parentInfo->triangles[i]);

    else
      vector_add(&right, parentInfo->triangles[i]);
  }

  vector_free(left);
  vector_free(right);
}

vec4* optimalVolumeInAxis(float* cost, enum axis_e axis, struct sceneInfo_t* s,
                          vec4* centroids, struct bvh_t* parentNode,
                          struct bvhNodeInfo_t* parentInfo) {
  float bucketWidth =
      fabs(parentNode->corner1[axis] - parentNode->corner2[axis]) / NUM_BUCKETS;

  vec4* volumes;

  for (int32_t i = 0; i < NUM_BUCKETS; i++) {
  }
}

// Returns a pointer to an array which contains four coordinates, 0 and 1 being
// the ones that describe the first volume, and 2 and 3 being the ones that
// describe the second volume.
vec4* findOptimalVolumes(struct sceneInfo_t* s, vec4* centroids,
                         struct bvh_t* parentNode,
                         struct bvhNodeInfo_t* parentInfo) {}

void constructTree(struct bvh_t** b, struct bvhNodeInfo_t** bvhInfo,
                   struct sceneInfo_t* s, vec4* centroids, int64_t parent) {}

struct bvh_t* constructBvh(uint32_t* numBvh, struct vertex_t* verts,
                           uint32_t numVerts) {
  struct bvh_t* b = vector_create();
  struct bvhNodeInfo_t* bvhInfo = vector_create();

  struct sceneInfo_t s = {.verts = verts, .numVerts = numVerts};

  vec4* centroids = calcCentroids(&s);

  free(centroids);
  vector_free(bvhInfo);
  return b;
}
