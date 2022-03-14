"""
Platformer Game
"""
import arcade
import os

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1.9
TILE_SCALING = 1.2
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
ON_LEVEL_MAP = False


# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1


# Movement speed of player, in pixels per frame
UPDATES_PER_FRAME = 10
PLAYER_MOVEMENT_SPEED = 4
GRAVITY = 1
PLAYER_JUMP_SPEED = 17

LAYER_NAME_PLAYER = "Player"





def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),

    ]
class PlayerCharacter(arcade.Sprite):
    """Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        # Track our state
        self.jumping = False
        

        # --- Load Textures ---

        
        main_path = os.path.join("./assets/player")

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}/player_0.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}/jump_0.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}/fall_0.png")
        

        
        

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
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING


        
        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return
        



        


        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 6  * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = self.walk_textures[frame][
            self.character_face_direction
        ]


        


        


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.score = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        # Load background sound
        self.background_1 = arcade.load_sound("assets/sound/background/mp3/night-forest-with-insects.mp3")
        arcade.play_sound(self.background_1, volume=0.25)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self, current_map):
        """Set up the game here. Call this function to restart the game."""

        # If we're on the start or end screen, we don't want the camera
        if current_map != "./assets/sand_map.json":
            ON_LEVEL_MAP = False
        else:
            ON_LEVEL_MAP = True

        # Setup the Cameras
        if ON_LEVEL_MAP:
            self.camera = arcade.Camera(self.width, self.height)
            self.gui_camera = arcade.Camera(self.width, self.height)

        # Name of map file to load
        map_name = current_map

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)



        
     
        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = PlayerCharacter()
    
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        






        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Platforms"]
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        if ON_LEVEL_MAP:
            self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        if ON_LEVEL_MAP:
            self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()


        self.scene.update_animation(
            delta_time, [LAYER_NAME_PLAYER]
        )

        # See if we hit any coins
        # coin_hit_list = arcade.check_for_collision_with_list(
        #     self.player_sprite, self.scene["Coins"]
        # )

        # Loop through each coin we hit (if any) and remove it
        # for coin in coin_hit_list:
        #     # Remove the coin
        #     coin.remove_from_sprite_lists()
        #     # Play a sound
        #     arcade.play_sound(self.collect_coin_sound)
        #     # Add one to the score
        #     self.score += 1

        # Position the camera
        if ON_LEVEL_MAP:
            self.center_camera_to_player()

        # Sign Collision Detection
        collision_list = arcade.check_for_collision_with_lists(self.player_sprite, [self.scene["Signs"]])
        for collision in collision_list:
            if self.scene["start"] in collision.sprite_lists: self.setup("../assets/sand_map.json")
        else: self.display_sign = False


def main():
    """Main function"""
    window = MyGame()
    window.setup("./assets/title.json")
    arcade.run()


if __name__ == "__main__":
    main()


# """
# Platformer Game
# """
# import arcade
# # import arcade.gui
# import os

# # Constants
# SCREEN_WIDTH = 1000
# SCREEN_HEIGHT = 650
# SCREEN_TITLE = "Platformer"

# # Constants used to scale our sprites from their original size
# CHARACTER_SCALING = 5
# TILE_SCALING = 0.5

# # Movement speed of player, in pixels per frame
# MAX_PLAYER_MOVEMENT_SPEED = 8
# GRAVITY = 1
# PLAYER_JUMP_SPEED = 20


# class MyGame(arcade.Window):
#     """
#     Main application class.
#     """

#     def __init__(self):

#         # Call the parent class and set up the window
#         super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
#         # Values for movement
#         self.left_pressed = False
#         self.right_pressed = False
#         self.move_right = False
#         self.move_left = False

#         # Our TileMap Object
#         self.tile_map = None


#         # Our Scene Object
#         self.scene = None

#         # Separate variable that holds the player sprite
#         self.player_sprite = None

#         # Our physics engine
#         self.physics_engine = None

#         arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

#         # Our camera
#         self.camera = None

#         # Load background sound
#         self.background_music = arcade.load_sound("assets/sound/background/mp3/night-forest-with-insects.mp3")
#         # play the background music
#         arcade.play_sound(self.background_music, volume=0.25)

#         # Load character movement sound
#         self.character_jump = arcade.load_sound("assets/sound/character_movement/jump_sound.wav")
        
#         # Initializes with no sign being displayed
#         self.display_sign = False

#     def setup(self):
#         """Set up the game here. Call this function to restart the game."""
        
#         # Initialize camera
#         self.camera = arcade.Camera(self.width, self.height)










#  # Name of map file to load
#         map_name = "assets/sand_map.json"

#         # Layer specific options are defined based on Layer names in a dictionary
#         # Doing this will make the SpriteList for the platforms layer
#         # use spatial hashing for detection.
#         layer_options = {
#             "Platforms": {
#                 "use_spatial_hash": True,
#             },
#         }

#         # Read in the tiled map
#         self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

#         # Initialize Scene with our TileMap, this will automatically add all layers
#         # from the map as SpriteLists in the scene in the proper order.
#         self.scene = arcade.Scene.from_tilemap(self.tile_map)



#         # Initialize Scene
#         self.scene = arcade.Scene()

#         # Create an example sign
#         sign = arcade.Sprite(":resources:images/tiles/signRight.png", TILE_SCALING)
#         sign.position = [512, 264]
#         self.scene.add_sprite("Signs", sign)

#         # Set up the player, specifically placing it at these coordinates.
#         image_source = os.path.join('assets/player_2.png')
#         self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
#         self.player_sprite.center_x = SCREEN_WIDTH / 2
#         self.player_sprite.center_y = 128
#         self.scene.add_sprite("Player", self.player_sprite)

#         # # Create the ground
#         # # This shows using a loop to place multiple sprites horizontally
#         # for x in range(0, 1250, 64):
#         #     wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
#         #     wall.center_x = x
#         #     wall.center_y = 32
#         #     self.scene.add_sprite("Walls", wall)

#         # # Put some crates on the ground
#         # # This shows using a coordinate list to place sprites
#         # coordinate_list = [[512, 200], [256, 200], [768, 200]]

#         # for coordinate in coordinate_list:
#         # #     # Add a crate on the ground
#         #     wall = arcade.Sprite(
#         #         ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
#         #     )
#         #     wall.position = coordinate
#         #     self.scene.add_sprite("Walls", wall)

#         # Create the 'physics engine'
#         self.physics_engine = arcade.PhysicsEnginePlatformer(
#             self.player_sprite, 
#             gravity_constant=GRAVITY,
#             walls=self.scene['Platforms']
#             )
       


#     def on_draw(self):
#         """Render the screen."""

#         # Clear the screen to the background color
#         arcade.start_render()

#         # Use the camera
#         self.camera.use()

#         # Draw our Scene
#         self.scene.draw()

#         # If colliding with a sign, display this text
#         if self.display_sign:
#             arcade.draw_text(
#                 text = "Continue forward to see how dinosaurs went extinct!",
#                 start_x=512,
#                 start_y=392,
#                 color=arcade.color.BLACK,
#                 font_size=20,
#                 anchor_x="center"
#             )

#     def on_key_press(self, key, modifiers):
#         """Called whenever a key is pressed."""

#         if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
#             if self.physics_engine.can_jump():
#                 self.player_sprite.change_y = PLAYER_JUMP_SPEED
#                 arcade.play_sound(self.character_jump)
#         elif key == arcade.key.LEFT or key == arcade.key.A:
#             self.left_pressed = True
#         elif key == arcade.key.RIGHT or key == arcade.key.D:
#             self.right_pressed = True

#         self.process_keychange()

#     def on_key_release(self, key, modifiers):
#         """Called when the user releases a key."""

#         if key == arcade.key.LEFT or key == arcade.key.A:
#             self.left_pressed = False
#         elif key == arcade.key.RIGHT or key == arcade.key.D:
#             self.right_pressed = False

#         self.process_keychange()

#     def process_keychange(self):
#         if self.right_pressed and not self.left_pressed:
#             #self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
#             self.move_right = True
#         elif self.left_pressed and not self.right_pressed:
#             #self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
#             self.move_left = True
#         #else:
#             #self.player_sprite.change_x = 0

#     def center_camera_to_player(self):
#         screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2.5)
#         screen_center_y = self.player_sprite.center_y - (
#             self.camera.viewport_height / 2.5
#         )

#         # Don't let camera travel past 0
#         if screen_center_x < 0:
#             screen_center_x = 0
#         if screen_center_y < 0:
#             screen_center_y = 0
#         player_centered = screen_center_x, screen_center_y

#         self.camera.move_to(player_centered)

#     def on_update(self, delta_time):
#         """Movement and game logic"""
#         # Acceleration/deceleration logic
#         if self.move_right == True and self.right_pressed == True:
#             if self.player_sprite.change_x < MAX_PLAYER_MOVEMENT_SPEED:
#                 self.player_sprite.change_x += 1
#         elif self.move_right == True and self.right_pressed == False:
#             if self.player_sprite.change_x > 0:
#                 self.player_sprite.change_x -= 0.5
#             else:
#                 self.move_right = False
#         elif self.move_left == True and self.left_pressed == True:
#             if self.player_sprite.change_x > -MAX_PLAYER_MOVEMENT_SPEED:
#                 self.player_sprite.change_x -= 1
#         elif self.move_left == True and self.left_pressed == False:
#             if self.player_sprite.change_x < 0:
#                 self.player_sprite.change_x += 0.5
#             else:
#                 self.move_left = False
#         # Move the player with the physics engine
#         self.physics_engine.update()
        
#         # Center the camera on the player
#         # Position the camera
#         self.center_camera_to_player()


#         # Sign Collision Detection
#         collision_list = arcade.check_for_collision_with_lists(self.player_sprite, [self.scene["Signs"])
#         if sign_collision: self.display_sign = True
#         else: self.display_sign = False


# def main():
#     """Main function"""
#     window = MyGame()
#     window.setup()
#     arcade.run()


# if __name__ == "__main__":
#     main()
















