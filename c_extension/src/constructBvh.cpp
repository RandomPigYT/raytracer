#include <FastBVH.h>
#include <iostream>

#include "../include/extension.h"

template <typename T>
T MAX(T a, T b){ return a > b ? a : b; }

template <typename T>
T MIN( T a, T b){ return a < b ? a : b; }

struct triangle_t {
	uint32_t id;
	struct vertex_t* verts;

	triangle_t(uint32_t id, vertex_t* verts){
		this->id = id;
		this->verts = verts;
	}
};


FastBVH::BBox<float> createBBox(const struct triangle_t& tri){
	FastBVH::Vector3<float> minPos;
	FastBVH::Vector3<float> maxPos;

	minPos[0] = MIN(tri.verts[0].position[0], tri.verts[1].position[0]);

	for (uint32_t i = 0; i < 3; i++){
		minPos[i] = MIN(tri.verts[0].position[i], tri.verts[1].position[i]);
		minPos[i] = MIN(minPos[i], tri.verts[2].position[i]);
	}

	for (uint32_t i = 0; i < 3; i++){
		maxPos[i] = MAX(tri.verts[0].position[i], tri.verts[1].position[i]);
		maxPos[i] = MAX(maxPos[i], tri.verts[2].position[i]);
	}

	return FastBVH::BBox<float>(minPos, maxPos);
}

void parseBvh(struct bvh_t* bvh, FastBVH::BVH<float, struct triangle_t>& rawBvh){


}


struct bvh_t* constructBvh(uint32_t* numBvh, struct vertex_t* verts,
													 uint32_t numVerts){
	uint32_t numTris = numVerts / 3;

	std::vector<struct triangle_t> tris;

	for (uint32_t i = 0; i < numTris; i++){
		struct triangle_t t = triangle_t(i, verts + (3 * i));
		tris.push_back(t);
	}
	
	FastBVH::DefaultBuilder<float> builder;
	FastBVH::BVH<float, struct triangle_t> rawBvh = builder(tris, createBBox);

	*numBvh = rawBvh.getNodes().size();
	struct bvh_t* bvh = (struct bvh_t*)malloc(*numBvh * sizeof(struct bvh_t));

	parseBvh(bvh, rawBvh);
	

	
	return bvh;
}

int freeBvh(struct bvh_t *volumes){
	free(volumes);
	return 1;
}
