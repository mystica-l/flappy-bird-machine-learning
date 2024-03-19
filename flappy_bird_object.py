import pygame
import pygame_set_up as pgsu

# FlappyBird
# Contains everything for a flappy bird character
class FlappyBird():
    # Radius is used for the collision box
    RADIUS = 20
    dead = False
    # Constructor
    def __init__(self, position_x, position_y, gravity, jump_force):
        # Image creation
        self.bird_image = pygame.image.load("assets/yellowbird-upflap.png")
        self.bird_image = pygame.transform.scale(self.bird_image, (int(self.bird_image.get_width() * pgsu.SCALE), int(self.bird_image.get_height() * pgsu.SCALE)))
        self.original_bird_image = self.bird_image
        # Sets starting position x and y, gravity, and the power of the jump
        self.position_x = position_x
        self.position_y = position_y
        self.gravity = gravity
        self.jump_force = jump_force
        # Variables to feed to machine learner
        self.distance_from_ground = 0
        # Dictates the speed of the bird when falling or jumping
        self.y_velocity = 0
        # Spins bird when falling
        self.angle_orientation = 0
        # Bird appears on screen with collision
        pgsu.screen.blit(self.bird_image, (position_x, position_y))
        self.dead = False

    # Sets velocity to jump_force when jumping 
    def jump(self):
        if self.dead == False:
            self.y_velocity = -self.jump_force

    # Updates bird position using delta_time (to keep game speed fixed regardless of FPS)
    def update(self, delta_time):
        if self.dead == False:
            # Angle changing when falling
            if self.y_velocity < 1:
                if self.angle_orientation < 30:
                    self.angle_orientation += 3
                    self.bird_image = pygame.transform.rotate(self.original_bird_image, self.angle_orientation)
            else:
                if self.angle_orientation > -90:
                    self.angle_orientation -= 2
                    self.bird_image = pygame.transform.rotate(self.original_bird_image, self.angle_orientation)
            # Adjustment of position based on gravity and current velocity
            self.y_velocity += delta_time * self.gravity
            self.position_y += delta_time * self.y_velocity
            pgsu.screen.blit(self.bird_image, (self.position_x - int(self.bird_image.get_width() / 2), self.position_y - int(self.bird_image.get_height() / 2)))

    # Kills the bird
    def death(self):
        self.y_velocity = 0
        self.gravity = 0
        self.jump_force = 0
        self.dead = True