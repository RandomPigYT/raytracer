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

using Node = FastBVH::ConstIterable<FastBVH::Node<float>>;

bool isInternalRight(Node nodes, uint32_t node, int64_t parent){
	if (parent < 0)
		return false;

	return parent + nodes[parent].right_offset == node;
}

bool isInternalLeft(Node nodes, uint32_t node, int64_t parent){
	if (parent < 0)
		return false;

	return parent + 1 == node;
}

int64_t findParentSibling(Node nodes, int64_t* parents, uint32_t node, int64_t parent){
	int64_t grandparent = parents[parent];
	while (grandparent != -1){
		if (grandparent + nodes[grandparent].right_offset != parent)
			return grandparent + nodes[grandparent].right_offset;
		
		parent = grandparent;
		grandparent = parents[grandparent];
	}
	
	return -1;
}

void parseBvh(struct bvh_t* bvh, FastBVH::BVH<float, struct triangle_t>& rawBvh){
	Node nodes = rawBvh.getNodes();
	auto primitives = rawBvh.getPrimitives();


	for (uint32_t i = 0; i < nodes.size(); i++){
		bvh[i].corner1[0] = nodes[i].bbox.min.x;
		bvh[i].corner1[1] = nodes[i].bbox.min.y;
		bvh[i].corner1[2] = nodes[i].bbox.min.z;

		bvh[i].corner2[0] = nodes[i].bbox.max.x;
		bvh[i].corner2[1] = nodes[i].bbox.max.y;
		bvh[i].corner2[2] = nodes[i].bbox.max.z;

		bvh[i].numTris = nodes[i].primitive_count;
		
		for (uint32_t j = 0; j < bvh[i].numTris; j++){
			bvh[i].triIndices[j] = primitives[nodes[i].start + j].id;
		}
	}


	int64_t* parents = (int64_t*)malloc(nodes.size() * sizeof(int64_t));

	parents[0] = -1;
	
	// Find the parents of the nodes
	for (uint32_t i = 0; i < nodes.size(); i++){
		if (nodes[i].isLeaf())
			continue;

		parents[i + 1] = i;
		parents[i + nodes[i].right_offset] = i;
	}


	// Assign hit and miss indices
	for (int i = 0; i < nodes.size(); i++){
		// Is last node
		if (i == nodes.size() - 1){
			bvh[i].hitIndex = -1;
			bvh[i].missIndex = -1;
			break;
		}
		
		bvh[i].hitIndex = i + 1;
		
		/* Miss indices */
		if (nodes[i].isLeaf()){
			bvh[i].missIndex = i + 1;
			continue;
		}

		// Is root node
		if (i == 0){
			bvh[i].missIndex = -1;
			continue;
		}

		if (isInternalLeft(nodes, i, parents[i])){
			bvh[i].missIndex = parents[i] + nodes[parents[i]].right_offset; // Sibling
			continue;
		}

		if (isInternalRight(nodes, i, parents[i]))
			bvh[i].missIndex = findParentSibling(nodes, parents, i, parents[i]);
	}


	free(parents);
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
