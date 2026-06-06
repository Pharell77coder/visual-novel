import pygame
import math
import random

from assets_manager import Assets
from models import Particle
from config import *

# ── Vitesse typewriter ─────────────────────────────────────────────────────────
SPEED_LEVELS = [0.3, 0.7, 1.0, 2.0, 4.0, 999]
SPEED_LABELS  = ["◂◂ très lent", "◂ lent", "● normal", "rapide ▸", "très rapide ▸▸", "⚡ instantané"]
SPEED_DEFAULT = 2   # index dans SPEED_LEVELS (= 1.0 char/frame)

# ── Dialogue Box ───────────────────────────────────────────────────────────────
class DialogueBox:
    W = 860
    H = 160
    MARGIN = 18
    LINE_H = 28

    def __init__(self, assets: Assets):
        self.assets = assets
        self.text = ""
        self.name = ""
        self.visible_chars = 0
        self.speed_idx = SPEED_DEFAULT
        self.speed = SPEED_LEVELS[self.speed_idx]
        self._speed_flash = 0.0   # secondes restantes d'affichage de l'indicateur
        self._accum = 0.0
        self.done = False
        self.choices = []
        self.choice_idx = 0
        self.show_choices = False
        # surface de la boîte
        self.surf = self._build_surf()
        self.x = (SCREEN_W - self.W) // 2
        self.y = SCREEN_H - self.H - 12

    def _build_surf(self):
        s = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        # fond sombre semi-transparent avec bord cyan
        pygame.draw.rect(s, (*DIALOGUE_BG, 230), (0, 0, self.W, self.H), border_radius=6)
        pygame.draw.rect(s, (*CYAN, 200),         (0, 0, self.W, self.H), width=2, border_radius=6)
        # NOTE : la ligne décorative du nom a été retirée d'ici (elle était figée
        # dans la surface et s'affichait même sans nom). Elle est désormais
        # dessinée dynamiquement dans draw() seulement quand self.name est défini.
        return s

    def set_text(self, text, name="", choices=None):
        self.text = text
        self.name = name
        self.visible_chars = 0
        self._accum = 0.0
        self.done = False
        self.choices = choices or []
        self.show_choices = False
        self.choice_idx = 0

    def skip(self):
        if not self.done:
            self.visible_chars = len(self.text)
            self.done = True
        elif self.choices:
            self.show_choices = True

    def speed_up(self):
        self.speed_idx = min(len(SPEED_LEVELS) - 1, self.speed_idx + 1)
        self.speed = SPEED_LEVELS[self.speed_idx]
        self._speed_flash = 1.8

    def speed_down(self):
        self.speed_idx = max(0, self.speed_idx - 1)
        self.speed = SPEED_LEVELS[self.speed_idx]
        self._speed_flash = 1.8

    def update(self, dt: float = 0.0):
        # Décompte du flash indicateur de vitesse
        if self._speed_flash > 0:
            self._speed_flash = max(0.0, self._speed_flash - dt)

        if not self.done:
            # 1. On mémorise le nombre ENTIER de lettres avant la mise à jour
            old_chars = int(self.visible_chars)
            
            # 2. Progression de l'affichage
            self._accum += self.speed
            self.visible_chars = min(len(self.text), int(self._accum))
            
            # 3. Calcul du nombre précis de nouvelles lettres apparues
            new_chars_count = int(self.visible_chars) - old_chars
            
            if new_chars_count > 0:
                # On isole le texte ajouté à cette frame
                added_text = self.text[old_chars:int(self.visible_chars)]
                
                # S'il y a du vrai texte (pas juste des espaces)
                if added_text.strip():
                    if self.assets.snd_click:
                        # ── LA CORRECTION : On utilise un canal pour forcer la répétition ──
                        # On trouve un canal audio libre
                        channel = pygame.mixer.find_channel()
                        if channel:
                            # stop() coupe immédiatement le clic précédent s'il tournait encore
                            channel.stop() 
                            # play() relance le son instantanément au millième de seconde près
                            channel.play(self.assets.snd_click)

            # 4. Fin du texte atteint
            if self.visible_chars >= len(self.text):
                self.done = True
                if self.choices:
                    self.show_choices = True
                    
    def select_choice(self, direction):
        if self.show_choices and self.choices:
            self.choice_idx = (self.choice_idx + direction) % len(self.choices)

    def get_choice(self):
        if self.show_choices and self.choices:
            return self.choice_idx
        return None

    def wrap_text(self, text, font, max_w):
        words = text.split(" ")
        lines, cur = [], ""
        for w in words:
            test = cur + (" " if cur else "") + w
            if font.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def draw(self, screen, t):
        # Animation légère de la boite (flottement)
        y_off = int(math.sin(t * 1.5) * 1.5)
        screen.blit(self.surf, (self.x, self.y + y_off))

        f = self.assets.font_med
        fs = self.assets.font_small

        # Nom du personnage
        if self.name:
            # Badge de nom — positionné ENTIÈREMENT au-dessus de la boîte
            # Badge height = 26px, on le place à -32 => bord bas à -32+26 = -6 (6px d'air)
            BADGE_H   = 26
            BADGE_OFF = -(BADGE_H + 6)   # 6px de marge entre badge et boîte

            name_surf = f.render(self.name, True, TEXT_NAME)
            nw = name_surf.get_width() + 20
            badge = pygame.Surface((nw, BADGE_H), pygame.SRCALPHA)
            pygame.draw.rect(badge, (*CYAN, 40),  (0, 0, nw, BADGE_H), border_radius=4)
            pygame.draw.rect(badge, (*CYAN, 180), (0, 0, nw, BADGE_H), width=1, border_radius=4)
            bx = self.x + self.MARGIN
            by = self.y + y_off + BADGE_OFF
            screen.blit(badge, (bx, by))
            screen.blit(name_surf, (bx + 10, by + (BADGE_H - name_surf.get_height()) // 2))

            # Ligne décorative sous le badge (seulement si un nom est présent)
            pygame.draw.line(screen,
                             (*CYAN, 90),
                             (self.x + self.MARGIN, self.y + y_off + 2),
                             (self.x + self.MARGIN + nw, self.y + y_off + 2),
                             1)

        # Texte principal (avec typewriter)
        visible = self.text[:int(self.visible_chars)]
        lines = self.wrap_text(visible, f, self.W - self.MARGIN * 2 - 20)
        for i, line in enumerate(lines[:4]):
            col = TEXT_MAIN
            surf = f.render(line, True, col)
            screen.blit(surf, (self.x + self.MARGIN + 10, self.y + y_off + 16 + i * self.LINE_H))

        # Indicateur "cliquez pour continuer"
        if self.done and not self.show_choices:
            blink = int(t * 3) % 2 == 0
            if blink:
                arrow = fs.render("▼ continuer", True, CYAN_DIM)
                screen.blit(arrow, (self.x + self.W - 130, self.y + y_off + self.H - 22))

        # Affichage des choix (Corrigé pour apparaître DANS la boîte de dialogue)
        if self.show_choices:
            # On place les boutons vers le bas de la boîte de dialogue, pas en dessous !
            cy = self.y + y_off + self.H - 50 
            
            for i, choice in enumerate(self.choices):
                selected = i == self.choice_idx
                cw = (self.W - (self.MARGIN * 2)) // len(self.choices) - 10
                cx = self.x + self.MARGIN + i * (cw + 10)
                
                # Fond du choix
                cs = pygame.Surface((cw, 34), pygame.SRCALPHA)
                if selected:
                    pygame.draw.rect(cs, (*CYAN, 60), (0, 0, cw, 34), border_radius=5)
                    pygame.draw.rect(cs, (*CYAN, 220), (0, 0, cw, 34), width=2, border_radius=5)
                else:
                    pygame.draw.rect(cs, (*DARK_BG, 220), (0, 0, cw, 34), border_radius=5)
                    pygame.draw.rect(cs, (*CYAN_DIM, 120), (0, 0, cw, 34), width=1, border_radius=5)
                screen.blit(cs, (cx, cy))
                
                col = CYAN if selected else TEXT_GRAY
                txt = f.render(choice, True, col)
                screen.blit(txt, (cx + (cw - txt.get_width()) // 2, cy + 8))

        # ── Indicateur de vitesse (flash temporaire) ───────────────────────────
        if self._speed_flash > 0:
            alpha = min(255, int(self._speed_flash * 200))
            label = SPEED_LABELS[self.speed_idx]
            fs2 = self.assets.font_small
            txt  = fs2.render(f"Vitesse : {label}", True, CYAN)
            badge_w = txt.get_width() + 20
            badge_h = 22
            bx = self.x + self.W - badge_w - 4
            by = self.y + y_off - badge_h - 6
            badge = pygame.Surface((badge_w, badge_h), pygame.SRCALPHA)
            pygame.draw.rect(badge, (*DARK_BG, min(210, alpha)), (0, 0, badge_w, badge_h), border_radius=4)
            pygame.draw.rect(badge, (*CYAN, min(200, alpha)), (0, 0, badge_w, badge_h), width=1, border_radius=4)
            badge.set_alpha(alpha)
            screen.blit(badge, (bx, by))
            txt_surf = pygame.Surface(txt.get_size(), pygame.SRCALPHA)
            txt_surf.blit(txt, (0, 0))
            txt_surf.set_alpha(alpha)
            screen.blit(txt_surf, (bx + 10, by + (badge_h - txt.get_height()) // 2))

# ── Panneau Preuves ─────────────────────────────────────────────────────────────
class EvidencePanel:
    def __init__(self, assets: Assets):
        self.assets = assets
        self.visible = False
        self.items = []   # liste de (nom, desc)
        self.selected = 0
        self.anim = 0.0

    def toggle(self):
        self.visible = not self.visible

    def add(self, name, desc):
        self.items.append((name, desc))

    def draw(self, screen, t):
        if not self.visible:
            return
        # Slide in depuis la droite
        target_x = SCREEN_W - 320
        px = int(target_x)
        py = 60

        panel = pygame.Surface((300, 340), pygame.SRCALPHA)
        pygame.draw.rect(panel, (*DARK_BG, 240), (0, 0, 300, 340), border_radius=8)
        pygame.draw.rect(panel, (*PINK_ACCENT, 200), (0, 0, 300, 340), width=2, border_radius=8)

        f = self.assets.font_med
        fs = self.assets.font_small

        title = f.render("── PREUVES ──", True, PINK_ACCENT)
        panel.blit(title, ((300 - title.get_width()) // 2, 10))

        for i, (name, desc) in enumerate(self.items):
            y = 50 + i * 60
            sel = i == self.selected
            row = pygame.Surface((280, 52), pygame.SRCALPHA)
            if sel:
                pygame.draw.rect(row, (*PINK_ACCENT, 40), (0, 0, 280, 52), border_radius=4)
                pygame.draw.rect(row, (*PINK_ACCENT, 160), (0, 0, 280, 52), width=1, border_radius=4)
            else:
                pygame.draw.rect(row, (20, 25, 45, 200), (0, 0, 280, 52), border_radius=4)
            nc = PINK_ACCENT if sel else GOLD
            ns = f.render(f"◆ {name}", True, nc)
            ds = fs.render(desc[:32], True, TEXT_GRAY)
            row.blit(ns, (8, 6))
            row.blit(ds, (8, 28))
            panel.blit(row, (10, y))

        screen.blit(panel, (px, py))

# ── Inventaire ──────────────────────────────────────────────────────────────────
class InventoryPanel:
    ITEMS = [
        ("Badge",     "Insigne de détective"),
        ("Dossier",   "Affaires en cours"),
        ("Revolver",  ".38 Special"),
    ]

    def __init__(self, assets: Assets):
        self.assets = assets
        self.visible = False

    def toggle(self):
        self.visible = not self.visible

    def draw(self, screen, t):
        if not self.visible:
            return
        px, py = 20, 60
        panel = pygame.Surface((260, 220), pygame.SRCALPHA)
        pygame.draw.rect(panel, (*DARK_BG, 240), (0, 0, 260, 220), border_radius=8)
        pygame.draw.rect(panel, (*CYAN, 200), (0, 0, 260, 220), width=2, border_radius=8)

        f = self.assets.font_med
        fs = self.assets.font_small

        title = f.render("── INVENTAIRE ──", True, CYAN)
        panel.blit(title, ((260 - title.get_width()) // 2, 10))

        for i, (name, desc) in enumerate(self.ITEMS):
            y = 50 + i * 55
            row = pygame.Surface((240, 46), pygame.SRCALPHA)
            pygame.draw.rect(row, (20, 30, 50, 200), (0, 0, 240, 46), border_radius=4)
            pygame.draw.rect(row, (*CYAN_DIM, 100), (0, 0, 240, 46), width=1, border_radius=4)
            ns = f.render(f"▸ {name}", True, GOLD)
            ds = fs.render(desc, True, TEXT_GRAY)
            row.blit(ns, (8, 4))
            row.blit(ds, (8, 24))
            panel.blit(row, (10, y))

        screen.blit(panel, (px, py))

# ── Backlog de dialogue ─────────────────────────────────────────────────────────
class BacklogPanel:
    """Historique scrollable de tous les dialogues déjà affichés.
    Touche B pour ouvrir/fermer. Molette ou ↑/↓ pour scroller.
    """
    PAD_X   = 55
    HEADER_H = 68   # hauteur réservée au titre + hint
    ENTRY_GAP = 5

    def __init__(self, assets: Assets):
        self.assets  = assets
        self.visible = False
        self.entries  = []   # list of {"name": str, "text": str}
        self.scroll   = 0    # index de la première entrée visible (0 = la plus ancienne)

    # ── API publique ───────────────────────────────────────────────────────────

    def add(self, name: str, text: str) -> None:
        """Ajoute une entrée au backlog (appelé à chaque chargement de node)."""
        if text and text.strip():
            self.entries.append({"name": name or "", "text": text})

    def toggle(self) -> None:
        self.visible = not self.visible
        if self.visible:
            # Ouvre sur les répliques les plus récentes
            self.scroll = max(0, len(self.entries) - self._page_size())

    def scroll_up(self) -> None:
        """Remonte vers les répliques plus anciennes."""
        self.scroll = max(0, self.scroll - 1)

    def scroll_down(self) -> None:
        """Redescend vers les répliques plus récentes."""
        self.scroll = min(max(0, len(self.entries) - self._page_size()),
                          self.scroll + 1)

    # ── Helpers internes ───────────────────────────────────────────────────────

    def _wrap(self, text: str, font, max_w: int) -> list:
        words = text.split()
        lines, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if font.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def _entry_lines(self, entry: dict, font, max_w: int) -> list:
        return self._wrap(entry["text"], font, max_w)

    def _entry_height(self, entry: dict, font_name, font_text, max_w: int) -> int:
        lines = self._entry_lines(entry, font_text, max_w)
        name_h = (font_name.get_height() + 4) if entry["name"] else 0
        return name_h + len(lines) * (font_text.get_height() + 2) + 16

    def _page_size(self) -> int:
        """Nombre approximatif d'entrées visibles (estimation grossière)."""
        fn = self.assets.font_med
        fs = self.assets.font_small
        max_w = SCREEN_W - self.PAD_X * 2 - 28
        available_h = SCREEN_H - self.HEADER_H - 20
        # Hauteur minimale d'une entrée (sans nom, 1 ligne)
        min_h = fs.get_height() + 2 + 16 + self.ENTRY_GAP
        return max(1, available_h // min_h)

    # ── Dessin ─────────────────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface, t: float) -> None:
        if not self.visible:
            return

        W, H   = SCREEN_W, SCREEN_H
        fn     = self.assets.font_med      # nom du perso
        fs     = self.assets.font_small    # corps du texte
        fb     = self.assets.font_big      # titre
        max_w  = W - self.PAD_X * 2 - 28  # largeur texte (laisse place scrollbar)

        # ── Fond semi-opaque ──────────────────────────────────────────────────
        bg = pygame.Surface((W, H), pygame.SRCALPHA)
        bg.fill((5, 8, 18, 225))
        screen.blit(bg, (0, 0))

        # ── En-tête ────────────────────────────────────────────────────────────
        title = fb.render("HISTORIQUE", True, CYAN)
        screen.blit(title, ((W - title.get_width()) // 2, 10))
        pygame.draw.line(screen, (*CYAN, 70), (self.PAD_X, 40), (W - self.PAD_X, 40), 1)
        hint = fs.render(
            "[B] fermer      [↑] [↓] ou molette pour naviguer", True, TEXT_GRAY)
        screen.blit(hint, ((W - hint.get_width()) // 2, 46))

        # ── Entrées ────────────────────────────────────────────────────────────
        y = self.HEADER_H
        bottom_limit = H - 20

        if not self.entries:
            msg = fn.render("Aucune réplique pour l'instant.", True, TEXT_GRAY)
            screen.blit(msg, ((W - msg.get_width()) // 2, H // 2))
            return

        visible_entries = self.entries[self.scroll:]
        for entry in visible_entries:
            eh = self._entry_height(entry, fn, fs, max_w)
            if y + eh > bottom_limit:
                break

            # Fond de l'entrée
            eb = pygame.Surface((max_w + 4, eh), pygame.SRCALPHA)
            pygame.draw.rect(eb, (12, 18, 40, 200), (0, 0, max_w + 4, eh), border_radius=5)
            pygame.draw.rect(eb, (*CYAN_DIM, 65), (0, 0, max_w + 4, eh), width=1, border_radius=5)
            screen.blit(eb, (self.PAD_X, y))

            iy = y + 8
            if entry["name"]:
                ns = fn.render(entry["name"], True, TEXT_NAME)
                screen.blit(ns, (self.PAD_X + 10, iy))
                iy += fn.get_height() + 4

            for line in self._entry_lines(entry, fs, max_w - 20):
                ls = fs.render(line, True, TEXT_MAIN)
                screen.blit(ls, (self.PAD_X + 10, iy))
                iy += fs.get_height() + 2

            y += eh + self.ENTRY_GAP

        # ── Scrollbar ──────────────────────────────────────────────────────────
        total = len(self.entries)
        page  = self._page_size()
        if total > page:
            sb_x = W - self.PAD_X - 14
            sb_y = self.HEADER_H
            sb_h = H - self.HEADER_H - 20
            pygame.draw.rect(screen, (*CYAN_DIM, 40),  (sb_x, sb_y, 8, sb_h), border_radius=4)
            max_s    = total - page
            thumb_h  = max(22, int(sb_h * page / total))
            thumb_y  = sb_y + int((sb_h - thumb_h) * self.scroll / max_s) if max_s else sb_y
            pygame.draw.rect(screen, (*CYAN, 160), (sb_x, thumb_y, 8, thumb_h), border_radius=4)

        # ── Flèches indicatrices ───────────────────────────────────────────────
        if self.scroll > 0:
            arr = fs.render("▲  répliques plus anciennes", True, CYAN_DIM)
            screen.blit(arr, (self.PAD_X, self.HEADER_H - 14))
        max_s = max(0, len(self.entries) - self._page_size())
        if self.scroll < max_s:
            arr = fs.render("▼  répliques plus récentes", True, CYAN_DIM)
            screen.blit(arr, (self.PAD_X, H - 18))


# ── Écran titre ─────────────────────────────────────────────────────────────────
class TitleScreen:
    def __init__(self, assets: Assets):
        self.assets = assets
        self.alpha = 0
        self.phase = "fade_in"  # fade_in → hold → done
        self.t = 0.0
        self.particles = []
        self.star_t = 0.0

    def update(self, dt):
        self.t += dt
        self.star_t += dt
        if self.phase == "fade_in":
            self.alpha = min(255, self.alpha + 3)
            if self.alpha >= 255:
                self.phase = "hold"
        # Spawn particles
        if random.random() < 0.3:
            x = random.randint(50, SCREEN_W - 50)
            y = SCREEN_H // 2 + 80
            self.particles.append(Particle(x, y, CYAN))
        self.particles = [p for p in self.particles if p.alive]
        for p in self.particles:
            p.update(dt)

    def handle_event(self, e):
        if self.phase == "hold":
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return True
        return False

    def draw(self, screen):
        # Fond avec gradient
        screen.fill(DARK_BG)
        # Étoiles
        for i in range(60):
            r = (i * 137 + 17) % SCREEN_W
            s = (i * 97  + 31) % (SCREEN_H // 2)
            a = int(120 + 100 * math.sin(self.star_t * 0.5 + i))
            pygame.draw.circle(screen, (a, a, min(255, a + 60)), (r, s), 1)

        # Lignes scan
        for y in range(0, SCREEN_H, 4):
            a = 30 + 10 * math.sin(y * 0.05 + self.t)
            pygame.draw.line(screen, (0, int(a), int(a*1.5)), (0, y), (SCREEN_W, y))

        # Titre
        title_s = self.assets.font_title.render(TITLE, True, CYAN)
        sub_s    = self.assets.font_med.render("UN THRILLER EN PIXEL ART", True, TEXT_GRAY)
        press_s  = self.assets.font_small.render("APPUYEZ SUR UNE TOUCHE POUR COMMENCER", True, CYAN_DIM)

        glow = pygame.Surface(title_s.get_size(), pygame.SRCALPHA)
        glow_col = (*CYAN, int(30 + 20 * math.sin(self.t * 2)))
        glow.fill(glow_col)
        screen.blit(glow, ((SCREEN_W - title_s.get_width()) // 2 - 4,
                            SCREEN_H // 2 - title_s.get_height() // 2 - 4))

        screen.blit(title_s, ((SCREEN_W - title_s.get_width()) // 2,
                               SCREEN_H // 2 - title_s.get_height() // 2))
        screen.blit(sub_s,   ((SCREEN_W - sub_s.get_width()) // 2,
                               SCREEN_H // 2 + 40))
        if self.phase == "hold" and int(self.t * 2) % 2 == 0:
            screen.blit(press_s, ((SCREEN_W - press_s.get_width()) // 2,
                                   SCREEN_H // 2 + 90))

        for p in self.particles:
            p.draw(screen)

        # Overlay d'alpha
        if self.alpha < 255:
            ov = pygame.Surface((SCREEN_W, SCREEN_H))
            ov.fill(BLACK)
            ov.set_alpha(255 - self.alpha)
            screen.blit(ov, (0, 0))