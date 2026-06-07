import pygame
import math
import random

from assets_manager import Assets
from models import Particle
from config import *

# ── Vitesse typewriter ─────────────────────────────────────────────────────────
SPEED_LEVELS = [0.3, 0.7, 1.0, 2.0, 4.0, 999]
SPEED_LABELS  = ["◂◂ très lent", "◂ lent", "● normal", "rapide ▸", "très rapide ▸▸", "⚡ instantané"]
SPEED_DEFAULT = 2

# ── Dialogue Box ───────────────────────────────────────────────────────────────
class DialogueBox:
    W = 860
    H = 160
    MARGIN = 18
    LINE_H = 28

    # ── Backlog (historique des dialogues) ────────────────────────────────────
    BACKLOG_MAX    = 80    # entrées maximum conservées
    BACKLOG_W      = 700
    BACKLOG_H      = 380
    BACKLOG_LINE_H = 26

    def __init__(self, assets: Assets):
        self.assets = assets
        self.text = ""
        self.name = ""
        self.visible_chars = 0
        self.speed_idx = SPEED_DEFAULT
        self.speed = SPEED_LEVELS[self.speed_idx]
        self._speed_flash = 0.0
        self._accum = 0.0
        self.done = False
        self.choices = []
        self.choice_idx = 0
        self.show_choices = False
        self.surf = self._build_surf()
        self.x = (SCREEN_W - self.W) // 2
        self.y = SCREEN_H - self.H - 12

        # Backlog
        self._backlog: list[tuple[str, str]] = []  # (name, text)
        self.backlog_open  = False
        self._backlog_scroll = 0   # index du premier item visible (0 = bas)

    def _build_surf(self):
        s = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        pygame.draw.rect(s, (*DIALOGUE_BG, 230), (0, 0, self.W, self.H), border_radius=6)
        pygame.draw.rect(s, (*CYAN, 200),         (0, 0, self.W, self.H), width=2, border_radius=6)
        return s

    def set_text(self, text, name="", choices=None):
        # Ajouter l'entrée courante dans le backlog si elle contient du texte
        if self.text and self.text.strip():
            entry = (self.name or "", self.text)
            self._backlog.append(entry)
            if len(self._backlog) > self.BACKLOG_MAX:
                self._backlog.pop(0)
            # Réinitialiser le scroll pour montrer le bas (le plus récent)
            self._backlog_scroll = 0

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

    # ── Backlog API ────────────────────────────────────────────────────────────

    def toggle_backlog(self):
        """Ouvre / ferme le panneau backlog."""
        self.backlog_open = not self.backlog_open
        if self.backlog_open:
            self._backlog_scroll = 0   # afficher les lignes les plus récentes

    def backlog_scroll(self, direction: int):
        """
        Scrolle dans le backlog.
        direction > 0 → vers le passé (plus vieux)
        direction < 0 → vers le présent (plus récent)
        """
        if not self.backlog_open:
            return
        # Calculer le max scroll (nombre de lignes rendues - lignes visibles)
        visible_lines = max(1, (self.BACKLOG_H - 60) // self.BACKLOG_LINE_H)
        max_scroll = max(0, len(self._backlog) - visible_lines)
        self._backlog_scroll = max(0, min(max_scroll, self._backlog_scroll + direction))

    def update(self, dt: float = 0.0):
        if self._speed_flash > 0:
            self._speed_flash = max(0.0, self._speed_flash - dt)

        if not self.done:
            old_chars = int(self.visible_chars)
            self._accum += self.speed
            self.visible_chars = min(len(self.text), int(self._accum))
            new_chars_count = int(self.visible_chars) - old_chars
            if new_chars_count > 0:
                added_text = self.text[old_chars:int(self.visible_chars)]
                if added_text.strip():
                    if self.assets.snd_click:
                        channel = pygame.mixer.find_channel()
                        if channel:
                            channel.stop()
                            channel.play(self.assets.snd_click)
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
        y_off = int(math.sin(t * 1.5) * 1.5)
        screen.blit(self.surf, (self.x, self.y + y_off))

        f  = self.assets.font_med
        fs = self.assets.font_small

        if self.name:
            BADGE_H   = 26
            BADGE_OFF = -(BADGE_H + 6)
            name_surf = f.render(self.name, True, TEXT_NAME)
            nw = name_surf.get_width() + 20
            badge = pygame.Surface((nw, BADGE_H), pygame.SRCALPHA)
            pygame.draw.rect(badge, (*CYAN, 40),  (0, 0, nw, BADGE_H), border_radius=4)
            pygame.draw.rect(badge, (*CYAN, 180), (0, 0, nw, BADGE_H), width=1, border_radius=4)
            bx = self.x + self.MARGIN
            by = self.y + y_off + BADGE_OFF
            screen.blit(badge, (bx, by))
            screen.blit(name_surf, (bx + 10, by + (BADGE_H - name_surf.get_height()) // 2))
            pygame.draw.line(screen, (*CYAN, 90),
                             (self.x + self.MARGIN, self.y + y_off + 2),
                             (self.x + self.MARGIN + nw, self.y + y_off + 2), 1)

        visible = self.text[:int(self.visible_chars)]
        lines = self.wrap_text(visible, f, self.W - self.MARGIN * 2 - 20)
        for i, line in enumerate(lines[:4]):
            surf = f.render(line, True, TEXT_MAIN)
            screen.blit(surf, (self.x + self.MARGIN + 10, self.y + y_off + 16 + i * self.LINE_H))

        if self.done and not self.show_choices:
            blink = int(t * 3) % 2 == 0
            if blink:
                arrow = fs.render("▼ continuer", True, CYAN_DIM)
                screen.blit(arrow, (self.x + self.W - 130, self.y + y_off + self.H - 22))

        if self.show_choices:
            cy = self.y + y_off + self.H - 50
            for i, choice in enumerate(self.choices):
                selected = i == self.choice_idx
                cw = (self.W - (self.MARGIN * 2)) // len(self.choices) - 10
                cx = self.x + self.MARGIN + i * (cw + 10)
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

        if self._speed_flash > 0:
            alpha = min(255, int(self._speed_flash * 200))
            label = SPEED_LABELS[self.speed_idx]
            fs2  = self.assets.font_small
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

        # ── Backlog overlay ────────────────────────────────────────────────────
        if self.backlog_open:
            self._draw_backlog(screen)

    # ── Rendu du backlog ───────────────────────────────────────────────────────

    def _draw_backlog(self, screen: pygame.Surface):
        """Affiche le panneau historique des dialogues (style VN classique)."""
        fn  = self.assets.font_med
        fs  = self.assets.font_small
        fb  = self.assets.font_big

        BW, BH = self.BACKLOG_W, self.BACKLOG_H
        bx = (SCREEN_W - BW) // 2
        by = (SCREEN_H - BH) // 2

        # Voile de fond
        veil = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 180))
        screen.blit(veil, (0, 0))

        # Fenêtre
        win = pygame.Surface((BW, BH), pygame.SRCALPHA)
        pygame.draw.rect(win, (*DARK_BG, 250), (0, 0, BW, BH), border_radius=10)
        pygame.draw.rect(win, (*CYAN, 200),    (0, 0, BW, BH), width=2, border_radius=10)

        # En-tête
        title_s = fb.render("── HISTORIQUE ──", True, CYAN)
        win.blit(title_s, ((BW - title_s.get_width()) // 2, 10))
        hint_s  = fs.render("[B] / [Échap] fermer   [↑↓] défiler", True, TEXT_GRAY)
        win.blit(hint_s,  ((BW - hint_s.get_width()) // 2, 36))
        pygame.draw.line(win, (*CYAN, 60), (16, 56), (BW - 16, 56), 1)

        screen.blit(win, (bx, by))

        # ── Zone de texte défilable ────────────────────────────────────────────
        CONTENT_TOP    = by + 62
        CONTENT_BOTTOM = by + BH - 10
        CONTENT_H      = CONTENT_BOTTOM - CONTENT_TOP
        PAD            = 18
        LINE_H         = self.BACKLOG_LINE_H
        MAX_TEXT_W     = BW - PAD * 2 - 16   # -16 pour la barre de scroll

        # Préparer toutes les lignes rendues (entrées les plus récentes en bas)
        all_lines: list[tuple[str, tuple, bool]] = []  # (texte, couleur, is_name)
        for name, txt in self._backlog:
            if name:
                all_lines.append((name, TEXT_NAME, True))
            # Wrap text
            words = txt.split()
            cur = ""
            wrapped = []
            for w in words:
                test = (cur + " " + w).strip()
                if fn.size(test)[0] <= MAX_TEXT_W:
                    cur = test
                else:
                    if cur:
                        wrapped.append(cur)
                    cur = w
            if cur:
                wrapped.append(cur)
            for line in wrapped:
                all_lines.append((line, TEXT_MAIN, False))
            all_lines.append(("", TEXT_GRAY, False))   # ligne vide entre entrées

        total_lines = len(all_lines)
        visible_count = max(1, CONTENT_H // LINE_H)

        # scroll : 0 = afficher les lignes les plus récentes (bas)
        # _backlog_scroll positif = remonter vers le passé
        max_scroll = max(0, total_lines - visible_count)
        scroll = max(0, min(max_scroll, self._backlog_scroll))
        # On affiche depuis la fin (lignes les plus récentes en bas)
        start_idx = max(0, total_lines - visible_count - scroll)
        end_idx   = min(total_lines, start_idx + visible_count)

        # Clip rect pour la zone de texte
        clip_rect = pygame.Rect(bx + PAD, CONTENT_TOP, BW - PAD * 2, CONTENT_H)
        old_clip = screen.get_clip()
        screen.set_clip(clip_rect)

        for i, li in enumerate(all_lines[start_idx:end_idx]):
            txt, col, is_name = li
            if not txt:
                continue
            font = fs if not is_name else fs
            col_use = col
            if is_name:
                ns = fs.render(txt, True, col_use)
                screen.blit(ns, (bx + PAD, CONTENT_TOP + i * LINE_H))
            else:
                ls = fn.render(txt, True, col_use)
                screen.blit(ls, (bx + PAD + 8, CONTENT_TOP + i * LINE_H))

        screen.set_clip(old_clip)

        # ── Barre de scroll ────────────────────────────────────────────────────
        if total_lines > visible_count:
            sb_x  = bx + BW - 14
            sb_y  = CONTENT_TOP
            sb_h  = CONTENT_H
            # Poignée
            thumb_h = max(20, int(sb_h * visible_count / total_lines))
            # Position : scroll 0 = bas → thumb en bas
            thumb_pos = int((sb_h - thumb_h) * (max_scroll - scroll) / max(1, max_scroll))
            pygame.draw.rect(screen, (*CYAN_DIM, 60), (sb_x, sb_y, 8, sb_h), border_radius=4)
            pygame.draw.rect(screen, (*CYAN, 180), (sb_x, sb_y + thumb_pos, 8, thumb_h), border_radius=4)


# ══════════════════════════════════════════════════════════════════════════════

# Durées d'animation (secondes)
_FLASH_DUR    = 0.55   # flash d'activation d'un slot de sélection
_COMBINE_DUR  = 0.90   # animation de fusion
_RESULT_DUR   = 3.50   # durée d'affichage de la déduction résultante

class EvidencePanel:
    """
    Panneau de preuves étendu.

    Modes :
        "browse"  — navigation normale (↑↓ / clic)
        "select"  — sélection de deux preuves à combiner

    Touches (quand le panneau est ouvert) :
        ↑ / ↓       naviguer
        C           basculer en mode sélection
        Entrée      en mode select : marquer / démarquer une preuve
        Espace      en mode select : lancer la combinaison si 2 slots pleins
        Échap       annuler la sélection / fermer
    """

    PANEL_W  = 320
    ROW_H    = 60
    ROW_GAP  = 6
    HEADER_H = 52

    def __init__(self, assets: Assets, deduction_engine=None):
        self.assets    = assets
        self.deduction = deduction_engine   # DeductionEngine | None
        self.visible   = False
        self.items     = []          # list of (nom, desc)
        self.selected  = 0           # indice survolé

        # Mode combinaison
        self._mode         = "browse"  # "browse" | "select"
        self._sel_a: int | None = None
        self._sel_b: int | None = None

        # Animations
        self._flash_a    = 0.0   # timer flash slot A
        self._flash_b    = 0.0   # timer flash slot B
        self._combine_t  = 0.0   # timer animation fusion (0 = inactive)
        self._combining  = False
        self._result_t   = 0.0   # timer affichage résultat
        self._result_msg: dict | None = None   # déduction débloquée
        self._fail_t     = 0.0   # timer message échec
        self._fail_msg   = ""

    # ── API ────────────────────────────────────────────────────────────────────

    def toggle(self):
        self.visible = not self.visible
        if not self.visible:
            self._reset_selection()

    def add(self, name, desc):
        self.items.append((name, desc))

    # ── Événements ────────────────────────────────────────────────────────────

    def handle_event(self, event) -> bool:
        """Retourne True si l'événement a été consommé."""
        if not self.visible:
            return False
        if self._combining:
            return True   # bloque tout pendant l'animation

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self._mode == "select":
                    self._reset_selection()
                else:
                    self.toggle()
                return True

            if event.key == pygame.K_c:
                if self._mode == "browse":
                    self._mode = "select"
                    self._sel_a = None
                    self._sel_b = None
                else:
                    self._reset_selection()
                return True

            if event.key in (pygame.K_UP,):
                self.selected = max(0, self.selected - 1)
                return True
            if event.key in (pygame.K_DOWN,):
                self.selected = min(len(self.items) - 1, self.selected + 1)
                return True

            if event.key == pygame.K_RETURN and self._mode == "select":
                self._toggle_select(self.selected)
                return True

            if event.key == pygame.K_SPACE and self._mode == "select":
                if self._sel_a is not None and self._sel_b is not None:
                    self._start_combine()
                return True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Hors panneau → fermer
            panel_rect = pygame.Rect(SCREEN_W - self.PANEL_W - 10, 60,
                                     self.PANEL_W, self._panel_height())
            if not panel_rect.collidepoint(event.pos):
                if self._mode == "select":
                    self._reset_selection()
                else:
                    self.toggle()
                return True
            # Clic sur une ligne
            row_i = self._row_at(event.pos)
            if row_i is not None:
                if self._mode == "select":
                    self._toggle_select(row_i)
                else:
                    self.selected = row_i
                return True
            # Clic sur le bouton [C] combiner
            if self._mode == "browse" and len(self.items) >= 2:
                btn = self._combine_btn_rect()
                if btn.collidepoint(event.pos):
                    self._mode = "select"
                    return True
            # Clic sur [Combiner !]
            if self._mode == "select" and self._sel_a is not None and self._sel_b is not None:
                go_btn = self._go_btn_rect()
                if go_btn and go_btn.collidepoint(event.pos):
                    self._start_combine()
                    return True

        elif event.type == pygame.MOUSEMOTION:
            row_i = self._row_at(event.pos)
            if row_i is not None:
                self.selected = row_i

        return False

    # ── Logique de sélection ──────────────────────────────────────────────────

    def _toggle_select(self, idx: int):
        if self._sel_a == idx:
            self._sel_a = None
        elif self._sel_b == idx:
            self._sel_b = None
        elif self._sel_a is None:
            self._sel_a = idx
            self._flash_a = _FLASH_DUR
        elif self._sel_b is None:
            self._sel_b = idx
            self._flash_b = _FLASH_DUR
        # Si les deux slots sont déjà pleins, remplacer le slot A
        else:
            self._sel_a = idx
            self._flash_a = _FLASH_DUR

    def _start_combine(self):
        if self._sel_a is None or self._sel_b is None:
            return
        self._combining  = True
        self._combine_t  = _COMBINE_DUR

    def _finish_combine(self):
        """Appelé quand l'animation de fusion se termine."""
        self._combining = False
        if self.deduction is None or self._sel_a is None or self._sel_b is None:
            self._show_fail("Aucune déduction disponible.")
            self._reset_selection()
            return

        name_a = self.items[self._sel_a][0]
        name_b = self.items[self._sel_b][0]
        result = self.deduction.try_combine(name_a, name_b)

        if result:
            self._result_msg = result
            self._result_t   = _RESULT_DUR
        else:
            self._show_fail("Ces deux indices ne mènent à rien de nouveau…")

        self._reset_selection()

    def _show_fail(self, msg: str):
        self._fail_msg = msg
        self._fail_t   = 2.0

    def _reset_selection(self):
        self._mode  = "browse"
        self._sel_a = None
        self._sel_b = None

    # ── Géométrie ─────────────────────────────────────────────────────────────

    def _panel_height(self) -> int:
        rows = max(1, len(self.items))
        base = self.HEADER_H + rows * (self.ROW_H + self.ROW_GAP)
        if self._mode == "select":
            base += 54   # barre d'action en bas
        elif len(self.items) >= 2:
            base += 36   # bouton [C]
        return min(base, SCREEN_H - 80)

    def _panel_rect(self) -> pygame.Rect:
        return pygame.Rect(SCREEN_W - self.PANEL_W - 10, 60,
                           self.PANEL_W, self._panel_height())

    def _row_rect(self, i: int, pr: pygame.Rect) -> pygame.Rect:
        y = pr.y + self.HEADER_H + i * (self.ROW_H + self.ROW_GAP)
        return pygame.Rect(pr.x + 8, y, pr.w - 16, self.ROW_H)

    def _row_at(self, pos) -> "int | None":
        pr = self._panel_rect()
        for i in range(len(self.items)):
            if self._row_rect(i, pr).collidepoint(pos):
                return i
        return None

    def _combine_btn_rect(self) -> pygame.Rect:
        pr = self._panel_rect()
        y  = pr.y + self.HEADER_H + len(self.items) * (self.ROW_H + self.ROW_GAP) + 4
        return pygame.Rect(pr.x + 8, y, pr.w - 16, 28)

    def _go_btn_rect(self) -> "pygame.Rect | None":
        if self._sel_a is None or self._sel_b is None:
            return None
        pr = self._panel_rect()
        y  = pr.y + self._panel_height() - 48
        return pygame.Rect(pr.x + 8, y, pr.w - 16, 36)

    # ── Mise à jour ────────────────────────────────────────────────────────────

    def update(self, dt: float):
        self._flash_a   = max(0.0, self._flash_a - dt)
        self._flash_b   = max(0.0, self._flash_b - dt)
        self._fail_t    = max(0.0, self._fail_t  - dt)
        self._result_t  = max(0.0, self._result_t - dt)

        if self._combining:
            self._combine_t = max(0.0, self._combine_t - dt)
            if self._combine_t <= 0.0:
                self._finish_combine()

    # ── Rendu ──────────────────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface, t: float):
        # NOTE: update() est appelé séparément par VNEngine._update(dt) avec le vrai dt.
        # Ne PAS appeler self.update() ici pour éviter un double avancement des timers.

        if not self.visible:
            # Afficher le résultat de déduction même panneau fermé
            if self._result_t > 0 and self._result_msg:
                self._draw_deduction_popup(screen, t)
            return

        pr = self._panel_rect()
        fn = self.assets.font_med
        fs = self.assets.font_small

        # ── Fond du panneau ────────────────────────────────────────────────────
        panel = pygame.Surface((pr.w, pr.h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (*DARK_BG, 245), (0, 0, pr.w, pr.h), border_radius=8)
        border_col = PINK_ACCENT if self._mode == "select" else PINK_ACCENT
        pygame.draw.rect(panel, (*border_col, 200 if self._mode == "select" else 180),
                         (0, 0, pr.w, pr.h), width=2, border_radius=8)

        # ── En-tête ────────────────────────────────────────────────────────────
        if self._mode == "select":
            title_text = "── COMBINER ──"
            title_col  = GOLD
        else:
            title_text = "── PREUVES ──"
            title_col  = PINK_ACCENT
        title = fn.render(title_text, True, title_col)
        panel.blit(title, ((pr.w - title.get_width()) // 2, 10))

        # Compteur
        count_s = fs.render(f"{len(self.items)} indice{'s' if len(self.items) > 1 else ''}",
                             True, TEXT_GRAY)
        panel.blit(count_s, ((pr.w - count_s.get_width()) // 2, 32))
        screen.blit(panel, (pr.x, pr.y))

        # ── Lignes de preuves ──────────────────────────────────────────────────
        for i, (name, desc) in enumerate(self.items):
            self._draw_row(screen, i, name, desc, pr, t)

        # ── Bouton [C] combiner (mode browse) ─────────────────────────────────
        if self._mode == "browse" and len(self.items) >= 2:
            btn = self._combine_btn_rect()
            bs = pygame.Surface((btn.w, btn.h), pygame.SRCALPHA)
            pygame.draw.rect(bs, (*GOLD, 30), (0, 0, btn.w, btn.h), border_radius=5)
            pygame.draw.rect(bs, (*GOLD, 160), (0, 0, btn.w, btn.h), width=1, border_radius=5)
            lbl = fs.render("[C] Combiner deux indices", True, GOLD)
            bs.blit(lbl, ((btn.w - lbl.get_width()) // 2, (btn.h - lbl.get_height()) // 2))
            screen.blit(bs, (btn.x, btn.y))

        # ── Barre d'action (mode select) ──────────────────────────────────────
        if self._mode == "select":
            self._draw_select_bar(screen, pr, t)

        # ── Animation de fusion ────────────────────────────────────────────────
        if self._combining:
            self._draw_combine_anim(screen, pr, t)

        # ── Popup de résultat ──────────────────────────────────────────────────
        if self._result_t > 0 and self._result_msg:
            self._draw_deduction_popup(screen, t)

        # ── Message d'échec ────────────────────────────────────────────────────
        if self._fail_t > 0:
            self._draw_fail_toast(screen)

    # ── Rendu d'une ligne ─────────────────────────────────────────────────────

    def _draw_row(self, screen, i, name, desc, pr, t):
        fn = self.assets.font_med
        fs = self.assets.font_small

        rr = self._row_rect(i, pr)
        is_hover = i == self.selected
        is_sel_a = i == self._sel_a
        is_sel_b = i == self._sel_b
        is_tagged = is_sel_a or is_sel_b

        row = pygame.Surface((rr.w, rr.h), pygame.SRCALPHA)

        # Couleur de fond selon état
        if is_sel_a:
            flash = self._flash_a / _FLASH_DUR
            bg_alpha = int(40 + flash * 60)
            border_col = CYAN
            border_a   = int(200 + flash * 55)
        elif is_sel_b:
            flash = self._flash_b / _FLASH_DUR
            bg_alpha = int(40 + flash * 60)
            border_col = GOLD
            border_a   = int(200 + flash * 55)
        elif is_hover and self._mode == "select":
            bg_alpha   = 25
            border_col = PINK_ACCENT
            border_a   = 120
        elif is_hover:
            bg_alpha   = 35
            border_col = PINK_ACCENT
            border_a   = 160
        else:
            bg_alpha   = 0
            border_col = (20, 25, 45)
            border_a   = 200

        pygame.draw.rect(row, (20, 25, 45, bg_alpha + 180), (0, 0, rr.w, rr.h), border_radius=4)
        pygame.draw.rect(row, (*border_col, border_a), (0, 0, rr.w, rr.h), width=1 + is_tagged, border_radius=4)

        # Icône de sélection
        if is_sel_a:
            ico = fn.render("①", True, CYAN)
        elif is_sel_b:
            ico = fn.render("②", True, GOLD)
        elif self._mode == "select" and is_hover:
            ico = fs.render("◈", True, PINK_ACCENT)
        else:
            ico = fn.render("◆", True, PINK_ACCENT if is_hover else GOLD)

        row.blit(ico, (8, (rr.h - ico.get_height()) // 2))

        name_col = (CYAN if is_sel_a else GOLD if is_sel_b else
                    PINK_ACCENT if is_hover else GOLD)
        ns = fn.render(name[:22], True, name_col)
        ds = fs.render(desc[:34], True, TEXT_GRAY)
        row.blit(ns, (32, 8))
        row.blit(ds, (32, 32))

        screen.blit(row, (rr.x, rr.y))

    # ── Barre d'action (mode select) ──────────────────────────────────────────

    def _draw_select_bar(self, screen, pr, t):
        fs  = self.assets.font_small
        fn  = self.assets.font_med
        bar_y = pr.y + pr.h - 52
        bar_w = pr.w - 16

        bar = pygame.Surface((bar_w, 48), pygame.SRCALPHA)
        pygame.draw.rect(bar, (*DARK_BG, 220), (0, 0, bar_w, 48), border_radius=6)
        pygame.draw.rect(bar, (*GOLD, 100), (0, 0, bar_w, 48), width=1, border_radius=6)

        if self._sel_a is None and self._sel_b is None:
            hint = fs.render("Sélectionnez 2 indices [Entrée]", True, TEXT_GRAY)
            bar.blit(hint, ((bar_w - hint.get_width()) // 2, 16))
        elif self._sel_b is None:
            a_name = self.items[self._sel_a][0][:18]
            t1 = fs.render(f"① {a_name}", True, CYAN)
            t2 = fs.render("+ sélectionnez le 2ᵉ…", True, TEXT_GRAY)
            bar.blit(t1, (8, 6))
            bar.blit(t2, (8, 28))
        else:
            a_name = self.items[self._sel_a][0][:14]
            b_name = self.items[self._sel_b][0][:14]
            combo  = fs.render(f"① {a_name}  +  ② {b_name}", True, GOLD)
            bar.blit(combo, ((bar_w - combo.get_width()) // 2, 4))

            # Bouton Combiner
            blink = int(t * 3) % 2 == 0
            go_col = (*CYAN, 220) if blink else (*CYAN, 140)
            pygame.draw.rect(bar, (*DARK_BG, 200), (4, 26, bar_w - 8, 18), border_radius=4)
            pygame.draw.rect(bar, go_col, (4, 26, bar_w - 8, 18), width=1, border_radius=4)
            go_lbl = fs.render("[Espace] Lancer la déduction !", True, CYAN if blink else CYAN_DIM)
            bar.blit(go_lbl, ((bar_w - go_lbl.get_width()) // 2, 28))

        screen.blit(bar, (pr.x + 8, bar_y))

    # ── Animation de fusion ────────────────────────────────────────────────────

    def _draw_combine_anim(self, screen, pr, t):
        """Animation de fusion : deux orbes qui se rejoignent au centre."""
        progress = 1.0 - (self._combine_t / _COMBINE_DUR)
        ease = progress * progress * (3.0 - 2.0 * progress)

        if self._sel_a is None or self._sel_b is None:
            return

        ra = self._row_rect(self._sel_a, pr)
        rb = self._row_rect(self._sel_b, pr)
        ax, ay = ra.centerx, ra.centery
        bx, by = rb.centerx, rb.centery
        cx = (SCREEN_W) // 2
        cy = SCREEN_H // 2

        # Orbe A (cyan) qui se déplace vers le centre
        ox_a = int(ax + (cx - ax) * ease)
        oy_a = int(ay + (cy - ay) * ease)
        r_a  = int(18 + 10 * math.sin(progress * math.pi))
        alpha_a = int(220 * (1.0 - ease * 0.3))

        orb_a = pygame.Surface((r_a * 2 + 4, r_a * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(orb_a, (*CYAN, alpha_a), (r_a + 2, r_a + 2), r_a)
        pygame.draw.circle(orb_a, (255, 255, 255, alpha_a // 2), (r_a + 2, r_a + 2), r_a // 2)
        screen.blit(orb_a, (ox_a - r_a - 2, oy_a - r_a - 2))

        # Orbe B (gold) qui se déplace vers le centre
        ox_b = int(bx + (cx - bx) * ease)
        oy_b = int(by + (cy - by) * ease)
        r_b  = int(18 + 10 * math.sin(progress * math.pi))
        alpha_b = int(220 * (1.0 - ease * 0.3))

        orb_b = pygame.Surface((r_b * 2 + 4, r_b * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(orb_b, (*GOLD, alpha_b), (r_b + 2, r_b + 2), r_b)
        pygame.draw.circle(orb_b, (255, 255, 255, alpha_b // 2), (r_b + 2, r_b + 2), r_b // 2)
        screen.blit(orb_b, (ox_b - r_b - 2, oy_b - r_b - 2))

        # Flash au centre lors de la fusion
        if progress > 0.75:
            flash_prog = (progress - 0.75) / 0.25
            flash_alpha = int(flash_prog * 180)
            flash_r = int(flash_prog * 60)
            if flash_r > 0:
                flash_surf = pygame.Surface((flash_r * 2, flash_r * 2), pygame.SRCALPHA)
                pygame.draw.circle(flash_surf, (220, 230, 245, flash_alpha),
                                   (flash_r, flash_r), flash_r)
                screen.blit(flash_surf, (cx - flash_r, cy - flash_r))

        # Voile sombre pendant l'animation
        veil = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        veil.fill((0, 0, 0, int(ease * 100)))
        screen.blit(veil, (0, 0))

    # ── Popup de déduction ────────────────────────────────────────────────────

    def _draw_deduction_popup(self, screen: pygame.Surface, t: float):
        """Popup central affichant la déduction débloquée."""
        if not self._result_msg:
            return

        # Alpha global
        fade_in  = min(1.0, (_RESULT_DUR - self._result_t) / 0.4)
        fade_out = min(1.0, self._result_t / 0.5)
        alpha = int(min(fade_in, fade_out) * 255)
        if alpha <= 0:
            return

        fn  = self.assets.font_med
        fs  = self.assets.font_small
        fb  = self.assets.font_big

        PW, PH = 560, 220
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2

        # Voile de fond
        veil = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        veil.fill((0, 0, 0, int(alpha * 0.55)))
        screen.blit(veil, (0, 0))

        # Fenêtre
        popup = pygame.Surface((PW, PH), pygame.SRCALPHA)
        pygame.draw.rect(popup, (*DARK_BG, min(255, alpha)), (0, 0, PW, PH), border_radius=10)
        pygame.draw.rect(popup, (*GOLD, min(230, alpha)), (0, 0, PW, PH), width=2, border_radius=10)

        # Titre
        head = fb.render("✦ DÉDUCTION ✦", True, GOLD)
        popup.blit(head, ((PW - head.get_width()) // 2, 12))
        pygame.draw.line(popup, (*GOLD, 80), (20, 44), (PW - 20, 44), 1)

        # Nom de la déduction
        dtitle = fn.render(self._result_msg.get("title", ""), True, CYAN)
        popup.blit(dtitle, ((PW - dtitle.get_width()) // 2, 52))

        # Texte — retour à la ligne manuel
        raw_text = self._result_msg.get("text", "")
        words = raw_text.split()
        lines, cur = [], ""
        max_w = PW - 40
        for w in words:
            test = (cur + " " + w).strip()
            if fs.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)

        for li, line in enumerate(lines[:4]):
            ls = fs.render(line, True, TEXT_MAIN)
            popup.blit(ls, ((PW - ls.get_width()) // 2, 80 + li * 22))

        # Sources
        if "from" in self._result_msg:
            fa, fb2 = self._result_msg["from"]
            src = fs.render(f"[ {fa}  ×  {fb2} ]", True, TEXT_GRAY)
            popup.blit(src, ((PW - src.get_width()) // 2, PH - 30))

        popup.set_alpha(alpha)
        screen.blit(popup, (px, py))

    # ── Toast d'échec ─────────────────────────────────────────────────────────

    def _draw_fail_toast(self, screen: pygame.Surface):
        fs = self.assets.font_small
        alpha = min(255, int(self._fail_t * 180))
        txt = fs.render(self._fail_msg, True, RED_ACCENT)
        tw = txt.get_width() + 24
        th = txt.get_height() + 14
        bx = (SCREEN_W - tw) // 2
        by = SCREEN_H // 2 + 120

        badge = pygame.Surface((tw, th), pygame.SRCALPHA)
        pygame.draw.rect(badge, (*DARK_BG, min(220, alpha)), (0, 0, tw, th), border_radius=6)
        pygame.draw.rect(badge, (*RED_ACCENT, min(200, alpha)), (0, 0, tw, th), width=1, border_radius=6)
        badge.set_alpha(alpha)

        txt_s = pygame.Surface(txt.get_size(), pygame.SRCALPHA)
        txt_s.blit(txt, (0, 0))
        txt_s.set_alpha(alpha)

        screen.blit(badge, (bx, by))
        screen.blit(txt_s, (bx + 12, by + 7))


# ══════════════════════════════════════════════════════════════════════════════
# ── DeductionPanel — panneau des déductions débloquées ────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

class DeductionPanel:
    """
    Panneau latéral gauche listant toutes les déductions débloquées.
    Touche D pour ouvrir/fermer.
    """
    PW = 340
    ROW_H = 72

    def __init__(self, assets: Assets, deduction_engine):
        self.assets    = assets
        self.deduction = deduction_engine
        self.visible   = False
        self.selected  = 0

    def toggle(self):
        self.visible = not self.visible

    def handle_event(self, event) -> bool:
        if not self.visible:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_d):
                self.toggle()
                return True
            if event.key == pygame.K_UP:
                self.selected = max(0, self.selected - 1)
                return True
            if event.key == pygame.K_DOWN:
                items = self.deduction.all_deductions() if self.deduction else []
                self.selected = min(len(items) - 1, self.selected + 1)
                return True
        return False

    def draw(self, screen: pygame.Surface, t: float):
        if not self.visible:
            return

        items = self.deduction.all_deductions() if self.deduction else []
        fn = self.assets.font_med
        fs = self.assets.font_small

        ph = min(SCREEN_H - 80, 60 + len(items) * (self.ROW_H + 6) + 20)
        ph = max(ph, 120)

        panel = pygame.Surface((self.PW, ph), pygame.SRCALPHA)
        pygame.draw.rect(panel, (*DARK_BG, 245), (0, 0, self.PW, ph), border_radius=8)
        pygame.draw.rect(panel, (*GOLD, 200), (0, 0, self.PW, ph), width=2, border_radius=8)

        title = fn.render("── DÉDUCTIONS ──", True, GOLD)
        panel.blit(title, ((self.PW - title.get_width()) // 2, 10))
        count_s = fs.render(f"{len(items)} déduction{'s' if len(items) > 1 else ''}", True, TEXT_GRAY)
        panel.blit(count_s, ((self.PW - count_s.get_width()) // 2, 32))

        if not items:
            msg = fs.render("Combinez des preuves [E → C]", True, TEXT_GRAY)
            panel.blit(msg, ((self.PW - msg.get_width()) // 2, ph // 2))
        else:
            for i, d in enumerate(items):
                y   = 54 + i * (self.ROW_H + 6)
                sel = i == self.selected
                row = pygame.Surface((self.PW - 16, self.ROW_H), pygame.SRCALPHA)
                bg_col = (*GOLD, 30) if sel else (10, 15, 35, 200)
                bd_col = (*GOLD, 160) if sel else (*GOLD, 60)
                pygame.draw.rect(row, bg_col, (0, 0, self.PW - 16, self.ROW_H), border_radius=5)
                pygame.draw.rect(row, bd_col, (0, 0, self.PW - 16, self.ROW_H), width=1, border_radius=5)

                # Titre de la déduction
                dt = fn.render(d.get("title", "?")[:26], True, GOLD if sel else TEXT_MAIN)
                row.blit(dt, (10, 6))

                # Insight
                ins = fs.render(d.get("insight", "")[:36], True, CYAN if sel else TEXT_GRAY)
                row.blit(ins, (10, 30))

                # Sources
                fr = d.get("from", ())
                if fr:
                    src_txt = f"{fr[0][:16]} × {fr[1][:16]}"
                    src_s = fs.render(src_txt, True, TEXT_GRAY)
                    row.blit(src_s, (10, 52))

                panel.blit(row, (8, y))

        screen.blit(panel, (10, 60))


# ── Panneau Preuves (version legacy simple — non utilisée mais gardée) ─────────
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

        f  = self.assets.font_med
        fs = self.assets.font_small

        title = f.render("── INVENTAIRE ──", True, CYAN)
        panel.blit(title, ((260 - title.get_width()) // 2, 10))

        for i, (name, desc) in enumerate(self.ITEMS):
            y   = 50 + i * 55
            row = pygame.Surface((240, 46), pygame.SRCALPHA)
            pygame.draw.rect(row, (20, 30, 50, 200), (0, 0, 240, 46), border_radius=4)
            pygame.draw.rect(row, (*CYAN_DIM, 100), (0, 0, 240, 46), width=1, border_radius=4)
            ns = f.render(f"▸ {name}", True, GOLD)
            ds = fs.render(desc, True, TEXT_GRAY)
            row.blit(ns, (8, 4))
            row.blit(ds, (8, 24))
            panel.blit(row, (10, y))

        screen.blit(panel, (px, py))


# ── Écran titre ─────────────────────────────────────────────────────────────────
class TitleScreen:
    def __init__(self, assets: Assets):
        self.assets = assets
        self.alpha = 0
        self.phase = "fade_in"
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
        screen.fill(DARK_BG)
        for i in range(60):
            r = (i * 137 + 17) % SCREEN_W
            s = (i * 97  + 31) % (SCREEN_H // 2)
            a = int(120 + 100 * math.sin(self.star_t * 0.5 + i))
            pygame.draw.circle(screen, (a, a, min(255, a + 60)), (r, s), 1)

        for y in range(0, SCREEN_H, 4):
            a = 30 + 10 * math.sin(y * 0.05 + self.t)
            pygame.draw.line(screen, (0, int(a), int(a*1.5)), (0, y), (SCREEN_W, y))

        title_s = self.assets.font_title.render(TITLE, True, CYAN)
        sub_s   = self.assets.font_med.render("UN THRILLER EN PIXEL ART", True, TEXT_GRAY)
        press_s = self.assets.font_small.render("APPUYEZ SUR UNE TOUCHE POUR COMMENCER", True, CYAN_DIM)

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

        if self.alpha < 255:
            ov = pygame.Surface((SCREEN_W, SCREEN_H))
            ov.fill(BLACK)
            ov.set_alpha(255 - self.alpha)
            screen.blit(ov, (0, 0))


# ── Écran de sélection des slots de sauvegarde ────────────────────────────────
class SaveSlotScreen:
    W = 620
    H = 380
    SLOT_H = 80
    SLOT_GAP = 14

    def __init__(self, assets, save_manager, mode: str = "save"):
        self.assets      = assets
        self.sm          = save_manager
        self.mode        = mode
        self.visible     = False
        self.selected    = 0
        self._slots_data = [None, None, None]
        self._confirm_slot = None
        self._result     = None

    def open(self, mode=None):
        if mode:
            self.mode = mode
        self._slots_data   = self.sm.all_slots()
        self.selected      = 0
        self._confirm_slot = None
        self._result       = None
        self.visible       = True

    def close(self):
        self.visible       = False
        self._confirm_slot = None

    def pop_result(self):
        r = self._result
        self._result = None
        return r

    def handle_event(self, event):
        if not self.visible:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._result = -1; self.close()
            elif event.key in (pygame.K_UP, pygame.K_LEFT):
                self.selected = (self.selected - 1) % 3
                self._confirm_slot = None
            elif event.key in (pygame.K_DOWN, pygame.K_RIGHT):
                self.selected = (self.selected + 1) % 3
                self._confirm_slot = None
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self._activate(self.selected)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            ox, oy = self._origin()
            if not pygame.Rect(ox, oy, self.W, self.H).collidepoint(mx, my):
                self._result = -1; self.close(); return
            for i in range(3):
                if self._slot_rect(i, ox, oy).collidepoint(mx, my):
                    if self.selected == i:
                        self._activate(i)
                    else:
                        self.selected = i; self._confirm_slot = None
                    return
            cancel_r = pygame.Rect(ox + self.W - 130, oy + self.H - 44, 110, 30)
            if cancel_r.collidepoint(mx, my):
                self._result = -1; self.close()
        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            ox, oy = self._origin()
            for i in range(3):
                if self._slot_rect(i, ox, oy).collidepoint(mx, my):
                    if self.selected != i:
                        self.selected = i; self._confirm_slot = None
                    break

    def _activate(self, slot):
        if self.mode == "save" and self._slots_data[slot] is not None:
            if self._confirm_slot == slot:
                self._result = slot; self.close()
            else:
                self._confirm_slot = slot
        else:
            if self.mode == "load" and self._slots_data[slot] is None:
                return
            self._result = slot; self.close()

    def _origin(self):
        return (SCREEN_W - self.W) // 2, (SCREEN_H - self.H) // 2

    def _slot_rect(self, i, ox, oy):
        y = oy + 64 + i * (self.SLOT_H + self.SLOT_GAP)
        return pygame.Rect(ox + 20, y, self.W - 40, self.SLOT_H)

    def draw(self, screen, t):
        if not self.visible:
            return
        ox, oy = self._origin()
        fn = self.assets.font_med
        fs = self.assets.font_small
        fb = self.assets.font_big

        veil = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 160))
        screen.blit(veil, (0, 0))

        win = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        pygame.draw.rect(win, (*DARK_BG, 250), (0, 0, self.W, self.H), border_radius=8)
        pygame.draw.rect(win, (*CYAN, 200),    (0, 0, self.W, self.H), width=2, border_radius=8)
        label = "SAUVEGARDER" if self.mode == "save" else "CHARGER"
        title = fb.render(f"── {label} ──", True, CYAN)
        win.blit(title, ((self.W - title.get_width()) // 2, 14))
        pygame.draw.line(win, (*CYAN, 60), (20, 44), (self.W - 20, 44), 1)
        screen.blit(win, (ox, oy))

        for i in range(3):
            data = self._slots_data[i]
            sel  = i == self.selected
            conf = i == self._confirm_slot
            r    = self._slot_rect(i, ox, oy)
            ss   = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
            bg_col     = (*CYAN, 35)       if sel else (10, 15, 35, 200)
            border_col = (*CYAN, 220)      if sel else (*CYAN_DIM, 90)
            pygame.draw.rect(ss, bg_col,     (0, 0, r.w, r.h), border_radius=6)
            pygame.draw.rect(ss, border_col, (0, 0, r.w, r.h), width=2 if sel else 1, border_radius=6)
            num_s = fb.render(f"SLOT {i + 1}", True, CYAN if sel else CYAN_DIM)
            ss.blit(num_s, (14, (r.h - num_s.get_height()) // 2))
            if data is None:
                empty_s = fn.render("— vide —", True, TEXT_GRAY)
                ss.blit(empty_s, (130, (r.h - empty_s.get_height()) // 2))
            else:
                scene_s = fn.render(data.get("scene_name", "…")[:38], True, TEXT_MAIN if sel else TEXT_GRAY)
                date_s  = fs.render(data.get("saved_at", ""), True, TEXT_GRAY)
                ev_n    = len(data.get("evidence", []))
                ded_n   = len(data.get("deductions", []))
                ev_s    = fs.render(f"{ev_n} preuve{'s' if ev_n>1 else ''}  •  {ded_n} déduction{'s' if ded_n>1 else ''}", True, GOLD)
                ss.blit(scene_s, (130, 12))
                ss.blit(date_s,  (130, 36))
                ss.blit(ev_s,    (130, 56))
            if conf:
                warn = fs.render("⚠  Écraser ? Appuyez encore pour confirmer", True, PINK_ACCENT)
                ss.blit(warn, (r.w - warn.get_width() - 10, r.h - warn.get_height() - 8))
            screen.blit(ss, (r.x, r.y))

        cancel_r = pygame.Rect(ox + self.W - 130, oy + self.H - 44, 110, 30)
        cb = pygame.Surface((110, 30), pygame.SRCALPHA)
        pygame.draw.rect(cb, (10, 15, 35, 200), (0, 0, 110, 30), border_radius=5)
        pygame.draw.rect(cb, (*CYAN_DIM, 150),  (0, 0, 110, 30), width=1, border_radius=5)
        cs = fs.render("[Échap] Annuler", True, TEXT_GRAY)
        cb.blit(cs, ((110 - cs.get_width()) // 2, (30 - cs.get_height()) // 2))
        screen.blit(cb, (cancel_r.x, cancel_r.y))

        hint_text = ("[↑↓] Naviguer   [Entrée] Confirmer" if self.mode == "load"
                     else "[↑↓] Naviguer   [Entrée] Sauvegarder")
        hint = fs.render(hint_text, True, TEXT_GRAY)
        screen.blit(hint, (ox + 20, oy + self.H - 38))