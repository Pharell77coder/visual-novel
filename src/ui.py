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

        # Indices figés au démarrage de l'animation (évite le crash après _reset_selection)
        self._anim_sel_a: int | None = None
        self._anim_sel_b: int | None = None

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
        # Mémoriser les indices AVANT tout reset pour l'animation
        self._anim_sel_a = self._sel_a
        self._anim_sel_b = self._sel_b
        self._combining  = True
        self._combine_t  = _COMBINE_DUR

    def _finish_combine(self):
        """Appelé quand l'animation de fusion se termine."""
        self._combining = False
        if self.deduction is None or self._anim_sel_a is None or self._anim_sel_b is None:
            self._show_fail("Aucune déduction disponible.")
            self._anim_sel_a = None
            self._anim_sel_b = None
            self._reset_selection()
            return

        name_a = self.items[self._anim_sel_a][0]
        name_b = self.items[self._anim_sel_b][0]
        result = self.deduction.try_combine(name_a, name_b)

        if result:
            self._result_msg = result
            self._result_t   = _RESULT_DUR
        else:
            self._show_fail("Ces deux indices ne mènent à rien de nouveau…")

        self._anim_sel_a = None
        self._anim_sel_b = None
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

        pygame.draw.rect(row, (20, 25, 45, min(255, bg_alpha + 180)), (0, 0, rr.w, rr.h), border_radius=4)
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
    # Boutons du menu principal
    MENU_ITEMS = [
        ("play",    "▶  NOUVELLE PARTIE"),
        ("load",    "⟳  CHARGER"),
        ("gallery", "◈  GALERIE CG"),
        ("quit",    "✕  QUITTER"),
    ]
    BTN_W = 280
    BTN_H = 38
    BTN_GAP = 10

    def __init__(self, assets: Assets):
        self.assets   = assets
        self.alpha    = 0
        self.phase    = "fade_in"   # "fade_in" → "hold"
        self.t        = 0.0
        self.particles = []
        self.star_t   = 0.0
        self._sel     = 0           # bouton sélectionné (index)
        self._hovered = 0           # bouton survolé à la souris

    # ── Géométrie des boutons ──────────────────────────────────────────────────

    def _btn_rect(self, i: int) -> pygame.Rect:
        total_h = len(self.MENU_ITEMS) * (self.BTN_H + self.BTN_GAP) - self.BTN_GAP
        start_y = SCREEN_H // 2 + 55
        x = (SCREEN_W - self.BTN_W) // 2
        y = start_y + i * (self.BTN_H + self.BTN_GAP)
        return pygame.Rect(x, y, self.BTN_W, self.BTN_H)

    # ── Mise à jour ────────────────────────────────────────────────────────────

    def update(self, dt):
        self.t      += dt
        self.star_t += dt
        if self.phase == "fade_in":
            self.alpha = min(255, self.alpha + 4)
            if self.alpha >= 255:
                self.phase = "hold"
        # Particules ambiantes
        if random.random() < 0.25:
            x = random.randint(50, SCREEN_W - 50)
            y = random.randint(SCREEN_H // 2 - 20, SCREEN_H // 2 + 20)
            self.particles.append(Particle(x, y, CYAN))
        self.particles = [p for p in self.particles if p.alive]
        for p in self.particles:
            p.update(dt)

    # ── Gestion des événements ─────────────────────────────────────────────────

    def handle_event(self, e):
        """
        Retourne l'action string si un bouton est activé :
            "play" | "load" | "gallery" | "quit"
        Retourne None sinon.
        """
        if self.phase != "hold":
            return None

        if e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_UP, pygame.K_LEFT):
                self._sel = (self._sel - 1) % len(self.MENU_ITEMS)
                return None
            if e.key in (pygame.K_DOWN, pygame.K_RIGHT, pygame.K_TAB):
                self._sel = (self._sel + 1) % len(self.MENU_ITEMS)
                return None
            if e.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.MENU_ITEMS[self._sel][0]

        elif e.type == pygame.MOUSEMOTION:
            mx, my = e.pos
            for i in range(len(self.MENU_ITEMS)):
                if self._btn_rect(i).collidepoint(mx, my):
                    self._sel = i
                    break

        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mx, my = e.pos
            for i, (action, _) in enumerate(self.MENU_ITEMS):
                if self._btn_rect(i).collidepoint(mx, my):
                    return action

        return None

    # ── Rendu ──────────────────────────────────────────────────────────────────

    def draw(self, screen):
        screen.fill(DARK_BG)

        # Étoiles décoratives
        for i in range(60):
            r = (i * 137 + 17) % SCREEN_W
            s = (i * 97  + 31) % (SCREEN_H // 2)
            a = int(120 + 100 * math.sin(self.star_t * 0.5 + i))
            pygame.draw.circle(screen, (a, a, min(255, a + 60)), (r, s), 1)

        # Lignes de fond CRT
        for y in range(0, SCREEN_H, 4):
            a = 30 + 10 * math.sin(y * 0.05 + self.t)
            pygame.draw.line(screen, (0, int(a), int(a * 1.5)), (0, y), (SCREEN_W, y))

        # Titre
        title_s = self.assets.font_title.render(TITLE, True, CYAN)
        sub_s   = self.assets.font_med.render("UN THRILLER EN PIXEL ART", True, TEXT_GRAY)

        glow_col = (*CYAN, int(30 + 20 * math.sin(self.t * 2)))
        glow = pygame.Surface(title_s.get_size(), pygame.SRCALPHA)
        glow.fill(glow_col)
        tx = (SCREEN_W - title_s.get_width()) // 2
        ty = SCREEN_H // 2 - 80
        screen.blit(glow, (tx - 4, ty - 4))
        screen.blit(title_s, (tx, ty))
        screen.blit(sub_s, ((SCREEN_W - sub_s.get_width()) // 2, ty + title_s.get_height() + 6))

        # Séparateur
        sep_y = ty + title_s.get_height() + 34
        pygame.draw.line(screen, (*CYAN_DIM, 120),
                         ((SCREEN_W - self.BTN_W) // 2, sep_y),
                         ((SCREEN_W + self.BTN_W) // 2, sep_y), 1)

        # Boutons du menu
        if self.phase == "hold":
            fn = self.assets.font_med
            for i, (action, label) in enumerate(self.MENU_ITEMS):
                r = self._btn_rect(i)
                sel = (i == self._sel)

                btn = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
                if sel:
                    pulse = 0.55 + 0.45 * math.sin(self.t * 3.5)
                    bg_a  = int(50 + 30 * pulse)
                    bd_a  = int(180 + 60 * pulse)
                    pygame.draw.rect(btn, (*CYAN, bg_a), (0, 0, r.w, r.h), border_radius=5)
                    pygame.draw.rect(btn, (*CYAN, bd_a), (0, 0, r.w, r.h), width=2, border_radius=5)
                    # Flèche de sélection
                    arr = fn.render("▸", True, CYAN)
                    btn.blit(arr, (6, (r.h - arr.get_height()) // 2))
                else:
                    pygame.draw.rect(btn, (*DARK_BG, 200), (0, 0, r.w, r.h), border_radius=5)
                    pygame.draw.rect(btn, (*CYAN_DIM, 80), (0, 0, r.w, r.h), width=1, border_radius=5)

                col  = CYAN if sel else TEXT_GRAY
                lbl  = fn.render(label, True, col)
                btn.blit(lbl, ((r.w - lbl.get_width()) // 2, (r.h - lbl.get_height()) // 2))
                screen.blit(btn, (r.x, r.y))

        # Particules
        for p in self.particles:
            p.draw(screen)

        # Fade-in
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


# ══════════════════════════════════════════════════════════════════════════════
# ── CGGallery — Galerie d'illustrations CG ────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

class CGGallery:
    """
    Galerie CG plein écran accessible depuis le menu titre.

    Layout :
        ┌──────────────────────────────────────────────────────────┐
        │  ── GALERIE CG ──          3 / 13                        │
        ├──────────────────────────────────────────────────────────┤
        │  [◀ prev]  [thumbnail]×5  [next ▶]     CHAPITRE I       │
        │                                                          │
        │  ┌───────── IMAGE PLEIN ─────────────────────────────┐   │
        │  │              (vignette sélectionnée)              │   │
        │  └────────────────────────────────────────────────────┘   │
        │                                                          │
        │  Titre CG                       [Entrée] Plein écran    │
        │  [Échap] Retour menu                                     │
        └──────────────────────────────────────────────────────────┘

    Touches :
        ← →         naviguer entre les CG
        Entrée      afficher en plein écran (fullview)
        Échap       quitter le fullview / retourner au menu
    """

    # Dimensions de la grille de vignettes
    THUMB_W    = 140
    THUMB_H    = 90
    THUMB_GAP  = 14
    THUMBS_ROW = 5            # vignettes par ligne
    PREVIEW_H  = 270          # hauteur de l'image preview centrale

    # Couleur des slots verrouillés
    LOCK_BG    = (8, 12, 24)
    LOCK_BORDER = (30, 40, 70)

    def __init__(self, assets, cg_manager):
        self.assets     = assets
        self.cg_mgr     = cg_manager
        self.visible    = False

        # Navigation
        self._cursor    = 0        # index dans CG_CATALOGUE
        self._fullview  = False    # mode plein écran

        # Animation d'entrée / de sélection
        self._enter_t   = 0.0     # alpha fade-in général
        self._slide_t   = 0.0     # slide de la preview lors d'un changement
        self._slide_dir = 0       # -1 gauche, +1 droite

        # Toast de déblocage
        self._toast_msg   = ""
        self._toast_timer = 0.0

        # Cache vignettes (petites surfaces)
        self._thumb_cache: dict[str, pygame.Surface] = {}

        # Import inline pour éviter les imports circulaires
        from cg_catalogue import CG_CATALOGUE
        self._catalogue = CG_CATALOGUE

    # ── Ouverture / fermeture ─────────────────────────────────────────────────

    def open(self):
        self.visible    = True
        self._fullview  = False
        self._enter_t   = 0.0
        self._slide_t   = 0.0

    def close(self):
        self.visible   = False
        self._fullview = False

    # ── Notification de déblocage (appelée depuis VNEngine) ───────────────────

    def notify_unlock(self, cg_id: str):
        """Affiche un toast '✦ Nouvelle illustration débloquée'."""
        from cg_catalogue import CG_INDEX
        entry = CG_INDEX.get(cg_id)
        if entry:
            self._toast_msg   = f"✦ Illustration débloquée : {entry['title']}"
            self._toast_timer = 4.0

    # ── Événements ────────────────────────────────────────────────────────────

    def handle_event(self, event) -> bool:
        """Retourne True si l'événement est consommé."""
        if not self.visible:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self._fullview:
                    self._fullview = False
                else:
                    self.close()
                return True

            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                entry = self._catalogue[self._cursor]
                if self.cg_mgr.is_unlocked(entry["id"]):
                    self._fullview = not self._fullview
                return True

            if event.key == pygame.K_LEFT:
                self._move(-1)
                return True
            if event.key == pygame.K_RIGHT:
                self._move(1)
                return True
            if event.key == pygame.K_UP:
                self._move(-self.THUMBS_ROW)
                return True
            if event.key == pygame.K_DOWN:
                self._move(self.THUMBS_ROW)
                return True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._fullview:
                self._fullview = False
                return True
            mx, my = event.pos
            # Clic sur une vignette
            idx = self._thumb_at(mx, my)
            if idx is not None:
                if idx == self._cursor:
                    entry = self._catalogue[self._cursor]
                    if self.cg_mgr.is_unlocked(entry["id"]):
                        self._fullview = True
                else:
                    self._move(idx - self._cursor)
                return True

        elif event.type == pygame.MOUSEWHEEL:
            self._move(-event.y)
            return True

        return False

    def _move(self, delta: int):
        old = self._cursor
        self._cursor = max(0, min(len(self._catalogue) - 1, self._cursor + delta))
        if self._cursor != old:
            self._slide_dir = 1 if delta > 0 else -1
            self._slide_t   = 0.25   # durée de l'animation slide

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt: float):
        if not self.visible:
            return
        self._enter_t   = min(1.0, self._enter_t + dt * 3.0)
        self._slide_t   = max(0.0, self._slide_t - dt)
        if self._toast_timer > 0:
            self._toast_timer = max(0.0, self._toast_timer - dt)

    # ── Rendu principal ───────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface, t: float):
        if not self.visible:
            return

        alpha_global = int(self._enter_t * 255)

        if self._fullview:
            self._draw_fullview(screen, alpha_global, t)
        else:
            self._draw_gallery(screen, alpha_global, t)

        self._draw_toast(screen)

    # ── Vue galerie (grille + preview) ────────────────────────────────────────

    def _draw_gallery(self, screen: pygame.Surface, alpha: int, t: float):
        fn = self.assets.font_med
        fs = self.assets.font_small
        fb = self.assets.font_big

        # Fond plein noir semi-transparent
        bg = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        bg.fill((0, 0, 0, min(230, alpha)))
        screen.blit(bg, (0, 0))

        # Grille d'étoiles décoratives
        for i in range(40):
            rx = (i * 233 + 17) % SCREEN_W
            ry = (i * 97  + 31) % SCREEN_H
            a  = int(60 + 40 * math.sin(t * 0.7 + i * 0.3))
            col = (a // 4, a // 2, min(255, a + 60))
            pygame.draw.circle(screen, col, (rx, ry), 1)

        # ── En-tête ───────────────────────────────────────────────────────────
        nb_unlocked = self.cg_mgr.count_unlocked()
        nb_total    = self.cg_mgr.total()

        header = fb.render("── GALERIE CG ──", True, CYAN)
        screen.blit(header, ((SCREEN_W - header.get_width()) // 2, 14))

        count_s = fs.render(
            f"{nb_unlocked} / {nb_total} illustrations débloquées",
            True, GOLD if nb_unlocked > 0 else TEXT_GRAY
        )
        screen.blit(count_s, ((SCREEN_W - count_s.get_width()) // 2, 46))
        pygame.draw.line(screen, (*CYAN, 80), (40, 68), (SCREEN_W - 40, 68), 1)

        # ── Grille de vignettes ───────────────────────────────────────────────
        n     = len(self._catalogue)
        row_w = self.THUMBS_ROW * (self.THUMB_W + self.THUMB_GAP) - self.THUMB_GAP
        gx    = (SCREEN_W - row_w) // 2
        gy    = 78

        # Calculer le nombre de rangées et la hauteur totale de la grille
        n_rows = (n + self.THUMBS_ROW - 1) // self.THUMBS_ROW
        grid_h = n_rows * (self.THUMB_H + self.THUMB_GAP)

        for idx, entry in enumerate(self._catalogue):
            col_i = idx % self.THUMBS_ROW
            row_i = idx // self.THUMBS_ROW
            tx = gx + col_i * (self.THUMB_W + self.THUMB_GAP)
            ty = gy + row_i * (self.THUMB_H + self.THUMB_GAP)

            unlocked = self.cg_mgr.is_unlocked(entry["id"])
            selected = idx == self._cursor

            self._draw_thumb(screen, entry, tx, ty, unlocked, selected, t)

        # ── Preview de l'image sélectionnée ───────────────────────────────────
        prev_y = gy + grid_h + 16
        prev_h = SCREEN_H - prev_y - 50
        prev_h = max(prev_h, 80)
        prev_w = min(int(prev_h * 16 / 9), SCREEN_W - 80)
        prev_x = (SCREEN_W - prev_w) // 2

        entry   = self._catalogue[self._cursor]
        unlocked = self.cg_mgr.is_unlocked(entry["id"])

        # Slide animation
        slide_ease = self._ease_out(1.0 - (self._slide_t / 0.25)) if self._slide_t > 0 else 1.0
        slide_off  = int(self._slide_dir * (1.0 - slide_ease) * 40)

        if unlocked:
            surf = self._get_thumb_large(entry["id"], (prev_w, prev_h))
        else:
            surf = self._make_locked_preview(entry, (prev_w, prev_h))

        # Cadre
        frame_rect = pygame.Rect(prev_x - 3, prev_y - 3, prev_w + 6, prev_h + 6)
        
        
        if unlocked:
            border_col = (*CYAN, 160)  # SI CYAN est déballable
        else:
            if hasattr(self, 'LOCK_BORDER'):
                border_col = (*self.LOCK_BORDER, 120)
            else:
                border_col = (30, 40, 70, 120)
        
        
        pygame.draw.rect(screen, border_col, frame_rect, 2, border_radius=4)

        if surf:
            s = surf.copy()
            s.set_alpha(alpha)
            screen.blit(s, (prev_x + slide_off, prev_y))

        # ── Métadonnées de la CG sélectionnée ────────────────────────────────
        label_y = prev_y + prev_h + 8
        if unlocked:
            title_s = fn.render(entry["title"], True, CYAN)
            chap_s  = fs.render(entry["chapter"], True, TEXT_GRAY)
            enter_s = fs.render("[Entrée] Plein écran", True, CYAN_DIM)
            screen.blit(title_s, (prev_x, label_y))
            screen.blit(chap_s,  (prev_x, label_y + 22))
            screen.blit(enter_s, (prev_x + prev_w - enter_s.get_width(), label_y))
        else:
            hint_s = fs.render(f"🔒 {entry['hint']}", True, TEXT_GRAY)
            screen.blit(hint_s, (prev_x, label_y))

        # ── Bas de page ───────────────────────────────────────────────────────
        esc_s = fs.render("[Échap] Retour au menu", True, TEXT_GRAY)
        nav_s = fs.render("[← →] Naviguer", True, TEXT_GRAY)
        screen.blit(esc_s, (20, SCREEN_H - 24))
        screen.blit(nav_s, (SCREEN_W - nav_s.get_width() - 20, SCREEN_H - 24))

    # ── Vue plein écran ───────────────────────────────────────────────────────

    def _draw_fullview(self, screen: pygame.Surface, alpha: int, t: float):
        fs = self.assets.font_small
        fb = self.assets.font_big

        entry = self._catalogue[self._cursor]

        # Fond noir
        screen.fill((0, 0, 0))

        # Image plein écran (letterboxed)
        surf = self.cg_mgr.get_surface(entry["id"])
        if surf:
            img_w, img_h = surf.get_width(), surf.get_height()
            scale = min(SCREEN_W / img_w, SCREEN_H / img_h)
            dw = int(img_w * scale)
            dh = int(img_h * scale)
            scaled = pygame.transform.smoothscale(surf, (dw, dh))
            dx = (SCREEN_W - dw) // 2
            dy = (SCREEN_H - dh) // 2
            screen.blit(scaled, (dx, dy))

        # Bandeau de titre en bas
        band = pygame.Surface((SCREEN_W, 44), pygame.SRCALPHA)
        band.fill((0, 0, 0, 160))
        screen.blit(band, (0, SCREEN_H - 44))

        title_s = fb.render(entry["title"], True, CYAN)
        chap_s  = fs.render(entry["chapter"], True, TEXT_GRAY)
        esc_s   = fs.render("[Échap] Retour galerie", True, CYAN_DIM)

        screen.blit(title_s, (20, SCREEN_H - 38))
        screen.blit(chap_s,  (24 + title_s.get_width(), SCREEN_H - 32))
        screen.blit(esc_s,   (SCREEN_W - esc_s.get_width() - 20, SCREEN_H - 32))

        # Fade-in léger
        if self._enter_t < 1.0:
            ov = pygame.Surface((SCREEN_W, SCREEN_H))
            ov.fill((0, 0, 0))
            ov.set_alpha(int((1.0 - self._enter_t) * 255))
            screen.blit(ov, (0, 0))

    # ── Rendu d'une vignette ──────────────────────────────────────────────────

    def _draw_thumb(
        self,
        screen: pygame.Surface,
        entry: dict,
        x: int, y: int,
        unlocked: bool,
        selected: bool,
        t: float,
    ):
        TW, TH = self.THUMB_W, self.THUMB_H

        cell = pygame.Surface((TW, TH), pygame.SRCALPHA)

        if unlocked:
            thumb = self._get_thumb(entry["id"])
            if thumb:
                cell.blit(thumb, (0, 0))
            else:
                cell.fill((10, 20, 40))

            # Léger assombrissement si non sélectionné
            if not selected:
                dim = pygame.Surface((TW, TH), pygame.SRCALPHA)
                dim.fill((0, 0, 0, 80))
                cell.blit(dim, (0, 0))
        else:
            # Fond verrouillé
            cell.fill((8, 12, 24))

            # Motif de fond hachuré discret
            for i in range(0, TW + TH, 18):
                pygame.draw.line(cell, (15, 22, 40), (max(0, i - TH), min(TH, i)),
                                 (min(TW, i), max(0, i - TW)), 1)

            # Icône cadenas
            cx2, cy2 = TW // 2, TH // 2 - 6
            pygame.draw.circle(cell, (30, 45, 70), (cx2, cy2), 12)
            pygame.draw.circle(cell, (50, 70, 110), (cx2, cy2), 12, 1)
            # Corps du cadenas
            pygame.draw.rect(cell, (30, 45, 70), (cx2 - 8, cy2 + 4, 16, 11), border_radius=2)
            pygame.draw.rect(cell, (50, 70, 110), (cx2 - 8, cy2 + 4, 16, 11), width=1, border_radius=2)
            # Trou de serrure
            pygame.draw.circle(cell, (15, 25, 50), (cx2, cy2 + 9), 3)

            # Index chapître (bas de la vignette)
            fs2 = self.assets.font_small
            ch_s = fs2.render(entry["chapter"][:12], True, (40, 55, 90))
            cell.blit(ch_s, ((TW - ch_s.get_width()) // 2, TH - 16))

        # Cadre de sélection
        if selected:
            pulse = 0.5 + 0.5 * math.sin(t * 4.0)
            border_alpha = int(180 + 60 * pulse)
            pygame.draw.rect(cell, (*CYAN, border_alpha), (0, 0, TW, TH), 2, border_radius=3)
            # Lueur extérieure
            glow = pygame.Surface((TW + 8, TH + 8), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*CYAN, int(40 * pulse)), (0, 0, TW + 8, TH + 8), border_radius=5)
            screen.blit(glow, (x - 4, y - 4))
        else:
            border_col = (*CYAN, 60) if unlocked else (30, 40, 70, 120)
            pygame.draw.rect(cell, border_col, (0, 0, TW, TH), 1, border_radius=3)

        screen.blit(cell, (x, y))

        # Numéro de la CG (en haut à gauche de la vignette, discret)
        fs3 = self.assets.font_small
        idx_s = fs3.render(f"#{self._catalogue.index(entry)+1:02d}", True,
                           (*CYAN, 180) if unlocked else (30, 40, 70))
        screen.blit(idx_s, (x + 4, y + 3))

    # ── Toast de déblocage ────────────────────────────────────────────────────

    def _draw_toast(self, screen: pygame.Surface):
        if self._toast_timer <= 0 or not self._toast_msg:
            return
        fs = self.assets.font_small
        alpha = min(255, int(self._toast_timer * 120))
        txt   = fs.render(self._toast_msg, True, GOLD)
        tw = txt.get_width() + 28
        th = txt.get_height() + 14
        bx = (SCREEN_W - tw) // 2
        by = SCREEN_H - 70

        badge = pygame.Surface((tw, th), pygame.SRCALPHA)
        pygame.draw.rect(badge, (*DARK_BG, min(230, alpha)), (0, 0, tw, th), border_radius=6)
        pygame.draw.rect(badge, (*GOLD, min(220, alpha)),    (0, 0, tw, th), width=1, border_radius=6)
        badge.set_alpha(alpha)

        ts = pygame.Surface(txt.get_size(), pygame.SRCALPHA)
        ts.blit(txt, (0, 0))
        ts.set_alpha(alpha)

        screen.blit(badge, (bx, by))
        screen.blit(ts,    (bx + 14, by + 7))

    # ── Helpers de cache ──────────────────────────────────────────────────────

    def _get_thumb(self, cg_id: str) -> pygame.Surface | None:
        """Retourne une vignette mise en cache (THUMB_W × THUMB_H)."""
        if cg_id not in self._thumb_cache:
            surf = self.cg_mgr.get_surface(cg_id, (self.THUMB_W, self.THUMB_H))
            self._thumb_cache[cg_id] = surf
        return self._thumb_cache.get(cg_id)

    def _get_thumb_large(
        self, cg_id: str, size: tuple[int, int]
    ) -> pygame.Surface | None:
        """Preview de taille arbitraire (non mis en cache pour éviter VRAM)."""
        return self.cg_mgr.get_surface(cg_id, size)

    def _make_locked_preview(
        self, entry: dict, size: tuple[int, int]
    ) -> pygame.Surface:
        """Preview verrouillée : fond sombre + indice texte."""
        w, h = size
        surf = pygame.Surface((w, h))
        # Dégradé
        for y in range(h):
            ratio = y / h
            r = int(6  + 8  * ratio)
            g = int(8  + 10 * ratio)
            b = int(18 + 22 * ratio)
            pygame.draw.line(surf, (r, g, b), (0, y), (w, y))

        # Motif hachuré
        for i in range(0, w + h, 30):
            pygame.draw.line(surf, (12, 18, 35),
                             (max(0, i - h), min(h, i)),
                             (min(w, i), max(0, i - w)), 1)

        # Grand cadenas central
        cx2, cy2 = w // 2, h // 2
        r2 = min(36, h // 5)
        pygame.draw.circle(surf, (20, 30, 55), (cx2, cy2 - r2 // 2), r2)
        pygame.draw.circle(surf, (40, 60, 100), (cx2, cy2 - r2 // 2), r2, 2)
        body_h = r2 + 10
        pygame.draw.rect(surf, (20, 30, 55),
                         (cx2 - r2, cy2 - r2 // 2 + r2 - 4, r2 * 2, body_h),
                         border_radius=4)
        pygame.draw.rect(surf, (40, 60, 100),
                         (cx2 - r2, cy2 - r2 // 2 + r2 - 4, r2 * 2, body_h),
                         width=2, border_radius=4)

        fn2 = self.assets.font_med
        fs2 = self.assets.font_small
        hint_s = fs2.render(entry["hint"], True, (80, 100, 140))
        surf.blit(hint_s, (w // 2 - hint_s.get_width() // 2,
                           cy2 + r2 + body_h // 2 + 10))

        return surf

    def _thumb_at(self, mx: int, my: int) -> int | None:
        """Retourne l'index de la vignette sous le curseur souris, ou None."""
        n     = len(self._catalogue)
        row_w = self.THUMBS_ROW * (self.THUMB_W + self.THUMB_GAP) - self.THUMB_GAP
        gx    = (SCREEN_W - row_w) // 2
        gy    = 78

        for idx in range(n):
            col_i = idx % self.THUMBS_ROW
            row_i = idx // self.THUMBS_ROW
            tx = gx + col_i * (self.THUMB_W + self.THUMB_GAP)
            ty = gy + row_i * (self.THUMB_H + self.THUMB_GAP)
            if pygame.Rect(tx, ty, self.THUMB_W, self.THUMB_H).collidepoint(mx, my):
                return idx
        return None

    @staticmethod
    def _ease_out(t: float) -> float:
        return 1.0 - (1.0 - t) ** 2

# ══════════════════════════════════════════════════════════════════════════════
# ── NarrativeMap — Carte narrative de fin de chapitre ─────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

class NarrativeMap:
    """
    Écran "carte narrative" affiché en fin de chapitre.

    Affiche un arbre de décision avec :
      - les branches choisies  (surlignées en cyan)
      - les branches ratées    (grisées, avec leur label)
      - un résumé des preuves & déductions collectées

    API :
        nm = NarrativeMap(assets)
        nm.show(chapter=1, choices_taken=["interrogation","team"],
                evidence=engine.evidence.items, deductions=engine.ded_engine.all_deductions())
        nm.handle_event(event)  →  "continue" | None
        nm.draw(screen, t)
        nm.update(dt)
    """

    # Définition statique de l'arbre pour chaque chapitre
    # Format par nœud : {"id": str, "label": str, "children": [...], "type": "choice"|"leaf"|"merge"}
    CHAPTER_TREES = {
        1: {
            "id": "root_ch1",
            "label": "Scène de crime\n2h37 du matin",
            "type": "root",
            "children": [
                {
                    "id": "interrogation",
                    "label": "Interroger\nles témoins",
                    "type": "choice",
                    "children": []
                },
                {
                    "id": "scene",
                    "label": "Examiner\nla scène",
                    "type": "choice",
                    "children": []
                },
            ],
        },
        2: {
            "id": "root_ch2",
            "label": "Chapitre II\nLa Taupe",
            "type": "root",
            "children": [
                {
                    "id": "ch2_trust",
                    "label": "Faire confiance\nà Natasha",
                    "type": "choice",
                    "children": [
                        {"id": "ch2_infiltrate", "label": "Infiltrer\nle Loft 7", "type": "choice", "children": [
                            {"id": "ch2_betray",  "label": "Exposer\nFerrière",          "type": "leaf", "children": []},
                            {"id": "ch2_protect", "label": "Protéger\nSato",             "type": "leaf", "children": []},
                        ]},
                        {"id": "ch2_press",      "label": "Contacter\nla presse",       "type": "choice", "children": [
                            {"id": "ch2_betray",  "label": "Exposer\nFerrière",          "type": "leaf", "children": []},
                            {"id": "ch2_protect", "label": "Protéger\nSato",             "type": "leaf", "children": []},
                        ]},
                    ],
                },
                {
                    "id": "ch2_resist",
                    "label": "Garder\nses distances",
                    "type": "choice",
                    "children": [
                        {"id": "ch2_infiltrate", "label": "Infiltrer\nle Loft 7", "type": "choice", "children": [
                            {"id": "ch2_betray",  "label": "Exposer\nFerrière",          "type": "leaf", "children": []},
                            {"id": "ch2_protect", "label": "Protéger\nSato",             "type": "leaf", "children": []},
                        ]},
                        {"id": "ch2_press",      "label": "Contacter\nla presse",       "type": "choice", "children": [
                            {"id": "ch2_betray",  "label": "Exposer\nFerrière",          "type": "leaf", "children": []},
                            {"id": "ch2_protect", "label": "Protéger\nSato",             "type": "leaf", "children": []},
                        ]},
                    ],
                },
            ],
        },
        3: {
            "id": "root_ch3",
            "label": "Chapitre III\nL'Architecte",
            "type": "root",
            "children": [
                {
                    "id": "ch3_confront",
                    "label": "Affronter\ndirectement",
                    "type": "choice",
                    "children": [
                        {"id": "ch3_expose",    "label": "Exposer\nmaintenant",  "type": "choice", "children": [
                            {"id": "ch3_sacrifice", "label": "Se sacrifier",     "type": "leaf", "children": []},
                            {"id": "ch3_escape",    "label": "Fuir avec\nles preuves", "type": "leaf", "children": []},
                        ]},
                        {"id": "ch3_negotiate", "label": "Négocier",             "type": "choice", "children": [
                            {"id": "ch3_sacrifice", "label": "Se sacrifier",     "type": "leaf", "children": []},
                            {"id": "ch3_escape",    "label": "Fuir avec\nles preuves", "type": "leaf", "children": []},
                        ]},
                    ],
                },
                {
                    "id": "ch3_shadow",
                    "label": "Observer\ndans l'ombre",
                    "type": "choice",
                    "children": [
                        {"id": "ch3_expose",    "label": "Exposer\nmaintenant",  "type": "choice", "children": [
                            {"id": "ch3_sacrifice", "label": "Se sacrifier",     "type": "leaf", "children": []},
                            {"id": "ch3_escape",    "label": "Fuir avec\nles preuves", "type": "leaf", "children": []},
                        ]},
                        {"id": "ch3_negotiate", "label": "Négocier",             "type": "choice", "children": [
                            {"id": "ch3_sacrifice", "label": "Se sacrifier",     "type": "leaf", "children": []},
                            {"id": "ch3_escape",    "label": "Fuir avec\nles preuves", "type": "leaf", "children": []},
                        ]},
                    ],
                },
            ],
        },
    }

    # ─── Style des nœuds ───────────────────────────────────────────────────────
    NODE_W      = 110
    NODE_H      = 52
    H_GAP       = 70    # espace horizontal entre colonnes
    V_GAP       = 18    # espace vertical entre nœuds frères

    def __init__(self, assets: Assets):
        self.assets        = assets
        self.visible       = False
        self._chapter      = 1
        self._choices_taken: set[str] = set()
        self._evidence     = []
        self._deductions   = []
        self._enter_t      = 0.0
        self._node_anims: dict[str, float] = {}   # id → timer d'apparition
        self._t            = 0.0
        # Layout calculé : {id: (cx, cy)}
        self._layout: dict[str, tuple[int, int]] = {}
        self._edges: list[tuple[str, str]] = []   # (parent_id, child_id)

    # ── API publique ───────────────────────────────────────────────────────────

    def show(
        self,
        chapter: int,
        choices_taken: list[str],
        evidence: list,
        deductions: list,
    ):
        self._chapter       = chapter
        self._choices_taken = set(choices_taken)
        self._evidence      = list(evidence)
        self._deductions    = list(deductions)
        self.visible        = True
        self._enter_t       = 0.0
        self._node_anims    = {}
        self._t             = 0.0
        self._compute_layout()

    def close(self):
        self.visible = False

    def handle_event(self, event) -> str | None:
        """Retourne "continue" si l'utilisateur veut passer, None sinon."""
        if not self.visible:
            return None
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                return "continue"
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Clic sur le bouton "Continuer"
            br = self._continue_btn_rect()
            if br.collidepoint(event.pos):
                return "continue"
        return None

    def update(self, dt: float):
        if not self.visible:
            return
        self._t       += dt
        self._enter_t  = min(1.0, self._enter_t + dt * 2.0)
        # Animer les nœuds progressivement
        for nid in list(self._layout.keys()):
            if nid not in self._node_anims:
                # Délai basé sur la position x du nœud (colonnes de gauche d'abord)
                cx = self._layout[nid][0]
                col_index = (cx - 60) // (self.NODE_W + self.H_GAP)
                delay = col_index * 0.18
                if self._t >= delay:
                    self._node_anims[nid] = 0.0
            if nid in self._node_anims and self._node_anims[nid] < 1.0:
                self._node_anims[nid] = min(1.0, self._node_anims[nid] + dt * 3.5)

    def draw(self, screen: pygame.Surface, t: float):
        if not self.visible:
            return

        alpha_global = int(self._enter_t * 255)
        fn  = self.assets.font_med
        fs  = self.assets.font_small
        fb  = self.assets.font_big

        # Fond
        bg = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        bg.fill((4, 6, 16, min(240, alpha_global)))
        screen.blit(bg, (0, 0))

        # Étoiles
        for i in range(35):
            rx = (i * 211 + 53) % SCREEN_W
            ry = (i * 73  + 17) % SCREEN_H
            a  = int(50 + 30 * math.sin(t * 0.6 + i * 0.4))
            pygame.draw.circle(screen, (a // 4, a // 2, min(255, a + 50)), (rx, ry), 1)

        # ── En-tête ────────────────────────────────────────────────────────────
        chapter_labels = {1: "CHAPITRE I — La Nuit sans Témoin",
                          2: "CHAPITRE II — La Taupe",
                          3: "CHAPITRE III — L'Architecte"}
        header = fb.render(f"── CARTE NARRATIVE ──", True, CYAN)
        sub    = fs.render(chapter_labels.get(self._chapter, ""), True, GOLD)
        screen.blit(header, ((SCREEN_W - header.get_width()) // 2, 12))
        screen.blit(sub,    ((SCREEN_W - sub.get_width()) // 2, 44))
        pygame.draw.line(screen, (*CYAN, 80), (40, 66), (SCREEN_W - 40, 66), 1)

        # ── Arbre ──────────────────────────────────────────────────────────────
        self._draw_tree(screen, t, alpha_global)

        # ── Légende ────────────────────────────────────────────────────────────
        leg_y = SCREEN_H - 92
        leg_items = [
            (CYAN,       "Chemin emprunté"),
            (TEXT_GRAY,  "Branche ratée"),
            (GOLD,       "Point de décision"),
        ]
        lx = 30
        for col, label in leg_items:
            dot = pygame.Surface((12, 12), pygame.SRCALPHA)
            pygame.draw.circle(dot, (*col, 200), (6, 6), 5)
            screen.blit(dot, (lx, leg_y + 2))
            ls = fs.render(label, True, col)
            screen.blit(ls, (lx + 16, leg_y))
            lx += ls.get_width() + 36

        # ── Stats ──────────────────────────────────────────────────────────────
        stat_y = SCREEN_H - 70
        pygame.draw.line(screen, (*CYAN, 40), (30, stat_y - 4), (SCREEN_W - 30, stat_y - 4), 1)
        n_ev  = len(self._evidence)
        n_ded = len(self._deductions)
        stat_txt = fs.render(
            f"Preuves collectées : {n_ev}   •   Déductions débloquées : {n_ded}",
            True, TEXT_GRAY
        )
        screen.blit(stat_txt, ((SCREEN_W - stat_txt.get_width()) // 2, stat_y))

        # Liste des preuves (jusqu'à 7, sur une ligne)
        if self._evidence:
            ev_names = "  ◆  ".join(e[0] for e in self._evidence[:7])
            if len(self._evidence) > 7:
                ev_names += f"  …+{len(self._evidence)-7}"
            ev_s = fs.render(ev_names, True, PINK_ACCENT)
            screen.blit(ev_s, ((SCREEN_W - ev_s.get_width()) // 2, stat_y + 20))

        # ── Bouton Continuer ───────────────────────────────────────────────────
        br = self._continue_btn_rect()
        pulse = 0.5 + 0.5 * math.sin(t * 3.0)
        btn = pygame.Surface((br.w, br.h), pygame.SRCALPHA)
        pygame.draw.rect(btn, (*CYAN, int(40 + 30 * pulse)), (0, 0, br.w, br.h), border_radius=6)
        pygame.draw.rect(btn, (*CYAN, int(180 + 60 * pulse)), (0, 0, br.w, br.h), width=2, border_radius=6)
        lbl = fn.render("▶  Continuer", True, CYAN)
        btn.blit(lbl, ((br.w - lbl.get_width()) // 2, (br.h - lbl.get_height()) // 2))
        screen.blit(btn, (br.x, br.y))

        hint = fs.render("[Espace / Entrée]", True, CYAN_DIM)
        screen.blit(hint, (br.x + (br.w - hint.get_width()) // 2, br.y - 18))

    # ── Layout ────────────────────────────────────────────────────────────────

    def _compute_layout(self):
        """Calcule les positions (cx, cy) de chaque nœud."""
        tree = self.CHAPTER_TREES.get(self._chapter)
        if not tree:
            return
        self._layout = {}
        self._edges  = []
        # Zone disponible pour l'arbre
        TREE_TOP    = 76
        TREE_BOTTOM = SCREEN_H - 110
        TREE_LEFT   = 50
        TREE_RIGHT  = SCREEN_W - 50
        tree_h = TREE_BOTTOM - TREE_TOP
        tree_w = TREE_RIGHT - TREE_LEFT

        # BFS pour calculer le nombre de colonnes (profondeur max)
        max_depth = self._tree_depth(tree)
        col_w = tree_w // max(1, max_depth)

        # Récursif : positionner chaque nœud
        self._layout_node(tree, 0, 0.0, 1.0,
                          TREE_TOP, TREE_BOTTOM,
                          TREE_LEFT, col_w, max_depth)

    def _tree_depth(self, node: dict) -> int:
        if not node.get("children"):
            return 1
        return 1 + max(self._tree_depth(c) for c in node["children"])

    def _layout_node(
        self, node: dict, depth: int,
        y_frac_start: float, y_frac_end: float,
        tree_top: int, tree_bottom: int,
        tree_left: int, col_w: int, max_depth: int,
    ):
        nid = node["id"]
        tree_h = tree_bottom - tree_top
        cy = int(tree_top + tree_h * (y_frac_start + y_frac_end) / 2)
        cx = tree_left + depth * col_w + col_w // 2
        self._layout[nid] = (cx, cy)

        children = node.get("children", [])
        if not children:
            return

        # Divise l'espace vertical entre les enfants
        n = len(children)
        span = y_frac_end - y_frac_start
        for i, child in enumerate(children):
            y0 = y_frac_start + i * span / n
            y1 = y_frac_start + (i + 1) * span / n
            self._edges.append((nid, child["id"]))
            self._layout_node(child, depth + 1, y0, y1,
                              tree_top, tree_bottom,
                              tree_left, col_w, max_depth)

    # ── Rendu de l'arbre ───────────────────────────────────────────────────────

    def _draw_tree(self, screen: pygame.Surface, t: float, alpha_global: int):
        fn = self.assets.font_med
        fs = self.assets.font_small

        # 1. Dessiner les arêtes en premier
        for (pid, cid) in self._edges:
            if pid not in self._layout or cid not in self._layout:
                continue
            px, py = self._layout[pid]
            cx2, cy2 = self._layout[cid]

            p_taken = pid.replace("root_ch1","taken").replace("root_ch2","taken").replace("root_ch3","taken")
            taken   = (cid in self._choices_taken)
            # Une arête est "prise" si l'enfant est dans les choix pris
            col   = CYAN if taken else TEXT_GRAY
            alpha = 200 if taken else 70
            width = 2 if taken else 1

            # Progression d'animation basée sur l'apparition du nœud enfant
            anim_c = self._node_anims.get(cid, 0.0)
            anim_p = self._node_anims.get(pid, 0.0)
            anim   = min(anim_p, anim_c)
            if anim <= 0:
                continue

            # Courbe de Bézier cubique (via segments)
            steps = 20
            mx1 = (px + cx2) // 2
            for step in range(steps):
                frac0 = step / steps
                frac1 = (step + 1) / steps
                # Utiliser frac1 pour la progression
                if frac1 > anim:
                    break
                # Point de Bézier
                b0x = int(px + (mx1 - px) * frac0)
                b0y = int(py)
                b1x = int(mx1 + (cx2 - mx1) * frac0)
                b1y = int(py + (cy2 - py) * frac0)
                bx0 = int(b0x + (b1x - b0x) * frac0)
                by0 = int(b0y + (b1y - b0y) * frac0)

                b0x2 = int(px + (mx1 - px) * frac1)
                b1x2 = int(mx1 + (cx2 - mx1) * frac1)
                b1y2 = int(py + (cy2 - py) * frac1)
                bx1  = int(b0x2 + (b1x2 - b0x2) * frac1)
                by1  = int(b0y + (b1y2 - b0y) * frac1)

                edge_col = (*col, int(alpha * anim))
                s = pygame.Surface((abs(bx1-bx0)+width*2+2, abs(by1-by0)+width*2+2), pygame.SRCALPHA)
                # Simple ligne directe dans l'espace écran
                pygame.draw.line(screen, (*col, int(alpha * anim)),
                                 (bx0, by0), (bx1, by1), width)

        # 2. Dessiner les nœuds
        for nid, (cx, cy) in self._layout.items():
            anim = self._node_anims.get(nid, 0.0)
            if anim <= 0:
                continue
            self._draw_node(screen, nid, cx, cy, anim, t)

    def _draw_node(
        self, screen: pygame.Surface,
        nid: str, cx: int, cy: int,
        anim: float, t: float,
    ):
        fn = self.assets.font_med
        fs = self.assets.font_small

        is_taken  = (nid in self._choices_taken) or nid.startswith("root_")
        is_root   = nid.startswith("root_")
        NW, NH = self.NODE_W, self.NODE_H

        # Scale d'entrée
        scale = min(1.0, anim * 1.2)
        sw = int(NW * scale)
        sh = int(NH * scale)
        if sw < 4 or sh < 4:
            return

        node_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
        alpha = int(anim * 220)

        if is_root:
            bg_col     = (*CYAN, int(30 * anim))
            border_col = (*CYAN, alpha)
            text_col   = CYAN
        elif is_taken:
            pulse = 0.6 + 0.4 * math.sin(t * 2.5 + cx * 0.01)
            bg_col     = (*CYAN, int(45 * pulse * anim))
            border_col = (*CYAN, alpha)
            text_col   = CYAN
        else:
            bg_col     = (12, 18, 35, int(180 * anim))
            border_col = (*TEXT_GRAY, int(80 * anim))
            text_col   = TEXT_GRAY

        pygame.draw.rect(node_surf, bg_col,     (0, 0, sw, sh), border_radius=5)
        pygame.draw.rect(node_surf, border_col, (0, 0, sw, sh), width=2 if is_taken else 1, border_radius=5)

        # Texte du nœud (multi-ligne si "\n")
        # Trouver le label depuis l'arbre
        label = self._find_label(nid)
        lines = label.split("\n") if label else [nid]
        line_h = fs.get_height() + 2
        total_text_h = len(lines) * line_h
        ty0 = (sh - total_text_h) // 2
        for li, line in enumerate(lines):
            ls = fs.render(line, True, text_col)
            if ls.get_width() > sw - 8:
                ls = fs.render(line[:12], True, text_col)
            ls.set_alpha(int(anim * 255))
            node_surf.blit(ls, ((sw - ls.get_width()) // 2, ty0 + li * line_h))

        # Marqueur "pris" (coche ou point)
        if is_taken and not is_root:
            check_s = fs.render("✔", True, (*CYAN, alpha))
            node_surf.blit(check_s, (sw - check_s.get_width() - 3, 2))

        # Lueur externe pour nœuds pris
        if is_taken and not is_root:
            glow_r = max(sw, sh) // 2 + 6
            glow = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
            ga = int(25 * anim * (0.5 + 0.5 * math.sin(t * 2.5 + cx * 0.01)))
            pygame.draw.rect(glow, (*CYAN, ga), (0, 0, glow_r * 2, glow_r * 2), border_radius=8)
            screen.blit(glow, (cx - glow_r, cy - glow_r))

        screen.blit(node_surf, (cx - sw // 2, cy - sh // 2))

    def _find_label(self, nid: str) -> str:
        """Cherche récursivement le label d'un nœud par son id."""
        tree = self.CHAPTER_TREES.get(self._chapter)
        if not tree:
            return nid
        return self._find_label_in(nid, tree) or nid

    def _find_label_in(self, nid: str, node: dict) -> str | None:
        if node["id"] == nid:
            return node.get("label", nid)
        for child in node.get("children", []):
            res = self._find_label_in(nid, child)
            if res:
                return res
        return None

    def _continue_btn_rect(self) -> pygame.Rect:
        bw, bh = 180, 40
        return pygame.Rect((SCREEN_W - bw) // 2, SCREEN_H - 48, bw, bh)