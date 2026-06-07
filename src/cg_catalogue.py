"""
cg_catalogue.py — Registre central des illustrations CG
=========================================================

Chaque CG est identifiée par un id unique (string).
La liste CG_CATALOGUE définit l'ordre d'affichage dans la galerie.

Structure d'une entrée :
    {
        "id":       str,          # identifiant unique, utilisé dans script.py
        "title":    str,          # titre affiché dans la galerie
        "chapter":  str,          # label du chapitre ("Chapitre I", …)
        "file":     str,          # chemin relatif depuis assets/cg/
        "hint":     str,          # indice affiché quand l'image est verrouillée
    }

Dans script.py, déclencher le déblocage d'une CG :
    {"cg": "cg_01_ruelle", ...}

Le moteur (VNEngine) lit la clé "cg" à chaque nœud et appelle
    cg_manager.unlock("cg_01_ruelle")
"""

from __future__ import annotations

CG_CATALOGUE: list[dict] = [

    # ── Chapitre I ──────────────────────────────────────────────────────────────
    {
        "id":      "cg_01_ruelle",
        "title":   "La Ruelle de Chinatown",
        "chapter": "Chapitre I",
        "file":    "cg_01_ruelle.png",
        "hint":    "Chapitre I — La scène de crime",
    },
    {
        "id":      "cg_02_cle_usb",
        "title":   "La Clé USB",
        "chapter": "Chapitre I",
        "file":    "cg_02_cle_usb.png",
        "hint":    "Chapitre I — L'indice découvert sur Vane",
    },
    {
        "id":      "cg_03_bureau_nuit",
        "title":   "Bureau, 3h du matin",
        "chapter": "Chapitre I",
        "file":    "cg_03_bureau_nuit.png",
        "hint":    "Chapitre I — Décrypter les secrets de Vane",
    },
    {
        "id":      "cg_04_toit",
        "title":   "Promesse sur les Toits",
        "chapter": "Chapitre I",
        "file":    "cg_04_toit.png",
        "hint":    "Chapitre I — La fin du premier acte",
    },

    # ── Chapitre II ─────────────────────────────────────────────────────────────
    {
        "id":      "cg_05_ferriere",
        "title":   "Ferrière dans l'Ombre",
        "chapter": "Chapitre II",
        "file":    "cg_05_ferriere.png",
        "hint":    "Chapitre II — Identification de la taupe",
    },
    {
        "id":      "cg_06_loft7",
        "title":   "Le Loft 7",
        "chapter": "Chapitre II",
        "file":    "cg_06_loft7.png",
        "hint":    "Chapitre II — Le centre de commandement",
    },
    {
        "id":      "cg_07_natasha",
        "title":   "Natasha — Contact",
        "chapter": "Chapitre II",
        "file":    "cg_07_natasha.png",
        "hint":    "Chapitre II — Une alliée inattendue",
    },
    {
        "id":      "cg_08_aeroport",
        "title":   "Fuite à l'Aéroport",
        "chapter": "Chapitre II",
        "file":    "cg_08_aeroport.png",
        "hint":    "Chapitre II — La course contre la montre",
    },

    # ── Chapitre III ────────────────────────────────────────────────────────────
    {
        "id":      "cg_09_geneve",
        "title":   "Genève sous la Pluie",
        "chapter": "Chapitre III",
        "file":    "cg_09_geneve.png",
        "hint":    "Chapitre III — La confrontation finale",
    },
    {
        "id":      "cg_10_architecte",
        "title":   "Face à l'Architecte",
        "chapter": "Chapitre III",
        "file":    "cg_10_architecte.png",
        "hint":    "Chapitre III — Le masque tombe",
    },
    {
        "id":      "cg_11_sacrifice",
        "title":   "Le Sacrifice",
        "chapter": "Chapitre III",
        "file":    "cg_11_sacrifice.png",
        "hint":    "Chapitre III — Branche : se sacrifier pour Sato",
    },
    {
        "id":      "cg_12_fuite",
        "title":   "Fuite dans la Nuit",
        "chapter": "Chapitre III",
        "file":    "cg_12_fuite.png",
        "hint":    "Chapitre III — Branche : fuir avec les preuves",
    },
    {
        "id":      "cg_13_epilogue",
        "title":   "Épilogue — Les Toits",
        "chapter": "Chapitre III",
        "file":    "cg_13_epilogue.png",
        "hint":    "Chapitre III — Atteindre la fin du jeu",
    },
    {"id": "cg_14_appartement",  "title": "La Photo",             "chapter": "Chapitre IV",  "file": "cg_14_appartement.png",  "hint": "Chapitre IV — Ce qu'on a trouvé sous la porte"},
    {"id": "cg_15_mira",         "title": "Le Parking",           "chapter": "Chapitre IV",  "file": "cg_15_mira.png",         "hint": "Chapitre IV — Premier contact avec Mira Voss"},
    {"id": "cg_16_archives",     "title": "Les Archives",         "chapter": "Chapitre IV",  "file": "cg_16_archives.png",     "hint": "Chapitre IV — La salle qui sera détruite"},
    {"id": "cg_17_trahison",     "title": "La Révélation",        "chapter": "Chapitre V",   "file": "cg_17_trahison.png",     "hint": "Chapitre V — Branche : douter de Mira"},
    {"id": "cg_18_berlin",       "title": "Berlin, Avant",        "chapter": "Chapitre V",   "file": "cg_18_berlin.png",       "hint": "Chapitre V — La nuit avant la tempête"},
    {"id": "cg_19_fantôme",      "title": "Démasqué",             "chapter": "Chapitre V",   "file": "cg_19_fantome.png",      "hint": "Chapitre V — Viktor Selg face à Raven"},
    {"id": "cg_20_parlement",    "title": "Le Parlement",         "chapter": "Chapitre VI",  "file": "cg_20_parlement.png",    "hint": "Chapitre VI — La nuit de l'exposition"},
    {"id": "cg_21_bunker",       "title": "Le Bunker",            "chapter": "Chapitre VII", "file": "cg_21_bunker.png",       "hint": "Chapitre VII — Le dernier refuge"},
    {"id": "cg_22_fin_lumière",  "title": "Fin — La Lumière",     "chapter": "Chapitre VII", "file": "cg_22_fin_lumiere.png",  "hint": "Chapitre VII — Branche : reprendre"},
    {"id": "cg_23_fin_ombre",    "title": "Fin — L'Ombre",        "chapter": "Chapitre VII", "file": "cg_23_fin_ombre.png",    "hint": "Chapitre VII — Branche : disparaître"}
]

# Index rapide id → entrée
CG_INDEX: dict[str, dict] = {cg["id"]: cg for cg in CG_CATALOGUE}
