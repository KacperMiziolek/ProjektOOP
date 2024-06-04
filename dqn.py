import numpy as np
from collections import deque

class dqn:
    def __init__(self, max_memory=100, discount=0.9):
        self.memory = deque(maxlen=max_memory)
        self.discount = discount

    def remember(self, transition, game_over):
        self.memory.append([transition, game_over])

    def get_batch(self, model, batch_size=10):
        len_memory = len(self.memory)
        if len_memory == 0:
            raise ValueError("Memory is empty. No batches can be created.")
        
        num_outputs = model.output_shape[-1]
        
        # Ensure the state has the expected dimensions
        state_shape = self.memory[0][0][0].shape

        inputs = np.zeros((min(len_memory, batch_size), *state_shape), dtype=np.float32)
        targets = np.zeros((min(len_memory, batch_size), num_outputs), dtype=np.float32)

        for i, idx in enumerate(np.random.randint(0, len_memory, size=min(len_memory, batch_size))):
            current_state, action, reward, next_state = self.memory[idx][0]
            game_over = self.memory[idx][1]

            inputs[i] = current_state
            targets[i] = model.predict(current_state[np.newaxis, ...])[0]  # Add batch dimension for prediction
            Q_sa = np.max(model.predict(next_state[np.newaxis, ...])[0])
            if game_over:
                targets[i, action] = reward
            else:
                targets[i, action] = reward + self.discount * Q_sa

        return inputs, targets
