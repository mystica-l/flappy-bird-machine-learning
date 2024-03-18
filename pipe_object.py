import pygame
import collider_objects
import random
import pygame_set_up as pgsu

# Pipe class
# Creates and moves pipes across the screen that kills the birds
class Pipe:
    # Scales pipe image
    SCALE = 1.3
    
    # Random ranges for the lowest and highest the bottom pipe can be as well as the size of the gap
    LOWEST_POSITION_Y = 550
    HIGHEST_POSITION_Y = 200
    SMALLEST_GAP = 940
    LARGEST_GAP = 950

    # Width and height of the collider as determined by resolution of picture & scale
    WIDTH = 67.6
    HEIGHT = 780

    # Creates pipe with x speed at position x
    def __init__(self, position_x, x_velocity):
        self.top_pipe_image  = pygame.image.load("assets/top-pipe.png")
        self.top_pipe_image = pygame.transform.scale(self.top_pipe_image, (int(self.top_pipe_image.get_width() * self.SCALE), int(self.top_pipe_image.get_height() * self.SCALE)))
        self.bottom_pipe_image = pygame.image.load("assets/bottom-pipe.png")
        self.bottom_pipe_image = pygame.transform.scale(self.bottom_pipe_image, (int(self.bottom_pipe_image.get_width() * self.SCALE), int(self.bottom_pipe_image.get_height() * self.SCALE)))

        self.position_y = int(random.uniform(self.HIGHEST_POSITION_Y, self.LOWEST_POSITION_Y))
        self.gap = int(random.uniform(self.SMALLEST_GAP, self.LARGEST_GAP))
        self.position_x = position_x
        self.top_pipe_collider = collider_objects.RectangleCollider(position_x, self.position_y - self.gap, self.WIDTH, self.HEIGHT)
        self.bottom_pipe_collider = collider_objects.RectangleCollider(position_x, self.position_y, self.WIDTH, self.HEIGHT)
        self.x_velocity = x_velocity

    # Moves pipe over and resets it if need be
    def update(self, delta_time):
        if self.position_x < -68:
            self.position_x = 1131
            self.position_y = int(random.uniform(self.HIGHEST_POSITION_Y, self.LOWEST_POSITION_Y))
            self.gap = int(random.uniform(self.SMALLEST_GAP, self.LARGEST_GAP))
        self.position_x -= delta_time * self.x_velocity
        pgsu.screen.blit(self.top_pipe_image, (self.position_x, self.position_y - self.gap))
        pgsu.screen.blit(self.bottom_pipe_image, (self.position_x, self.position_y))
        self.top_pipe_collider.update(self.position_x, self.position_y - self.gap)
        self.bottom_pipe_collider.update(self.position_x, self.position_y)