#version 450 core

layout (location = 0) in vec4 aPos;
layout (location = 1) in vec4 normal;

out vec4 normalCoords;
out vec4 v;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 normalView;
uniform vec3 camPos;

void main(){
    
    mat4 modelViewProj = projection * view * model;

    gl_Position = modelViewProj * vec4(aPos.xyz, 1.0);
    mat4 rotate = mat4(model[0], model[1], model[2], vec4(0, 0, 0, 1)) / determinant(model);


    normalCoords = normalize(view * rotate * normal);
}