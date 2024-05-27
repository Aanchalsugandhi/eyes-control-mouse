
import pygame
import sys
import random

pygame.init()


screen_width, screen_height = 800, 600
ball_radius = 20
ball_color = (255, 0, 0)
cursor_color = (0, 0, 255)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catch the Ball")


cursor_x, cursor_y = screen_width // 2, screen_height // 2


score = 0

clock = pygame.time.Clock()

def spawn_ball():
    ball_x = random.randint(0, screen_width - 2 * ball_radius)
    ball_y = 0
    return ball_x, ball_y

def draw_cursor():
    pygame.draw.circle(screen, cursor_color, (cursor_x, cursor_y), ball_radius)

def draw_ball(ball_x, ball_y):
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

def main():
    global cursor_x, cursor_y, score

    ball_x, ball_y = spawn_ball()
    ball_speed = 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        cursor_x, cursor_y = pygame.mouse.get_pos()


        ball_y += ball_speed

        if (
            cursor_x - ball_radius < ball_x < cursor_x + ball_radius
            and cursor_y - ball_radius < ball_y < cursor_y + ball_radius
        ):
            score += 1
            ball_x, ball_y = spawn_ball()

        if ball_y > screen_height:
            ball_x, ball_y = spawn_ball()


        screen.fill((0, 0, 0))


        draw_cursor()
        draw_ball(ball_x, ball_y)


        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if _name_ == "_main_":
    main()