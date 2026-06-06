# ═══════════════════════════════════════════════════════════════════════════════
# NUIT SANS TÉMOIN — script.py complet (Chapitres I & II)
# ═══════════════════════════════════════════════════════════════════════════════
#
# CONVENTION DES IDs DE BRANCHE :
#   Chapitre I  → pas de préfixe  (ex: "scene", "interrogation", "solo", "team")
#   Chapitre II → préfixe "ch2_" (ex: "ch2_trust", "ch2_resist", ...)
#
# Cela évite toute collision dans le dict id_map du VNEngine.
#
# ARBRE DE DÉCISIONS :
#
#   ┌── CHAPITRE I ──────────────────────────────────────────────────────┐
#   │  CHOIX 1 : "Interroger" → [interrogation]                         │
#   │          / "Examiner"   → [scene]                                 │
#   │  CHOIX 2 : "Agir seul"  → [solo]                                  │
#   │          / "Faire confiance à Sato" → [team]                      │
#   └────────────────────────────────────────────────────────────────────┘
#                         ↓
#   ┌── CHAPITRE II ─────────────────────────────────────────────────────┐
#   │  CHOIX A : "Faire confiance" → [ch2_trust]                        │
#   │          / "Garder ses distances" → [ch2_resist]                  │
#   │  CHOIX B : "Infiltrer" → [ch2_infiltrate]                         │
#   │          / "Contacter la presse" → [ch2_press]                    │
#   │  CHOIX C : "Exposer Ferrière seul" → [ch2_betray]                 │
#   │          / "Protéger Sato" → [ch2_protect]                        │
#   └────────────────────────────────────────────────────────────────────┘
#
# PREUVES (9 au total sur les deux chapitres) :
#   Ch1 : Dossier Vane, Clé USB, Trace de pneus, Fichiers Synarchie
#   Ch2 : Registre Offshore, Photo du Fantôme, Enregistrement Taro,
#          Clé du Loft 7, Rapport interne
#
# EXPRESSIONS detective : 0=neutre 1=sourire 2=large 3=colère 4=triste
#                         5=regard 6=smirk  7=shocked 8=smug  9=tired
# EXPRESSIONS policiere : 0=neutre 1=sérieux 2=sourire 3=shocked
# ═══════════════════════════════════════════════════════════════════════════════

SCRIPT = [

    # ══════════════════════════════════════════════════════════════════════════
    # ████  CHAPITRE I — "La Nuit sans Témoin"  ████
    # ══════════════════════════════════════════════════════════════════════════

    # ── ACTE 1 : La scène de crime ─────────────────────────────────────────────
    {"bg": "scene_de_crime", "rain": False,
     "char": None, "side": "left",
     "name": "", "text": "2h37 du matin. La pluie n'a pas cessé depuis trois jours."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Encore une nuit blanche. Encore un mort que personne ne réclame."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. Vous avez mis le temps. La victime : Marcus Vane, 42 ans, comptable."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un comptable dans une ruelle de Chinatown. Ça sent le règlement de comptes.",
     "evidence": ("Dossier Vane", "Victime : M.Vane, comptable")},

    {"bg": "scene_de_crime", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Pas d'arme sur place. Mais on a trouvé ça dans sa poche..."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Une clé USB cryptée. Intéressant.",
     "evidence": ("Clé USB", "Données cryptées inconnues")},

    # CHOIX 1 ──────────────────────────────────────────────────────────────────
    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Que faire ensuite ?",
     "choices": ["Interroger les témoins", "Examiner la scène"],
     "choice_branch": {"0": "interrogation", "1": "scene"}},

    # Branche : examiner la scène ──────────────────────────────────────────────
    {"id": "scene",
     "bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je scrute chaque centimètre. Des traces de pneus... une plaque partiellement effacée.",
     "evidence": ("Trace de pneus", "Véhicule lourd, pneus larges")},

    # Branche : interroger ─────────────────────────────────────────────────────
    {"id": "interrogation",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "On a un témoin. Il refuse de parler, mais il a vu quelque chose cette nuit-là."},

    # ── ACTE 2 : La rue ────────────────────────────────────────────────────────
    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je retourne dans la rue. La pluie efface les traces, mais pas les mensonges."},

    {"bg": "rue", "rain": True,
     "char": None, "side": "left",
     "name": "", "text": "Un homme dans l'ombre. Son manteau dégouline. Il m'a vu arriver."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 2, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ne fuis pas. J'ai juste quelques questions. Tu seras rentré avant l'aube."},

    # ── ACTE 3 : Le bureau ─────────────────────────────────────────────────────
    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "3h du matin. Je décrypte la clé USB. Des noms. Des montants. Des millions planqués offshore."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vane ne comptait pas des feuilles de paie. Il comptait l'argent sale de la Synarchie.",
     "evidence": ("Fichiers Synarchie", "Réseau criminel financier")},

    {"bg": "bureau", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven, faites attention. Ces gens-là... ils font disparaître plus que des preuves."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je sais. C'est pour ça que j'adore ce métier."},

    # CHOIX 2 ──────────────────────────────────────────────────────────────────
    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Comment procéder ?",
     "choices": ["Agir seul", "Faire confiance à Sato"],
     "choice_branch": {"0": "solo", "1": "team"}},

    # Branche solo ─────────────────────────────────────────────────────────────
    {"id": "solo",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Cette ville. Elle ne dort jamais. Et moi non plus."},

    # Branche équipe ───────────────────────────────────────────────────────────
    {"id": "team",
     "bg": "toit", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "On fait équipe, alors. Je couvre vos arrières, vous couvrez les miens."},

    # ── ACTE FINAL : Le toit ───────────────────────────────────────────────────
    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La vérité est là, quelque part dans cette ville de néons et de mensonges."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Et moi, je la trouverai. C'est ma promesse à Marcus Vane. À tous les Marcus de ce monde."},

    # Interlude chapitres ──────────────────────────────────────────────────────
    {"bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "", "text": "─── FIN DU CHAPITRE I ───"},

    # ══════════════════════════════════════════════════════════════════════════
    # ████  CHAPITRE II — "Le Prix de la Vérité"  ████
    # ══════════════════════════════════════════════════════════════════════════

    # ── ACTE 1 : Transition & découverte du Registre ───────────────────────────
    {"bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "", "text": "CHAPITRE II — Le Prix de la Vérité"},

    {"bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Trois jours ont passé. La clé USB de Marcus Vane a ouvert une boîte de Pandore."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "72 heures sans dormir. Des noms, des virements, des sociétés écrans... La Synarchie est partout."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Trois juges. Un sénateur. Deux directeurs de banque. Et au sommet... un nom effacé. Toujours ce même nom effacé.",
     "evidence": ("Registre Offshore", "Politiques & juges corrompus")},

    {"bg": "bureau", "rain": True,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. Mon chef vient de me convoquer. Il veut qu'on rende la clé USB. Motif : 'preuves saisies illégalement'."},

    {"bg": "bureau", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Illégalement. Bien sûr. Quelqu'un là-haut a peur, Sato. Et la peur rend les gens dangereux."},

    {"bg": "bureau", "rain": True,
     "char": "policiere", "expr": 0, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Il y a autre chose. Un homme m'a contactée ce matin. Il dit avoir des informations sur la mort de Vane. Il veut vous rencontrer."},

    {"bg": "bureau", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un informateur qui sort du néant au moment où l'enquête devient dangereuse. Soit c'est une chance, soit c'est un piège."},

    # ── ACTE 2 : La rencontre avec Taro ────────────────────────────────────────
    {"bg": "rue", "rain": True,
     "char": None, "side": "left",
     "name": "", "text": "Le lieu de rendez-vous : une ruelle derrière le marché couvert de Chinatown. 23h00."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je prends position vingt minutes en avance. Les pièges se voient mieux quand on arrive le premier."},

    {"bg": "rue", "rain": True,
     "char": None, "side": "left",
     "name": "INCONNU",
     "text": "Détective Raven... J'espérais que vous viendriez seul. Je m'appelle Taro. J'étais le comptable de Vane."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le comptable du comptable. Pratique. Qu'est-ce qui vous retient encore en vie, Taro ?"},

    {"bg": "rue", "rain": True,
     "char": None, "side": "left",
     "name": "TARO",
     "text": "Eux ne savent pas que j'existe. Marcus gardait mes noms hors des registres. Mais j'ai tout vu. Tout entendu."},

    {"bg": "rue", "rain": True,
     "char": None, "side": "left",
     "name": "TARO",
     "text": "La nuit de sa mort, Marcus avait rendez-vous avec un homme qui portait un badge de la police.",
     "evidence": ("Photo du Fantôme", "Silhouette avec badge policier")},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un flic. Il y a un flic dans la Synarchie."},

    {"bg": "rue", "rain": True,
     "char": None, "side": "left",
     "name": "TARO",
     "text": "Pas juste un flic. Quelqu'un de haut placé. J'ai un enregistrement. La voix... vous la reconnaîtrez."},

    # CHOIX A ──────────────────────────────────────────────────────────────────
    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Taro tend un téléphone. Sur l'écran : un fichier audio. Comment réagir ?",
     "choices": ["Lui faire confiance", "Garder ses distances"],
     "choice_branch": {"0": "ch2_trust", "1": "ch2_resist"}},

    # ── Branche : Faire confiance ──────────────────────────────────────────────
    {"id": "ch2_trust",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je prends le téléphone. La voix sur l'enregistrement est froide, calculée. Et familière.",
     "evidence": ("Enregistrement Taro", "Voix inconnue — ordre de tuer Vane")},

    {"id": "ch2_trust_2",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je connais cette voix. Je l'ai entendue ce matin même dans les couloirs du commissariat central."},

    # ── Branche : Garder ses distances ────────────────────────────────────────
    {"id": "ch2_resist",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je ne touche pas à l'appareil. Les téléphones piégés existent. On me copie les empreintes, on me géolocalise. Non merci."},

    {"id": "ch2_resist_2",
     "bg": "rue", "rain": True,
     "char": None, "side": "left",
     "name": "TARO",
     "text": "Je comprends la prudence. Alors je vais juste vous dire le nom. Commandant Ferrière. Brigade criminelle."},

    {"id": "ch2_resist_3",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ferrière. Le supérieur direct de Sato. Mon sang se glace.",
     "evidence": ("Enregistrement Taro", "Ferrière impliqué — Synarchie")},

    # ── ACTE 3 : La révélation — Ferrière ─────────────────────────────────────
    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Commandant Ferrière. C'est lui qui a ordonné de rendre la clé USB. C'est lui qui fait pression. C'est lui."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "C'est impossible. Ferrière est dans la police depuis vingt ans. C'est lui qui m'a recrutée."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vingt ans. Le temps de monter très haut. Le temps de se vendre très cher."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Si Ferrière est dans la Synarchie... alors toute mon enquête sur les dossiers classifiés... il l'a vue."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Sato. Écoutez-moi. Il faut agir vite, mais sans se précipiter. Si on rate notre coup, on est morts."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Taro avait mentionné un endroit. Le Loft 7, dans les anciens docks. Le QG opérationnel de la Synarchie."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Une clé dans les affaires de Vane. Que la police n'a pas répertoriée. Loft 7.",
     "evidence": ("Clé du Loft 7", "Accès QG de la Synarchie")},

    # CHOIX B ──────────────────────────────────────────────────────────────────
    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "On a 48 heures avant que Ferrière réalise qu'on sait. Comment frapper ?",
     "choices": ["Infiltrer le Loft 7", "Contacter la presse"],
     "choice_branch": {"0": "ch2_infiltrate", "1": "ch2_press"}},

    # ── Branche : Infiltrer ────────────────────────────────────────────────────
    {"id": "ch2_infiltrate",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Les docks au petit matin. Brume sur l'eau. Le Loft 7 est au troisième niveau d'un entrepôt désaffecté."},

    {"id": "ch2_infiltrate_2",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La clé tourne. L'intérieur : des serveurs, des câbles, des dizaines d'écrans. Des dossiers classés par ville."},

    {"id": "ch2_infiltrate_3",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Paris. Bruxelles. Tokyo. Ils ne sont pas juste criminels. C'est un réseau de gouvernance parallèle.",
     "evidence": ("Rapport interne", "Réseau actif dans 12 pays")},

    {"id": "ch2_infiltrate_4",
     "bg": "rue", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Soudain. Des pas dans l'escalier. Deux hommes. Et derrière eux, une voix familière."},

    {"id": "ch2_infiltrate_5",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ferrière. Il est ici. Il savait que je viendrais."},

    # ── Branche : Presse ──────────────────────────────────────────────────────
    {"id": "ch2_press",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Natasha Mori. Journaliste d'investigation au Tribune. On s'est rencontrés sur l'affaire Colombe, il y a trois ans."},

    {"id": "ch2_press_2",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je lui envoie une copie cryptée des fichiers Synarchie. Et j'attends. Vingt minutes plus tard, elle rappelle."},

    {"id": "ch2_press_3",
     "bg": "bureau", "rain": False,
     "char": None, "side": "left",
     "name": "NATASHA MORI (téléphone)",
     "text": "Raven... C'est énorme. On publie demain matin. Mais mon rédac' chef vient d'être convoqué par la préfecture. Ils savent déjà."},

    {"id": "ch2_press_4",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ils ont des oreilles partout. Il faut les forcer à agir avant qu'ils musèlent le Tribune.",
     "evidence": ("Rapport interne", "Fuite détectée — fenêtre courte")},

    # ── ACTE 4 : La confrontation ──────────────────────────────────────────────
    {"bg": "salle_interrogatoire", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Quelle que soit la voie choisie, tout converge vers le même point. Ferrière sait que Raven est sur lui."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Ferrière m'a convoquée. Il prétend avoir des preuves que vous avez fabriqué des éléments. Il veut vous faire tomber."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 8, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Bien sûr. Parce que si je tombe, les preuves tombent avec moi. C'est son dernier recours."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Il m'a demandé de témoigner contre vous. De dire que vous m'avez forcée à accéder à des dossiers classifiés."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Et vous, Sato ? Qu'est-ce que vous avez répondu ?"},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "J'ai dit que j'avais besoin de réfléchir. Mais ce que je n'ai pas dit... c'est que j'ai enregistré toute la conversation."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Sato. Vous venez de sauver l'enquête. Et peut-être nos deux peaux."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "On fait équipe, non ? Alors qu'est-ce qu'on fait de l'enregistrement ?"},

    # CHOIX C ──────────────────────────────────────────────────────────────────
    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "L'enregistrement suffit à coincer Ferrière. Mais l'utiliser expose Sato directement. Comment procéder ?",
     "choices": ["Exposer Ferrière seul", "Protéger Sato coûte que coûte"],
     "choice_branch": {"0": "ch2_betray", "1": "ch2_protect"}},

    # ── Branche : Exposer Ferrière ─────────────────────────────────────────────
    {"id": "ch2_betray",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je transmets l'enregistrement à l'Inspection Générale. Directement. Sans passer par Ferrière."},

    {"id": "ch2_betray_2",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Sato sera entendue. Elle risque une suspension. Mais Ferrière sera en cellule avant la nuit. C'est le calcul."},

    {"id": "ch2_betray_3",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Vous ne m'avez pas consultée. Vous avez décidé seul. C'est... c'est ce que vous faites toujours, Raven ?"},

    {"id": "ch2_betray_4",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "...Oui. Et c'est pour ça que je travaille seul depuis dix ans."},

    # ── Branche : Protéger Sato ────────────────────────────────────────────────
    {"id": "ch2_protect",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On garde l'enregistrement de Sato en réserve. Coup de pression uniquement. On frappe Ferrière autrement."},

    {"id": "ch2_protect_2",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "J'ai une autre carte : Taro. Il est prêt à témoigner sous protection judiciaire. En échange : une nouvelle identité."},

    {"id": "ch2_protect_3",
     "bg": "bureau", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "C'est risqué. Mais si ça marche, on tient quelque chose de propre. De solide."},

    {"id": "ch2_protect_4",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Exactement. On fait ça dans les règles, Sato. Pour une fois, on fait ça bien."},

    # ── ÉPILOGUE DU CHAPITRE II ────────────────────────────────────────────────
    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le soleil se lève sur la ville. Ferrière sera arrêté d'ici ce soir. Mais le nom effacé au sommet du registre..."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il est toujours là. En creux. Une absence qui pèse comme une présence. Quelqu'un de plus grand. De plus patient."},

    {"bg": "toit", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Et Taro ? Il a disparu ce matin. Nouvelle identité activée. Mais il a laissé quelque chose pour vous."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Une enveloppe. Une adresse à Genève. Et un seul mot écrit à l'intérieur : 'ARCHITECT'."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "L'Architecte. Le nom effacé a un titre. Et une adresse. La prochaine fois, on ne le ratera pas."},

    {"bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "─── FIN DU CHAPITRE II ───\n\nCHAPITRE III : 'L'Architecte' — À venir"},
]