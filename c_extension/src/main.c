#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#include "../include/extension.h"


int main(void){
	
	typedef struct vertex_t Vert;

	Vert v[51];

	srand(time(NULL));

	float maxVal = 5.0f;
	float minVal = -5.0f;
	for (int i = 0; i < 51; i++){
		v[i].position[0] = ((float)rand() / (float)RAND_MAX) * (maxVal - minVal) + minVal;
		v[i].position[1] = ((float)rand() / (float)RAND_MAX) * (maxVal - minVal) + minVal;
		v[i].position[2] = ((float)rand() / (float)RAND_MAX) * (maxVal - minVal) + minVal;

		printf("%f %f %f\n", v[i].position[0], v[i].position[1], v[i].position[2]);

	}

	unsigned int numBvh;

	struct bvh_t* b = constructBvh(&numBvh, v, 51);

	for (int i = 0; i < numBvh; i++){
		printf("%d\n", b[i].numTris);
	}

}
