import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
TILE_SCALING_2 = 0.76
COIN_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

LEFT_VIEWPORT_MARGIN = 230
RIGHT_VIEWPORT_MARGIN = 230
TOP_VIEWPORT_MARGIN = 100
BOTTOM_VIEWPORT_MARGIN = 50


class MyGame(arcade.Window):

    def __init__(self):
        super(MyGame, self).__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_list = None
        self.coin_list = None
        self.wall_list = None

        self.player_sprite = None

        self.physics_engine = None

        self.view_bottom = 0
        self.view_left = 0

        self.score = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("C:/Users/Vlad/Desktop/Python/Arcade games/platform_tutorial/"
                                                    "sounds/coin4.wav")
        self.jump_sound = arcade.load_sound("C:/Users/Vlad/Desktop/Python/Arcade games/platform_tutorial/"
                                            "sounds/jump2.wav")

        arcade.set_background_color((100, 149, 237))

    def setup(self):

        # Used to keep track of our scoring
        self.view_bottom = 0
        self.view_left = 0

        self.score = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        image_source = "C:/Users/Vlad/Desktop/Python/Arcade games/platform_tutorial/images/player_1/player_stand.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 105
        self.player_list.append(self.player_sprite)

        # Adding grass tiles on the ground
        for x in range(0, 1250, 64):
            wall = arcade.Sprite("C:/Users/Vlad/Desktop/Python/Arcade games/platform_tutorial/images/"
                                 "tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Adding some grass tiles in the air
        for x in range(550, 750, 195):
            wall = arcade.Sprite("C:/Users/Vlad/Desktop/Python/Arcade games/platform_tutorial/images/"
                                 "tiles/grassHalf.png", TILE_SCALING_2)
            wall.center_x = x
            wall.center_y = 320
            self.wall_list.append(wall)

        # Adding crate obstacles
        coordinate_list = [[512, 96],
                           [256, 96],
                           [768, 96]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite("C:/Users/Vlad/Desktop/Python/Arcade games/platform_tutorial/images/tiles/"
                                 "boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        # Adding reversed spikes in the air
        coordinate_list_2 = [[55, 450],
                             [200, 450]]

        for coordinate in coordinate_list_2:
            wall = arcade.Sprite("C:/Users/Vlad/Desktop/Python/Arcade games/platform_tutorial/images/tiles/"
                                 "spikes.png", TILE_SCALING, flipped_vertically=True)
            wall.position = coordinate
            self.wall_list.append(wall)

        # Using a loop to add coins for our hero to collect
        for x in range(128, 1250, 256):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.coin_list.append(coin)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        arcade.start_render()

        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):

        self.physics_engine.update()

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)

            self.score += 1

        changed = False

        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
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

    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
