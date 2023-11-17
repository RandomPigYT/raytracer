#version 450 core

layout (location = 0) in vec4 aPos;
layout (location = 1) in vec4 normal;

out vec4 normalCoords;

void main(){

    gl_Position = vec4(aPos.xyz, 1.0);
    normalCoords = normal;

}