import pygame
from pygame import*
pygame.font.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 700, 500
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ping Pong Game')

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100

FONT = pygame.font.SysFont('comicsens', 40)
MAX_SCORE = 10

right_score = 0
left_score = 0

PADDLE_VEL = 5

CLOCK = pygame.time.Clock()
FPS = 60

class Ball():
    BALL_VEL = 7

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ball_rect = pygame.Rect(self.x, self.y, 10, 10)
        self.x_vel = self.BALL_VEL
        self.y_vel = 0
    
    def move_ball(self):
        self.ball_rect.x += self.x_vel
        self.ball_rect.y += self.y_vel

    def reset(self):
        self.x_vel = self.BALL_VEL
        self.y_vel = 0
        self.ball_rect.x = self.x
        self.ball_rect.y = self.y
    
    def paddle_collision(self, paddle: Rect):
        if abs(self.ball_rect.center[1] - paddle.center[1]) < 5:
            self.y_vel = 0
        else:
            self.y_vel = (self.ball_rect.center[1] - paddle.center[1]) * 0.05  
        self.x_vel *= -1 

    def check_collisions(self, right_paddle: Rect, left_paddle: Rect):
            global right_score, left_score
            if self.ball_rect.y + self.ball_rect.height >= SCREEN_HEIGHT or self.ball_rect.y <= 0:
                self.y_vel *= -1
            if self.ball_rect.x + self.ball_rect.width > SCREEN_WIDTH:
                right_score += 1
                self.reset()
                self.x_vel *= -1
            if self.ball_rect.x < 0:
                left_score += 1
                self.reset()
            if self.ball_rect.x + self.ball_rect.width >= right_paddle.x and self.ball_rect.y +5 >= right_paddle.y and self.ball_rect.y -5 + self.ball_rect.height <= right_paddle.y + PADDLE_HEIGHT:
                self.paddle_collision(right_paddle)
            if self.ball_rect.x <= left_paddle.x + PADDLE_WIDTH and self.ball_rect.y +5 >= left_paddle.y and self.ball_rect.y -5 + self.ball_rect.height <= left_paddle.y + PADDLE_HEIGHT:
                self.paddle_collision(left_paddle)

def draw_window(left_paddle, right_paddle, ball: Ball):
    SCREEN.fill('black')
    pygame.draw.rect(SCREEN, "white", left_paddle)
    pygame.draw.rect(SCREEN, "white", right_paddle)

    right_text = FONT.render(str(right_score), 1, 'white')
    left_text = FONT.render(str(left_score), 1, 'white')

    SCREEN.blit(right_text, (10, 10))
    SCREEN.blit(left_text, (SCREEN_WIDTH - left_text.get_width() - 10, 10))

    for i in range(0, SCREEN_HEIGHT, 50): 
        pygame.draw.rect(SCREEN, 'gray', pygame.Rect(SCREEN_WIDTH / 2 - 5, i, 10, 30)) 

    pygame.draw.rect(SCREEN, "white", ball.ball_rect)
    pygame.display.update()

def draw_winner(text):
    draw_text = FONT.render(text, 1, 'white')
    posision=()
    if right_score == 10:
        posision = (SCREEN_WIDTH/4, SCREEN_HEIGHT/2)
    if left_score == 10:
        posision = (525, SCREEN_HEIGHT/2)
    SCREEN.blit(draw_text, posision)
    pygame.display.update()
    pygame.time.delay(3000)

def move_paddles(keys_pressed, left_paddle: Rect, right_paddle: Rect):
    if keys_pressed[K_w] and left_paddle.y > 0:
        left_paddle.y -= PADDLE_VEL
    if keys_pressed[K_s] and left_paddle.y + PADDLE_HEIGHT < SCREEN_HEIGHT:
        left_paddle.y += PADDLE_VEL

    if keys_pressed[K_UP] and right_paddle.y > 0:
        right_paddle.y -= PADDLE_VEL
    if keys_pressed[K_DOWN] and right_paddle.y + PADDLE_HEIGHT < SCREEN_HEIGHT:
        right_paddle.y += PADDLE_VEL



def main():
    global right_score, left_score
    ball = Ball(SCREEN_WIDTH /2, SCREEN_HEIGHT /2)

    left_paddle = pygame.Rect(0, SCREEN_HEIGHT /2 - PADDLE_HEIGHT /2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(SCREEN_WIDTH - PADDLE_WIDTH, SCREEN_HEIGHT /2 - PADDLE_HEIGHT /2, PADDLE_WIDTH, PADDLE_HEIGHT)
    run = True
    while run:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
                pygame.quit()
                
        if right_score == 10 or left_score == 10:
            draw_winner('WIN')
            run = False

        ball.move_ball()
        keys_pressed = pygame.key.get_pressed()
        move_paddles(keys_pressed, left_paddle, right_paddle)
        draw_window(left_paddle, right_paddle, ball)
        ball.check_collisions(right_paddle, left_paddle)

    right_score = 0
    left_score = 0
    ball.reset()
    
    main()

if __name__ == "__main__" :
    main()