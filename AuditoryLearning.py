"""
Auditory Learning project.
"""
import arcade
import random

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Auditory Learning"

# Constants for sizing
TARGET_RADIUS = 15
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
CHORD_X = [0,10,15,5,20]
CHORD_Y = [5,15,10,0,20]

# Constant for the color of the different types
TYPE_COLOR = [arcade.color.AIR_FORCE_BLUE, arcade.color.ANDROID_GREEN, 
arcade.color.BANANA_YELLOW, arcade.color.BRILLIANT_ROSE, arcade.color.CYBER_GRAPE]

# Constant for base rate of travel
RATE_OF_TRAVEL = .5

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

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Sprite lists with all the sprites for the program
        self.target_list = []
        self.active_target_list = arcade.SpriteList()
        self.defence_list = arcade.SpriteList()

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
        # Clear the screen
        self.clear()

        # Draw the active sprites
        if self.score >= 30:
            if self.active_target_list[0].draw_delay >= 15:
                self.active_target_list.draw()
        else:
            self.active_target_list.draw()
        self.defence_list.draw()

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

    def on_update(self, delta):
        # Make sure there is a target
        if len(self.active_target_list) == 0:
            active = self.target_list.pop(0)
            self.sound = arcade.load_sound(active.chord)
            self.active_target_list.append(active)
        
        # Make sure the target hasn't collided with the defence point
        failure = arcade.get_distance_between_sprites(self.defence_list[0], self.active_target_list[0])
        if (failure < TARGET_RADIUS + DEFENCE_RADIUS):
            # write a print to file for the active_target_list[0] chord type 
            # and the "score" to represent which iteration  
            x = 0
        else:
            self.active_target_list[0].move_to_center(RATE_OF_TRAVEL + self.score / 50)
            if self.active_target_list[0].sound_frequency % 30 == 0:
                arcade.play_sound(self.sound)
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