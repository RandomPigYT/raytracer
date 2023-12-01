#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "../include/extension.h"
#include "../include/fastBVHWrapper.h"
#include "c-vector/vec.h"

int main(void) {
  typedef struct vertex_t Vert;

  Vert* v = malloc(42 * sizeof(Vert));

  srand(time(NULL));

  float maxVal = 5.0f;
  float minVal = -5.0f;
  for (int i = 0; i < 42; i++) {
    v[i].position[0] =
        ((float)rand() / (float)RAND_MAX) * (maxVal - minVal) + minVal;
    v[i].position[1] =
        ((float)rand() / (float)RAND_MAX) * (maxVal - minVal) + minVal;
    v[i].position[2] =
        ((float)rand() / (float)RAND_MAX) * (maxVal - minVal) + minVal;
  }

  unsigned int numBvh;
  struct bvh_t* b = constructBvh(&numBvh, v, 42);

  cppTest();
}
