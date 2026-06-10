import pygame
import random
import math

from config import SCREEN_W, SCREEN_H

# ── Effet de pluie ──────────────────────────────────────────────────────────────
class RainEffect:
    def __init__(self, count=120):
        self.drops = [(random.randint(0, SCREEN_W),
                       random.randint(0, SCREEN_H),
                       random.uniform(6, 14),
                       random.uniform(0.4, 0.8)) for _ in range(count)]

    def update(self):
        new = []
        for x, y, sp, alpha in self.drops:
            y += sp
            if y > SCREEN_H:
                y = random.randint(-20, 0)
                x = random.randint(0, SCREEN_W)
            new.append((x, y, sp, alpha))
        self.drops = new

    def draw(self, screen):
        for x, y, sp, alpha in self.drops:
            length = int(sp * 2.5)
            col = (100, 140, 200, int(alpha * 180))
            s = pygame.Surface((2, length), pygame.SRCALPHA)
            s.fill(col)
            screen.blit(s, (int(x), int(y)))

# ── Particle Spark ──────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, col):
        self.x = x + random.uniform(-3, 3)
        self.y = y + random.uniform(-3, 3)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-1.5, -0.3)
        self.life = random.uniform(0.5, 1.5)
        self.max_life = self.life
        self.col = col
        self.r = random.randint(2, 4)

    def update(self, dt):
        self.life -= dt
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.04

    @property
    def alive(self):
        return self.life > 0

    def draw(self, screen):
        # On calcule l'alpha et on utilise max(0, ...) pour s'assurer qu'il ne descende JAMAIS sous 0
        a = max(0, int(255 * (self.life / self.max_life)))
        
        s = pygame.Surface((self.r*2, self.r*2), pygame.SRCALPHA)
        
        # On extrait les 3 composants RGB (au cas où)
        clean_rgb = tuple(int(c) for c in self.col[:3])
        
        pygame.draw.circle(s, (*clean_rgb, a), (self.r, self.r), self.r)
        screen.blit(s, (int(self.x - self.r), int(self.y - self.r)))