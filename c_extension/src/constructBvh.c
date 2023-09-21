#include <float.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

#include "../include/extension.h"
#include "c-vector/vec.h"

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

enum side_e { LEFT, RIGHT };

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

float MIN(float x, float y) { return x < y ? x : y; }

float MAX(float x, float y) { return x > y ? x : y; }

float calcSurfaceArea(vec4* volume) {
  float l = volume[1][X_AXIS] - volume[0][X_AXIS];
  float b = volume[1][Y_AXIS] - volume[0][Y_AXIS];
  float h = volume[1][Y_AXIS] - volume[0][Z_AXIS];

  return 2 * ((l * b) + (b * h) + (l * h));
}

float calcCentroidSpan(vec4* centroids, uint32_t* triangles, enum axis_e axis) {
  float maxPos = -INFINITY;
  float minPos = INFINITY;

  for (uint32_t i = 0; i < vector_size(triangles); i++) {
    maxPos = MAX(maxPos, centroids[triangles[i]][axis]);
    minPos = MIN(minPos, centroids[triangles[i]][axis]);
  }

  float span = maxPos - minPos;

  return span;
}

vec4* getCorners(struct vertex_t* verts, uint32_t* triangles) {
  vec4 minCorner = {INFINITY, INFINITY, INFINITY, INFINITY};
  vec4 maxCorner = {-INFINITY, -INFINITY, -INFINITY, -INFINITY};

  for (uint32_t i = 0; i < vector_size(triangles); i++) {
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
    // triangle, and then sets it as the 'maxCorner' if it is greater than
    // 'maxCorner'
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
                       float bucketWidth, enum axis_e axis, uint32_t** leftTris,
                       uint32_t** rightTris) {
  uint32_t* left = vector_create();
  uint32_t* right = vector_create();

  for (uint32_t i = 0; i < vector_size(parentInfo->triangles); i++) {
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

  *leftTris = left;
  *rightTris = right;

  free(leftVolume);
  free(rightVolume);

  // vector_free(left);
  // vector_free(right);

  return volumes;
}

vec4* optimalVolumeInAxis(float* cost, enum axis_e axis, struct sceneInfo_t* s,
                          vec4* centroids, struct bvh_t* parentNode,
                          struct bvhNodeInfo_t* parentInfo, uint32_t** leftTris,
                          uint32_t** rightTris) {
  float centroidSpan = calcCentroidSpan(centroids, parentInfo->triangles, axis);

  uint32_t numBuckets =
      ceil(fabs(parentNode->corner2[axis] - parentNode->corner1[axis]) /
           (centroidSpan / 2));

  float bucketWidth =
      fabs(parentNode->corner2[axis] - parentNode->corner1[axis]) / numBuckets;

  vec4* volumes = NULL;
  float minCost = INFINITY;

  *leftTris = NULL;
  *rightTris = NULL;

  for (uint32_t i = 0; i < numBuckets; i++) {
    uint32_t* tempLeftTris;
    uint32_t* tempRightTris;

    vec4* v =
        constructVolumes(s, centroids, parentNode, parentInfo, i, bucketWidth,
                         axis, &tempLeftTris, &tempRightTris);

    vec4 leftVolume[2];
    vec4 rightVolume[2];
    memcpy(leftVolume, v, 2 * sizeof(vec4));
    memcpy(rightVolume, v + 2, 2 * sizeof(vec4));

    float leftSurfaceArea =
        vector_size(tempLeftTris) > 0 ? calcSurfaceArea(leftVolume) : INFINITY;
    float rightSurfaceArea = vector_size(tempRightTris) > 0
                                 ? calcSurfaceArea(rightVolume)
                                 : INFINITY;

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
        0.125f + ((float)vector_size(tempLeftTris) * p_a) +
        ((float)vector_size(tempRightTris) *
         p_b);  // C = t_trav + p_a * n * t_isect + p_b * n * t_isect

    if (tempCost < minCost) {
      minCost = tempCost;

      if (volumes != NULL) free(volumes);
      if (*leftTris != NULL) vector_free(*leftTris);
      if (*rightTris != NULL) vector_free(*rightTris);

      volumes = v;
      *leftTris = tempLeftTris;
      *rightTris = tempRightTris;
    }

    else {
      free(v);
      vector_free(tempLeftTris);
      vector_free(tempRightTris);
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
                         struct bvhNodeInfo_t* parentInfo, uint32_t** leftTris,
                         uint32_t** rightTris) {
  vec4* volumes = NULL;
  float minCost = INFINITY;

  *leftTris = NULL;
  *rightTris = NULL;

  for (int axis = 0; axis < 3; axis++) {
    uint32_t* tempLeftTris;
    uint32_t* tempRightTris;

    float tempCost;
    vec4* v = optimalVolumeInAxis(&tempCost, axis, s, centroids, parentNode,
                                  parentInfo, &tempLeftTris, &tempRightTris);

    if (tempCost < minCost) {
      if (volumes != NULL) free(volumes);
      if (*leftTris != NULL) vector_free(*leftTris);
      if (*rightTris != NULL) vector_free(*rightTris);

      minCost = tempCost;
      volumes = v;

      *leftTris = tempLeftTris;
      *rightTris = tempRightTris;
    }

    else {
      free(v);
      if (tempLeftTris != NULL) vector_free(tempLeftTris);
      if (tempRightTris != NULL) vector_free(tempRightTris);
    }
  }

  return volumes;
}

void assignHitMissIndices(struct bvh_t* b, struct bvhNodeInfo_t* bvhInfo,
                          int64_t nodeIndex, enum side_e side) {
  // If last node in array
  if (nodeIndex == vector_size(b) - 1) {
    b[nodeIndex].hitIndex = -1;
    b[nodeIndex].missIndex = -1;

    return;
  }

  /* Hit index */
  b[nodeIndex].hitIndex = nodeIndex + 1;

  /* Miss index */
  // If leaf node
  if (bvhInfo[nodeIndex].left == -1 && bvhInfo[nodeIndex].right == -1) {
    b[nodeIndex].missIndex = nodeIndex + 1;
    return;
  }

  // If root node
  if (bvhInfo[nodeIndex].parent == -1) b[nodeIndex].missIndex = -1;

  // If internal left node
  else if (side == LEFT)
    b[nodeIndex].missIndex =
        bvhInfo[bvhInfo[nodeIndex].parent].right;  // sibling node

  // If internal right node
  else {
    b[nodeIndex].missIndex = -1;

    // Search until a super-node is the left sibling of another node
    int64_t parent = bvhInfo[nodeIndex].parent;
    while (parent != -1) {
			printf("%ld\n", parent);
      int64_t grandparent = bvhInfo[parent].parent;

      if (bvhInfo[grandparent].right != parent) {
        b[nodeIndex].missIndex = bvhInfo[grandparent].right;
        break;
      }

      parent = grandparent;
    }
  }


  assignHitMissIndices(b, bvhInfo, bvhInfo[nodeIndex].left, LEFT);
  assignHitMissIndices(b, bvhInfo, bvhInfo[nodeIndex].right, RIGHT);
}

void constructTree(struct bvh_t** b, struct bvhNodeInfo_t** bvhInfo,
                   struct sceneInfo_t* s, vec4* centroids) {
  uint32_t nodeIndex = vector_size(*b) - 1;
  uint32_t numTris = vector_size((*bvhInfo)[nodeIndex].triangles);

  if (numTris <= 4) {
    (*b)[nodeIndex].numTris = numTris;
    memcpy((*b)[nodeIndex].triIndices, (*bvhInfo)[nodeIndex].triangles,
           numTris * sizeof(uint32_t));

    (*bvhInfo)[nodeIndex].left = -1;
    (*bvhInfo)[nodeIndex].right = -1;

    return;
  }

  uint32_t* leftTris;
  uint32_t* rightTris;

  vec4* volumes =
      findOptimalVolumes(s, centroids, &(*b)[nodeIndex], &(*bvhInfo)[nodeIndex],
                         &leftTris, &rightTris);

  // Left node
  struct bvh_t* leftNodeRef = vector_add_asg(b);
  struct bvhNodeInfo_t* leftNodeInfoRef = vector_add_asg(bvhInfo);

  leftNodeInfoRef->parent = nodeIndex;
  leftNodeInfoRef->triangles = leftTris;

  memcpy(leftNodeRef->corner1, volumes, sizeof(vec4));
  memcpy(leftNodeRef->corner2, volumes + 1, sizeof(vec4));

  (*bvhInfo)[nodeIndex].left = vector_size(*b) - 1;

  leftNodeRef->numTris = 0;

  constructTree(b, bvhInfo, s, centroids);

  // Right node
  struct bvh_t* rightNodeRef = vector_add_asg(b);
  struct bvhNodeInfo_t* rightNodeInfoRef = vector_add_asg(bvhInfo);

  rightNodeInfoRef->parent = nodeIndex;
  rightNodeInfoRef->triangles = rightTris;

  memcpy(rightNodeRef->corner1, volumes + 2, sizeof(vec4));
  memcpy(rightNodeRef->corner2, volumes + 3, sizeof(vec4));

  (*bvhInfo)[nodeIndex].right = vector_size(*b) - 1;

  rightNodeRef->numTris = 0;

  constructTree(b, bvhInfo, s, centroids);

  free(volumes);
}

void cleanBvhInfo(struct bvhNodeInfo_t* bvhInfo) {
  for (uint32_t i = 0; i < vector_size(bvhInfo); i++) {
    vector_free(bvhInfo[i].triangles);
  }
}

int freeBvh(struct bvh_t* volumes) {
  vector_free(volumes);
  return 1;
}

struct bvh_t* constructBvh(uint32_t* numBvh, struct vertex_t* verts,
                           uint32_t numVerts) {
  struct bvh_t* b = vector_create();
  struct bvhNodeInfo_t* bvhInfo = vector_create();

  struct sceneInfo_t s = {.verts = verts, .numVerts = numVerts};

  vec4* centroids = calcCentroids(&s);

  struct bvhNodeInfo_t* startNodeInfoRef = vector_add_asg(&bvhInfo);
  startNodeInfoRef->parent = -1;
  startNodeInfoRef->triangles = vector_create();

  // Generates an array with indices from 0 to the number of triangles minus one
  for (uint32_t i = 0; i < numVerts / 3; i++) {
    vector_add(&(startNodeInfoRef->triangles), i);
  }

  struct bvh_t* startNodeRef = vector_add_asg(&b);

  vec4* corners = getCorners(verts, startNodeInfoRef->triangles);
  memcpy(startNodeRef->corner1, corners, sizeof(vec4));
  memcpy(startNodeRef->corner2, corners + 1, sizeof(vec4));
  free(corners);

  startNodeRef->numTris = 0;

  constructTree(&b, &bvhInfo, &s, centroids);
  assignHitMissIndices(b, bvhInfo, 0, LEFT);

  free(centroids);

  cleanBvhInfo(bvhInfo);
  vector_free(bvhInfo);

  *numBvh = vector_size(b);

	
//for (int i = 0; i < vector_size(b); i++){
//	printf("%d %d\n", b[i].hitIndex, b[i].missIndex);
//}
	

  return b;
}
