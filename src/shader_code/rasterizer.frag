#version 450 core

out vec4 fragColour;
in vec4 normalCoords;



#define NEAR 0.1f

void main(){
    vec3 baseColour = vec3(162.0f / 255.0f, 164.0f / 255.0f, 165.0f / 255.0f);




    float multiplier = dot(vec3(0.0f, 0.0f, -1.0f), -normalCoords.xyz);
    // float multiplier = dot(-fragDir, -normalCoords.xyz);
    fragColour = vec4(baseColour * abs(multiplier), 1.0f);
}