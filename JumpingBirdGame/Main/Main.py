import pygame
import sys

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
YELLOW = (255, 255, 0)

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

running = True

while running:

    # --------------------------------------------------
    # 1) Input / events
    # --------------------------------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # KEYDOWN = når man trykker en tast ned (én gang)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Når vi hopper, sætter vi hastigheden til en "kick" opad
                bird_velocity = jump_strength

    # --------------------------------------------------
    # 2) Update / fysik
    # --------------------------------------------------

    # Tyngdekraft: hastigheden bliver mere og mere positiv (= nedad)
    bird_velocity += gravity

    # Position opdateres med hastigheden
    bird_y += bird_velocity

    # --------------------------------------------------
    # 3) Tegn
    # --------------------------------------------------
    screen.fill(BLUE)

    bird_rect = pygame.Rect(bird_x, int(bird_y), bird_width, bird_height)
    pygame.draw.rect(screen, YELLOW, bird_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()