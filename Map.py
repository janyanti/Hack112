# MAP CLASS

import pygame
import os


class Map(pygame.sprite.Sprite):
    MAP_DIMENSIONS = (16, 16)
    TOP_LEFT = (0, 0)
    SIDE_LENGTH = 600

    @staticmethod
    def init(file):
        Map.map_img = pygame.image.load(os.path.join("Assets", file))

    # board key:
    # 'S' = start
    # 'X' = ballon path
    # 'E' = end
    # 'T'
    # 'O' = available tower tile
    # '1234' = towers

    def __init__(self, board):
        super(Map, self).__init__()
        self.image = Map.map_img
        self.rect = pygame.Rect(Map.TOP_LEFT[0], Map.TOP_LEFT[1], Map.SIDE_LENGTH, Map.SIDE_LENGTH)
        self.board = board
