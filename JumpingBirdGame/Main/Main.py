import pygame
import sys
import random

pygame.init()

# --------------------------------------------------
# Indstillinger
# --------------------------------------------------
WIDTH = 400
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Python")
clock = pygame.time.Clock()

# --------------------------------------------------
# Farver
# --------------------------------------------------
BLUE = (100, 180, 255)
#YELLOW = (255, 255, 0)
PINK = (255, 182, 193)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)

# --------------------------------------------------
# Fugle-data
# --------------------------------------------------
bird_x = 100
bird_y = HEIGHT // 2
bird_width = 40
bird_height = 30

# "Fysik"-variabler:
bird_velocity = 0.0      # Hvor hurtigt fuglen bevæger sig i y-retningen
gravity = 0.5            # Hvor meget hastigheden øges nedad per frame
jump_strength = -10      # Negativ = opad (fordi y-aksen går nedad)


# --------------------------------------------------
# Pipe-data
# --------------------------------------------------
pipe_width = 60
pipe_gap = 150
pipe_speed = 3

pipe_x = WIDTH
pipe_height = random.randint(150, 400)

score = 0
font = pygame.font.SysFont(None, 40)
game_over = False


running = True

while running:

    # --------------------------------------------------
    # 1) Input / events
    # --------------------------------------------------
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

        # --------------------------------------------------
        # 2) Update / fysik
        # --------------------------------------------------

        bird_velocity += gravity
        bird_y += bird_velocity

        # Flyt pipes mod venstre
        pipe_x -= pipe_speed

        # Når pipe forsvinder, reset den
        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(120, 450)
            score += 1

        # --------------------------------------------------
        # Kollision
        # --------------------------------------------------

        bird_rect = pygame.Rect(bird_x, int(bird_y), bird_width, bird_height)

        top_pipe = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
        bottom_pipe = pygame.Rect(pipe_x, pipe_height + pipe_gap,
                                  pipe_width, HEIGHT)

        # Rammer pipe?
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            game_over = True

        # Rammer jorden eller toppen?
        if bird_y <= 0 or bird_y >= HEIGHT:
            game_over = True

    # --------------------------------------------------
    # 3) Tegn
    # --------------------------------------------------
    screen.fill(BLUE)

    # Tegn pipes
    top_pipe = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
    bottom_pipe = pygame.Rect(pipe_x, pipe_height + pipe_gap,
                              pipe_width, HEIGHT)

    pygame.draw.rect(screen, GREEN, top_pipe)
    pygame.draw.rect(screen, GREEN, bottom_pipe)

    # ------------------------------  Tegn fugl  -------------------------------------------
    bird_rect = pygame.Rect(bird_x, int(bird_y), bird_width, bird_height)
    pygame.draw.rect(screen, PINK, bird_rect)

    # Øjne (hvid del)
    eye_radius = 6
    eye_x = bird_x + bird_width - 12
    eye_y = int(bird_y) + 10

    pygame.draw.circle(screen, WHITE, (eye_x, eye_y), eye_radius)

    # Pupillen (sort del)
    pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), 3)

    # Næb (orange trekant)
    beak_color = (255, 165, 0)
    beak_points = [
        (bird_x + bird_width, int(bird_y) + 15),  # venstre punkt
        (bird_x + bird_width + 10, int(bird_y) + 10),  # top punkt
        (bird_x + bird_width + 10, int(bird_y) + 20)  # bund punkt
    ]
    pygame.draw.polygon(screen, beak_color, beak_points)

    # Vinge (mørkere pink)
    wing_color = (255, 20, 147)
    wing_points = [
        (bird_x + 5, int(bird_y) + 15),  # nær toppen af fuglen
        (bird_x + 20, int(bird_y) + 10),  # spids
        (bird_x + 20, int(bird_y) + 25)  # bund
    ]
    pygame.draw.polygon(screen, wing_color, wing_points)

    #-----------------------------------------------------------------------------------------

    # Tegn score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render("GAME OVER - Tryk R", True, WHITE)
        screen.blit(game_over_text, (40, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()