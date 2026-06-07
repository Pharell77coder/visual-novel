"""
interrogation.py — Mini-jeu d'interrogatoire
============================================

Système de pression psychologique sur un suspect avec timer et actions.
Actions : Press (confrontation directe), Bluff (manipulation), Silence (attente).

Suspects disponibles : "taro" | "ferriere"

─── Intégration VNEngine (main.py) ────────────────────────────────────────────

    from interrogation import InterrogationMinigame

    # Création :
    self.interro = InterrogationMinigame(
        screen     = self.screen,
        assets     = self.assets,
        suspect_id = "taro",      # ou "ferriere"
        time_limit = 90,
        on_success = lambda: self._load_node("sc_taro_confesse"),
        on_failure = lambda: self._load_node("sc_taro_silence"),
    )

    # Dans update(dt, events) — AVANT le dessin :
    if self.interro:
        result = self.interro.update(dt, events)
        if result == "success":
            fn = self.interro.on_success
            self.interro = None
            fn()
        elif result == "failure":
            fn = self.interro.on_failure
            self.interro = None
            fn()

    # Dans draw() :
    if self.interro:
        self.interro.draw(self.screen)

─── Hook script.py ────────────────────────────────────────────────────────────

    {
        "id":         "sc_42",
        "type":       "interrogation",
        "suspect":    "taro",
        "time_limit": 90,
        "on_success": "sc_43_confesse",
        "on_failure": "sc_44_echappe",
    }

─── Mécanique ─────────────────────────────────────────────────────────────────

    Actions et coûts :
        PRESS   → pression forte (+10-18%),  coût -8s,  cooldown 3s
        BLUFF   → pression risquée (+15-22% / -4-9%), coût -5s, cooldown 5s
        SILENCE → pression douce (+3-7%),    coût -2s,  cooldown 0.8s

    Victoire  : pression ≥ 100 % avant la fin du timer
    Défaite   : timer épuisé

    Profils suspects :
        Taro     — vulnérable au Silence (×1.4), résiste au Bluff (p=0.45)
        Ferrière — vulnérable au Bluff  (×1.3), résiste au Silence (×0.7)

─── États du suspect (seuils de pression) ────────────────────────────────────

    0 %  → DÉFIANT     25 %  → RÉSISTANT     50 %  → NERVEUX
    70 % → FISSURÉ     85 %  → CRAQUANT      100 % → CRAQUÉ (fin)
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Literal, Optional

import pygame

from config import (
    SCREEN_W, SCREEN_H,
    BLACK, WHITE, CYAN, CYAN_DIM, DARK_BG, DIALOGUE_BG,
    TEXT_MAIN, TEXT_NAME, TEXT_GRAY, PINK_ACCENT, GOLD, RED_ACCENT,
)

# ══════════════════════════════════════════════════════════════════════════════
# Constantes
# ══════════════════════════════════════════════════════════════════════════════

PRESSURE_WIN   = 1.0      # seuil de victoire
PRESSURE_DECAY = 0.0012   # décroissance passive par seconde (crée l'urgence)
_PAD           = 14       # padding général UI

# Coûts timer par action (secondes)
_COST_PRESS   = 8.0
_COST_BLUFF   = 5.0
_COST_SILENCE = 2.0

# Délai (s) avant d'appeler on_success / on_failure après la fin
_END_HOLD = 3.2

# Seuils marqueurs sur la jauge
_BAR_MARKERS = (0.25, 0.50, 0.70, 0.85)

# ══════════════════════════════════════════════════════════════════════════════
# État du suspect
# ══════════════════════════════════════════════════════════════════════════════

class SuspectState(Enum):
    DEFIANT   = 0  # 0 – 24 %
    RESISTANT = 1  # 25 – 49 %
    NERVOUS   = 2  # 50 – 69 %
    CRACKING  = 3  # 70 – 84 %
    BREAKING  = 4  # 85 – 99 %


def _state_from(p: float) -> SuspectState:
    if p >= 0.85: return SuspectState.BREAKING
    if p >= 0.70: return SuspectState.CRACKING
    if p >= 0.50: return SuspectState.NERVOUS
    if p >= 0.25: return SuspectState.RESISTANT
    return SuspectState.DEFIANT


# (label_affiché, couleur_RGB)
_STATE_META: dict[SuspectState, tuple[str, tuple]] = {
    SuspectState.DEFIANT:   ("DÉFIANT",   (210,  55,  55)),
    SuspectState.RESISTANT: ("RÉSISTANT", (215, 105,  35)),
    SuspectState.NERVOUS:   ("NERVEUX",   (200, 175,  40)),
    SuspectState.CRACKING:  ("FISSURÉ",   (120, 210,  70)),
    SuspectState.BREAKING:  ("CRAQUANT",  ( 50, 230, 110)),
}

# ══════════════════════════════════════════════════════════════════════════════
# Slot d'action (avec cooldown)
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class _ActionSlot:
    name:     str
    label:    str
    desc:     str
    color:    tuple
    key:      int        # touche principale (AZERTY : A, Z, E)
    key_alt:  int        # touche alternative (1, 2, 3)
    cooldown: float
    _cd: float = field(default=0.0, init=False)

    @property
    def ready(self) -> bool:
        return self._cd <= 0.0

    def tick(self, dt: float) -> None:
        self._cd = max(0.0, self._cd - dt)

    def trigger(self) -> None:
        self._cd = self.cooldown

    @property
    def cd_frac(self) -> float:
        """1.0 = cooldown plein, 0.0 = prêt."""
        return self._cd / self.cooldown if self.cooldown > 0 else 0.0

    @property
    def cd_remain(self) -> float:
        return self._cd


def _build_actions() -> list[_ActionSlot]:
    return [
        _ActionSlot(
            "press",   "PRESS",   "Confronter avec une preuve directe",
            RED_ACCENT, pygame.K_a, pygame.K_1, 3.0,
        ),
        _ActionSlot(
            "bluff",   "BLUFF",   "Prétendre avoir une preuve décisive",
            GOLD,       pygame.K_z, pygame.K_2, 5.0,
        ),
        _ActionSlot(
            "silence", "SILENCE", "Laisser le suspect se décomposer",
            CYAN,       pygame.K_e, pygame.K_3, 0.8,
        ),
    ]


# ══════════════════════════════════════════════════════════════════════════════
# Feedback flottant
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class _Feedback:
    text:     str
    color:    tuple
    positive: bool = True
    life:     float = field(default=2.8, init=False)
    _max:     float = field(default=2.8, init=False)

    def tick(self, dt: float) -> None:
        self.life = max(0.0, self.life - dt)

    @property
    def alive(self) -> bool:
        return self.life > 0.0

    @property
    def alpha(self) -> int:
        ratio = self.life / self._max
        if ratio < 0.25:
            return int(255 * ratio / 0.25)
        return 255


# ══════════════════════════════════════════════════════════════════════════════
# Flash d'écran
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class _ScreenFlash:
    color: tuple
    life:  float = 0.35
    _max:  float = field(default=0.35, init=False)

    def tick(self, dt: float) -> None:
        self.life = max(0.0, self.life - dt)

    @property
    def alive(self) -> bool:
        return self.life > 0.0

    @property
    def alpha(self) -> int:
        return int(90 * (self.life / self._max))


# ══════════════════════════════════════════════════════════════════════════════
# Profil du suspect
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class SuspectProfile:
    id:   str
    name: str
    role: str

    # Résistance globale (0 = très fragile, 1 = acier)
    resistance: float = 0.5

    # Multiplicateurs par type d'action
    press_mult:   float = 1.0
    bluff_mult:   float = 1.0
    silence_mult: float = 1.0

    # Probabilité de succès du bluff (0-1)
    bluff_p: float = 0.55

    # Index de sprite par label d'état
    expr: dict[str, int] = field(default_factory=dict)

    # Dialogue idle par label d'état
    idle: dict[str, list[str]] = field(default_factory=dict)

    # Réactions aux actions
    react_press:    list[str] = field(default_factory=list)
    react_bluff_ok: list[str] = field(default_factory=list)
    react_bluff_no: list[str] = field(default_factory=list)
    react_silence:  list[str] = field(default_factory=list)

    # Lignes de fin
    line_success: str = ""
    line_failure: str = ""


# ══════════════════════════════════════════════════════════════════════════════
# Profil : Taro Mitsuki
# ══════════════════════════════════════════════════════════════════════════════

TARO = SuspectProfile(
    id         = "taro",
    name       = "Taro Mitsuki",
    role       = "Informateur — Synarchie",
    resistance   = 0.45,
    press_mult   = 1.20,   # craque sous la confrontation directe
    bluff_mult   = 0.80,   # vérifie ses informations, méfiant
    silence_mult = 1.45,   # l'attente l'angoisse profondément
    bluff_p      = 0.42,   # difficile à bluffer, il connaît les ficelles

    expr = {
        "DÉFIANT":   1,
        "RÉSISTANT": 1,
        "NERVEUX":   3,
        "FISSURÉ":   3,
        "CRAQUANT":  3,
    },

    idle = {
        "DÉFIANT": [
            "Je n'ai rien à vous dire.",
            "Vous perdez votre temps.",
            "Appelez mon avocat.",
            "Je ne connais pas ce Vane.",
        ],
        "RÉSISTANT": [
            "Ce que vous pensez savoir… c'est rien.",
            "Je suis une simple connaissance de Vane.",
            "Ces gens-là, si vous les cherchez, vous les trouvez.",
            "Je veux une garantie avant de parler.",
        ],
        "NERVEUX": [
            "Attendez— je veux d'abord une garantie.",
            "Vous réalisez à qui vous vous attaquez ?",
            "Si je parle… ma famille…",
            "Ces gens-là ne plaisantent pas avec les témoins.",
        ],
        "FISSURÉ": [
            "L'enregistrement… comment vous l'avez eu ?",
            "C'était pas censé se passer comme ça.",
            "Ferrière m'a dit que Vane avait compris les règles…",
            "J'ai juste transmis des messages. C'est tout ce que j'ai fait.",
        ],
        "CRAQUANT": [
            "D'accord. D'accord… écoutez-moi bien.",
            "Le Loft 7, c'est Ferrière qui gère. Moi j'ai juste livré les messages.",
            "Il y a un registre. Genève. Tout y est.",
            "Je vais tout vous dire — mais j'ai besoin d'une protection.",
        ],
    },

    react_press = [
        "Vous avez rien — c'est du bluff !",
        "Ces preuves ne prouvent rien du tout.",
        "J'ai le droit de garder le silence.",
        "Vous m'impressionnez pas.",
        "C'est des suppositions. Rien de concret.",
    ],
    react_bluff_ok = [
        "Comment… comment vous avez ce document ?",
        "Ils m'avaient dit que ça resterait secret.",
        "Très bien. On peut peut-être s'arranger.",
        "Attendez— d'où ça sort, ça ?",
    ],
    react_bluff_no = [
        "C'est faux. Je sais exactement ce que vous avez.",
        "Vous inventez. Mauvais coup, inspecteur.",
        "Vous croyez que je suis naïf ?",
        "J'ai fait ce métier. Je reconnais un bluff.",
    ],
    react_silence = [
        "Pourquoi vous me regardez comme ça ?",
        "… Dites quelque chose.",
        "Ce silence… c'est une tactique, hein.",
        "Arrêtez de me fixer. C'est déstabilisant.",
        "C'est quoi ce jeu ?",
    ],

    line_success = (
        "D'accord… d'accord. Je vais tout vous dire. "
        "Ferrière, le Loft 7, Genève — tout. "
        "Mais je veux une protection pour ma famille."
    ),
    line_failure = (
        "Mon avocat arrive dans dix minutes. "
        "Après ça, vous n'entendrez plus un seul mot de moi."
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
# Profil : Capitaine Ferrière
# ══════════════════════════════════════════════════════════════════════════════

FERRIERE = SuspectProfile(
    id         = "ferriere",
    name       = "Capitaine Ferrière",
    role       = "Police — Agent Synarchie",
    resistance   = 0.72,
    press_mult   = 0.88,   # aguerri, supporte la pression frontale
    bluff_mult   = 1.35,   # son ego le rend aveugle aux manipulations
    silence_mult = 0.65,   # le silence ne l'atteint presque pas
    bluff_p      = 0.62,   # surestime ses protections, plus facile à bluffer

    expr = {
        "DÉFIANT":   1,
        "RÉSISTANT": 1,
        "NERVEUX":   1,
        "FISSURÉ":   3,
        "CRAQUANT":  3,
    },

    idle = {
        "DÉFIANT": [
            "Je suis flic depuis vingt-deux ans. Vous croyez me faire peur ?",
            "Vous n'avez rien. Sinon, je serais en garde à vue.",
            "Cette conversation est terminée.",
            "J'ai vu des centaines d'interrogatoires. Celui-là m'impressionne pas.",
        ],
        "RÉSISTANT": [
            "Vane ? Je le croisais au boulot. Point.",
            "Mes supérieurs sont au courant de cet entretien ?",
            "Faites attention à ce que vous insinuez, inspecteur.",
            "Vous jouez à quoi, exactement ?",
        ],
        "NERVEUX": [
            "Cette photo… c'est pas moi.",
            "L'enregistrement peut être truqué. Facilement.",
            "Je veux voir votre chef de service maintenant.",
            "Vous réalisez ce que vous faites, là ?",
        ],
        "FISSURÉ": [
            "Où est-ce que vous avez trouvé ça ?",
            "Ces chiffres ne prouvent rien hors contexte.",
            "Vane a fait des erreurs. Moi, j'exécutais des ordres.",
            "Quelqu'un vous a donné ça. Qui ?",
        ],
        "CRAQUANT": [
            "Très bien. Il y a des gens au-dessus de moi.",
            "Si je tombe, je ne tombe pas seul. Vous comprenez ?",
            "Je veux une immunité partielle. Après, je vous donne tout.",
            "On peut s'arranger. Hors procès-verbal.",
        ],
    },

    react_press = [
        "Vous appelez ça une preuve ? Faites-moi rire.",
        "J'ai vu des interrogatoires. Vous n'avez rien de solide.",
        "Continuez. J'ai toute la nuit.",
        "C'est du bluff de débutant.",
        "Vous avez un badge et des suppositions. C'est tout.",
    ],
    react_bluff_ok = [
        "Qui vous a donné ça ? Qui…",
        "Ce document ne devrait pas exister.",
        "D'accord. Je vois ce que vous avez. Je peux m'expliquer.",
        "Attendez. Attendez. D'où ça sort ?",
    ],
    react_bluff_no = [
        "Ce document est un faux. Je le saurais s'il existait.",
        "Essayez encore. Je connais les limites de votre dossier.",
        "Vous bluffez. Et je tiens.",
        "Je reconnais un bluff à trois kilomètres.",
    ],
    react_silence = [
        "Très spirituel.",
        "… Comme vous voulez.",
        "Le silence ne me dérange pas du tout.",
        "Prenez votre temps, inspecteur.",
        "Je peux attendre aussi longtemps que vous.",
    ],

    line_success = (
        "Vous voulez les noms ? Je vous donne les noms. "
        "Mais je parle uniquement au procureur. "
        "Et Ferrière a des conditions."
    ),
    line_failure = (
        "Entretien terminé. "
        "Parlez à mon avocat. "
        "Et bonne chance avec votre carrière après ça."
    ),
)


SUSPECTS: dict[str, SuspectProfile] = {
    "taro":     TARO,
    "ferriere": FERRIERE,
}


# ══════════════════════════════════════════════════════════════════════════════
# Mini-jeu principal
# ══════════════════════════════════════════════════════════════════════════════

class InterrogationMinigame:
    """
    Mini-jeu d'interrogatoire complet.

    Paramètres
    ----------
    screen     : pygame.Surface  — surface principale du jeu
    assets     : Assets          — gestionnaire d'assets (pour polices et sprites)
    suspect_id : str             — "taro" ou "ferriere"
    time_limit : float           — durée en secondes (défaut : 90)
    on_success : Callable | None — appelé quand le suspect craque
    on_failure : Callable | None — appelé quand le timer s'épuise
    """

    def __init__(
        self,
        screen:     pygame.Surface,
        assets,
        suspect_id: str = "taro",
        time_limit: float = 90.0,
        on_success: Optional[Callable] = None,
        on_failure: Optional[Callable] = None,
    ) -> None:
        if suspect_id not in SUSPECTS:
            raise ValueError(
                f"Suspect inconnu : '{suspect_id}'. "
                f"Valeurs disponibles : {list(SUSPECTS)}"
            )

        self.screen     = screen
        self.assets     = assets
        self.suspect    = SUSPECTS[suspect_id]
        self.time_left  = float(time_limit)
        self.time_max   = float(time_limit)
        self.on_success = on_success or (lambda: None)
        self.on_failure = on_failure or (lambda: None)

        # État du jeu
        self.pressure   = 0.0
        self.state      = SuspectState.DEFIANT
        self.actions    = _build_actions()

        # Dialogue
        self._line         = self._idle_line()
        self._line_timer   = 0.0
        self._line_delay   = 4.5   # secondes entre rotations de dialogue idle

        # Feedbacks et effets visuels
        self._feedbacks: list[_Feedback] = []
        self._flash: Optional[_ScreenFlash] = None
        self._pressure_pulse = 0.0   # valeur 0-1 pour l'animation de la jauge

        # Fin de jeu
        self._result: Optional[str] = None
        self._end_timer = _END_HOLD

        # Tension : légère vibration du portrait quand la pression monte
        self._portrait_shake   = 0.0
        self._portrait_shake_t = 0.0

        # Initialisation des polices
        self._font_title = getattr(assets, "font_title", None) or \
                           pygame.font.SysFont("monospace", 28, bold=True)
        self._font_big   = getattr(assets, "font_big",   None) or \
                           pygame.font.SysFont("monospace", 22, bold=True)
        self._font_med   = getattr(assets, "font_med",   None) or \
                           pygame.font.SysFont("monospace", 16)
        self._font_small = getattr(assets, "font_small", None) or \
                           pygame.font.SysFont("monospace", 12)

        # Cache du fond
        self._bg = getattr(assets, "bg", {}).get("salle_interrogatoire", None)

        # Calcul des zones et boutons
        self._layout: dict[str, pygame.Rect] = {}
        self._btn_rects: list[pygame.Rect]   = []
        self._compute_layout()

    # ──────────────────────────────────────────────────────────────────────────
    # Layout
    # ──────────────────────────────────────────────────────────────────────────

    def _compute_layout(self) -> None:
        W, H = SCREEN_W, SCREEN_H

        self._layout["header"] = pygame.Rect(0, 0, W, 46)

        # Zone portrait (gauche)
        self._layout["portrait"] = pygame.Rect(12, 52, 288, 320)

        # Barre de pression (haut droite)
        self._layout["pressure"] = pygame.Rect(315, 64, 580, 22)

        # Horloge timer (cercle centré)
        self._timer_center = (880, 148)
        self._timer_radius = 52

        # Zone d'info suspect (sous portrait)
        self._layout["state_badge"] = pygame.Rect(12, 378, 288, 30)

        # Boîte de dialogue
        self._layout["dialogue"] = pygame.Rect(12, 415, W - 24, 62)

        # Boutons d'action
        BTN_W, BTN_H = 198, 58
        GAP          = 22
        total_w      = 3 * BTN_W + 2 * GAP
        bx           = (W - total_w) // 2
        by           = H - BTN_H - 8
        self._btn_rects = [
            pygame.Rect(bx + i * (BTN_W + GAP), by, BTN_W, BTN_H)
            for i in range(3)
        ]

        # Hint clavier (au-dessus des boutons)
        self._hint_y = by - 18

    # ──────────────────────────────────────────────────────────────────────────
    # Dialogue helpers
    # ──────────────────────────────────────────────────────────────────────────

    def _idle_line(self) -> str:
        label = _STATE_META[self.state][0]
        lines = self.suspect.idle.get(label, ["…"])
        return random.choice(lines)

    def _set_line(self, text: str) -> None:
        self._line       = text
        self._line_timer = 0.0   # réinitialise le timer idle

    # ──────────────────────────────────────────────────────────────────────────
    # Résolution des actions
    # ──────────────────────────────────────────────────────────────────────────

    def _do_press(self) -> _Feedback:
        base  = random.uniform(0.10, 0.18)
        # Ferrière DÉFIANT résiste davantage
        if self.state == SuspectState.DEFIANT and self.suspect.resistance > 0.6:
            base *= 0.65
        delta = base * self.suspect.press_mult
        self.pressure = min(1.0, self.pressure + delta)
        self.time_left = max(0.0, self.time_left - _COST_PRESS)
        self._start_shake(0.6)
        self._flash = _ScreenFlash(RED_ACCENT)
        return _Feedback(
            random.choice(self.suspect.react_press),
            (255, 190, 190), positive=True,
        )

    def _do_bluff(self) -> _Feedback:
        success = random.random() < self.suspect.bluff_p
        self.time_left = max(0.0, self.time_left - _COST_BLUFF)
        if success:
            delta = random.uniform(0.15, 0.22) * self.suspect.bluff_mult
            self.pressure = min(1.0, self.pressure + delta)
            self._flash = _ScreenFlash(GOLD)
            self._start_shake(1.0)
            return _Feedback(
                random.choice(self.suspect.react_bluff_ok),
                (200, 255, 140), positive=True,
            )
        else:
            penalty = random.uniform(0.04, 0.09)
            self.pressure = max(0.0, self.pressure - penalty)
            self._flash = _ScreenFlash(PINK_ACCENT)
            return _Feedback(
                random.choice(self.suspect.react_bluff_no),
                (255, 140, 100), positive=False,
            )

    def _do_silence(self) -> _Feedback:
        base  = random.uniform(0.03, 0.07) * self.suspect.silence_mult
        self.pressure = min(1.0, self.pressure + base)
        self.time_left = max(0.0, self.time_left - _COST_SILENCE)
        return _Feedback(
            random.choice(self.suspect.react_silence),
            (150, 220, 255), positive=True,
        )

    def _trigger(self, idx: int) -> None:
        if self._result is not None:
            return
        slot = self.actions[idx]
        if not slot.ready:
            return
        slot.trigger()

        handlers = (self._do_press, self._do_bluff, self._do_silence)
        fb = handlers[idx]()

        self._feedbacks.append(fb)
        self._set_line(fb.text)

    def _start_shake(self, intensity: float) -> None:
        self._portrait_shake   = intensity * 5.0
        self._portrait_shake_t = 0.0

    # ──────────────────────────────────────────────────────────────────────────
    # Update
    # ──────────────────────────────────────────────────────────────────────────

    def update(
        self,
        dt: float,
        events: list[pygame.event.Event],
    ) -> Optional[Literal["success", "failure"]]:
        """
        Logique principale.
        Retourne "success", "failure", ou None (jeu en cours).
        """
        # ── Phase de fin ──────────────────────────────────────────────────
        if self._result is not None:
            self._end_timer -= dt
            if self._end_timer <= 0.0:
                return self._result
            return None

        # ── Timer ─────────────────────────────────────────────────────────
        self.time_left = max(0.0, self.time_left - dt)

        # ── Décroissance passive pression ─────────────────────────────────
        self.pressure = max(0.0, self.pressure - PRESSURE_DECAY * dt)

        # ── Cooldowns ─────────────────────────────────────────────────────
        for slot in self.actions:
            slot.tick(dt)

        # ── Feedbacks / effets ────────────────────────────────────────────
        self._feedbacks = [f for f in self._feedbacks if f.alive]
        for f in self._feedbacks:
            f.tick(dt)

        if self._flash and self._flash.alive:
            self._flash.tick(dt)

        # ── Shake portrait ────────────────────────────────────────────────
        if self._portrait_shake > 0:
            self._portrait_shake_t += dt * 30
            self._portrait_shake = max(0.0, self._portrait_shake - dt * 8)

        # ── Pulse jauge ───────────────────────────────────────────────────
        self._pressure_pulse = (self._pressure_pulse + dt * 3) % (2 * math.pi)

        # ── Rotation ligne idle ───────────────────────────────────────────
        self._line_timer += dt
        if self._line_timer >= self._line_delay:
            self._line_timer = 0.0
            self._line       = self._idle_line()

        # ── État du suspect ───────────────────────────────────────────────
        self.state = _state_from(self.pressure)

        # ── Vérification victoire ─────────────────────────────────────────
        if self.pressure >= PRESSURE_WIN:
            self._result   = "success"
            self._end_timer = _END_HOLD
            self._set_line(self.suspect.line_success)
            self._flash = _ScreenFlash((50, 230, 110))
            return None

        # ── Vérification défaite ──────────────────────────────────────────
        if self.time_left <= 0.0:
            self._result   = "failure"
            self._end_timer = _END_HOLD
            self._set_line(self.suspect.line_failure)
            self._flash = _ScreenFlash(RED_ACCENT)
            return None

        # ── Événements clavier / souris ───────────────────────────────────
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                for i, slot in enumerate(self.actions):
                    if ev.key in (slot.key, slot.key_alt):
                        self._trigger(i)
                        break
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for i, rect in enumerate(self._btn_rects):
                    if rect.collidepoint(ev.pos):
                        self._trigger(i)
                        break

        return None

    # ──────────────────────────────────────────────────────────────────────────
    # Draw — dispatcher
    # ──────────────────────────────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface) -> None:
        self._draw_background(surface)
        self._draw_header(surface)
        self._draw_portrait(surface)
        self._draw_state_badge(surface)
        self._draw_pressure_bar(surface)
        self._draw_timer(surface)
        self._draw_stat_details(surface)
        self._draw_dialogue(surface)
        self._draw_hint(surface)
        self._draw_buttons(surface)
        self._draw_feedbacks(surface)
        if self._flash and self._flash.alive:
            self._draw_flash(surface)
        if self._result is not None:
            self._draw_end_screen(surface)

    # ──────────────────────────────────────────────────────────────────────────
    # Draw helpers
    # ──────────────────────────────────────────────────────────────────────────

    def _draw_background(self, surf: pygame.Surface) -> None:
        if self._bg:
            surf.blit(self._bg, (0, 0))
        else:
            surf.fill((10, 12, 24))

        # Voile sombre (pour lisibilité de l'UI)
        dark = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        dark.fill((0, 0, 10, 170))
        surf.blit(dark, (0, 0))

        # Vignette
        for i in range(6):
            r = SCREEN_W // 2 - i * 60
            if r <= 0:
                break
            a = i * 8
            vig = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            pygame.draw.ellipse(vig, (0, 0, 0, a),
                                pygame.Rect(SCREEN_W // 2 - r,
                                            SCREEN_H // 2 - r // 2,
                                            r * 2, r))
            surf.blit(vig, (0, 0))

    def _draw_header(self, surf: pygame.Surface) -> None:
        bar = pygame.Surface((SCREEN_W, 46), pygame.SRCALPHA)
        bar.fill((4, 6, 18, 240))
        surf.blit(bar, (0, 0))
        pygame.draw.line(surf, CYAN, (0, 46), (SCREEN_W, 46), 1)

        # Titre centré
        title_str = f"INTERROGATOIRE — {self.suspect.name.upper()}"
        title_s   = self._font_title.render(title_str, True, CYAN)
        surf.blit(title_s,
                  (SCREEN_W // 2 - title_s.get_width() // 2, 8))

        # Rôle (droite)
        role_s = self._font_small.render(self.suspect.role, True, TEXT_GRAY)
        surf.blit(role_s, (SCREEN_W - role_s.get_width() - _PAD, 16))

    def _draw_portrait(self, surf: pygame.Surface) -> None:
        rect = self._layout["portrait"]
        state_label, state_col = _STATE_META[self.state]
        expr_idx = self.suspect.expr.get(state_label, 0)

        # Shake offset
        shake_x = 0
        if self._portrait_shake > 0:
            shake_x = int(math.sin(self._portrait_shake_t) * self._portrait_shake)

        sprite = None
        try:
            sprite = self.assets.get_char(self.suspect.id, expr_idx)
        except Exception:
            pass

        if sprite:
            sw, sh = sprite.get_size()
            scale  = min(rect.w / sw, rect.h / sh, 1.0)
            nw, nh = int(sw * scale), int(sh * scale)
            scaled = pygame.transform.smoothscale(sprite, (nw, nh))
            bx = rect.x + (rect.w - nw) // 2 + shake_x
            by = rect.y + rect.h - nh
            surf.blit(scaled, (bx, by))
        else:
            # Placeholder si le sprite est absent
            ph = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            ph.fill((*state_col, 25))
            pygame.draw.rect(ph, state_col, ph.get_rect(), 2, border_radius=8)
            surf.blit(ph, (rect.x + shake_x, rect.y))
            n_s = self._font_med.render(self.suspect.name, True, state_col)
            surf.blit(n_s, (
                rect.x + shake_x + rect.w // 2 - n_s.get_width() // 2,
                rect.y + rect.h // 2,
            ))

        # Bordure lumineuse dont l'intensité suit la pression
        glow_a = int(60 + 80 * self.pressure)
        pygame.draw.rect(surf, (*state_col, glow_a),
                         rect.inflate(4, 4), 2, border_radius=6)

    def _draw_state_badge(self, surf: pygame.Surface) -> None:
        rect  = self._layout["state_badge"]
        label, col = _STATE_META[self.state]

        badge = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        badge.fill((*col, 55))
        surf.blit(badge, rect.topleft)
        pygame.draw.rect(surf, col, rect, 1)

        lbl_s = self._font_med.render(label, True, col)
        surf.blit(lbl_s, (
            rect.x + rect.w // 2 - lbl_s.get_width() // 2,
            rect.y + (rect.h - lbl_s.get_height()) // 2,
        ))

    def _draw_pressure_bar(self, surf: pygame.Surface) -> None:
        rect = self._layout["pressure"]

        # Label au-dessus
        pct   = int(self.pressure * 100)
        label = self._font_small.render(
            f"PRESSION PSYCHOLOGIQUE  {pct} %", True, TEXT_NAME
        )
        surf.blit(label, (rect.x, rect.y - 18))

        # Fond
        bg = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        bg.fill((18, 20, 38, 210))
        surf.blit(bg, rect.topleft)
        pygame.draw.rect(surf, (55, 65, 105), rect, 1)

        # Remplissage (dégradé bleu → vert → orange → rouge)
        fill_w = int(rect.w * self.pressure)
        if fill_w > 0:
            fill = pygame.Surface((fill_w, rect.h), pygame.SRCALPHA)
            for i in range(fill_w):
                t = i / rect.w
                if t < 0.50:
                    # bleu → cyan
                    r = int(40  + 20  * t * 2)
                    g = int(80  + 140 * t * 2)
                    b = 220
                elif t < 0.70:
                    # cyan → vert
                    f = (t - 0.50) / 0.20
                    r = int(60  + 160 * f)
                    g = 220
                    b = int(220 - 160 * f)
                elif t < 0.85:
                    # vert → orange
                    f = (t - 0.70) / 0.15
                    r = int(220 + 35  * f)
                    g = int(220 - 100 * f)
                    b = int(60  - 40  * f)
                else:
                    # orange → rouge
                    f = (t - 0.85) / 0.15
                    r = 255
                    g = int(120 - 120 * f)
                    b = max(0, int(20 - 20 * f))
                pygame.draw.line(fill, (r, g, b, 235), (i, 0), (i, rect.h - 1))
            surf.blit(fill, rect.topleft)

        # Effet de pulse sur le bord droit de la barre (si pression > 0)
        if self.pressure > 0.05:
            pulse_a = int(80 + 60 * math.sin(self._pressure_pulse))
            pw      = min(4, fill_w)
            if pw > 0:
                pulse_r = pygame.Rect(rect.x + fill_w - pw, rect.y, pw, rect.h)
                ps      = pygame.Surface((pw, rect.h), pygame.SRCALPHA)
                ps.fill((255, 255, 255, pulse_a))
                surf.blit(ps, pulse_r.topleft)

        # Marqueurs de seuil
        for threshold in _BAR_MARKERS:
            mx = rect.x + int(rect.w * threshold)
            pygame.draw.line(surf, (160, 165, 210),
                             (mx, rect.y - 5), (mx, rect.y + rect.h + 5), 1)

        # Prochain seuil
        if self._result is None:
            next_t = next((t for t in _BAR_MARKERS if t > self.pressure), None)
            if next_t is not None:
                nxt_s = self._font_small.render(
                    f"seuil suivant : {int(next_t * 100)} %", True, TEXT_GRAY
                )
                surf.blit(nxt_s, (rect.right - nxt_s.get_width(), rect.y - 18))

    def _draw_timer(self, surf: pygame.Surface) -> None:
        cx, cy = self._timer_center
        R      = self._timer_radius
        Ri     = R - 14

        frac = self.time_left / self.time_max if self.time_max > 0 else 0.0

        # Couleur du timer selon urgence
        if frac > 0.50:
            col = (210, 225, 255)
        elif frac > 0.25:
            col = GOLD
        else:
            # Clignotement rouge en urgence
            blink = int(220 + 35 * math.sin(pygame.time.get_ticks() / 200))
            col   = (blink, 40, 40)

        # Fond du cercle
        pygame.draw.circle(surf, (22, 24, 44), (cx, cy), R)

        # Arc de progression
        if frac > 0.0:
            steps = max(6, int(50 * frac))
            a0    = -math.pi / 2
            a1    = a0 + 2 * math.pi * frac
            pts   = [(cx, cy)]
            for i in range(steps + 1):
                a = a0 + (a1 - a0) * i / steps
                pts.append((
                    cx + R * math.cos(a),
                    cy + R * math.sin(a),
                ))
            if len(pts) >= 3:
                pygame.draw.polygon(surf, col, pts)
        pygame.draw.circle(surf, (8, 10, 22), (cx, cy), Ri)

        # Bord
        pygame.draw.circle(surf, col, (cx, cy), R, 2)

        # Texte MM:SS
        secs  = int(self.time_left)
        m, s  = divmod(secs, 60)
        t_str = f"{m:02d}:{s:02d}"
        t_s   = self._font_big.render(t_str, True, col)
        surf.blit(t_s, (cx - t_s.get_width() // 2,
                        cy - t_s.get_height() // 2))

        # Label "TEMPS"
        lbl = self._font_small.render("TEMPS", True, TEXT_GRAY)
        surf.blit(lbl, (cx - lbl.get_width() // 2, cy + R + 4))

    def _draw_stat_details(self, surf: pygame.Surface) -> None:
        """Infos rapides à droite : multiplicateurs d'action."""
        x, y = 315, 100
        lines = [
            (f"PRESS   ×{self.suspect.press_mult:.1f}",   RED_ACCENT),
            (f"BLUFF   ×{self.suspect.bluff_mult:.1f}",   GOLD),
            (f"SILENCE ×{self.suspect.silence_mult:.1f}", CYAN),
        ]
        for label, col in lines:
            ls = self._font_small.render(label, True, col)
            surf.blit(ls, (x, y))
            y += 18

    def _draw_dialogue(self, surf: pygame.Surface) -> None:
        rect = self._layout["dialogue"]

        box = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        box.fill((6, 8, 20, 215))
        surf.blit(box, rect.topleft)
        pygame.draw.rect(surf, CYAN_DIM, rect, 1)

        # Nom du suspect
        name_s = self._font_small.render(
            f"[ {self.suspect.name.upper()} ]", True, TEXT_NAME
        )
        surf.blit(name_s, (rect.x + 10, rect.y + 7))

        # Texte enveloppé sur 2 lignes
        max_w = rect.w - 145
        words = self._line.split()
        lines_out: list[str] = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if self._font_med.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines_out.append(cur)
                cur = w
        if cur:
            lines_out.append(cur)

        for i, ln in enumerate(lines_out[:2]):
            ls = self._font_med.render(ln, True, TEXT_MAIN)
            surf.blit(ls, (rect.x + 135, rect.y + 10 + i * 22))

    def _draw_hint(self, surf: pygame.Surface) -> None:
        hint = self._font_small.render(
            "[A] Press    [Z] Bluff    [E] Silence", True, TEXT_GRAY
        )
        surf.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, self._hint_y))

    def _draw_buttons(self, surf: pygame.Surface) -> None:
        for slot, rect in zip(self.actions, self._btn_rects):
            col    = slot.color
            dim_a  = 110 if not slot.ready else 255
            dim_col = tuple(min(255, int(c * dim_a / 255)) for c in col[:3])

            # Fond du bouton
            btn_bg = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            bg_a   = 35 if slot.ready else 18
            btn_bg.fill((*col[:3], bg_a))
            surf.blit(btn_bg, rect.topleft)

            # Bordure
            border_col = col if slot.ready else (70, 75, 90)
            pygame.draw.rect(surf, border_col, rect, 2, border_radius=6)

            # Touche
            key_char = {"press": "A", "bluff": "Z", "silence": "E"}[slot.name]
            key_s = self._font_small.render(f"[{key_char}]", True,
                                            (*dim_col, dim_a))
            surf.blit(key_s, (rect.x + 8, rect.y + 8))

            # Nom de l'action (centré)
            name_s = self._font_med.render(slot.label, True,
                                           (*dim_col, dim_a))
            surf.blit(name_s, (
                rect.x + rect.w // 2 - name_s.get_width() // 2,
                rect.y + 8,
            ))

            # Description
            desc_s = self._font_small.render(
                slot.desc[:28], True, (*TEXT_GRAY[:3], dim_a)
            )
            surf.blit(desc_s, (
                rect.x + rect.w // 2 - desc_s.get_width() // 2,
                rect.y + rect.h - 20,
            ))

            # Arc de cooldown (coin supérieur droit)
            if not slot.ready:
                acx = rect.right - 16
                acy = rect.y + 16
                ar  = 12
                pygame.draw.circle(surf, (35, 38, 58), (acx, acy), ar)

                ready_frac = 1.0 - slot.cd_frac
                if ready_frac > 0:
                    a0  = -math.pi / 2
                    a1  = a0 + 2 * math.pi * ready_frac
                    stp = max(4, int(16 * ready_frac))
                    pts = [(acx, acy)]
                    for j in range(stp + 1):
                        a = a0 + (a1 - a0) * j / stp
                        pts.append((acx + ar * math.cos(a),
                                    acy + ar * math.sin(a)))
                    if len(pts) >= 3:
                        pygame.draw.polygon(surf, col, pts)
                pygame.draw.circle(surf, (8, 10, 22), (acx, acy), ar - 5)

                cd_s = self._font_small.render(
                    f"{slot.cd_remain:.0f}", True, col
                )
                surf.blit(cd_s, (acx - cd_s.get_width() // 2,
                                  acy - cd_s.get_height() // 2))

    def _draw_feedbacks(self, surf: pygame.Surface) -> None:
        visible = self._feedbacks[-3:]
        base_y  = self._layout["dialogue"].y - 8
        for i, fb in enumerate(reversed(visible)):
            col = (*fb.color[:3], fb.alpha)
            s   = self._font_small.render(fb.text[:62], True, col)
            x   = SCREEN_W // 2 - s.get_width() // 2
            y   = base_y - i * 20
            surf.blit(s, (x, y))

    def _draw_flash(self, surf: pygame.Surface) -> None:
        fl = self._flash
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((*fl.color[:3], fl.alpha))
        surf.blit(overlay, (0, 0))

    def _draw_end_screen(self, surf: pygame.Surface) -> None:
        success = self._result == "success"
        col     = (50, 230, 110) if success else (220, 50, 50)
        title   = "SUSPECT CRAQUÉ" if success else "INTERROGATOIRE ÉCHOUÉ"
        line    = self.suspect.line_success if success else self.suspect.line_failure

        # Fond semi-transparent
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((*col, 120))
        surf.blit(overlay, (0, 0))

        # Cadre central
        BW, BH = 720, 210
        BX, BY = SCREEN_W // 2 - BW // 2, SCREEN_H // 2 - BH // 2
        box = pygame.Surface((BW, BH), pygame.SRCALPHA)
        box.fill((4, 6, 18, 235))
        surf.blit(box, (BX, BY))
        pygame.draw.rect(surf, col,
                         pygame.Rect(BX, BY, BW, BH), 2, border_radius=10)

        # Titre
        title_s = self._font_title.render(title, True, col)
        surf.blit(title_s, (
            SCREEN_W // 2 - title_s.get_width() // 2, BY + 18
        ))

        # Ligne finale (enveloppée)
        words = line.split()
        lines_out: list[str] = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if self._font_med.size(test)[0] < BW - 40:
                cur = test
            else:
                lines_out.append(cur)
                cur = w
        if cur:
            lines_out.append(cur)

        for i, ln in enumerate(lines_out[:3]):
            ls = self._font_med.render(ln, True, TEXT_MAIN)
            surf.blit(ls, (
                SCREEN_W // 2 - ls.get_width() // 2,
                BY + 72 + i * 26,
            ))

        # Compte à rebours avant transition
        ct  = max(1, int(self._end_timer) + 1)
        ct_s = self._font_small.render(
            f"transition dans {ct}s…", True, TEXT_GRAY
        )
        surf.blit(ct_s, (
            SCREEN_W // 2 - ct_s.get_width() // 2,
            BY + BH - 26,
        ))


# ══════════════════════════════════════════════════════════════════════════════
# Utilitaire : résumé console (debug / tests)
# ══════════════════════════════════════════════════════════════════════════════

def print_suspect_summary(suspect_id: str) -> None:
    """Affiche les stats du suspect en console pour le game design."""
    p = SUSPECTS[suspect_id]
    w = 60
    print("=" * w)
    print(f" {p.name}  ({p.role})")
    print("-" * w)
    print(f"  Résistance   : {p.resistance:.2f}")
    print(f"  Press  ×{p.press_mult:.2f}  |  Bluff ×{p.bluff_mult:.2f} (p={p.bluff_p:.0%})"
          f"  |  Silence ×{p.silence_mult:.2f}")
    print("-" * w)
    print("  Seuils de changement d'état :")
    for state, (label, col) in _STATE_META.items():
        t_map = {
            SuspectState.DEFIANT:   " 0 – 24 %",
            SuspectState.RESISTANT: "25 – 49 %",
            SuspectState.NERVOUS:   "50 – 69 %",
            SuspectState.CRACKING:  "70 – 84 %",
            SuspectState.BREAKING:  "85 – 99 %",
        }
        print(f"    {label:<12} {t_map[state]}")
    print("=" * w)


if __name__ == "__main__":
    # Résumé en console si exécuté directement
    for sid in SUSPECTS:
        print_suspect_summary(sid)
        print()
