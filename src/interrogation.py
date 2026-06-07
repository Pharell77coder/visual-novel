"""
interrogation.py — Mini-jeu d'interrogatoire
============================================

Suspects disponibles :
    "taro"     — Informateur, vulnérable au Silence
    "ferriere" — Capitaine corrompu, vulnérable au Bluff
    "natasha"  — Journaliste, vulnérable au Press (direct)
    "mira"     — Ex-analyste, vulnérable au Silence et Bluff
    "ghost"    — Viktor Selg, très résistant, vulnérable au Press ciblé
    "architect"— L'Architecte, résistance maximale, répond au Bluff
    "senator"  — Arnheim, ego immense, vulnérable au Bluff
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

PRESSURE_WIN   = 1.0
PRESSURE_DECAY = 0.0012
_PAD           = 14

_COST_PRESS   = 8.0
_COST_BLUFF   = 5.0
_COST_SILENCE = 2.0

_END_HOLD = 3.2

_BAR_MARKERS = (0.25, 0.50, 0.70, 0.85)

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
# Slot d'action
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
    resistance: float = 0.5
    press_mult:   float = 1.0
    bluff_mult:   float = 1.0
    silence_mult: float = 1.0
    bluff_p: float = 0.55
    expr: dict[str, int] = field(default_factory=dict)
    idle: dict[str, list[str]] = field(default_factory=dict)
    react_press:    list[str] = field(default_factory=list)
    react_bluff_ok: list[str] = field(default_factory=list)
    react_bluff_no: list[str] = field(default_factory=list)
    react_silence:  list[str] = field(default_factory=list)
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
    press_mult   = 1.20,
    bluff_mult   = 0.80,
    silence_mult = 1.45,
    bluff_p      = 0.42,
    expr = {
        "DÉFIANT":   1, "RÉSISTANT": 1,
        "NERVEUX":   3, "FISSURÉ":   3, "CRAQUANT":  3,
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
    press_mult   = 0.88,
    bluff_mult   = 1.35,
    silence_mult = 0.65,
    bluff_p      = 0.62,
    expr = {
        "DÉFIANT":   1, "RÉSISTANT": 1,
        "NERVEUX":   1, "FISSURÉ":   3, "CRAQUANT":  3,
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


# ══════════════════════════════════════════════════════════════════════════════
# Profil : Natasha Mori — Journaliste d'investigation
# ══════════════════════════════════════════════════════════════════════════════

NATASHA = SuspectProfile(
    id         = "natasha",
    name       = "Natasha Mori",
    role       = "Journaliste — Tribune International",
    resistance   = 0.38,
    press_mult   = 1.40,   # les faits directs la percutent : elle sait les reconnaître
    bluff_mult   = 0.70,   # elle détecte les bluffs, c'est son métier
    silence_mult = 1.10,   # le silence l'incite à remplir le vide
    bluff_p      = 0.32,   # très difficile à bluffer — flair de journaliste

    expr = {
        "DÉFIANT":   1, "RÉSISTANT": 1,
        "NERVEUX":   2, "FISSURÉ":   3, "CRAQUANT":  3,
    },

    idle = {
        "DÉFIANT": [
            "Je protège mes sources. C'est constitutionnel.",
            "Mon rédacteur en chef est au courant que je suis ici.",
            "Vous perdez votre temps. Et le mien.",
            "Je n'ai aucune obligation de vous parler.",
        ],
        "RÉSISTANT": [
            "Ce que vous me montrez ne me surprend pas autant que vous le croyez.",
            "J'ai travaillé deux ans sur cette histoire. Vous pensez que je n'ai rien ?",
            "Raven. Qu'est-ce que vous voulez vraiment ?",
            "Je suis journaliste. Je pose les questions, normalement.",
        ],
        "NERVEUX": [
            "D'accord. Il y a des choses que je n'ai pas publiées. Encore.",
            "Ce contact… je ne savais pas qui il était vraiment.",
            "Si c'est vrai ce que vous dites, alors moi aussi j'ai été manipulée.",
            "Combien de temps vous me demandez de garder ça ?",
        ],
        "FISSURÉ": [
            "Il m'a contactée il y a six mois. Il connaissait des détails impossibles.",
            "Je n'ai pas vérifié assez. C'est ma faute professionnelle.",
            "Il y a un document. Je l'ai. Mais je voulais le publier moi-même.",
            "Si je vous le donne, vous me garantissez quoi en échange ?",
        ],
        "CRAQUANT": [
            "Très bien. Je vais tout vous montrer. Mais on partage l'exclusivité.",
            "Le serveur miroir. J'ai l'adresse. Et la clé d'accès.",
            "Je savais que cette affaire était trop grosse pour une seule personne.",
            "On travaille ensemble ou on ne travaille pas. C'est ma condition.",
        ],
    },

    react_press = [
        "Cette preuve… elle est solide. Je dois l'admettre.",
        "D'où vous sortez ça ? Ce n'est pas dans mes dossiers.",
        "C'est du bon travail. Je peux pas le nier.",
        "Vous avez fait vos devoirs. Mieux que je ne le pensais.",
        "Ça, c'est vérifiable. Je vais devoir revoir ma position.",
    ],
    react_bluff_ok = [
        "Attendez… ce document existe vraiment ?",
        "Je croyais l'avoir. Il m'a échappé ?",
        "C'est cohérent avec ce que j'ai. Je vous crois.",
        "Vous bluffez peut-être. Mais la conclusion est juste.",
    ],
    react_bluff_no = [
        "Non. Ce document n'existe pas. J'aurais su.",
        "Essayez autre chose. Je connais chaque source sur cette affaire.",
        "Mauvais bluff, Raven. Même pour un détective.",
        "Je suis journaliste. Les fausses pistes, c'est mon quotidien.",
    ],
    react_silence = [
        "… Vous attendez quoi ? Que je parle en premier ?",
        "D'accord. Le silence. Classique.",
        "Très bien. Je peux attendre aussi. J'ai l'habitude des sources mutiques.",
        "Vous pensez que ça marche sur moi ? Peut-être un peu.",
        "Ce silence… il me rend nerveuse. Et ça m'énerve d'admettre ça.",
    ],

    line_success = (
        "D'accord, Raven. Je vous fais confiance. "
        "J'ai l'adresse du serveur miroir et la clé d'accès. "
        "Mais quand tout ça sera terminé, j'ai l'exclusivité. "
        "C'est non négociable."
    ),
    line_failure = (
        "Je n'ai rien à vous donner qui ne soit pas déjà public. "
        "Si vous avez d'autres questions, passez par mon avocat. "
        "Et publiez rien sans me prévenir."
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
# Profil : Mira Voss — Ex-analyste du Renseignement
# ══════════════════════════════════════════════════════════════════════════════

MIRA = SuspectProfile(
    id         = "mira",
    name       = "Mira Voss",
    role       = "Ex-analyste RG — Contact indépendant",
    resistance   = 0.50,
    press_mult   = 1.00,   # résiste bien aux confrontations directes
    bluff_mult   = 1.25,   # l'incertitude l'atteint : elle ne sait plus à qui faire confiance
    silence_mult = 1.30,   # le silence lui pèse, elle a besoin de clarté

    bluff_p      = 0.55,   # moyenne — elle analyse, mais doute d'elle-même

    expr = {
        "DÉFIANT":   1, "RÉSISTANT": 1,
        "NERVEUX":   2, "FISSURÉ":   3, "CRAQUANT":  3,
    },

    idle = {
        "DÉFIANT": [
            "Je suis venue ici de mon plein gré. Je peux partir de même.",
            "Ce que vous insinuez est faux.",
            "Vous doutez de moi. C'est normal. Mais vous avez tort.",
            "J'ai pris des risques que vous ne pouvez pas imaginer.",
        ],
        "RÉSISTANT": [
            "Qu'est-ce qui vous fait penser que je vous cache quelque chose ?",
            "La lacune dans mon dossier. Je vous l'ai dit : protection judiciaire.",
            "Si j'étais contre vous, je n'aurais pas mis cette clé USB sous votre porte.",
            "On travaille ensemble depuis des mois, Raven. Qu'est-ce qui a changé ?",
        ],
        "NERVEUX": [
            "D'accord. Il y a une partie que je ne vous ai pas encore dite.",
            "Mon directeur de cabinet… il ne m'a pas juste licenciée.",
            "J'avais peur de la réaction si vous saviez tout depuis le début.",
            "Ce n'est pas de la trahison. C'est de la prudence.",
        ],
        "FISSURÉ": [
            "Les dix-huit mois. J'étais en contact avec l'un des membres du réseau.",
            "Je pensais pouvoir double-jouer. Les retourner de l'intérieur.",
            "J'ai échoué. Et depuis, j'essaie de réparer.",
            "Je voulais vous le dire. J'attendais le bon moment.",
        ],
        "CRAQUANT": [
            "Très bien. Je vais tout vous dire. Depuis le début.",
            "Le contact à Berlin… ce n'est pas le premier à m'avoir approchée.",
            "J'ai un autre dossier. Plus complet. Je le gardais en réserve.",
            "Je ne suis pas votre ennemie, Raven. Je n'ai jamais été votre ennemie.",
        ],
    },

    react_press = [
        "Cette preuve… je ne la connaissais pas. C'est plus grave que je ne le pensais.",
        "D'accord. Vous avez raison sur ce point. Je ne peux pas le nier.",
        "Vous êtes allé plus loin que moi. Je dois l'admettre.",
        "Ce document change tout. Donnez-moi un moment.",
        "C'est solide. Je ne m'y attendais pas.",
    ],
    react_bluff_ok = [
        "Ce dossier existe ? Vous l'avez vraiment ?",
        "Je pensais que personne ne l'avait trouvé.",
        "Si c'est vrai, alors oui. On doit parler.",
        "Ça expliquerait beaucoup de choses que je n'arrivais pas à relier.",
    ],
    react_bluff_no = [
        "Non. Ce dossier n'existe pas sous cette forme. J'aurais su.",
        "Vous testez mes réactions. Je connais la technique.",
        "Je ne suis pas facile à manipuler, Raven. J'ai fait de l'analyse.",
        "Mauvaise piste. Mais l'intention était bonne.",
    ],
    react_silence = [
        "… Le silence. Vous voulez que je continue à parler seule.",
        "D'accord. Je comprends pourquoi vous faites ça.",
        "C'est efficace. Je dois l'admettre.",
        "Vous avez appris ça où ? Psychologie d'interrogatoire ?",
        "Très bien. Vous voulez de la vérité. Je vais vous en donner.",
    ],

    line_success = (
        "D'accord. Je vais tout vous dire — vraiment tout cette fois. "
        "Il y a un troisième dossier. Que je n'ai montré à personne. "
        "Il a les noms des sept protégés de l'Architecte. "
        "Je l'ai gardé parce que j'avais peur. J'aurais dû vous faire confiance plus tôt."
    ),
    line_failure = (
        "Je vous ai dit ce que je pouvais. "
        "Si ce n'est pas suffisant pour vous, "
        "je ne sais pas ce que vous attendez de moi. "
        "Bonne chance, Raven."
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
# Profil : Viktor Selg — "Le Fantôme"
# ══════════════════════════════════════════════════════════════════════════════

GHOST = SuspectProfile(
    id         = "ghost",
    name       = "Viktor Selg",
    role       = "Le Fantôme — Diplomate suédois, réseau Synarchie",
    resistance   = 0.80,
    press_mult   = 1.30,   # les faits concrets le déstabilisent — il n'est pas habitué à être acculé
    bluff_mult   = 0.60,   # il ne croit rien sans preuve, il a construit sa vie sur la méfiance
    silence_mult = 0.50,   # le silence ne l'atteint pas — il le pratique depuis trente ans

    bluff_p      = 0.28,   # presque impossible à bluffer — il a tout anticipé

    expr = {
        "DÉFIANT":   1, "RÉSISTANT": 1,
        "NERVEUX":   1, "FISSURÉ":   3, "CRAQUANT":  3,
    },

    idle = {
        "DÉFIANT": [
            "Détective Raven. C'est décevant de finir ainsi.",
            "Vous n'avez rien qui tienne devant un tribunal européen.",
            "J'ai trente ans d'impunité derrière moi. Vous croyez que ça s'arrête là ?",
            "Mon équipe d'avocats est meilleure que tout ce qu'Interpol peut aligner.",
        ],
        "RÉSISTANT": [
            "Genève était un sacrifice. Ferrière, Arnheim — des sacrifices.",
            "Ce que vous appelez des preuves, moi j'appelle ça des artefacts.",
            "Vous avez une heure. Après, mon avion décolle.",
            "Chaque document que vous avez a une explication légale. Je les ai toutes préparées.",
        ],
        "NERVEUX": [
            "Le serveur de Berlin. Comment vous l'avez trouvé ?",
            "Le contact… il a parlé. Voilà qui est intéressant.",
            "Vous êtes plus rapide que je ne le pensais. Mes félicitations.",
            "Certains détails que vous citez… ils ne devraient pas exister sous cette forme.",
        ],
        "FISSURÉ": [
            "D'accord. Vous avez fait du bon travail. Je l'admets.",
            "L'Architecte vous a utilisé. Comme il nous a tous utilisés.",
            "Je ne suis pas le monstre de cette histoire. Je suis l'exécutant.",
            "Si je parle… il y a des gens qui ne resteront pas passifs.",
        ],
        "CRAQUANT": [
            "Très bien. On peut parler. Mais uniquement de ce qui m'implique directement.",
            "L'Architecte. Son vrai nom. Vous voulez ça, n'est-ce pas ?",
            "Je peux vous donner sept noms. Ceux qu'il vous manque encore.",
            "Mais je veux une garantie écrite avant de prononcer un seul mot de plus.",
        ],
    },

    react_press = [
        "Ce document… D'où il sort ? Ce n'était pas censé exister.",
        "Vous avez accès à des sources que je croyais sécurisées. Impressionnant.",
        "C'est solide. Je ne vais pas prétendre le contraire.",
        "Voilà une preuve que je n'avais pas anticipée.",
        "Bien. Vous avez fait vos devoirs. Je dois réévaluer ma position.",
    ],
    react_bluff_ok = [
        "Ce rapport… comment vous avez pu l'obtenir ?",
        "Ça ne devrait pas exister. Mais si c'est vrai…",
        "D'accord. Peut-être que je vous ai sous-estimé.",
        "Je dois vérifier ça. Donnez-moi un moment.",
    ],
    react_bluff_no = [
        "Non. Ce document est une fabrication. Et je sais pourquoi.",
        "Vous bluffez. Je le vois à la façon dont vous le tenez.",
        "Mauvaise tentative. Je connais chaque pièce du dossier réel.",
        "J'ai construit ma vie sur la détection du mensonge. Essayez encore.",
    ],
    react_silence = [
        "… Intéressant. Vous pensez que le silence me dérange.",
        "J'ai passé trente ans à parler à des gens puissants dans des pièces silencieuses.",
        "Prenez votre temps.",
        "Ce silence ne m'affecte pas. Je l'utilise comme vous.",
        "Vous perdez du temps précieux.",
    ],

    line_success = (
        "Très bien. Je vais parler. "
        "Pas par peur. Par calcul. "
        "L'Architecte m'a sacrifié comme il a sacrifié Ferrière. "
        "Son vrai nom : Constantine Havel. "
        "Et il est toujours libre. Voilà votre prochaine cible."
    ),
    line_failure = (
        "Le temps est écoulé. "
        "Mon avion décolle dans quarante minutes. "
        "Et vous n'avez rien qui puisse m'arrêter légalement. "
        "Au revoir, détective."
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
# Profil : L'Architecte — Constantine Havel
# ══════════════════════════════════════════════════════════════════════════════

ARCHITECT = SuspectProfile(
    id         = "architect",
    name       = "L'Architecte",
    role       = "Constantine Havel — Fondateur Synarchie",
    resistance   = 0.90,   # résistance maximale — il a tout vu venir
    press_mult   = 0.70,   # les preuves directes l'intéressent mais ne le déstabilisent pas
    bluff_mult   = 1.50,   # son ego le rend paradoxalement sensible à la manipulation ciblée
    silence_mult = 0.40,   # le silence ne l'atteint pas — il pense toujours au coup suivant

    bluff_p      = 0.70,   # surestime ses propres certitudes, peut être trompé sur les détails

    expr = {
        "DÉFIANT":   0, "RÉSISTANT": 1,
        "NERVEUX":   1, "FISSURÉ":   2, "CRAQUANT":  3,
    },

    idle = {
        "DÉFIANT": [
            "Raven. Nous voici au terme de quelque chose d'assez remarquable.",
            "Vous avez nettoyé ce que je ne pouvais pas nettoyer moi-même. Merci.",
            "Je ne suis pas en position de faiblesse. Je suis en position d'observation.",
            "Ce que vous appelez une arrestation, j'appelle ça un déménagement.",
        ],
        "RÉSISTANT": [
            "Les preuves que vous avez ne couvrent que ce que j'ai voulu exposer.",
            "L'iceberg. Vous avez la pointe. Le reste est intact.",
            "Trente ans. Vingt-trois pays. Deux cents personnes. Tout ça reste opérationnel.",
            "Vous pensez avoir gagné. C'est touchant.",
        ],
        "NERVEUX": [
            "Ce document… Vane l'a vraiment conservé ? C'est étonnant.",
            "Je dois admettre que vous m'avez surpris sur quelques points.",
            "Le testament. Je croyais l'avoir neutralisé il y a sept ans.",
            "Vous avez accès à des sources que je croyais définitivement fermées.",
        ],
        "FISSURÉ": [
            "Très bien. Admettons que vous ayez plus que je ne le pensais.",
            "Qu'est-ce que vous voulez réellement, Raven ? Pas la prison. La vérité ?",
            "Je peux vous donner ce que personne d'autre n'a jamais eu.",
            "Nous pourrions avoir une conversation productive. Si vous en êtes capable.",
        ],
        "CRAQUANT": [
            "D'accord. Je parle. Pas parce que vous m'y forcez.",
            "Parce que cette organisation mérite mieux que de mourir avec moi.",
            "Il y a des choses que vous devriez savoir sur la vraie nature du réseau.",
            "Je peux vous donner les sept noms. Et la preuve de ce qu'ils ont fait.",
        ],
    },

    react_press = [
        "Ce document… c'est du travail sérieux. Je l'admets.",
        "Vane a été plus prévoyant que je ne le croyais.",
        "Vous avez cette pièce. D'accord. Ça change légèrement l'équilibre.",
        "Intéressant. Vous avez accès à ça.",
        "Cette preuve est réelle. Je ne vais pas la nier.",
    ],
    react_bluff_ok = [
        "Vous avez ça ? Vraiment ? Ça m'étonne.",
        "Ce dossier… je pensais qu'il avait été détruit.",
        "D'accord. Si vous avez ça, alors on peut parler différemment.",
        "Vous m'avez surpris. C'est rare. Profitez-en.",
    ],
    react_bluff_no = [
        "Non. Ce document n'existe pas sous cette forme.",
        "Essayez encore. Mais sans me faire perdre mon temps.",
        "Vous bluffez. Et vous le faites mal.",
        "J'ai construit des systèmes de désinformation pendant trente ans. Je reconnais la technique.",
    ],
    react_silence = [
        "Le silence. Vous pensez que ça m'affecte.",
        "… Je l'utilise depuis trente ans. Il me connaît bien.",
        "Prenez le temps qu'il vous faut.",
        "Ce silence ne m'inquiète pas. Rien ne m'inquiète.",
        "Quand vous serez prêt, nous reprendrons.",
    ],

    line_success = (
        "Très bien. Puisque vous insistez. "
        "Les sept noms que vous n'avez pas encore : "
        "deux chefs d'État, trois directeurs de banque centrale, deux juges internationaux. "
        "Je vous les donne. "
        "Pas par peur. Par respect pour ce que vous avez accompli. "
        "Et parce que cette organisation mérite une fin digne."
    ),
    line_failure = (
        "Vous avez fait du travail remarquable, Raven. "
        "Mais vous n'avez pas assez. "
        "Ce qui reste de la Synarchie survivra. "
        "Et moi aussi, probablement."
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
# Profil : Sénateur Arnheim — Législateur corrompu
# ══════════════════════════════════════════════════════════════════════════════

SENATOR = SuspectProfile(
    id         = "senator",
    name       = "Sénateur Arnheim",
    role       = "Délégué sécurité transnationale — Synarchie",
    resistance   = 0.62,
    press_mult   = 0.90,   # supporte bien les preuves directes — il a des avocats
    bluff_mult   = 1.55,   # ego démesuré : il croit toujours savoir plus que l'adversaire
    silence_mult = 0.80,   # le silence l'impatiente, mais pas au point de le briser seul

    bluff_p      = 0.68,   # ego = vulnérabilité : facile à manipuler sur ses certitudes

    expr = {
        "DÉFIANT":   1, "RÉSISTANT": 1,
        "NERVEUX":   2, "FISSURÉ":   3, "CRAQUANT":  3,
    },

    idle = {
        "DÉFIANT": [
            "Vous réalisez à qui vous parlez ? J'ai l'immunité parlementaire.",
            "Cette conversation n'a aucune valeur légale.",
            "J'ai voté des lois qui protègent les gens comme moi des gens comme vous.",
            "Mon bureau de communication va adorer cette histoire.",
        ],
        "RÉSISTANT": [
            "Ce compte en Lettonie… c'est un fonds de prévoyance légal. Mon comptable confirmera.",
            "Vous confondez influence et corruption. Ce n'est pas la même chose.",
            "J'ai servi ce pays pendant dix-huit ans. Dix-huit ans.",
            "Selg est un conseiller parmi d'autres. Je ne contrôle pas leurs activités.",
        ],
        "NERVEUX": [
            "D'où vous sortez cet enregistrement ? Il est tronqué, évidemment.",
            "Ce que vous interprétez comme des ordres, c'est du conseil stratégique.",
            "Mes avocats vont contester chaque élément de ce dossier.",
            "Il y a des gens qui n'apprécieront pas que vous poursuiviez cette enquête.",
        ],
        "FISSURÉ": [
            "D'accord. J'ai eu des contacts avec Selg. Ce n'est pas un crime.",
            "La banque lettone… c'était avant que je sache ce que le réseau faisait vraiment.",
            "Je n'ai pas commandité de crime. J'ai fermé les yeux. Ce n'est pas pareil.",
            "Si je coopère, qu'est-ce que vous pouvez garantir ?",
        ],
        "CRAQUANT": [
            "Très bien. Je vais vous donner quelque chose.",
            "Il y a deux autres sénateurs. Dans le réseau depuis plus longtemps que moi.",
            "Et un magistrat à la Cour pénale internationale. Je les ai vus à Genève.",
            "Mais je veux que ma coopération soit notée. Par écrit. Maintenant.",
        ],
    },

    react_press = [
        "Ce document… d'où il sort ? Il ne devrait pas exister.",
        "Voilà qui est plus solide que je ne le pensais.",
        "Ce compte… les montants ne correspondent pas exactement à ce que…",
        "C'est compromettant. Je dois l'admettre.",
        "Vous avez de bonnes sources. Meilleures que celles de mon équipe.",
    ],
    react_bluff_ok = [
        "Vous avez le relevé complet ? Comment c'est possible ?",
        "Ce rapport d'Interpol… il est officiel ?",
        "D'accord. Si vous avez ça, alors la situation est différente.",
        "Je ne savais pas que ce dossier existait encore sous cette forme.",
    ],
    react_bluff_no = [
        "Ce document est un faux. Je l'aurais su s'il existait.",
        "Vous bluffez. Et vous n'avez pas le niveau pour ça face à moi.",
        "J'ai vu passer mille dossiers dans ma carrière. Celui-là sent le vide.",
        "Essayez autre chose. Ceci ne marche pas.",
    ],
    react_silence = [
        "Vous attendez quelque chose ? Dites-le.",
        "… Le silence. Très professionnel.",
        "Je ne suis pas intimidé par les pauses, inspecteur.",
        "Mon temps vaut beaucoup. Ne le gaspillez pas.",
        "Vous voulez que je parle en premier. C'est non.",
    ],

    line_success = (
        "D'accord. Voilà ce que vous voulez : "
        "deux sénateurs, un magistrat international. "
        "Et les détails du financement de la commission de Berlin. "
        "Mais je veux un accord. Maintenant. Avant de dire un mot de plus."
    ),
    line_failure = (
        "Cette conversation n'a jamais eu lieu. "
        "Mon avocat déposera une plainte d'ici une heure. "
        "Et vous ferez face à des accusations de harcèlement d'élu. "
        "Bonne journée, inspecteur."
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
# Registre
# ══════════════════════════════════════════════════════════════════════════════

SUSPECTS: dict[str, SuspectProfile] = {
    "taro":     TARO,
    "ferriere": FERRIERE,
    "natasha":  NATASHA,
    "mira":     MIRA,
    "ghost":    GHOST,
    "architect": ARCHITECT,
    "senator":  SENATOR,
}


# ══════════════════════════════════════════════════════════════════════════════
# Mini-jeu principal
# ══════════════════════════════════════════════════════════════════════════════

class InterrogationMinigame:
    """
    Mini-jeu d'interrogatoire.
    Suspects disponibles : taro, ferriere, natasha, mira, ghost, architect, senator
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

        self.pressure   = 0.0
        self.state      = SuspectState.DEFIANT
        self.actions    = _build_actions()

        self._line         = self._idle_line()
        self._line_timer   = 0.0
        self._line_delay   = 4.5

        self._feedbacks: list[_Feedback] = []
        self._flash: Optional[_ScreenFlash] = None
        self._pressure_pulse = 0.0

        self._result: Optional[str] = None
        self._end_timer = _END_HOLD

        self._portrait_shake   = 0.0
        self._portrait_shake_t = 0.0

        self._font_title = getattr(assets, "font_title", None) or \
                           pygame.font.SysFont("monospace", 28, bold=True)
        self._font_big   = getattr(assets, "font_big",   None) or \
                           pygame.font.SysFont("monospace", 22, bold=True)
        self._font_med   = getattr(assets, "font_med",   None) or \
                           pygame.font.SysFont("monospace", 16)
        self._font_small = getattr(assets, "font_small", None) or \
                           pygame.font.SysFont("monospace", 12)

        self._bg = getattr(assets, "bg", {}).get("salle_interrogatoire", None)

        self._layout: dict[str, pygame.Rect] = {}
        self._btn_rects: list[pygame.Rect]   = []
        self._compute_layout()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _compute_layout(self) -> None:
        W, H = SCREEN_W, SCREEN_H
        self._layout["header"]    = pygame.Rect(0, 0, W, 46)
        self._layout["portrait"]  = pygame.Rect(12, 52, 288, 320)
        self._layout["pressure"]  = pygame.Rect(315, 64, 580, 22)
        self._timer_center = (880, 148)
        self._timer_radius = 52
        self._layout["state_badge"] = pygame.Rect(12, 378, 288, 30)
        self._layout["dialogue"]    = pygame.Rect(12, 415, W - 24, 62)

        BTN_W, BTN_H = 198, 58
        GAP          = 22
        total_w      = 3 * BTN_W + 2 * GAP
        bx           = (W - total_w) // 2
        by           = H - BTN_H - 8
        self._btn_rects = [
            pygame.Rect(bx + i * (BTN_W + GAP), by, BTN_W, BTN_H)
            for i in range(3)
        ]
        self._hint_y = by - 18

    # ── Dialogue helpers ──────────────────────────────────────────────────────

    def _idle_line(self) -> str:
        label = _STATE_META[self.state][0]
        lines = self.suspect.idle.get(label, ["…"])
        return random.choice(lines)

    def _set_line(self, text: str) -> None:
        self._line       = text
        self._line_timer = 0.0

    # ── Actions ───────────────────────────────────────────────────────────────

    def _do_press(self) -> _Feedback:
        base  = random.uniform(0.10, 0.18)
        if self.state == SuspectState.DEFIANT and self.suspect.resistance > 0.6:
            base *= 0.65
        delta = base * self.suspect.press_mult
        self.pressure = min(1.0, self.pressure + delta)
        self.time_left = max(0.0, self.time_left - _COST_PRESS)
        self._start_shake(0.6)
        self._flash = _ScreenFlash(RED_ACCENT)
        return _Feedback(random.choice(self.suspect.react_press), (255, 190, 190), positive=True)

    def _do_bluff(self) -> _Feedback:
        success = random.random() < self.suspect.bluff_p
        self.time_left = max(0.0, self.time_left - _COST_BLUFF)
        if success:
            delta = random.uniform(0.15, 0.22) * self.suspect.bluff_mult
            self.pressure = min(1.0, self.pressure + delta)
            self._flash = _ScreenFlash(GOLD)
            self._start_shake(1.0)
            return _Feedback(random.choice(self.suspect.react_bluff_ok), (200, 255, 140), positive=True)
        else:
            penalty = random.uniform(0.04, 0.09)
            self.pressure = max(0.0, self.pressure - penalty)
            self._flash = _ScreenFlash(PINK_ACCENT)
            return _Feedback(random.choice(self.suspect.react_bluff_no), (255, 140, 100), positive=False)

    def _do_silence(self) -> _Feedback:
        base  = random.uniform(0.03, 0.07) * self.suspect.silence_mult
        self.pressure = min(1.0, self.pressure + base)
        self.time_left = max(0.0, self.time_left - _COST_SILENCE)
        return _Feedback(random.choice(self.suspect.react_silence), (150, 220, 255), positive=True)

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

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt: float, events: list[pygame.event.Event]) -> Optional[Literal["success", "failure"]]:
        if self._result is not None:
            self._end_timer -= dt
            if self._end_timer <= 0.0:
                return self._result
            return None

        self.time_left = max(0.0, self.time_left - dt)
        self.pressure = max(0.0, self.pressure - PRESSURE_DECAY * dt)

        for slot in self.actions:
            slot.tick(dt)

        self._feedbacks = [f for f in self._feedbacks if f.alive]
        for f in self._feedbacks:
            f.tick(dt)

        if self._flash and self._flash.alive:
            self._flash.tick(dt)

        if self._portrait_shake > 0:
            self._portrait_shake_t += dt * 30
            self._portrait_shake = max(0.0, self._portrait_shake - dt * 8)

        self._pressure_pulse = (self._pressure_pulse + dt * 3) % (2 * math.pi)

        self._line_timer += dt
        if self._line_timer >= self._line_delay:
            self._line_timer = 0.0
            self._line       = self._idle_line()

        self.state = _state_from(self.pressure)

        if self.pressure >= PRESSURE_WIN:
            self._result   = "success"
            self._end_timer = _END_HOLD
            self._set_line(self.suspect.line_success)
            self._flash = _ScreenFlash((50, 230, 110))
            return None

        if self.time_left <= 0.0:
            self._result   = "failure"
            self._end_timer = _END_HOLD
            self._set_line(self.suspect.line_failure)
            self._flash = _ScreenFlash(RED_ACCENT)
            return None

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

    # ── Draw ──────────────────────────────────────────────────────────────────

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
            a = i * 8
            vig = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            pygame.draw.ellipse(vig, (0, 0, 0, a),
                                pygame.Rect(SCREEN_W // 2 - r, SCREEN_H // 2 - r // 2, r * 2, r))
            surf.blit(vig, (0, 0))

    def _draw_header(self, surf: pygame.Surface) -> None:
        bar = pygame.Surface((SCREEN_W, 46), pygame.SRCALPHA)
        bar.fill((4, 6, 18, 240))
        surf.blit(bar, (0, 0))
        pygame.draw.line(surf, CYAN, (0, 46), (SCREEN_W, 46), 1)
        title_str = f"INTERROGATOIRE — {self.suspect.name.upper()}"
        title_s   = self._font_title.render(title_str, True, CYAN)
        surf.blit(title_s, (SCREEN_W // 2 - title_s.get_width() // 2, 8))
        role_s = self._font_small.render(self.suspect.role, True, TEXT_GRAY)
        surf.blit(role_s, (SCREEN_W - role_s.get_width() - _PAD, 16))

    def _draw_portrait(self, surf: pygame.Surface) -> None:
        rect = self._layout["portrait"]
        state_label, state_col = _STATE_META[self.state]
        expr_idx = self.suspect.expr.get(state_label, 0)

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
            ph = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            ph.fill((*state_col, 25))
            pygame.draw.rect(ph, state_col, ph.get_rect(), 2, border_radius=8)
            surf.blit(ph, (rect.x + shake_x, rect.y))
            n_s = self._font_med.render(self.suspect.name, True, state_col)
            surf.blit(n_s, (
                rect.x + shake_x + rect.w // 2 - n_s.get_width() // 2,
                rect.y + rect.h // 2,
            ))

        glow_a = int(60 + 80 * self.pressure)
        pygame.draw.rect(surf, (*state_col, glow_a), rect.inflate(4, 4), 2, border_radius=6)

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
        pct   = int(self.pressure * 100)
        label = self._font_small.render(
            f"PRESSION PSYCHOLOGIQUE  {pct} %", True, TEXT_NAME
        )
        surf.blit(label, (rect.x, rect.y - 18))

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
                    r = int(40  + 20  * t * 2)
                    g = int(80  + 140 * t * 2)
                    b = 220
                elif t < 0.70:
                    f = (t - 0.50) / 0.20
                    r = int(60  + 160 * f)
                    g = 220
                    b = int(220 - 160 * f)
                elif t < 0.85:
                    f = (t - 0.70) / 0.15
                    r = int(220 + 35  * f)
                    g = int(220 - 100 * f)
                    b = int(60  - 40  * f)
                else:
                    f = (t - 0.85) / 0.15
                    r = 255
                    g = int(120 - 120 * f)
                    b = max(0, int(20 - 20 * f))
                pygame.draw.line(fill, (r, g, b, 235), (i, 0), (i, rect.h - 1))
            surf.blit(fill, rect.topleft)

        if self.pressure > 0.05:
            pulse_a = int(80 + 60 * math.sin(self._pressure_pulse))
            pw      = min(4, fill_w)
            if pw > 0:
                pulse_r = pygame.Rect(rect.x + fill_w - pw, rect.y, pw, rect.h)
                ps      = pygame.Surface((pw, rect.h), pygame.SRCALPHA)
                ps.fill((255, 255, 255, pulse_a))
                surf.blit(ps, pulse_r.topleft)

        for threshold in _BAR_MARKERS:
            mx = rect.x + int(rect.w * threshold)
            pygame.draw.line(surf, (160, 165, 210),
                             (mx, rect.y - 5), (mx, rect.y + rect.h + 5), 1)

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

        secs  = int(self.time_left)
        m, s  = divmod(secs, 60)
        t_str = f"{m:02d}:{s:02d}"
        t_s   = self._font_big.render(t_str, True, col)
        surf.blit(t_s, (cx - t_s.get_width() // 2, cy - t_s.get_height() // 2))
        lbl = self._font_small.render("TEMPS", True, TEXT_GRAY)
        surf.blit(lbl, (cx - lbl.get_width() // 2, cy + R + 4))

    def _draw_stat_details(self, surf: pygame.Surface) -> None:
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

        name_s = self._font_small.render(
            f"[ {self.suspect.name.upper()} ]", True, TEXT_NAME
        )
        surf.blit(name_s, (rect.x + 10, rect.y + 7))

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

            btn_bg = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            bg_a   = 35 if slot.ready else 18
            btn_bg.fill((*col[:3], bg_a))
            surf.blit(btn_bg, rect.topleft)

            border_col = col if slot.ready else (70, 75, 90)
            pygame.draw.rect(surf, border_col, rect, 2, border_radius=6)

            key_char = {"press": "A", "bluff": "Z", "silence": "E"}[slot.name]
            key_s = self._font_small.render(f"[{key_char}]", True, (*dim_col, dim_a))
            surf.blit(key_s, (rect.x + 8, rect.y + 8))

            name_s = self._font_med.render(slot.label, True, (*dim_col, dim_a))
            surf.blit(name_s, (
                rect.x + rect.w // 2 - name_s.get_width() // 2,
                rect.y + 8,
            ))

            desc_s = self._font_small.render(
                slot.desc[:28], True, (*TEXT_GRAY[:3], dim_a)
            )
            surf.blit(desc_s, (
                rect.x + rect.w // 2 - desc_s.get_width() // 2,
                rect.y + rect.h - 20,
            ))

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
                        pts.append((acx + ar * math.cos(a), acy + ar * math.sin(a)))
                    if len(pts) >= 3:
                        pygame.draw.polygon(surf, col, pts)
                pygame.draw.circle(surf, (8, 10, 22), (acx, acy), ar - 5)
                cd_s = self._font_small.render(f"{slot.cd_remain:.0f}", True, col)
                surf.blit(cd_s, (acx - cd_s.get_width() // 2, acy - cd_s.get_height() // 2))

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

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((*col, 120))
        surf.blit(overlay, (0, 0))

        BW, BH = 720, 210
        BX, BY = SCREEN_W // 2 - BW // 2, SCREEN_H // 2 - BH // 2
        box = pygame.Surface((BW, BH), pygame.SRCALPHA)
        box.fill((4, 6, 18, 235))
        surf.blit(box, (BX, BY))
        pygame.draw.rect(surf, col, pygame.Rect(BX, BY, BW, BH), 2, border_radius=10)

        title_s = self._font_title.render(title, True, col)
        surf.blit(title_s, (SCREEN_W // 2 - title_s.get_width() // 2, BY + 18))

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

        ct  = max(1, int(self._end_timer) + 1)
        ct_s = self._font_small.render(f"transition dans {ct}s…", True, TEXT_GRAY)
        surf.blit(ct_s, (SCREEN_W // 2 - ct_s.get_width() // 2, BY + BH - 26))


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
    for sid in SUSPECTS:
        print_suspect_summary(sid)
        print()