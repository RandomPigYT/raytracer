#version 450 core


out vec4 fragColour;
in vec2 texCoords;

uniform sampler2D tex;

void main(){
	
	vec3 texCol = texture(tex, texCoords).rgb;
	fragColour = vec4(texCol, 1.0);
}
