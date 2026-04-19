from src.entities.block import Block
from src.render.render_methods import sort_chunks_by_distance
from src.chunk import Chunk
import os
import json
from math import floor
import pygame


class World:
    def __init__(self, play_scene):
        self.world_name = play_scene.world_name
        self.world_path = f'{os.getcwd()}/src/worlds/{self.world_name}'
        self.textures_path = f'{os.getcwd()}/src/resourcepack'
        self.load_settings()
        self.play_scene = play_scene

        self.chunks = []
        self.loaded_chunks_pos = []
        self.chunks_load()
        for chunk in self.chunks:
            chunk.make_polygons_mesh()
        self.textures = {}
        self.load_textures()

    def load_settings(self):
        with open(f'{self.world_path}/world_settings.json', 'r') as file:
            self.settings = json.load(file)
        self.world_max_y = self.settings['world_max_y']
        self.world_gravity = self.settings['gravity']

    def load_textures(self):
        for filename in os.listdir(self.textures_path):
            surface = pygame.image.load(f"{self.textures_path}/{filename}").convert()
            texture = []
            for texture_y in range(surface.get_height()):
                texture.append([])
                for texture_x in range(surface.get_width()):
                    texture[texture_y].append(surface.get_at((texture_x, texture_y)))

            self.textures[filename[:-4]] = texture

    def save_settings(self):
        with open(f'{self.world_path}/world_settings.json', 'w') as file:
            json.dump(self.settings, file, ensure_ascii=False, indent=4)

    def chunks_load(self):
        for name in os.listdir(f'{self.world_path}'):
            full_path = os.path.join(f'{self.world_path}', name)
            if os.path.isdir(full_path):
                print(f'load {name}')
                x, z = map(int, name.replace('chunk(', '').replace(')', '').split(','))
                if [x, z] in self.loaded_chunks_pos:
                    continue
                self.chunks.append(Chunk(self, x, z))
                self.loaded_chunks_pos.append([x, z])

    def get_block(self, x, y, z):
        chunk_x = x//16
        chunk_z = z//16
        chunk_block_x = x - 16*chunk_x
        chunk_block_y = floor(y)
        chunk_block_z = z - 16*chunk_z

        chunk = next((chunk for chunk in self.chunks if chunk.x == chunk_x and chunk.z == chunk_z), None)
        if not chunk:
            return

        blocks = chunk.blocks
        block = blocks[chunk_block_y][chunk_block_x][chunk_block_z]

        return block

    def get_block_id(self, x, y, z):
        block = self.get_block(x, y, z)
        if block:
            return self.get_block(x, y, z).id
        else:
            return

    # def save_world(self):

    def draw(self):
        chunks_sorted = sort_chunks_by_distance(self.chunks, [self.play_scene.player.x, self.play_scene.player.z])
        for chunk in chunks_sorted:
            chunk.draw()



# import os
#
# with open(f'{os.getcwd()}/worlds/testing_UV/chunk(0,0)/blocks.data', 'bw') as file:
#     for y in range(25):
#         for x in range(16):
#             for z in range(16):
#                 if x == 8 and y == 8 and z == 8:
#                     block = Block(None, 1, x, y, z)
#                 else:
#                     block = Block(None, 0, x, y, z)
#                 file.write(block.id.to_bytes(1))



# world = World(None)
#
# world.chunks_load()
