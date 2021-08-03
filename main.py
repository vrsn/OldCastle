import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Old Castle"


class OldCastleGame(arcade.Window):

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Init the objects lists
        self.wall_list = None
        self.player_list = None

        # Character
        self.player_char = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        pass

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Code to draw the screen goes here


def main():
    """ Main method """
    window = OldCastleGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()