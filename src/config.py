import os
from enum import Enum

# ── Configuration ─────────────────────────────────────────────────────────────
SCREEN_W, SCREEN_H = 960, 540
FPS = 60
TITLE = "NUIT SANS TÉMOIN"

# Couleurs
BLACK        = (0,   0,   0  )
WHITE        = (255, 255, 255)
CYAN         = (0,   220, 255)
CYAN_DIM     = (0,   120, 160)
DARK_BG      = (8,   10,  20 )
DIALOGUE_BG  = (10,  14,  28 )
TEXT_MAIN    = (220, 230, 245)
TEXT_NAME    = (0,   220, 255)
TEXT_GRAY    = (140, 150, 170)
PINK_ACCENT  = (255, 80,  160)
GOLD         = (255, 200, 60 )
RED_ACCENT   = (220, 50,  50 )

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SRC_DIR)
ASSETS = os.path.join(BASE, "assets")
# print(f"Assets path: {ASSETS}")

# ── Expressions ────────────────────────────────────────────────────────────────
class Expr(Enum):
    NEUTRE   = 0
    SOURIRE  = 1
    LARGE    = 2
    COLERE   = 3
    TRISTE   = 4
    REGARD   = 5
    SMIRK    = 6
    SHOCKED  = 7   # detective7 (index ≥ 7 → fallback to 0)

POLICIERE_EXPR = {
    "neutre":   0,
    "serieux":  1,
    "sourire":  2,
    "shocked":  3,
}

# ── Configuration Audio ────────────────────────────────────────────────────────
DEFAULT_MUSIC = "jazz.mp3"