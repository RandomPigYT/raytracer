#version 430 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in int lol;

void main() {
	


		gl_Position = vec4(aPos.x + lol, aPos.y + lol, aPos.z, 1.0);


}
