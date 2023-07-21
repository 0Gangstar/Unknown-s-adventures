#version 430
out vec4 fragColor;
uniform sampler2D u_texture;
in vec2 v_uv;
in float v_num;
void main() {
    if (int(v_num) == 1) {
        fragColor = texture(u_texture, vec2(v_uv[0], -v_uv[1]));
    }
}
