#version 430
in vec2 in_position;
in vec2 in_uv;
in float num;
out vec2 v_uv;
out float v_num;

void main()
{
    v_uv = in_uv;
    v_num = num;
    gl_Position = vec4(in_position, 0.0, 1.0);
}
