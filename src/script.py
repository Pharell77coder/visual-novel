# ═══════════════════════════════════════════════════════════════════════════════
# NUIT SANS TÉMOIN — script.py complet (Chapitres I, II & III)
# ═══════════════════════════════════════════════════════════════════════════════
#
# PERSONNAGES :
#   detective  — 10 expressions (0=neutre 1=sourire 2=large 3=colère 4=triste
#                                5=regard  6=smirk   7=shocked 8=smug  9=tired)
#   policiere  — 4 expressions  (0=neutre 1=serieux 2=sourire 3=shocked)
#   ferriere   — 4 expressions  (0=neutre 1=serieux 2=sourire 3=shocked)
#   natasha    — 4 expressions  (0=neutre 1=serieux 2=sourire 3=shocked)
#   taro       — 4 expressions  (0=neutre 1=serieux 2=sourire 3=shocked)
#   architect  — 4 expressions  (0=neutre 1=serieux 2=sourire 3=shocked)
#
# BACKGROUNDS :
#   Ch1 : bureau, rue, salle_interrogatoire, scene_de_crime, toit
#   Ch2 : (mêmes) + aeroport_jetpack, geneve
#   Ch3 : geneve, aeroport_jetpack, bureau, salle_interrogatoire, toit
#
# ARBRE DE DÉCISIONS :
#   Ch1 : Choix 1 → interrogation / scene
#         Choix 2 → solo / team
#   Ch2 : Choix A → ch2_trust / ch2_resist
#         Choix B → ch2_infiltrate / ch2_press
#         Choix C → ch2_betray / ch2_protect
#   Ch3 : Choix D → ch3_confront / ch3_shadow
#         Choix E → ch3_expose / ch3_negotiate
#         Choix F → ch3_sacrifice / ch3_escape
#
# PREUVES (14 au total) :
#   Ch1 : Dossier Vane, Clé USB, Trace de pneus, Fichiers Synarchie
#   Ch2 : Registre Offshore, Photo du Fantôme, Enregistrement Taro,
#          Clé du Loft 7, Rapport interne
#   Ch3 : Passeport Fantôme, Schéma du Réseau, Accord Secret,
#          Enregistrement final, Identité de l'Architecte
#
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

    # ── ACTE FINAL Ch1 : Le toit ───────────────────────────────────────────────
    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La vérité est là, quelque part dans cette ville de néons et de mensonges."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Et moi, je la trouverai. C'est ma promesse à Marcus Vane. À tous les Marcus de ce monde."},

    {"bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "", "text": "─── FIN DU CHAPITRE I ───"},

    # ══════════════════════════════════════════════════════════════════════════
    # ████  CHAPITRE II — "Le Prix de la Vérité"  ████
    # ══════════════════════════════════════════════════════════════════════════

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
     "char": "ferriere", "expr": 1, "side": "right",
     "name": "CDT. FERRIÈRE",
     "text": "Officier Sato. Cette enquête est terminée. Remettez-moi tout ce que vous avez sur l'affaire Vane. Ce soir."},

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

    # ── ACTE 2 Ch2 : La rencontre avec Taro ───────────────────────────────────
    {"bg": "rue", "rain": True,
     "char": None, "side": "left",
     "name": "", "text": "Le lieu de rendez-vous : une ruelle derrière le marché couvert de Chinatown. 23h00."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je prends position vingt minutes en avance. Les pièges se voient mieux quand on arrive le premier."},

    {"bg": "rue", "rain": True,
     "char": "taro", "expr": 0, "side": "right",
     "name": "TARO",
     "text": "Détective Raven... J'espérais que vous viendriez seul. Je m'appelle Taro. J'étais l'assistant comptable de Vane."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le comptable du comptable. Pratique. Qu'est-ce qui vous retient encore en vie, Taro ?"},

    {"bg": "rue", "rain": True,
     "char": "taro", "expr": 1, "side": "right",
     "name": "TARO",
     "text": "Eux ne savent pas que j'existe. Marcus gardait mes noms hors des registres. Mais j'ai tout vu. Tout entendu."},

    {"bg": "rue", "rain": True,
     "char": "taro", "expr": 1, "side": "right",
     "name": "TARO",
     "text": "La nuit de sa mort, Marcus avait rendez-vous avec un homme qui portait un badge de la police.",
     "evidence": ("Photo du Fantôme", "Silhouette avec badge policier")},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un flic. Il y a un flic dans la Synarchie."},

    {"bg": "rue", "rain": True,
     "char": "taro", "expr": 0, "side": "right",
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
     "text": "Je connais cette voix. Je l'ai entendue ce matin même dans les couloirs du commissariat central. Ferrière."},

    # ── Branche : Garder ses distances ────────────────────────────────────────
    {"id": "ch2_resist",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je ne touche pas à l'appareil. Les téléphones piégés existent. On me copie les empreintes, on me géolocalise. Non merci."},

    {"id": "ch2_resist_2",
     "bg": "rue", "rain": True,
     "char": "taro", "expr": 0, "side": "right",
     "name": "TARO",
     "text": "Je comprends la prudence. Alors je vais juste vous dire le nom. Commandant Ferrière. Brigade criminelle."},

    {"id": "ch2_resist_3",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ferrière. Le supérieur direct de Sato. Mon sang se glace.",
     "evidence": ("Enregistrement Taro", "Ferrière impliqué — Synarchie")},

    # ── ACTE 3 Ch2 : La révélation — Ferrière ─────────────────────────────────
    {"bg": "salle_interrogatoire", "rain": False,
     "char": "ferriere", "expr": 1, "side": "right",
     "name": "CDT. FERRIÈRE",
     "text": "Raven. Je savais que vous ne lâcheriez pas. Vous êtes prévisible, comme tous les idéalistes."},

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

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Une clé dans les affaires de Vane. Que la police n'a pas répertoriée. Loft 7.",
     "evidence": ("Clé du Loft 7", "Accès QG de la Synarchie")},

    # CHOIX B ──────────────────────────────────────────────────────────────────
    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "On a 48h avant que Ferrière réalise qu'on sait. Comment frapper ?",
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
     "char": "ferriere", "expr": 3, "side": "right",
     "name": "CDT. FERRIÈRE",
     "text": "Raven. Je savais que vous viendriez ici. Saisissez-le."},

    {"id": "ch2_infiltrate_6",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ferrière. Il est ici. Il savait que je viendrais. Sato... j'espère que tu as le plan B."},

    # ── Branche : Presse ──────────────────────────────────────────────────────
    {"id": "ch2_press",
     "bg": "bureau", "rain": False,
     "char": "natasha", "expr": 0, "side": "right",
     "name": "NATASHA MORI",
     "text": "Raven. Ça fait longtemps. Vous avez quelque chose de solide ?"},

    {"id": "ch2_press_2",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je lui envoie une copie cryptée des fichiers Synarchie. Et j'attends. Vingt minutes plus tard, elle rappelle."},

    {"id": "ch2_press_3",
     "bg": "bureau", "rain": False,
     "char": "natasha", "expr": 3, "side": "right",
     "name": "NATASHA MORI",
     "text": "C'est énorme. On publie demain matin. Mais mon rédac' chef vient d'être convoqué par la préfecture. Ils savent déjà."},

    {"id": "ch2_press_4",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ils ont des oreilles partout. Il faut les forcer à agir avant qu'ils musèlent le Tribune.",
     "evidence": ("Rapport interne", "Fuite détectée — fenêtre courte")},

    # ── ACTE 4 Ch2 : La confrontation ─────────────────────────────────────────
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
     "char": "ferriere", "expr": 2, "side": "right",
     "name": "CDT. FERRIÈRE",
     "text": "Je vous ai sous-estimé, Raven. Dommage. J'aurais pu vous utiliser. Vous êtes exactement le genre de chien qu'on dresse bien."},

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

    # ── ÉPILOGUE CH2 ──────────────────────────────────────────────────────────
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
     "name": "", "text": "─── FIN DU CHAPITRE II ───"},

    # ══════════════════════════════════════════════════════════════════════════
    # ████  CHAPITRE III — "L'Architecte"  ████
    # ══════════════════════════════════════════════════════════════════════════

    {"bg": "aeroport_jetpack", "rain": False,
     "char": None, "side": "left",
     "name": "", "text": "CHAPITRE III — L'Architecte"},

    {"bg": "aeroport_jetpack", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Aéroport. 4h du matin. Un jet privé en attente sur le tarmac. Natasha Mori a arrangé l'embarquement."},

    {"bg": "aeroport_jetpack", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Raven. Passeport propre. Alias : Thomas Renard. Durée du séjour : 72h. Après ça, Genève devient trop dangereuse."},

    {"bg": "aeroport_jetpack", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "72 heures pour trouver l'Architecte. Identifier un fantôme qui contrôle douze pays. Dans une ville qu'il possède probablement."},

    {"bg": "aeroport_jetpack", "rain": False,
     "char": "natasha", "expr": 0, "side": "right",
     "name": "NATASHA MORI",
     "text": "J'ai fait des recherches. L'adresse laissée par Taro correspond à une fondation philanthropique. Façade classique."},

    {"bg": "aeroport_jetpack", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Une fondation. Bien sûr. L'argent sale adore les bonnes causes."},

    {"bg": "aeroport_jetpack", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Je vous rejoins dans six heures. J'ai un contact à Interpol qui peut nous couvrir. Officiellement."},

    {"bg": "aeroport_jetpack", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Non. Sato reste. Si je disparais à Genève, il faut quelqu'un pour porter les preuves en lieu sûr."},

    {"bg": "aeroport_jetpack", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven... ne faites pas l'idiot. Ces gens-là ne jouent pas."},

    {"bg": "aeroport_jetpack", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Moi non plus."},

    # ── ACTE 2 Ch3 : Arrivée à Genève ─────────────────────────────────────────
    {"bg": "geneve", "rain": True,
     "char": None, "side": "left",
     "name": "", "text": "Genève. Il pleut. Bien sûr. Il pleut toujours quand les choses sérieuses commencent."},

    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La Fondation Meridian. Façade en pierre du XVIIIe. Discret. Respectable. Parfait pour cacher l'irrespectable."},

    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je surveille l'entrée depuis une heure. Deux gardes. Rotation toutes les trente minutes. Caméras aux angles."},

    {"bg": "geneve", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Un homme sort. Costume gris. Cravate sombre. Il lève les yeux vers moi depuis la rue, comme s'il savait."},

    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il sait. Il m'attendait."},

    {"bg": "geneve", "rain": True,
     "char": "architect", "expr": 2, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Détective Raven. Vous avez mis plus de temps que prévu. Entrez donc. J'ai du thé."},

    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il m'invite. Comme si j'étais un visiteur attendu. Comme si toute cette enquête... était prévue."},

    {"bg": "geneve", "rain": True,
     "char": "architect", "expr": 1, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Parce qu'elle l'était, Raven. Vane devait mourir. Ferrière devait tomber. Et vous deviez venir jusqu'ici."},

    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous avez tout orchestré. Depuis le début. Même l'enquête."},

    {"bg": "geneve", "rain": True,
     "char": "architect", "expr": 0, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Ferrière était devenu incontrôlable. Trop gourmand. Trop visible. Il me fallait quelqu'un d'honnête pour le nettoyer proprement.",
     "evidence": ("Passeport Fantôme", "Identité multiple — fondation Meridian")},

    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous m'avez utilisé. Comme un outil de nettoyage."},

    {"bg": "geneve", "rain": True,
     "char": "architect", "expr": 1, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Je préfère 'instrument de précision'. Vous avez du talent, Raven. C'est rare. Et les gens de talent m'intéressent.",
     "evidence": ("Schéma du Réseau", "Organigramme Synarchie — 12 nations")},

    # CHOIX D ──────────────────────────────────────────────────────────────────
    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "L'Architecte propose... un accord. Comment répondre à cette manipulation ?",
     "choices": ["Affronter directement", "Jouer le jeu — l'observer"],
     "choice_branch": {"0": "ch3_confront", "1": "ch3_shadow"}},

    # ── Branche : Affronter ────────────────────────────────────────────────────
    {"id": "ch3_confront",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Assez. Je ne suis l'instrument de personne. Pas même d'un homme qui se croit au-dessus des lois."},

    {"id": "ch3_confront_2",
     "bg": "geneve", "rain": True,
     "char": "architect", "expr": 3, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Décevant. Vraiment. J'espérais mieux de vous."},

    {"id": "ch3_confront_3",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Pendant qu'il parle, je transmets sa position en temps réel à Natasha. Et j'enregistre tout."},

    # ── Branche : Observer ─────────────────────────────────────────────────────
    {"id": "ch3_shadow",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je souris. Je joue le jeu. Laisser un homme parler, c'est lui donner une corde pour se pendre."},

    {"id": "ch3_shadow_2",
     "bg": "geneve", "rain": True,
     "char": "architect", "expr": 2, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Excellent choix. Laissez-moi vous montrer quelque chose. L'accord que j'ai préparé. Pour vous. Et pour Sato."},

    {"id": "ch3_shadow_3",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il sort un dossier. Je mémorise chaque détail. Chaque chiffre. Chaque nom.",
     "evidence": ("Accord Secret", "Contrat de corruption — 6 gouvernements")},

    # ── ACTE 3 Ch3 : La vérité sur le réseau ──────────────────────────────────
    {"bg": "geneve", "rain": True,
     "char": "architect", "expr": 0, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "La Synarchie n'est pas un réseau criminel, Raven. C'est un système de stabilité. Nous maintenons l'ordre là où les États ont échoué."},

    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "En tuant des comptables. En corrompant des juges. En achetant des commandants de police."},

    {"bg": "geneve", "rain": True,
     "char": "architect", "expr": 1, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "En faisant des choix difficiles. Ceux que les démocraties sont trop lâches pour faire."},

    {"bg": "geneve", "rain": True,
     "char": "natasha", "expr": 3, "side": "right",
     "name": "NATASHA MORI",
     "text": "Raven. Je suis en ligne. J'ai tout reçu. L'enregistrement tourne déjà sur cinq serveurs miroirs."},

    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous avez entendu, Architecte ? La presse a tout. Dans quatre heures, votre nom sera sur tous les écrans du monde."},

    {"bg": "geneve", "rain": True,
     "char": "architect", "expr": 3, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Mon nom... Vous croyez vraiment que vous avez trouvé mon vrai nom ?",
     "evidence": ("Enregistrement final", "Aveux de l'Architecte — diffusion mondiale")},

    # CHOIX E ──────────────────────────────────────────────────────────────────
    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "L'Architecte semble... amusé. Trop calme. Quelque chose ne va pas. Quelle est la bonne décision ?",
     "choices": ["Exposer maintenant — tout publier", "Négocier — obtenir les noms restants"],
     "choice_branch": {"0": "ch3_expose", "1": "ch3_negotiate"}},

    # ── Branche : Exposer ─────────────────────────────────────────────────────
    {"id": "ch3_expose",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Natasha, publie. Tout. Maintenant. On ne négocie pas avec les architectes du crime."},

    {"id": "ch3_expose_2",
     "bg": "geneve", "rain": True,
     "char": "natasha", "expr": 2, "side": "right",
     "name": "NATASHA MORI",
     "text": "C'est parti. Le Tribune, Le Monde, The Guardian... simultané. Dans deux minutes, c'est mondial."},

    {"id": "ch3_expose_3",
     "bg": "geneve", "rain": True,
     "char": "architect", "expr": 3, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Vous venez de déstabiliser douze gouvernements en même temps, Raven. Êtes-vous certain d'être le héros de cette histoire ?"},

    # ── Branche : Négocier ────────────────────────────────────────────────────
    {"id": "ch3_negotiate",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Attendez, Natasha. Pas encore. Architecte... il y a d'autres noms dans ce registre. Donnez-les moi. Tous."},

    {"id": "ch3_negotiate_2",
     "bg": "geneve", "rain": True,
     "char": "architect", "expr": 0, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Intéressant. Vous avez plus de finesse que je ne le pensais. Voilà qui change tout."},

    {"id": "ch3_negotiate_3",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il fait glisser un autre dossier sur la table. Plus épais. Beaucoup plus épais.",
     "evidence": ("Identité de l'Architecte", "Nom réel + liste complète Synarchie")},

    # ── ACTE FINAL Ch3 : Le choix ultime ──────────────────────────────────────
    {"bg": "geneve", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "La situation a basculé. Des sirènes au loin. Interpol. Quelqu'un a donné la position. Mais qui ?"},

    {"bg": "geneve", "rain": True,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. C'est moi. J'ai contacté Interpol directement. Ils arrivent. Mais la Synarchie aussi."},

    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Sato... vous n'étiez pas censée venir."},

    {"bg": "geneve", "rain": True,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Non. Mais on fait équipe, Raven. Vous l'aviez oublié ?"},

    {"bg": "geneve", "rain": True,
     "char": "architect", "expr": 3, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Touchant. Vraiment. Mais vous comprenez que ni l'un ni l'autre ne peut quitter cette pièce vivant."},

    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Deux gardes bloquent la sortie. L'Architecte garde son calme. Le temps se fige.",
     "choices": ["Se sacrifier pour couvrir Sato", "Fuir avec les preuves"],
     "choice_branch": {"0": "ch3_sacrifice", "1": "ch3_escape"}},

    # ── Branche : Sacrifice ────────────────────────────────────────────────────
    {"id": "ch3_sacrifice",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Sato. Prenez le dossier. Sortez par l'arrière. Ne vous retournez pas."},

    {"id": "ch3_sacrifice_2",
     "bg": "geneve", "rain": True,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven... Non. Je ne vous laisse pas ici."},

    {"id": "ch3_sacrifice_3",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "C'est un ordre, Officier Sato. Allez."},

    {"id": "ch3_sacrifice_4",
     "bg": "geneve", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Elle part. Je retourne me placer face aux gardes. Face à l'Architecte. Pour la dernière fois peut-être."},

    {"id": "ch3_sacrifice_5",
     "bg": "geneve", "rain": True,
     "char": "architect", "expr": 1, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Vous mourrez pour une femme que vous connaissez depuis trois semaines."},

    {"id": "ch3_sacrifice_6",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Non. Je meurs pour que quelqu'un d'honnête continue d'exister dans ce monde que vous avez pourri."},

    # ── Branche : Fuite ───────────────────────────────────────────────────────
    {"id": "ch3_escape",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Les preuves d'abord. Toujours les preuves. Je plonge vers la fenêtre latérale. Sato comprend et suit."},

    {"id": "ch3_escape_2",
     "bg": "geneve", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Le verre éclate. La pluie nous accueille. Les coups de feu dans notre dos. On court."},

    {"id": "ch3_escape_3",
     "bg": "geneve", "rain": True,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "La voiture d'Interpol ! Là, à droite !"},

    {"id": "ch3_escape_4",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On s'engouffre dedans. Les portières claquent. Les pneus crissent. On a les preuves. On a survécu."},

    # ── ÉPILOGUE FINAL ─────────────────────────────────────────────────────────
    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Deux semaines plus tard. Les premières arrestations ont commencé. Trois ministres. Un juge de la Cour internationale."},

    {"bg": "toit", "rain": False,
     "char": "natasha", "expr": 2, "side": "right",
     "name": "NATASHA MORI",
     "text": "Le Pulitzer, Raven. Ils parlent du Pulitzer. Et vous ? Où allez-vous, maintenant ?"},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "L'Architecte s'est volatilisé avant l'arrivée d'Interpol. Il existe d'autres noms dans ce registre. Des plus grands encore."},

    {"bg": "toit", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Suspension levée. Médaille du mérite. Et une offre d'Interpol. Je leur ai dit que j'avais déjà un partenaire."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Sato... vous êtes incorrigible."},

    {"bg": "toit", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "On fait équipe, Raven. C'est vous qui me l'avez appris."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Quelque part dans cette ville — ou dans une autre — l'Architecte reconstruit. Il est patient. Il l'a toujours été."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mais moi aussi."},

    {"bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "─── FIN DU CHAPITRE III ───\n\nNUIT SANS TÉMOIN — L'histoire continue..."},
]