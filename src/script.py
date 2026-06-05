# ── Scène / Script du jeu ───────────────────────────────────────────────────────
SCRIPT = [
    # ── ACTE 1 : La scène de crime ──────────────────────────────────────────────
    {"bg": "scene_de_crime", "music": False, "rain": False,
     "char": None, "expr": None, "side": "left",
     "name": "", "text": "2h37 du matin. La pluie n'a pas cessé depuis trois jours."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN", "text": "Encore une nuit blanche. Encore un mort que personne ne réclame."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO", "text": "Raven. Vous avez mis le temps. La victime : Marcus Vane, 42 ans, comptable."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN", "text": "Un comptable... dans une ruelle de Chinatown. Ça sent le règlement de comptes.",
     "evidence": ("Dossier Vane", "Victime : M.Vane, comptable")},

    {"bg": "scene_de_crime", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO", "text": "Pas d'arme sur place. Mais on a trouvé ça dans sa poche..."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN", "text": "Une clé USB cryptée. Intéressant.",
     "evidence": ("Clé USB", "Données cryptées inconnues")},

    # CHOIX 1
    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Que faire ensuite ?",
     "choices": ["Interroger les témoins", "Examiner la scène"],
     "choice_branch": {"0": "interrogation", "1": "scene"}},

    # Branche : examiner la scène
    {"id": "scene",
     "bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN", "text": "Je scrute chaque centimètre. Des traces de pneus... une plaque partiellement effacée.",
     "evidence": ("Trace de pneus", "Véhicule lourd, pneus larges")},

    # Branche : interroger
    {"id": "interrogation",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO", "text": "On a un témoin. Il refuse de parler, mais il a vu quelque chose cette nuit-là."},

    # ── ACTE 2 : La rue ─────────────────────────────────────────────────────────
    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN", "text": "Je retourne dans la rue. La pluie efface les traces, mais pas les mensonges."},

    {"bg": "rue", "rain": True,
     "char": None, "expr": None, "side": "left",
     "name": "", "text": "Un homme dans l'ombre. Son manteau dégouline. Il m'a vu arriver."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 2, "side": "left",
     "name": "DÉTECTIVE RAVEN", "text": "Ne fuis pas. J'ai juste quelques questions. Tu seras rentré avant l'aube."},

    # ── ACTE 3 : Le bureau ───────────────────────────────────────────────────────
    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN", "text": "3h du matin. Je décrypte la clé USB. Des noms. Des montants. Des millions planqués offshore."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN", "text": "Vane ne comptait pas des feuilles de paie. Il comptait l'argent sale de la Synarchie.",
     "evidence": ("Fichiers Synarchie", "Réseau criminel financier")},

    {"bg": "bureau", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO", "text": "Raven, faites attention. Ces gens-là... ils font disparaître plus que des preuves."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN", "text": "Je sais. C'est pour ça que j'adore ce métier."},

    # CHOIX 2
    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Comment procéder ?",
     "choices": ["Agir seul", "Faire confiance à Sato"],
     "choice_branch": {"0": "solo", "1": "team"}},

    # Branche solo
    {"id": "solo",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN", "text": "Cette ville. Elle ne dort jamais. Et moi non plus."},

    # Branche équipe
    {"id": "team",
     "bg": "toit", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO", "text": "On fait équipe, alors. Je couvre vos arrières, vous couvrez les miens."},

    # ── ACTE FINAL : Le toit ─────────────────────────────────────────────────────
    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN", "text": "La vérité est là, quelque part dans cette ville de néons et de mensonges."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Et moi, je la trouverai. C'est ma promesse à Marcus Vane. À tous les Marcus de ce monde."},

    {"bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "", "text": "─── FIN DU CHAPITRE I ───\n\nNUIT SANS TÉMOIN continuera..."},
]
