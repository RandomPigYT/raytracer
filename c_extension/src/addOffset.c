#include "../include/extension.h"
#include <stdio.h>
#include <stdbool.h>




void* addOffset(void* ptr, uint64_t n, uint64_t size, int8_t sign){


	
	return (void*)((char*)ptr + (n * size * sign));
}
