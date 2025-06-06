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

screenWidth = 500
screenHeight = 500
cellSize = 25
numberOfCell = int(screenWidth / cellSize)
frames = 60
movePer = 200

MOVE_EVENT = pygame.USEREVENT + 1

class SNAKE:
    def __init__(self):
        self.body = [pygame.math.Vector2(numberOfCell // 2, numberOfCell // 2),
                     pygame.math.Vector2(numberOfCell // 2, numberOfCell // 2),
                     pygame.math.Vector2(numberOfCell // 2, numberOfCell // 2),
                     pygame.math.Vector2(numberOfCell // 2, numberOfCell // 2),
                     pygame.math.Vector2(numberOfCell // 2, numberOfCell // 2)]

class FRUIT:
    def __init__(self, snake):
        self.snake = snake
        self.relocate()

    def place(self, screen):
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
            if new_pos not in self.snake.body:
                self.pos = new_pos
                break

# Game class starts here
class Game:
    def __init__(self):
        # 3. Define game settings
        self.screen = pygame.display.set_mode((screenWidth,screenHeight))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.score = 0
        self.direction = 0 #0:up; 1:right, 2: down, 3: left;
        pygame.time.set_timer(MOVE_EVENT, movePer)

        # 4. Initialize snake
        self.snake = SNAKE()

        # 5. Define Fruit class
        self.fruit = FRUIT(self.snake)

        self.direction_changed = False 


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 6.1 Handle user input
                if event.type == pygame.KEYDOWN and not self.direction_changed:
                    if event.key == pygame.K_UP and self.direction != 2:
                        self.direction = 0
                        self.direction_changed = True
                    elif event.key == pygame.K_RIGHT and self.direction != 3:
                        self.direction = 1
                        self.direction_changed = True
                    elif event.key == pygame.K_DOWN and self.direction != 0:
                        self.direction = 2
                        self.direction_changed = True
                    elif event.key == pygame.K_LEFT and self.direction != 1:
                        self.direction = 3
                        self.direction_changed = True


                # 6.2 Move the snake
                if event.type == MOVE_EVENT:
                    self.direction_changed = False
                    head = self.snake.body[0]            
                    if self.direction == 0:
                        new_head = pygame.math.Vector2(head.x, head.y - 1)
                    elif self.direction == 1:
                        new_head = pygame.math.Vector2(head.x + 1, head.y)
                    elif self.direction == 2:
                        new_head = pygame.math.Vector2(head.x, head.y + 1)
                    elif self.direction == 3:
                        new_head = pygame.math.Vector2(head.x - 1, head.y)

                    # 6.2.1 Check self-collision (ignore tail if not growing)
                    if self.fruit.pos != new_head:
                        tail = self.snake.body[-1]
                        body_without_tail = self.snake.body[:-1]
                        if new_head in body_without_tail:
                            pygame.display.set_caption("GAME OVER")
                            pygame.quit()
                            sys.exit()
                    else:
                        if new_head in self.snake.body:
                            pygame.display.set_caption("GAME OVER")
                            pygame.quit()
                            sys.exit()


                    self.snake.body.insert(0, new_head)

                    # 6.3 Check if fruit is eaten
                    if self.fruit.pos != new_head:
                        self.snake.body.pop()
                    else:
                        self.score += 1
                        self.fruit.relocate()
                        gotcha_sound = pygame.mixer.Sound("gotcha.wav")
                        gotcha_sound.play()

                    # 6.4 Wall collision
                    if (new_head.x >= numberOfCell or new_head.x < 0 or 
                        new_head.y >= numberOfCell or new_head.y < 0):
                        pygame.display.set_caption("GAME OVER")
                        pygame.quit()
                        sys.exit()

            # 6.5 Clear screen and redraw everything
            self.screen.fill(backgroundColor)

            # 6.6 Draw the snake
            for block in self.snake.body:
                rect = pygame.Rect(int(block.x * cellSize), int(block.y * cellSize), cellSize, cellSize)
                if block == self.snake.body[0]:
                    pygame.draw.rect(self.screen, (headColor), rect)
                else:
                    pygame.draw.rect(self.screen, (snakeColor), rect)

            # 6.7 Draw the fruit
            self.fruit.place(self.screen)
            
            # 6.8 Update the display and tick the clock
            pygame.display.update()
            self.clock.tick(frames)

# Entry point
if __name__ == "__main__":
    game = Game()
    game.run()
