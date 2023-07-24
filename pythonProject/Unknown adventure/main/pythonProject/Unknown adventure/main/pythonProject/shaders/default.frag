#version 430
out vec4 fragColor;
uniform sampler2D u_texture;
uniform sampler2D u_texture2;
uniform sampler2D u_texture3;
uniform sampler2D u_texture4;
uniform sampler2D u_texture5;
uniform sampler2D u_texture6;
in vec2 v_uv;
in float v_num;
in float v_dark;
vec4 color;
float dark_pic = 0.25;
float blue_cnt = 0.1;
void main() {
    switch (int(v_num)) {
    case 1:
        color = texture(u_texture, vec2(v_uv[0], -v_uv[1]));
        fragColor = vec4(color[0] - v_dark - dark_pic, color[1] - v_dark - dark_pic, color[2] - v_dark - dark_pic + blue_cnt, color[3]);
        break;
    case 2:
        color = texture(u_texture2, vec2(v_uv[0], -v_uv[1]));
        fragColor = vec4(color[0] - v_dark - dark_pic, color[1] - v_dark - dark_pic, color[2] - v_dark - dark_pic + blue_cnt, color[3]);
        break;  
    case 3:
        color = texture(u_texture3, vec2(v_uv[0], -v_uv[1]));
        fragColor = vec4(color[0] - v_dark - dark_pic, color[1] - v_dark - dark_pic, color[2] - v_dark - dark_pic + blue_cnt, color[3]);
        break;
    case 4:
        color = texture(u_texture4, vec2(v_uv[0], -v_uv[1]));
        fragColor = vec4(color[0] - v_dark - dark_pic, color[1] - v_dark - dark_pic, color[2] - v_dark - dark_pic + blue_cnt, color[3]);
        break;
    case 5:
        color = texture(u_texture5, vec2(v_uv[0], -v_uv[1]));
        fragColor = vec4(color[0] - v_dark - dark_pic, color[1] - v_dark - dark_pic, color[2] - v_dark - dark_pic + blue_cnt, color[3]);
        break;    
    case 6:
        color = texture(u_texture6, vec2(v_uv[0], -v_uv[1]));
        fragColor = vec4(color[0] - v_dark - dark_pic, color[1] - v_dark - dark_pic, color[2] - v_dark - dark_pic + blue_cnt, color[3]);
        break;    
    case 7:
        fragColor = texture(u_texture5, vec2(v_uv[0], -v_uv[1])); 
        break;    
    case 8:
        fragColor = texture(u_texture5, vec2(v_uv[0], -v_uv[1])); 
        break;    
    case 9:
        fragColor = texture(u_texture5, vec2(v_uv[0], -v_uv[1])); 
        break;    
    case 10:
        fragColor = texture(u_texture5, vec2(v_uv[0], -v_uv[1])); 
        break;
    case 11:
        fragColor = texture(u_texture5, vec2(v_uv[0], -v_uv[1])); 
        break;    
    case 12:
        fragColor = texture(u_texture5, vec2(v_uv[0], -v_uv[1])); 
        break;    
    case 13:
        fragColor = texture(u_texture5, vec2(v_uv[0], -v_uv[1])); 
        break;    
    case 14:
        fragColor = texture(u_texture5, vec2(v_uv[0], -v_uv[1])); 
        break;    
    case 15:
        fragColor = texture(u_texture5, vec2(v_uv[0], -v_uv[1])); 
        break;    
    case 16:
        fragColor = texture(u_texture5, vec2(v_uv[0], -v_uv[1])); 
        break;    
    }
}
