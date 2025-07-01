#version 330 core

out vec4 fragColor;

in vec2 uv;
in vec3 v_normal;
in vec3 v_fragPos;
in vec3 frag_color;

uniform sampler2D u_texture;
uniform vec3 light_position;
uniform vec3 light_color;
uniform vec3 camera_position;
uniform float ambient;
uniform float shininess;
uniform float gamma;

void main() {
    vec3 norm = normalize(v_normal);
    vec3 lightDir = normalize(light_position - v_fragPos);
    vec3 viewDir = normalize(camera_position - v_fragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 ambient = ambient * light_color;
    vec3 diffuse = diff * light_color;
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    vec3 specular = spec * light_color;
    vec3 lighting = (ambient + diffuse + specular) * frag_color;
    vec4 tex_color = texture(u_texture, uv);
    vec3 finalColor = pow(tex_color.rgb * lighting, vec3(1 / gamma));
    fragColor = vec4(finalColor, 1.0) * vec4(frag_color, 1.0);
}
