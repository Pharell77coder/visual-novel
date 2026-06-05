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
    
    # On commence par lister les pixels des 4 bords de l'image (le fond potentiel)
    frontiere = []
    for x in range(w):
        frontiere.append((x, 0))
        frontiere.append((x, h - 1))
    for y in range(1, h - 1):
        frontiere.append((0, y))
        frontiere.append((w - 1, y))
        
    # On récupère les couleurs des coins comme référence du damier
    couleurs_reference = [surf.get_at((0, 0)), surf.get_at((w-1, 0)), surf.get_at((0, h-1))]
    
    visite = set(frontiere)
    arr = pygame.PixelArray(out)
    
    while frontiere:
        cx, cy = frontiere.pop()
        
        # Récupère la couleur du pixel actuel
        col = surf.unmap_rgb(arr[cx, cy])
        r, g, b = col[0], col[1], col[2]
        
        # Est-ce que ce pixel ressemble aux couleurs du damier de fond ?
        est_damier = any(abs(r - ref[0]) < tol and abs(g - ref[1]) < tol and abs(b - ref[2]) < tol for ref in couleurs_reference)
        
        if est_damier:
            # On le rend transparent
            arr[cx, cy] = (0, 0, 0, 0)
            
            # On propage le nettoyage aux pixels voisins
            for nx, ny in ((cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)):
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visite:
                    visite.add((nx, ny))
                    frontiere.append((nx, ny))
                    
    del arr
    return out

# ── Assets Manager ─────────────────────────────────────────────────────────────
class Assets:
    def __init__(self):
        self.bg = {}
        self.detective = {}
        self.policiere = {}
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
        for name in ["bureau", "rue", "salle_interrogatoire", "scene_de_crime", "toit"]:
            path = os.path.join(bg_dir, f"{name}.png")
            if os.path.exists(path):
                self.bg[name] = load_img(path, (SCREEN_W, SCREEN_H))

    def _load_characters(self):
        # Detective : 10 expressions (0-9)
        det_dir = os.path.join(ASSETS, "characters", "detective")
        CH = 320  # hauteur portrait
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

    def _load_ui(self):
        ui_dir = os.path.join(ASSETS, "ui")
        for name in ["dialogue", "inventaire", "preuve"]:
            path = os.path.join(ui_dir, f"{name}.png")
            if os.path.exists(path):
                self.ui[name] = pygame.image.load(path).convert()

    def _load_audio(self):
        """Vérifie et configure le chemin absolu de la musique de fond."""
        # Jointure propre : racine/assets/audio/jazz.mp3
        music_path = os.path.join(ASSETS, "audio", DEFAULT_MUSIC)
        
        if os.path.exists(music_path):
            self.bg_music = music_path
        else:
            self.bg_music = None
            print(f"[!] Attention : Fichier audio introuvable à l'adresse : {music_path}")
        # ── AJOUT : Chargement du bruitage de clic ────────────────────────────
        click_path = os.path.join(ASSETS, "audio", DIALOGUE_CLICK)
        if os.path.exists(click_path):
            self.snd_click = pygame.mixer.Sound(click_path)
            self.snd_click.set_volume(0.2)  # Baisser un peu le volume pour que ce ne soit pas agressif
        else:
            self.snd_click = None
            print(f"[!] Attention : Bruitage de dialogue introuvable à : {click_path}")
