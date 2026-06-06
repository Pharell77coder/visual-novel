"""
test_transitions.py — Démo visuelle standalone des 5 transitions
=================================================================

Exécuter directement :
    python test_transitions.py

Touches :
    ESPACE / clic    → déclencher la transition suivante
    ← →              → choisir le type de transition
    Q / Échap        → quitter
"""

import sys
import math
import pygame
from transitions import Transition, TRANSITION_GUIDE

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 1280, 720
FPS = 60
FONT_NAME = None  # pygame default

TRANSITION_NAMES = list(TRANSITION_GUIDE.keys())

# Palette de couleurs pour simuler des "scènes"
SCENE_COLORS = [
    (18,  22,  40),   # bleu nuit — bureau
    (35,  20,  20),   # bordeaux — salle d'interrogatoire
    (10,  30,  20),   # vert sombre — parc
    (30,  25,  10),   # ocre — café
    (20,  10,  35),   # violet — flashback
]
SCENE_LABELS = ["Bureau", "Interrogatoire", "Parc nocturne", "Café", "Flashback"]
ACCENT_COLORS = [
    (80,  120, 200),
    (200,  70,  70),
    (60,  160,  80),
    (190, 150,  40),
    (140,  80, 210),
]


def make_scene(surf: pygame.Surface, idx: int, font_big, font_small) -> None:
    """Dessine une scène de test reconnaissable."""
    bg = SCENE_COLORS[idx % len(SCENE_COLORS)]
    accent = ACCENT_COLORS[idx % len(ACCENT_COLORS)]
    label = SCENE_LABELS[idx % len(SCENE_LABELS)]

    surf.fill(bg)

    # Lignes décoratives
    for i in range(0, WIDTH, 60):
        alpha_surf = pygame.Surface((1, HEIGHT), pygame.SRCALPHA)
        a = 20 if i % 120 == 0 else 10
        alpha_surf.fill((*accent, a))
        surf.blit(alpha_surf, (i, 0))

    # Titre de scène
    label_surf = font_big.render(label, True, accent)
    surf.blit(label_surf, (WIDTH // 2 - label_surf.get_width() // 2, HEIGHT // 2 - 30))

    # Numéro de scène
    num_surf = font_small.render(f"Scène {idx + 1}", True, (*accent[:3], 180))
    surf.blit(num_surf, (WIDTH // 2 - num_surf.get_width() // 2, HEIGHT // 2 + 30))

    # Petits carrés de texture
    for row in range(0, HEIGHT, 120):
        for col in range(0, WIDTH, 120):
            rect = pygame.Rect(col + 50, row + 50, 20, 20)
            pygame.draw.rect(surf, (*accent, 30), rect, border_radius=3)


def draw_hud(
    screen: pygame.Surface,
    tr_name: str,
    tr_idx: int,
    scene_idx: int,
    font_ui,
    transitioning: bool,
) -> None:
    """Affiche le HUD d'information en bas de l'écran."""
    guide = TRANSITION_GUIDE.get(tr_name, "")

    # Fond semi-transparent
    hud = pygame.Surface((WIDTH, 80), pygame.SRCALPHA)
    hud.fill((0, 0, 0, 160))
    screen.blit(hud, (0, HEIGHT - 80))

    # Nom de la transition sélectionnée
    name_col = (255, 200, 80) if not transitioning else (80, 200, 255)
    name_surf = font_ui.render(f"[← →] Transition : {tr_name}", True, name_col)
    screen.blit(name_surf, (20, HEIGHT - 70))

    # Description
    desc_surf = font_ui.render(guide, True, (160, 160, 160))
    screen.blit(desc_surf, (20, HEIGHT - 45))

    # Instruction droite
    action = "En cours…" if transitioning else "ESPACE ou clic → déclencher"
    action_col = (80, 200, 255) if transitioning else (200, 200, 200)
    act_surf = font_ui.render(action, True, action_col)
    screen.blit(act_surf, (WIDTH - act_surf.get_width() - 20, HEIGHT - 70))

    # Indicateur de sélection des transitions
    dot_y = HEIGHT - 25
    spacing = 28
    start_x = WIDTH // 2 - len(TRANSITION_NAMES) * spacing // 2
    for i, name in enumerate(TRANSITION_NAMES):
        color = (255, 200, 80) if i == tr_idx else (80, 80, 80)
        pygame.draw.circle(screen, color, (start_x + i * spacing, dot_y), 6 if i == tr_idx else 4)


# ---------------------------------------------------------------------------
# Boucle principale
# ---------------------------------------------------------------------------

def main():
    pygame.init()
    pygame.display.set_caption("Test — Nuit Sans Témoin — Transitions")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    font_big   = pygame.font.SysFont(FONT_NAME, 52, bold=True)
    font_small = pygame.font.SysFont(FONT_NAME, 28)
    font_ui    = pygame.font.SysFont(FONT_NAME, 18)

    # Pré-générer les surfaces de scène
    scenes: list[pygame.Surface] = []
    for i in range(len(SCENE_COLORS)):
        s = pygame.Surface((WIDTH, HEIGHT))
        make_scene(s, i, font_big, font_small)
        scenes.append(s)

    scene_idx  = 0
    tr_idx     = 0
    transition: Transition | None = None
    prev_surf: pygame.Surface | None = None

    # Dessiner la scène initiale
    screen.blit(scenes[scene_idx], (0, 0))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False

                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    if transition is None:
                        # Capturer la scène courante
                        prev_surf = screen.copy()
                        # Passer à la scène suivante
                        scene_idx = (scene_idx + 1) % len(scenes)
                        # Créer la transition
                        tr_name = TRANSITION_NAMES[tr_idx]
                        transition = Transition.create(tr_name, (WIDTH, HEIGHT))

                elif event.key == pygame.K_LEFT:
                    tr_idx = (tr_idx - 1) % len(TRANSITION_NAMES)

                elif event.key == pygame.K_RIGHT:
                    tr_idx = (tr_idx + 1) % len(TRANSITION_NAMES)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if transition is None:
                    prev_surf = screen.copy()
                    scene_idx = (scene_idx + 1) % len(scenes)
                    tr_name = TRANSITION_NAMES[tr_idx]
                    transition = Transition.create(tr_name, (WIDTH, HEIGHT))

        # --- Update ---
        if transition is not None:
            done = transition.update(dt)
            if done:
                transition = None
                prev_surf = None

        # --- Draw ---
        # 1. Nouvelle scène (ou scène courante)
        screen.blit(scenes[scene_idx], (0, 0))

        # 2. Transition par-dessus
        if transition is not None and prev_surf is not None:
            transition.draw(screen, prev_surf)

        # 3. HUD
        draw_hud(screen, TRANSITION_NAMES[tr_idx], tr_idx, scene_idx, font_ui,
                 transition is not None)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
