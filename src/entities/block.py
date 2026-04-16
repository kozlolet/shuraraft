class Block:
    def __init__(self, chunk, id:int, x:int, y:int, z:int):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.chunk = chunk