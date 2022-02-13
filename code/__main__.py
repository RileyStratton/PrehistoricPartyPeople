"""
Platformer Game
"""
import arcade
# import arcade.gui
import os

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 5
TILE_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 8
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # Load sound
        self.background_music = arcade.load_sound("assets/sound/background/mp3/night-forest-with-insects.mp3")
        # play the background music
        arcade.play_sound(self.background_music, volume=0.25)

        # Enables a GUI Manager to make signs work
        # self.manager = arcade.gui.UIManager(self)
        # self.manager.enable()

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Initialize Scene
        self.scene = arcade.Scene()

        # Set up the player, specifically placing it at these coordinates.
        image_source = os.path.join('assets/player_2.png')
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[512, 200], [256, 200], [768, 200]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
            )
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, 
            gravity_constant=GRAVITY, 
            walls=self.scene["Walls"]
        )

        # Create an example sign
        sign = arcade.Sprite(":resources:images/tiles/signRight.png", TILE_SCALING)
        sign.position = [512, 264]
        self.scene.add_sprite("Signs", sign)



    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our Scene
        self.scene.draw()

        # Sign display
        # self.manager.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
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

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Collision Detection
        # player_collision_list = arcade.check_for_collision_with_lists(
        #     self.player_sprite,
        #     [
        #         self.scene["Signs"]
        #     ])

        # for collision in player_collision_list:
        #     if self.scene["Signs"] in collision.sprite_lists:
        #         self.display_sign()

            # if self.scene["Signs"] not in collision.sprite_lists:
            #     self.remove_sign()

    # def display_sign(self):
    #     self.message_box = arcade.gui.UIMessageBox(
    #         width=300,
    #         height=200,
    #         message_text=(
    #             "You should have a look on the new GUI features "
    #             "coming up with arcade 2.6!"
    #         )
    #     )

    #     if self.manager.get_widgets_at(0) == self.message_box:
    #         print ("huzzah")
    #     else:
    #         self.manager.add(self.message_box)
    #         print ("boo")
    #         print(self.manager.get_widgets_at(0))

    # def remove_sign(self):
    #     print(self.manager)

        


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
