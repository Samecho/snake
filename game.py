# 1. Import modules
import pygame
import sys 
import random

# 2.Initialize pygame
pygame.init()

pygame.mixer.music.load("bgm.wav")    
pygame.mixer.music.play(-1)           
pygame.mixer.music.set_volume(0.5)     

# 3. Define game settings
backgroundColor = (128,192,255)
snakeColor = (64,192,0)
headColor = (32,96,0)
fruitColor = (255,128,128)

screenWidth = 750
screenHeight = 750
cellSize = 25
numberOfCell = int(screenWidth / cellSize)
frames = 60
screen = pygame.display.set_mode((screenWidth,screenHeight))
clock = pygame.time.Clock()
score = 0

MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 150)

# 4. Initialize snake
class SNAKE:
    def __init__(self):
        self.body = [pygame.math.Vector2(numberOfCell // 2, numberOfCell // 2),
                     pygame.math.Vector2(numberOfCell // 2, numberOfCell // 2),
                     pygame.math.Vector2(numberOfCell // 2, numberOfCell // 2),
                     pygame.math.Vector2(numberOfCell // 2, numberOfCell // 2),
                     pygame.math.Vector2(numberOfCell // 2, numberOfCell // 2)]

direction = 0 #0:up; 1:right, 2: down, 3: left;
snake = SNAKE()

# 5. Define Fruit class

class FRUIT:
    def __init__(self):
        self.pos = pygame.math.Vector2(
            random.randint(0, numberOfCell - 1),
            random.randint(0, numberOfCell - 1)
        )
    
    def place(self):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cellSize),
            int(self.pos.y * cellSize),
            cellSize,
            cellSize
        )
        pygame.draw.rect(screen, (fruitColor), fruit_rect)

    def relocate(self):
        while True:
            new_pos = pygame.math.Vector2(
                random.randint(0, numberOfCell - 1),
                random.randint(0, numberOfCell - 1)
            )
            if new_pos not in snake.body:
                self.pos = new_pos
                break
fruit = FRUIT()

# 6. Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 6.1 Handle user input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 2:
                direction = 0
            if event.key == pygame.K_RIGHT and direction != 3:
                direction = 1
            if event.key == pygame.K_DOWN and direction != 0:
                direction = 2
            if event.key == pygame.K_LEFT and direction != 1:
                direction = 3

        # 6.2 Move the snake
        if event.type == MOVE_EVENT:
            head = snake.body[0]            
            if direction == 0:  # up
                new_head = pygame.math.Vector2(head.x, head.y - 1)
            elif direction == 1:  # right
                new_head = pygame.math.Vector2(head.x + 1, head.y)
            elif direction == 2:  # down
                new_head = pygame.math.Vector2(head.x, head.y + 1)
            elif direction == 3:  # left
                new_head = pygame.math.Vector2(head.x - 1, head.y)

            # 6.2.1 Check self-collision
            if new_head in snake.body:
                pygame.display.set_caption("GAME OVER")
                pygame.quit()
                sys.exit()

            snake.body.insert(0, new_head)

            # 6.3 Check if fruit is eaten
            if fruit.pos != new_head:
                snake.body.pop()
            else:
                score += 1
                fruit.relocate()
                gotcha_sound = pygame.mixer.Sound("gotcha.wav")
                gotcha_sound.play()


            # 6.4 Wall collision
            if new_head.x >= numberOfCell or new_head.x < 0 or new_head.y >= numberOfCell or new_head.y < 0:
                pygame.display.set_caption("GAME OVER")
                pygame.quit()
                sys.exit()

            
    # 6.5 Clear screen and redraw everything
    screen.fill(backgroundColor)

    # 6.6 Draw the snake
    for block in snake.body:
        if block == snake.body[0]:
            rect = pygame.Rect(int(block.x * cellSize), int(block.y * cellSize), cellSize, cellSize)
            pygame.draw.rect(screen, (headColor), rect)
        else:
            rect = pygame.Rect(int(block.x * cellSize), int(block.y * cellSize), cellSize, cellSize)
            pygame.draw.rect(screen, (snakeColor), rect)

    # 6.7 Draw the fruit
    fruit.place()
    
    # 6.8 Update the display and tick the clock
    pygame.display.update()
    clock.tick(frames)
