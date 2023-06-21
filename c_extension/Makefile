CC:=gcc
LD:=ld

CFLAGS:=-Wall -Wextra -g -std=gnu17 
LDFLAGS:=-L/usr/local/lib -lglfw -pthread -lGL -lrt -lXrandr -lXxf86vm -lXi -lXinerama -lX11

WINFLAGS:=-L/usr/i686-w64-mingw32/bin/glfw3.dll

BIN:=bin
OBJ:=obj
SRC:=src
INCLUDE:=include
LIB:=lib

TARGET:=$(BIN)/PigEngine.out
LIBTARGET:=$(LIB)/extension.so

SRCS:=$(shell find $(SRC) -type  f -name "*.c")
OBJS:=$(patsubst $(SRC)/%.c, $(OBJ)/%.o, $(SRCS))
INCLUDES:=$(shell find $(INCLUDE) -type f -name "*.h")

DIRS:=$(patsubst $(SRC)/%, $(OBJ)/%, $(shell find $(SRC)/ -mindepth 1 -type d))

CREATE_DIR_COMMAND:=./dirs.sh

.PHONY: all clean dirs library

all: dirs $(TARGET)

library: $(LIBTARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $@ $(LDFLAGS)

$(LIBTARGET): $(SRCS)
	$(CC) $(CFLAGS) -fPIC -shared -o $@ $^ $(LDFLAGS)

$(OBJ)/%.o: $(SRC)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

dirs:
	@$(CREATE_DIR_COMMAND) $(DIRS)

clean:
	-@rm -rf $(OBJ)/*
	-@rm -rf $(BIN)/*

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

