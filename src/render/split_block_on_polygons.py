def split_block_on_polygons(block):
    world = block.chunk.world

    x = block.x + 16*block.chunk.x  # absolute
    y = block.y                     # absolute
    z = block.z + 16*block.chunk.z  # absolute

    polygons = []

    # -Z face
    if not world.get_block_id(x, y, z-1):
        polygons.append({
            "polygon": {
                "pos": [[x+1, y, z], [x, y+1, z], [x, y, z]],
                "uv":  [[1, 1],       [0, 0],     [0, 1]]
            },
            "id": block.id,
            "face_dir": '-z'
        })
        polygons.append({
            "polygon": {
                "pos": [[x+1, y, z], [x, y+1, z], [x+1, y+1, z]],
                "uv":  [[1, 1],       [0, 0],     [1, 0]]
            },
            "id": block.id,
            "face_dir": '-z'
        })

    # -X face
    if not world.get_block_id(x-1, y, z):
        polygons.append({
            "polygon": {
                "pos": [[x, y, z], [x, y+1, z+1], [x, y, z+1]],
                "uv":  [[1, 1],    [0, 0],        [0, 1]]
            },
            "id": block.id,
            "face_dir": '-x'
        })
        polygons.append({
            "polygon": {
                "pos": [[x, y, z], [x, y+1, z+1], [x, y+1, z]],
                "uv":  [[1, 1],    [0, 0],        [1, 0]]
            },
            "id": block.id,
            "face_dir": '-x'
        })

    # +X face
    if not world.get_block_id(x+1, y, z):
        polygons.append({
            "polygon": {
                "pos": [[x+1, y+1, z], [x+1, y, z+1], [x+1, y, z]],
                "uv":  [[0, 0],         [1, 1],        [0, 1]]
            },
            "id": block.id,
            "face_dir": '+x'
        })
        polygons.append({
            "polygon": {
                "pos": [[x+1, y+1, z], [x+1, y, z+1], [x+1, y+1, z+1]],
                "uv":  [[0, 0],         [1, 1],        [1, 0]]
            },
            "id": block.id,
            "face_dir": '+x'
        })

    # +Z face
    if not world.get_block_id(x, y, z+1):
        polygons.append({
            "polygon": {
                "pos": [[x, y+1, z+1], [x+1, y, z+1], [x, y, z+1]],
                "uv":  [[1, 0],         [0, 1],        [1, 1]]
            },
            "id": block.id,
            "face_dir": '+z'
        })
        polygons.append({
            "polygon": {
                "pos": [[x, y+1, z+1], [x+1, y, z+1], [x+1, y+1, z+1]],
                "uv":  [[1, 0],         [0, 1],        [0, 0]]
            },
            "id": block.id,
            "face_dir": '+z'
        })

    # -Y face (низ)
    if not world.get_block_id(x, y-1, z):
        polygons.append({
            "polygon": {
                "pos": [[x, y, z+1], [x+1, y, z], [x, y, z]],
                "uv":  [[0, 1],       [1, 0],     [0, 0]]
            },
            "id": block.id,
            "face_dir": '-y'
        })
        polygons.append({
            "polygon": {
                "pos": [[x, y, z+1], [x+1, y, z], [x+1, y, z+1]],
                "uv":  [[0, 1],       [1, 0],     [1, 1]]
            },
            "id": block.id,
            "face_dir": '-y'
        })

    # +Y face (верх)
    if not world.get_block_id(x, y+1, z):
        polygons.append({
            "polygon": {
                "pos": [[x, y+1, z+1], [x+1, y+1, z], [x, y+1, z]],
                "uv":  [[0, 0],         [1, 1],        [0, 1]]
            },
            "id": block.id,
            "face_dir": '+y'
        })
        polygons.append({
            "polygon": {
                "pos": [[x, y+1, z+1], [x+1, y+1, z], [x+1, y+1, z+1]],
                "uv":  [[0, 0],         [1, 1],        [1, 0]]
            },
            "id": block.id,
            "face_dir": '+y'
        })

    return polygons