#version 450 core

layout (location = 0) in vec4 aPos;
layout (location = 1) in vec4 normal;

out vec4 normalCoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 normalView;

out mat4 modelViewProj;
void main(){
    
    modelViewProj = projection * view * model;

    gl_Position = modelViewProj * vec4(aPos.xyz, 1.0);
    // mat4 rotate = mat4(model[0], model[1], model[2], vec4(0, 0, 0, 1)) / determinant(model);
    mat4 trans = mat4(1.0f);
    trans[3] = view[3];
    normalCoords = normalize(normalView * model * normal);
}