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
MAX_PLAYER_MOVEMENT_SPEED = 8
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Values for movement
        self.left_pressed = False
        self.right_pressed = False
        self.move_right = False
        self.move_left = False

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # Our camera
        self.camera = None

        # Load sound
        self.background_music = arcade.load_sound("assets/sound/background/mp3/night-forest-with-insects.mp3")
        # play the background music
        arcade.play_sound(self.background_music, volume=0.25)

        # Enables a GUI Manager to make signs work
        # self.manager = arcade.gui.UIManager(self)
        # self.manager.enable()

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        
        # Initialize camera
        self.camera = arcade.Camera(self.width, self.height)

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

        # Use the camera
        self.camera.use()

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
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()

    def process_keychange(self):
        if self.right_pressed and not self.left_pressed:
            #self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            self.move_right = True
        elif self.left_pressed and not self.right_pressed:
            #self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            self.move_left = True
        #else:
            #self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2.5)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2.5
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""
        # Acceleration/deceleration logic
        if self.move_right == True and self.right_pressed == True:
            if self.player_sprite.change_x < MAX_PLAYER_MOVEMENT_SPEED:
                self.player_sprite.change_x += 1
        elif self.move_right == True and self.right_pressed == False:
            if self.player_sprite.change_x > 0:
                self.player_sprite.change_x -= 0.5
            else:
                self.move_right = False
        elif self.move_left == True and self.left_pressed == True:
            if self.player_sprite.change_x > -MAX_PLAYER_MOVEMENT_SPEED:
                self.player_sprite.change_x -= 1
        elif self.move_left == True and self.left_pressed == False:
            if self.player_sprite.change_x < 0:
                self.player_sprite.change_x += 0.5
            else:
                self.move_left = False
        # Move the player with the physics engine
        self.physics_engine.update()
        
        # Center the camera on the player
        # Position the camera
        self.center_camera_to_player()


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
