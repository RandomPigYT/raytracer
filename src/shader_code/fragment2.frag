#version 450 core


out vec4 fragColour;
in vec2 texCoords;

// uniform sampler2D tex;

uniform vec2 resolution;

uniform vec3 cameraPos;
uniform vec3 cameraDir;

struct Vertex {
	
	vec4 position;
	vec4 normal;
	vec2 texelCoord;

};

layout (std430, binding = 0) buffer Verts{
	Vertex verts[];
};


vec2 testIntersect(Vertex v[3], vec3 rayOrigin, vec3 rayDir ){
	float epsilon = 0.0000001;

	vec3 positions[] = {v[0].position.xyz, v[1].position.xyz, v[2].position.xyz};

	
	
	vec3 edge1 = positions[1] - positions[0];
	vec3 edge2 = positions[2] - positions[0];

	vec3 cross_rayDir_edge2 = cross(rayDir, edge2);
	
	double det = dot(edge1, cross_rayDir_edge2);

	if (det > -epsilon && det < epsilon)
		return vec2(0, 0);

	double invDet = 1 / det;

	vec3 origMinusPos0 =  rayOrigin - positions[0];

	double baryU = dot(origMinusPos0, cross_rayDir_edge2) * invDet;
	if (baryU < 0.0 || baryU > 1.0)
		return vec2(0, 0);
	
	
	vec3 cross_oriMinusPos0_edge1 = cross(origMinusPos0, edge1);

	double baryV = dot(rayDir, cross_oriMinusPos0_edge1) * invDet;
	if (baryV < 0 || baryU + baryV > 1.0)
		return vec2(0, 0);
	
	double rayT;

	rayT = dot(edge2, cross_oriMinusPos0_edge1) * invDet;
	return vec2(1, rayT);
}



vec3 getRayDir(float fov /* in degrees */, float aspectRatio){
	
	
	vec2 texelCoord = gl_FragCoord.xy;

	

	vec2 ndc = vec2((texelCoord.x + 0.5) / float(resolution[0]), (texelCoord.y + 0.5) / float(resolution[1]));

	
	vec2 pixelCamera;
	pixelCamera.x = ((2 * ndc.x) - 1) * aspectRatio * tan(radians(fov / 2));
	pixelCamera.y = ((2 * ndc.y) - 1) * tan(radians(fov / 2));

	vec3 rayDir = vec3(pixelCamera, -1.0f);


	return rayDir;
}


void main(){
    
	vec4 colour = vec4(0, 0, 0, 1);
	// float aspectRatio = float(resolution[0]) / float(resolution[1]);
	float aspectRatio = 1920 / 1080;
	vec3 rayDir = getRayDir(90, aspectRatio);

	bool inter = false;
    for (int i = 0; i < verts.length(); i++){

		Vertex temp[] = {verts[i], verts[i + 1], verts[i + 2]};
		vec2 intersectResult = testIntersect(temp, cameraPos, rayDir);

		vec4 edge1 = verts[i + 1].position - verts[i].position;
		vec4 edge2 = verts[i + 2].position - verts[i].position;

		vec3 normal = normalize(cross(edge2.xyz, edge1.xyz));

		if (intersectResult[0] == 1){
			if (intersectResult[1] < 0)
				continue;

			colour = vec4(normal, 1);
			inter = true;
		}
		

    }
    
	if (inter)
		colour = vec4(1, 0, 0, 1);

    // vec3 texCol = texture(tex, texCoords).rgb;
    fragColour = vec4(colour);
}

