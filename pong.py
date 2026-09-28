import sys
import random
import pygame

RESOLUTION = (800, 600)

RIGHT = "RIGHT"
LEFT = "LEFT"
UP = "UP"
DOWN = "DOWN"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Ball(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill(color)
        self.initial_position = (RESOLUTION[0] / 2, RESOLUTION[1] / 2)
        self.rect = self.image.get_rect()
        self.rect.center = self.initial_position
        self.x_speed = 10
        self.y_speed = 6
        self.direction = None
        self.blit_me = True

    def update(self):
        self.move()
        self.check_x_border()
        self.check_y_border()
        if not self.blit_me:
            self.reset()

    def set_random_direction(self):
        if random.randint(0, 1):
            self.direction = RIGHT
        else:
            self.direction = LEFT

    def move(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

    def check_x_border(self):
        if self.rect.left <= 0 or self.rect.right >= RESOLUTION[0]:
            self.blit_me = False

    def check_y_border(self):
        if self.rect.top <= 0 or self.rect.bottom >= RESOLUTION[1]:
            self.y_speed *= -1

    def reset(self):

        self.blit_me  = True
        self.rect.center = self.initial_position
        self.direction = self.set_random_direction()

class Paddle(pygame.sprite.Sprite):
    def __init__(self, number, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 150))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = 0
        self.max_speed = 10
        self.number = number
        rand = 10

        if self.number == 1:
            self.initial_position = self.rect.center = (self.rect.width / 2 + rand, RESOLUTION[1] / 2)

        elif self.number == 2:
            self.initial_position = self.rect.center = (RESOLUTION[0] - rand - self.rect.width / 2, RESOLUTION[1] / 2)

    def set_speed(self, direction):
        if direction == UP:
            self.speed = self.max_speed * -1
        elif direction == DOWN:
            self.speed = self.max_speed

        elif direction == None:
            self.speed = 0

    def move(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= RESOLUTION[1]:
            self.rect.bottom = RESOLUTION[1]
        self.rect.y += self.speed

    def update(self):
        self.move()

    def reset(self):
        self.rect.center = self.initial_position

class Game:

    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(0)
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.screen.fill(BLACK)
        self.timer = pygame.time.Clock()
        self.ball = Ball(GREEN)
        self.ball.set_random_direction()
        self.paddles = (Paddle(1, RED),
                        Paddle(2, BLUE))

    def blit_ball(self):
        self.screen.blit(self.ball.image, self.ball.rect)

    def blit_paddles(self):
        for paddle in self.paddles:
            self.screen.blit(paddle.image, paddle.rect)

    def check_collision(self):
        if self.ball.rect.colliderect(self.paddles[0].rect) or self.ball.rect.colliderect(self.paddles[1].rect):
            self.ball.x_speed *= -1

    def run(self):
        while True:
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                _quit = event.type == pygame.QUIT
                w = event.type == pygame.KEYDOWN and event.key == pygame.K_w
                notw = event.type == pygame.KEYUP and event.key == pygame.K_w
                s = event.type == pygame.KEYDOWN and event.key == pygame.K_s
                nots = event.type == pygame.KEYUP and event.key == pygame.K_s
                up = event.type == pygame.KEYDOWN and event.key == pygame.K_UP
                notup = event.type == pygame.KEYUP and event.key == pygame.K_UP
                down = event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN
                notdown = event.type == pygame.KEYUP and event.key == pygame.K_DOWN
                esc = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                if _quit or esc:
                    pygame.quit()
                    sys.exit()
                if w:
                    self.paddles[0].set_speed(UP)
                elif s:
                    self.paddles[0].set_speed(DOWN)
                elif notw or nots:
                    self.paddles[0].set_speed(None)
                if up:
                    self.paddles[1].set_speed(UP)
                elif down:
                    self.paddles[1].set_speed(DOWN)
                elif notup or notdown:
                    self.paddles[1].set_speed(None)
            self.check_collision()
            for paddle in self.paddles:
                paddle.update()
            self.ball.update()
            self.blit_ball()
            self.blit_paddles()
            pygame.display.update()
            self.timer.tick(60)

if __name__ == "__main__":
    pong = Game()
    pong.run()
