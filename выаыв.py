import moderngl
import pygame
import numpy


# класс который отслеживает и выполняет внутриигровые события. События отправляются классу например при взаимодействии с челом.
# Отправляеся сама функция и аргументы (персонаж который использует функцию и цель). Класс событий выполняет ивенты постоянно.
# Ивенты возвращают 1, если активны, или 0, если закончились, тогда класс их удаляет из себя.
# Ивенты челов, когда заканчиваются, вызывают interaction() персонажа, который и вызвал этот ивент


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


def convert_vertex(pt, surface_size):
    return pt[0] / surface_size[0] * 2 - 1, 1 - pt[1] / surface_size[1] * 2


def get_object_verts(rect, image_pos, source, window_size):
    vert1 = convert_vertex((rect[0], rect[1]), window_size)
    vert2 = convert_vertex((rect[0] + rect[2], rect[1]), window_size)
    vert3 = convert_vertex((rect[0] + rect[2], rect[1] + rect[3]), window_size)
    vert4 = convert_vertex((rect[0], rect[1] + rect[3]), window_size)
    img_vert1 = image_pos[0], image_pos[1]
    img_vert2 = image_pos[2], image_pos[1]
    img_vert3 = image_pos[2], image_pos[3]
    img_vert4 = image_pos[0], image_pos[3]
    return (*vert1, *img_vert1, source, *vert2, *img_vert2, source, *vert3, *img_vert3, source,
            *vert1, *img_vert1, source, *vert3, *img_vert3, source, *vert4, *img_vert4, source)


def draw(vertices):
    vertices = numpy.array(vertices, dtype='f4').tobytes()
    buffer = ctx.buffer(vertices)
    vao = ctx.vertex_array(program, [(buffer, "2f4 2f4 f4", "in_position", "in_uv", "num")])
    vao.render()
    buffer.release()
    vao.release()



def load_texture(image, location):
    dirt_bytes = pygame.image.tostring(image, 'RGBA', False)
    texture = ctx.texture(image.get_size(), 4, bytes(dirt_bytes))
    texture.use(location=location)
    return texture

def convert_texture_pos(texture_pos):
    vert1 = texture_pos[0] / 6400, 1 - texture_pos[1] / 6400
    vert2 = (texture_pos[0] + texture_pos[2]) / 6400, 1 - (texture_pos[1] + texture_pos[3]) / 6400
    return *vert1, *vert2


pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

screen = pygame.display.set_mode((1920, 1016), pygame.DOUBLEBUF | pygame.OPENGL)

ctx = moderngl.create_context()
ctx.enable(moderngl.BLEND)
program = get_shader_program("default2")

running = True
# test_char = characters.sprites()[1]
clock = pygame.time.Clock()

pos = 560, 440
radius = 100

point = [convert_vertex(pos, screen_size)]
print(point)


set_uniform('u_texture', 1)
image = pygame.image.load("test.png").convert_alpha()
load_texture(image, 1)

texture_pos = convert_texture_pos(image.get_rect())

verts = get_object_verts(pygame.Rect(0, 0, 6400, 6400), texture_pos, 1, screen_size)
print(verts)

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
    ctx.clear(0, 0, 0, 1)
    draw(verts)
    pygame.display.flip()
    clock.tick(60)
