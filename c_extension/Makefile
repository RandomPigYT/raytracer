CC:=gcc
CPP:=g++
LD:=ld

CFLAGS:=-Wall -Wextra -g -std=gnu17 -O2
LDFLAGS:=-lm -I./include/Fast-BVH/include -lstdc++
INCLUDEFLAGS:=-I./include/Fast-BVH/include
CPPFLAGS:=-Wall -Wextra -g -std=c++17 -O2

WINFLAGS:=-L/usr/x86_64-mingw32/bin/cglm.dll -I./include/Fast-BVH/include -lstdc++

PLATFORM:=linux


BIN:=bin
OBJ:=obj
SRC:=src
INCLUDE:=include
LIB:=lib

TARGET:=$(BIN)/PigEngine.out
LIBTARGET:=$(LIB)/extension.so

ifeq ($(PLATFORM), windows)
 	LDFLAGS = $(WINFLAGS)
	LIBTARGET = $(LIB)/extension.dll
	CC = x86_64-w64-mingw32-gcc
	CPP = x86_64-w64-mingw32-g++
endif

SRCS:=$(shell find $(SRC) -type  f -name "*.c")
CPPSRCS:=$(shell find $(SRC) -type f -name "*.cpp")
OBJS:=$(patsubst $(SRC)/%.c, $(OBJ)/%.o, $(SRCS))
CPPOBJS:=$(patsubst $(SRC)/%.cpp, $(OBJ)/%.o, $(CPPSRCS))
INCLUDES:=$(shell find $(INCLUDE) -type f -name "*.h")

DIRS:=$(patsubst $(SRC)/%, $(OBJ)/%, $(shell find $(SRC)/ -mindepth 1 -type d))

CREATE_DIR_COMMAND:=./dirs.sh

.PHONY: all clean dirs library

all: dirs $(TARGET)
	
lib: $(LIBTARGET)

$(TARGET): $(OBJS) $(CPPOBJS)
	$(CPP) $(CPPFLAGS) $(OBJS) $(CPPOBJS) -o $@ $(INCLUDEFLAGS)

$(LIBTARGET): $(SRCS) $(CPPSRCS)
	$(CC) $(CFLAGS) -fPIC -shared -o $@ $^ $(LDFLAGS) 

$(OBJ)/%.o: $(SRC)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

$(OBJ)/%.o: $(SRC)/%.cpp
	$(CPP) $(CPPFLAGS) -c $< -o $@ $(INCLUDEFLAGS)

dirs:
	@$(CREATE_DIR_COMMAND) $(DIRS)

clean:
	-@rm -rf $(OBJ)/*
	-@rm -rf $(BIN)/*
	-@rm -rf $(LIB)/*

run: $(TARGET)
	@./$(TARGET)

VAL_OUT:=valgrind-out.txt

valgrind:
	@valgrind --leak-check=full \
         --show-leak-kinds=all \
         --track-origins=yes \
         --verbose \
         --log-file=$(VAL_OUT)\
         ./$(TARGET) car.obj

format:
	@clang-format $(SRCS) $(INCLUDES) --style=Google -i

