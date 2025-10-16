# main.py
import pygame
import sys
import random
from pathlib import Path

# ---------------------- Configuration ----------------------
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)
PAUSE_OVERLAY = (0, 0, 0, 180)  # (not used as rgba in plain draw but kept for concept)

# Files / paths
RESOURCES_DIR = Path("resources")
MUSIC_FILE = RESOURCES_DIR / "music.mp3"
EAT_SOUND_FILE = RESOURCES_DIR / "eat.wav"
GAME_OVER_SOUND_FILE = RESOURCES_DIR / "gameover.wav"
SCORES_FILE = "scores.txt"

# Gameplay tuning
BASE_SPEED = 2             # very slow starting speed (level 1)
SPEED_PER_LEVEL = 2
POINTS_PER_LEVEL = 5
MAX_SPEED = 20             # safety cap (optional)

# ---------------------- High Scores ----------------------
def save_score_to_file(score, level):
    """Append final score and level to scores.txt"""
    try:
        with open(SCORES_FILE, "a") as f:
            f.write(f"{score},{level}\n")
    except Exception as e:
        print("Error saving score:", e)

def load_scores_from_file():
    """Return a sorted list of (score, level) from scores.txt"""
    scores = []
    try:
        with open(SCORES_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    try:
                        s = int(parts[0])
                        lv = int(parts[1])
                        scores.append((s, lv))
                    except ValueError:
                        continue
    except FileNotFoundError:
        return []
    except Exception as e:
        print("Error reading scores:", e)
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores

# ---------------------- Helpers ----------------------
def random_food_position(snake):
    max_x = (WINDOW_WIDTH // CELL_SIZE) - 1
    max_y = (WINDOW_HEIGHT // CELL_SIZE) - 1
    while True:
        x = random.randint(0, max_x) * CELL_SIZE
        y = random.randint(0, max_y) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

def draw_score_level(surface, font, score, level):
    txt = font.render(f"Score: {score}    Level: {level}", True, YELLOW)
    surface.blit(txt, (10, 8))

def draw_center_text(surface, font, text, y, color=WHITE):
    surf = font.render(text, True, color)
    surface.blit(surf, ((WINDOW_WIDTH - surf.get_width()) // 2, y))

# ---------------------- Game Loop ----------------------
def game_loop(screen, clock, sound_on=True):
    # Initial state
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (CELL_SIZE, 0)
    food = random_food_position(snake)
    score = 0
    level = 1
    speed = BASE_SPEED

    ui_font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 64)

    # Load SFX
    eat_sound = None
    game_over_sound = None
    if sound_on:
        try:
            eat_sound = pygame.mixer.Sound(str(EAT_SOUND_FILE))
            game_over_sound = pygame.mixer.Sound(str(GAME_OVER_SOUND_FILE))
        except Exception as e:
            print("Warning: couldn't load sound effects:", e)
            eat_sound = None
            game_over_sound = None

    running = True
    paused = False

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif ev.type == pygame.KEYDOWN:
                # Pause/resume with P
                if ev.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        # Pause music if playing
                        try:
                            pygame.mixer.music.pause()
                        except Exception:
                            pass
                    else:
                        try:
                            pygame.mixer.music.unpause()
                        except Exception:
                            pass
                # Skip movement input while paused
                if paused:
                    continue

                # Movement keys; forbid immediate reverse
                if ev.key in (pygame.K_UP, pygame.K_w) and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif ev.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif ev.key in (pygame.K_LEFT, pygame.K_a) and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif ev.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

        if paused:
            # Draw paused overlay and wait (still in main loop)
            # overlay effect: dim screen with a rectangle and text
            overlay_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay_surf.set_alpha(140)
            overlay_surf.fill((0, 0, 0))
            screen.blit(overlay_surf, (0, 0))
            draw_center_text(screen, big_font, "PAUSED", WINDOW_HEIGHT // 2 - 40, color=WHITE)
            draw_center_text(screen, ui_font, "Press P to resume", WINDOW_HEIGHT // 2 + 20, color=WHITE)
            pygame.display.update()
            clock.tick(10)
            continue

        # Move snake
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)
        snake.insert(0, new_head)

        # Collisions (walls + self)
        if (new_head[0] < 0 or new_head[0] >= WINDOW_WIDTH or
            new_head[1] < 0 or new_head[1] >= WINDOW_HEIGHT or
            new_head in snake[1:]):
            running = False
            break

        # Eat food
        if new_head == food:
            score += 1
            if sound_on and eat_sound:
                try:
                    eat_sound.play()
                except Exception:
                    pass
            food = random_food_position(snake)
            if score % POINTS_PER_LEVEL == 0:
                level += 1
                speed = min(MAX_SPEED, speed + SPEED_PER_LEVEL)
        else:
            snake.pop()

        # Drawing
        screen.fill(DARK_GRAY)
        # Draw snake
        for i, pos in enumerate(snake):
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            if i == 0:
                pygame.draw.rect(screen, YELLOW, rect)
            else:
                pygame.draw.rect(screen, GREEN, rect)
        # Draw food
        pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))
        # Draw score/level
        draw_score_level(screen, ui_font, score, level)

        pygame.display.update()
        clock.tick(speed)

    # Game over actions
    if sound_on and game_over_sound:
        try:
            game_over_sound.play()
        except Exception:
            pass

    # Save score to file
    save_score_to_file(score, level)

    # Game Over Screen
    go_font = pygame.font.SysFont(None, 48)
    screen.fill(BLACK)
    draw_center_text(screen, go_font, "GAME OVER", WINDOW_HEIGHT // 2 - 50)
    draw_center_text(screen, ui_font, f"Score: {score}    Level: {level}", WINDOW_HEIGHT // 2 + 10)
    draw_center_text(screen, ui_font, "Press any key to return to menu", WINDOW_HEIGHT // 2 + 50)
    pygame.display.update()

    # Ensure music is playing (menu may handle music). Unpause if it was paused earlier.
    try:
        pygame.mixer.music.unpause()
    except Exception:
        pass

    # wait for key to return to menu
    waiting = True
    while waiting:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                waiting = False
        clock.tick(10)

# ---------------------- High Scores Screen ----------------------
def show_high_scores(screen, clock):
    opt_font = pygame.font.SysFont(None, 36)
    title_font = pygame.font.SysFont(None, 48)

    scores = load_scores_from_file()
    screen.fill(BLACK)
    title = title_font.render("HIGH SCORES", True, WHITE)
    screen.blit(title, ((WINDOW_WIDTH - title.get_width()) // 2, 60))
    y = 130

    if not scores:
        no_scores = opt_font.render("No scores saved yet!", True, WHITE)
        screen.blit(no_scores, (140, y))
    else:
        for i, (s, lvl) in enumerate(scores[:10]):
            txt = opt_font.render(f"{i+1}. Score: {s}   Level: {lvl}", True, WHITE)
            screen.blit(txt, (140, y))
            y += 40

    info = pygame.font.SysFont(None, 24).render("Press any key to return", True, WHITE)
    screen.blit(info, (140, y + 40))
    pygame.display.update()

    waiting = True
    while waiting:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                waiting = False
        clock.tick(10)

# ---------------------- Main Menu ----------------------
def main_menu(screen, clock):
    title_font = pygame.font.SysFont(None, 72)
    opt_font = pygame.font.SysFont(None, 36)
    sound_on = True

    # Load and start background music once (looping). We'll control volume and pause/unpause later.
    try:
        if MUSIC_FILE.exists():
            pygame.mixer.music.load(str(MUSIC_FILE))
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.6 if sound_on else 0.0)
        else:
            print(f"Music file not found: {MUSIC_FILE}")
    except Exception as e:
        print("Music not started:", e)

    while True:
        screen.fill(BLACK)
        draw_center_text(screen, title_font, "SNAKE", 60)
        screen.blit(opt_font.render("1 - Start New Game", True, WHITE), (140, 170))
        screen.blit(opt_font.render("2 - View High Scores", True, WHITE), (140, 220))
        screen.blit(opt_font.render(f"3 - Sound: {'On' if sound_on else 'Off'}", True, WHITE), (140, 270))
        screen.blit(opt_font.render("4 - Exit", True, WHITE), (140, 320))
        screen.blit(pygame.font.SysFont(None, 20).render("In-game: P = pause/resume", True, WHITE), (10, WINDOW_HEIGHT - 24))
        pygame.display.update()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    # Start new game
                    # Ensure music is playing/unpaused if sound_on
                    try:
                        if sound_on:
                            pygame.mixer.music.unpause()
                            pygame.mixer.music.set_volume(0.6)
                    except Exception:
                        pass
                    game_loop(screen, clock, sound_on)
                elif ev.key == pygame.K_2:
                    show_high_scores(screen, clock)
                elif ev.key == pygame.K_3:
                    sound_on = not sound_on
                    try:
                        pygame.mixer.music.set_volume(0.6 if sound_on else 0.0)
                    except Exception:
                        pass
                elif ev.key == pygame.K_4:
                    pygame.quit(); sys.exit()
        clock.tick(15)

# ---------------------- Entry Point ----------------------
def main():
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception:
        print("Warning: mixer init failed.")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    if not RESOURCES_DIR.exists():
        print(f"Warning: resources folder not found at '{RESOURCES_DIR}'. Place background.mp3, eat.wav, gameover.wav there if you want sound.")

    main_menu(screen, clock)

if __name__ == "__main__":
    main()
