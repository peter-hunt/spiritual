from pygame.constants import SRCALPHA
from pygame.image import load as load_image
from pygame.surface import Surface

from .smartdata import SmartData

__all__ = [
    'TILEMAP_IDS', 'TILEMAPS',
    'TILE_IDS', 'COLLISSION_TILES', 'TILES',
]


class TilemapData(SmartData):
    boolmaps: dict[str, list[list[int]]]
    sources: dict[str, str]

    def get_size(self):
        firstmap = next(iter(self.boolmaps.values()))
        return (len(firstmap), len(firstmap[0]))


class Tilemap(SmartData):
    tilemap: list[list[str]]
    sources: dict[str, str]

    def get_size(self):
        return (len(self.tilemap), len(self.tilemap[0]))

    def __getitem__(self, key):
        if not isinstance(key, tuple):
            raise TypeError('Tilemap indices must be tuples')
        if len(key) != 2:
            raise TypeError('Tilemap indices must be 2-tuples')
        if not isinstance(key[0], int):
            raise TypeError('Tilemap row index must be an integer')
        if not isinstance(key[1], int):
            raise TypeError('Tilemap column index must be an integer')
        if not (0 <= key[0] < len(self.tilemap)):
            return 'empty'
        if not (0 <= key[1] < len(self.tilemap[0])):
            return 'empty'
        return self.tilemap[key[0]][key[1]]

    @classmethod
    def loaddata(cls, data: TilemapData):
        size = data.get_size()
        tilemap = [['empty' for j in range(size[0])] for i in range(size[1])]
        for i in range(size[0]):
            for j in range(size[1]):
                for tile in data.boolmaps:
                    if data.boolmaps[tile][i][j]:
                        tilemap[j][i] = tile
                        break
        return cls(tilemap, data.sources)


TILEMAP_IDS = (
    'spawn',
)

TILEMAPS = {}
for _id in TILEMAP_IDS:
    with open(f'assets/{_id}.json', 'r') as file:
        TILEMAPS[_id] = Tilemap.loaddata(TilemapData.load(file))
        # TILEMAPS[_id] = Tilemap.load(pickle_load(file))


# obj = TilemapData(
#     {
#         'grass': [
#             [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
#             [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#             [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
#             [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
#         ],
#     },
#     {
#         'grass': 'assets/grass.png',
#     },
# )


# with open('assets/spawn.json', 'w') as file:
#     obj.dump(file)

# with open('assets/spawn.json') as file:
#     obj = TilemapData.load(file)
#     print(obj)
#     print(obj.boolmaps)
#     print(obj.sources)
#     tilemap = Tilemap.loaddata(obj)
#     print(tilemap.tilemap)


TILE_IDS = (
    'empty',
    'grass',
)

COLLISSION_TILES = (
    'empty',
)

TILES = {}
for _id in TILE_IDS:
    if _id == 'empty':
        TILES[_id] = Surface((16, 16), SRCALPHA)
    else:
        TILES[_id] = load_image(f'assets/{_id}.png')
