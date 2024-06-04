import numpy as np
import time
import pygame
from environment import Environment
from brain import Brain

# Initialize Pygame
pygame.init()

# Define parameters
nLastStates = 4
filepathToOpen = 'model2.h5'
filepathToOpen_prey = 'model3.h5'

# Create Environment and Brain objects
env = Environment()
brain = Brain((env.screen_width, env.screen_height, nLastStates))
model = brain.load_model(filepathToOpen)
brain_prey = Brain((env.screen_width, env.screen_height, nLastStates))
model_prey = brain_prey.load_model(filepathToOpen_prey)

# Initialize the Pygame screen
screen = pygame.display.set_mode((env.screen_width, env.screen_height))
pygame.display.set_caption("Savannah Simulation")

# Load the background image
background_image = pygame.image.load('savanna1.png')

# Function to reset game states
def resetstates(screenMap, grid_size, nLastStates):
    # Reshape screenMap into a 2D grid
    grid = np.reshape(screenMap, (grid_size, grid_size))
    
    # Initialize currentstate as a 3D array with shape (grid_size, grid_size, nLastStates)
    currentstate = np.zeros((grid_size, grid_size, nLastStates), dtype=np.float32)
    
    # Fill the last channel with the grid representation
    currentstate[:, :, -1] = grid

    return np.expand_dims(currentstate, axis=0), np.expand_dims(currentstate, axis=0)

# Main loop
font = pygame.font.SysFont(None, 24)

while True:
    # Handle Pygame events to prevent the window from becoming unresponsive
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Resetting the game and game states
    env.reset()
    gameOver = False
    last_action_time = time.time()

    # Game loop
    while not gameOver:
        # Handle Pygame events within the game loop as well
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Choose actions to perform every 10 milliseconds
        if time.time() - last_action_time >= 0.01:
            last_action_time = time.time()
            screenMap = env.get_grid_state()
            grid_size = env.grid_size  # Ensure grid_size is correctly defined
            currentstate, _ = resetstates(screenMap, grid_size, nLastStates)

            # Predict actions for predators and prey
            qvalues = model.predict(currentstate)[0]
            action = np.argmax(qvalues)
            
            qvalues_prey = model_prey.predict(currentstate)[0]
            action_prey = np.argmax(qvalues_prey)
            
            # Update environment
            gameOver, _, _ = env.update_predator_food(action)
            _, _ = env.update_prey(action_prey)

            # Add new game frame to next state and remove the oldest frame
            nextstate = np.append(currentstate[:, :, :, 1:], currentstate[:, :, :, :1], axis=3)

            # Update current state
            currentstate = nextstate

            # Draw the background image
            screen.blit(background_image, (0, 0))

            # Draw all sprites
            env.all_sprites.draw(screen)

            # Draw the sidebar
            pygame.draw.rect(screen, env.sidebar_color, (env.game_area_width, 0, env.sidebar_width, env.screen_height))
            prey_count_text = font.render(f"Prey: {len(env.prey_group)}", True, env.white)
            screen.blit(prey_count_text, (env.game_area_width + 10, 10))
            predator_count_text = font.render(f"Predators: {len(env.predator_group)}", True, env.white)
            screen.blit(predator_count_text, (env.game_area_width + 10, 30))
            food_count_text = font.render(f"Food: {len(env.food_group)}", True, env.white)
            screen.blit(food_count_text, (env.game_area_width + 10, 50))

            pygame.display.flip()  # Update the display
