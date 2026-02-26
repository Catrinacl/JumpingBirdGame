import pygame
import sys
import random

pygame.init()

# -------------------------------------------------------------------
# Indstillinger
# -------------------------------------------------------------------
WIDTH = 400
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Python")
clock = pygame.time.Clock()

# -------------------------------------------------------------------
# Farver
# -------------------------------------------------------------------
BLUE = (100, 180, 255)
PINK = (255, 182, 193)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 120, 0)
CLOUD_WHITE = (245, 245, 245)

# -------------------------------------------------------------------
# Fugle-data
# -------------------------------------------------------------------
bird_x = 100
bird_y = HEIGHT // 2
bird_width = 40
bird_height = 30

# "Fysik"-variabler:
bird_velocity = 0.0      # Hvor hurtigt fuglen bevæger sig i y-retningen
gravity = 0.5            # Hvor meget hastigheden øges nedad per frame
jump_strength = -10      # Negativ = opad (fordi y-aksen går nedad)


# -------------------------------------------------------------------
# Pipe-data
# -------------------------------------------------------------------
pipe_width = 60
pipe_gap = 150
pipe_speed = 3

pipe_x = WIDTH
pipe_height = random.randint(150, 400)

score = 0
font = pygame.font.SysFont(None, 40)
game_over = False

ground_height = 80


running = True

while running:

    # -------------------------------------------------------------------
    # Input / events
    # -------------------------------------------------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity = jump_strength

            # Tryk R for at genstarte
            if event.key == pygame.K_r and game_over:
                bird_y = HEIGHT // 2
                bird_velocity = 0
                pipe_x = WIDTH
                pipe_height = random.randint(150, 400)
                score = 0
                game_over = False

    if not game_over:

        # -------------------------------------------------------------------
        # Update / fysik
        # -------------------------------------------------------------------

        bird_velocity += gravity
        bird_y += bird_velocity

        # Flyt pipes mod venstre
        pipe_x -= pipe_speed

        # Når pipe forsvinder, reset den
        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(120, 450)
            score += 1

        # -------------------------------------------------------------------
        # Kollision
        # -------------------------------------------------------------------

        bird_rect = pygame.Rect(bird_x, int(bird_y), bird_width, bird_height)

        top_pipe = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
        bottom_pipe = pygame.Rect(pipe_x, pipe_height + pipe_gap,
                                  pipe_width, HEIGHT)

        # Hvis den rammer en top eller bottom pipe -> game over
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            game_over = True

        # Hvis den rammer jorden eller toppen -> game over
        if bird_y <= 0 or bird_y + bird_height >= HEIGHT - ground_height:
            game_over = True

    # -------------------------------------------------------------------
    # Tegnedelen
    # -------------------------------------------------------------------
    screen.fill(BLUE)

    # Skyer
    pygame.draw.circle(screen, CLOUD_WHITE, (80, 100), 25)
    pygame.draw.circle(screen, CLOUD_WHITE, (110, 100), 30)
    pygame.draw.circle(screen, CLOUD_WHITE, (140, 100), 25)

    pygame.draw.circle(screen, CLOUD_WHITE, (250, 180), 20)
    pygame.draw.circle(screen, CLOUD_WHITE, (275, 180), 25)
    pygame.draw.circle(screen, CLOUD_WHITE, (300, 180), 20)

    # Pipes
    top_pipe = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
    bottom_pipe = pygame.Rect(pipe_x, pipe_height + pipe_gap,
                              pipe_width, HEIGHT)

    pygame.draw.rect(screen, GREEN, top_pipe)
    pygame.draw.rect(screen, GREEN, bottom_pipe)

    # ------------------------------  FUGLEN  -------------------------------------------

    # Rund krop
    bird_radius = 20
    bird_center = (bird_x + bird_width // 2, int(bird_y) + bird_height // 2)

    pygame.draw.circle(screen, PINK, bird_center, bird_radius)

    # Øje
    eye_radius = 6
    eye_x = bird_center[0] + 6
    eye_y = bird_center[1] - 5

    pygame.draw.circle(screen, WHITE, (eye_x, eye_y), eye_radius)
    pygame.draw.circle(screen, (0, 0, 0), (eye_x + 2, eye_y), 3)

    # Næb
    beak_color = (255, 165, 0)

    beak_tip_x = bird_center[0] + bird_radius + 14
    beak_mid_y = bird_center[1]

    beak_points = [
        (bird_center[0] + bird_radius, beak_mid_y - 5),  # øverste bagpunkt
        (bird_center[0] + bird_radius, beak_mid_y + 5),  # nederste bagpunkt
        (beak_tip_x, beak_mid_y)  # spidsen
    ]

    pygame.draw.polygon(screen, beak_color, beak_points)

    # Vinge
    wing_color = (255, 20, 147) #mørkere pink
    wing_center = (bird_center[0] - 5, bird_center[1] + 5)

    pygame.draw.circle(screen, wing_color, wing_center, 8)

    #----------------------------------------SCORE-------------------------------------------

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render("GAME OVER - Tryk R", True, WHITE)
        screen.blit(game_over_text, (40, HEIGHT // 2))

    # Græs
    ground_rect = pygame.Rect(0, HEIGHT - ground_height, WIDTH, ground_height)
    pygame.draw.rect(screen, DARK_GREEN, ground_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()