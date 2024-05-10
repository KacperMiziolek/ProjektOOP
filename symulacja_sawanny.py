
import random 
import pygame
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (247,209,139,255)
SIDEBAR_COLOR = (88,88,88)

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 700
SIDEBAR_WIDTH = 200  # Width of the sidebar
GAME_AREA_WIDTH = SCREEN_WIDTH - SIDEBAR_WIDTH  # Width of the game area
NUM_PREY = 75
NUM_PREDATORS = 15
FOOD_AMOUNT = 1000
FOOD_RADIUS = 5
PREY_SPEED = 4
PREDATOR_SPEED = 5

RTH = 1

class Prey(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        #self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, GAME_AREA_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.speed = PREY_SPEED
        self.hp = random.randint(10, 20)

    def update(self):
        if pygame.sprite.spritecollideany(self, predator_group):
            prey_group.remove(self)
            all_sprites.remove(self)
        elif pygame.sprite.spritecollideany(self, food_group):
            self.hp += 1
        self.rect.x += random.randint(-self.speed, self.speed)
        self.rect.y += random.randint(-self.speed, self.speed)
        self.rect.x = max(0, min(GAME_AREA_WIDTH, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT, self.rect.y))


class Predator(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, GAME_AREA_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.speed = PREDATOR_SPEED
        self.hp = random.randint(14, 28)

    def update(self, prey_group):
        if pygame.sprite.spritecollideany(self, prey_group):
            self.hp += 3
        distance = 1
        if distance != 0:
            self.rect.x += random.randint(-self.speed, self.speed)
            self.rect.y += random.randint(-self.speed, self.speed)
        self.rect.x = max(0, min(GAME_AREA_WIDTH, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT, self.rect.y))


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.rth = RTH
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, GAME_AREA_WIDTH), random.randint(0, SCREEN_HEIGHT))

    def update(self):
        if pygame.sprite.spritecollideany(self, prey_group):
            food_group.remove(self)
            all_sprites.remove(self)
        self.rect.x = max(0, min(GAME_AREA_WIDTH, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT, self.rect.y))


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Savannah Simulation")

all_sprites = pygame.sprite.Group()
prey_group = pygame.sprite.Group()
predator_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()
pygame.time.set_timer(pygame.USEREVENT, 4000)

for _ in range(NUM_PREY):
    prey = Prey()
    all_sprites.add(prey)
    prey_group.add(prey)


for _ in range(FOOD_AMOUNT):
    food = Food()
    all_sprites.add(food)
    food_group.add(food)



for _ in range(NUM_PREDATORS):
    predator = Predator()
    all_sprites.add(predator)
    predator_group.add(predator)

game_over = 0

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
            for prey in prey_group:
                prey.hp -= 1
                if prey.hp <= 0:
                    prey_group.remove(prey)
                    all_sprites.remove(prey)
            for predator in predator_group:
                predator.hp -= 1
                if predator.hp <= 0:
                    predator_group.remove(predator)
                    all_sprites.remove(predator)
        elif game_over:
            running = False

    prey_count = len(prey_group)
    predator_count = len(predator_group)

    # Clear the sidebar surface
    sidebar_surface.fill(SIDEBAR_COLOR)

    prey_text = font.render("Prey: {}".format(prey_count), True, WHITE)
    predator_text = font.render("Predators: {}".format(predator_count), True, WHITE)

    prey_rect = prey_text.get_rect()
    prey_rect.topleft = (10, 10)

    predator_rect = predator_text.get_rect()
    predator_rect.topleft = (10, 60)

    prey_group.update()
    predator_group.update(prey_group)
    food_group.update()

    screen.fill(BACKGROUND_COLOR)  # Fill the screen with the background color
    all_sprites.draw(screen)

    # Blit the text surfaces onto the sidebar surface
    sidebar_surface.blit(prey_text, prey_rect)
    sidebar_surface.blit(predator_text, predator_rect)

    # Blit the sidebar onto the screen
    screen.blit(sidebar_surface, (GAME_AREA_WIDTH, 0))

    pygame.draw.line(screen, BLACK, (GAME_AREA_WIDTH, 0), (GAME_AREA_WIDTH, SCREEN_HEIGHT), 3)
    pygame.display.flip()

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
