import random
import pygame
#import numpy as np

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (247, 209, 139, 255)
SIDEBAR_COLOR = (88, 88, 88)

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 700
SIDEBAR_WIDTH = 200  # Width of the sidebar
GAME_AREA_WIDTH = SCREEN_WIDTH - SIDEBAR_WIDTH  # Width of the game area
NUM_PREY = 75
NUM_PREDATORS = 15
FOOD_AMOUNT = 1000
FOOD_RADIUS = 5
PREY_SPEED = 2
PREDATOR_SPEED = 3

RTH = 1


class Prey(pygame.sprite.Sprite):
    def __init__(self, environment):
        super().__init__()
        self.environment = environment
        self.image = pygame.Surface((8, 8))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (
        random.randint(0, self.environment.game_area_width), random.randint(0, self.environment.screen_height))
        self.speed_x = random.choice([PREY_SPEED, -PREY_SPEED])
        self.speed_y = random.choice([PREY_SPEED, -PREY_SPEED])
        self.hp = random.randint(10, 20)
        self.posReward = 3
        self.negReward = -10

    def update(self, action):
        if pygame.sprite.spritecollideany(self, self.environment.predator_group):
            self.environment.prey_group.remove(self)
            self.environment.all_sprites.remove(self)
        elif pygame.sprite.spritecollideany(self, self.environment.food_group):
            self.hp += 1

        # Update according to the action
        reward = 0
        collected = 0
        game_over = 0

        if action == 0:  # Move up
            self.rect.y -= self.speed_y
        elif action == 1:  # Move down
            self.rect.y += self.speed_y
        elif action == 2:  # Move right
            self.rect.x += self.speed_x
        elif action == 3:  # Move left
            self.rect.x -= self.speed_x

        if self.rect.left <= 0 or self.rect.right >= self.environment.game_area_width:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0 or self.rect.bottom >= self.environment.screen_height:
            self.speed_y = -self.speed_y

        if pygame.sprite.spritecollideany(self, self.environment.food_group):
            reward = self.posReward
            collected += 1
        if pygame.sprite.spritecollideany(self, self.environment.predator_group):
            reward = self.negReward

        if len(self.environment.prey_group) == 0:
            game_over = 1

        return reward, collected, game_over


class Predator(pygame.sprite.Sprite):
    def __init__(self, environment):
        super().__init__()
        self.environment = environment
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (
        random.randint(0, self.environment.game_area_width), random.randint(0, self.environment.screen_height))
        self.speed_x = random.choice([PREDATOR_SPEED, -PREDATOR_SPEED])
        self.speed_y = random.choice([PREDATOR_SPEED, -PREDATOR_SPEED])
        self.hp = random.randint(14, 28)
        self.posReward = 3
        self.negReward = -10
        self.defReward = -0.03

    def update(self, action):
        if pygame.sprite.spritecollideany(self, self.environment.prey_group):
            self.hp += 3

        # Update according to the action
        reward = 0
        collected = 0
        game_over = 0

        if action == 0:  # Move up
            self.rect.y -= self.speed_y
        elif action == 1:  # Move down
            self.rect.y += self.speed_y
        elif action == 2:  # Move right
            self.rect.x += self.speed_x
        elif action == 3:  # Move left
            self.rect.x -= self.speed_x

        if self.rect.left <= 0 or self.rect.right >= self.environment.game_area_width:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0 or self.rect.bottom >= self.environment.screen_height:
            self.speed_y = -self.speed_y

        if pygame.sprite.spritecollideany(self, self.environment.prey_group):
            reward = self.posReward
            collected += 1
        if self.hp == 0:
            reward = self.negReward

        if len(self.environment.predator_group) == 0:
            game_over = 1

        return reward, collected, game_over


class Food(pygame.sprite.Sprite):
    def __init__(self, environment):
        super().__init__()
        self.environment = environment
        self.image = pygame.Surface((4, 4))
        self.rth = RTH
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (
        random.randint(0, self.environment.game_area_width), random.randint(0, self.environment.screen_height))

    def update(self):
        if pygame.sprite.spritecollideany(self, self.environment.prey_group):
            self.environment.food_group.remove(self)
            self.environment.all_sprites.remove(self)
        self.rect.x = max(0, min(self.environment.game_area_width, self.rect.x))
        self.rect.y = max(0, min(self.environment.screen_height, self.rect.y))


class Environment:
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.game_area_width = GAME_AREA_WIDTH
        self.all_sprites = pygame.sprite.Group()
        self.prey_group = pygame.sprite.Group()
        self.predator_group = pygame.sprite.Group()
        self.food_group = pygame.sprite.Group()
        pygame.time.set_timer(pygame.USEREVENT, 4000)

        self.reset()

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

    def update(self):
        game_over = 0
        for prey in self.prey_group:
            reward, collected, game_over = prey.update(action=random.randint(0, 3))
            if game_over == 1:
                return game_over

        for predator in self.predator_group:
            reward, collected, game_over = predator.update(action=random.randint(0, 3))
            if game_over == 1:
                return game_over

        for food in self.food_group:
            food.update()

        if len(self.prey_group) == 0 or len(self.predator_group) == 0:
            game_over = 1

        return game_over


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Savannah Simulation")

environment = Environment()

font = pygame.font.Font(None, 36)

# Create a sidebar surface
sidebar_surface = pygame.Surface((SIDEBAR_WIDTH, SCREEN_HEIGHT))
sidebar_surface.fill(SIDEBAR_COLOR)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            for prey in environment.prey_group:
                prey.hp -= 1
                if prey.hp <= 0:
                    environment.prey_group.remove(prey)
                    environment.all_sprites.remove(prey)
            for predator in environment.predator_group:
                predator.hp -= 1
                if predator.hp <= 0:
                    environment.predator_group.remove(predator)
                    environment.all_sprites.remove(predator)

            #if len(environment.prey_group) == 0 or len(environment.predator_group) == 0:
             #   environment.reset()

    game_over = environment.update()
    if game_over == 1:
        print("Game Over")
        environment.reset()

    prey_count = len(environment.prey_group)
    predator_count = len(environment.predator_group)

    # Clear the sidebar surface
    sidebar_surface.fill(SIDEBAR_COLOR)

    prey_text = font.render("Prey: {}".format(prey_count), True, WHITE)
    predator_text = font.render("Predators: {}".format(predator_count), True, WHITE)

    prey_rect = prey_text.get_rect()
    prey_rect.topleft = (10, 10)

    predator_rect = predator_text.get_rect()
    predator_rect.topleft = (10, 60)

    screen.fill(BACKGROUND_COLOR)  # Fill the screen with the background color
    environment.all_sprites.draw(screen)

    # Blit the text surfaces onto the sidebar surface
    sidebar_surface.blit(prey_text, prey_rect)
    sidebar_surface.blit(predator_text, predator_rect)

    # Blit the sidebar onto the screen
    screen.blit(sidebar_surface, (GAME_AREA_WIDTH, 0))

    pygame.draw.line(screen, BLACK, (GAME_AREA_WIDTH, 0), (GAME_AREA_WIDTH, SCREEN_HEIGHT), 3)
    pygame.display.flip()

pygame.quit()
