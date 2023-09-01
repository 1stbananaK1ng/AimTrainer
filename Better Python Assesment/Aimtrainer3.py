import random
import arcade
import os
import time

# Constants
SPRITE_SCALING_PLAYER = 0.000000000001
SPRITE_SCALING_TARGET = 0.2
SPRITE_SCALING_BARROL = 0.25
TARGET_RADIUS = 25

CROSSHAIR_IMAGE_PATH = "Images\Crosshair.png"

MOVING_TARGET_SPAWN_INTERVAL = 5
MOVING_TARGET_SPEED = 500

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Aim Trainer"
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 100
BUTTON_X, BUTTON_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50

TEXTURE1 = ":resources:images/pinball/pool_cue_ball.png"
TEXTURE2 = ":resources:images/space_shooter/meteorGrey_big2.png"


#start screen
class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.window.set_mouse_visible(True)
        self.original_button_hovered = False
        self.versatile_button_hovered = False
        self.barrel_button_hovered = False
        
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Aim Trainer", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200,
                         arcade.color.WHITE, font_size=80, anchor_x="center")
        arcade.draw_text("By Oakley Co", SCREEN_WIDTH // 1.4, SCREEN_HEIGHT // 2 + 170,
                         arcade.color.YELLOW, font_size=10, anchor_x="center")
        arcade.draw_text("Press 'i' for instructions", SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2 + 200, 
                        arcade.color.YELLOW, font_size=20, anchor_x="center", rotation=45)
        self.draw_buttons()

    def draw_buttons(self):
        # Draw the first button
        if self.original_button_hovered:
            arcade.draw_rectangle_filled(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, arcade.color.RED_VIOLET)
        else:
            arcade.draw_rectangle_filled(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, arcade.color.DARK_BYZANTIUM)
        arcade.draw_text("Original", BUTTON_X, BUTTON_Y, arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")

        # Draw the second button
        if self.versatile_button_hovered:
            arcade.draw_rectangle_filled(BUTTON_X, BUTTON_Y - BUTTON_HEIGHT - 30, BUTTON_WIDTH, BUTTON_HEIGHT, arcade.color.RED_VIOLET)
        else:
            arcade.draw_rectangle_filled(BUTTON_X, BUTTON_Y - BUTTON_HEIGHT - 30, BUTTON_WIDTH, BUTTON_HEIGHT, arcade.color.DARK_BYZANTIUM)
        arcade.draw_text("Versatile", BUTTON_X, BUTTON_Y - BUTTON_HEIGHT - 30, arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")

        # Draw the third button
        if self.barrel_button_hovered:
            arcade.draw_rectangle_filled(BUTTON_X, BUTTON_Y - 2 * (BUTTON_HEIGHT + 30), BUTTON_WIDTH, BUTTON_HEIGHT, arcade.color.RED_VIOLET)
        else:
            arcade.draw_rectangle_filled(BUTTON_X, BUTTON_Y - 2 * (BUTTON_HEIGHT + 30), BUTTON_WIDTH, BUTTON_HEIGHT, arcade.color.DARK_BYZANTIUM)
        arcade.draw_text("Barrol Shooter", BUTTON_X, BUTTON_Y - 2 * (BUTTON_HEIGHT + 30), arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")

    def on_mouse_motion(self, x, y, dx, dy):
        # Check if the mouse is hovering over any of the buttons
        self.original_button_hovered = (
            BUTTON_X - BUTTON_WIDTH / 2 < x < BUTTON_X + BUTTON_WIDTH / 2
            and BUTTON_Y - BUTTON_HEIGHT / 2 < y < BUTTON_Y + BUTTON_HEIGHT / 2
        )

        self.versatile_button_hovered = (
            BUTTON_X - BUTTON_WIDTH / 2 < x < BUTTON_X + BUTTON_WIDTH / 2
            and BUTTON_Y - BUTTON_HEIGHT - 30 - BUTTON_HEIGHT / 2 < y < BUTTON_Y - BUTTON_HEIGHT - 30 + BUTTON_HEIGHT / 2
        )

        self.barrel_button_hovered = (
            BUTTON_X - BUTTON_WIDTH / 2 < x < BUTTON_X + BUTTON_WIDTH / 2
            and BUTTON_Y - 2 * (BUTTON_HEIGHT + 30) - BUTTON_HEIGHT / 2 < y < BUTTON_Y - 2 * (BUTTON_HEIGHT + 30) + BUTTON_HEIGHT / 2
        )

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Check if any of the buttons are clicked
            if (
                BUTTON_X - BUTTON_WIDTH / 2 < x < BUTTON_X + BUTTON_WIDTH / 2
                and BUTTON_Y - BUTTON_HEIGHT / 2 < y < BUTTON_Y + BUTTON_HEIGHT / 2
            ):
                #go to main game
                game_view = MyGame()
                game_view.setup()
                self.window.show_view(game_view)

            elif (
                BUTTON_X - BUTTON_WIDTH / 2 < x < BUTTON_X + BUTTON_WIDTH / 2
                and BUTTON_Y - BUTTON_HEIGHT - 30 - BUTTON_HEIGHT / 2 < y < BUTTON_Y - BUTTON_HEIGHT - 30 + BUTTON_HEIGHT / 2
            ):
                #go to versitile game
                game_viewhard = MyGameHard()
                game_viewhard.setup()
                self.window.show_view(game_viewhard)

            elif (
                BUTTON_X - BUTTON_WIDTH / 2 < x < BUTTON_X + BUTTON_WIDTH / 2
                and BUTTON_Y - 2 * (BUTTON_HEIGHT + 30) - BUTTON_HEIGHT / 2 < y < BUTTON_Y - 2 * (BUTTON_HEIGHT + 30) + BUTTON_HEIGHT / 2
            ):
                #go to barrol shooter
                barrol_view = Barrol()  
                barrol_view.setup()  
                self.window.show_view(barrol_view)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.I:
            #go to intrsuctions
            Empty_View = EmptyView()
            self.window.show_view(Empty_View)
        elif symbol == arcade.key.C:
            #go to CPS test
            CPS_test = CPSStart()
            CPS_test.setup()
            self.window.show_view(CPS_test)

#intsruction screen
class EmptyView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):
        #draw top and bottom paragraphs that explain instructions
        arcade.start_render()

        x = SCREEN_WIDTH // 4  # Left alignment x-coordinate
        arcade.draw_text("Instructions", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250,
                         arcade.color.YELLOW, font_size=50, anchor_x="center")

        y = SCREEN_HEIGHT // 2 + 150
        left_margin = x

        top_p = [
            "You have 20 seconds to hit as many targets as possible.",
            "To hit a target, you must click on it. This increases your points.",
            "Once your time runs out, it gives your final score, accuracy,",
            "and average reaction time. This is the premise for all game modes",
            "but with different features such as moving targets, etc.",
            "It's important to note that targets on [VERSITILE] mode have a",
            "lifespan of 6 seconds and you will lose a point if you do not",
            "click them in that time. And the bird in [BARROL SHOOTER] gives",
            "two points while the barrols give one."
        ]

        bottom_p = [
            "Press [ANY KEY] during a game or at [GAME OVER] to exit to",
            "[MAIN MENU]. You have the option to beat your high score on",
            "all modes. P.S Click 'C' in [MAIN MENU] for a [CPS TEST]."
        ]

        line_height = 30

        #appropriatly space lines within screen
        for line in top_p:
            arcade.draw_text(line, left_margin, y, arcade.color.WHITE, font_size=15, anchor_x="left")
            y -= line_height

        y = SCREEN_HEIGHT // 2 - 150
        for line in bottom_p:
            arcade.draw_text(line, left_margin, y, arcade.color.WHITE, font_size=15, anchor_x="left")
            y -= line_height
        
        arcade.draw_text("[Press 'B' to go back]", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 300,
                    arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.B:
            #go back to start screen
            instruction_view = InstructionView()
            self.window.show_view(instruction_view)

#game over screen
class GameOverView(arcade.View):
    def __init__(self, score, accuracy, high_score, rxn_time):
        super().__init__()
        self.score = score
        self.accuracy = accuracy
        self.high_score = high_score
        self.rxn_time = rxn_time
        self.window.set_mouse_visible(True)

    def on_draw(self):
        #render appropraite text
        arcade.start_render()

        # background colour
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                     arcade.color.LIGHT_GRAY)

        # Draw game over text (biggest)
        arcade.draw_text("Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 160,
                         arcade.color.ORANGE, font_size=70, anchor_x="center", bold=True)

        # Draw high score (smaller and below)
        high_score_text = f"Highscore: {self.high_score}"
        self.draw_styled_text(high_score_text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100,
                              arcade.color.BLUE_SAPPHIRE, font_size=40, anchor_x="center")

        # Draw scores and average reaction time
        score_text = f"Your Score: {self.score}"
        if self.accuracy > 100:
            accuracy_text = "Accuracy: 100.00%"
        else:
            accuracy_text = f"Accuracy: {self.accuracy:.2f}%"
        reaction_time_text = f"Avg RXN Time: {self.rxn_time:.2f}s"

        self.draw_styled_text(score_text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                              arcade.color.BLACK, font_size=30, anchor_x="center")
        self.draw_styled_text(accuracy_text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 75,
                              arcade.color.BLACK, font_size=30, anchor_x="center")
        self.draw_styled_text(reaction_time_text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150,
                              arcade.color.BLACK, font_size=30, anchor_x="center")

        # Draw play again instructions
        arcade.draw_text("Press any key to play again", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 225,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def draw_styled_text(self, text, x, y, color, font_size, anchor_x):
        arcade.draw_text(text, x, y, color, font_size=font_size, anchor_x=anchor_x, bold=True)

    def on_key_press(self, symbol, modifiers):
        #go back to start screen
        instruction_view = InstructionView()
        self.window.show_view(instruction_view)

#main game with generic aim training functions
class MyGame(arcade.View):
    def __init__(self):
        #prepare appropriate varaiables
        super().__init__()
        self.emitters = []
        self.player_list = None
        self.target_list = None
        self.score = 0
        self.timer = 20
        self.clicks = 0
        self.accuracy = 0
        self.rxn_time = 0
        self.last_click_time = 0
        self.size_increase_duration = 0.15
        self.target_sound = arcade.Sound(":resources:sounds/hurt1.wav")
        self.game_over_sound = arcade.Sound(":resources:sounds/gameover3.wav")
        self.player_sprite = None
        self.window.set_mouse_visible(False)
        self.high_score = self.get_high_score()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()
        self.crosshair = arcade.SpriteList()

        # Create the crosshair sprite
        self.crosshair = arcade.Sprite(CROSSHAIR_IMAGE_PATH)
        self.crosshair.scale = 2  # Adjust the scale of the crosshair sprite

        img = ":resources:images/enemies/saw.png"
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.create_target()

    #set up high_score function
    def get_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

    #target details
    def create_target(self):
        maxspawn_x = SCREEN_WIDTH - 100
        maxspawn_y = SCREEN_HEIGHT - 100
        target = arcade.Sprite("Images\Target.png", SPRITE_SCALING_TARGET)
        target.center_x = random.randint(100, maxspawn_x)
        target.center_y = random.randint(100, maxspawn_y) 
        self.target_list.append(target)

    def on_draw(self):
        #render appropriate textures used
        arcade.start_render()
        self.target_list.draw()
        self.player_list.draw()
        self.crosshair.draw()

        for emitter in self.emitters:
            emitter.draw()

        output = f"High Score: {self.high_score}"
        arcade.draw_text(text=output, start_x=10, start_y=50, color=arcade.color.WHITE, font_size=14)

        output = f"Score: {self.score}"
        arcade.draw_text(text=output, start_x=10, start_y=20, color=arcade.color.WHITE, font_size=14)

        output = f"Timer: {int(self.timer)}"
        arcade.draw_text(text=output, start_x=10, start_y=620, color=arcade.color.WHITE, font_size=14)

        output = f"Total Clicks: {self.clicks}"
        arcade.draw_text(text=output, start_x=850, start_y=620, color=arcade.color.WHITE, font_size=14)

    def on_mouse_motion(self, x, y, dx, dy):
        #if mouse is moving, crosshair and corsshair hitbox matches motion
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y
        self.crosshair.center_x = x
        self.crosshair.center_y = y

        targets_hit_list = arcade.check_for_collision_with_list(self.crosshair, self.target_list)
        if targets_hit_list:
            self.crosshair.texture = arcade.load_texture("Images\CROSSUNDERLINE.png")
        else:
            self.crosshair.texture = arcade.load_texture(CROSSHAIR_IMAGE_PATH)

    def on_update(self, delta_time):
        self.timer -= delta_time
        self.rxn_time += delta_time

        if self.timer < 0:
            #if timer gets below zero then go to game over screen
            if self.score > 0:
                self.accuracy = (self.score / self.clicks) * 100
                self.rxn_time = self.rxn_time / self.score
            else:
                self.accuracy = 0
                self.rxn_time = 0
            
            self.game_over_sound.play()
            game_over_view = GameOverView(self.score, self.accuracy, self.high_score, self.rxn_time)
            self.window.show_view(game_over_view)
        
        for emitter in self.emitters:
            emitter.update()
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, emitter._particles)
            for particle in hit_list:
                particle.kill()

        current_time = time.time()
        if current_time - self.last_click_time > self.size_increase_duration:
            self.crosshair.scale = 0.6  # Reset crosshair size

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            targets_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.target_list)
            #checks if click is on target, if so deleate and score plus 1

            for target in targets_hit_list:
                target.remove_from_sprite_lists()
                self.create_target()
                self.score += 1

                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()

                # Create a particle effect only when a target is clicked
                emitter = arcade.make_interval_emitter(
                    center_xy=(target.center_x, target.center_y),  # Use the center of the clicked target as emitter position
                    filenames_and_textures=(":resources:images/items/gemRed.png", ":resources:images/pinball/pool_cue_ball.png"),
                    emit_interval=0.001,
                    emit_duration=0.05,
                    particle_speed=4,
                    particle_lifetime_min=0.05,
                    particle_lifetime_max=0.5,
                    particle_scale=0.2,
                    fade_particles=True
                )
                self.emitters.append(emitter)

                self.target_sound.play()
                self.last_click_time = time.time()  # Update last_click_time
                self.crosshair.scale = 0.9  # Increase crosshair size

            self.clicks += 1

    def on_key_press(self, symbol, modifiers):
        #go to game over screen
        if self.score > 0:
            self.accuracy = (self.score / self.clicks) * 100
            self.rxn_time = self.rxn_time / self.score
        else:
            self.accuracy = 0
            self.rxn_time = 0
        self.game_over_sound.play()
        game_over_view = GameOverView(self.score, self.accuracy, self.high_score, self.rxn_time)
        self.window.show_view(game_over_view)

#Simple start screen that lets user prepare themselves before starting
class CPSStart(arcade.View):
    def __init__(self):
        super().__init__()
        self.window.set_mouse_visible(False)


    def setup(self):
        self.crosshair = arcade.SpriteList()

        # Create the crosshair sprite
        self.crosshair = arcade.Sprite(CROSSHAIR_IMAGE_PATH)
        self.crosshair.scale = 0.6  # Adjust the scale of the crosshair sprite

    def on_show(self):
        arcade.set_background_color(arcade.color.ALLOY_ORANGE)

    def on_draw(self):
        #draw text
        arcade.start_render()
        self.crosshair.draw()

        arcade.draw_text("Click To start", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        output = f"High Score: Who knows??"
        arcade.draw_text(text=output, start_x=10, start_y=50, color=arcade.color.WHITE, font_size=14)

        output = f"Time: 0"
        arcade.draw_text(output, 10, 10, arcade.color.WHITE, 18)

        output = f"Clicks: 0"
        arcade.draw_text(output, 870, 610, arcade.color.WHITE, 18)
    
    def on_mouse_motion(self, x, y, dx, dy):
        #crosshair follows mouse
        self.crosshair.center_x = x
        self.crosshair.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        #once ready, user clicks to start program
        if button == arcade.MOUSE_BUTTON_LEFT:
            CPS_view = CPS()
            CPS_view.setup()
            self.window.show_view(CPS_view)
    
    def on_key_press(self, symbol, modifiers):
        #escape back to start screen
        instruction_view = InstructionView()
        self.window.show_view(instruction_view)

#extra option for finding out what your average CPS is
class CPS(arcade.View):
    def __init__(self):
        #set up neede variables
        super().__init__()
        arcade.set_background_color(arcade.color.ALLOY_ORANGE)
        self.emitters = []
        self.player_list = None
        self.crosshair_list = arcade.SpriteList()
        self.window.set_mouse_visible(False)
        self.last_click_time = 0
        self.size_increase_duration = 0.15
        self.score = 0
        self.click_count = 0
        self.high_score = self.get_high_score()

        self.timer = 0
        self.total_time = 10.0  # 10 seconds

    def setup(self):
        self.coin_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.crosshair = arcade.SpriteList()


        # Create the crosshair sprite
        self.crosshair = arcade.Sprite(CROSSHAIR_IMAGE_PATH)
        self.crosshair.scale = 2  # Adjust the scale of the crosshair sprite


        img = ":resources:images/enemies/saw.png"
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    #set up high_score function
    def get_high_score(self):
        try:
            with open("[CPS]high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("[CPS]high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.crosshair.draw()

        for emitter in self.emitters:
            emitter.draw()

        # Display the remaining time on the screen
        output = f"High Score: {self.high_score}"
        arcade.draw_text(text=output, start_x=10, start_y=50, color=arcade.color.WHITE, font_size=14)

        output = f"Time: {self.total_time - self.timer:.1f}"
        arcade.draw_text(output, 10, 10, arcade.color.WHITE, 18)

        output = f"Clicks: {self.click_count}"
        arcade.draw_text(output, 870, 610, arcade.color.WHITE, 18)

    def on_update(self, delta_time):
        self.timer += delta_time

        if self.timer >= self.total_time:
            # Time's up, switch to the score view
            cps_score = self.click_count / self.total_time
            CPSgame_over_view = CPSGameOverView(cps_score, self.high_score)
            self.window.show_view(CPSgame_over_view)


        for emitter in self.emitters:
            emitter.update()
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, emitter._particles)
            for particle in hit_list:
                particle.kill
                self.score += 1

        current_time = time.time()
        if current_time - self.last_click_time > self.size_increase_duration:
            self.crosshair.scale = 0.6  # Reset crosshair size

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y
        self.crosshair.center_x = x
        self.crosshair.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:  # Check if left mouse button is clicked
            emitter = arcade.make_interval_emitter( #creates partcile effect on click
                center_xy=(x, y),
                filenames_and_textures=(TEXTURE1, TEXTURE2),
                emit_interval=0.001,
                emit_duration=0.05,
                particle_speed=4,
                particle_lifetime_min=0.05,
                particle_lifetime_max=1,
                particle_scale=0.2,
                fade_particles=True
            )
            self.emitters.append(emitter)
            self.click_count += 1
            self.last_click_time = time.time()  # Update last_click_time
            self.crosshair.scale = 0.9  # Increase crosshair size

            if self.click_count > self.high_score:
                self.high_score = self.click_count
                self.save_high_score()
    
    def on_key_press(self, symbol, modifiers):
        #if key is press, go to game over screen
        cps_score = round(self.click_count / self.timer, 1)
        CPSgame_over_view = CPSGameOverView(cps_score, self.high_score)
        self.window.show_view(CPSgame_over_view)

#gives results of your CPS after test- gameover screen
class CPSGameOverView(arcade.View):
    def __init__(self, score, high_score):
        super().__init__()
        self.score = score
        self.high_score = high_score
        self.window.set_mouse_visible(True)

    def on_draw(self):
        arcade.start_render()

        # Draw a background
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                     arcade.color.LIGHT_GRAY)

        # Draw game over text
        arcade.draw_text("Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100,
                         arcade.color.ORANGE, font_size=60, anchor_x="center", bold=True)

        # Draw scores
        arcade.draw_text(f"Your CPS: {self.score}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text(f"Highscore: {float(self.high_score / 10)}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

        # Draw play again instructions
        arcade.draw_text("Press any key to play again", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 175,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
    
    def on_key_press(self, symbol, modifiers):
        #if key press, go back to start screen
        instruction_view = InstructionView()
        self.window.show_view(instruction_view)

#harder game option with moving targets
class MyGameHard(arcade.View):
    def __init__(self):
        #set up appropriate variables
        super().__init__()
        self.emitters = []
        self.player_list = None
        self.target_list = None
        self.targetMoving_list = None
        self.targetMovingBackAndForth_list = None
        self.score = 0
        self.timer = 20
        self.clicks = 0
        self.accuracy = 0
        self.rxn_time = 0
        self.last_click_time = 0
        self.size_increase_duration = 0.15
        self.target_lifetime = 6.0
        self.target_sound = arcade.Sound(":resources:sounds/hurt1.wav")
        self.game_over_sound = arcade.Sound(":resources:sounds/gameover3.wav")
        self.player_sprite = None
        self.crosshair_list = arcade.SpriteList()
        self.window.set_mouse_visible(False)
        self.target_speed = 3  
        self.high_score = self.get_high_score()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()
        self.targetMoving_list = arcade.SpriteList()
        self.targetMovingBackAndForth_list = arcade.SpriteList() 
        self.crosshair = arcade.SpriteList()

        # Create the crosshair sprite
        self.crosshair = arcade.Sprite(CROSSHAIR_IMAGE_PATH)
        self.crosshair.scale = 2  
        

        img = ":resources:images/enemies/saw.png"
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.create_target()
        self.create_targetMoving()
        self.create_targetMovingBackAndForth()
    
    def get_high_score(self):
        #prepare high_score function
        try:
            with open("[HARD]high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0
    
    def save_high_score(self):
        with open("[HARD]high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def create_target(self):
        #details for stationary target
        maxspawn_x = SCREEN_WIDTH - 100
        maxspawn_y = SCREEN_HEIGHT - 100
        target = arcade.Sprite("Images\Target.png", SPRITE_SCALING_TARGET)
        target.center_x = random.randint(100, maxspawn_x)
        target.center_y = random.randint(100, maxspawn_y) 
        target.lifetime = self.target_lifetime
        self.target_list.append(target)

    def create_targetMoving(self):
        #details for moving target
        maxspawn_x = SCREEN_WIDTH - 100
        maxspawn_y = SCREEN_HEIGHT - 100
        targetMoving = arcade.Sprite("Images\Target-blue.png", SPRITE_SCALING_TARGET)
        targetMoving.center_x = random.randint(100, maxspawn_x)
        targetMoving.center_y = random.randint(100, maxspawn_y)
        targetMoving.change_x = random.uniform(-6, 6)
        targetMoving.change_y = random.uniform(-6, 6)
        targetMoving.change_angle = -2
        targetMoving.lifetime = self.target_lifetime
        self.targetMoving_list.append(targetMoving)

    def create_targetMovingBackAndForth(self):
        #details for horizontily moving target
        maxspawn_x = SCREEN_WIDTH - 100
        maxspawn_y = SCREEN_HEIGHT - 100
        targetMovingBackAndForth = arcade.Sprite("Images\Target-green.png", SPRITE_SCALING_TARGET)
        targetMovingBackAndForth.center_x = random.randint(100, maxspawn_x)
        targetMovingBackAndForth.center_y = random.randint(100, maxspawn_y)
        targetMovingBackAndForth.change_x = random.uniform(-8, 8)  # Random speed between -8 and 8 in x direction
        targetMovingBackAndForth.change_y = 0  # No vertical movement
        targetMovingBackAndForth.lifetime = self.target_lifetime
        self.targetMovingBackAndForth_list.append(targetMovingBackAndForth)

    def update_moving_targets(self):
        #details for how the moving target actually moves
        for targetMoving in self.targetMoving_list:
            targetMoving.center_x += targetMoving.change_x
            targetMoving.center_y += targetMoving.change_y

            # Check for collision with window boundaries and reverse the movement direction if needed
            if targetMoving.center_x < TARGET_RADIUS or targetMoving.center_x > SCREEN_WIDTH - TARGET_RADIUS:
                targetMoving.change_x *= -1
            
            if targetMoving.center_y < TARGET_RADIUS or targetMoving.center_y > SCREEN_HEIGHT - TARGET_RADIUS:
                targetMoving.change_y *= -1

    def update_moving_back_and_forth_targets(self):
        #details for how the horizontaly moving targets actually move side to side
        for targetBackAndForth in self.targetMovingBackAndForth_list:
            targetBackAndForth.center_x += targetBackAndForth.change_x

            if targetBackAndForth.center_x < TARGET_RADIUS or targetBackAndForth.center_x > SCREEN_WIDTH - TARGET_RADIUS:
                targetBackAndForth.change_x *= -1

    def on_draw(self):
        #render targets and text
        arcade.start_render()
        self.target_list.draw()
        self.targetMoving_list.draw()
        self.targetMovingBackAndForth_list.draw()
        self.player_list.draw()
        self.crosshair.draw()

        for emitter in self.emitters:
            emitter.draw()
        
        output = f"High Score: {self.high_score}"
        arcade.draw_text(text=output, start_x=10, start_y=50, color=arcade.color.WHITE, font_size=14)

        output = f"Score: {self.score}"
        arcade.draw_text(text=output, start_x=10, start_y=20, color=arcade.color.WHITE, font_size=14)

        output = f"Timer: {int(self.timer)}"
        arcade.draw_text(text=output, start_x=10, start_y=620, color=arcade.color.WHITE, font_size=14)

        output = f"Total Clicks: {self.clicks}"
        arcade.draw_text(text=output, start_x=850, start_y=620, color=arcade.color.WHITE, font_size=14)

    def on_mouse_motion(self, x, y, dx, dy):
        #have crosshair follow mouse
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y
        self.crosshair.center_x = x
        self.crosshair.center_y = y

        targets_hit_list = (
            arcade.check_for_collision_with_list(self.crosshair, self.target_list)
            + arcade.check_for_collision_with_list(self.crosshair, self.targetMoving_list)
            + arcade.check_for_collision_with_list(self.crosshair, self.targetMovingBackAndForth_list)
        )

        if targets_hit_list:
            self.crosshair.texture = arcade.load_texture("Images\CROSSUNDERLINE.png")
        else:
            self.crosshair.texture = arcade.load_texture(CROSSHAIR_IMAGE_PATH)


    def on_update(self, delta_time):
        #so all 'moving' parts work
        self.timer -= delta_time
        self.rxn_time += delta_time

        if self.timer < 0:
            #if timer gets less than zero then game over
            if self.score > 0:
                self.accuracy = (self.score / self.clicks) * 100
                self.rxn_time = self.rxn_time / self.score
            else:
                self.accuracy = 0
                self.rxn_time = 0
            
            self.game_over_sound.play()
            game_over_view = GameOverView(self.score, self.accuracy, self.high_score, self.rxn_time)
            self.window.show_view(game_over_view)

        # Call the method to update the positions of moving targets
        self.update_moving_targets()
        self.update_moving_back_and_forth_targets()

        for emitter in self.emitters:
            emitter.update()
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, emitter._particles)
            for particle in hit_list:
                particle.kill()
        
        #set up lifespan for all three targets making it so if they go 6 seconds without being hit, they get destroyed and player looses one point
        for target in self.target_list:
            target.lifetime -= delta_time
            if target.lifetime <= 0:
                self.target_list.remove(target)
                if self.score > 0:
                    self.score -= 1  # Decrease player's score
                emitter = arcade.make_interval_emitter( #create a partcile effect on destruction
                    center_xy=(target.center_x, target.center_y),
                    filenames_and_textures=(":resources:images/items/gemRed.png", ":resources:images/pinball/pool_cue_ball.png"),
                    emit_interval=0.001,
                    emit_duration=0.05,
                    particle_speed=4,
                    particle_lifetime_min=0.05,
                    particle_lifetime_max=0.5,
                    particle_scale=0.2,
                    fade_particles=True
                )
                self.emitters.append(emitter)
                self.target_sound.play()
                self.create_target()

        for targetMoving in self.targetMoving_list:
            targetMoving.lifetime -= delta_time
            if targetMoving.lifetime <= 0:
                self.targetMoving_list.remove(targetMoving)
                if self.score > 0:
                    self.score -= 1  # Decrease player's score
                emitter = arcade.make_interval_emitter( #create a partcile effect on destruction
                    center_xy=(targetMoving.center_x, targetMoving.center_y),
                    filenames_and_textures=(":resources:images/items/gemBlue.png", ":resources:images/pinball/pool_cue_ball.png"),
                    emit_interval=0.001,
                    emit_duration=0.05,
                    particle_speed=4,
                    particle_lifetime_min=0.05,
                    particle_lifetime_max=0.5,
                    particle_scale=0.2,
                    fade_particles=True
                )
                self.emitters.append(emitter)
                self.target_sound.play()
                self.create_targetMoving()
        
        for targetMovingBackAndForth in self.targetMovingBackAndForth_list:
            targetMovingBackAndForth.lifetime -= delta_time
            if targetMovingBackAndForth.lifetime <= 0:
                self.targetMovingBackAndForth_list.remove(targetMovingBackAndForth)
                if self.score > 0:
                    self.score -= 1  # Decrease player's score
                emitter = arcade.make_interval_emitter( #create a partcile effect on destruction
                    center_xy=(targetMovingBackAndForth.center_x, targetMovingBackAndForth.center_y),
                    filenames_and_textures=(":resources:images/items/gemGreen.png", ":resources:images/pinball/pool_cue_ball.png"),
                    emit_interval=0.001,
                    emit_duration=0.05,
                    particle_speed=4,
                    particle_lifetime_min=0.05,
                    particle_lifetime_max=0.5,
                    particle_scale=0.2,
                    fade_particles=True
                )
                self.emitters.append(emitter)
                self.target_sound.play()
                self.create_targetMovingBackAndForth()
        
        current_time = time.time()
        if current_time - self.last_click_time > self.size_increase_duration:
            self.crosshair.scale = 0.6  # Reset crosshair size

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Check for hitting regular targets (red targets)
            targets_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.target_list)

            for target in targets_hit_list:
                target.remove_from_sprite_lists()
                self.create_target()
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()

                # Create a particle effect only when a target is clicked
                emitter = arcade.make_interval_emitter(
                    center_xy=(target.center_x, target.center_y),
                    filenames_and_textures=(":resources:images/items/gemRed.png", ":resources:images/pinball/pool_cue_ball.png"),
                    emit_interval=0.001,
                    emit_duration=0.05,
                    particle_speed=4,
                    particle_lifetime_min=0.05,
                    particle_lifetime_max=0.5,
                    particle_scale=0.2,
                    fade_particles=True
                )
                self.emitters.append(emitter)
                self.target_sound.play()
                self.last_click_time = time.time()  # Update last_click_time
                self.crosshair.scale = 0.9  # Increase crosshair size

            # Check for hitting the moving targets (blue targets)
            targetsM_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.targetMoving_list)

            for targetM in targetsM_hit_list:
                targetM.remove_from_sprite_lists()
                self.create_targetMoving()
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()

                # Create a particle effect only when a target is clicked
                emitter = arcade.make_interval_emitter(
                    center_xy=(targetM.center_x, targetM.center_y),
                    filenames_and_textures=(":resources:images/items/gemBlue.png", ":resources:images/pinball/pool_cue_ball.png"),
                    emit_interval=0.001,
                    emit_duration=0.05,
                    particle_speed=4,
                    particle_lifetime_min=0.05,
                    particle_lifetime_max=0.5,
                    particle_scale=0.2,
                    fade_particles=True
                )
                self.emitters.append(emitter)
                self.target_sound.play()
                self.last_click_time = time.time()  # Update last_click_time
                self.crosshair.scale = 0.9  # Increase crosshair size

            # Check for hitting the moving back-and-forth target (green target)
            targetsBackAndForth_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.targetMovingBackAndForth_list)

            for targetBackAndForth in targetsBackAndForth_hit_list:
                targetBackAndForth.remove_from_sprite_lists()
                self.create_targetMovingBackAndForth()
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()

                # Create a particle effect only when the target is clicked
                emitter = arcade.make_interval_emitter(
                    center_xy=(targetBackAndForth.center_x, targetBackAndForth.center_y),
                    filenames_and_textures=(":resources:images/items/gemGreen.png", ":resources:images/pinball/pool_cue_ball.png"),
                    emit_interval=0.001,
                    emit_duration=0.05,
                    particle_speed=4,
                    particle_lifetime_min=0.05,
                    particle_lifetime_max=0.5,
                    particle_scale=0.2,
                    fade_particles=True
                )
                self.emitters.append(emitter)
                self.target_sound.play()
                self.last_click_time = time.time()  # Update last_click_time
                self.crosshair.scale = 0.9  # Increase crosshair size

            self.clicks += 1

    def on_key_press(self, symbol, modifiers):
        #if key is press, then go to game_over screen
        if self.score > 0:
            self.accuracy = (self.score / self.clicks) * 100
            self.rxn_time = self.rxn_time / self.score
        else:
            self.accuracy = 0
            self.rxn_time = 0
        self.game_over_sound.play()
        game_over_view = GameOverView(self.score, self.accuracy, self.high_score, self.rxn_time)
        self.window.show_view(game_over_view)

#funner gamemode that lanches barrols into the air
class Barrol(arcade.View):
    def __init__(self):
        #set up required variables
        super().__init__()
        self.emitters = []
        self.player_list = None
        self.target_list = None
        self.score = 0
        self.timer = 20
        self.clicks = 0
        self.accuracy = 0
        self.rxn_time = 0
        self.last_click_time = 0
        self.size_increase_duration = 0.15
        self.target_sound = arcade.Sound("Images\Barrelbreak.wav")
        self.brid_sound = arcade.Sound("Images\BirdSound.mp3")
        self.game_over_sound = arcade.Sound(":resources:sounds/gameover3.wav")
        self.player_sprite = None
        self.crosshair_list = arcade.SpriteList()
        self.window.set_mouse_visible(False)
        self.high_score = self.get_high_score()
        self.moving_target = None
        self.moving_target_spawn_timer = 0

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()
        self.crosshair = arcade.SpriteList()

        img = ":resources:images/enemies/saw.png"
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the crosshair sprite
        self.crosshair = arcade.Sprite(CROSSHAIR_IMAGE_PATH)
        self.crosshair.scale = 2  # Adjust the scale of the crosshair sprite

        self.create_target()
        self.create_target()
        self.create_target()

        self.moving_target_spawn_timer = MOVING_TARGET_SPAWN_INTERVAL

    def get_high_score(self):
        #set up highscore functions
        try:
            with open("Barrolhigh_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("Barrolhigh_score.txt", "w") as file:
            file.write(str(self.high_score))

    def create_target(self):
        #details for the barrel target
        maxspawn_x = SCREEN_WIDTH - 100
        target = arcade.Sprite("Images\Barrolez.png", SPRITE_SCALING_BARROL)
        target.center_x = random.randint(100, maxspawn_x)
        target.center_y = 0  # Set initial position at the bottom of the screen
        target.change_angle = -1
        target.velocity = random.uniform(100, 200)  # Randomized initial velocity
        target.gravity = 400  # Set gravity
        target.jumping = False
        self.target_list.append(target)

    def on_draw(self):
        #render targets and text
        arcade.start_render()
        self.target_list.draw()
        self.player_list.draw()
        self.crosshair.draw()

        if self.moving_target:
            self.moving_target.draw()

        for emitter in self.emitters:
            emitter.draw()

        output = f"High Score: {self.high_score}"
        arcade.draw_text(text=output, start_x=10, start_y=50, color=arcade.color.WHITE, font_size=14)

        output = f"Score: {self.score}"
        arcade.draw_text(text=output, start_x=10, start_y=20, color=arcade.color.WHITE, font_size=14)

        output = f"Timer: {int(self.timer)}"
        arcade.draw_text(text=output, start_x=10, start_y=620, color=arcade.color.WHITE, font_size=14)

        output = f"Total Clicks: {self.clicks}"
        arcade.draw_text(text=output, start_x=850, start_y=620, color=arcade.color.WHITE, font_size=14)

    def on_mouse_motion(self, x, y, dx, dy):
        #have crosshair follow mouse
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y
        self.crosshair.center_x = x
        self.crosshair.center_y = y

        targets_hit_list = arcade.check_for_collision_with_list(self.crosshair, self.target_list)

        # Check for collision with the moving target
        if self.moving_target and self.moving_target.collides_with_point((x, y)):
            targets_hit_list.append(self.moving_target)

        if targets_hit_list:
            self.crosshair.texture = arcade.load_texture("Images\CROSSUNDERLINE.png")
        else:
            self.crosshair.texture = arcade.load_texture(CROSSHAIR_IMAGE_PATH)

    def on_update(self, delta_time):
        #make all 'moving' parts work
        self.timer -= delta_time
        self.rxn_time += delta_time
        maxspawn_x = SCREEN_WIDTH - 100

        if self.timer < 0:
            #if timer is less then zero then game over
            if self.score > 0:
                self.accuracy = (self.score / self.clicks) * 100
                self.rxn_time = self.rxn_time / self.score
            else:
                self.accuracy = 0
                self.rxn_time = 0
            self.game_over_sound.play()
            game_over_view = GameOverView(self.score, self.accuracy, self.high_score, self.rxn_time)
            self.window.show_view(game_over_view)

        for emitter in self.emitters:
            emitter.update()
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, emitter._particles)
            for particle in hit_list:
                particle.kill()

        #barrel jumping physics
        for target in self.target_list:
            if not target.jumping and target.center_y <= 0:  # When the target hits the bottom
                target.center_x = random.randint(100, maxspawn_x)
                target.center_y = 0  # Reset position to the bottom
                target.velocity = random.uniform(450, 650)  # Randomize initial velocity
                target.jumping = True

            if target.jumping:
                target.center_y += target.velocity * delta_time
                target.velocity -= target.gravity * delta_time

                if target.center_y <= 0:  # When the target hits the ground
                    target.center_y = 0
                    target.velocity = random.uniform(100, 200)  # Randomize initial velocity
                    target.jumping = False
            
            target.angle += target.change_angle
        
        # Update the moving target if it exists
        if self.moving_target:
            self.moving_target.center_x -= MOVING_TARGET_SPEED * delta_time

            # Check if the moving target has gone off the screen
            if self.moving_target.left > SCREEN_WIDTH:
                self.moving_target = None

        # Spawn a new moving target if the timer allows
        self.moving_target_spawn_timer -= delta_time
        if self.moving_target_spawn_timer <= 0:
            self.moving_target_spawn_timer = MOVING_TARGET_SPAWN_INTERVAL
            self.moving_target = arcade.Sprite("Images\Owl.png", 0.15)
            self.moving_target.center_x = SCREEN_WIDTH + self.moving_target.width / 2
            self.moving_target.center_y = random.randint(400, 630)
        
        current_time = time.time()
        if current_time - self.last_click_time > self.size_increase_duration:
            self.crosshair.scale = 0.6  # Reset crosshair size

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            targets_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.target_list)
            #if click on target, destroy target and score goes up by 1

            for target in targets_hit_list:
                target.remove_from_sprite_lists()
                self.create_target()
                self.score += 1

                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()

                # Create a particle effect only when a target is clicked
                emitter = arcade.make_interval_emitter(
                    center_xy=(target.center_x, target.center_y),  # Use the center of the clicked target as emitter position
                    filenames_and_textures=(":resources:images/items/gemRed.png", ":resources:images/pinball/pool_cue_ball.png"),
                    emit_interval=0.001,
                    emit_duration=0.05,
                    particle_speed=4,
                    particle_lifetime_min=0.05,
                    particle_lifetime_max=0.5,
                    particle_scale=0.2,
                    fade_particles=True
                )
                self.emitters.append(emitter)

                self.target_sound.play()
                self.last_click_time = time.time()  # Update last_click_time
                self.crosshair.scale = 0.9  # Increase crosshair size

            self.clicks += 1 #increase score by 1

            if self.moving_target and self.moving_target.collides_with_point((x, y)):
                self.moving_target = None
                self.score += 2

                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()

                # Create a particle effect for the clicked moving target
                emitter = arcade.make_interval_emitter(
                    center_xy=(x, y),  # Use the click position as emitter position
                    filenames_and_textures=(":resources:images/items/gemRed.png", ":resources:images/pinball/pool_cue_ball.png"),
                    emit_interval=0.001,
                    emit_duration=0.05,
                    particle_speed=4,
                    particle_lifetime_min=0.05,
                    particle_lifetime_max=0.5,
                    particle_scale=0.2,
                    fade_particles=True
                )
                self.emitters.append(emitter)

                self.brid_sound.play()
                self.last_click_time = time.time()  # Update last_click_time
                self.crosshair.scale = 0.9  # Increase crosshair size

    def on_key_press(self, symbol, modifiers):
        #if key press, go to game over screen
        if self.score > 0:
            self.accuracy = (self.score / self.clicks) * 100
            self.rxn_time = self.rxn_time / self.score
        else:
            self.accuracy = 0
            self.rxn_time = 0
        self.game_over_sound.play()
        game_over_view = GameOverView(self.score, self.accuracy, self.high_score, self.rxn_time)
        self.window.show_view(game_over_view)

def main():
    #details for lanching game
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    instruction_view = InstructionView()
    empty_view = EmptyView()
    window.show_view(instruction_view)
    arcade.run()


if __name__ == "__main__":
    main() #launch game
