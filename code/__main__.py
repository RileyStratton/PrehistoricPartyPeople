"""
Platformer Game
"""
import arcade
import os

import constants
from player import Player


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(
            constants.SCREEN_WIDTH, 
            constants.SCREEN_HEIGHT, 
            constants.SCREEN_TITLE
        )

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
        self.background_1 = arcade.load_sound(constants.BACKGROUND_1)
        self.background_2 = arcade.load_sound(constants.BACKGROUND_2)
        self.background_3 = arcade.load_sound(constants.BACKGROUND_3)
        self.background_4 = arcade.load_sound(constants.BACKGROUND_4)

        # Load dinosaur sounds
        self.dinosaur_growl = arcade.load_sound(constants.DINOSAUR_GROWL)

        # if sound played
        self.sound_played = False

        self.background_player = None

        arcade.play_sound(self.background_1, volume=0.15)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.on_level_map = False

    def setup(self, current_map):
        """Set up the game here. Call this function to restart the game."""

        # If we're on the start or end screen, we don't want the camera
        if current_map != "./assets/sand_map.json":
            self.on_level_map = False
        else:
            self.on_level_map = True

        # Setup the Cameras
        if self.on_level_map:
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
        self.tile_map = arcade.load_tilemap(map_name, constants.TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        
        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = Player()
    
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite(constants.LAYER_NAME_PLAYER, self.player_sprite)

        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, 
            gravity_constant=constants.GRAVITY, 
            walls=self.scene["Platforms"]
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        if self.on_level_map:
            self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        if self.on_level_map:
            self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            text=score_text,
            start_x=10,
            start_y=10,
            color=arcade.csscolor.WHITE,
            font_size=18,
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = constants.PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound, volume=0.05)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED

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
            delta_time, [constants.LAYER_NAME_PLAYER]
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
        if self.on_level_map:
            self.center_camera_to_player()

        # Sign Collision Detection
        if not self.on_level_map:
            menu_collision_list = arcade.check_for_collision_with_lists(self.player_sprite, [self.scene["start"]])
            for collision in menu_collision_list:
                if self.scene["start"] in collision.sprite_lists: 
                    self.setup("./assets/sand_map.json")
        # elif self.on_level_map:
        #     collision_list = arcade.check_for_collision_with_lists(self.player_sprite, [
        #         self.scene["cave"],
        #         self.scene["forest"],
        #         self.scene["swamp"],
        #         self.scene["desert"]])
        #     for collision in collision_list:
        #         if self.scene["cave"] in collision.sprite_lists:
        #             arcade.play_sound(self.background_3)
        #         elif self.scene["forest"] in collision.sprite_lists:
        #             arcade.play_sound(self.background_1)
        #         elif self.scene["desert"] in collision.sprite_lists:
        #             arcade.play_sound(self.background_2)
        #         elif self.scene["swamp"] in collision.sprite_lists:
        #             arcade.play_sound(self.background_4)
            
            pass
            # for collision in collision_list:
            #     if self.scene["dino"] in collision.sprite_lists: 
            #       self.display_sign = True
            #       arcade.play_sound(self.dinosuar_growl)
            #     else: self.display_sign = False


def main():
    """Main function"""
    window = MyGame()
    window.setup("./assets/title.json")
    arcade.run()


if __name__ == "__main__":
    main()
















