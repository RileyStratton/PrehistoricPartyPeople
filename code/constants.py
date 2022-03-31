# Write your contant variables here
import os

# store absolute path to game folder
PATH = os.path.dirname(os.path.abspath(__file__))

# screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

# window title
SCREEN_TITLE = "Prehistoric Party"


# ------------ CHARACTER ------------

# character asset path
IDLE_TEXTURE = os.path.join(PATH, "..", "assets", "player", "player_0.png")
JUMP_TEXTURE = os.path.join(PATH, "..", "assets", "player", "jump_0.png")
FALL_TEXTURE = os.path.join(PATH, "..", "assets", "player", "fall_0.png")

# character and object scaling
CHARACTER_SCALING = 1.9
TILE_SCALING = 1.2
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# identify character direction
RIGHT_FACING = 0
LEFT_FACING = 1

# character movement
UPDATES_PER_FRAME = 10
PLAYER_MOVEMENT_SPEED = 4
GRAVITY = 1
PLAYER_JUMP_SPEED = 17

# layer name
LAYER_NAME_PLAYER = "Player"


# ------------ SOUNDS ------------

# background music
BACKGROUND_1 = os.path.join(PATH, "..", "assets", "sound", "background", "field_theme_1.wav")
BACKGROUND_2 = os.path.join(PATH, "..", "assets", "sound", "background", "night_theme_1.wav")
BACKGROUND_3 = os.path.join(PATH, "..", "assets", "sound", "background", "dungeon_theme_1.wav")
BACKGROUND_4 = os.path.join(PATH, "..", "assets", "sound", "background", "cave_theme_1.wav")

# dinosaur growl
DINOSAUR_GROWL = os.path.join(PATH, "..", "assets", "sound", "fx", "dinosuar_growl_3.wav")

