"""
cg_manager.py — Gestionnaire de déblocage des illustrations CG
==============================================================

API publique :
    mgr = CGManager(assets_base_path)
    mgr.unlock("cg_01_ruelle")       → True si nouvellement débloqué, False sinon
    mgr.is_unlocked("cg_01_ruelle")  → bool
    mgr.unlocked_ids()               → list[str]
    mgr.to_list()                    → list[str]   (pour JSON)
    mgr.from_list(data)              → None         (restaure depuis JSON)
    mgr.get_surface("cg_01_ruelle")  → pygame.Surface | None (chargé à la demande)

Les images sont chargées en lazy loading depuis assets/cg/<file>.
"""

from __future__ import annotations

import os
import pygame
from typing import Optional

from cg_catalogue import CG_CATALOGUE, CG_INDEX


class CGManager:
    def __init__(self, assets_base: str) -> None:
        self._cg_dir       = os.path.join(assets_base, "cg")
        self._unlocked:    set[str] = set()
        self._new_unlocks: list[str] = []          # file pour les notifications
        self._cache:       dict[str, pygame.Surface] = {}  # lazy-loaded surfaces

    # ── Déblocage ──────────────────────────────────────────────────────────────

    def unlock(self, cg_id: str) -> bool:
        """
        Débloque une CG.
        Retourne True si c'est un déblocage nouveau (False si déjà connu).
        Ignore silencieusement les ids inconnus.
        """
        if cg_id not in CG_INDEX:
            print(f"[CGManager] id inconnu ignoré : '{cg_id}'")
            return False
        if cg_id in self._unlocked:
            return False
        self._unlocked.add(cg_id)
        self._new_unlocks.append(cg_id)
        return True

    def pop_new_unlocks(self) -> list[str]:
        """Consomme et retourne la liste des déblocages récents."""
        out = list(self._new_unlocks)
        self._new_unlocks.clear()
        return out

    def is_unlocked(self, cg_id: str) -> bool:
        return cg_id in self._unlocked

    def unlocked_ids(self) -> list[str]:
        return list(self._unlocked)

    def count_unlocked(self) -> int:
        return len(self._unlocked)

    def total(self) -> int:
        return len(CG_CATALOGUE)

    # ── Images (lazy loading) ──────────────────────────────────────────────────

    def get_surface(
        self,
        cg_id: str,
        target_size: tuple[int, int] | None = None,
    ) -> Optional[pygame.Surface]:
        """
        Retourne la surface pygame de la CG demandée, ou None si non trouvée.
        L'image est mise en cache après le premier chargement.
        Si target_size est fourni, l'image est redimensionnée à cette taille.
        """
        entry = CG_INDEX.get(cg_id)
        if entry is None:
            return None

        cache_key = f"{cg_id}_{target_size}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        path = os.path.join(self._cg_dir, entry["file"])
        if not os.path.exists(path):
            # Générer un placeholder coloré si le fichier est absent
            surf = self._make_placeholder(entry, target_size or (640, 360))
            self._cache[cache_key] = surf
            return surf

        try:
            raw = pygame.image.load(path).convert()
            if target_size:
                raw = pygame.transform.smoothscale(raw, target_size)
            self._cache[cache_key] = raw
            return raw
        except pygame.error as e:
            print(f"[CGManager] Erreur chargement {path}: {e}")
            surf = self._make_placeholder(entry, target_size or (640, 360))
            self._cache[cache_key] = surf
            return surf

    def _make_placeholder(self, entry: dict, size: tuple[int, int]) -> pygame.Surface:
        """
        Génère une surface de substitution quand le fichier PNG est absent.
        Affiche le titre et le chapitre sur un fond sombre dégradé.
        """
        w, h = size
        surf = pygame.Surface(size)

        # Fond dégradé bleu-nuit
        for y in range(h):
            ratio = y / h
            r = int(8  + 12  * ratio)
            g = int(10 + 15  * ratio)
            b = int(20 + 30  * ratio)
            pygame.draw.line(surf, (r, g, b), (0, y), (w, y))

        # Cadre cyan
        pygame.draw.rect(surf, (0, 120, 160), (0, 0, w, h), 2)

        # Icône verrou / image manquante
        cx, cy = w // 2, h // 2 - 30
        icon_r = min(40, w // 8)
        pygame.draw.circle(surf, (0, 60, 80), (cx, cy), icon_r)
        pygame.draw.circle(surf, (0, 160, 200), (cx, cy), icon_r, 2)

        # Texte (utilise la police pygame par défaut)
        font_big   = pygame.font.SysFont("monospace", max(14, w // 40), bold=True)
        font_small = pygame.font.SysFont("monospace", max(10, w // 60))

        title_surf = font_big.render(entry.get("title", "CG"), True, (0, 220, 255))
        chap_surf  = font_small.render(entry.get("chapter", ""), True, (140, 150, 170))
        miss_surf  = font_small.render("[ image manquante ]", True, (80, 90, 110))

        surf.blit(title_surf, (w // 2 - title_surf.get_width() // 2, cy + icon_r + 10))
        surf.blit(chap_surf,  (w // 2 - chap_surf.get_width()  // 2, cy + icon_r + 36))
        surf.blit(miss_surf,  (w // 2 - miss_surf.get_width()  // 2, h - 30))

        return surf

    # ── Sérialisation ──────────────────────────────────────────────────────────

    def to_list(self) -> list[str]:
        """Sérialise pour JSON."""
        return sorted(self._unlocked)

    def from_list(self, data: list[str]) -> None:
        """Restaure depuis JSON."""
        self._unlocked = set(str(x) for x in data if x in CG_INDEX)
        self._new_unlocks.clear()
