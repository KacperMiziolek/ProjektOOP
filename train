import gc
import numpy as np
import matplotlib.pyplot as plt
import pygame
from brain import Brain
from DQN import dqn
from environment import Environment
from memory_profiler import profile

pygame.init()

# Define parameters
memSize = 20
batchSize = 1
learningRate = 0.00005
gamma = 0.9
nLastStates = 4
epsilon = 1.0
epsilonDecayRate = 0.001
minEpsilon = 0.05
filepathToSave = 'model2.h5'
filepathToSave_prey = 'model3.h5'

# Create environment, brain, and experience replay memory
env = Environment()
brain = Brain((env.grid_size, env.grid_size, nLastStates), learningRate)
model = brain.model
Dqn = dqn(memSize, gamma)
brain_prey = Brain((env.grid_size, env.grid_size, nLastStates), learningRate)
Dqn_prey = dqn(memSize, gamma)
model2 = brain_prey.model

def resetstates(screenMap,nLastStates):
    # Initialize the state with the given number of channels
    currentstate = np.stack([screenMap] * nLastStates, axis=-1)
    
    return currentstate, currentstate



@profile
def main_loop():
    epoch = 0
    scores = list()
    scores2 = list()
    maxNCollected = 0
    maxNCollected_prey = 0
    nCollected = 0
    nCollected_prey = 0
    totNCollected = 0
    totNCollected_prey = 0
    epsilon = 1.0
    while True:
        env.reset()
        epoch += 1
        gameOver = False
        while not gameOver:
            screenMap = env.get_grid_state()
            currentstate, nextstate = resetstates(screenMap, nLastStates)

            # Choose actions
            if np.random.rand() < epsilon:
                action = np.random.randint(0, 4)
            else:
                qvalues = model.predict(currentstate[np.newaxis, ...])[0]
                action = np.argmax(qvalues)
            
            if np.random.rand() < epsilon:
                action_prey = np.random.randint(0, 4)
            else:
                qvalues2 = model2.predict(currentstate[np.newaxis, ...])[0]
                action_prey = np.argmax(qvalues2)

            # Update environment for predator and prey
            gameOver, reward, collected = env.update_predator_food(action)
            reward_prey, collected_prey = env.update_prey(action_prey)
            
            nCollected += collected
            nCollected_prey += collected_prey

            # Update state
            nextState = np.append(nextstate[..., 1:], currentstate[..., -1:], axis=-1)

            # Remember and train
            Dqn.remember([currentstate, action, reward, nextState], gameOver)
            Dqn_prey.remember([currentstate, action_prey, reward_prey, nextState], gameOver)
            inputs, targets = Dqn.get_batch(model, batchSize)
            model.train_on_batch(inputs, targets)
            inputs_prey, targets_prey = Dqn_prey.get_batch(model2, batchSize)
            model2.train_on_batch(inputs_prey, targets_prey)
            
            currentstate = nextState

        if nCollected > maxNCollected and nCollected > 2:
            maxNCollected = nCollected
            model.save(filepathToSave)
        if nCollected_prey > maxNCollected_prey and nCollected_prey > 15:
            maxNCollected_prey = nCollected_prey
            model2.save(filepathToSave_prey)
        totNCollected += nCollected
        nCollected = 0
        totNCollected_prey += nCollected_prey
        nCollected_prey = 0
        
        if epoch % 100 == 0 and epoch != 0:
            scores.append(totNCollected / 100)
            scores2.append(totNCollected_prey / 100)
            totNCollected = 0
            totNCollected_prey = 0
            plt.plot(scores)
            plt.xlabel('Epoch / 100')
            plt.ylabel('Average Score')
            plt.savefig('stats.png')
            plt.close()
            
            gc.collect()
        
        if epsilon > minEpsilon:
            epsilon -= epsilonDecayRate
        
        print(f'Epoch: {epoch} Current Best predator: {maxNCollected} prey: {maxNCollected_prey}')
        print(f'Epsilon: {epsilon:.5f}')

if __name__ == '__main__':
    main_loop()
    pygame.quit()
