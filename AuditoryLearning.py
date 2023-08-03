"""
Auditory Learning project.
"""
import arcade
import random
import pyautogui
import time
import csv
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane

# Screen title and size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Auditory Learning"

# Constants for sizing
TARGET_RADIUS = 18
DEFENCE_RADIUS = 40

# Constants for number of different targets
# CHORD_TYPES = 5
# CHORD_SAMPLES = 12

# CHORD_FILES = [['resources\D7_A4_Piano.wav','resources\D7_AS4_Piano.wav','resources\D7_B4_Piano.wav','resources\D7_C4_Piano.wav',
# 'resources\D7_CS4_Piano.wav','resources\D7_D4_Piano.wav','resources\D7_DS4_Piano.wav','resources\D7_E4_Piano.wav',
# 'resources\D7_F4_Piano.wav','resources\D7_FS4_Piano.wav','resources\D7_G4_Piano.wav','resources\D7_GS4_Piano.wav'],
# ['resources\FD7_A4_Piano.wav','resources\FD7_AS4_Piano.wav','resources\FD7_B4_Piano.wav','resources\FD7_C4_Piano.wav',
# 'resources\FD7_CS4_Piano.wav','resources\FD7_D4_Piano.wav','resources\FD7_DS4_Piano.wav','resources\FD7_E4_Piano.wav',
# 'resources\FD7_F4_Piano.wav','resources\FD7_FS4_Piano.wav','resources\FD7_G4_Piano.wav','resources\FD7_GS4_Piano.wav'],
# ['resources\HD7_A4_Piano.wav','resources\HD7_AS4_Piano.wav','resources\HD7_B4_Piano.wav','resources\HD7_C4_Piano.wav',
# 'resources\HD7_CS4_Piano.wav','resources\HD7_D4_Piano.wav','resources\HD7_DS4_Piano.wav','resources\HD7_E4_Piano.wav',
# 'resources\HD7_F4_Piano.wav','resources\HD7_FS4_Piano.wav','resources\HD7_G4_Piano.wav','resources\HD7_GS4_Piano.wav'],
# ['resources\M7_A4_Piano.wav','resources\M7_AS4_Piano.wav','resources\M7_B4_Piano.wav','resources\M7_C4_Piano.wav',
# 'resources\M7_CS4_Piano.wav','resources\M7_D4_Piano.wav','resources\M7_DS4_Piano.wav','resources\M7_E4_Piano.wav',
# 'resources\M7_F4_Piano.wav','resources\M7_FS4_Piano.wav','resources\M7_G4_Piano.wav','resources\M7_GS4_Piano.wav'],
# ['resources\mi7_A4_Piano.wav','resources\mi7_AS4_Piano.wav','resources\mi7_B4_Piano.wav','resources\mi7_C4_Piano.wav',
# 'resources\mi7_CS4_Piano.wav','resources\mi7_D4_Piano.wav','resources\mi7_DS4_Piano.wav','resources\mi7_E4_Piano.wav',
# 'resources\mi7_F4_Piano.wav','resources\mi7_FS4_Piano.wav','resources\mi7_G4_Piano.wav','resources\mi7_GS4_Piano.wav']]


# Control constants
CHORD_TYPES = 5
CHORD_SAMPLES = 5

CHORD_FILES = [['control\_a_ControlAudioHighNormalSpeak.wav', 'control\_a_ControlAudioHighSung.wav','control\_a_ControlAudioMaleHigh.wav',
                'control\_a_ControlAudioMaleNormal.wav', 'control\_a_ControlAudioNormalSpeak.wav'],
                ['control\_e_ControlAudioHighNormalSpeak.wav', 'control\_e_ControlAudioHighSung.wav','control\_e_ControlAudioMaleHigh.wav',
                'control\_e_ControlAudioMaleNormal.wav', 'control\_e_ControlAudioNormalSpeak.wav'],
                ['control\_i_ControlAudioHighNormalSpeak.wav', 'control\_i_ControlAudioHighSung.wav','control\_i_ControlAudioMaleHigh.wav',
                'control\_i_ControlAudioMaleNormal.wav', 'control\_i_ControlAudioNormalSpeak.wav'],
                ['control\_o_ControlAudioHighNormalSpeak.wav', 'control\_o_ControlAudioHighSung.wav','control\_o_ControlAudioMaleHigh.wav',
                'control\_o_ControlAudioMaleNormal.wav', 'control\_o_ControlAudioNormalSpeak.wav'],
                ['control\_u_ControlAudioHighNormalSpeak.wav', 'control\_u_ControlAudioHighSung.wav','control\_u_ControlAudioMaleHigh.wav',
                'control\_u_ControlAudioMaleNormal.wav', 'control\_u_ControlAudioNormalSpeak.wav']]

# Constant start points for the different chord types
CHORD_X = [SCREEN_WIDTH/4,SCREEN_WIDTH/4*3,0,SCREEN_WIDTH/2,SCREEN_WIDTH]
CHORD_Y = [0,0,SCREEN_HEIGHT/4*3,SCREEN_HEIGHT,SCREEN_HEIGHT/5*4]

# Constant for the color of the different types
TYPE_COLOR = [(122, 40, 203), (165, 1, 4), 
(176, 254, 118), (255, 190, 239), (68, 204, 255) ]

# Constant for base rate of travel
RATE_OF_TRAVEL = .5

# Global variables for number of runs, timer, and trial data
timer = 600
subject = ''
results = []

# function for centering the mouse
def center_mouse():
    screen = pyautogui.size()
    pyautogui.moveTo(screen[0] / 2, screen[1] / 2, 0)

# function to get time in seconds since epoch at start of trial
def get_time():
    return time.time_ns() / (10 ** 9) # convert to floating-point seconds

# function to calculate trial duration in partial seconds
def calc_time(start):
    return (time.time_ns() / (10 ** 9)) - start 

def add_run_to_file(subject, round, difficulty, chord, pass_fail, start_time, reaction_time):
    global results
    results.append({'subject': subject, 'round': round, 'difficulty': difficulty, 
                    'chord': chord, 'pass_fail': pass_fail, 'start_time': start_time, 
                    'reaction_time': reaction_time})

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

class GameView(arcade.View):
    """ Main application class. """

    def __init__(self):
        super().__init__()

        # Sprite list with all the targets and sprite for center.
        self.target_list = None
        self.active_target_list = None
        self.defence_list = None
        self.score = 0
        self.sound = None
        self.sound_player = None
        self.failure = 0
        self.start_timer = 0
        self.start_time = 0
        self.written = False
        self.up_delay = False
        self.draw_delay = 0

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Sprite lists with all the sprites for the program
        self.target_list = []
        self.active_target_list = arcade.SpriteList()
        self.defence_list = arcade.SpriteList()
        self.score = 0
        self.failure = 2400
        self.start_timer = timer
        self.start_time = get_time()
        self.written = False
        self.up_delay = False
        self.draw_delay = 0

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

        # Center mouse at start of round
        center_mouse()

    def on_draw(self):
        """ Render the screen. """
        global timer

        # Clear the screen
        self.clear()

        # Draw the active sprites
        if self.score >= 15:
            if self.active_target_list[0].draw_delay == self.draw_delay:
                self.active_target_list.draw()
        else:
            self.active_target_list.draw()
        self.defence_list.draw()

        # render the timer
        mins, secs = divmod(timer, 60)
        t = '{:02d}:{:02d}'.format(mins, secs)
        arcade.draw_text(t, SCREEN_WIDTH - 100, SCREEN_HEIGHT- 30)

        if timer == 0 or self.failure < TARGET_RADIUS + DEFENCE_RADIUS:
            if timer > 0:
                arcade.draw_text("Hit space to continue.", SCREEN_WIDTH/3+55, SCREEN_HEIGHT/3 * 2)
            else:
                arcade.draw_text("Thank you for your participation. Please e-mail me the Results.csv file that was created.", 85, SCREEN_HEIGHT/4 * 3)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        global timer

        # Get list of targets we've clicked on
        if timer == 0 or self.failure < TARGET_RADIUS + DEFENCE_RADIUS:
            return
        hit = arcade.get_sprites_at_point((x, y), self.active_target_list)

        # Have we clicked on a target?
        if len(hit) > 0:
            # Update data for csv
            self.score += 1
            trial_duration = calc_time(self.start_time)
            add_run_to_file(subject, self.score, self.draw_delay, 
                            self.active_target_list[0].chord, 'Pass', self.start_timer, trial_duration)
            
            # arcade.stop_sound(self.sound_player)
            # Add 1 second pause between trials
            time.sleep(1.0)

            # Remove the active target
            hit_target = self.active_target_list.pop()
            hit_target.sound_frequency = 0
            hit_target.draw_delay = 0
            self.target_list.append(hit_target)

            # Pull out the active target and activate its sound file
            active = self.target_list.pop(0)
            self.sound = arcade.load_sound(active.chord)
            self.active_target_list.append(active)

            
            self.up_delay = False
            center_mouse()
            self.start_time = get_time()
            self.start_timer = timer

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.failure < TARGET_RADIUS + DEFENCE_RADIUS:
            self.setup()


    def on_update(self, delta):
        global timer, results
        if timer > 0:
            # Make sure there is a target
            if len(self.active_target_list) == 0:
                active = self.target_list.pop(0)
                self.sound = arcade.load_sound(active.chord)
                self.active_target_list.append(active)
            
            # Make sure the target hasn't collided with the defence point
            self.failure = arcade.get_distance_between_sprites(self.defence_list[0], 
                                                               self.active_target_list[0])
            if (self.failure < TARGET_RADIUS + DEFENCE_RADIUS):
                # Update data for csv
                trial_duration = calc_time(self.start_time)
                if not self.written:
                    add_run_to_file(subject, self.score + 1, self.active_target_list[0].draw_delay, 
                                    self.active_target_list[0].chord, 'Fail', self.start_timer, 
                                    trial_duration)
                    self.written = True
            else:
                self.active_target_list[0].move_to_center(RATE_OF_TRAVEL + self.score / 100)
                if self.active_target_list[0].sound_frequency % 30 == 0:
                    self.sound_player = arcade.play_sound(self.sound)
                if self.active_target_list[0].sound_frequency % 60 == 0:
                    timer -= 1
                if ((self.score % len(self.target_list)) == 0):
                    random.shuffle(self.target_list)
                if self.score % 15 == 0 and not self.up_delay:
                    self.up_delay = True
                    self.draw_delay += 10    
                if self.active_target_list[0].draw_delay < self.draw_delay:
                    self.active_target_list[0].draw_delay += 1
                self.active_target_list[0].sound_frequency += 1
        if timer == 0:
            # Test is over
            trial_duration = calc_time(self.start_time)
            if not self.written:
                add_run_to_file(subject, self.score + 1, self.draw_delay,
                                 self.active_target_list[0].chord, 'Time Out', self.start_timer, 
                                 trial_duration)
                self.written = True

            # write to CSV file
            data_file = open('Results.csv', 'w', newline='')
            csv_writer = csv.writer(data_file)
            count = 0
            for data in results:
                if count == 0:
                    header = data.keys()
                    csv_writer.writerow(header)
                    count += 1
                csv_writer.writerow(data.values())
 
            data_file.close()

class LoginView(arcade.View):
    """ Class for a title screen and controls to start game """
    def __init__(self):
        super().__init__()
        self.manager = UIManager()
        self.manager.enable()
        self.textbox = UIInputText(x=SCREEN_WIDTH/2-100, y=SCREEN_HEIGHT/2-25, 
                                   width=200, height=50, text="")
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        bg_tex = arcade.load_texture(":resources:gui_basic_assets/window/grey_panel.png")

        self.manager.add(
            UITexturePane(
                self.textbox,
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            ))
        
    def on_draw(self):
        self.clear()
        arcade.draw_text('Please enter your participant ID and hit enter to begin', 
                         SCREEN_WIDTH/2-200, SCREEN_HEIGHT/2+75)
        self.manager.draw()


    def on_key_press(self, key, modifiers):
        """ Progress if Enter is pressed """
        global subject 
        if key == arcade.key.ENTER:
            subject = self.textbox.text
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)


def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, center_window=True)
    start_view = LoginView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()