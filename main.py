import pygame
import neural_network as nn
import flappy_bird_object as fb
import pipe_object as po
import pygame_set_up as pgsu
import button_object

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

def display_text(text, font, text_col, x, y):
    text_img = font.render(text, True, text_col)
    pgsu.screen.blit(text_img, (x, y))


# Game Main Method
def main():
    # Decides the speed of the game, increasing slows game, decreasing speeds up game
    GAME_SPEED_DIVIDER = 8

    # Boolean that decides when to reset the birds
    new_birds = False

    # Constants to decide how many birds are there and what percentage of birds get evolved
    NUM_FLAPPY_BIRDS = 50
    ELITISM = 0.2
    run = True

    
    # Keeps track of generation number
    generation = 1
    score = 0
    num_alive = NUM_FLAPPY_BIRDS

    normalSpeedButton = button_object.Button(15, 640, 120, 40, "1x Speed", (220, 220, 220), (0, 0, 0))
    doubleSpeedButton = button_object.Button(150, 640, 120, 40, "2x Speed", (220, 220, 220), (0, 0, 0))
    maxSpeedButton = button_object.Button(285, 640, 120, 40, "Max Speed", (220, 220, 220), (0, 0, 0))

    # Initializiation of all the birds and their assigned neural networks
    player_list = []
    neural_network_list = []
    best_neural_network_list = []
    for i in range(0, NUM_FLAPPY_BIRDS):
        player_list.append(fb.FlappyBird(100, 150, 0.09 , 3.6))
        neural_network_list.append(nn.NeuralNetwork())
    pipe_array = [po.Pipe(800, 2), po.Pipe(1200, 2), po.Pipe(1600, 2)]
    closest_pipe = 0

    # Game loop
    while run:
        # Exit loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if normalSpeedButton.is_clicked(pygame.mouse.get_pos()):
                    GAME_SPEED_DIVIDER = 8
                if doubleSpeedButton.is_clicked(pygame.mouse.get_pos()):
                    GAME_SPEED_DIVIDER = 4
                if maxSpeedButton.is_clicked(pygame.mouse.get_pos()):
                    GAME_SPEED_DIVIDER = 2

        # If new birds are going to be made
        if new_birds == True:
            # Reset all the players and neural networks
            player_list = []
            neural_network_list = []

            # Keep the best bird
            player_list.append(fb.FlappyBird(100, 200, 0.09, 3.6))
            neural_network_list.append(best_neural_network_list[0])
            generation += 1
            
            # Add to the lists the new birds and neural networks based off the old ones
            for i in range(1, NUM_FLAPPY_BIRDS):
                player_list.append(fb.FlappyBird(100, 150, 0.09 , 3.6))
                obj = nn.NeuralNetwork(best_neural_network_list[i % int(ELITISM * NUM_FLAPPY_BIRDS)])
                neural_network_list.append(obj)
                pipe_array = [po.Pipe(800, 2), po.Pipe(1200, 2), po.Pipe(1600, 2)]
                closest_pipe = 0
            new_birds = False
            score = 0
        num_alive = 0
        # delta_time used to keep game objects at constistent speed
        delta_time = pgsu.clock.tick(pgsu.FPS) / GAME_SPEED_DIVIDER

        score += delta_time

        # Sky image
        pgsu.screen.blit(pgsu.sky_image, (0, -125))

        # Update the pipes
        for pipe in pipe_array:
            pipe.update(delta_time)

        # Ground image
        pgsu.screen.blit(pgsu.ground_image, (0, 600))

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
            neural_network_list[i].update_inputs([player_list[i].position_y,
                                                  player_list[i].y_velocity,
                                                  pipe_array[closest_pipe].position_x,
                                                  abs(pipe_array[closest_pipe].position_y - player_list[i].position_y),
                                                  abs((pipe_array[closest_pipe].position_y - player_list[i].position_y + pipe_array[closest_pipe].gap - pipe_array[closest_pipe].HEIGHT / 2) - player_list[i].position_y)] )
            if neural_network_list[i].activation() >= 0.99:
                player_list[i].jump()
            if player_list[i].dead == False:
                neural_network_list[i].fitness_score += delta_time
        all_dead = True

        # Iterate through the birds and check if any of them are alive
        for i in range(0, NUM_FLAPPY_BIRDS):
            if player_list[i].dead == False:
                all_dead = False
                num_alive += 1

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

        display_text("Score: ", pgsu.text_font, (255, 255, 255), 5, 2)
        display_text(str(int(score)), pgsu.text_font, (255, 255, 255), 70, 2)
        display_text("Generation: ", pgsu.text_font, (255, 255, 255), 5, 25)
        display_text(str(generation), pgsu.text_font, (255, 255, 255), 120, 25)
        display_text("Num. Birds Left: ", pgsu.text_font, (255, 255, 255), 5, 50)
        display_text(str(num_alive), pgsu.text_font, (255, 255, 255), 165, 50)
        normalSpeedButton.draw(pgsu.screen)
        doubleSpeedButton.draw(pgsu.screen)
        maxSpeedButton.draw(pgsu.screen)
        pygame.display.update()

            
    pygame.quit()

main()
