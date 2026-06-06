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
    """Charge N sprites pour un personnage, retourne un dict {index: surface}."""
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

# ── Assets Manager ─────────────────────────────────────────────────────────────
class Assets:
    def __init__(self):
        self.bg = {}
        self.detective = {}
        self.policiere = {}
        # Nouveaux personnages Ch2 & Ch3
        self.ferriere  = {}
        self.natasha   = {}
        self.taro      = {}
        self.architect = {}
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
        # Ch1 backgrounds
        for name in ["bureau", "rue", "salle_interrogatoire", "scene_de_crime", "toit"]:
            path = os.path.join(bg_dir, f"{name}.png")
            if os.path.exists(path):
                self.bg[name] = load_img(path, (SCREEN_W, SCREEN_H))
        # Ch2 & Ch3 backgrounds
        for name in ["aeroport_jetpack", "geneve"]:
            path = os.path.join(bg_dir, f"{name}.png")
            if os.path.exists(path):
                self.bg[name] = load_img(path, (SCREEN_W, SCREEN_H))

    def _load_characters(self):
        CH = 320  # hauteur portrait standard

        # Detective : 10 expressions (0-9)
        det_dir = os.path.join(ASSETS, "characters", "detective")
        for i in range(10):
            path = os.path.join(det_dir, f"detective{i}.png")
            if os.path.exists(path):
                raw = load_alpha(path)
                raw = remove_checker(raw)
                ratio = raw.get_width() / raw.get_height()
                w = int(CH * ratio)
                self.detective[i] = pygame.transform.smoothscale(raw, (w, CH))

        # Policière : 4 expressions (0-3)
        pol_dir = os.path.join(ASSETS, "characters", "policiere")
        for i in range(4):
            path = os.path.join(pol_dir, f"policiere{i}.png")
            if os.path.exists(path):
                raw = load_alpha(path)
                raw = remove_checker(raw)
                ratio = raw.get_width() / raw.get_height()
                w = int(CH * ratio)
                self.policiere[i] = pygame.transform.smoothscale(raw, (w, CH))

        # Nouveaux personnages : 4 expressions chacun (0-3)
        chars_to_load = {
            "ferriere":  self.ferriere,
            "natasha":   self.natasha,
            "taro":      self.taro,
            "architect": self.architect,
        }
        for char_name, target_dict in chars_to_load.items():
            char_dir = os.path.join(ASSETS, "characters", char_name)
            loaded = _load_char_sprites(char_dir, char_name, 4, CH)
            target_dict.update(loaded)

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

    def get_char(self, char_name, expr=0):
        """Helper centralisé : retourne le sprite d'un personnage à l'expression donnée."""
        table = {
            "detective": self.detective,
            "policiere":  self.policiere,
            "ferriere":   self.ferriere,
            "natasha":    self.natasha,
            "taro":       self.taro,
            "architect":  self.architect,
        }
        sprites = table.get(char_name, {})
        return sprites.get(expr, sprites.get(0))