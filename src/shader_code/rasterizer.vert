#version 450 core

layout (location = 0) in vec4 aPos;
layout (location = 1) in vec4 normal;

out vec4 normalCoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main(){

    gl_Position = projection * view * model * vec4(aPos.xyz, 1.0);
    normalCoords = normal;
}