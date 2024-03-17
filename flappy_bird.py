import pygame
import random
import neural_network as nn

# pygame clock and screen initialization
pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# scaled up images
SCALE = 1.75

#FPS
FPS = 144

# Background images
sky_image = pygame.image.load("assets/background-day.png")
sky_image = pygame.transform.scale(sky_image, (int(sky_image.get_width() * SCALE), int(sky_image.get_height() * SCALE)))

ground_image = pygame.image.load("assets/base.png")
ground_image = pygame.transform.scale(ground_image, (int(ground_image.get_width() * SCALE), int(ground_image.get_height() * SCALE/1.75)))

# RectangleCollider
# Creates a rectangle using a top left coordinate and a width and height
# Used for collision detection
class RectangleCollider:
    # Constructor
    def __init__(self, position_left, position_top, width, height):
        self.position_left = position_left
        self.position_top = position_top
        self.width = width
        self.height = height
    # Updating the rectangle's position
    def update(self, position_left, position_top):
        self.position_left = position_left
        self.position_top = position_top

# CircleCollider
# Creates a circle around a center with a radius
# Used for collision deteciton
class CircleCollider:
    # Constructor
    def __init__(self, position_x, position_y, radius):
        self.position_x = position_x
        self.position_y = position_y
        self.radius = radius
    # Updating the circle's position
    def update(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y
 
# death_check
# Takes in a bird and a pipe and returns true if there's ever a collision
# between the bird/pipe or the bird and the floor
def death_check(player, pipe_array):
    for pipe in pipe_array:
        player_center = [player.collider.position_x, player.collider.position_y]
        top_pipe_center = [pipe.top_pipe_collider.position_left + pipe.top_pipe_collider.width / 2, pipe.top_pipe_collider.position_top + pipe.top_pipe_collider.height / 2]
        bottom_pipe_center = [pipe.bottom_pipe_collider.position_left + pipe.bottom_pipe_collider.width / 2, pipe.bottom_pipe_collider.position_top + pipe.top_pipe_collider.height / 2]
        distance_x =  abs(top_pipe_center[0] - player_center[0])
        distance_y_top = abs(top_pipe_center[1] - player_center[1])
        distance_y_bottom = abs(bottom_pipe_center[1] - player_center[1])
        collision_distance_x = player.collider.radius + pipe.top_pipe_collider.width / 2
        collision_distance_y = player.collider.radius + pipe.top_pipe_collider.height / 2 

        # Checks if the distance between the bird and the pipe allows for them to be touching
        if distance_x <= collision_distance_x and (distance_y_top <= collision_distance_y or distance_y_bottom <= collision_distance_y):
            return True
    
    # Checks for the bird hitting the floor or the ceiling
    floor_check = player_center[1] + player.collider.radius
    if floor_check >= 600:
        return True
    if player_center[1] < -25:
        return True
    
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
        self.bird_image = pygame.transform.scale(self.bird_image, (int(self.bird_image.get_width() * SCALE), int(self.bird_image.get_height() * SCALE)))
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
        screen.blit(self.bird_image, (position_x, position_y))
        self.collider = CircleCollider(position_x, position_y, self.RADIUS)
        #
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
            screen.blit(self.bird_image, (self.position_x - int(self.bird_image.get_width() / 2), self.position_y - int(self.bird_image.get_height() / 2)))
            self.collider.update(self.position_x, self.position_y)

    # Kills the bird
    def death(self):
        self.y_velocity = 0
        self.gravity = 0
        self.jump_force = 0
        self.dead = True

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
        self.top_pipe_collider = RectangleCollider(position_x, self.position_y - self.gap, self.WIDTH, self.HEIGHT)
        self.bottom_pipe_collider = RectangleCollider(position_x, self.position_y, self.WIDTH, self.HEIGHT)
        self.x_velocity = x_velocity

    # Moves pipe over
    def update(self, delta_time):
        if self.position_x < -68:
            self.position_x = 1131
            self.position_y = int(random.uniform(self.HIGHEST_POSITION_Y, self.LOWEST_POSITION_Y))
            self.gap = int(random.uniform(self.SMALLEST_GAP, self.LARGEST_GAP))
        screen.blit(self.top_pipe_image, (self.position_x, self.position_y - self.gap))
        self.position_x -= delta_time * self.x_velocity
        screen.blit(self.bottom_pipe_image, (self.position_x, self.position_y))
        self.top_pipe_collider.update(self.position_x, self.position_y - self.gap)
        self.bottom_pipe_collider.update(self.position_x, self.position_y)


# Game Main Method
def main():
    # Decides the speed of the game, increasing slows game, decreasing speeds up game
    GAME_SPEED_DIVIDER = 1.5

    # Keeps track of generation number
    generation = 1
    print(generation)

    # Boolean that decides when to reset the birds
    new_birds = False

    # Constants to decide how many birds are there and what percentage of birds get evolved
    NUM_FLAPPY_BIRDS = 50
    ELITISM = 0.2
    run = True

    # Initializiation of all the birds and their assigned neural networks
    player_list = []
    neural_network_list = []
    best_neural_network_list = []
    for i in range(0, NUM_FLAPPY_BIRDS):
        player_list.append(FlappyBird(100, 150, 0.09 , 3.6))
        neural_network_list.append(nn.NeuralNetwork())
    pipe_array = [Pipe(800, 2), Pipe(1200, 2), Pipe(1600, 2)]
    closest_pipe = 0

    # Game loop
    while run:
        # Exit loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    GAME_SPEED_DIVIDER = 7

        # If new birds are going to be made
        if new_birds == True:
            # Reset all the players and neural networks
            player_list = []
            neural_network_list = []

            # Keep the best bird
            player_list.append(FlappyBird(100, 200, 0.09, 3.6))
            neural_network_list.append(best_neural_network_list[0])
            generation += 1
            print(generation)
            
            # Add to the lists the new birds and neural networks based off the old ones
            for i in range(1, NUM_FLAPPY_BIRDS):
                player_list.append(FlappyBird(100, 150, 0.09 , 3.6))
                obj = nn.NeuralNetwork(best_neural_network_list[i % int(ELITISM * NUM_FLAPPY_BIRDS)])
                neural_network_list.append(obj)
                pipe_array = [Pipe(800, 2), Pipe(1200, 2), Pipe(1600, 2)]
                closest_pipe = 0
            new_birds = False

        # delta_time used to keep game objects at constistent speed
        delta_time = clock.tick(FPS) / GAME_SPEED_DIVIDER
        
        # Sky image
        screen.blit(sky_image, (0, -125))

        # Update the pipes
        for pipe in pipe_array:
            pipe.update(delta_time)

        # Ground image
        screen.blit(ground_image, (0, 600))

        # closest_pipe stores which pipe to pull data from for the inputs to the neural network
        for pipe_index in range(0, 3):
            if pipe_array[pipe_index].position_x < 20:
                closest_pipe = (pipe_index + 1) % 3

        # Iterate through each birds and update their position based on velocity and gravity
        # Check to see if any of them died
        for i in range(0, NUM_FLAPPY_BIRDS):
            player_list[i].update(delta_time)
            if death_check(player_list[i], pipe_array):
                player_list[i].death()
        
        # Iterate through the birds and update their inputs, if the activation value  of the bird
        # based on the inputs is above 0.99, jump
        for i in range(0, NUM_FLAPPY_BIRDS):
            neural_network_list[i].update_inputs([player_list[i].position_y, player_list[i].y_velocity, pipe_array[closest_pipe].position_x, pipe_array[closest_pipe].position_y, pipe_array[closest_pipe].position_y + pipe_array[closest_pipe].gap - pipe_array[closest_pipe].HEIGHT / 2])
            if neural_network_list[i].activation() >= 0.99:
                player_list[i].jump()
            if player_list[i].dead == False:
                neural_network_list[i].fitness_score += delta_time
        all_dead = True

        # Iterate through the birds and check if any of them are alive
        for i in range(0, NUM_FLAPPY_BIRDS):
            if player_list[i].dead == False:
                all_dead = False

        # Clear the lists and neural networks if they are all dead
        # Save the best birds under best_neural_network_list
        if all_dead == True:
            del pipe_array
            del player_list
            del best_neural_network_list
            best_neural_network_list = []
            neural_network_list = sorted(neural_network_list, key = lambda x : x.fitness_score, reverse = True)
            for i in range(0, int(ELITISM * NUM_FLAPPY_BIRDS)):
                best_neural_network_list.append(neural_network_list[i])
            del neural_network_list
            new_birds = True
                
        pygame.display.update()

            
    pygame.quit()

main()
