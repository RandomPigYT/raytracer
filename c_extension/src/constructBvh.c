#include "../include/extension.h"
#include "c-vector/vec.h"

struct bvhNodeInfo_t {
  int32_t left;
  int32_t right;
  int32_t parent;
};


vec4* calcCentroids(struct vertex_t* verts, uint32_t numVerts) {
	uint32_t numTris = numVerts / 3;

	vec4* centroids = malloc(numTris * sizeof(vec4));

	
	for (uint32_t i = 0; i < numTris; i++){
		vec4 c;

		// Adds the three position vectors of the triangle and stores the result in 'c'
		glm_vec4_add(verts[3 * i].position, verts[(3 * i) + 1].position, c);
		glm_vec4_add(c, verts[(3 * i) + 2].position, c);

		// Divides the result in 'c' by 3 and stores the reasult in the ith index of 'centroids'
		glm_vec4_divs(c, 3.0f, centroids[i]);
	}
	


	return centroids;
}


struct bvh_t* constructBvh(uint32_t* numBvh, struct vertex_t* verts, uint32_t numVerts) {
  struct bvh_t* b = vector_create();
  struct bvhNodeInfo_t* bvhInfo = vector_create();

	vec4* centroids = calcCentroids(verts, numVerts);

	
	free(centroids);
  return b;
}
