# Import the pygame module
import pygame
# Import random for random numbers.
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('jet.png').convert()
        self.surf.set_colorkey((255, 255, 255),RLEACCEL)
        self.rect = self.surf.get_rect()

    # Move the sprite based on user keypresses.
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep the player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object by extending pygame,sprite.Sprite
# The surface you draw on the screen is now an attribute of enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load('missile.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # To move the sprite based on speed and
    # remove the sprite when it passes off the edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load('cloud.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
                                             )
        )
        # Move the cloud based on a constant speed
        # Remove the cloud once it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Setup for music and sound playback. Defaults are good.
pygame.mixer.init()


# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy and new cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load and play background music
# Sound and Source: Chris Bailey - artist Tripnet
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load('Sky_dodge_theme.ogg')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.2)

# Load all the sound files
# Sound sources Chris Bailey
move_up_sound = pygame.mixer.Sound('Jet_up.ogg')
move_down_sound = pygame.mixer.Sound('Jet_down.ogg')
collision_sound = pygame.mixer.Sound('Boom.ogg')

# Adjust the volumn of the sounds
move_up_sound.set_volume(0.6)
move_down_sound.set_volume(0.6)
collision_sound.set_volume(1.5)

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create a new enemy and add it to the sprite group
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add (new_enemy)

        # Add a new cloud?
        elif event.type == ADDCLOUD:
            # Create a new cloud and add it to the sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Get the set of keys pressed and check for user input.
    pressed_keys = pygame.key.get_pressed()

    # Update player sprite based on user keypresses
    player.update(pressed_keys)

    # Update enemy position and clouds
    enemies.update()
    clouds.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # check if any enemies have collided with player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()

        # Stop and moving sounds, music, and play collision
        move_up_sound.stop()
        move_down_sound.stop()
        pygame.mixer.music.stop()
        pygame.time.delay(50)
        collision_sound.play()
        pygame.time.delay(50)

        # Stop the loop
        running = False

    # Update everything in the display
    pygame.display.flip()

    # Ensure the game maintains a rate of 30 frames per second
    clock.tick(30)

# All done, stop and quit the mixer.

pygame.mixer.quit()

