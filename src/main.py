import pygame
import sys
import os
import math

from config import *
from assets_manager import *
from models import *
from ui import DialogueBox, EvidencePanel, InventoryPanel, TitleScreen, SaveSlotScreen, DeductionPanel
from script import SCRIPT
from transitions import Transition
from save_manager import SaveManager
from deductions import DeductionEngine

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

        # ── Système de déductions ──────────────────────────────────────────────
        self.ded_engine  = DeductionEngine()
        self.ded_panel   = DeductionPanel(self.assets, self.ded_engine)

        # ── UI ────────────────────────────────────────────────────────────────
        self.dlg         = DialogueBox(self.assets)
        self.evidence    = EvidencePanel(self.assets, self.ded_engine)
        self.inventory   = InventoryPanel(self.assets)
        self.rain        = RainEffect()
        self.title_screen = TitleScreen(self.assets)

        # ── Sauvegarde ─────────────────────────────────────────────────────────
        self.save_manager = SaveManager()
        self.save_screen  = SaveSlotScreen(self.assets, self.save_manager, mode="save")

        # ── État ──────────────────────────────────────────────────────────────
        self.state = "title"   # title → game → save_menu → load_menu → end

        self.script_idx      = 0
        self.script          = SCRIPT
        self._build_index()
        self.current_node    = None
        self.fade_alpha      = 255
        self.fading_in       = True
        self.show_rain       = False
        self.bg_surf         = None
        self.char_surf       = None
        self.char_side       = "left"
        self.particles       = []
        self._current_bg_name = None

        # Musique
        if self.assets.bg_music:
            pygame.mixer.music.load(self.assets.bg_music)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

        self.transition: Transition | None = None
        self._prev_surface: "pygame.Surface | None" = None

        # Toast
        self._toast_msg   = ""
        self._toast_timer = 0.0
        self._toast_ok    = True

    # ── Index de script ────────────────────────────────────────────────────────

    def _build_index(self):
        self.id_map = {}
        for i, node in enumerate(self.script):
            if "id" in node:
                self.id_map[node["id"]] = i

    # ── Helpers sauvegarde ─────────────────────────────────────────────────────

    def _scene_label(self) -> str:
        node = self.current_node
        if not node:
            return "Début"
        name = node.get("name", "")
        text = node.get("text", "")
        if name:
            return f"{name} — {text[:30]}"
        return text[:50] or f"Scène {self.script_idx}"

    def _do_save(self, slot: int) -> None:
        ok = self.save_manager.save(
            slot        = slot,
            script_idx  = self.script_idx,
            evidence    = self.evidence.items,
            bg_name     = self._current_bg_name,
            scene_name  = self._scene_label(),
            deductions  = self.ded_engine.to_list(),
        )
        self._toast(f"Sauvegarde slot {slot + 1} — OK" if ok else "Erreur sauvegarde !", ok)

    def _do_load(self, slot: int) -> None:
        data = self.save_manager.load(slot)
        if data is None:
            self._toast("Slot vide !", success=False)
            return
        self.evidence.items = list(data["evidence"])
        # Restaurer les déductions
        ded_data = data.get("deductions", [])
        self.ded_engine.from_list(ded_data)
        self._load_node(data["script_idx"])
        self._toast(f"Chargement slot {slot + 1} — OK", success=True)

    def _toast(self, msg: str, success: bool = True) -> None:
        self._toast_msg   = msg
        self._toast_timer = 2.5
        self._toast_ok    = success

    # ── Chargement de nœud ────────────────────────────────────────────────────

    def _load_node(self, idx: int) -> None:
        if idx >= len(self.script):
            self.state = "end"
            return
        node = self.script[idx]
        self._prev_surface = self.screen.copy()
        self.current_node  = node
        self.script_idx    = idx

        bg_name = node.get("bg")
        if bg_name and bg_name in self.assets.bg:
            self.bg_surf = self.assets.bg[bg_name]

        self.show_rain = node.get("rain", False)

        char = node.get("char")
        expr = node.get("expr", 0)
        self.char_side = node.get("side", "left")
        if char:
            self.char_surf = self.assets.get_char(char, expr)
        else:
            self.char_surf = None

        choices = node.get("choices")
        self.dlg.set_text(node.get("text", ""), node.get("name", ""), choices)

        ev = node.get("evidence")
        if ev:
            if not any(e[0] == ev[0] for e in self.evidence.items):
                self.evidence.add(*ev)
                for _ in range(20):
                    self.particles.append(Particle(SCREEN_W - 50, 80, PINK_ACCENT))

        bg_changed   = bg_name is not None and bg_name != self._current_bg_name
        has_explicit = "transition" in node

        if bg_changed or has_explicit:
            tr_name   = node.get("transition", "fade_black")
            tr_kwargs = {}
            if tr_name == "iris" and "iris_center" in node:
                tr_kwargs["center"] = tuple(node["iris_center"])
            try:
                self.transition = Transition.create(tr_name, self.screen.get_size(), **tr_kwargs)
            except ValueError as e:
                print(f"[transitions] {e}")
                self.transition = Transition.create("fade_black", self.screen.get_size())
        else:
            self.transition = None

        if bg_name:
            self._current_bg_name = bg_name

        self.fading_in  = False
        self.fade_alpha = 0

    def _advance(self, choice=None):
        node = self.current_node
        chosen_branch_id = None

        if node and "choices" in node and choice is not None:
            branch   = node.get("choice_branch", {})
            branch_id = branch.get(str(choice))
            chosen_branch_id = branch_id
            if branch_id and branch_id in self.id_map:
                next_idx = self.id_map[branch_id]
            else:
                next_idx = self.script_idx + 1
        else:
            next_idx = self.script_idx + 1

        if chosen_branch_id is None:
            while next_idx < len(self.script):
                if "id" not in self.script[next_idx]:
                    break
                next_idx += 1

        self._load_node(next_idx)

    # ── Boucle principale ──────────────────────────────────────────────────────

    def run(self):
        self.title_screen.update(0)
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.t += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.state in ("save_menu", "load_menu"):
                        self.state = "game"
                        self.save_screen.close()
                    else:
                        pygame.quit(); sys.exit()
                self._handle_event(event)

            self._update(dt)
            self._draw()
            pygame.display.flip()

    # ── Gestion des événements ─────────────────────────────────────────────────

    def _handle_event(self, event):
        if self.state == "title":
            if self.title_screen.handle_event(event):
                self.state = "game"
                self._load_node(0)
            return

        if self.state in ("save_menu", "load_menu"):
            self.save_screen.handle_event(event)
            result = self.save_screen.pop_result()
            if result is not None:
                if result == -1:
                    self.state = "game"
                else:
                    if self.state == "save_menu":
                        self._do_save(result)
                    else:
                        self._do_load(result)
                    self.state = "game"
            return

        if self.state == "game":
            if self.transition is not None:
                return

            # Le panneau de preuves consomme l'événement en mode select
            if self.evidence.visible:
                consumed = self.evidence.handle_event(event)
                if consumed:
                    return

            # Panneau de déductions
            if self.ded_panel.handle_event(event):
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.save_screen.open(mode="save")
                    self.state = "save_menu"
                    return
                if event.key == pygame.K_l:
                    self.save_screen.open(mode="load")
                    self.state = "load_menu"
                    return
                if event.key == pygame.K_e:
                    self.evidence.toggle()
                    return
                if event.key == pygame.K_d:
                    self.ded_panel.toggle()
                    return
                if event.key == pygame.K_i:
                    self.inventory.toggle()
                    return

                # Navigation dialogue (bloquée si le panneau preuves est ouvert)
                if not self.evidence.visible:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        if self.dlg.show_choices:
                            self._advance(self.dlg.get_choice())
                        elif self.dlg.done:
                            self._advance()
                        else:
                            self.dlg.skip()
                    elif event.key == pygame.K_LEFT:
                        self.dlg.select_choice(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.dlg.select_choice(1)

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.evidence.visible:
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
            if pygame.Rect(cx, cy, cw, 34).collidepoint(mx, my):
                return i
        return None

    # ── Mise à jour ────────────────────────────────────────────────────────────

    def _update(self, dt):
        if self.state == "title":
            self.title_screen.update(dt)
            return

        if self.state in ("game", "save_menu", "load_menu"):
            if self.transition is not None:
                if self.transition.update(dt):
                    self.transition = None

            self.dlg.update(dt)
            self.evidence.update(dt)   # timers d'animation
            if self.show_rain:
                self.rain.update()
            if self.fading_in:
                self.fade_alpha = max(0, self.fade_alpha - 8)
            self.particles = [p for p in self.particles if p.alive]
            for p in self.particles:
                p.update(dt)

            if self._toast_timer > 0:
                self._toast_timer = max(0.0, self._toast_timer - dt)

    # ── Rendu ──────────────────────────────────────────────────────────────────

    def _draw(self):
        if self.state == "title":
            self.title_screen.draw(self.screen)
            return
        if self.state == "end":
            self._draw_end()
            return
        self._draw_game()
        if self.state in ("save_menu", "load_menu"):
            self.save_screen.draw(self.screen, self.t)

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
            cx = 60 if self.char_side == "left" else SCREEN_W - cw - 60
            shadow = self.char_surf.copy()
            shadow.fill((0, 0, 0, 80), special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(shadow, (cx + 4, cy + 4))
            breath_y = int(math.sin(self.t * 1.2) * 3)
            self.screen.blit(self.char_surf, (cx, cy + breath_y))

        # Panneaux
        self.evidence.draw(self.screen, self.t)
        self.ded_panel.draw(self.screen, self.t)
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

        if self.transition is not None and self._prev_surface is not None:
            self.transition.draw(self.screen, self._prev_surface)

        self._draw_toast()

    def _draw_hud(self):
        f   = self.assets.font_small
        hud = pygame.Surface((SCREEN_W, 28), pygame.SRCALPHA)
        pygame.draw.rect(hud, (*DARK_BG, 200), (0, 0, SCREEN_W, 28))
        pygame.draw.line(hud, (*CYAN, 80), (0, 27), (SCREEN_W, 27))

        t1 = f.render(TITLE, True, CYAN)
        t2 = f.render(
            f"[E] Preuves({len(self.evidence.items)})  "
            f"[D] Déductions({self.ded_engine.count()})  [I] Inv.",
            True, TEXT_GRAY)
        t3 = f.render("[S] Sauver  [L] Charger  [ESPACE] Continuer", True, TEXT_GRAY)

        hud.blit(t1, (10, 7))
        hud.blit(t2, (SCREEN_W // 2 - t2.get_width() // 2, 7))
        hud.blit(t3, (SCREEN_W - t3.get_width() - 10, 7))
        self.screen.blit(hud, (0, 0))

    def _draw_toast(self):
        if self._toast_timer <= 0:
            return
        fs    = self.assets.font_small
        alpha = min(255, int(self._toast_timer * 180))
        col   = CYAN if self._toast_ok else RED_ACCENT
        msg_surf = fs.render(self._toast_msg, True, col)
        tw = msg_surf.get_width() + 24
        th = msg_surf.get_height() + 14

        badge = pygame.Surface((tw, th), pygame.SRCALPHA)
        pygame.draw.rect(badge, (*DARK_BG, min(220, alpha)), (0, 0, tw, th), border_radius=6)
        pygame.draw.rect(badge, (*col, min(200, alpha)),     (0, 0, tw, th), width=1, border_radius=6)
        badge.set_alpha(alpha)

        txt_s = pygame.Surface(msg_surf.get_size(), pygame.SRCALPHA)
        txt_s.blit(msg_surf, (0, 0))
        txt_s.set_alpha(alpha)

        bx = (SCREEN_W - tw) // 2
        by = SCREEN_H - self.dlg.H - th - 14
        self.screen.blit(badge, (bx, by))
        self.screen.blit(txt_s, (bx + 12, by + 7))

    def _draw_end(self):
        self.screen.fill(DARK_BG)
        f  = self.assets.font_big
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
            (f"Preuves : {len(self.evidence.items)}  •  Déductions : {self.ded_engine.count()}", GOLD),
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
            self.screen.blit(surf, ((SCREEN_W - surf.get_width()) // 2, start_y + i * 44))


# ── Lancement ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    engine = VNEngine()
    engine.run()