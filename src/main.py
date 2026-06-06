import pygame
import sys
import os
import math

from config import *
from assets_manager import *
from models import *
from ui import DialogueBox, EvidencePanel, InventoryPanel, TitleScreen
from script import SCRIPT
from transitions import Transition   

# ── Moteur principal ────────────────────────────────────────────────────────────
class VNEngine:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock  = pygame.time.Clock()
        self.t = 0.0
        self.assets    = Assets()
        self.dlg       = DialogueBox(self.assets)
        self.evidence  = EvidencePanel(self.assets)
        self.inventory = InventoryPanel(self.assets)
        self.rain      = RainEffect()
        self.title_screen = TitleScreen(self.assets)
        self.state     = "title"   # title → game → end

        # Script
        self.script_idx = 0
        self.script     = SCRIPT
        self._build_index()
        self.current_node = None
        self.fade_alpha = 255
        self.fading_in  = True
        self.show_rain  = False
        self.bg_surf    = None
        self.char_surf  = None
        self.char_side  = "left"
        self.particles  = []
        

        # Musique
        if self.assets.bg_music:
            pygame.mixer.music.load(self.assets.bg_music)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        
        self.transition: Transition | None = None
        # Surface capturée juste avant le changement de scène.
        # Elle est passée à transition.draw() pour composer l'animation.
        self._prev_surface: "pygame.Surface | None" = None

    def _build_index(self):
        """Construit un dict id → index pour les branches."""
        self.id_map = {}
        for i, node in enumerate(self.script):
            if "id" in node:
                self.id_map[node["id"]] = i

    def _load_node(self, idx: int) -> None:
        if idx >= len(self.script):
            self.state = "end"
            return
        node = self.script[idx]

        # Capturer la frame courante AVANT de modifier la scène
        self._prev_surface = self.screen.copy()

        self.current_node = node

        # Background
        bg_name = node.get("bg")
        if bg_name and bg_name in self.assets.bg:
            self.bg_surf = self.assets.bg[bg_name]

        # Pluie
        self.show_rain = node.get("rain", False)

        # Personnage — compatible avec tous les chars (detective, policiere,
        # ferriere, natasha, taro, architect)
        char = node.get("char")
        expr = node.get("expr", 0)
        self.char_side = node.get("side", "left")
        if char:
            self.char_surf = self.assets.get_char(char, expr)
        else:
            self.char_surf = None

        # Dialogue
        choices = node.get("choices")
        self.dlg.set_text(node.get("text", ""), node.get("name", ""), choices)

        # Preuve à collecter
        ev = node.get("evidence")
        if ev:
            if not any(e[0] == ev[0] for e in self.evidence.items):
                self.evidence.add(*ev)
                for _ in range(20):
                    self.particles.append(Particle(SCREEN_W - 50, 80, PINK_ACCENT))

        # Transition — déclenchée seulement si le bg change OU si "transition" est explicite.
        # Sans cette condition, chaque ligne de dialogue déclencherait un fondu.
        bg_changed = bg_name is not None and bg_name != getattr(self, "_current_bg_name", None)
        has_explicit = "transition" in node

        if bg_changed or has_explicit:
            tr_name = node.get("transition", "fade_black")
            tr_kwargs = {}
            if tr_name == "iris" and "iris_center" in node:
                tr_kwargs["center"] = tuple(node["iris_center"])
            try:
                self.transition = Transition.create(tr_name, self.screen.get_size(), **tr_kwargs)
            except ValueError as e:
                print(f"[transitions] Avertissement : {e} — fondu noir utilisé par défaut.")
                self.transition = Transition.create("fade_black", self.screen.get_size())
        else:
            self.transition = None

        if bg_name:
            self._current_bg_name = bg_name

        # Fade-in de secours (désactivé si une transition gère déjà l'entrée)
        self.fading_in = False
        self.fade_alpha = 0

    def _advance(self, choice=None):
        """Avance dans le script. Gère les branches et saute les IDs alternatifs."""
        node = self.current_node
        chosen_branch_id = None

        if node and "choices" in node and choice is not None:
            branch = node.get("choice_branch", {})
            branch_id = branch.get(str(choice))
            chosen_branch_id = branch_id
            if branch_id and branch_id in self.id_map:
                next_idx = self.id_map[branch_id]
            else:
                next_idx = self.script_idx + 1
        else:
            next_idx = self.script_idx + 1

        # Si on n'est pas en train de suivre une branche, on saute les nœuds
        # qui ont un "id" (= débuts de branches alternatives non prises).
        if chosen_branch_id is None:
            while next_idx < len(self.script):
                candidate = self.script[next_idx]
                if "id" not in candidate:
                    break
                next_idx += 1

        self.script_idx = next_idx
        self._load_node(next_idx)

    def run(self):
        self.title_screen.update(0)
        dt = 1 / FPS

        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.t += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                self._handle_event(event)

            self._update(dt)
            self._draw()
            pygame.display.flip()

    def _handle_event(self, event):
        if self.state == "title":
            if self.title_screen.handle_event(event):
                self.state = "game"
                self.script_idx = 0
                self._load_node(0)
            return

        if self.state == "game":
            # Bloquer les inputs pendant une transition pour éviter de sauter une scène
            if self.transition is not None:
                return

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    if self.dlg.show_choices:
                        choice = self.dlg.get_choice()
                        self._advance(choice)
                    elif self.dlg.done:
                        self._advance()
                    else:
                        self.dlg.skip()
                elif event.key == pygame.K_LEFT:
                    self.dlg.select_choice(-1)
                elif event.key == pygame.K_RIGHT:
                    self.dlg.select_choice(1)
                elif event.key == pygame.K_e:
                    self.evidence.toggle()
                elif event.key == pygame.K_i:
                    self.inventory.toggle()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                dlg_rect = pygame.Rect(self.dlg.x, self.dlg.y, self.dlg.W, self.dlg.H)
                if self.dlg.show_choices:
                    choice = self._check_choice_click(mx, my)
                    if choice is not None:
                        self._advance(choice)
                elif dlg_rect.collidepoint(mx, my) or not self.dlg.show_choices:
                    if self.dlg.done:
                        self._advance()
                    else:
                        self.dlg.skip()

    def _check_choice_click(self, mx, my):
        choices = self.dlg.choices
        if not choices:
            return None
        cy = self.dlg.y + self.dlg.H - 50
        for i, _ in enumerate(choices):
            cw = (self.dlg.W - (self.dlg.MARGIN * 2)) // len(choices) - 10
            cx = self.dlg.x + self.dlg.MARGIN + i * (cw + 10)
            r = pygame.Rect(cx, cy, cw, 34)
            if r.collidepoint(mx, my):
                return i
        return None

    def _update(self, dt):
        if self.state == "title":
            self.title_screen.update(dt)
            return

        if self.state == "game":
            # Avancer la transition EN PREMIER (avant la logique de jeu)
            if self.transition is not None:
                done = self.transition.update(dt)
                if done:
                    self.transition = None

            self.dlg.update()
            if self.show_rain:
                self.rain.update()
            if self.fading_in:
                self.fade_alpha = max(0, self.fade_alpha - 8)
            self.particles = [p for p in self.particles if p.alive]
            for p in self.particles:
                p.update(dt)

    def _draw(self):
        if self.state == "title":
            self.title_screen.draw(self.screen)
            return
        if self.state == "end":
            self._draw_end()
            return
        if self.state == "game":
            self._draw_game()

    def _draw_game(self):
        self.screen.fill(DARK_BG)

        if self.bg_surf:
            self.screen.blit(self.bg_surf, (0, 0))
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 80))
        self.screen.blit(overlay, (0, 0))

        if self.show_rain:
            self.rain.draw(self.screen)

        if self.char_surf:
            cw, ch = self.char_surf.get_size()
            cy = SCREEN_H - self.dlg.H - ch - 24
            if self.char_side == "left":
                cx = 60
            else:
                cx = SCREEN_W - cw - 60
            shadow_surf = self.char_surf.copy()
            shadow_surf.fill((0, 0, 0, 80), special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(shadow_surf, (cx + 4, cy + 4))
            breath_y = int(math.sin(self.t * 1.2) * 3)
            self.screen.blit(self.char_surf, (cx, cy + breath_y))

        self.evidence.draw(self.screen, self.t)
        self.inventory.draw(self.screen, self.t)
        self._draw_hud()
        self.dlg.draw(self.screen, self.t)

        for p in self.particles:
            p.draw(self.screen)

        if self.fade_alpha > 0:
            ov = pygame.Surface((SCREEN_W, SCREEN_H))
            ov.fill(BLACK)
            ov.set_alpha(self.fade_alpha)
            self.screen.blit(ov, (0, 0))

        # Transition en dernier (layer le plus haut)
        if self.transition is not None and self._prev_surface is not None:
            self.transition.draw(self.screen, self._prev_surface)



    def _draw_hud(self):
        f = self.assets.font_small
        hud = pygame.Surface((SCREEN_W, 28), pygame.SRCALPHA)
        pygame.draw.rect(hud, (*DARK_BG, 200), (0, 0, SCREEN_W, 28))
        pygame.draw.line(hud, (*CYAN, 80), (0, 27), (SCREEN_W, 27))

        t1 = f.render(TITLE, True, CYAN)
        t2 = f.render(f"[I] Inventaire  [E] Preuves({len(self.evidence.items)})", True, TEXT_GRAY)
        t3 = f.render("[ESPACE] Continuer", True, TEXT_GRAY)

        hud.blit(t1, (10, 7))
        hud.blit(t2, (SCREEN_W // 2 - t2.get_width() // 2, 7))
        hud.blit(t3, (SCREEN_W - t3.get_width() - 10, 7))
        self.screen.blit(hud, (0, 0))

    def _draw_end(self):
        self.screen.fill(DARK_BG)
        f = self.assets.font_big
        fs = self.assets.font_med
        for i in range(80):
            r = (i * 137 + 17) % SCREEN_W
            s = (i * 97  + 31) % SCREEN_H
            a = int(80 + 60 * math.sin(self.t * 0.5 + i))
            pygame.draw.circle(self.screen, (a, a, min(255, a + 60)), (r, s), 1)

        msgs = [
            ("FIN DU CHAPITRE III", CYAN),
            ("Merci d'avoir joué à NUIT SANS TÉMOIN", TEXT_MAIN),
            ("", WHITE),
            (f"Preuves collectées : {len(self.evidence.items)}", GOLD),
            ("", WHITE),
            ("Appuyez sur ECHAP pour quitter", TEXT_GRAY),
        ]
        total_h = len(msgs) * 44
        start_y = (SCREEN_H - total_h) // 2

        for i, (msg, col) in enumerate(msgs):
            if not msg:
                continue
            font = f if i == 0 else fs
            surf = font.render(msg, True, col)
            self.screen.blit(surf, ((SCREEN_W - surf.get_width()) // 2,
                                     start_y + i * 44))

# ── Lancement ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    engine = VNEngine()
    engine.run()