"""
Space Dodger - versión simple y clara (PyGame)
Guarda como: space_dodger_simple.py
Requisitos: pip install pygame
Ejecutar: python space_dodger_simple.py
Controles: Flechas o WASD para mover, P para pausar, ESC para salir.
"""

import pygame
import random
import sys

# ---------- Config ----------
WIDTH, HEIGHT = 640, 480
FPS = 60

PLAYER_SIZE = 30
PLAYER_SPEED = 5

ENEMY_MIN_SIZE = 18
ENEMY_MAX_SIZE = 36
ENEMY_SPEED_BASE = 2

# ---------- Inicialización ----------
def init():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Dodger (Simple)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 26)
    big = pygame.font.SysFont(None, 48)
    return screen, clock, font, big

# ---------- Dibujo de texto ----------
def draw_text(scr, font, text, x, y, center=False):
    surf = font.render(text, True, (255,255,255))
    r = surf.get_rect()
    if center:
        r.center = (x, y)
    else:
        r.topleft = (x, y)
    scr.blit(surf, r)

# ---------- Crear enemigo ----------
def spawn_enemy(level):
    size = random.randint(ENEMY_MIN_SIZE, ENEMY_MAX_SIZE)
    x = random.randint(0, WIDTH - size)
    speed = ENEMY_SPEED_BASE + level * 0.2 + (ENEMY_MAX_SIZE - size) * 0.03
    color = (200, 60 + min(120, level*6), 60)
    return {"x": x, "y": -size, "size": size, "speed": speed, "color": color}

# ---------- Mover jugador ----------
def move_player(keys, player):
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player["x"] -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player["x"] += PLAYER_SPEED
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player["y"] -= PLAYER_SPEED
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player["y"] += PLAYER_SPEED
    # límites pantalla
    player["x"] = max(0, min(WIDTH - player["size"], player["x"]))
    player["y"] = max(0, min(HEIGHT - player["size"], player["y"]))

# ---------- Colisiones ----------
def check_collision(player, enemies):
    px, py, ps = player["x"], player["y"], player["size"]
    for e in enemies:
        ex, ey, es = e["x"], e["y"], e["size"]
        if (px < ex + es and px + ps > ex and py < ey + es and py + ps > ey):
            return True
    return False

# ---------- Menú principal (simple) ----------
def menu(screen, clock, font, big):
    selected = 0
    options = ["Jugar", "Salir"]
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(options)
                elif ev.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(options)
                elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if options[selected] == "Jugar":
                        return True
                    else:
                        return False
        screen.fill((10,10,30))
        draw_text(screen, big, "Space Dodger", WIDTH//2, 80, center=True)
        for i, o in enumerate(options):
            col = (255,255,0) if i == selected else (200,200,200)
            surf = font.render(o, True, col)
            rect = surf.get_rect(center=(WIDTH//2, 180 + i*40))
            screen.blit(surf, rect)
        pygame.display.flip()
        clock.tick(FPS)

# ---------- Bucle del juego ----------
def game_loop(screen, clock, font):
    player = {"x": WIDTH//2 - PLAYER_SIZE//2, "y": HEIGHT - 60, "size": PLAYER_SIZE}
    enemies = []
    lives = 3
    score = 0
    level = 1
    spawn_acc = 0
    spawn_interval = 1.0  # segundos

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # segundos por frame
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return False
                if ev.key == pygame.K_p:
                    pause(screen, clock, font)

        keys = pygame.key.get_pressed()
        move_player(keys, player)

        # generar enemigos
        spawn_acc += dt
        current_interval = max(0.25, spawn_interval - (level-1)*0.05)
        if spawn_acc >= current_interval:
            spawn_acc = 0
            enemies.append(spawn_enemy(level))

        # actualizar enemigos
        for e in enemies:
            e["y"] += e["speed"]
        enemies = [e for e in enemies if e["y"] <= HEIGHT + e["size"]]

        # colisiones
        if check_collision(player, enemies):
            # quitar enemigo más cercano (simple)
            enemies = enemies[1:] if enemies else []
            lives -= 1
            if lives <= 0:
                game_over(screen, clock, font, score)
                return True  # vuelve al menú

        # puntuación y nivel simple
        score += int(10 * dt * level)
        if score // 200 > (level - 1):
            level += 1

        # dibujar
        screen.fill((7,7,20))
        # jugador (triángulo)
        px, py, ps = player["x"], player["y"], player["size"]
        pygame.draw.polygon(screen, (100,200,255), [(px+ps//2, py), (px+ps, py+ps), (px, py+ps)])
        # enemigos
        for e in enemies:
            pygame.draw.rect(screen, e["color"], (e["x"], e["y"], e["size"], e["size"]))
        # HUD
        draw_text(screen, font, f"Puntos: {score}", 8, 8)
        draw_text(screen, font, f"Vidas: {lives}", 8, 34)
        draw_text(screen, font, f"Nivel: {level}", WIDTH-110, 8)
        draw_text(screen, font, "Pausa: P   Salir: ESC", WIDTH-220, HEIGHT-30)
        pygame.display.flip()
    return True

# ---------- Pausa ----------
def pause(screen, clock, font):
    paused = True
    while paused:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_p:
                    return
                if ev.key == pygame.K_ESCAPE:
                    return
        draw_text(screen, font, "Pausado - P para reanudar", WIDTH//2, HEIGHT//2, center=True)
        pygame.display.flip()
        clock.tick(10)

# ---------- Game Over ----------
def game_over(screen, clock, font, score):
    waiting = True
    while waiting:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                waiting = False
            if ev.type == pygame.KEYDOWN:
                waiting = False
        screen.fill((30,5,5))
        draw_text(screen, font, f"Game Over - Puntos: {score}", WIDTH//2, HEIGHT//2 - 20, center=True)
        draw_text(screen, font, "Presiona cualquier tecla para volver al menú", WIDTH//2, HEIGHT//2 + 20, center=True)
        pygame.display.flip()
        clock.tick(10)

# ---------- Main ----------
def main():
    screen, clock, font, big = init()
    while True:
        start = menu(screen, clock, font, big)
        if not start:
            break
        back = game_loop(screen, clock, font)
        if not back:
            break
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
