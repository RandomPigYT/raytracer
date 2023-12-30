#version 450 core

out vec4 fragColour;
in vec2 texCoords;

uniform sampler2D tex;

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
	vec3 texCol = texture(tex, texCoords).rgb;
	texCol = toneMap(clamp(texCol, 0.0f, 10.0f));
	texCol = gammaCorrect(texCol, 2.2);
	fragColour = vec4(texCol, 1.0);
}
