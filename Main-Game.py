import pygame
import sys
import random

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mirror Image: Find Your Better Self")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (89, 65, 42)
RED = (200, 0, 0)
GREY = (50, 50, 50)

# Fonts
font = pygame.font.SysFont('arial', 24)
small_font = pygame.font.SysFont('arial', 18)

# Music
pygame.mixer.init()
pygame.mixer.music.load('sounds/tension-loop.wav')
pygame.mixer.music.play(-1)  # Loop indefinitely

# Load images
kate_portrait = pygame.image.load('images/kate.png')
tesca_portrait = pygame.image.load('images/tesca.png')

# Game States
STATE_INTRO = 0
STATE_DIALOGUE = 1
STATE_MIRROR = 2
STATE_PORTAL_ROOM = 3
STATE_CHOICE = 4
STATE_ASCENSION = 5
STATE_END = 6
game_state = STATE_INTRO

# Dialogue Variables
dialogue_queue = [
    ("Kate", "I don't know what I'm supposed to see..."),
    ("Tesca", "You must look deeper, child. Trust the process."),
    ("Kate", "Is there really a better me in there?"),
]
dialogue_index = 0

# Choice Options
choice_options = ["Trust Tesca", "Resist", "Look Deeper"]
selected_choice = 0
player_decision = None
ending_type = None

# Mirror Variables
mirror_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 150, 200, 300)
reflection_offset = 0
reflection_direction = 1

# Portal Room Variables
portal_mirrors = [pygame.Rect(random.randint(100, 700), random.randint(50, 500), 50, 100) for _ in range(20)]

# Ascension Animation Variables
ascension_progress = 0
ascension_max = 100

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if game_state == STATE_INTRO:
                game_state = STATE_DIALOGUE

            elif game_state == STATE_DIALOGUE:
                dialogue_index += 1
                if dialogue_index >= len(dialogue_queue):
                    game_state = STATE_MIRROR

            elif game_state == STATE_MIRROR:
                game_state = STATE_PORTAL_ROOM

            elif game_state == STATE_PORTAL_ROOM:
                game_state = STATE_CHOICE

            elif game_state == STATE_CHOICE:
                if event.key == pygame.K_UP:
                    selected_choice = (selected_choice - 1) % len(choice_options)
                elif event.key == pygame.K_DOWN:
                    selected_choice = (selected_choice + 1) % len(choice_options)
                elif event.key == pygame.K_RETURN:
                    player_decision = choice_options[selected_choice]
                    game_state = STATE_ASCENSION

    # Scene Rendering
    if game_state == STATE_INTRO:
        text = font.render("Kate stares into the mirror. Press any key to begin.", True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))

    elif game_state == STATE_DIALOGUE:
        speaker, dialogue = dialogue_queue[dialogue_index]
        pygame.draw.rect(screen, GREY, (50, HEIGHT - 150, WIDTH - 100, 100))
        text = small_font.render(dialogue, True, WHITE)
        screen.blit(text, (70, HEIGHT - 130))
        portrait = kate_portrait if speaker == "Kate" else tesca_portrait
        screen.blit(portrait, (WIDTH - 200, HEIGHT - 200))

    elif game_state == STATE_MIRROR:
        pygame.draw.rect(screen, BROWN, mirror_rect)
        reflection_offset += reflection_direction * 0.5
        if abs(reflection_offset) > 5:
            reflection_direction *= -1
        reflection_rect = mirror_rect.copy()
        reflection_rect.y += int(reflection_offset)
        pygame.draw.rect(screen, WHITE, reflection_rect, 2)
        text = font.render("Your reflection wavers... Press any key.", True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 50))

    elif game_state == STATE_PORTAL_ROOM:
        for m in portal_mirrors:
            pygame.draw.rect(screen, WHITE, m, 2)
        text = font.render("You are lost in the Portal Room... Press any key.", True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 50))

    elif game_state == STATE_CHOICE:
        text = font.render("What will you do?", True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 100))
        for idx, option in enumerate(choice_options):
            color = RED if idx == selected_choice else WHITE
            opt_text = font.render(option, True, color)
            screen.blit(opt_text, (WIDTH//2 - opt_text.get_width()//2, HEIGHT//2 - 50 + idx * 40))
            if idx == selected_choice:
                arrow = font.render(">", True, RED)
                screen.blit(arrow, (WIDTH//2 - opt_text.get_width()//2 - 30, HEIGHT//2 - 50 + idx * 40))

    elif game_state == STATE_ASCENSION:
        if ascension_progress < ascension_max:
            ascension_progress += 1
        pygame.draw.circle(screen, RED, (WIDTH//2, HEIGHT//2), ascension_progress)
        text = font.render("Kate transforms...", True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 50))

        if ascension_progress >= ascension_max:
            if player_decision == "Trust Tesca":
                ending_type = "ascended"
            elif player_decision == "Resist":
                ending_type = "resisted"
            elif player_decision == "Look Deeper":
                ending_type = "consumed"
            game_state = STATE_END

    elif game_state == STATE_END:
        if ending_type == "ascended":
            lines = [
                "You Ascended. Your Better Self stands tall.",
                "Yet... was it truly better? Press ESC to exit."
            ]
        elif ending_type == "resisted":
            lines = [
                "You resisted. The Mirror cracked and you awoke elsewhere.",
                "You are free... but unchanged. Press ESC to exit."
            ]
        elif ending_type == "consumed":
            lines = [
                "You looked deeper and got lost within the Mirror.",
                "No one will ever know what became of you. Press ESC to exit."
            ]
        for idx, line in enumerate(lines):
            text = font.render(line, True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + idx * 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
