#include <float.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

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

inline float MIN(float x, float y) { return x < y ? x : y; }

inline float MAX(float x, float y) { return x > y ? x : y; }

float calcSurfaceArea(vec4* volume) {
  float l = volume[1][X_AXIS] - volume[0][X_AXIS];
  float b = volume[1][Y_AXIS] - volume[0][Y_AXIS];
  float h = volume[1][Y_AXIS] - volume[0][Z_AXIS];

  return 2 * ((l * b) + (b * h) + (l * h));
}

vec4* getCorners(struct vertex_t* verts, uint32_t* triangles) {
  vec4 minCorner;
  vec4 maxCorner;

  for (int i = 0; i < vector_size(triangles); i++) {
    // Finds the smallest coordinates for each axis from the vertices of a
    // triangle, and then sets it as the 'minCorner' if it is lower than
    // 'minCorner'
    for (int j = 0; j < 3; j++) {
      float temp = MIN(verts[3 * triangles[i]].position[j],
                       verts[3 * triangles[i] + 1].position[j]);
      temp = MIN(temp, verts[3 * triangles[i] + 2].position[j]);

      minCorner[j] = MIN(minCorner[j], temp);
    }

    // Finds the largest coordinates for each axis from the vertices of a
    // triangle, and then sets it as the 'minCorner' if it is greater than
    // 'minCorner'
    for (int j = 0; j < 3; j++) {
      float temp = MAX(verts[3 * triangles[i]].position[j],
                       verts[3 * triangles[i] + 1].position[j]);
      temp = MAX(temp, verts[3 * triangles[i] + 2].position[j]);

      maxCorner[j] = MAX(maxCorner[j], temp);
    }
  }

  vec4* corners = malloc(2 * sizeof(vec4));

  memcpy(corners, minCorner, sizeof(vec4));
  memcpy(corners + 1, maxCorner, sizeof(vec4));

  return corners;
}

vec4* constructVolumes(struct sceneInfo_t* s, vec4* centroids,
                       struct bvh_t* parentNode,
                       struct bvhNodeInfo_t* parentInfo, uint32_t bucketIndex,
                       float bucketWidth, enum axis_e axis, uint32_t* numLeft,
                       uint32_t* numRight) {
  uint32_t* left = vector_create();
  uint32_t* right = vector_create();

  for (int i = 0; i < vector_size(parentInfo->triangles); i++) {
    if (centroids[parentInfo->triangles[i]][axis] <=
        parentNode->corner1[axis] + ((bucketIndex + 1) * bucketWidth))
      vector_add(&left, parentInfo->triangles[i]);

    else
      vector_add(&right, parentInfo->triangles[i]);
  }

  vec4* leftVolume = getCorners(s->verts, left);
  vec4* rightVolume = getCorners(s->verts, right);

  vec4* volumes = malloc(4 * sizeof(vec4));
  memcpy(volumes, leftVolume, 2 * sizeof(vec4));
  memcpy(volumes + 2, rightVolume, 2 * sizeof(vec4));

  *numLeft = vector_size(left);
  *numRight = vector_size(right);

  free(leftVolume);
  free(rightVolume);

  vector_free(left);
  vector_free(right);

  return volumes;
}

vec4* optimalVolumeInAxis(float* cost, enum axis_e axis, struct sceneInfo_t* s,
                          vec4* centroids, struct bvh_t* parentNode,
                          struct bvhNodeInfo_t* parentInfo) {
  float bucketWidth =
      fabs(parentNode->corner1[axis] - parentNode->corner2[axis]) / NUM_BUCKETS;

  vec4* volumes = NULL;
  float minCost = INFINITY;

  for (int32_t i = 0; i < NUM_BUCKETS; i++) {
    uint32_t numLeftTris;
    uint32_t numRightTris;

    vec4* v = constructVolumes(s, centroids, parentNode, parentInfo, i,
                               bucketWidth, axis, &numLeftTris, &numRightTris);

    vec4 leftVolume[2];
    vec4 rightVolume[2];
    memcpy(leftVolume, v, 2 * sizeof(vec4));
    memcpy(rightVolume, v + 2, 2 * sizeof(vec4));

    float leftSurfaceArea = calcSurfaceArea(leftVolume);
    float rightSurfaceArea = calcSurfaceArea(rightVolume);

    vec4 parentVolume[2];
    memcpy(parentVolume, parentNode->corner1, sizeof(vec4));
    memcpy(parentVolume + 1, parentNode->corner2, sizeof(vec4));

    float parentSurfaceArea = calcSurfaceArea(parentVolume);
    parentSurfaceArea = parentSurfaceArea > FLT_EPSILON
                            ? parentSurfaceArea
                            : FLT_EPSILON;  // To avoid division by 0

    float p_a = leftSurfaceArea / parentSurfaceArea;
    float p_b = rightSurfaceArea / parentSurfaceArea;

    float tempCost =
        0.125f + (numLeftTris * p_a) +
        (numRightTris *
         p_b);  // C = t_trav + p_a * n * t_isect + p_b * n * t_isect

    if (tempCost < minCost) {
      minCost = tempCost;

      if (volumes != NULL) free(volumes);

      volumes = v;
    }

    else {
      free(v);
    }
  }

  *cost = minCost;
  return volumes;
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
