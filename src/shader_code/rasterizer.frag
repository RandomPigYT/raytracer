#version 450 core

out vec4 fragColour;
in vec4 normalCoords;

uniform vec2 resolution;
uniform vec3 camPos;
uniform float fov;
uniform mat4 projection;
uniform mat4 view;

#define NEAR 0.1f
#define SCREEN_ORIGIN vec2(0, 0)

vec3 toneMap(vec3 x){
	float a = 2.51f;
	float b = 0.03f;
	float c = 2.43f;
	float d = 0.59f;
	float e = 0.14f;

	return clamp((x*(a*x+b))/(x*(c*x+d)+e), 0.0f, 1.0f);
}

vec3 gammaCorrect(vec3 x, float gamma){
	const float invGamma = 1 / gamma;
	return pow(x, vec3(invGamma));
}

void main(){
    float aspect = resolution[0] / resolution[1];

    vec3 baseColour = vec3(162.0f / 255.0f, 164.0f / 255.0f, 165.0f / 255.0f);

    vec4 ndc;
    ndc.xy = ((gl_FragCoord.xy / resolution) * 2.0f) - 1.0f;
    ndc.z = (2.0f * gl_FragCoord.z - gl_DepthRange.near - gl_DepthRange.far) / 
        (gl_DepthRange.far - gl_DepthRange.near);
    ndc.w = 1.0f;

    vec4 clipPos = ndc / gl_FragCoord.w;

    vec4 relativePos = inverse(projection) * clipPos;

    vec3 fragDir = normalize(relativePos.xyz);

    float multiplier = dot(-fragDir.xyz, -normalCoords.xyz);
    
    fragColour = vec4(baseColour * abs(multiplier), 1.0f);
    fragColour = vec4(toneMap(fragColour.rgb), 1.0f);

    fragColour = vec4(gammaCorrect(fragColour.rgb, 2.2), 1.0f);
}