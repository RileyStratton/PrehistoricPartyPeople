import os
import arcade
import constants


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),

    ]


class Player(arcade.Sprite):
    """This class will be setup the player attributes."""

    def __init__(self):

        # Set up parent class
        super().__init__()

        # setup player starting position
        self.center_x = 128
        self.center_y = 128

        # Default to face-right
        self.character_face_direction = constants.RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = constants.CHARACTER_SCALING

        # Track our state
        self.jumping = False
        
        # --- Load Textures ---

        
        main_path = os.path.join("./assets/player")
    

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(constants.IDLE_TEXTURE)
        self.jump_texture_pair = load_texture_pair(constants.JUMP_TEXTURE)
        self.fall_texture_pair = load_texture_pair(constants.FALL_TEXTURE)
        
        # Load textures for walking
        self.walk_textures = []
        for i in range(7):
            texture = load_texture_pair(f"{main_path}/player_{i}.png")
            self.walk_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used
        self.hit_box = self.texture.hit_box_points


    def update_animation(self, key, delta_time: float= 1 / 60):
    
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == constants.RIGHT_FACING:
            self.character_face_direction = constants.LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == constants.LEFT_FACING:
            self.character_face_direction = constants.RIGHT_FACING

        # if character is moving left, flip the character texture to face left
        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        # if the character is moving right, flip the character texture to face right
        elif self.change_y < 0:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 6  * constants.UPDATES_PER_FRAME:
            self.cur_texture = 0
            
        frame = self.cur_texture // constants.UPDATES_PER_FRAME
        self.texture = self.walk_textures[frame][
            self.character_face_direction
        ]