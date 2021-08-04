import arcade
import wall_list_builder

# Constants
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Old Castle Maze"

PLAYER_CHAR_SCALING = 0.35
PLAYER_MOVEMENT_SPEED = 8

LEFT_VIEWPORT_MARGIN = SCREEN_WIDTH / 2
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH / 2
BOTTOM_VIEWPORT_MARGIN = SCREEN_HEIGHT / 2
TOP_VIEWPORT_MARGIN = SCREEN_HEIGHT / 2


TILE_SCALING = 0.25
WALL_TILE_SIZE = 128 * TILE_SCALING
MAZE_STARTING_WIDTH = 4
MAZE_STARTING_HEIGHT = 4

# TODO: Create a menu to control the game
# TODO: Track the time for each level
# TODO: Add animation to character movement
# TODO: Think about the obstacles

class OldCastleGame(arcade.Window):
    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Init the objects lists
        self.player_list = None
        self.wall_list = None
        self.coin_list = None

        # Character
        self.player_char = None

        # Define physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Sound
        self.collect_coin_sound = arcade.load_sound("sounds/coin1.wav")

        # Set background color
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # Initialize global counters
        self.coin_counter = None
        self.maze_size = 0

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # As we are using 5 bricks to build a wall, we are using this magic number.
        # TODO: Fix magic numbers with the constants. Change logic in the maze_generator accordingly.
        maze_cell_width = MAZE_STARTING_WIDTH + self.maze_size
        maze_cell_height = MAZE_STARTING_HEIGHT + self.maze_size
        maze_width = maze_cell_width * 5 * WALL_TILE_SIZE
        maze_height = maze_cell_height * 5 * WALL_TILE_SIZE
        vertical_start = WALL_TILE_SIZE + maze_height

        self.coin_counter = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        # Create the player character
        image_source = "images/player/player_stand.png"
        self.player_char = arcade.Sprite(image_source, PLAYER_CHAR_SCALING)
        self.player_char.center_x = (vertical_start - WALL_TILE_SIZE) / 2 + WALL_TILE_SIZE
        self.player_char.center_y = (WALL_TILE_SIZE + maze_width) / 2 + WALL_TILE_SIZE
        self.player_list.append(self.player_char)

        # Create the walls
        print(WALL_TILE_SIZE)
        coordinate_list = wall_list_builder.create_wall_list(
                        maze_cell_width,
                        maze_cell_height,
                        vertical_start,
                        WALL_TILE_SIZE,
                        WALL_TILE_SIZE
        )

        for coordinate in coordinate_list:
            wall = arcade.Sprite("images/obstacles/brickGrey.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        # Create coins in 4 corners of the maze
        coin_coordinates = [
            ((WALL_TILE_SIZE * 4.5), (maze_height - WALL_TILE_SIZE * 1.5)),                 # top left
            ((maze_width - WALL_TILE_SIZE * 0.5), (maze_height - WALL_TILE_SIZE * 1.5)),    # top right
            ((maze_width - WALL_TILE_SIZE * 0.5), (WALL_TILE_SIZE * 3.5)),                  # bottom right
            ((WALL_TILE_SIZE * 4.5), (WALL_TILE_SIZE * 3.5))                                # bottom left
        ]

        for coordinate in coin_coordinates:
            new_coin = arcade.Sprite("images/items/coinGold.png", TILE_SCALING)
            new_coin.position = coordinate
            self.coin_list.append(new_coin)

        # Physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_char, self.wall_list)

        pass

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()

        self.wall_list.draw()
        self.player_list.draw()
        self.coin_list.draw()

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
        elif key == arcade.key.ENTER:
            if self.coin_counter == 4:
                self.maze_size += 1
                self.setup()


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

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_char, self.coin_list)

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Update coin counter
            self.coin_counter += 1

            if self.coin_counter > 3:
                # TODO change to a menu.
                print("VICTORY")

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