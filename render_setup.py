import moderngl
import pygame
from settings import screen_size


def set_uniform(u_name, u_value):
    try:
        program[u_name] = u_value
    except KeyError:
        print(f'uniform: {u_name} - not used in shader')


def get_shader_program(name):
    with open(f"shaders/{name}.vert") as file:
        vertex_shader = file.read()
    with open(f"shaders/{name}.frag") as file:
        fragment_shader = file.read()
    shader_program = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
    return shader_program


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode(screen_size, flags=pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN)

ctx = moderngl.create_context()

ctx.enable(int(moderngl.BLEND))

program = get_shader_program("default")

set_uniform('u_texture', 1)
set_uniform('u_texture2', 2)
set_uniform('u_texture3', 3)
set_uniform("u_texture4", 4)
set_uniform("u_texture5", 5)
set_uniform("u_texture6", 6)

