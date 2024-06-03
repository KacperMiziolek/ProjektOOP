# Importing necessary libraries
from environment import Environment
from brain import Brain
import numpy as np
import time
import pygame
pygame.init()

# Defining parameters
nLastStates = 4
filepathToOpen = 'model2.h5'
filepathToOpen_prey = 'model3.h5'

# Creating Environment and Brain objects
env = Environment()
brain = Brain((env.screen_width, env.screen_height, nLastStates))
model = brain.load_model(filepathToOpen)
brain_prey = Brain((env.screen_width, env.screen_height, nLastStates))
model_prey = brain_prey.load_model(filepathToOpen_prey)

# Initialize the Pygame screen
screen = pygame.display.set_mode((env.screen_width, env.screen_height))
pygame.display.set_caption("Savannah Simulation")

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
            currentstate, nextstate = resetstates(screenMap, grid_size, nLastStates)
            # Predict actions
            qvalues = model.predict(currentstate)[0]
            action = np.argmax(qvalues)
            
            qvalues_prey = model_prey.predict(currentstate)[0]
            action_prey = np.argmax(qvalues_prey)
            print(qvalues)
            screenMap=env.get_grid_state()
            # Update environment
            gameOver, _, _ = env.update_predator_food(action)
            _, _ = env.update_prey(action_prey)

            # Add new game frame to next state and remove the oldest frame
            
            nextState = np.append(nextstate[:, :, :, 1:], currentstate[:, :, :, :1], axis=3)

            # Update current state
            currentState = nextState

            # Update the display
            screen.fill(env.backgroundcolor)  # Fill the screen with the background color
            env.all_sprites.draw(screen)      # Draw all sprites
            pygame.display.flip()             # Update the display
