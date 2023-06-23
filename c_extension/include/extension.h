#ifndef RAYTRACE_EXTENSION_H
#define RAYTRACE_EXTENSION_H

#include <cglm/cglm.h>
#include <stdint.h>

void* addOffset(void* ptr, uint64_t n, uint64_t size, int8_t sign);

#endif
