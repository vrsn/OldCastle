import arcade
import wall_list_builder

# Constants
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Old Castle Maze"

PLAYER_CHAR_SCALING = 0.35
PLAYER_MOVEMENT_SPEED = 8

TILE_SCALING = 0.25

LEFT_VIEWPORT_MARGIN = SCREEN_WIDTH/2
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH/2
BOTTOM_VIEWPORT_MARGIN = SCREEN_HEIGHT/2
TOP_VIEWPORT_MARGIN = SCREEN_HEIGHT/2

WALL_TILE_SIZE = 32
HORIZONTAL_START = 30
VERTICAL_START = 1000


class OldCastleGame(arcade.Window):
    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Init the objects lists
        self.player_list = None
        self.wall_list = None

        # Character
        self.player_char = None

        # Define physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Create the player character
        image_source = "images/player/player_stand.png"
        self.player_char = arcade.Sprite(image_source, PLAYER_CHAR_SCALING)
        self.player_char.center_x = 500
        self.player_char.center_y = 300
        self.player_list.append(self.player_char)

        # Create the walls
        coordinate_list = wall_list_builder.create_wall_list(8, 8, VERTICAL_START, HORIZONTAL_START, WALL_TILE_SIZE)

        for coordinate in coordinate_list:
            wall = arcade.Sprite("images/obstacles/brickGrey.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        # Physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_char, self.wall_list)

        pass

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()

        self.wall_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.player_char.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_char.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_char.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_char.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Called when the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_char.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_char.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_char.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_char.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        # Move the player with the physics engine
        self.physics_engine.update()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_char.left < left_boundary:
            self.view_left -= left_boundary - self.player_char.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_char.right > right_boundary:
            self.view_left += self.player_char.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_char.top > top_boundary:
            self.view_bottom += self.player_char.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_char.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_char.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    window = OldCastleGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()