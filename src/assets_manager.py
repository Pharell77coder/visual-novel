import pygame
import os

from config import ASSETS, DIALOGUE_CLICK, SCREEN_W, SCREEN_H, DEFAULT_MUSIC

# ── Utilitaires ────────────────────────────────────────────────────────────────
def load_img(path, size=None, colorkey=None):
    img = pygame.image.load(path).convert()
    if colorkey:
        img.set_colorkey(colorkey)
    if size:
        img = pygame.transform.scale(img, size)
    return img

def load_alpha(path, size=None):
    """Charge une image en gardant la transparence."""
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.smoothscale(img, size)
    return img

def remove_checker(surf, tol=0):
    """Supprime le damier de fond en partant des bords, sans toucher à l'intérieur du personnage."""
    out = surf.copy().convert_alpha()
    w, h = out.get_size()
    
    frontiere = []
    for x in range(w):
        frontiere.append((x, 0))
        frontiere.append((x, h - 1))
    for y in range(1, h - 1):
        frontiere.append((0, y))
        frontiere.append((w - 1, y))
        
    couleurs_reference = [surf.get_at((0, 0)), surf.get_at((w-1, 0)), surf.get_at((0, h-1))]
    
    visite = set(frontiere)
    arr = pygame.PixelArray(out)
    
    while frontiere:
        cx, cy = frontiere.pop()
        col = surf.unmap_rgb(arr[cx, cy])
        r, g, b = col[0], col[1], col[2]
        est_damier = any(abs(r - ref[0]) < tol and abs(g - ref[1]) < tol and abs(b - ref[2]) < tol for ref in couleurs_reference)
        if est_damier:
            arr[cx, cy] = (0, 0, 0, 0)
            for nx, ny in ((cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)):
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visite:
                    visite.add((nx, ny))
                    frontiere.append((nx, ny))
    del arr
    return out

def _load_char_sprites(char_dir, char_name, count, ch_height):
    """
    Charge N sprites depuis char_dir.
    Retourne un dict {index: surface}.
    Si un sous-dossier 'left/' ou 'right/' existe, charge depuis là ;
    sinon charge depuis char_dir directement.
    """
    sprites = {}
    for i in range(count):
        path = os.path.join(char_dir, f"{char_name}{i}.png")
        if os.path.exists(path):
            raw = load_alpha(path)
            raw = remove_checker(raw)
            ratio = raw.get_width() / raw.get_height()
            w = int(ch_height * ratio)
            sprites[i] = pygame.transform.smoothscale(raw, (w, ch_height))
    return sprites


def _load_char_sprites_sided(char_dir, char_name, count, ch_height):
    """
    Charge les variantes directionnelles left/ et right/ d'un personnage.

    Structure attendue dans le repo :
        characters/<char>/left/<char>0.png … <char>N.png
        characters/<char>/right/<char>0.png … <char>N.png

    Retourne un dict :
        {
            "left":  {0: Surface, 1: Surface, …},
            "right": {0: Surface, 1: Surface, …},
            "default": {0: Surface, …},   # racine du dossier (fallback)
        }

    Logique de fallback :
        - Si left/ absent  → miroir horizontal de right/ (ou du default)
        - Si right/ absent → miroir horizontal de left/ (ou du default)
        - Si aucun sous-dossier → default = racine, left/right = miroirs auto
    """
    result = {"left": {}, "right": {}, "default": {}}

    # 1. Charger le dossier racine (toujours)
    result["default"] = _load_char_sprites(char_dir, char_name, count, ch_height)

    # 2. Charger left/ si présent
    left_dir = os.path.join(char_dir, "left")
    if os.path.isdir(left_dir):
        result["left"] = _load_char_sprites(left_dir, char_name, count, ch_height)

    # 3. Charger right/ si présent
    right_dir = os.path.join(char_dir, "right")
    if os.path.isdir(right_dir):
        result["right"] = _load_char_sprites(right_dir, char_name, count, ch_height)

    # 4. Générer les miroirs manquants
    source_for_flip = result["right"] or result["left"] or result["default"]

    if not result["left"]:
        result["left"] = {
            i: pygame.transform.flip(s, True, False)
            for i, s in source_for_flip.items()
        }
    if not result["right"]:
        result["right"] = {
            i: pygame.transform.flip(s, True, False)
            for i, s in (result["left"] or result["default"]).items()
        }

    return result

# ── Assets Manager ─────────────────────────────────────────────────────────────
class Assets:
    def __init__(self):
        self.bg = {}
        # Sprites avec variantes directionnelles.
        # Chaque entrée est un dict {"left": {expr: Surface}, "right": {…}, "default": {…}}
        self.detective = {}
        self.policiere = {}
        self.ferriere  = {}
        self.natasha   = {}
        self.taro      = {}
        self.architect = {}
        self.mira      = {}
        self.ghost     = {}
        self.senator   = {}
        self.ui = {}
        self.font_big   = None
        self.font_med   = None
        self.font_small = None
        self.bg_music = None
        self._load_fonts()
        self._load_backgrounds()
        self._load_characters()
        self._load_ui()
        self._load_audio()

    def _load_fonts(self):
        font_path = os.path.join(ASSETS, "font", "joystix.ttf")
        if os.path.exists(font_path):
            self.font_big   = pygame.font.Font(font_path, 22)
            self.font_med   = pygame.font.Font(font_path, 16)
            self.font_small = pygame.font.Font(font_path, 12)
            self.font_title = pygame.font.Font(font_path, 36)
        else:
            self.font_big   = pygame.font.SysFont("monospace", 22, bold=True)
            self.font_med   = pygame.font.SysFont("monospace", 16)
            self.font_small = pygame.font.SysFont("monospace", 12)
            self.font_title = pygame.font.SysFont("monospace", 36, bold=True)

    def _load_backgrounds(self):
        bg_dir = os.path.join(ASSETS, "backgrounds")
        # Chargement automatique de tous les PNG du dossier backgrounds
        for fname in sorted(os.listdir(bg_dir)):
            if fname.lower().endswith(".png"):
                name = fname[:-4]   # "bureau.png" → "bureau"
                path = os.path.join(bg_dir, fname)
                self.bg[name] = load_img(path, (SCREEN_W, SCREEN_H))
        # Alias : le script Ch7 utilise "sous_sol" mais le fichier est data_center.png
        if "data_center" in self.bg and "sous_sol" not in self.bg:
            self.bg["sous_sol"] = self.bg["data_center"]

    def _load_characters(self):
        CH = 320  # hauteur portrait standard

        # Detective : 10 expressions (0-9)
        det_dir = os.path.join(ASSETS, "characters", "detective")
        self.detective = _load_char_sprites_sided(det_dir, "detective", 10, CH)

        # Policière : 4 expressions (0-3)
        pol_dir = os.path.join(ASSETS, "characters", "policiere")
        self.policiere = _load_char_sprites_sided(pol_dir, "policiere", 4, CH)

        # Nouveaux personnages : 4 expressions chacun (0-3)
        chars_cfg = {
            "ferriere":  ("ferriere",  4),
            "natasha":   ("natasha",   4),
            "taro":      ("taro",      4),
            "architect": ("architect", 4),
            "mira":      ("mira",      4),
            "ghost":     ("ghost",     4),
            "senator":   ("senator",   4),
        }
        for attr, (char_name, count) in chars_cfg.items():
            char_dir = os.path.join(ASSETS, "characters", char_name)
            # BUGFIX : fallback pour le typo "nathasha" dans le dépôt
            if char_name == "natasha" and not os.path.exists(char_dir):
                char_dir = os.path.join(ASSETS, "characters", "nathasha")
            setattr(self, attr, _load_char_sprites_sided(char_dir, char_name, count, CH))

    def _load_ui(self):
        ui_dir = os.path.join(ASSETS, "ui")
        for name in ["dialogue", "inventaire", "preuve"]:
            path = os.path.join(ui_dir, f"{name}.png")
            if os.path.exists(path):
                self.ui[name] = pygame.image.load(path).convert()

    def _load_audio(self):
        music_path = os.path.join(ASSETS, "audio", DEFAULT_MUSIC)
        if os.path.exists(music_path):
            self.bg_music = music_path
        else:
            self.bg_music = None
            print(f"[!] Attention : Fichier audio introuvable à : {music_path}")

        click_path = os.path.join(ASSETS, "audio", DIALOGUE_CLICK)
        if os.path.exists(click_path):
            self.snd_click = pygame.mixer.Sound(click_path)
            self.snd_click.set_volume(0.2)
        else:
            self.snd_click = None
            print(f"[!] Attention : Bruitage introuvable à : {click_path}")

    def get_char(self, char_name: str, expr: int = 0, side: str = "left"):
        """
        Retourne le sprite d'un personnage à l'expression et la direction données.

        Parameters
        ----------
        char_name : str     Nom du personnage ("detective", "policiere", …)
        expr      : int     Index d'expression (0-9 pour detective, 0-3 pour les autres)
        side      : str     "left" | "right"  (correspond au sous-dossier d'asset)

        Priorité des fallbacks :
            side → "default" → autre side → None
        """
        table = {
            "detective": self.detective,
            "policiere":  self.policiere,
            "ferriere":   self.ferriere,
            "natasha":    self.natasha,
            "taro":       self.taro,
            "architect":  self.architect,
            "mira":       self.mira,
            "ghost":      self.ghost,
            "senator":    self.senator,
        }
        sided = table.get(char_name)
        if sided is None:
            return None

        # Essayer dans l'ordre : side demandé → default → autre side
        other = "right" if side == "left" else "left"
        for key in (side, "default", other):
            sprites = sided.get(key, {})
            surf = sprites.get(expr) or sprites.get(0)
            if surf is not None:
                return surf
        return None