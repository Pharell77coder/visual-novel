"""
save_manager.py — Système de sauvegarde JSON sur 3 slots
=========================================================

Structure d'un slot :
    {
        "slot":        int,           # 0-2
        "script_idx":  int,
        "evidence":    [[nom, desc], ...],
        "deductions":  [dict, ...],   # liste des déductions débloquées
        "bg_name":     str | None,
        "saved_at":    "YYYY-MM-DD HH:MM",
        "scene_name":  str
    }

Utilisation :
    sm = SaveManager()
    sm.save(slot=0, script_idx=42, evidence=[("Clé USB", "...")],
            bg_name="bureau", scene_name="...", deductions=[...])
    data = sm.load(slot=0)   # None si vide
    sm.delete(slot=1)
    slots = sm.all_slots()   # liste de 3 éléments (None si vide)
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Optional

# ── Chemin du répertoire de sauvegarde ────────────────────────────────────────
_SRC_DIR  = os.path.dirname(os.path.abspath(__file__))
_BASE_DIR = os.path.dirname(_SRC_DIR) if os.path.basename(_SRC_DIR) == "src" else _SRC_DIR
SAVE_DIR  = os.path.join(_BASE_DIR, "saves")
NUM_SLOTS = 3


def _slot_path(slot: int) -> str:
    return os.path.join(SAVE_DIR, f"slot_{slot}.json")


class SaveManager:
    def __init__(self) -> None:
        os.makedirs(SAVE_DIR, exist_ok=True)

    # ── Écriture ───────────────────────────────────────────────────────────────

    def save(
        self,
        slot:        int,
        script_idx:  int,
        evidence:    list,
        bg_name:     Optional[str] = None,
        scene_name:  str = "",
        deductions:  Optional[list] = None,
        cg_unlocked: Optional[list] = None,   # liste des ids CG débloqués
    ) -> bool:
        """
        Sauvegarde l'état dans le slot donné (0-2).
        Retourne True en cas de succès.
        """
        if not (0 <= slot < NUM_SLOTS):
            print(f"[SaveManager] Slot invalide : {slot}")
            return False

        data = {
            "slot":        slot,
            "script_idx":  script_idx,
            "evidence":    [list(e) for e in evidence],
            "deductions":  deductions or [],
            "cg_unlocked": cg_unlocked or [],           # NOUVEAU
            "bg_name":     bg_name,
            "scene_name":  scene_name[:60],
            "saved_at":    datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        try:
            with open(_slot_path(slot), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[SaveManager] Sauvegarde slot {slot} — scène {script_idx}")
            return True
        except OSError as e:
            print(f"[SaveManager] Erreur écriture slot {slot} : {e}")
            return False

    # ── Lecture ────────────────────────────────────────────────────────────────

    def load(self, slot: int) -> Optional[dict]:
        """Retourne le dict du slot, ou None s'il est vide / invalide."""
        path = _slot_path(slot)
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Reconvertit les listes [nom, desc] en tuples
            data["evidence"]    = [tuple(e) for e in data.get("evidence", [])]
            data["deductions"]  = data.get("deductions", [])
            data["cg_unlocked"] = data.get("cg_unlocked", [])   # rétrocompatibilité
            return data
        except (OSError, json.JSONDecodeError) as e:
            print(f"[SaveManager] Erreur lecture slot {slot} : {e}")
            return None

    # ── Suppression ────────────────────────────────────────────────────────────

    def delete(self, slot: int) -> bool:
        path = _slot_path(slot)
        if os.path.exists(path):
            try:
                os.remove(path)
                return True
            except OSError as e:
                print(f"[SaveManager] Erreur suppression slot {slot} : {e}")
        return False

    # ── Lecture de tous les slots ──────────────────────────────────────────────

    def all_slots(self) -> list:
        """Retourne une liste de NUM_SLOTS éléments (dict ou None)."""
        return [self.load(i) for i in range(NUM_SLOTS)]