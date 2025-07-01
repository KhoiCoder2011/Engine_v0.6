#version 330 core

in vec2 frag_texcoord;
out vec4 color;
uniform sampler2D texture0;
uniform float alpha;

void main() {
    color = texture(texture0, frag_texcoord) * alpha;
}