"""
Auditory Learning project.
"""
import arcade
import random

# Screen title and size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1200
SCREEN_TITLE = "Auditory Learning"

# Constants for sizing
TARGET_RADIUS = 18
DEFENCE_RADIUS = 50

# Constants for number of different targets
CHORD_TYPES = 5
CHORD_SAMPLES = 12

CHORD_FILES = [['resources\D7_A4_Piano.wav','resources\D7_AS4_Piano.wav','resources\D7_B4_Piano.wav','resources\D7_C4_Piano.wav',
'resources\D7_CS4_Piano.wav','resources\D7_D4_Piano.wav','resources\D7_DS4_Piano.wav','resources\D7_E4_Piano.wav',
'resources\D7_F4_Piano.wav','resources\D7_FS4_Piano.wav','resources\D7_G4_Piano.wav','resources\D7_GS4_Piano.wav'],
['resources\FD7_A4_Piano.wav','resources\FD7_AS4_Piano.wav','resources\FD7_B4_Piano.wav','resources\FD7_C4_Piano.wav',
'resources\FD7_CS4_Piano.wav','resources\FD7_D4_Piano.wav','resources\FD7_DS4_Piano.wav','resources\FD7_E4_Piano.wav',
'resources\FD7_F4_Piano.wav','resources\FD7_FS4_Piano.wav','resources\FD7_G4_Piano.wav','resources\FD7_GS4_Piano.wav'],
['resources\HD7_A4_Piano.wav','resources\HD7_AS4_Piano.wav','resources\HD7_B4_Piano.wav','resources\HD7_C4_Piano.wav',
'resources\HD7_CS4_Piano.wav','resources\HD7_D4_Piano.wav','resources\HD7_DS4_Piano.wav','resources\HD7_E4_Piano.wav',
'resources\HD7_F4_Piano.wav','resources\HD7_FS4_Piano.wav','resources\HD7_G4_Piano.wav','resources\HD7_GS4_Piano.wav'],
['resources\M7_A4_Piano.wav','resources\M7_AS4_Piano.wav','resources\M7_B4_Piano.wav','resources\M7_C4_Piano.wav',
'resources\M7_CS4_Piano.wav','resources\M7_D4_Piano.wav','resources\M7_DS4_Piano.wav','resources\M7_E4_Piano.wav',
'resources\M7_F4_Piano.wav','resources\M7_FS4_Piano.wav','resources\M7_G4_Piano.wav','resources\M7_GS4_Piano.wav'],
['resources\mi7_A4_Piano.wav','resources\mi7_AS4_Piano.wav','resources\mi7_B4_Piano.wav','resources\mi7_C4_Piano.wav',
'resources\mi7_CS4_Piano.wav','resources\mi7_D4_Piano.wav','resources\mi7_DS4_Piano.wav','resources\mi7_E4_Piano.wav',
'resources\mi7_F4_Piano.wav','resources\mi7_FS4_Piano.wav','resources\mi7_G4_Piano.wav','resources\mi7_GS4_Piano.wav']]

# Constant start points for the different chord types
CHORD_X = [SCREEN_WIDTH/4,SCREEN_WIDTH/4*3,0,SCREEN_WIDTH/2,SCREEN_WIDTH]
CHORD_Y = [0,0,SCREEN_HEIGHT/4*3,SCREEN_HEIGHT,SCREEN_HEIGHT/5*4]

# Constant for the color of the different types
TYPE_COLOR = [(122, 40, 203), (165, 1, 4), 
(176, 254, 118), (255, 190, 239), (68, 204, 255) ]

# Constant for base rate of travel
RATE_OF_TRAVEL = .5

# Global variables for number of runs and current time
run = 1
timer = 30

class Target(arcade.SpriteCircle):
    """ Base Target Class """

    def __init__(self, chord, key, radius=1):
        """ Card constructor """

        # Attributes for type and sound
        self._color = TYPE_COLOR[chord]
        self.chord = CHORD_FILES[chord][key]

        self.draw_delay = 0
        self.sound_frequency = 0

        # Call the parent
        super().__init__(radius, self._color)
    
    def move_to_center(self, rate):
        """ Movement function for the targets """
        center_x = self.position[0]
        center_y = self.position[1]
        if center_x > SCREEN_WIDTH / 2:
            center_x -= rate
        else:
            center_x += rate
        
        if center_y > SCREEN_HEIGHT / 2:
            center_y -= rate
        else:
            center_y += rate
        
        self.position = (center_x, center_y)

class Defence(arcade.SpriteCircle):
    """ Base defense stuff """
    def __init__(self, radius=1):
        self._color = arcade.color.EGYPTIAN_BLUE

        super().__init__(radius, self._color)

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite list with all the targets and sprite for center.
        self.target_list = None
        self.active_target_list = None
        self.defence_list = None
        self.score = 0
        self.sound = None
        self.failure = 0
        self.original_run = 1

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Sprite lists with all the sprites for the program
        self.target_list = []
        self.active_target_list = arcade.SpriteList()
        self.defence_list = arcade.SpriteList()

        self.score = 0
        self.failure = 2400
        self.original_run = run

        # Create every target
        for chord in range(CHORD_TYPES):
            for key in range(CHORD_SAMPLES):
                target = Target(chord, key, TARGET_RADIUS)
                target.position = (CHORD_X[chord], CHORD_Y[chord])
                self.target_list.append(target)
        random.shuffle(self.target_list)

        # Pull out the active target and activate its sound file
        active = self.target_list.pop(0)
        self.sound = arcade.load_sound(active.chord)
        self.active_target_list.append(active)

        # Remember to set a defensive center XD
        earth = Defence(DEFENCE_RADIUS)
        earth.position = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        self.defence_list.append(earth)

    def on_draw(self):
        """ Render the screen. """
        global timer

        # Clear the screen
        self.clear()

        # Draw the active sprites
        if self.score >= 30:
            if self.active_target_list[0].draw_delay >= 15:
                self.active_target_list.draw()
        else:
            self.active_target_list.draw()
        self.defence_list.draw()

        # render the timer
        mins, secs = divmod(timer, 60)
        t = '{:02d}:{:02d}'.format(mins, secs)
        arcade.draw_text(t, SCREEN_WIDTH - 100, SCREEN_HEIGHT- 30)

        if self.failure < TARGET_RADIUS + DEFENCE_RADIUS:
            if timer > 0:
                arcade.draw_text("Hit space to continue.", SCREEN_WIDTH/3, SCREEN_HEIGHT/3 * 2)
            else:
                arcade.draw_text("Thank you for your participation. Please e-mail me the trainingResults.txt files that were created.", SCREEN_WIDTH/3, SCREEN_HEIGHT/4 * 3)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        # Get list of targets we've clicked on
        hit = arcade.get_sprites_at_point((x, y), self.active_target_list)

        # Have we clicked on a target?
        if len(hit) > 0:
            self.score += 1
            hit_target = self.active_target_list.pop()
            hit_target.draw_delay = 0
            self.target_list.append(hit_target)

            # Pull out the active target and activate its sound file
            active = self.target_list.pop(0)
            self.sound = arcade.load_sound(active.chord)
            self.active_target_list.append(active)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.failure < TARGET_RADIUS + DEFENCE_RADIUS:
            self.setup()


    def on_update(self, delta):
        global timer, run

        if timer > 0  and run == self.original_run:
            # Make sure there is a target
            if len(self.active_target_list) == 0:
                active = self.target_list.pop(0)
                self.sound = arcade.load_sound(active.chord)
                self.active_target_list.append(active)
            
            # Make sure the target hasn't collided with the defence point
            self.failure = arcade.get_distance_between_sprites(self.defence_list[0], self.active_target_list[0])
            if (self.failure < TARGET_RADIUS + DEFENCE_RADIUS):
                # write a print to file for the active_target_list[0] chord type 
                # and the "score" to represent which iteration
                result = open(f'trainingResults{run}.txt', 'w')
                result.write(f'Subject failed on round {self.score+1} on chord {self.active_target_list[0].chord}')
                result.close()
                run += 1 
            else:
                self.active_target_list[0].move_to_center(RATE_OF_TRAVEL + self.score / 50)
                if self.active_target_list[0].sound_frequency % 30 == 0:
                    arcade.play_sound(self.sound)
                if self.active_target_list[0].sound_frequency % 60 == 0:
                    timer -= 1
                if ((self.score % len(self.target_list)) == 0):
                    random.shuffle(self.target_list)
                if self.score >= 30:
                    self.active_target_list[0].draw_delay += 1
                self.active_target_list[0].sound_frequency += 1

def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()