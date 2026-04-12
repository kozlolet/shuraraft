from src.render.block_render import BlockRender


class Block:
    def __init__(self, world, id:int, x:int, y:int, z:int):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.world = world

    def get_bytes(self):
        self.id.to_bytes(1), self.x.to_bytes(2), self.y.to_bytes(2), self.z.to_bytes(2)

        block_bytes = b''
        block_bytes += self.id.to_bytes(1)
        block_bytes += self.x.to_bytes(2)
        block_bytes += self.y.to_bytes(2)
        block_bytes += self.z.to_bytes(2)

        return block_bytes

    def draw(self):
        block_render = BlockRender(self)
        block_render.split_block_on_polygons()
        block_render.block_polygons_render()



