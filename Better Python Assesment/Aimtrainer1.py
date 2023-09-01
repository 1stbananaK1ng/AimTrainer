import random
import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.1
SPRITE_SCALING_TARGET = 0.3
TARGET_COUNT = 100

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Aim trainer"


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Variables that will hold sprite lists
        self.player_list = None
        self.target_list = None

        # Set up the player info
        self.player_sprite = None

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()

        # Set up the player
        img = ":resources:images/enemies/saw.png"
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.create_target()

    def create_target(self):
        """ Create a new target sprite and add it to the target list. """
        target = arcade.Sprite(":resources:images/pinball/bumper.png", SPRITE_SCALING_TARGET)

        # Position the target randomly within the screen boundaries
        target.center_x = random.randrange(SCREEN_WIDTH)
        target.center_y = random.randrange(SCREEN_HEIGHT)

        # Add the target to the target list
        self.target_list.append(target)

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.target_list.draw()
        self.player_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """
        pass

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """ Called whenever a mouse button is pressed. """
        targets_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.target_list)

        # Loop through each colliding sprite, remove it, add to the score, and create a new target
        for target in targets_hit_list:
            target.remove_from_sprite_lists()
            self.create_target()


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
