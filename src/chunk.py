import os
from src.entities.block import Block
from src.render.render_methods import chunk_polygons_render
from src.render.split_block_on_polygons import split_block_on_polygons


class Chunk:
    def __init__(self, world, x, z):
        self.world = world
        self.x = x
        self.z = z
        self.blocks = []
        self.polygons_mesh = []

        self.load_blocks()

    def load_blocks(self):
        with open(f'{os.getcwd()}/src/worlds/{self.world.world_name}/chunk({self.x},{self.z})/blocks.data', 'br') as file:
            for y in range(self.world.world_max_y):
                self.blocks.append([])
                for x in range(16):
                    self.blocks[y].append([])
                    for z in range(16):
                        data = file.read(1)
                        block_id = int.from_bytes(data, byteorder='big')
                        self.blocks[y][x].append(Block(self, block_id, x, y, z))

    def make_polygons_mesh(self):
        for y in range(self.world.world_max_y):
            for x in range(16):
                for z in range(16):
                    if self.blocks[y][x][z].id == 0:
                        continue
                    polygons_list = split_block_on_polygons(self.blocks[y][x][z])
                    for polygon in polygons_list:
                        self.polygons_mesh.append(polygon)

    def draw(self):
        chunk_polygons_render(self, self.polygons_mesh)

