import random
import arcade

# Constants
SPRITE_SCALING_PLAYER = 0.000000000001
SPRITE_SCALING_TARGET = 0.3
TARGET_RADIUS = 25

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Aim Trainer"


class Crosshair:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 30

    def update(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        half_size = self.size // 2.5
        arcade.draw_line(self.x - half_size, self.y, self.x + half_size, self.y, arcade.color.WHITE, 2)
        arcade.draw_line(self.x, self.y - half_size, self.x, self.y + half_size, arcade.color.WHITE, 2)


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Aim Trainer", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Press any button to start the game", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Click anywhere for instructions", SCREEN_WIDTH // 7 + 10, SCREEN_HEIGHT // 2 + 250, 
                        arcade.color.YELLOW, font_size=20, anchor_x="center", rotation=45)

    def on_key_press(self, symbol, modifiers):
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)
    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        Empty_View = EmptyView()
        self.window.show_view(Empty_View)


class EmptyView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):
        arcade.start_render()

        x = SCREEN_WIDTH // 6  # Left alignment x-coordinate
        arcade.draw_text("Instructions", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250,
                         arcade.color.YELLOW, font_size=50, anchor_x="center")

        arcade.draw_text("You have 20 seconds to hit as many targets as possible.", x, SCREEN_HEIGHT // 2 + 150, 
                        arcade.color.WHITE, font_size=20, anchor_x="left"
        )
        arcade.draw_text("To hit a target, you must click on it. This increases your", x, SCREEN_HEIGHT // 2 + 100, 
                        arcade.color.WHITE, font_size=20, anchor_x="left"
        )

        arcade.draw_text("points. Once your time runs out, it gives your final score", x, SCREEN_HEIGHT // 2 + 50,
                        arcade.color.WHITE, font_size=20, anchor_x="left")

        arcade.draw_text("and accuracy.", x, SCREEN_HEIGHT // 2, 
                        arcade.color.WHITE, font_size=20, anchor_x="left" )

        arcade.draw_text("Press 'B' to go back", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 375,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.B:
            instruction_view = InstructionView()
            self.window.show_view(instruction_view)


class GameOverView(arcade.View):
    def __init__(self, score, accuracy):
        super().__init__()
        self.score = score
        self.accuracy = accuracy
        self.window.set_mouse_visible(True)

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text(f"Score: {self.score}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 75,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text(f"Accuracy: {self.accuracy:.2f}%", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Press any button to play again", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 225,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        instruction_view = InstructionView()
        self.window.show_view(instruction_view)


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_list = None
        self.target_list = None
        self.score = 0
        self.timer = 20
        self.clicks = 0
        self.accuracy = 0
        self.player_sprite = None
        self.crosshair_list = arcade.SpriteList()
        self.window.set_mouse_visible(False)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()
        self.crosshair = Crosshair()

        img = ":resources:images/enemies/saw.png"
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.create_target()

    def create_target(self):
        target = arcade.SpriteCircle(TARGET_RADIUS, arcade.color.RED, SPRITE_SCALING_TARGET)
        target.center_x = random.randint(100, 900)
        target.center_y = random.randint(100, 700) 
        self.target_list.append(target)

    def on_draw(self):
        arcade.start_render()
        self.target_list.draw()
        self.player_list.draw()
        self.crosshair.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(text=output, start_x=10, start_y=20, color=arcade.color.WHITE, font_size=14)

        output = f"Timer: {int(self.timer)}"
        arcade.draw_text(text=output, start_x=10, start_y=750, color=arcade.color.WHITE, font_size=14)

        output = f"Total Clicks: {self.clicks}"
        arcade.draw_text(text=output, start_x=850, start_y=750, color=arcade.color.WHITE, font_size=14)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y
        self.crosshair.update(x, y)

    def on_update(self, delta_time):
        self.timer -= delta_time

        if self.timer < 0:
            accuracy = 0 if self.clicks == 0 else (self.score / self.clicks) * 100
            game_over_view = GameOverView(self.score, accuracy)
            self.window.show_view(game_over_view)

    def on_mouse_press(self, x, y, button, modifiers):
        targets_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.target_list)

        for target in targets_hit_list:
            target.remove_from_sprite_lists()
            self.create_target()
            self.score += 1

        self.clicks += 1

    def on_key_press(self, symbol, modifiers):
        game_over_view = GameOverView(self.score, self.accuracy)
        self.window.show_view(game_over_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    instruction_view = InstructionView()
    empty_view = EmptyView()
    window.show_view(instruction_view)
    arcade.run()


if __name__ == "__main__":
    main()
