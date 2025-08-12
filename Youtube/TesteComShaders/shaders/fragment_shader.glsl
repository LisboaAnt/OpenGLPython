#version 330 core
in vec2 fragTexCoord;
in vec3 fragNormal;
in vec3 fragColor;

out vec4 FragColor;

uniform sampler2D texture1;
uniform bool useTexture;

void main()
{
    if (useTexture) {
        FragColor = texture(texture1, fragTexCoord);
    } else {
        FragColor = vec4(fragColor, 1.0);
    }
}
