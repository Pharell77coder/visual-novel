# visual novel - 🕵️ NUIT SANS TÉMOIN

> *Un thriller néo-noir en pixel art — Visual Novel pygame*

---

## Présentation

**Nuit sans Témoin** est un visual novel en français développé avec Python et pygame. Le joueur incarne le détective Raven, lancé sur les traces d'un comptable assassiné qui dissimulait les secrets d'une organisation criminelle secrète : la **Synarchie**. L'enquête se déroule en trois chapitres et couvre des environnements variés — ruelle de Chinatown, aéroport, salle d'interrogatoire, les toits de la ville, Genève.

---

## Structure du projet

```
visual-novel/
├── assets/
│   ├── audio/          # jazz.mp3, click.wav, ...
│   ├── backgrounds/    # bureau.png, rue.png, salle_interrogatoire.png, ...
│   ├── characters/
│   │   ├── detective/  # detective0.png … detective9.png (+ left/ right/)
│   │   ├── policiere/  # policiere0.png … policiere3.png
│   │   ├── ferriere/   # ferriere0.png … ferriere3.png
│   │   ├── nathasha/   # ← dossier réel (typo repo) — géré automatiquement
│   │   ├── taro/       # taro0.png … taro3.png
│   │   └── architect/  # architect0.png … architect3.png
│   ├── font/           # joystix.ttf
│   └── ui/             # dialogue.png, inventaire.png, preuve.png
├── saves/              # slot_0.json, slot_1.json, slot_2.json
└── src/
    ├── main.py             # Moteur principal VNEngine
    ├── script.py           # Toute la narration (nœuds de dialogue)
    ├── ui.py               # DialogueBox, EvidencePanel, DeductionPanel, ...
    ├── assets_manager.py   # Chargement sprites, sons, polices
    ├── config.py           # Constantes (couleurs, chemins, dimensions)
    ├── deductions.py       # Moteur de combinaison de preuves
    ├── save_manager.py     # Sauvegarde JSON (3 slots)
    ├── models.py           # RainEffect, Particle
    ├── transitions.py      # FadeBlack, FadeWhite, Iris, SlideLeft, SlideRight
    ├── interrogation.py    # Mini-jeu d'interrogatoire
    └── test_transitions.py # Démo standalone des transitions
```

---

## Prérequis

| Logiciel | Version minimale |
|----------|-----------------|
| Python   | 3.10            |
| pygame   | 2.0             |

```bash
pip install pygame
```

---

## Lancement

```bash
cd src
python main.py
```

---

## Contrôles en jeu

### Navigation principale

| Touche / Action | Effet |
|-----------------|-------|
| `ESPACE` / `Entrée` | Avancer / Confirmer le choix |
| `←` `→` | Naviguer entre les choix de dialogue |
| `Clic gauche` | Avancer / Choisir |
| `Échap` | Quitter |

### Panneaux

| Touche | Panneau |
|--------|---------|
| `E` | Ouvrir/fermer **Preuves** |
| `D` | Ouvrir/fermer **Déductions** |
| `I` | Ouvrir/fermer **Inventaire** |
| `S` | Ouvrir le menu **Sauvegarde** |
| `L` | Ouvrir le menu **Chargement** |

### Backlog — Historique des dialogues `B`

> *Fonctionnalité classique des visual novels : relisez tout ce qui a déjà été dit.*

| Touche / Action | Effet |
|-----------------|-------|
| `B` | Ouvrir/fermer l'historique |
| `↑` / `↓` | Défiler dans l'historique |
| `Molette souris` (hors backlog) | Voir ci-dessous |
| `Échap` ou clic | Fermer l'historique |

Le backlog conserve les **80 dernières répliques** (nom du personnage + texte). Il est persistant pendant la session mais se remet à zéro à chaque nouvelle partie.

### Vitesse du typewriter `+` / `-` / Molette

> *Réglez le rythme d'apparition du texte selon vos préférences.*

| Action | Effet |
|--------|-------|
| `+` ou `=` ou Molette ↑ | Augmenter la vitesse |
| `-` ou Molette ↓ | Diminuer la vitesse |

Six niveaux disponibles :

| Niveau | Label | Caractères/frame |
|--------|-------|-----------------|
| 0 | ◂◂ très lent | 0.3 |
| 1 | ◂ lent | 0.7 |
| **2** | **● normal** *(défaut)* | **1.0** |
| 3 | rapide ▸ | 2.0 |
| 4 | très rapide ▸▸ | 4.0 |
| 5 | ⚡ instantané | ∞ |

Un badge de confirmation s'affiche brièvement au-dessus de la boîte de dialogue lors de chaque changement.

---

## Système de preuves et déductions

### Preuves

Certains nœuds de script ajoutent automatiquement une preuve à l'inventaire. Une animation de particules roses signale chaque nouvel indice (coin supérieur droit).

Ouvrez le panneau `[E]` pour consulter vos preuves.

### Combinaisons de preuves

Dans le panneau Preuves :

1. Appuyez sur `C` pour entrer en mode **Combiner**
2. Sélectionnez une première preuve (`Entrée`)
3. Sélectionnez une deuxième preuve (`Entrée`)
4. Appuyez sur `Espace` pour lancer la déduction

Si la combinaison est connue, une **déduction** s'affiche sous forme de popup avec titre, texte d'analyse et sources. Sinon : *"Ces deux indices ne mènent à rien de nouveau…"*

Les déductions débloquées sont consultables dans le panneau `[D]`.

**14 preuves** réparties sur 3 chapitres → **17 combinaisons** possibles.

---

## Sauvegarde

3 slots de sauvegarde (fichiers JSON dans `saves/`).

Chaque slot enregistre :
- Position dans le script (`script_idx`)
- Preuves collectées
- Déductions débloquées
- Fond courant
- Nom de la scène + horodatage

### Écran de sauvegarde

- `↑` / `↓` pour naviguer entre les slots
- `Entrée` pour confirmer
- Écraser un slot existant demande une **double confirmation** (message d'avertissement rose)
- `Échap` pour annuler

---

## Mini-jeu d'interrogatoire

Déclenché automatiquement par les nœuds de type `"type": "interrogation"` dans `script.py`.

### Suspects disponibles

| ID | Nom | Profil |
|----|-----|--------|
| `taro` | Taro Mitsuki | Vulnérable au Silence (×1.45), méfiant face au Bluff |
| `ferriere` | Capitaine Ferrière | Vulnérable au Bluff (×1.35), résistant au Silence (×0.65) |

### Actions

| Touche | Action | Effet | Cooldown | Coût timer |
|--------|--------|-------|----------|-----------|
| `A` | **PRESS** | Confrontation directe (+10–18%) | 3 s | −8 s |
| `Z` | **BLUFF** | Manipulation risquée (+15–22% ou −4–9%) | 5 s | −5 s |
| `E` | **SILENCE** | Attente psychologique (+3–7%) | 0.8 s | −2 s |

### Victoire / Défaite

- **Victoire** : pression ≥ 100 % avant la fin du timer → branche `on_success` du script
- **Défaite** : timer épuisé → branche `on_failure` du script

### Intégration dans script.py

```python
{
    "id":         "sc_42",
    "type":       "interrogation",
    "suspect":    "taro",         # "taro" | "ferriere"
    "time_limit": 90,             # secondes
    "on_success": "sc_43_confesse",
    "on_failure": "sc_44_echappe",
}
```

---

## Transitions visuelles

| Nom | Effet | Usage recommandé |
|-----|-------|-----------------|
| `fade_black` | Fondu au noir *(défaut)* | Changements de lieu, ellipses |
| `fade_white` | Fondu au blanc | Révélations, flashbacks |
| `iris` | Ouverture/fermeture circulaire | Genre noir, fin de scène intimiste |
| `slide_left` | Glissement vers la gauche | Avancée narrative, action |
| `slide_right` | Glissement vers la droite | Retours en arrière, flashbacks |

Spécifier dans un nœud de script :

```python
{"bg": "rue", "transition": "slide_left", ...}
{"bg": "bureau", "transition": "iris", "iris_center": [480, 270], ...}
```

Tester les transitions visuellement :

```bash
python test_transitions.py
```

---

## Personnages

| Clé | Nom | Expressions disponibles |
|-----|-----|------------------------|
| `detective` | Détective Raven | 10 (0=neutre … 9=fatigué) |
| `policiere` | Off. Leïla Sato | 4 (0=neutre, 1=sérieux, 2=sourire, 3=choqué) |
| `ferriere` | Capitaine Ferrière | 4 |
| `natasha` | Natasha | 4 |
| `taro` | Taro Mitsuki | 4 |
| `architect` | L'Architecte | 4 |

---

## Ajouter une scène

```python
# Nœud minimal
{"bg": "bureau", "char": "detective", "expr": 0, "side": "left",
 "name": "DÉTECTIVE RAVEN", "text": "Ma réplique."}

# Avec preuve
{"bg": "rue", "char": "detective", "expr": 5, "side": "left",
 "name": "DÉTECTIVE RAVEN", "text": "Intéressant...",
 "evidence": ("Clé USB", "Description courte")}

# Avec choix
{"bg": "bureau", "char": "detective", "expr": 0, "side": "left",
 "name": "", "text": "Que faire ?",
 "choices": ["Option A", "Option B"],
 "choice_branch": {"0": "id_branche_a", "1": "id_branche_b"}}

# Nœud cible (avec id)
{"id": "id_branche_a", "bg": "rue", ...}
```

---

## Bugs corrigés (version actuelle)

| Fichier | Bug | Correction |
|---------|-----|-----------|
| `save_manager.py` | `TypeError: save() got unexpected keyword argument 'deductions'` | Paramètre `deductions` ajouté à `SaveManager.save()` |
| `save_manager.py` | Sauvegardes anciennes sans clé `"deductions"` causaient une `KeyError` au chargement | Rétrocompatibilité via `.get("deductions", [])` |
| `main.py` | Mini-jeu interrogatoire (`InterrogationMinigame`) non importé ni connecté | Import + `_start_interrogation()` + boucle `update/draw` intégrés |
| `main.py` | Double `pygame.display.flip()` pendant l'interrogatoire | Retour anticipé dans `_draw()` quand `self.interro is not None` |
| `main.py` | Backlog (`[B]`) et vitesse (`+/-`, molette) non câblés dans `_handle_event()` | Branchements ajoutés |
| `ui.py` | `DialogueBox` : méthodes `toggle_backlog()`, `backlog_scroll()`, `_draw_backlog()` absentes | Implémentées complètement |
| `ui.py` | `EvidencePanel.draw()` appelait `self.update(0)` → timers d'animation gelés | Appel supprimé (update appelé correctement par le moteur) |
| `assets_manager.py` | Dossier `nathasha/` (typo) dans le dépôt mais code cherche `natasha/` → sprites chargés silencieusement vides | Fallback automatique : essaie les deux noms |

---

## Licence

Projet personnel / éducatif. Assets visuels et musicaux propriétaires — non redistribuables.