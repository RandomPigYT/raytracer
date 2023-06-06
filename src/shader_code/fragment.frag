#version 450 core


out vec4 fragColour;
in vec2 tex;

uniform sampler2D ourTex;

void main(){

	fragColour = texture(ourTex, tex);
}
