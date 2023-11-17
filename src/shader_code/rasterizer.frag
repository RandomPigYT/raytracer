#version 450 core

out vec4 fragColour;
in vec4 normalCoords;
void main(){

    fragColour = vec4(-normalCoords.xyz, 1.0f);
}