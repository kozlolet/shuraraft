from src.entities.block import Block
from src.render.render_methods import sort_blocks_by_distance


class World:
    def __init__(self, play_scene):
        self.play_scene = play_scene

    def load_world(self):
        with open('src/world.shura', 'br') as file:
            blocks_bytes = file.read()

        blocks_int = int.from_bytes(blocks_bytes, byteorder='big')

        self.blocks = []
        while blocks_int:
            block = blocks_int & 0xffffffffffffff
            blocks_int = blocks_int >> 8*7

            block_z = block & 0xffff
            block >>= 16
            block_y = block & 0xffff
            block >>= 16
            block_x = block & 0xffff
            block >>= 16
            block_id = block & 0xff

            self.blocks.append(Block(self, block_id, block_x, block_y, block_z))

    def save_world(self):
        print('saving world...')
        with open('world.shura', 'bw') as file:
            for block in self.blocks:
                file.write(block.get_bytes())

    def draw(self):
        sorted_blocks = sort_blocks_by_distance(self.blocks, (self.play_scene.player.x, self.play_scene.player.y, self.play_scene.player.z))
        for block in sorted_blocks:
            block.draw()

# size = 20
# with open('world.shura', 'bw') as file:
#     for x in range(size):
#         for z in range(size):
#             block = Block(None, 1, x, 0, z)
#             file.write(block.get_bytes())