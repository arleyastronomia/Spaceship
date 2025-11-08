# SpaceShip

## Resumen
Spaceship es un juego hecho con PyGame. Controlas una nave triangular que debe esquivar enemigos cuadrados que caen desde arriba. El objetivo es sobrevivir el mayor tiempo y obtener puntos.

## Requisitos
- Python 3.8 o superior
- PyGame: `pip install pygame`

## Archivos
- `spaceship.py` — código (archivo único).

## Controles
- Mover: Flechas o WASD
- Pausa: P
- Salir / volver al menú: ESC

## Funciones
- `init()` — inicializa PyGame y fuentes.
- `menu()` — menú principal.
- `game_loop()` — bucle del juego.
- `spawn_enemy(level)` — genera enemigos.
- `move_player(keys, player)` — mueve al jugador.
- `check_collision(player, enemies)` — detecta colisiones.
- `pause()` y `game_over()` — pantallas auxiliares.

## Cómo ejecutar
1. Guarda `space_dodger_simple.py` en una carpeta.
2. Instala PyGame:
   ```bash
   pip install pygame
