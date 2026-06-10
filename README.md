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

---

# 🏆 GUIDE DE COMPLÉTION 100%

Ce guide officiel vous permettra de débloquer **l'intégralité du contenu** : toutes les preuves, les 17 combinaisons de déductions, les 23 CG (illustrations), et les 2 fins alternatives du jeu[cite: 1]. 

> ⚠️ **Note sur la rejouabilité** : Certains choix scénaristiques mènent à des branches mutuellement exclusives[cite: 1]. **Au moins deux parties complètes (runs) sont indispensables** pour obtenir le 100%[cite: 1].

---

## 📅 CHAPITRE I — La Nuit sans Témoin

### Preuves du Chapitre I (4)
* **Dossier Vane** : Automatique — scène de crime[cite: 1].
* **Clé USB** : Automatique — fouille de Vane $\rightarrow$ **Débloque la CG 02**[cite: 1].
* **Trace de pneus** : Choix 1 $\rightarrow$ "Examiner la scène" (branche scene)[cite: 1]. *Exclusif Run 1*[cite: 1].
* **Témoignage rue** : Choix 1 $\rightarrow$ "Interroger les témoins" (branche interrogation)[cite: 1]. *Exclusif Run 2*[cite: 1].
* **Fichiers Synarchie** : Automatique — décryptage bureau nuit $\rightarrow$ **Débloque la CG 03**[cite: 1].
* **Enregistrement Taro** : Mini-jeu d'interrogatoire Taro (succès)[cite: 1].

> **Note** : Trace de pneus et Témoignage rue sont mutuellement exclusifs selon le Choix 1[cite: 1]. Prévoir deux runs[cite: 1].

### Déductions à combiner `[D]` (Chapitre I)
* `Dossier Vane` + `Clé USB` $\rightarrow$ **Double comptabilité**[cite: 1]
* `Clé USB` + `Fichiers Synarchie` $\rightarrow$ **La clé de tout**[cite: 1]
* `Trace de pneus` + `Dossier Vane` $\rightarrow$ **La voiture de l'exécuteur**[cite: 1]
* `Trace de pneus` + `Fichiers Synarchie` $\rightarrow$ **Logistique intégrée**[cite: 1]

### Illustrations (CG) du Chapitre I
* **CG 01** : Scène de crime, automatique[cite: 1]
* **CG 02** : La clé USB, automatique[cite: 1]
* **CG 03** : Bureau 3h du matin, automatique[cite: 1]
* **CG 04** : Sur les toits, fin du chapitre, automatique[cite: 1]

> **Choix 2 (solo vs team)** : Impact sur les branches mais pas sur les CG de ce chapitre[cite: 1]. Choisir les deux en deux runs pour compléter la carte narrative[cite: 1].

---

## 📅 CHAPITRE II — Le Prix de la Vérité

### Preuves du Chapitre II (5)
* **Registre Offshore** : Automatique — rencontre Natasha[cite: 1].
* **Photo du Fantôme** : Automatique (variante selon branche trust/resist)[cite: 1].
* **Enregistrement Taro** : Reporté depuis Ch1 si mini-jeu réussi — ou ré-obtenu ici si raté[cite: 1].
* **Clé du Loft 7** : Branche "S'infiltrer" (ch2_infiltrate)[cite: 1].
* **Rapport interne** : Branche "S'infiltrer" ou "Faire pression" (ch2_press)[cite: 1].

### Choix du Chapitre II

| Choix | Branches disponibles | Impact CG |
| :---: | :--- | :--- |
| **Choix A** | Trust Natasha / Résister seul | Aucun sur les CG[cite: 1] |
| **Choix B** | S'infiltrer / Faire pression | Rapport interne + Clé Loft 7[cite: 1] |
| **Choix C** | Trahir / Protéger | Aucun CG exclusif[cite: 1] |

### Illustrations (CG) du Chapitre II
* **CG 05** : Ferrière dans l'ombre, automatique en début de chapitre[cite: 1]
* **CG 06** : Le Loft 7 ⚠️ *(Branche ch2_infiltrate uniquement)*[cite: 1]
* **CG 07** : Natasha Contact, automatique[cite: 1]
* **CG 08** : Fuite à l'aéroport, automatique vers la fin[cite: 1]

### Déductions à combiner `[D]` (Chapitre II)
* `Registre Offshore` + `Fichiers Synarchie` $\rightarrow$ **Le circuit de blanchiment**[cite: 1]
* `Photo du Fantôme` + `Enregistrement Taro` $\rightarrow$ **Identification Ferrière**[cite: 1]
* `Photo du Fantôme` + `Clé du Loft 7` $\rightarrow$ **Le QG du fantôme**[cite: 1]
* `Enregistrement Taro` + `Registre Offshore` $\rightarrow$ **La commission de Ferrière**[cite: 1]
* `Clé du Loft 7` + `Rapport interne` $\rightarrow$ **Nœud opérationnel**[cite: 1]

---

## 📅 CHAPITRE III — L'Architecte

### Preuves du Chapitre III (5)
* **Accord Secret** : Branche ch3_confront (confronter Voss)[cite: 1].
* **Enregistrement final** : Branche ch3_expose (transmettre à Interpol)[cite: 1].
* **Schéma du Réseau** : Automatique — rencontre Voss[cite: 1].
* **Identité de l'Architecte** : Automatique[cite: 1].
* **Passeport Fantôme** : Automatique — arrestation Selg[cite: 1].

### Choix du Chapitre III

| Choix | Branches disponibles | CG exclusifs |
| :---: | :--- | :--- |
| **Choix D** | Confronter / Observer dans l'ombre | —[cite: 1] |
| **Choix E** | Exposer à Interpol / Négocier | —[cite: 1] |
| **Choix F** | Se sacrifier / Fuir | CG 11 (sacrifice) ou CG 12 (fuite)[cite: 1] |

### Illustrations (CG) du Chapitre III
* **CG 09** : Genève sous la pluie, automatique[cite: 1]
* **CG 10** : Face à l'Architecte, automatique[cite: 1]
* **CG 11** : ⚠️ **Exclusif** $\rightarrow$ Choix F : "Se sacrifier pour Sato"[cite: 1]
* **CG 12** : ⚠️ **Exclusif** $\rightarrow$ Choix F : "Fuir avec les preuves"[cite: 1]
* **CG 13** : Épilogue sur les toits, automatique (fin du chapitre)[cite: 1]

### Déductions à combiner `[D]` (Chapitre III)
* `Passeport Fantôme` + `Schéma du Réseau` $\rightarrow$ **L'Architecte multinational**[cite: 1]
* `Schéma du Réseau` + `Registre Offshore` $\rightarrow$ **L'épine dorsale financière**[cite: 1]
* `Accord Secret` + `Enregistrement final` $\rightarrow$ **L'aveu contractuel**[cite: 1]
* `Identité de l'Architecte` + `Passeport Fantôme` $\rightarrow$ **Le masque final**[cite: 1]
* `Identité de l'Architecte` + `Schéma du Réseau` $\rightarrow$ **L'organigramme complet**[cite: 1]
* `Enregistrement final` + `Rapport interne` $\rightarrow$ **Opérations confirmées**[cite: 1]
* `Clé USB` + `Accord Secret` $\rightarrow$ **Le fil directeur** *(Transversale)*[cite: 1]
* `Dossier Vane` + `Identité de l'Architecte` $\rightarrow$ **De la ruelle au sommet** *(Transversale)*[cite: 1]

---

## 📅 CHAPITRE IV — L'Héritage

* **CG 14** : La Photo, automatique en ouverture[cite: 1].

### Preuves du Chapitre IV (5)
* **Photo de surveillance** : Automatique[cite: 1].
* **Clé USB #2** : Automatique[cite: 1].
* **Badge magnétique** : Automatique[cite: 1].
* **Liste de contacts** : Automatique[cite: 1].
* **Dossier Mira** : Automatique — rencontre Mira $\rightarrow$ **Débloque la CG 15**[cite: 1].

### Choix du Chapitre IV
* **Choix G** : Contacter Sato / Agir seul[cite: 1]
* **Choix H** : Protéger Mira / Enregistrer secrètement[cite: 1]
* **Choix I** : Contacter la presse / S'infiltrer au Parlement[cite: 1]

### Illustrations (CG) du Chapitre IV
* **CG 15** : Le Parking, automatique (rencontre Mira)[cite: 1]
* **CG 16** : Les Archives, branche ch4_infiltrate (Choix I $\rightarrow$ "S'infiltrer")[cite: 1]

### Déductions à combiner `[D]` (Chapitre IV)
* `Photo de surveillance` + `Badge magnétique` $\rightarrow$ **Surveillance institutionnelle**[cite: 1]
* `Clé USB #2` + `Fichiers Synarchie` $\rightarrow$ **Le successeur prévu**[cite: 1]
* `Liste de contacts` + `Identité de l'Architecte` $\rightarrow$ **Réseau survivant**[cite: 1]
* `Dossier Mira` + `Photo de surveillance` $\rightarrow$ **Mira — actif ou double jeu ?**[cite: 1]

---

## 📅 CHAPITRE V — Le Fantôme

### Preuves du Chapitre V (4)
* **Identité du Fantôme** : Automatique[cite: 1].
* **Accord de Berlin** : Automatique[cite: 1].
* **Serveur miroir** : Branche ch5_follow_ghost (suivre discrètement)[cite: 1].
* **Témoin protégé** : Branche ch5_confront_ghost ou ch5_follow_ghost[cite: 1].

### Choix du Chapitre V

| Choix | Branches disponibles | CG exclusifs |
| :---: | :--- | :--- |
| **Choix J** | Faire entièrement confiance à Mira / Jouer double jeu | CG 17 si double jeu[cite: 1] |
| **Choix K** | Affronter le Fantôme / Le suivre | CG 19 si affrontement direct[cite: 1] |
| **Choix L** | Brûler le serveur / Garder intact | —[cite: 1] |

### Illustrations (CG) du Chapitre V
* **CG 17** : ⚠️ **Exclusif** $\rightarrow$ Choix J : "Jouer double jeu" (ch5_doubt_mira)[cite: 1]
* **CG 18** : Berlin avant la tempête, automatique[cite: 1]
* **CG 19** : ⚠️ **Exclusif** $\rightarrow$ Choix K : "L'affronter directement" (ch5_confront_ghost)[cite: 1]

### Déductions à combiner `[D]` (Chapitre V)
* `Identité du Fantôme` + `Accord de Berlin` $\rightarrow$ **L'architecte adjoint**[cite: 1]
* `Serveur miroir` + `Clé USB #2` $\rightarrow$ **Les données ne meurent pas**[cite: 1]
* `Témoin protégé` + `Enregistrement Taro` $\rightarrow$ **Chaîne de commandement**[cite: 1]

---

## 📅 CHAPITRE VI — Parlement

### Preuves du Chapitre VI (4)
* **Enregistrement parlement** : Automatique[cite: 1].
* **Compte numéroté** : Automatique[cite: 1].
* **Identité du Sénateur** : Branche ch6_senate (attaquer par le Sénat)[cite: 1].
* **Dossier fantôme vol 219** : Automatique[cite: 1].

### Choix du Chapitre VI
* **Choix M** : Par le Sénat / Par l'underground[cite: 1]
* **Choix N** : En équipe / Seul[cite: 1]
* **Choix O** : Exposer en live / Laisser fuir vers le bunker[cite: 1]

### Illustrations (CG) du Chapitre VI
* **CG 20** : Le Parlement, automatique[cite: 1]

### Déductions à combiner `[D]` (Chapitre VI)
* `Enregistrement parlement` + `Accord Secret` $\rightarrow$ **Corruption au sommet de l'UE**[cite: 1]
* `Compte numéroté` + `Registre Offshore` $\rightarrow$ **Même banque, vingt ans**[cite: 1]
* `Identité du Sénateur` + `Liste de contacts` $\rightarrow$ **Le législateur est la Synarchie**[cite: 1]

---

## 📅 CHAPITRE VII — La Décision

### Preuves du Chapitre VII (4)
* **Testament de Vane** : Automatique — ouverture bunker[cite: 1].
* **Preuve ultime** : Automatique[cite: 1].
* **Coordonnées bunker** : Automatique[cite: 1].
* **Décision finale** : Selon branche finale[cite: 1].

### Choix du Chapitre VII
* **Choix P** : Intégrer Sato / La tenir à l'écart[cite: 1]
* **Choix Q** : Accord partiel avec l'Architecte / Refus total[cite: 1]
* **Choix R** : "Reprendre" / "Disparaître" $\rightarrow$ *Fins exclusives*[cite: 1]

### Illustrations (CG) du Chapitre VII
* **CG 21** : Le Bunker, automatique[cite: 1]
* **CG 22** : ⚠️ **Exclusif** $\rightarrow$ Choix R : "Reprendre — la lumière a besoin de quelqu'un" $\rightarrow$ **Fin Lumière**[cite: 1]
* **CG 23** : ⚠️ **Exclusif** $\rightarrow$ Choix R : "Disparaître — et vivre enfin" $\rightarrow$ **Fin Ombre**[cite: 1]

### Déductions à combiner `[D]` (Chapitre VII)
* `Testament de Vane` + `Dossier Vane` $\rightarrow$ **Vane savait depuis le début**[cite: 1]
* `Preuve ultime` + `Schéma du Réseau` $\rightarrow$ **L'organigramme complet (Ch1–Ch7)**[cite: 1]
* `Coordonnées bunker` + `Passeport Fantôme` $\rightarrow$ **L'Architecte n'a jamais fui**[cite: 1]

---

## 🔁 Récap — Ce qui nécessite au moins 2 parties

Tout le reste (preuves, déductions, CG 01 à 05, 07 à 10, 13 à 15, 18, 20, 21) s'obtient en avançant naturellement, quelle que soit la branche[cite: 1].

| Élément | Run 1 | Run 2 |
| :--- | :--- | :--- |
| **CG 11 vs CG 12** | Se sacrifier[cite: 1] | Fuir[cite: 1] |
| **CG 22 vs CG 23** | Fin Lumière[cite: 1] | Fin Ombre[cite: 1] |
| **CG 17** | Double-jeu Mira[cite: 1] | —[cite: 1] |
| **CG 19** | Confronter le Fantôme[cite: 1] | —[cite: 1] |
| **CG 06** | S'infiltrer (Ch2)[cite: 1] | —[cite: 1] |
| **CG 16** | S'infiltrer Parlement (Ch4)[cite: 1] | —[cite: 1] |
| **Exclusivité Ch1** | Trace de pneus[cite: 1] | Témoignage rue[cite: 1] |
---