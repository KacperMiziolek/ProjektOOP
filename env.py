import random
import numpy as np
import pygame

# Initialize pygame
pygame.init()

# Set up clock for controlling frame rate
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (247, 209, 139)
SIDEBAR_COLOR = (88, 88, 88)

# Set screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SIDEBAR_WIDTH = 150  # Width of the sidebar
GAME_AREA_WIDTH = SCREEN_WIDTH - SIDEBAR_WIDTH  # Width of the game area

# Simulation parameters
NUM_PREY = 50
NUM_PREDATORS = 20
FOOD_AMOUNT = 750
FOOD_RADIUS = 5
PREY_SPEED = 5
PREDATOR_SPEED = 6

# Other constants
GRID_SIZE = 20


class Prey(pygame.sprite.Sprite):
    def __init__(self, environment):
        super().__init__()
        self.environment = environment
        self.image = pygame.Surface((8, 8))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(0, self.environment.game_area_width),
            random.randint(0, self.environment.screen_height)
        )
        self.speed_x = random.choice([PREY_SPEED, -PREY_SPEED])
        self.speed_y = random.choice([PREY_SPEED, -PREY_SPEED])
        self.hp = random.randint(13, 26)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.posReward = 3
        self.negReward = -10
        self.defReward=-0.03
        self.last_negative_reward_time = pygame.time.get_ticks()
    def update(self, action):
        reward, collected = 0, 0

        # Movement
        if action == 0:  # Move up
            self.rect.y -= self.speed_y
        elif action == 1:  # Move down
            self.rect.y += self.speed_y
        elif action == 2:  # Move right
            self.rect.x += self.speed_x
        elif action == 3:  # Move left
            self.rect.x -= self.speed_x

        # Screen boundaries
        if self.rect.left <= 0 or self.rect.right >= self.environment.game_area_width:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0 or self.rect.bottom >= self.environment.screen_height:
            self.speed_y = -self.speed_y

        # Collision detection
        if pygame.sprite.spritecollideany(self, self.environment.food_group):
            reward = self.posReward
            collected += 1
            self.hp += 1  # Eating food restores HP

        if pygame.sprite.spritecollideany(self, self.environment.predator_group):
            reward = self.negReward
            self.environment.prey_group.remove(self)
            self.environment.all_sprites.remove(self)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_negative_reward_time >= 1000:  # 1 second
            for _ in self.environment.prey_group:
                reward -= 0.03  # Apply negative reward to prey
            self.last_negative_reward_time = current_time
        return reward, collected

class Predator(pygame.sprite.Sprite):
    def __init__(self, environment):
        super().__init__()
        self.environment = environment
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(0, self.environment.game_area_width),
            random.randint(0, self.environment.screen_height)
        )
        self.speed_x = random.choice([PREDATOR_SPEED, -PREDATOR_SPEED])
        self.speed_y = random.choice([PREDATOR_SPEED, -PREDATOR_SPEED])
        self.hp = random.randint(14, 28)
        self.posReward = 3
        self.negReward = -10
        self.defReward = -0.03
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.last_negative_reward_time = pygame.time.get_ticks()
    def update(self, action):
        reward, collected = 0, 0

        # Movement
        if action == 0:  # Move up
            self.rect.y -= self.speed_y
        elif action == 1:  # Move down
            self.rect.y += self.speed_y
        elif action == 2:  # Move right
            self.rect.x += self.speed_x
        elif action == 3:  # Move left
            self.rect.x -= self.speed_x

        # Screen boundaries
        if self.rect.left <= 0 or self.rect.right >= self.environment.game_area_width:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0 or self.rect.bottom >= self.environment.screen_height:
            self.speed_y = -self.speed_y

        # Collision detection
        if pygame.sprite.spritecollideany(self, self.environment.prey_group):
            reward = self.posReward
            collected += 1
            self.hp += 3  # Eating prey restores HP

        if self.hp <= 0:
            reward = self.negReward
            self.environment.predator_group.remove(self)
            self.environment.all_sprites.remove(self)
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_negative_reward_time >= 1000:  # 1 second
            for _ in self.environment.predator_group:
                reward -= 0.03  # Apply negative reward to prey
            self.last_negative_reward_time = current_time    
        
        return reward, collected

class Food(pygame.sprite.Sprite):
    def __init__(self, environment):
        super().__init__()
        self.environment = environment
        self.image = pygame.Surface((4, 4))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(0, self.environment.game_area_width),
            random.randint(0, self.environment.screen_height)
        )

    def update(self):
        if pygame.sprite.spritecollideany(self, self.environment.prey_group):
            self.environment.food_group.remove(self)
            self.environment.all_sprites.remove(self)

class Environment:
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.game_area_width = GAME_AREA_WIDTH
        self.all_sprites = pygame.sprite.Group()
        self.prey_group = pygame.sprite.Group()
        self.predator_group = pygame.sprite.Group()
        self.food_group = pygame.sprite.Group()
        self.grid_size=GRID_SIZE
        self.reset()
        self.backgroundcolor = BACKGROUND_COLOR
        # Add variables to track last HP update time
        self.last_hp_update_time = pygame.time.get_ticks()
    def reset(self):
        self.all_sprites.empty()
        self.prey_group.empty()
        self.predator_group.empty()
        self.food_group.empty()

        for _ in range(NUM_PREY):
            prey = Prey(self)
            self.all_sprites.add(prey)
            self.prey_group.add(prey)

        for _ in range(FOOD_AMOUNT):
            food = Food(self)
            self.all_sprites.add(food)
            self.food_group.add(food)

        for _ in range(NUM_PREDATORS):
            predator = Predator(self)
            self.all_sprites.add(predator)
            self.predator_group.add(predator)

    def update_hp(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hp_update_time >= 4000:  # 4 seconds
            for predator in self.predator_group:
                predator.hp -= 2

                if predator.hp <= 0:
                    self.predator_group.remove(predator)
                    self.all_sprites.remove(predator)
            for prey in self.prey_group:
                prey.hp -= 3
                if prey.hp <= 0:
                    self.prey_group.remove(prey)
                    self.all_sprites.remove(prey)
            self.last_hp_update_time = current_time

    def update_predator_food(self, action):
        self.update_hp()
        game_over = 0
        reward = 0  # Initialize reward variable
        collected = 0  # Initialize collected variable

        for predator in self.predator_group:
            # Unpack the values from the update method correctly
            predator_reward, predator_collected = predator.update(action)
            reward += predator_reward  # Accumulate rewards
            collected += predator_collected  # Accumulate collected items

        for food in self.food_group:
            food.update()

        if len(self.prey_group) == 0 or len(self.predator_group) == 0:
            print(len(self.prey_group))
            print(len(self.predator_group))
            game_over = 1
        return game_over, reward, collected

    def update_prey(self, action):
        self.update_hp()
        reward = 0
        collected_food = 0
        for prey in self.prey_group:
            prey_reward, prey_collected = prey.update(action)
            reward += prey_reward
            collected_food += prey_collected
        return reward, collected_food

    def get_grid_state(self):
        # Initialize the grid with zeros
        grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        CELL_HEIGHT=60
        CELL_WIDTH=60
        CELL_HEIGHT_PREDATOR=50
        CELL_WIDTH_PREDATOR=50
        # Place prey on the grid
        for prey in self.prey_group:
            grid_x =abs(prey.rect.x // CELL_WIDTH)
            grid_y =abs(prey.rect.y // CELL_HEIGHT)
            grid[grid_y, grid_x] = 1  # Prey is represented by 1

        # Place predators on the grid
        for predator in self.predator_group:
            grid_x = abs(predator.rect.x // CELL_WIDTH_PREDATOR)
            grid_y = abs(predator.rect.y // CELL_HEIGHT_PREDATOR)
            grid[grid_y, grid_x] = 2  # Predator is represented by 2

        # Place food on the grid
        for food in self.food_group:
            grid_x = abs(food.rect.x // CELL_WIDTH)
            grid_y = abs(food.rect.y // CELL_HEIGHT)
            grid[grid_y, grid_x] = 3  # Food is represented by 3

        
        return grid

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Savannah Simulation")

    environment = Environment()

    font = pygame.font.SysFont(None, 24)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(environment.backgroundcolor)

        # Update and draw all sprites
        
        environment.all_sprites.draw(screen)

        # Draw the sidebar
        pygame.draw.rect(screen, SIDEBAR_COLOR, (GAME_AREA_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
        environment.update_predator_food(action=random.randint(0,4))
        environment.update_prey(action=random.randint(0,4))
        # Render text on the sidebar
        prey_count_text = font.render(f"Prey: {len(environment.prey_group)}", True, WHITE)
        screen.blit(prey_count_text, (GAME_AREA_WIDTH + 10, 10))

        predator_count_text = font.render(f"Predators: {len(environment.predator_group)}", True, WHITE)
        screen.blit(predator_count_text, (GAME_AREA_WIDTH + 10, 30))

        food_count_text = font.render(f"Food: {len(environment.food_group)}", True, WHITE)
        screen.blit(food_count_text, (GAME_AREA_WIDTH + 10, 50))

        # Get the current state of the environment
        state = environment.get_grid_state()
        print(state)  # For debugging purposes, print the state
        if len(environment.predator_group) == 0 or len(environment.prey_group) == 0:
            environment.reset()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
