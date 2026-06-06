"""
transitions.py — Système de transitions visuelles pour Nuit Sans Témoin
=======================================================================

Usage depuis script.py :
    {"id": "sc_02", "bg": "bureau", "transition": "iris",       ...}
    {"id": "sc_03", "bg": "rue",    "transition": "fade_black", ...}
    {"id": "sc_04", "bg": "metro",  "transition": "slide_left", ...}
    {"id": "sc_05", "bg": "quai",   "transition": "fade_white", ...}
    (sans clé "transition" → FadeBlack par défaut)

Usage depuis VNEngine (main.py) :
    # Dans _load_node()
    tr_name = node.get("transition", "fade_black")
    self.transition = Transition.create(tr_name, self.screen.get_size())

    # Dans _update_game(dt)
    if self.transition:
        done = self.transition.update(dt)
        if done:
            self.transition = None

    # Dans _draw_game()
    self._draw_background()
    self._draw_characters()
    self._draw_ui()
    if self.transition:
        self.transition.draw(self.screen, self._prev_surface)

Convention :
    • update(dt: float) → bool   True quand l'animation est terminée
    • draw(screen, prev_surf)     prev_surf = capture de la scène précédente
    • Capturer prev_surf AVANT de charger la nouvelle scène :
        self._prev_surface = self.screen.copy()
        self._load_node(next_id)
        self.transition = Transition.create(...)
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Tuple

import pygame

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------
Size = Tuple[int, int]
Surface = pygame.Surface


# ---------------------------------------------------------------------------
# Classe de base
# ---------------------------------------------------------------------------

class Transition(ABC):
    """
    Classe abstraite dont héritent toutes les transitions.

    Attributs communs
    -----------------
    duration : float    Durée totale en secondes
    elapsed  : float    Temps écoulé depuis le début
    progress : float    Progression normalisée [0.0, 1.0]
    done     : bool     True quand la transition est achevée
    """

    REGISTRY: dict[str, type["Transition"]] = {}

    def __init__(self, size: Size, duration: float = 0.55) -> None:
        self.size = size
        self.duration = duration
        self.elapsed = 0.0
        self.progress = 0.0
        self.done = False

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def create(cls, name: str, size: Size, **kwargs) -> "Transition":
        """
        Instancie une transition par son nom.

        >>> tr = Transition.create("iris", (1280, 720))
        >>> tr = Transition.create("slide_left", (1280, 720), duration=0.4)
        """
        key = name.lower().strip()
        klass = cls.REGISTRY.get(key)
        if klass is None:
            available = ", ".join(cls.REGISTRY.keys())
            raise ValueError(
                f"Transition inconnue : '{name}'. "
                f"Valeurs disponibles : {available}"
            )
        return klass(size, **kwargs)

    @classmethod
    def register(cls, name: str):
        """Décorateur pour enregistrer une sous-classe dans le REGISTRY."""
        def decorator(klass):
            cls.REGISTRY[name.lower()] = klass
            return klass
        return decorator

    # ------------------------------------------------------------------
    # Interface publique
    # ------------------------------------------------------------------

    def update(self, dt: float) -> bool:
        """
        Avance l'animation de dt secondes.
        Retourne True quand la transition est terminée.
        """
        if self.done:
            return True
        self.elapsed = min(self.elapsed + dt, self.duration)
        self.progress = self.elapsed / self.duration if self.duration > 0 else 1.0
        if self.elapsed >= self.duration:
            self.done = True
        return self.done

    @abstractmethod
    def draw(self, screen: Surface, prev_surf: Surface) -> None:
        """
        Compose la frame de transition sur screen.

        Parameters
        ----------
        screen    : surface cible (la scène courante est déjà dessinée dessus)
        prev_surf : capture de la scène précédente (fournie par VNEngine)
        """

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def ease_in_out(t: float) -> float:
        """Courbe ease-in-out cubique : lent → rapide → lent."""
        return t * t * (3.0 - 2.0 * t)

    @staticmethod
    def ease_in(t: float) -> float:
        """Accélération quadratique."""
        return t * t

    @staticmethod
    def ease_out(t: float) -> float:
        """Décélération quadratique."""
        return 1.0 - (1.0 - t) * (1.0 - t)

    def _make_overlay(self, color: Tuple[int, int, int], alpha: int) -> Surface:
        """Crée une surface plein-écran colorée semi-transparente."""
        surf = pygame.Surface(self.size, pygame.SRCALPHA)
        surf.fill((*color, alpha))
        return surf


# ---------------------------------------------------------------------------
# FadeBlack — fondu au noir (défaut)
# ---------------------------------------------------------------------------

@Transition.register("fade_black")
class FadeBlack(Transition):
    """
    Fondu noir classique : scène précédente → noir → nouvelle scène.

    Phase 0→0.5 : sortie (prev_surf → noir)
    Phase 0.5→1 : entrée (noir → scène courante)

    Recommandé pour : changements de lieu importants, ellipses temporelles,
                      transitions entre actes.
    """

    def __init__(self, size: Size, duration: float = 0.7) -> None:
        super().__init__(size, duration)
        self._black = pygame.Surface(size)
        self._black.fill((0, 0, 0))

    def draw(self, screen: Surface, prev_surf: Surface) -> None:
        t = self.ease_in_out(self.progress)

        if t < 0.5:
            # Phase sortie : prev_surf qui s'assombrit
            fade_out = self.ease_in_out(t * 2.0)            # 0 → 1 sur la 1re moitié
            screen.blit(prev_surf, (0, 0))
            self._black.set_alpha(int(fade_out * 255))
            screen.blit(self._black, (0, 0))
        else:
            # Phase entrée : nouvelle scène qui émerge du noir
            fade_in = self.ease_out((t - 0.5) * 2.0)        # 0 → 1 sur la 2e moitié
            # screen contient déjà la nouvelle scène (dessinée par VNEngine)
            self._black.set_alpha(int((1.0 - fade_in) * 255))
            screen.blit(self._black, (0, 0))


# ---------------------------------------------------------------------------
# FadeWhite — fondu au blanc
# ---------------------------------------------------------------------------

@Transition.register("fade_white")
class FadeWhite(Transition):
    """
    Fondu blanc : effet d'éblouissement ou de flashback.

    Recommandé pour : révélations, flashbacks, dénouements émotionnels,
                      scènes en plein air avec lumière intense.
    """

    def __init__(self, size: Size, duration: float = 0.65) -> None:
        super().__init__(size, duration)
        self._white = pygame.Surface(size)
        self._white.fill((255, 255, 255))

    def draw(self, screen: Surface, prev_surf: Surface) -> None:
        t = self.ease_in_out(self.progress)

        if t < 0.5:
            fade_out = self.ease_in(t * 2.0)
            screen.blit(prev_surf, (0, 0))
            self._white.set_alpha(int(fade_out * 255))
            screen.blit(self._white, (0, 0))
        else:
            fade_in = self.ease_out((t - 0.5) * 2.0)
            self._white.set_alpha(int((1.0 - fade_in) * 255))
            screen.blit(self._white, (0, 0))


# ---------------------------------------------------------------------------
# Iris — ouverture/fermeture circulaire
# ---------------------------------------------------------------------------

@Transition.register("iris")
class Iris(Transition):
    """
    Fermeture en iris puis ouverture : cercle noir qui se rétracte / s'élargit.

    Le centre de l'iris est configurable (défaut : centre de l'écran,
    mais on peut le pointer sur un personnage ou un objet).

    Parameters
    ----------
    center : (x, y) ou None   Centre de l'iris en pixels. None = centre écran.
    duration : float           Durée totale.

    Recommandé pour : révélations dramatiques, fin de scène intimiste,
                      transitions « à l'ancienne » (genre noir).
    """

    def __init__(
        self,
        size: Size,
        duration: float = 0.75,
        center: Tuple[int, int] | None = None,
    ) -> None:
        super().__init__(size, duration)
        self.center = center or (size[0] // 2, size[1] // 2)
        # Rayon max : doit couvrir le coin le plus éloigné du centre
        cx, cy = self.center
        w, h = size
        corners = [(0, 0), (w, 0), (0, h), (w, h)]
        self._max_radius = int(
            max(math.hypot(cx - x, cy - y) for x, y in corners) + 2
        )
        # Surface de masque réutilisable
        self._mask = pygame.Surface(size, pygame.SRCALPHA)

    def draw(self, screen: Surface, prev_surf: Surface) -> None:
        t = self.ease_in_out(self.progress)
        self._mask.fill((0, 0, 0, 0))   # transparent

        if t < 0.5:
            # Fermeture : rayon qui diminue sur prev_surf
            close_t = self.ease_in(1.0 - t * 2.0)          # 1 → 0
            radius = int(close_t * self._max_radius)
            screen.blit(prev_surf, (0, 0))
            # Masque noir plein, puis on découpe un cercle transparent
            self._mask.fill((0, 0, 0, 255))
            if radius > 0:
                pygame.draw.circle(self._mask, (0, 0, 0, 0), self.center, radius)
            screen.blit(self._mask, (0, 0))
        else:
            # Ouverture : rayon qui grandit sur la nouvelle scène
            open_t = self.ease_out((t - 0.5) * 2.0)        # 0 → 1
            radius = int(open_t * self._max_radius)
            # Fond noir, cercle transparent laissant voir la nouvelle scène
            self._mask.fill((0, 0, 0, 255))
            if radius > 0:
                pygame.draw.circle(self._mask, (0, 0, 0, 0), self.center, radius)
            screen.blit(self._mask, (0, 0))


# ---------------------------------------------------------------------------
# SlideLeft — glissement horizontal
# ---------------------------------------------------------------------------

@Transition.register("slide_left")
class SlideLeft(Transition):
    """
    La nouvelle scène entre par la droite et pousse l'ancienne vers la gauche.

    Recommandé pour : passage au chapitre suivant, déplacements spatiaux
                      (ex : on quitte le bureau pour aller dans la rue),
                      transitions d'action rapides.

    Le paramètre `parallax` ajoute un léger décalage différentiel entre
    les deux surfaces pour simuler une profondeur (0.0 = aucun, 0.3 = marqué).
    """

    def __init__(
        self,
        size: Size,
        duration: float = 0.45,
        parallax: float = 0.15,
    ) -> None:
        super().__init__(size, duration)
        self.parallax = parallax

    def draw(self, screen: Surface, prev_surf: Surface) -> None:
        t = self.ease_in_out(self.progress)
        w = self.size[0]

        # Déplacement principal
        offset = int(t * w)
        # Offset légèrement réduit pour prev_surf (effet parallaxe)
        prev_offset = int(t * w * (1.0 + self.parallax))

        # Dessiner prev_surf décalée vers la gauche
        screen.blit(prev_surf, (-prev_offset, 0))
        # Dessiner la nouvelle scène entrant par la droite
        # screen contient déjà la nouvelle frame : on la blit par-dessus
        # en la décalant, puis on la reblit à sa position finale par morceaux.
        # Plus simple : on travaille avec une copie.
        new_surf = screen.copy()            # nouvelle scène déjà rendue
        screen.blit(prev_surf, (-prev_offset, 0))
        screen.blit(new_surf, (w - offset, 0))


# ---------------------------------------------------------------------------
# SlideRight — glissement vers la droite (retour arrière)
# ---------------------------------------------------------------------------

@Transition.register("slide_right")
class SlideRight(Transition):
    """
    Inverse de SlideLeft : la nouvelle scène entre par la gauche.

    Recommandé pour : retours en arrière, flashbacks,
                      navigation vers un lieu précédent.
    """

    def __init__(self, size: Size, duration: float = 0.45, parallax: float = 0.15) -> None:
        super().__init__(size, duration)
        self.parallax = parallax

    def draw(self, screen: Surface, prev_surf: Surface) -> None:
        t = self.ease_in_out(self.progress)
        w = self.size[0]

        offset = int(t * w)
        prev_offset = int(t * w * (1.0 + self.parallax))

        new_surf = screen.copy()
        screen.blit(prev_surf, (prev_offset, 0))
        screen.blit(new_surf, (offset - w, 0))


# ---------------------------------------------------------------------------
# Tableau de recommandations (consulté par le script designer)
# ---------------------------------------------------------------------------

TRANSITION_GUIDE = {
    "fade_black":  "Changements de lieu majeurs, ellipses, transitions inter-actes",
    "fade_white":  "Révélations, flashbacks, éblouissements, dénouements émotionnels",
    "iris":        "Fin de scène intimiste, révélations dramatiques, genre noir",
    "slide_left":  "Avancée dans le récit, déplacements spatiaux, action",
    "slide_right": "Retours en arrière, flashbacks, navigation vers le passé",
}
