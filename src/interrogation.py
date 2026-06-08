"""
interrogation.py — Mini-jeu d'interrogatoire v2
================================================

Nouveautés v2 :
  • Decay suspendu quand pression ≥ 95 % (victoire accessible)
  • evidence_hints : preuves contextuelles → boutons supplémentaires en jeu
  • Mode contre-interrogatoire : le suspect pose des questions, le joueur choisit
    Vrai / Mensonge / Silence — avec conséquences sur la pression et le timer
  • Layout dynamique : les boutons d'indices s'ajoutent au-dessus des boutons std

Suspects disponibles :
    taro | ferriere | natasha | mira | ghost | architect | senator

Intégration script.py (inchangée) :
    {
        "type":       "interrogation",
        "suspect":    "ferriere",
        "time_limit": 90,
        "on_success": "sc_confesse",
        "on_failure": "sc_echappe",
    }

Intégration main.py — passer les preuves collectées :
    self.interro = InterrogationMinigame(
        ...,
        collected_evidence = [name for name, _ in self.evidence.items],
    )
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

PRESSURE_WIN          = 1.0
PRESSURE_DECAY        = 0.0012   # décroissance passive par seconde
PRESSURE_DECAY_CUTOFF = 0.95     # ≥ ce seuil → decay suspendu (victoire accessible)
_PAD                  = 14

_COST_PRESS   = 8.0
_COST_BLUFF   = 5.0
_COST_SILENCE = 2.0
_COST_EVIDENCE = 4.0   # coût timer pour un bouton preuve contextuelle

_END_HOLD = 3.2

_BAR_MARKERS = (0.25, 0.50, 0.70, 0.85, 0.95)

# Contre-interrogatoire
_COUNTER_INTERVAL_MIN = 18.0   # délai min avant qu'une question surgisse
_COUNTER_INTERVAL_MAX = 35.0   # délai max

PINK_EVIDENCE = (180, 80, 255)   # couleur des boutons preuves contextuelles

# ══════════════════════════════════════════════════════════════════════════════
# État du suspect
# ══════════════════════════════════════════════════════════════════════════════

class SuspectState(Enum):
    DEFIANT   = 0
    RESISTANT = 1
    NERVOUS   = 2
    CRACKING  = 3
    BREAKING  = 4


def _state_from(p: float) -> SuspectState:
    if p >= 0.85: return SuspectState.BREAKING
    if p >= 0.70: return SuspectState.CRACKING
    if p >= 0.50: return SuspectState.NERVOUS
    if p >= 0.25: return SuspectState.RESISTANT
    return SuspectState.DEFIANT


_STATE_META: dict[SuspectState, tuple[str, tuple]] = {
    SuspectState.DEFIANT:   ("DÉFIANT",   (210,  55,  55)),
    SuspectState.RESISTANT: ("RÉSISTANT", (215, 105,  35)),
    SuspectState.NERVOUS:   ("NERVEUX",   (200, 175,  40)),
    SuspectState.CRACKING:  ("FISSURÉ",   (120, 210,  70)),
    SuspectState.BREAKING:  ("CRAQUANT",  ( 50, 230, 110)),
}

# ══════════════════════════════════════════════════════════════════════════════
# Slot d'action standard
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class _ActionSlot:
    name:     str
    label:    str
    desc:     str
    color:    tuple
    key:      int
    key_alt:  int
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
        return self._cd / self.cooldown if self.cooldown > 0 else 0.0

    @property
    def cd_remain(self) -> float:
        return self._cd


def _build_actions() -> list[_ActionSlot]:
    return [
        _ActionSlot("press",   "PRESS",   "Confronter avec une preuve",
                    RED_ACCENT, pygame.K_a, pygame.K_1, 3.0),
        _ActionSlot("bluff",   "BLUFF",   "Prétendre avoir un document",
                    GOLD,       pygame.K_z, pygame.K_2, 5.0),
        _ActionSlot("silence", "SILENCE", "Laisser le suspect se décomposer",
                    CYAN,       pygame.K_e, pygame.K_3, 0.8),
    ]

# ══════════════════════════════════════════════════════════════════════════════
# Slot de preuve contextuelle
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class _EvidenceSlot:
    evidence_name: str          # nom de la preuve (doit être dans evidence_hints)
    label:         str          # label court affiché sur le bouton
    multiplier:    float        # bonus multiplicateur de pression
    reaction:      str          # réplique du suspect
    key:           int          # touche (pygame.K_1 … pygame.K_5 selon position)
    used:          bool = False  # chaque preuve ne peut être utilisée qu'une fois
    _cd:           float = field(default=0.0, init=False)
    cooldown:      float = 12.0

    @property
    def ready(self) -> bool:
        return not self.used and self._cd <= 0.0

    def tick(self, dt: float) -> None:
        self._cd = max(0.0, self._cd - dt)

    def trigger(self) -> None:
        self.used = True   # usage unique

# ══════════════════════════════════════════════════════════════════════════════
# Contre-interrogatoire : question du suspect
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class _CounterQuestion:
    """Une question posée par le suspect qui force le joueur à répondre."""
    question:      str
    answer_true:   str    # réponse honnête → petit bonus pression, pas de pénalité timer
    answer_lie:    str    # réponse mensongère → fort bonus si cru, grosse pénalité si détecté
    answer_silence: str   # silence → bonus moyen, pas de timer
    # Conséquences sur la pression selon réponse
    delta_true:    float = 0.06
    delta_lie_ok:  float = 0.14   # si le mensonge passe
    delta_lie_fail: float = -0.10  # si le suspect détecte le mensonge
    delta_silence: float = 0.04
    lie_detect_p:  float = 0.40   # probabilité que le suspect détecte le mensonge


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
    resistance:   float = 0.5
    press_mult:   float = 1.0
    bluff_mult:   float = 1.0
    silence_mult: float = 1.0
    bluff_p:      float = 0.55

    # Sprites par état
    expr: dict[str, int] = field(default_factory=dict)
    # Dialogues idle par état
    idle: dict[str, list[str]] = field(default_factory=dict)
    # Réactions aux actions standard
    react_press:    list[str] = field(default_factory=list)
    react_bluff_ok: list[str] = field(default_factory=list)
    react_bluff_no: list[str] = field(default_factory=list)
    react_silence:  list[str] = field(default_factory=list)
    line_success: str = ""
    line_failure: str = ""

    # ── NOUVEAU v2 ────────────────────────────────────────────────────────────
    # Preuves contextuelles : nom_preuve → (label_bouton, multiplicateur, réplique_suspect)
    evidence_hints: dict[str, tuple[str, float, str]] = field(default_factory=dict)
    # Questions de contre-interrogatoire (le suspect interroge le joueur)
    counter_questions: list[_CounterQuestion] = field(default_factory=list)


# ══════════════════════════════════════════════════════════════════════════════
# Profil : Taro Mitsuki
# ══════════════════════════════════════════════════════════════════════════════

TARO = SuspectProfile(
    id         = "taro",
    name       = "Taro Mitsuki",
    role       = "Informateur — Synarchie",
    resistance   = 0.45,
    press_mult   = 1.20,
    bluff_mult   = 0.80,
    silence_mult = 1.45,
    bluff_p      = 0.42,
    expr = {
        "DÉFIANT": 1, "RÉSISTANT": 1,
        "NERVEUX": 3, "FISSURÉ": 3, "CRAQUANT": 3,
    },
    idle = {
        "DÉFIANT":   ["Je n'ai rien à vous dire.", "Vous perdez votre temps.",
                      "Appelez mon avocat.", "Je ne connais pas ce Vane."],
        "RÉSISTANT": ["Ce que vous pensez savoir… c'est rien.",
                      "Je suis une simple connaissance de Vane.",
                      "Ces gens-là, si vous les cherchez, vous les trouvez.",
                      "Je veux une garantie avant de parler."],
        "NERVEUX":   ["Attendez— je veux d'abord une garantie.",
                      "Vous réalisez à qui vous vous attaquez ?",
                      "Si je parle… ma famille…",
                      "Ces gens-là ne plaisantent pas avec les témoins."],
        "FISSURÉ":   ["L'enregistrement… comment vous l'avez eu ?",
                      "C'était pas censé se passer comme ça.",
                      "Ferrière m'a dit que Vane avait compris les règles…",
                      "J'ai juste transmis des messages. C'est tout."],
        "CRAQUANT":  ["D'accord. D'accord… écoutez-moi bien.",
                      "Le Loft 7, c'est Ferrière qui gère.",
                      "Il y a un registre. Genève. Tout y est.",
                      "Je vais tout vous dire — mais j'ai besoin d'une protection."],
    },
    react_press    = ["Vous avez rien — c'est du bluff !", "Ces preuves ne prouvent rien.",
                      "J'ai le droit de garder le silence.", "Vous m'impressionnez pas.",
                      "C'est des suppositions. Rien de concret."],
    react_bluff_ok = ["Comment… comment vous avez ce document ?",
                      "Ils m'avaient dit que ça resterait secret.",
                      "Très bien. On peut peut-être s'arranger.",
                      "Attendez— d'où ça sort, ça ?"],
    react_bluff_no = ["C'est faux. Je sais exactement ce que vous avez.",
                      "Vous inventez. Mauvais coup.", "Vous croyez que je suis naïf ?",
                      "J'ai fait ce métier. Je reconnais un bluff."],
    react_silence  = ["Pourquoi vous me regardez comme ça ?", "… Dites quelque chose.",
                      "Ce silence… c'est une tactique, hein.",
                      "Arrêtez de me fixer. C'est déstabilisant.", "C'est quoi ce jeu ?"],
    line_success = ("D'accord… d'accord. Je vais tout vous dire. "
                    "Ferrière, le Loft 7, Genève — tout. "
                    "Mais je veux une protection pour ma famille."),
    line_failure = ("Mon avocat arrive dans dix minutes. "
                    "Après ça, vous n'entendrez plus un seul mot de moi."),

    evidence_hints = {
        "Enregistrement Taro": ("Jouer l'enreg.", 1.80,
            "C'est ma voix… mais ce contexte est tronqué. Vous… vous l'avez vraiment ?"),
        "Photo du Fantôme":    ("Montrer la photo", 1.50,
            "Cette photo… je ne l'ai jamais vue. Qui vous l'a donnée ?"),
        "Dossier Vane":        ("Citer le dossier", 1.30,
            "Vane gardait ces notes ? Je croyais qu'il avait tout brûlé."),
    },
    counter_questions = [
        _CounterQuestion(
            question       = "Comment vous avez su pour le Loft 7 ?",
            answer_true    = "Par les dossiers de Vane.",
            answer_lie     = "Un informateur anonyme.",
            answer_silence = "…",
            delta_true     = 0.05, delta_lie_ok = 0.12, delta_lie_fail = -0.08,
            delta_silence  = 0.07, lie_detect_p = 0.35,
        ),
        _CounterQuestion(
            question       = "Vous travaillez seul ou avec la police ?",
            answer_true    = "Avec l'officier Sato.",
            answer_lie     = "Entièrement seul.",
            answer_silence = "Peu importe qui je suis.",
            delta_true     = 0.04, delta_lie_ok = 0.10, delta_lie_fail = -0.12,
            delta_silence  = 0.06, lie_detect_p = 0.45,
        ),
    ],
)


# ══════════════════════════════════════════════════════════════════════════════
# Profil : Capitaine Ferrière
# ══════════════════════════════════════════════════════════════════════════════

FERRIERE = SuspectProfile(
    id         = "ferriere",
    name       = "Capitaine Ferrière",
    role       = "Police — Agent Synarchie",
    resistance   = 0.72,
    press_mult   = 0.88,
    bluff_mult   = 1.35,
    silence_mult = 0.65,
    bluff_p      = 0.62,
    expr = {
        "DÉFIANT": 1, "RÉSISTANT": 1,
        "NERVEUX": 1, "FISSURÉ": 3, "CRAQUANT": 3,
    },
    idle = {
        "DÉFIANT":   ["Je suis flic depuis vingt-deux ans. Vous croyez me faire peur ?",
                      "Vous n'avez rien. Sinon, je serais en garde à vue.",
                      "Cette conversation est terminée.",
                      "J'ai vu des centaines d'interrogatoires. Celui-là m'impressionne pas."],
        "RÉSISTANT": ["Vane ? Je le croisais au boulot. Point.",
                      "Mes supérieurs sont au courant de cet entretien ?",
                      "Faites attention à ce que vous insinuez.",
                      "Vous jouez à quoi, exactement ?"],
        "NERVEUX":   ["Cette photo… c'est pas moi.",
                      "L'enregistrement peut être truqué. Facilement.",
                      "Je veux voir votre chef de service maintenant.",
                      "Vous réalisez ce que vous faites, là ?"],
        "FISSURÉ":   ["Où est-ce que vous avez trouvé ça ?",
                      "Ces chiffres ne prouvent rien hors contexte.",
                      "Vane a fait des erreurs. Moi, j'exécutais des ordres.",
                      "Quelqu'un vous a donné ça. Qui ?"],
        "CRAQUANT":  ["Très bien. Il y a des gens au-dessus de moi.",
                      "Si je tombe, je ne tombe pas seul. Vous comprenez ?",
                      "Je veux une immunité partielle. Après, je vous donne tout.",
                      "On peut s'arranger. Hors procès-verbal."],
    },
    react_press    = ["Vous appelez ça une preuve ? Faites-moi rire.",
                      "J'ai vu des interrogatoires. Vous n'avez rien de solide.",
                      "Continuez. J'ai toute la nuit.", "C'est du bluff de débutant.",
                      "Vous avez un badge et des suppositions. C'est tout."],
    react_bluff_ok = ["Qui vous a donné ça ? Qui…",
                      "Ce document ne devrait pas exister.",
                      "D'accord. Je vois ce que vous avez. Je peux m'expliquer.",
                      "Attendez. Attendez. D'où ça sort ?"],
    react_bluff_no = ["Ce document est un faux. Je le saurais s'il existait.",
                      "Essayez encore. Je connais les limites de votre dossier.",
                      "Vous bluffez. Et je tiens.",
                      "Je reconnais un bluff à trois kilomètres."],
    react_silence  = ["Très spirituel.", "… Comme vous voulez.",
                      "Le silence ne me dérange pas du tout.",
                      "Prenez votre temps, inspecteur.",
                      "Je peux attendre aussi longtemps que vous."],
    line_success = ("Vous voulez les noms ? Je vous donne les noms. "
                    "Mais je parle uniquement au procureur. "
                    "Et Ferrière a des conditions."),
    line_failure = ("Entretien terminé. Parlez à mon avocat. "
                    "Et bonne chance avec votre carrière après ça."),

    evidence_hints = {
        "Enregistrement Taro": ("Jouer l'enreg. Taro", 1.80,
            "Cette voix… Taro a parlé. Intéressant. Je pensais qu'il était plus prudent."),
        "Photo du Fantôme":    ("Montrer la photo", 1.50,
            "Ce badge… c'est le mien. Mais cette photo peut venir de n'importe où."),
        "Registre Offshore":   ("Citer le registre", 1.60,
            "Ces chiffres… d'où vous sortez ça ? Quelqu'un vous a fourni des données classifiées."),
        "Clé du Loft 7":       ("Montrer la clé", 1.70,
            "Cette clé… comment vous avez eu ça ? Elle ne devrait pas exister hors du réseau."),
    },
    counter_questions = [
        _CounterQuestion(
            question       = "Vous avez un mandat pour cet entretien ?",
            answer_true    = "Entretien informel. Vous êtes libre de partir.",
            answer_lie     = "Oui. Signé ce matin.",
            answer_silence = "La question n'est pas là.",
            delta_true     = 0.08, delta_lie_ok = 0.05, delta_lie_fail = -0.15,
            delta_silence  = 0.03, lie_detect_p = 0.70,
        ),
        _CounterQuestion(
            question       = "Qui d'autre est au courant de cette enquête ?",
            answer_true    = "L'officier Sato et deux journalistes.",
            answer_lie     = "Personne. C'est entièrement confidentiel.",
            answer_silence = "Plus de gens que vous ne le pensez.",
            delta_true     = 0.06, delta_lie_ok = 0.14, delta_lie_fail = -0.10,
            delta_silence  = 0.10, lie_detect_p = 0.40,
        ),
    ],
)


# ══════════════════════════════════════════════════════════════════════════════
# Profil : Natasha Mori
# ══════════════════════════════════════════════════════════════════════════════

NATASHA = SuspectProfile(
    id         = "natasha",
    name       = "Natasha Mori",
    role       = "Journaliste — Tribune International",
    resistance   = 0.38,
    press_mult   = 1.40,
    bluff_mult   = 0.70,
    silence_mult = 1.10,
    bluff_p      = 0.32,
    expr = {
        "DÉFIANT": 1, "RÉSISTANT": 1,
        "NERVEUX": 2, "FISSURÉ": 3, "CRAQUANT": 3,
    },
    idle = {
        "DÉFIANT":   ["Je protège mes sources. C'est constitutionnel.",
                      "Mon rédacteur en chef est au courant que je suis ici.",
                      "Vous perdez votre temps. Et le mien.",
                      "Je n'ai aucune obligation de vous parler."],
        "RÉSISTANT": ["Ce que vous me montrez ne me surprend pas autant que vous le croyez.",
                      "J'ai travaillé deux ans sur cette histoire.",
                      "Raven. Qu'est-ce que vous voulez vraiment ?",
                      "Je suis journaliste. Je pose les questions, normalement."],
        "NERVEUX":   ["D'accord. Il y a des choses que je n'ai pas publiées. Encore.",
                      "Ce contact… je ne savais pas qui il était vraiment.",
                      "Si c'est vrai ce que vous dites, alors moi aussi j'ai été manipulée.",
                      "Combien de temps vous me demandez de garder ça ?"],
        "FISSURÉ":   ["Il m'a contactée il y a six mois. Il connaissait des détails impossibles.",
                      "Je n'ai pas vérifié assez. C'est ma faute professionnelle.",
                      "Il y a un document. Je l'ai. Mais je voulais le publier moi-même.",
                      "Si je vous le donne, vous me garantissez quoi en échange ?"],
        "CRAQUANT":  ["Très bien. Je vais tout vous montrer. Mais on partage l'exclusivité.",
                      "Le serveur miroir. J'ai l'adresse. Et la clé d'accès.",
                      "Je savais que cette affaire était trop grosse pour une seule personne.",
                      "On travaille ensemble ou on ne travaille pas."],
    },
    react_press    = ["Cette preuve… elle est solide. Je dois l'admettre.",
                      "D'où vous sortez ça ? Ce n'est pas dans mes dossiers.",
                      "C'est du bon travail. Je peux pas le nier.",
                      "Vous avez fait vos devoirs. Mieux que je ne le pensais.",
                      "Ça, c'est vérifiable. Je vais devoir revoir ma position."],
    react_bluff_ok = ["Attendez… ce document existe vraiment ?",
                      "Je croyais l'avoir. Il m'a échappé ?",
                      "C'est cohérent avec ce que j'ai. Je vous crois.",
                      "Vous bluffez peut-être. Mais la conclusion est juste."],
    react_bluff_no = ["Non. Ce document n'existe pas. J'aurais su.",
                      "Essayez autre chose. Je connais chaque source sur cette affaire.",
                      "Mauvais bluff, Raven. Même pour un détective.",
                      "Je suis journaliste. Les fausses pistes, c'est mon quotidien."],
    react_silence  = ["… Vous attendez quoi ? Que je parle en premier ?",
                      "D'accord. Le silence. Classique.",
                      "Je peux attendre aussi. J'ai l'habitude des sources mutiques.",
                      "Vous pensez que ça marche sur moi ? Peut-être un peu.",
                      "Ce silence… il me rend nerveuse. Et ça m'énerve d'admettre ça."],
    line_success = ("D'accord, Raven. Je vous fais confiance. "
                    "J'ai l'adresse du serveur miroir et la clé d'accès. "
                    "Mais quand tout ça sera terminé, j'ai l'exclusivité. Non négociable."),
    line_failure = ("Je n'ai rien à vous donner qui ne soit pas déjà public. "
                    "Si vous avez d'autres questions, passez par mon avocat."),

    evidence_hints = {
        "Fichiers Synarchie":  ("Montrer les fichiers", 1.60,
            "Ces fichiers… comment vous les avez eus ? C'est ce que je cherchais depuis des mois."),
        "Registre Offshore":   ("Citer le registre", 1.40,
            "Ce registre correspond exactement à ce que ma source m'avait décrit. C'est réel."),
        "Clé USB":             ("Mentionner la clé", 1.50,
            "La clé USB de Vane… c'est donc vrai. Il avait tout documenté."),
    },
    counter_questions = [
        _CounterQuestion(
            question       = "Vous avez publié des éléments de cette enquête ?",
            answer_true    = "Seulement ce qui était déjà vérifiable.",
            answer_lie     = "Rien du tout. Confidentialité totale.",
            answer_silence = "Ça ne change rien à notre conversation.",
            delta_true     = 0.07, delta_lie_ok = 0.09, delta_lie_fail = -0.11,
            delta_silence  = 0.05, lie_detect_p = 0.55,
        ),
    ],
)


# ══════════════════════════════════════════════════════════════════════════════
# Profil : Mira Voss
# ══════════════════════════════════════════════════════════════════════════════

MIRA = SuspectProfile(
    id         = "mira",
    name       = "Mira Voss",
    role       = "Ex-analyste RG — Contact indépendant",
    resistance   = 0.50,
    press_mult   = 1.00,
    bluff_mult   = 1.25,
    silence_mult = 1.30,
    bluff_p      = 0.55,
    expr = {
        "DÉFIANT": 1, "RÉSISTANT": 1,
        "NERVEUX": 2, "FISSURÉ": 3, "CRAQUANT": 3,
    },
    idle = {
        "DÉFIANT":   ["Je suis venue ici de mon plein gré. Je peux partir de même.",
                      "Ce que vous insinuez est faux.",
                      "Vous doutez de moi. C'est normal. Mais vous avez tort.",
                      "J'ai pris des risques que vous ne pouvez pas imaginer."],
        "RÉSISTANT": ["Qu'est-ce qui vous fait penser que je vous cache quelque chose ?",
                      "La lacune dans mon dossier. Je vous l'ai dit : protection judiciaire.",
                      "Si j'étais contre vous, je n'aurais pas mis cette clé USB sous votre porte.",
                      "On travaille ensemble depuis des mois, Raven. Qu'est-ce qui a changé ?"],
        "NERVEUX":   ["D'accord. Il y a une partie que je ne vous ai pas encore dite.",
                      "Mon directeur de cabinet… il ne m'a pas juste licenciée.",
                      "J'avais peur de la réaction si vous saviez tout depuis le début.",
                      "Ce n'est pas de la trahison. C'est de la prudence."],
        "FISSURÉ":   ["Les dix-huit mois. J'étais en contact avec l'un des membres du réseau.",
                      "Je pensais pouvoir double-jouer. Les retourner de l'intérieur.",
                      "J'ai échoué. Et depuis, j'essaie de réparer.",
                      "Je voulais vous le dire. J'attendais le bon moment."],
        "CRAQUANT":  ["Très bien. Je vais tout vous dire. Depuis le début.",
                      "Le contact à Berlin… ce n'est pas le premier à m'avoir approchée.",
                      "J'ai un autre dossier. Plus complet. Je le gardais en réserve.",
                      "Je ne suis pas votre ennemie, Raven. Je ne l'ai jamais été."],
    },
    react_press    = ["Cette preuve… je ne la connaissais pas. C'est plus grave que je ne le pensais.",
                      "D'accord. Vous avez raison sur ce point. Je ne peux pas le nier.",
                      "Vous êtes allé plus loin que moi. Je dois l'admettre.",
                      "Ce document change tout. Donnez-moi un moment.",
                      "C'est solide. Je ne m'y attendais pas."],
    react_bluff_ok = ["Ce dossier existe ? Vous l'avez vraiment ?",
                      "Je pensais que personne ne l'avait trouvé.",
                      "Si c'est vrai, alors oui. On doit parler.",
                      "Ça expliquerait beaucoup de choses que je n'arrivais pas à relier."],
    react_bluff_no = ["Non. Ce dossier n'existe pas sous cette forme. J'aurais su.",
                      "Vous testez mes réactions. Je connais la technique.",
                      "Je ne suis pas facile à manipuler. J'ai fait de l'analyse.",
                      "Mauvaise piste. Mais l'intention était bonne."],
    react_silence  = ["… Le silence. Vous voulez que je continue à parler seule.",
                      "D'accord. Je comprends pourquoi vous faites ça.",
                      "C'est efficace. Je dois l'admettre.",
                      "Vous avez appris ça où ? Psychologie d'interrogatoire ?",
                      "Très bien. Vous voulez de la vérité. Je vais vous en donner."],
    line_success = ("D'accord. Je vais tout vous dire — vraiment tout cette fois. "
                    "Il y a un troisième dossier. Que je n'ai montré à personne. "
                    "Il a les noms des sept protégés de l'Architecte. "
                    "Je l'ai gardé parce que j'avais peur. J'aurais dû vous faire confiance plus tôt."),
    line_failure = ("Je vous ai dit ce que je pouvais. "
                    "Si ce n'est pas suffisant pour vous, bonne chance, Raven."),

    evidence_hints = {
        "Clé USB #2":          ("Montrer la clé #2", 1.55,
            "Cette clé… elle a les mêmes marquages que celle de Vane. Quelqu'un a préparé ça."),
        "Badge magnétique":    ("Montrer le badge", 1.45,
            "Ce badge… il appartient à quelqu'un du Parlement. Ça confirme ce que j'avais soupçonné."),
        "Dossier Mira":        ("Citer votre dossier", 1.35,
            "Vous avez fait vérifier mon dossier. Je m'y attendais. Mais la lacune a une explication."),
    },
    counter_questions = [
        _CounterQuestion(
            question       = "Pourquoi vous avez attendu si longtemps pour me contacter ?",
            answer_true    = "Je devais vérifier que vous étiez fiable.",
            answer_lie     = "J'avais d'autres pistes à explorer d'abord.",
            answer_silence = "Le timing n'était pas le bon avant.",
            delta_true     = 0.09, delta_lie_ok = 0.07, delta_lie_fail = -0.09,
            delta_silence  = 0.05, lie_detect_p = 0.38,
        ),
    ],
)


# ══════════════════════════════════════════════════════════════════════════════
# Profil : Viktor Selg — "Le Fantôme"
# ══════════════════════════════════════════════════════════════════════════════

GHOST = SuspectProfile(
    id         = "ghost",
    name       = "Viktor Selg",
    role       = "Le Fantôme — Diplomate suédois, réseau Synarchie",
    resistance   = 0.80,
    press_mult   = 1.30,
    bluff_mult   = 0.60,
    silence_mult = 0.50,
    bluff_p      = 0.28,
    expr = {
        "DÉFIANT": 1, "RÉSISTANT": 1,
        "NERVEUX": 1, "FISSURÉ": 3, "CRAQUANT": 3,
    },
    idle = {
        "DÉFIANT":   ["Détective Raven. C'est décevant de finir ainsi.",
                      "Vous n'avez rien qui tienne devant un tribunal européen.",
                      "J'ai trente ans d'impunité derrière moi.",
                      "Mon équipe d'avocats est meilleure que tout ce qu'Interpol peut aligner."],
        "RÉSISTANT": ["Genève était un sacrifice. Ferrière, Arnheim — des sacrifices.",
                      "Ce que vous appelez des preuves, moi j'appelle ça des artefacts.",
                      "Vous avez une heure. Après, mon avion décolle.",
                      "Chaque document que vous avez a une explication légale."],
        "NERVEUX":   ["Le serveur de Berlin. Comment vous l'avez trouvé ?",
                      "Le contact… il a parlé. Voilà qui est intéressant.",
                      "Vous êtes plus rapide que je ne le pensais. Mes félicitations.",
                      "Certains détails que vous citez… ils ne devraient pas exister."],
        "FISSURÉ":   ["D'accord. Vous avez fait du bon travail. Je l'admets.",
                      "L'Architecte vous a utilisé. Comme il nous a tous utilisés.",
                      "Je ne suis pas le monstre de cette histoire. Je suis l'exécutant.",
                      "Si je parle… il y a des gens qui ne resteront pas passifs."],
        "CRAQUANT":  ["Très bien. On peut parler. Mais uniquement de ce qui m'implique.",
                      "L'Architecte. Son vrai nom. Vous voulez ça, n'est-ce pas ?",
                      "Je peux vous donner sept noms. Ceux qu'il vous manque encore.",
                      "Mais je veux une garantie écrite avant de prononcer un seul mot de plus."],
    },
    react_press    = ["Ce document… D'où il sort ? Ce n'était pas censé exister.",
                      "Vous avez accès à des sources que je croyais sécurisées. Impressionnant.",
                      "C'est solide. Je ne vais pas prétendre le contraire.",
                      "Voilà une preuve que je n'avais pas anticipée.",
                      "Bien. Vous avez fait vos devoirs. Je dois réévaluer ma position."],
    react_bluff_ok = ["Ce rapport… comment vous avez pu l'obtenir ?",
                      "Ça ne devrait pas exister. Mais si c'est vrai…",
                      "D'accord. Peut-être que je vous ai sous-estimé.",
                      "Je dois vérifier ça. Donnez-moi un moment."],
    react_bluff_no = ["Non. Ce document est une fabrication. Et je sais pourquoi.",
                      "Vous bluffez. Je le vois à la façon dont vous le tenez.",
                      "Mauvaise tentative. Je connais chaque pièce du dossier réel.",
                      "J'ai construit ma vie sur la détection du mensonge."],
    react_silence  = ["… Intéressant. Vous pensez que le silence me dérange.",
                      "J'ai passé trente ans à parler dans des pièces silencieuses.",
                      "Prenez votre temps.", "Ce silence ne m'affecte pas.",
                      "Vous perdez du temps précieux."],
    line_success = ("Très bien. Je vais parler. Pas par peur. Par calcul. "
                    "L'Architecte m'a sacrifié comme il a sacrifié Ferrière. "
                    "Son vrai nom : Constantine Havel. Voilà votre prochaine cible."),
    line_failure = ("Le temps est écoulé. Mon avion décolle dans quarante minutes. "
                    "Et vous n'avez rien qui puisse m'arrêter légalement. Au revoir."),

    evidence_hints = {
        "Accord de Berlin":    ("Montrer l'Accord 94", 1.90,
            "Ce document… c'est l'original. Comment vous avez eu accès au serveur miroir ?"),
        "Identité du Fantôme": ("Nommer Viktor Selg", 1.70,
            "Vous avez mon vrai nom. D'accord. La partie commence seulement."),
        "Serveur miroir":      ("Citer le serveur", 1.80,
            "Le serveur de Berlin… vous étiez là. Qui d'autre ? Ça change tout."),
        "Témoin protégé":      ("Citer le témoin", 1.65,
            "Mon ancien bras droit a parlé. Je vois. Sa nouvelle identité ne tiendra pas longtemps."),
    },
    counter_questions = [
        _CounterQuestion(
            question       = "Interpol est-il impliqué dans votre enquête ?",
            answer_true    = "Pas officiellement. Pas encore.",
            answer_lie     = "Oui. Ils ont tout le dossier.",
            answer_silence = "Ce qui compte, c'est ce que j'ai dans cette pièce.",
            delta_true     = 0.05, delta_lie_ok = 0.18, delta_lie_fail = -0.08,
            delta_silence  = 0.09, lie_detect_p = 0.50,
        ),
        _CounterQuestion(
            question       = "Comment vous avez trouvé l'adresse de ce lieu ?",
            answer_true    = "Par les coordonnées dans le testament de Vane.",
            answer_lie     = "Un contact à l'intérieur du réseau.",
            answer_silence = "Disons que j'ai de bonnes sources.",
            delta_true     = 0.06, delta_lie_ok = 0.10, delta_lie_fail = -0.14,
            delta_silence  = 0.07, lie_detect_p = 0.60,
        ),
    ],
)


# ══════════════════════════════════════════════════════════════════════════════
# Profil : L'Architecte
# ══════════════════════════════════════════════════════════════════════════════

ARCHITECT = SuspectProfile(
    id         = "architect",
    name       = "L'Architecte",
    role       = "Constantine Havel — Fondateur Synarchie",
    resistance   = 0.90,
    press_mult   = 0.70,
    bluff_mult   = 1.50,
    silence_mult = 0.40,
    bluff_p      = 0.70,
    expr = {
        "DÉFIANT": 0, "RÉSISTANT": 1,
        "NERVEUX": 1, "FISSURÉ": 2, "CRAQUANT": 3,
    },
    idle = {
        "DÉFIANT":   ["Raven. Nous voici au terme de quelque chose d'assez remarquable.",
                      "Vous avez nettoyé ce que je ne pouvais pas nettoyer moi-même. Merci.",
                      "Je ne suis pas en position de faiblesse. Je suis en position d'observation.",
                      "Ce que vous appelez une arrestation, j'appelle ça un déménagement."],
        "RÉSISTANT": ["Les preuves que vous avez ne couvrent que ce que j'ai voulu exposer.",
                      "L'iceberg. Vous avez la pointe. Le reste est intact.",
                      "Trente ans. Vingt-trois pays. Deux cents personnes. Tout ça reste opérationnel.",
                      "Vous pensez avoir gagné. C'est touchant."],
        "NERVEUX":   ["Ce document… Vane l'a vraiment conservé ? C'est étonnant.",
                      "Je dois admettre que vous m'avez surpris sur quelques points.",
                      "Le testament. Je croyais l'avoir neutralisé il y a sept ans.",
                      "Vous avez accès à des sources que je croyais définitivement fermées."],
        "FISSURÉ":   ["Très bien. Admettons que vous ayez plus que je ne le pensais.",
                      "Qu'est-ce que vous voulez réellement, Raven ? La vérité ?",
                      "Je peux vous donner ce que personne d'autre n'a jamais eu.",
                      "Nous pourrions avoir une conversation productive."],
        "CRAQUANT":  ["D'accord. Je parle. Pas parce que vous m'y forcez.",
                      "Parce que cette organisation mérite mieux que de mourir avec moi.",
                      "Il y a des choses que vous devriez savoir sur la vraie nature du réseau.",
                      "Je peux vous donner les sept noms. Et la preuve de ce qu'ils ont fait."],
    },
    react_press    = ["Ce document… c'est du travail sérieux. Je l'admets.",
                      "Vane a été plus prévoyant que je ne le croyais.",
                      "Vous avez cette pièce. D'accord. Ça change légèrement l'équilibre.",
                      "Intéressant. Vous avez accès à ça.",
                      "Cette preuve est réelle. Je ne vais pas la nier."],
    react_bluff_ok = ["Vous avez ça ? Vraiment ? Ça m'étonne.",
                      "Ce dossier… je pensais qu'il avait été détruit.",
                      "D'accord. Si vous avez ça, alors on peut parler différemment.",
                      "Vous m'avez surpris. C'est rare. Profitez-en."],
    react_bluff_no = ["Non. Ce document n'existe pas sous cette forme.",
                      "Essayez encore. Mais sans me faire perdre mon temps.",
                      "Vous bluffez. Et vous le faites mal.",
                      "J'ai construit des systèmes de désinformation pendant trente ans."],
    react_silence  = ["Le silence. Vous pensez que ça m'affecte.",
                      "… Je l'utilise depuis trente ans. Il me connaît bien.",
                      "Prenez le temps qu'il vous faut.",
                      "Ce silence ne m'inquiète pas. Rien ne m'inquiète.",
                      "Quand vous serez prêt, nous reprendrons."],
    line_success = ("Très bien. Puisque vous insistez. "
                    "Les sept noms que vous n'avez pas encore : "
                    "deux chefs d'État, trois directeurs de banque centrale, deux juges internationaux. "
                    "Pas par peur. Par respect pour ce que vous avez accompli."),
    line_failure = ("Vous avez fait du travail remarquable, Raven. "
                    "Mais vous n'avez pas assez. Ce qui reste de la Synarchie survivra."),

    evidence_hints = {
        "Testament de Vane":   ("Citer le testament", 2.00,
            "Ce testament… Vane a vraiment tout documenté. Trente ans. Il attendait quelqu'un comme vous."),
        "Preuve ultime":       ("Présenter la preuve", 1.90,
            "La preuve ultime. Vous l'avez réellement. D'accord. La conversation change de nature."),
        "Schéma du Réseau":    ("Montrer le schéma", 1.70,
            "Ce schéma… c'est presque complet. Il manque sept cases. Je peux les remplir."),
        "Accord Secret":       ("Citer l'Accord Secret", 1.80,
            "L'Accord Secret de Genève. Six gouvernements. Vous avez ça. Impressive detective work."),
        "Identité de l'Architecte": ("Nommer Constantine Havel", 2.10,
            "Mon vrai nom. Vane l'avait. Vous l'avez. D'accord. Je n'ai plus rien à cacher."),
    },
    counter_questions = [
        _CounterQuestion(
            question       = "Vous pensez vraiment pouvoir me juger ? Dans quel tribunal ?",
            answer_true    = "La Cour pénale internationale. À La Haye.",
            answer_lie     = "Un tribunal d'exception. Déjà constitué.",
            answer_silence = "Le tribunal qui convient à vos crimes.",
            delta_true     = 0.10, delta_lie_ok = 0.05, delta_lie_fail = -0.06,
            delta_silence  = 0.08, lie_detect_p = 0.80,
        ),
        _CounterQuestion(
            question       = "Si je coopère, qu'est-ce qui change pour les sept noms que vous n'avez pas ?",
            answer_true    = "Ils tombent avec vous. C'est l'objectif.",
            answer_lie     = "On peut négocier. Certains pourraient être protégés.",
            answer_silence = "Ça dépend de ce que vous me donnez.",
            delta_true     = 0.12, delta_lie_ok = 0.20, delta_lie_fail = -0.05,
            delta_silence  = 0.09, lie_detect_p = 0.35,
        ),
    ],
)


# ══════════════════════════════════════════════════════════════════════════════
# Profil : Sénateur Arnheim
# ══════════════════════════════════════════════════════════════════════════════

SENATOR = SuspectProfile(
    id         = "senator",
    name       = "Sénateur Arnheim",
    role       = "Délégué sécurité transnationale — Synarchie",
    resistance   = 0.62,
    press_mult   = 0.90,
    bluff_mult   = 1.55,
    silence_mult = 0.80,
    bluff_p      = 0.68,
    expr = {
        "DÉFIANT": 1, "RÉSISTANT": 1,
        "NERVEUX": 2, "FISSURÉ": 3, "CRAQUANT": 3,
    },
    idle = {
        "DÉFIANT":   ["Vous réalisez à qui vous parlez ? J'ai l'immunité parlementaire.",
                      "Cette conversation n'a aucune valeur légale.",
                      "J'ai voté des lois qui protègent les gens comme moi.",
                      "Mon bureau de communication va adorer cette histoire."],
        "RÉSISTANT": ["Ce compte en Lettonie… c'est un fonds de prévoyance légal.",
                      "Vous confondez influence et corruption.",
                      "J'ai servi ce pays pendant dix-huit ans. Dix-huit ans.",
                      "Selg est un conseiller parmi d'autres."],
        "NERVEUX":   ["D'où vous sortez cet enregistrement ? Il est tronqué, évidemment.",
                      "Ce que vous interprétez comme des ordres, c'est du conseil stratégique.",
                      "Mes avocats vont contester chaque élément de ce dossier.",
                      "Il y a des gens qui n'apprécieront pas que vous poursuiviez ceci."],
        "FISSURÉ":   ["D'accord. J'ai eu des contacts avec Selg. Ce n'est pas un crime.",
                      "La banque lettone… c'était avant que je sache ce que le réseau faisait.",
                      "Je n'ai pas commandité de crime. J'ai fermé les yeux.",
                      "Si je coopère, qu'est-ce que vous pouvez garantir ?"],
        "CRAQUANT":  ["Très bien. Je vais vous donner quelque chose.",
                      "Il y a deux autres sénateurs. Dans le réseau depuis plus longtemps que moi.",
                      "Et un magistrat à la Cour pénale internationale.",
                      "Mais je veux que ma coopération soit notée. Par écrit. Maintenant."],
    },
    react_press    = ["Ce document… d'où il sort ? Il ne devrait pas exister.",
                      "Voilà qui est plus solide que je ne le pensais.",
                      "Ce compte… les montants ne correspondent pas exactement à ce que…",
                      "C'est compromettant. Je dois l'admettre.",
                      "Vous avez de bonnes sources. Meilleures que celles de mon équipe."],
    react_bluff_ok = ["Vous avez le relevé complet ? Comment c'est possible ?",
                      "Ce rapport d'Interpol… il est officiel ?",
                      "D'accord. Si vous avez ça, alors la situation est différente.",
                      "Je ne savais pas que ce dossier existait encore sous cette forme."],
    react_bluff_no = ["Ce document est un faux. Je l'aurais su s'il existait.",
                      "Vous bluffez. Et vous n'avez pas le niveau pour ça face à moi.",
                      "J'ai vu passer mille dossiers dans ma carrière.",
                      "Essayez autre chose. Ceci ne marche pas."],
    react_silence  = ["Vous attendez quelque chose ? Dites-le.",
                      "… Le silence. Très professionnel.",
                      "Je ne suis pas intimidé par les pauses.",
                      "Mon temps vaut beaucoup. Ne le gaspillez pas.",
                      "Vous voulez que je parle en premier. C'est non."],
    line_success = ("D'accord. Voilà ce que vous voulez : "
                    "deux sénateurs, un magistrat international. "
                    "Et les détails du financement de la commission de Berlin. "
                    "Mais je veux un accord. Maintenant."),
    line_failure = ("Cette conversation n'a jamais eu lieu. "
                    "Mon avocat déposera une plainte d'ici une heure. Bonne journée."),

    evidence_hints = {
        "Enregistrement parlement": ("Jouer l'enreg. parlement", 1.85,
            "Cet enregistrement… c'était une réunion à huis clos. Quelqu'un a trahi. Qui ?"),
        "Compte numéroté":     ("Citer le compte letton", 1.70,
            "Ce compte… vous avez les relevés complets ? Pas seulement les totaux ?"),
        "Identité du Sénateur": ("Nommer Arnheim", 1.60,
            "Mon nom dans ce dossier. D'accord. Ça dépasse ce que j'avais anticipé."),
        "Registre Offshore":   ("Croiser avec Vane Ch1", 1.75,
            "La même banque que Vane. Vingt ans. Vous avez fait le lien. Impressionnant."),
    },
    counter_questions = [
        _CounterQuestion(
            question       = "Vous avez une autorisation pour enregistrer cet entretien ?",
            answer_true    = "Non. C'est une conversation informelle.",
            answer_lie     = "Oui. Mandat judiciaire en bonne et due forme.",
            answer_silence = "La légalité de cet entretien n'est pas votre seul problème.",
            delta_true     = 0.07, delta_lie_ok = 0.03, delta_lie_fail = -0.18,
            delta_silence  = 0.11, lie_detect_p = 0.75,
        ),
        _CounterQuestion(
            question       = "Avez-vous des preuves qui m'impliquent directement dans un crime ?",
            answer_true    = "Oui. Le compte letton et l'enregistrement.",
            answer_lie     = "Bien plus que ça. Vous n'imaginez pas l'étendue du dossier.",
            answer_silence = "Assez pour que vous soyez inquiet.",
            delta_true     = 0.08, delta_lie_ok = 0.20, delta_lie_fail = -0.06,
            delta_silence  = 0.12, lie_detect_p = 0.30,
        ),
    ],
)


# ══════════════════════════════════════════════════════════════════════════════
# Registre
# ══════════════════════════════════════════════════════════════════════════════

SUSPECTS: dict[str, SuspectProfile] = {
    "taro":      TARO,
    "ferriere":  FERRIERE,
    "natasha":   NATASHA,
    "mira":      MIRA,
    "ghost":     GHOST,
    "architect": ARCHITECT,
    "senator":   SENATOR,
}


# ══════════════════════════════════════════════════════════════════════════════
# Mini-jeu principal
# ══════════════════════════════════════════════════════════════════════════════

class InterrogationMinigame:
    """
    Mini-jeu d'interrogatoire v2.

    Nouveautés :
      • Decay suspendu ≥ 95% → victoire toujours accessible
      • Preuves contextuelles (boutons supplémentaires si collectées en jeu)
      • Contre-interrogatoire : le suspect pose une question, 3 réponses possibles

    Paramètre supplémentaire :
      collected_evidence : list[str]   — noms des preuves collectées dans le script
    """

    def __init__(
        self,
        screen:             pygame.Surface,
        assets,
        suspect_id:         str = "taro",
        time_limit:         float = 90.0,
        on_success:         Optional[Callable] = None,
        on_failure:         Optional[Callable] = None,
        collected_evidence: Optional[list[str]] = None,
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

        self.pressure   = 0.0
        self.state      = SuspectState.DEFIANT
        self.actions    = _build_actions()

        # ── Preuves contextuelles ──────────────────────────────────────────────
        ev = collected_evidence or []
        self._ev_slots: list[_EvidenceSlot] = []
        ev_keys = [pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i]
        for idx, (ev_name, (label, mult, reaction)) in enumerate(
            self.suspect.evidence_hints.items()
        ):
            if ev_name in ev and idx < len(ev_keys):
                self._ev_slots.append(_EvidenceSlot(
                    evidence_name = ev_name,
                    label         = label,
                    multiplier    = mult,
                    reaction      = reaction,
                    key           = ev_keys[idx],
                ))

        # ── Contre-interrogatoire ─────────────────────────────────────────────
        self._counter_active:    bool = False
        self._counter_q:         Optional[_CounterQuestion] = None
        self._counter_choices:   list[str] = []
        self._counter_idx:       int = 0       # choix survolé (0=Vrai,1=Mensonge,2=Silence)
        self._counter_timer:     float = self._next_counter_delay()
        self._counter_used:      set[int] = set()   # indices des questions déjà posées
        self._counter_btn_rects: list[pygame.Rect] = []

        # ── Dialogue ──────────────────────────────────────────────────────────
        self._line         = self._idle_line()
        self._line_timer   = 0.0
        self._line_delay   = 4.5

        # ── Effets visuels ────────────────────────────────────────────────────
        self._feedbacks:       list[_Feedback] = []
        self._flash:           Optional[_ScreenFlash] = None
        self._pressure_pulse:  float = 0.0
        self._result:          Optional[str] = None
        self._end_timer:       float = _END_HOLD
        self._portrait_shake:  float = 0.0
        self._portrait_shake_t: float = 0.0

        # ── Polices ───────────────────────────────────────────────────────────
        self._font_title = getattr(assets, "font_title", None) or \
                           pygame.font.SysFont("monospace", 28, bold=True)
        self._font_big   = getattr(assets, "font_big",   None) or \
                           pygame.font.SysFont("monospace", 22, bold=True)
        self._font_med   = getattr(assets, "font_med",   None) or \
                           pygame.font.SysFont("monospace", 16)
        self._font_small = getattr(assets, "font_small", None) or \
                           pygame.font.SysFont("monospace", 12)

        self._bg = getattr(assets, "bg", {}).get("salle_interrogatoire", None)

        self._layout:    dict[str, pygame.Rect] = {}
        self._btn_rects: list[pygame.Rect]      = []
        self._ev_rects:  list[pygame.Rect]      = []
        self._compute_layout()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _compute_layout(self) -> None:
        W, H = SCREEN_W, SCREEN_H
        self._layout["header"]     = pygame.Rect(0, 0, W, 46)
        self._layout["portrait"]   = pygame.Rect(12, 52, 288, 320)
        self._layout["pressure"]   = pygame.Rect(315, 64, W - 430, 22)
        self._timer_center         = (W - 80, 148)
        self._timer_radius         = 52
        self._layout["state_badge"]= pygame.Rect(12, 378, 288, 30)
        self._layout["dialogue"]   = pygame.Rect(12, 415, W - 24, 62)

        # Boutons standard (3) — rangée du bas
        BTN_W, BTN_H = 198, 58
        GAP           = 22
        total_w       = 3 * BTN_W + 2 * GAP
        bx            = (W - total_w) // 2
        by            = H - BTN_H - 8
        self._btn_rects = [
            pygame.Rect(bx + i * (BTN_W + GAP), by, BTN_W, BTN_H)
            for i in range(3)
        ]
        self._hint_y = by - 20

        # Boutons preuves contextuelles — rangée au-dessus
        EV_W, EV_H = 190, 42
        EV_GAP     = 14
        n_ev       = len(self._ev_slots)
        if n_ev:
            ev_total_w = n_ev * EV_W + (n_ev - 1) * EV_GAP
            evx        = (W - ev_total_w) // 2
            evy        = by - EV_H - 36
            self._ev_rects = [
                pygame.Rect(evx + i * (EV_W + EV_GAP), evy, EV_W, EV_H)
                for i in range(n_ev)
            ]
            self._hint_y = evy - 18
        else:
            self._ev_rects = []

        # Boutons contre-interrogatoire (calculés à la demande)
        self._counter_btn_rects = []

    def _recompute_counter_rects(self) -> None:
        W, H = SCREEN_W, SCREEN_H
        CB_W, CB_H = 300, 50
        CB_GAP     = 16
        total_w    = 3 * CB_W + 2 * CB_GAP
        cbx        = (W - total_w) // 2
        cby        = H - CB_H - 20
        self._counter_btn_rects = [
            pygame.Rect(cbx + i * (CB_W + CB_GAP), cby, CB_W, CB_H)
            for i in range(3)
        ]

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _idle_line(self) -> str:
        label = _STATE_META[self.state][0]
        lines = self.suspect.idle.get(label, ["…"])
        return random.choice(lines)

    def _set_line(self, text: str) -> None:
        self._line       = text
        self._line_timer = 0.0

    def _next_counter_delay(self) -> float:
        return random.uniform(_COUNTER_INTERVAL_MIN, _COUNTER_INTERVAL_MAX)

    def _start_shake(self, intensity: float) -> None:
        self._portrait_shake   = intensity * 5.0
        self._portrait_shake_t = 0.0

    # ── Actions standard ──────────────────────────────────────────────────────

    def _do_press(self) -> _Feedback:
        base = random.uniform(0.10, 0.18)
        if self.state == SuspectState.DEFIANT and self.suspect.resistance > 0.6:
            base *= 0.65
        self.pressure  = min(1.0, self.pressure + base * self.suspect.press_mult)
        self.time_left = max(0.0, self.time_left - _COST_PRESS)
        self._start_shake(0.6)
        self._flash = _ScreenFlash(RED_ACCENT)
        return _Feedback(random.choice(self.suspect.react_press), (255, 190, 190))

    def _do_bluff(self) -> _Feedback:
        success        = random.random() < self.suspect.bluff_p
        self.time_left = max(0.0, self.time_left - _COST_BLUFF)
        if success:
            delta         = random.uniform(0.15, 0.22) * self.suspect.bluff_mult
            self.pressure = min(1.0, self.pressure + delta)
            self._flash   = _ScreenFlash(GOLD)
            self._start_shake(1.0)
            return _Feedback(random.choice(self.suspect.react_bluff_ok), (200, 255, 140))
        else:
            self.pressure = max(0.0, self.pressure - random.uniform(0.04, 0.09))
            self._flash   = _ScreenFlash(PINK_ACCENT)
            return _Feedback(random.choice(self.suspect.react_bluff_no), (255, 140, 100), False)

    def _do_silence(self) -> _Feedback:
        self.pressure  = min(1.0, self.pressure + random.uniform(0.03, 0.07) * self.suspect.silence_mult)
        self.time_left = max(0.0, self.time_left - _COST_SILENCE)
        return _Feedback(random.choice(self.suspect.react_silence), (150, 220, 255))

    def _do_evidence(self, slot: _EvidenceSlot) -> _Feedback:
        """Utiliser une preuve contextuelle — usage unique, fort bonus."""
        bonus          = random.uniform(0.14, 0.22) * slot.multiplier
        self.pressure  = min(1.0, self.pressure + bonus)
        self.time_left = max(0.0, self.time_left - _COST_EVIDENCE)
        slot.trigger()
        self._start_shake(1.2)
        self._flash = _ScreenFlash(PINK_EVIDENCE)
        return _Feedback(slot.reaction, (220, 180, 255))

    def _trigger(self, idx: int) -> None:
        if self._result is not None or self._counter_active:
            return
        slot = self.actions[idx]
        if not slot.ready:
            return
        slot.trigger()
        fb = (self._do_press, self._do_bluff, self._do_silence)[idx]()
        self._feedbacks.append(fb)
        self._set_line(fb.text)

    def _trigger_evidence(self, idx: int) -> None:
        if self._result is not None or self._counter_active:
            return
        if idx >= len(self._ev_slots):
            return
        slot = self._ev_slots[idx]
        if not slot.ready:
            return
        fb = self._do_evidence(slot)
        self._feedbacks.append(fb)
        self._set_line(fb.text)

    # ── Contre-interrogatoire ─────────────────────────────────────────────────

    def _launch_counter(self) -> None:
        """Choisit une question non encore posée et l'affiche."""
        available = [
            (i, q) for i, q in enumerate(self.suspect.counter_questions)
            if i not in self._counter_used
        ]
        if not available:
            self._counter_timer = self._next_counter_delay()
            return
        idx, q = random.choice(available)
        self._counter_used.add(idx)
        self._counter_q       = q
        self._counter_choices = [q.answer_true, q.answer_lie, q.answer_silence]
        self._counter_idx     = 0
        self._counter_active  = True
        self._recompute_counter_rects()
        self._set_line(q.question)
        self._flash = _ScreenFlash((200, 120, 50))   # flash orange = interruption

    def _resolve_counter(self, choice: int) -> None:
        """Résout la réponse du joueur (0=Vrai, 1=Mensonge, 2=Silence)."""
        q = self._counter_q
        if q is None:
            self._counter_active = False
            return

        if choice == 0:   # Vrai
            self.pressure = min(1.0, self.pressure + q.delta_true)
            fb = _Feedback(q.answer_true + " — Réponse honnête.", (180, 230, 180))
        elif choice == 1:  # Mensonge
            detected = random.random() < q.lie_detect_p
            if detected:
                self.pressure = max(0.0, self.pressure + q.delta_lie_fail)
                self.time_left = max(0.0, self.time_left - 6.0)
                fb = _Feedback("Mensonge détecté ! Le suspect reprend l'avantage.", (255, 80, 80), False)
                self._flash = _ScreenFlash(RED_ACCENT)
            else:
                self.pressure = min(1.0, self.pressure + q.delta_lie_ok)
                fb = _Feedback("Le mensonge passe. Pression accrue.", (230, 200, 100))
                self._flash = _ScreenFlash(GOLD)
        else:              # Silence
            self.pressure = min(1.0, self.pressure + q.delta_silence)
            fb = _Feedback("Silence gardé. La tension monte légèrement.", (150, 200, 255))

        self._feedbacks.append(fb)
        self._set_line(fb.text)
        self._counter_active = False
        self._counter_q      = None
        self._counter_timer  = self._next_counter_delay()

    # ── Update ────────────────────────────────────────────────────────────────

    def update(
        self, dt: float, events: list[pygame.event.Event]
    ) -> Optional[Literal["success", "failure"]]:

        # Phase de fin
        if self._result is not None:
            self._end_timer -= dt
            if self._end_timer <= 0.0:
                return self._result
            return None

        self.time_left = max(0.0, self.time_left - dt)

        # Decay suspendu au-delà du seuil — victoire toujours accessible
        if self.pressure < PRESSURE_DECAY_CUTOFF:
            self.pressure = max(0.0, self.pressure - PRESSURE_DECAY * dt)

        # Cooldowns actions std
        for slot in self.actions:
            slot.tick(dt)
        for ev_slot in self._ev_slots:
            ev_slot.tick(dt)

        # Feedbacks / effets
        self._feedbacks = [f for f in self._feedbacks if f.alive]
        for f in self._feedbacks:
            f.tick(dt)
        if self._flash and self._flash.alive:
            self._flash.tick(dt)

        # Shake portrait
        if self._portrait_shake > 0:
            self._portrait_shake_t += dt * 30
            self._portrait_shake    = max(0.0, self._portrait_shake - dt * 8)

        self._pressure_pulse = (self._pressure_pulse + dt * 3) % (2 * math.pi)

        # Rotation ligne idle (seulement si pas de contre-interrogatoire)
        if not self._counter_active:
            self._line_timer += dt
            if self._line_timer >= self._line_delay:
                self._line_timer = 0.0
                self._line       = self._idle_line()

        self.state = _state_from(self.pressure)

        # Timer contre-interrogatoire (seulement si des questions existent)
        if (not self._counter_active
                and self.suspect.counter_questions
                and self._result is None):
            self._counter_timer -= dt
            if self._counter_timer <= 0.0:
                self._launch_counter()

        # Victoire
        if self.pressure >= PRESSURE_WIN:
            self._result    = "success"
            self._end_timer = _END_HOLD
            self._set_line(self.suspect.line_success)
            self._flash = _ScreenFlash((50, 230, 110))
            return None

        # Défaite
        if self.time_left <= 0.0:
            self._result    = "failure"
            self._end_timer = _END_HOLD
            self._set_line(self.suspect.line_failure)
            self._flash = _ScreenFlash(RED_ACCENT)
            return None

        # Événements
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if self._counter_active:
                    # Navigation dans les réponses
                    if ev.key == pygame.K_LEFT:
                        self._counter_idx = (self._counter_idx - 1) % 3
                    elif ev.key == pygame.K_RIGHT:
                        self._counter_idx = (self._counter_idx + 1) % 3
                    elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self._resolve_counter(self._counter_idx)
                    elif ev.key == pygame.K_a:
                        self._resolve_counter(0)
                    elif ev.key == pygame.K_z:
                        self._resolve_counter(1)
                    elif ev.key == pygame.K_e:
                        self._resolve_counter(2)
                else:
                    # Actions standard
                    for i, slot in enumerate(self.actions):
                        if ev.key in (slot.key, slot.key_alt):
                            self._trigger(i)
                            break
                    # Preuves contextuelles
                    for i, ev_slot in enumerate(self._ev_slots):
                        if ev.key == ev_slot.key and ev_slot.ready:
                            self._trigger_evidence(i)
                            break

            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self._counter_active:
                    for i, rect in enumerate(self._counter_btn_rects):
                        if rect.collidepoint(ev.pos):
                            self._resolve_counter(i)
                            break
                else:
                    for i, rect in enumerate(self._btn_rects):
                        if rect.collidepoint(ev.pos):
                            self._trigger(i)
                            break
                    for i, rect in enumerate(self._ev_rects):
                        if rect.collidepoint(ev.pos):
                            self._trigger_evidence(i)
                            break

            elif ev.type == pygame.MOUSEMOTION and self._counter_active:
                for i, rect in enumerate(self._counter_btn_rects):
                    if rect.collidepoint(ev.pos):
                        self._counter_idx = i
                        break

        return None

    # ══════════════════════════════════════════════════════════════════════════
    # Draw
    # ══════════════════════════════════════════════════════════════════════════

    def draw(self, surface: pygame.Surface) -> None:
        self._draw_background(surface)
        self._draw_header(surface)
        self._draw_portrait(surface)
        self._draw_state_badge(surface)
        self._draw_pressure_bar(surface)
        self._draw_timer(surface)
        self._draw_stat_details(surface)
        self._draw_dialogue(surface)
        if self._counter_active:
            self._draw_counter_overlay(surface)
        else:
            self._draw_hint(surface)
            self._draw_buttons(surface)
            self._draw_ev_buttons(surface)
        self._draw_feedbacks(surface)
        if self._flash and self._flash.alive:
            self._draw_flash(surface)
        if self._result is not None:
            self._draw_end_screen(surface)

    # ── Fond ──────────────────────────────────────────────────────────────────

    def _draw_background(self, surf: pygame.Surface) -> None:
        if self._bg:
            surf.blit(self._bg, (0, 0))
        else:
            surf.fill((10, 12, 24))
        dark = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        dark.fill((0, 0, 10, 170))
        surf.blit(dark, (0, 0))
        for i in range(6):
            r = SCREEN_W // 2 - i * 60
            if r <= 0:
                break
            vig = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            pygame.draw.ellipse(vig, (0, 0, 0, i * 8),
                                pygame.Rect(SCREEN_W//2 - r, SCREEN_H//2 - r//2, r*2, r))
            surf.blit(vig, (0, 0))

    # ── En-tête ───────────────────────────────────────────────────────────────

    def _draw_header(self, surf: pygame.Surface) -> None:
        bar = pygame.Surface((SCREEN_W, 46), pygame.SRCALPHA)
        bar.fill((4, 6, 18, 240))
        surf.blit(bar, (0, 0))
        pygame.draw.line(surf, CYAN, (0, 46), (SCREEN_W, 46), 1)
        title_s = self._font_title.render(
            f"INTERROGATOIRE — {self.suspect.name.upper()}", True, CYAN)
        surf.blit(title_s, (SCREEN_W // 2 - title_s.get_width() // 2, 8))
        role_s = self._font_small.render(self.suspect.role, True, TEXT_GRAY)
        surf.blit(role_s, (SCREEN_W - role_s.get_width() - _PAD, 16))

    # ── Portrait ──────────────────────────────────────────────────────────────

    def _draw_portrait(self, surf: pygame.Surface) -> None:
        rect = self._layout["portrait"]
        state_label, state_col = _STATE_META[self.state]
        expr_idx = self.suspect.expr.get(state_label, 0)
        shake_x  = 0
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
            surf.blit(scaled, (rect.x + (rect.w - nw)//2 + shake_x, rect.y + rect.h - nh))
        else:
            ph = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            ph.fill((*state_col, 25))
            pygame.draw.rect(ph, state_col, ph.get_rect(), 2, border_radius=8)
            surf.blit(ph, (rect.x + shake_x, rect.y))
            n_s = self._font_med.render(self.suspect.name, True, state_col)
            surf.blit(n_s, (rect.x + shake_x + rect.w//2 - n_s.get_width()//2, rect.y + rect.h//2))

        glow_a = int(60 + 80 * self.pressure)
        pygame.draw.rect(surf, (*state_col, glow_a), rect.inflate(4, 4), 2, border_radius=6)

    # ── Badge état ────────────────────────────────────────────────────────────

    def _draw_state_badge(self, surf: pygame.Surface) -> None:
        rect        = self._layout["state_badge"]
        label, col  = _STATE_META[self.state]
        badge = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        badge.fill((*col, 55))
        surf.blit(badge, rect.topleft)
        pygame.draw.rect(surf, col, rect, 1)
        lbl_s = self._font_med.render(label, True, col)
        surf.blit(lbl_s, (rect.x + rect.w//2 - lbl_s.get_width()//2,
                           rect.y + (rect.h - lbl_s.get_height())//2))

    # ── Barre de pression ─────────────────────────────────────────────────────

    def _draw_pressure_bar(self, surf: pygame.Surface) -> None:
        rect = self._layout["pressure"]
        pct  = int(self.pressure * 100)

        # Indicateur "decay suspendu"
        decay_label = "▲ ZONE CRITIQUE — MAINTENIR LA PRESSION" if self.pressure >= PRESSURE_DECAY_CUTOFF else f"PRESSION PSYCHOLOGIQUE  {pct} %"
        col_lbl = GOLD if self.pressure >= PRESSURE_DECAY_CUTOFF else TEXT_NAME
        label_s = self._font_small.render(decay_label, True, col_lbl)
        surf.blit(label_s, (rect.x, rect.y - 18))

        bg = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        bg.fill((18, 20, 38, 210))
        surf.blit(bg, rect.topleft)
        pygame.draw.rect(surf, (55, 65, 105), rect, 1)

        fill_w = int(rect.w * self.pressure)
        if fill_w > 0:
            fill = pygame.Surface((fill_w, rect.h), pygame.SRCALPHA)
            for i in range(fill_w):
                t = i / rect.w
                if t < 0.50:
                    r, g, b = int(40 + 20*t*2), int(80 + 140*t*2), 220
                elif t < 0.70:
                    f = (t-0.50)/0.20; r, g, b = int(60+160*f), 220, int(220-160*f)
                elif t < 0.85:
                    f = (t-0.70)/0.15; r, g, b = int(220+35*f), int(220-100*f), int(60-40*f)
                elif t < 0.95:
                    f = (t-0.85)/0.10; r, g, b = 255, int(120-80*f), 0
                else:
                    f = (t-0.95)/0.05; r = 255; g = int(40 + 160*f); b = 0
                pygame.draw.line(fill, (r, g, b, 235), (i, 0), (i, rect.h-1))
            surf.blit(fill, rect.topleft)

        # Pulse bord
        if self.pressure > 0.05:
            pulse_a = int(80 + 60 * math.sin(self._pressure_pulse))
            pw      = min(4, fill_w)
            if pw > 0:
                ps = pygame.Surface((pw, rect.h), pygame.SRCALPHA)
                ps.fill((255, 255, 255, pulse_a))
                surf.blit(ps, (rect.x + fill_w - pw, rect.y))

        for threshold in _BAR_MARKERS:
            mx  = rect.x + int(rect.w * threshold)
            col = GOLD if threshold == 0.95 else (160, 165, 210)
            pygame.draw.line(surf, col, (mx, rect.y - 5), (mx, rect.y + rect.h + 5), 1)

        if self._result is None and self.pressure < PRESSURE_DECAY_CUTOFF:
            next_t = next((t for t in _BAR_MARKERS if t > self.pressure), None)
            if next_t is not None:
                nxt_s = self._font_small.render(
                    f"seuil : {int(next_t*100)} %", True, TEXT_GRAY)
                surf.blit(nxt_s, (rect.right - nxt_s.get_width(), rect.y - 18))

    # ── Timer ─────────────────────────────────────────────────────────────────

    def _draw_timer(self, surf: pygame.Surface) -> None:
        cx, cy = self._timer_center
        R, Ri  = self._timer_radius, self._timer_radius - 14
        frac   = self.time_left / self.time_max if self.time_max > 0 else 0.0

        if frac > 0.50:
            col = (210, 225, 255)
        elif frac > 0.25:
            col = GOLD
        else:
            blink = int(220 + 35 * math.sin(pygame.time.get_ticks() / 200))
            col   = (blink, 40, 40)

        pygame.draw.circle(surf, (22, 24, 44), (cx, cy), R)
        if frac > 0.0:
            steps = max(6, int(50 * frac))
            a0    = -math.pi / 2
            a1    = a0 + 2 * math.pi * frac
            pts   = [(cx, cy)]
            for i in range(steps + 1):
                a = a0 + (a1 - a0) * i / steps
                pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
            if len(pts) >= 3:
                pygame.draw.polygon(surf, col, pts)
        pygame.draw.circle(surf, (8, 10, 22), (cx, cy), Ri)
        pygame.draw.circle(surf, col, (cx, cy), R, 2)

        secs = int(self.time_left)
        m, s = divmod(secs, 60)
        t_s  = self._font_big.render(f"{m:02d}:{s:02d}", True, col)
        surf.blit(t_s, (cx - t_s.get_width()//2, cy - t_s.get_height()//2))
        lbl = self._font_small.render("TEMPS", True, TEXT_GRAY)
        surf.blit(lbl, (cx - lbl.get_width()//2, cy + R + 4))

    # ── Stats ─────────────────────────────────────────────────────────────────

    def _draw_stat_details(self, surf: pygame.Surface) -> None:
        x, y = 315, 100
        for label, col in [
            (f"PRESS   ×{self.suspect.press_mult:.1f}",   RED_ACCENT),
            (f"BLUFF   ×{self.suspect.bluff_mult:.1f}",   GOLD),
            (f"SILENCE ×{self.suspect.silence_mult:.1f}", CYAN),
        ]:
            ls = self._font_small.render(label, True, col)
            surf.blit(ls, (x, y))
            y += 18

    # ── Dialogue ──────────────────────────────────────────────────────────────

    def _draw_dialogue(self, surf: pygame.Surface) -> None:
        rect = self._layout["dialogue"]
        box  = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        box.fill((6, 8, 20, 215))
        surf.blit(box, rect.topleft)
        pygame.draw.rect(surf, CYAN_DIM, rect, 1)

        name_s = self._font_small.render(f"[ {self.suspect.name.upper()} ]", True, TEXT_NAME)
        surf.blit(name_s, (rect.x + 10, rect.y + 7))

        max_w    = rect.w - 145
        words    = self._line.split()
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

    # ── Hint clavier ──────────────────────────────────────────────────────────

    def _draw_hint(self, surf: pygame.Surface) -> None:
        hint_parts = ["[A] Press  [Z] Bluff  [E] Silence"]
        if self._ev_slots:
            ev_keys = ["R", "T", "Y", "U", "I"]
            for i, sl in enumerate(self._ev_slots):
                if sl.ready:
                    hint_parts.append(f"[{ev_keys[i]}] {sl.label[:18]}")
        hint = self._font_small.render("   ".join(hint_parts), True, TEXT_GRAY)
        surf.blit(hint, (SCREEN_W//2 - hint.get_width()//2, self._hint_y))

    # ── Boutons standard ──────────────────────────────────────────────────────

    def _draw_buttons(self, surf: pygame.Surface) -> None:
        for slot, rect in zip(self.actions, self._btn_rects):
            col     = slot.color
            dim_a   = 110 if not slot.ready else 255
            dim_col = tuple(min(255, int(c * dim_a / 255)) for c in col[:3])

            btn_bg = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            btn_bg.fill((*col[:3], 35 if slot.ready else 18))
            surf.blit(btn_bg, rect.topleft)

            border_col = col if slot.ready else (70, 75, 90)
            pygame.draw.rect(surf, border_col, rect, 2, border_radius=6)

            key_char = {"press": "A", "bluff": "Z", "silence": "E"}[slot.name]
            surf.blit(self._font_small.render(f"[{key_char}]", True, (*dim_col, dim_a)),
                      (rect.x + 8, rect.y + 8))
            name_s = self._font_med.render(slot.label, True, (*dim_col, dim_a))
            surf.blit(name_s, (rect.x + rect.w//2 - name_s.get_width()//2, rect.y + 8))
            desc_s = self._font_small.render(slot.desc[:28], True, (*TEXT_GRAY[:3], dim_a))
            surf.blit(desc_s, (rect.x + rect.w//2 - desc_s.get_width()//2, rect.y + rect.h - 20))

            if not slot.ready:
                acx, acy, ar = rect.right - 16, rect.y + 16, 12
                pygame.draw.circle(surf, (35, 38, 58), (acx, acy), ar)
                rf = 1.0 - slot.cd_frac
                if rf > 0:
                    a0, a1 = -math.pi/2, -math.pi/2 + 2*math.pi*rf
                    stp    = max(4, int(16 * rf))
                    pts    = [(acx, acy)] + [(acx + ar*math.cos(a0+(a1-a0)*j/stp),
                                              acy + ar*math.sin(a0+(a1-a0)*j/stp))
                                             for j in range(stp+1)]
                    if len(pts) >= 3:
                        pygame.draw.polygon(surf, col, pts)
                pygame.draw.circle(surf, (8, 10, 22), (acx, acy), ar - 5)
                cd_s = self._font_small.render(f"{slot.cd_remain:.0f}", True, col)
                surf.blit(cd_s, (acx - cd_s.get_width()//2, acy - cd_s.get_height()//2))

    # ── Boutons preuves contextuelles ─────────────────────────────────────────

    def _draw_ev_buttons(self, surf: pygame.Surface) -> None:
        ev_keys = ["R", "T", "Y", "U", "I"]
        for i, (slot, rect) in enumerate(zip(self._ev_slots, self._ev_rects)):
            if slot.used:
                # Bouton grisé avec mention "utilisé"
                used_s = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
                used_s.fill((20, 20, 30, 120))
                pygame.draw.rect(used_s, (50, 55, 70, 120), (0, 0, rect.w, rect.h), 1, border_radius=5)
                surf.blit(used_s, rect.topleft)
                lbl = self._font_small.render("✔ " + slot.label[:22], True, (80, 90, 110))
                surf.blit(lbl, (rect.x + rect.w//2 - lbl.get_width()//2,
                                rect.y + rect.h//2 - lbl.get_height()//2))
                continue

            ready = slot.ready
            dim_a = 230 if ready else 80
            col   = PINK_EVIDENCE

            btn_bg = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            btn_bg.fill((*col, 40 if ready else 12))
            surf.blit(btn_bg, rect.topleft)
            pygame.draw.rect(surf, (*col, dim_a), rect, 2 if ready else 1, border_radius=5)

            key_s = self._font_small.render(f"[{ev_keys[i]}]", True, (*col, dim_a))
            surf.blit(key_s, (rect.x + 6, rect.y + 4))

            lbl_s = self._font_small.render(slot.label[:24], True, (*col, dim_a))
            surf.blit(lbl_s, (rect.x + rect.w//2 - lbl_s.get_width()//2,
                               rect.y + rect.h//2 - lbl_s.get_height()//2))

            # Indicateur "×mult"
            mult_s = self._font_small.render(f"×{slot.multiplier:.1f}", True,
                                             (*GOLD, dim_a))
            surf.blit(mult_s, (rect.right - mult_s.get_width() - 6, rect.y + 4))

    # ── Contre-interrogatoire overlay ─────────────────────────────────────────

    def _draw_counter_overlay(self, surf: pygame.Surface) -> None:
        if not self._counter_q:
            return

        # Voile orange "interruption"
        veil = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        veil.fill((60, 30, 0, 80))
        surf.blit(veil, (0, 0))

        # Bandeau question
        bw, bh = SCREEN_W - 40, 48
        bx, by = 20, self._layout["dialogue"].y - bh - 8
        band   = pygame.Surface((bw, bh), pygame.SRCALPHA)
        band.fill((35, 18, 4, 230))
        pygame.draw.rect(band, GOLD, (0, 0, bw, bh), 2, border_radius=6)
        surf.blit(band, (bx, by))

        lbl = self._font_small.render("⚡ CONTRE-INTERROGATOIRE", True, GOLD)
        surf.blit(lbl, (bx + 12, by + 6))
        q_s = self._font_med.render(self._counter_q.question, True, TEXT_MAIN)
        surf.blit(q_s, (bx + 12, by + 24))

        # 3 boutons réponse
        labels = ["Vrai [A]", "Mensonge [Z]", "Silence [E]"]
        colors = [(100, 220, 120), (220, 160, 60), (100, 180, 255)]
        for i, (rect, label, col) in enumerate(
            zip(self._counter_btn_rects, labels, colors)
        ):
            selected = i == self._counter_idx
            btn = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            bg_a = 80 if selected else 30
            btn.fill((*col, bg_a))
            border_w = 2 if selected else 1
            pygame.draw.rect(btn, (*col, 220 if selected else 120),
                             (0, 0, rect.w, rect.h), border_w, border_radius=6)
            # Texte de la réponse (courte)
            answer_text = self._counter_choices[i]
            ans_s = self._font_small.render(answer_text[:36], True,
                                            col if selected else TEXT_GRAY)
            lbl_s = self._font_small.render(label, True, col if selected else TEXT_GRAY)
            btn.blit(lbl_s, (8, 4))
            btn.blit(ans_s, (8, 22))
            surf.blit(btn, (rect.x, rect.y))

        # Hint navigation
        hint = self._font_small.render(
            "[← →] Choisir  [Entrée/Espace] Confirmer", True, TEXT_GRAY)
        surf.blit(hint, (SCREEN_W//2 - hint.get_width()//2,
                         self._counter_btn_rects[0].y - 18))

    # ── Feedbacks ─────────────────────────────────────────────────────────────

    def _draw_feedbacks(self, surf: pygame.Surface) -> None:
        visible = self._feedbacks[-3:]
        base_y  = self._layout["dialogue"].y - 8
        for i, fb in enumerate(reversed(visible)):
            col = (*fb.color[:3], fb.alpha)
            s   = self._font_small.render(fb.text[:62], True, col)
            surf.blit(s, (SCREEN_W//2 - s.get_width()//2, base_y - i * 20))

    def _draw_flash(self, surf: pygame.Surface) -> None:
        fl = self._flash
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((*fl.color[:3], fl.alpha))
        surf.blit(overlay, (0, 0))

    # ── Écran de fin ──────────────────────────────────────────────────────────

    def _draw_end_screen(self, surf: pygame.Surface) -> None:
        success = self._result == "success"
        col     = (50, 230, 110) if success else (220, 50, 50)
        title   = "SUSPECT CRAQUÉ" if success else "INTERROGATOIRE ÉCHOUÉ"
        line    = self.suspect.line_success if success else self.suspect.line_failure

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((*col, 120))
        surf.blit(overlay, (0, 0))

        BW, BH = 720, 210
        BX, BY = SCREEN_W//2 - BW//2, SCREEN_H//2 - BH//2
        box = pygame.Surface((BW, BH), pygame.SRCALPHA)
        box.fill((4, 6, 18, 235))
        surf.blit(box, (BX, BY))
        pygame.draw.rect(surf, col, pygame.Rect(BX, BY, BW, BH), 2, border_radius=10)

        title_s = self._font_title.render(title, True, col)
        surf.blit(title_s, (SCREEN_W//2 - title_s.get_width()//2, BY + 18))

        words = line.split()
        lines_out: list[str] = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if self._font_med.size(test)[0] < BW - 40:
                cur = test
            else:
                lines_out.append(cur); cur = w
        if cur:
            lines_out.append(cur)
        for i, ln in enumerate(lines_out[:3]):
            ls = self._font_med.render(ln, True, TEXT_MAIN)
            surf.blit(ls, (SCREEN_W//2 - ls.get_width()//2, BY + 72 + i * 26))

        ct_s = self._font_small.render(
            f"transition dans {max(1, int(self._end_timer)+1)}s…", True, TEXT_GRAY)
        surf.blit(ct_s, (SCREEN_W//2 - ct_s.get_width()//2, BY + BH - 26))


# ══════════════════════════════════════════════════════════════════════════════
# Debug console
# ══════════════════════════════════════════════════════════════════════════════

def print_suspect_summary(suspect_id: str) -> None:
    p = SUSPECTS[suspect_id]
    w = 60
    print("=" * w)
    print(f" {p.name}  ({p.role})")
    print("-" * w)
    print(f"  Résistance   : {p.resistance:.2f}")
    print(f"  Press ×{p.press_mult:.2f}  Bluff ×{p.bluff_mult:.2f} (p={p.bluff_p:.0%})"
          f"  Silence ×{p.silence_mult:.2f}")
    print(f"  Preuves contextuelles : {list(p.evidence_hints.keys())}")
    print(f"  Questions contre-interro : {len(p.counter_questions)}")
    print("=" * w)


if __name__ == "__main__":
    for sid in SUSPECTS:
        print_suspect_summary(sid)
        print()