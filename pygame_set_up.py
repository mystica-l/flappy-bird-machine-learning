import pygame

# pygame clock and screen initialization
pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# scaled up images
SCALE = 1.75

#FPS
FPS = 30

# Background images
sky_image = pygame.image.load("assets/background-day.png")
sky_image = pygame.transform.scale(sky_image, (int(sky_image.get_width() * SCALE), int(sky_image.get_height() * SCALE)))

ground_image = pygame.image.load("assets/base.png")
ground_image = pygame.transform.scale(ground_image, (int(ground_image.get_width() * SCALE), int(ground_image.get_height() * SCALE/1.75)))

text_font = pygame.font.SysFont("Arial", 20, bold = True)