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

# ═══════════════════════════════════════════════════════════════════════════════
# NUIT SANS TÉMOIN — script_chapitres_4_5_6_7.py
# Chapitres IV, V, VI & VII — "L'Héritage"
# ═══════════════════════════════════════════════════════════════════════════════
#
# PERSONNAGES :
#   detective  — 10 expressions (0=neutre 1=sourire 2=large 3=colère 4=triste
#                                5=regard  6=smirk   7=shocked 8=smug  9=tired)
#   policiere  — 4 expressions  (0=neutre 1=serieux 2=sourire 3=shocked)
#   natasha    — 4 expressions  (0=neutre 1=serieux 2=sourire 3=shocked)
#   taro       — 4 expressions  (0=neutre 1=serieux 2=sourire 3=shocked)
#   architect  — 4 expressions  (0=neutre 1=serieux 2=sourire 3=shocked)
#   mira       — 4 expressions  (0=neutre 1=serieux 2=sourire 3=shocked)  [NOUVEAU]
#   ghost      — 4 expressions  (0=neutre 1=serieux 2=sourire 3=shocked)  [NOUVEAU Ch6]
#   senator    — 4 expressions  (0=neutre 1=serieux 2=sourire 3=shocked)  [NOUVEAU Ch7]
#
# BACKGROUNDS Ch4-7 (à créer) :
#   appartement   — intérieur nuit, lumière froide
#   parking       — parking souterrain, béton, néons
#   archives      — salle d'archives, poussiéreux, vert
#   train         — compartiment de train nuit
#   hôtel_berlin  — chambre d'hôtel luxueuse, Berlin
#   parlement     — couloirs du parlement européen
#   sous_sol      — salle de serveurs clandestine
#   toit          — (existant, réutilisé)
#   bureau        — (existant, réutilisé)
#   rue           — (existant, réutilisé)
#
# ARBRE DE DÉCISIONS :
#   Ch4 : Choix G → ch4_contact / ch4_solo
#         Choix H → ch4_protect / ch4_record
#         Choix I → ch4_press / ch4_infiltrate
#   Ch5 : Choix J → ch5_trust_mira / ch5_doubt_mira
#         Choix K → ch5_confront_ghost / ch5_follow_ghost
#         Choix L → ch5_burn / ch5_keep
#   Ch6 : Choix M → ch6_senate / ch6_underground
#         Choix N → ch6_ally / ch6_alone
#         Choix O → ch6_expose_live / ch6_disappear
#   Ch7 : Choix P → ch7_trust_sato / ch7_protect_sato
#         Choix Q → ch7_architect_deal / ch7_architect_end
#         Choix R → ch7_light / ch7_shadow  (fin ouverte)
#
# PREUVES :
#   Ch4 : Photo de surveillance, Clé USB #2, Liste de contacts, Badge magnétique,
#          Dossier Mira
#   Ch5 : Identité du Fantôme, Serveur miroir, Accord de Berlin, Témoin protégé
#   Ch6 : Enregistrement parlement, Compte numéroté, Identité du Sénateur,
#          Dossier fantôme vol 219
#   Ch7 : Testament de Vane, Preuve ultime, Coordonnées bunker, Décision finale
#
# DÉDUCTIONS :
#   Ch4 : Photo surveillance + Badge magnétique → "Surveillance institutionnelle"
#         Clé USB #2 + Fichiers Synarchie       → "Le successeur prévu"
#         Liste contacts + Identité Architecte   → "Réseau survivant — 3 ministres"
#         Dossier Mira + Photo surveillance      → "Mira — actif ou double jeu ?"
#   Ch5 : Identité Fantôme + Accord Berlin      → "Le Fantôme est l'architecte adjoint"
#         Serveur miroir + Clé USB #2            → "Les données ne meurent pas"
#         Témoin protégé + Enregistrement Taro   → "Chaîne de commandement reconstituée"
#   Ch6 : Enregistrement parlement + Accord Secret → "Corruption au sommet de l'UE"
#         Compte numéroté + Registre Offshore    → "Même banque, 20 ans après"
#         Identité Sénateur + Liste contacts     → "Le législateur est la Synarchie"
#   Ch7 : Testament Vane + Dossier Vane Ch1      → "Vane savait depuis le début"
#         Preuve ultime + Schéma du Réseau        → "L'organigramme est complet"
#         Coordonnées bunker + Passeport Fantôme  → "L'Architecte n'a jamais fui"
#
# CG :
#   cg_14_appartement  — Raven face à la photo de surveillance
#   cg_15_mira         — Premier contact avec Mira, parking souterrain
#   cg_16_archives     — La salle des archives secrètes
#   cg_17_trahison     — Mira révèle sa vraie nature (branche ch5_doubt_mira)
#   cg_18_berlin       — Raven et Sato, chambre d'hôtel Berlin, avant la tempête
#   cg_19_fantôme      — Le Fantôme démasqué
#   cg_20_parlement    — Vue sur le parlement européen la nuit
#   cg_21_bunker       — Le bunker de l'Architecte
#   cg_22_fin_lumière  — Épilogue : Raven sur le toit, aube dorée
#   cg_23_fin_ombre    — Épilogue : Raven disparaît dans la foule
#
# ═══════════════════════════════════════════════════════════════════════════════

# ── Instructions d'intégration ─────────────────────────────────────────────────
# Pour intégrer ces chapitres dans script.py :
# 1. Remplacer le ] final de SCRIPT = [...] par une virgule
# 2. Coller le contenu de SCRIPT_CH4567 à la suite
# 3. Terminer par ]
# Ou utiliser : SCRIPT = SCRIPT + SCRIPT_CH4567
# ─────────────────────────────────────────────────────────────────────────────


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
     "cg": "cg_01_ruelle",
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
     "cg": "cg_02_cle_usb",
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
     "bg": "salle_interrogatoire", "rain": False, "transition": "iris",
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "On a un témoin. Il refuse de parler, mais il a vu quelque chose cette nuit-là."},

    # ── ACTE 2 : La rue ────────────────────────────────────────────────────────
    {"bg": "rue", "rain": True, "transition": "fade_black",
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
    {"bg": "bureau", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_03_bureau_nuit",
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
     "bg": "toit", "rain": False, "transition": "slide_left",
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Cette ville. Elle ne dort jamais. Et moi non plus."},

    # Branche équipe ───────────────────────────────────────────────────────────
    {"id": "team",
     "bg": "toit", "rain": False, "transition": "slide_left",
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
     "cg": "cg_04_toit",
     "text": "Et moi, je la trouverai. C'est ma promesse à Marcus Vane. À tous les Marcus de ce monde."},

    {"bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "", "text": "─── FIN DU CHAPITRE I ───"},

    # ── Marqueur fin de chapitre I → carte narrative ─────────────────────────
    {"chapter_end": 1, "bg": "toit", "char": None, "side": "left",
     "name": "", "text": ""},

    # ══════════════════════════════════════════════════════════════════════════
    # ████  CHAPITRE II — "Le Prix de la Vérité"  ████
    # ══════════════════════════════════════════════════════════════════════════

    {"bg": "toit", "rain": False, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "", "text": "CHAPITRE II — Le Prix de la Vérité"},

    {"bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Trois jours ont passé. La clé USB de Marcus Vane a ouvert une boîte de Pandore."},

    {"bg": "bureau", "rain": False, "transition": "fade_black",
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
    {"bg": "rue", "rain": True, "transition": "slide_left",
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
    {"bg": "salle_interrogatoire", "rain": False, "transition": "iris",
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

    {"bg": "bureau", "rain": False, "transition": "fade_black",
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
     "bg": "rue", "rain": True, "transition": "slide_left",
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
    {"bg": "salle_interrogatoire", "rain": False, "transition": "iris",
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
     "bg": "bureau", "rain": False, "transition": "fade_black",
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
    {"bg": "toit", "rain": False, "transition": "slide_left",
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

    # ── Marqueur fin de chapitre II → carte narrative ────────────────────────
    {"chapter_end": 2, "bg": "toit", "char": None, "side": "left",
     "name": "", "text": ""},

    # ══════════════════════════════════════════════════════════════════════════
    # ████  CHAPITRE III — "L'Architecte"  ████
    # ══════════════════════════════════════════════════════════════════════════

    {"bg": "aeroport_jetpack", "rain": False, "transition": "fade_black",
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
    {"bg": "geneve", "rain": True, "transition": "slide_left",
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
    {"bg": "toit", "rain": False, "transition": "fade_white",
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

    # ── Marqueur fin de chapitre III → carte narrative ───────────────────────
    {"chapter_end": 3, "bg": "toit", "char": None, "side": "left",
     "name": "", "text": ""},

    # ── Titre ──────────────────────────────────────────────────────────────────
    {"bg": "appartement", "rain": True, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "", "text": "CHAPITRE IV — L'Héritage"},

    {"bg": "appartement", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Six mois après Genève. La Synarchie est officiellement démantelée. Officiellement."},

    # ── ACTE 1 Ch4 : L'appartement, minuit ────────────────────────────────────
    {"bg": "appartement", "rain": True,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_14_appartement",
     "text": "Je suis en congé forcé depuis trois semaines. La Préfecture appelle ça 'une période de décompression'. J'appelle ça une mise au placard."},

    {"bg": "appartement", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mon appartement ressemble à un bureau. Dossiers partout. Fils rouges. Photos. Je n'arrive plus à m'arrêter."},

    {"bg": "appartement", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Un bruit. Pas une souris. Quelqu'un a glissé une enveloppe sous la porte. En pleine nuit."},

    {"bg": "appartement", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Une clé USB. Et une photo. Moi. Hier. Dans ma cuisine. Prise depuis l'extérieur, travers la vitre.",
     "evidence": ("Photo de surveillance", "Raven photographié chez lui — 48h")},

    {"bg": "appartement", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ils savent où j'habite. Ils savent ce que je mange. Ils savent que je n'ai pas arrêté d'enquêter."},

    {"bg": "appartement", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La clé USB. Elle est identique à celle de Vane. Même modèle. Même usure sur le coin droit. Ce n'est pas un hasard.",
     "evidence": ("Clé USB #2", "Données partiellement cryptées — expéditeur inconnu")},

    {"bg": "appartement", "rain": True,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je passe la nuit à la déchiffrer. 80% des fichiers sont corrompus. Mais ce qui reste... Une liste. Des noms codés. Et un badge."},

    {"bg": "appartement", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le badge d'accès porte un logo. Celui du Parlement Européen. Ce n'est plus une affaire de rue. Ça n'a jamais été une affaire de rue.",
     "evidence": ("Badge magnétique", "Accès Parlement Européen — identité inconnue")},

    {"bg": "appartement", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La liste de contacts. Noms codifiés. Mais trois d'entre eux... des initiales que je reconnais. Des ministres en exercice.",
     "evidence": ("Liste de contacts", "Noms codés — 3 correspondances ministérielles")},

    # ── Choix G ────────────────────────────────────────────────────────────────
    {"bg": "appartement", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Quelqu'un m'envoie ces informations. Quelqu'un qui sait où je vis. Comment répondre ?",
     "choices": ["Contacter Sato — on fait équipe", "Agir seul — c'est un piège possible"],
     "choice_branch": {"0": "ch4_contact", "1": "ch4_solo"}},

    # ── Branche : Contacter Sato ───────────────────────────────────────────────
    {"id": "ch4_contact",
     "bg": "bureau", "rain": False, "transition": "slide_left",
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. Il est 3h du matin. Vous avez une bonne raison de... Oh. Je vois. Je suis là dans vingt minutes."},

    {"id": "ch4_contact_2",
     "bg": "bureau", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Le badge d'accès. J'en ai un identique dans mes dossiers. Affaire classée il y a deux ans. Un diplomate mort dans un accident de voiture."},

    {"id": "ch4_contact_3",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Accident. Comme Vane. Comme tous ceux qui approchent trop près. Combien d'accidents faut-il avant qu'on appelle ça un système ?"},

    # ── Branche : Agir seul ────────────────────────────────────────────────────
    {"id": "ch4_solo",
     "bg": "appartement", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Sato est dans les registres. Si quelqu'un me surveille, il surveille aussi mes contacts. Je ne la mets pas en danger."},

    {"id": "ch4_solo_2",
     "bg": "appartement", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je travaille seul cette nuit. Demain, si je suis encore vivant, j'aviserai. C'est le plan. Simple. Brutal. Efficace."},

    {"id": "ch4_solo_3",
     "bg": "appartement", "rain": True,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je croise le badge avec les données de la clé. Un nom commence à prendre forme. Quelqu'un que je n'aurais pas dû chercher. Pas seul."},

    # ── ACTE 2 Ch4 : Le parking souterrain ────────────────────────────────────
    {"bg": "parking", "rain": False, "transition": "iris",
     "char": None, "side": "left",
     "name": "",
     "text": "Une adresse dans la clé USB. Un parking sous-terrain du 8ème arrondissement. 17h30. L'heure des employés de bureau."},

    {"bg": "parking", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je prends position entre deux colonnes en béton. Néons qui clignotent. Odeur d'huile. Un endroit choisi pour ne pas être mémorisé."},

    {"bg": "parking", "rain": False,
     "char": "mira", "expr": 0, "side": "right",
     "name": "MIRA VOSS",
     "cg": "cg_15_mira",
     "text": "Détective Raven. Je vous ai envoyé la clé. Je m'appelle Mira Voss. J'étais analyste au Renseignement Intérieur."},

    {"bg": "parking", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Étais. Passé. Vous avez quitté le service. Ou on vous en a sortie."},

    {"bg": "parking", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "On m'a poussée dehors il y a huit mois. Après que j'ai signalé des anomalies dans les flux de financement parlementaire. Ils m'ont dit que je fantasmais."},

    {"bg": "parking", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mais vous n'avez pas abandonné."},

    {"bg": "parking", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "J'ai passé huit mois à reconstruire ce que j'avais vu. La Synarchie ne s'est pas effondrée à Genève. Elle s'est réorganisée. Sous un nouveau nom. Un nouveau visage."},

    {"bg": "parking", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un successeur. L'Architecte avait prévu sa propre chute. Il avait formé quelqu'un."},

    {"bg": "parking", "rain": False,
     "char": "mira", "expr": 0, "side": "right",
     "name": "MIRA VOSS",
     "text": "Ils l'appellent le Fantôme. Personne ne connaît son identité. Pas même la plupart des membres du réseau. C'est la leçon que l'Architecte a tirée de Genève.",
     "evidence": ("Dossier Mira", "Analyste ex-RG — 8 mois d'enquête indépendante")},

    {"bg": "parking", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le Fantôme. Un nom qui ne renvoie à rien. C'est ça, la vraie protection. Ne pas exister."},

    {"bg": "parking", "rain": False,
     "char": "mira", "expr": 3, "side": "right",
     "name": "MIRA VOSS",
     "text": "Il existe. J'ai une piste. Mais si je vous la donne maintenant, vous devenez une cible aussi. Êtes-vous prêt ?"},

    # ── Choix H ────────────────────────────────────────────────────────────────
    {"bg": "parking", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Mira Voss. Analyste mise sur la touche. Elle a des infos. Et un agenda que je ne connais pas encore.",
     "choices": ["Lui accorder ma confiance — elle a pris des risques pour venir", "Enregistrer secrètement — vérifier avant d'aller plus loin"],
     "choice_branch": {"0": "ch4_protect", "1": "ch4_record"}},

    # ── Branche : Faire confiance à Mira ──────────────────────────────────────
    {"id": "ch4_protect",
     "bg": "parking", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Oui. Je suis prêt. Vous avez traversé tout ça seule pendant huit mois. C'est déjà une preuve que vous n'êtes pas un leurre."},

    {"id": "ch4_protect_2",
     "bg": "parking", "rain": False,
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "Le Fantôme a un bureau au Parlement Européen. Pas au nom de la Synarchie, bien sûr. Au nom d'une commission consultative sur la sécurité numérique."},

    {"id": "ch4_protect_3",
     "bg": "parking", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Une commission. Parfait. Surveiller la sécurité numérique depuis l'intérieur. Accès aux données. Accès aux systèmes. Accès aux hommes."},

    # ── Branche : Enregistrer Mira ─────────────────────────────────────────────
    {"id": "ch4_record",
     "bg": "parking", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Oui. Je suis prêt. En appuyant sur record. Discrètement. Dans ma poche. Mira Voss mérite une vérification avant une confiance."},

    {"id": "ch4_record_2",
     "bg": "parking", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "Le Fantôme a un bureau au Parlement. Pas en son nom. Au nom d'une commission consultative. C'est là que les décisions se prennent. Loin des caméras."},

    {"id": "ch4_record_3",
     "bg": "parking", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je vérifie l'enregistrement ce soir. Analyse de voix. Croisement d'informations. Si Mira dit vrai, je la rappelle. Si elle ment, j'ai une preuve."},

    # ── ACTE 3 Ch4 : La salle des archives ────────────────────────────────────
    {"bg": "archives", "rain": False, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "",
     "text": "Mira possède un accès à des archives déclassifiées partiellement. Des dossiers sur la restructuration post-Genève."},

    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_16_archives",
     "text": "Des cartons. Des microfils. Des disques durs de récupération. Ce qu'on a sauvé quand ils ont 'accidentellement' formaté les serveurs du Renseignement."},

    {"bg": "archives", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "J'ai passé quatre mois ici. Ce bâtiment sera démoli dans deux semaines. Tout part à la destruction. Légalement."},

    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La destruction programmée. Bien sûr. Propre. Bureaucratique. Parfaitement légal."},

    {"bg": "archives", "rain": False,
     "char": "mira", "expr": 0, "side": "right",
     "name": "MIRA VOSS",
     "text": "Regardez ça. Dossier 219-K. Vol 219. Paris-Budapest, il y a dix ans. Crash inexpliqué. 147 morts. L'enquête a été close en 72 heures."},

    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je connais ce crash. Tout le monde le connaît. On nous a dit que c'était une panne technique. Mais..."},

    {"bg": "archives", "rain": False,
     "char": "mira", "expr": 3, "side": "right",
     "name": "MIRA VOSS",
     "text": "Parmi les 147 morts. Le témoin principal d'un procès anticorruption à Bruxelles. Trois journalistes d'investigation. Et un ancien comptable de la Synarchie."},

    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vane. Marcus Vane connaissait le crash 219. C'est pour ça qu'ils l'ont tué maintenant. Il allait parler."},

    {"bg": "archives", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "Et moi j'ai trouvé le nom du commanditaire. Le Fantôme n'est pas apparu après Genève. Il existait déjà. Il y a dix ans. Il était l'Architecte adjoint."},

    # ── Choix I ────────────────────────────────────────────────────────────────
    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Ces archives sont détruites dans deux semaines. Et le Fantôme nous cherche. Comment frapper en premier ?",
     "choices": ["Contacter la presse internationale — rendre public maintenant", "S'infiltrer au Parlement — aller chercher le Fantôme sur son terrain"],
     "choice_branch": {"0": "ch4_press", "1": "ch4_infiltrate"}},

    # ── Branche : Contacter la presse ─────────────────────────────────────────
    {"id": "ch4_press",
     "bg": "archives", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Natasha. Je sais que vous êtes en surveillance. Oui, je sais que vous avez posé des journalistes autour de moi depuis Genève. Vous avez fait des copies des archives ?"},

    {"id": "ch4_press_2",
     "bg": "archives", "rain": False,
     "char": "natasha", "expr": 2, "side": "right",
     "name": "NATASHA MORI",
     "text": "Raven. Bien sûr que j'en ai fait. Ce sont vos nouvelles données. Le crash 219. Dix ans. On publie ça et la commission parlementaire tombe."},

    {"id": "ch4_press_3",
     "bg": "archives", "rain": False,
     "char": "mira", "expr": 3, "side": "right",
     "name": "MIRA VOSS",
     "text": "Attendez. Si on publie maintenant, le Fantôme disparaît. On a son profil mais pas son identité. On perd la seule chance de le piéger."},

    {"id": "ch4_press_4",
     "bg": "archives", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mira a raison. On publie les données du crash 219. On garde le reste. La pression de la presse force la commission à bouger. Et quand elle bouge, le Fantôme se trahit."},

    # ── Branche : Infiltrer le Parlement ──────────────────────────────────────
    {"id": "ch4_infiltrate",
     "bg": "parking", "rain": False, "transition": "slide_left",
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On n'expose pas ce qu'on n'a pas. On identifie d'abord le Fantôme. Et pour ça, il faut entrer dans sa maison."},

    {"id": "ch4_infiltrate_2",
     "bg": "parking", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "J'ai un badge de consultant. Périmé depuis six mois. Mais les accès de la commission ne sont pas encore révoqués. J'ai vérifié hier."},

    {"id": "ch4_infiltrate_3",
     "bg": "parking", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Six mois. Quelqu'un a oublié de révoquer l'accès d'une analyste licenciée. Le genre de négligence qui n'existe pas dans leur monde. Sauf si on l'a voulu ainsi."},

    {"id": "ch4_infiltrate_4",
     "bg": "parking", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mira. Votre badge. On vous a laissé cet accès ouvert. Ce n'est pas une négligence. C'est une invitation. C'est peut-être un piège."},

    {"id": "ch4_infiltrate_5",
     "bg": "parking", "rain": False,
     "char": "mira", "expr": 3, "side": "right",
     "name": "MIRA VOSS",
     "text": "...Je sais. J'y ai pensé. Mais si c'est un piège, c'est qu'ils ont peur. Et la peur, ça se retourne."},

    # ── ÉPILOGUE CH4 ───────────────────────────────────────────────────────────
    {"bg": "toit", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Cette nuit-là, j'établis les connexions. La Synarchie n'est pas morte. Elle a mué. Elle est passée du crime organisé à la politique institutionnelle."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vane comptait l'argent d'un comptable local. Le Fantôme alloue des budgets nationaux. L'échelle a changé. La méthode reste la même."},

    {"bg": "toit", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. Interpol m'a contactée. Officiellement, ils ont clos le dossier Synarchie. Officieusement... ils savent que ça continue. Ils attendent quelqu'un qui veut bien s'y coller."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 8, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Interpol. Des ressources. Une couverture légale. Et sûrement des fuites dans leurs rangs. Mais tout ça, c'est pour demain."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Cette nuit, il y a juste moi. La pluie sur les toits de Paris. Et un Fantôme quelque part dans l'Europe qui pense avoir gagné."},

    {"bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "", "text": "─── FIN DU CHAPITRE IV ───"},

    # Marqueur fin de chapitre → NarrativeMap
    {"chapter_end": 4, "bg": "toit", "char": None, "side": "left", "name": "", "text": ""},

    # ══════════════════════════════════════════════════════════════════════════
    # ████  CHAPITRE V — "Le Fantôme"  ████
    # ══════════════════════════════════════════════════════════════════════════

    {"bg": "train", "rain": True, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "", "text": "CHAPITRE V — Le Fantôme"},

    {"bg": "train", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Trois semaines après. Train Paris-Berlin, 23h47. Mira a trouvé une conférence parlementaire. Le Fantôme sera là."},

    # ── ACTE 1 Ch5 : Le train, nuit ───────────────────────────────────────────
    {"bg": "train", "rain": True,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Compartiment seul. Dossiers sur la tablette. Le dossier 219 est devenu une bombe à retardement depuis que Natasha en a publié les grandes lignes."},

    {"bg": "train", "rain": True,
     "char": "mira", "expr": 0, "side": "right",
     "name": "MIRA VOSS",
     "text": "J'ai reçu une réponse. D'une adresse cryptée. Quelqu'un qui dit connaître l'identité du Fantôme. Il veut un échange. Les données de Genève contre le nom."},

    {"bg": "train", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un échange. Quelqu'un qui veut nos données de Genève. Et qui propose en retour ce qu'on cherche le plus. C'est beau comme piège."},

    {"bg": "train", "rain": True,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "Peut-être. Ou peut-être que c'est quelqu'un de l'intérieur du réseau qui veut en sortir. Ça arrive. Surtout quand le navire prend l'eau."},

    {"bg": "train", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Depuis Genève, j'ai appris une chose. Quand quelqu'un vous offre exactement ce que vous voulez, demandez-vous d'abord ce que vous allez perdre en échange."},

    # ── Choix J ────────────────────────────────────────────────────────────────
    {"bg": "train", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Mira. Six mois qu'on travaille ensemble. Mais je ne sais toujours pas tout d'elle. Est-ce qu'elle nous guide — ou nous conduit ?",
     "choices": ["Lui faire entièrement confiance — elle a prouvé sa bonne foi", "Jouer double jeu — l'observer sans la laisser tout contrôler"],
     "choice_branch": {"0": "ch5_trust_mira", "1": "ch5_doubt_mira"}},

    # ── Branche : Confiance Mira ───────────────────────────────────────────────
    {"id": "ch5_trust_mira",
     "bg": "train", "rain": True,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mira a tout risqué. Son poste. Sa sécurité. Si elle voulait me trahir, elle avait eu cent occasions. Je réponds à l'adresse cryptée. On accepte l'échange."},

    {"id": "ch5_trust_mira_2",
     "bg": "train", "rain": True,
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "Bien. Je prépare le paquet d'échange. Données réelles mais incomplètes. On donne assez pour avoir l'air sérieux. Pas assez pour tout perdre si c'est un piège."},

    {"id": "ch5_trust_mira_3",
     "bg": "train", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je savais qu'elle était intelligente. La confirmation que j'avais encore raison de lui faire confiance."},

    # ── Branche : Douter de Mira ──────────────────────────────────────────────
    {"id": "ch5_doubt_mira",
     "bg": "train", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "J'accepte. Mais en parallèle, je contacte Sato. Code qu'on a mis en place pour les urgences. Si Mira nous mène dans un piège, Sato a notre position."},

    {"id": "ch5_doubt_mira_2",
     "bg": "train", "rain": True,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Reçu. Raven... soyez prudent. J'ai fait vérifier Mira Voss par un contact à la DGSI. Son dossier est propre. Mais il y a une lacune de dix-huit mois. De deux à quatre ans après votre affaire."},

    {"id": "ch5_doubt_mira_3",
     "bg": "train", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Dix-huit mois. C'est long pour une lacune. Court pour une formation. Je garde l'œil ouvert. Sur tout le monde."},

    {"id": "ch5_doubt_mira_4",
     "bg": "train", "rain": True,
     "char": "mira", "expr": 3, "side": "right",
     "name": "MIRA VOSS",
     "cg": "cg_17_trahison",
     "text": "Raven... je sais que vous m'avez fait vérifier. C'est normal. Je vous dirais la même chose à votre place. Les dix-huit mois... je les expliquerai. À Berlin. Pas maintenant."},

    {"id": "ch5_doubt_mira_5",
     "bg": "train", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Elle sait que je l'ai fait vérifier. Soit elle est très bien informée. Soit elle est très honnête. Dans les deux cas, je ne peux pas me permettre de la perdre."},

    # ── ACTE 2 Ch5 : L'hôtel à Berlin ─────────────────────────────────────────
    {"bg": "hotel_berlin", "rain": False, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "",
     "text": "Berlin. Hôtel Adlon. Chambre 412. La conférence parlementaire commence demain. Le contact mystère nous donne rendez-vous ce soir."},

    {"bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_18_berlin",
     "text": "Sato nous a rejoints. Natasha aussi. Quatre personnes dans une chambre d'hôtel à Berlin. La situation ressemble à un roman d'espionnage de mauvaise qualité."},

    {"bg": "hotel_berlin", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "La situation ressemble surtout à nos trois autres fois où ça a failli très mal tourner. Donc je suis à ma place."},

    {"bg": "hotel_berlin", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Mon rédacteur en chef a reçu une mise en demeure ce matin. Anonyme. 'Publiez encore sur le vol 219 et des gens mourront.' Quelle délicatesse."},

    {"bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ça confirme qu'on frappe juste. Quand ils menacent, c'est qu'ils ont peur. Et la peur, ça produit des erreurs."},

    {"bg": "hotel_berlin", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "23h00. On frappe à la porte. Double coup. Pause. Triple coup. Le signal convenu."},

    {"bg": "hotel_berlin", "rain": False,
     "char": "ghost", "expr": 0, "side": "right",
     "name": "???",
     "text": "Détective Raven. Mon nom n'a pas d'importance pour l'instant. Ce qui importe : je suis l'ancien bras droit du Fantôme. Et je veux sortir."},

    {"bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "L'ancien bras droit. Combien de fois ai-je entendu 'je veux sortir' avant qu'on essaie de me retourner ? Trop. Prouvez-le. Maintenant."},

    {"bg": "hotel_berlin", "rain": False,
     "char": "ghost", "expr": 1, "side": "right",
     "name": "???",
     "text": "Le Fantôme. Son vrai nom. Il s'appelle Viktor Selg. Diplomate suédois. Attaché culturel officiel. Conseiller non officiel de trois commissions européennes.",
     "evidence": ("Identité du Fantôme", "Viktor Selg — diplomate suédois, conseiller UE")},

    {"bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Viktor Selg. J'ai lu son nom dans des comptes rendus de presse. Prix pour services diplomatiques. Homme de l'année dans deux publications. Une façade impeccable."},

    {"bg": "hotel_berlin", "rain": False,
     "char": "ghost", "expr": 1, "side": "right",
     "name": "???",
     "text": "Et il a un serveur miroir. Toutes les données de la Synarchie. Y compris ce que l'Architecte n'a jamais montré à personne. L'Accord de Berlin. 1994.",
     "evidence": ("Accord de Berlin", "Pacte fondateur Synarchie — six États, 1994")},

    # ── Choix K ────────────────────────────────────────────────────────────────
    {"bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Viktor Selg. Un nom. Un serveur. Et un contact qui veut en sortir. Comment approcher le Fantôme ?",
     "choices": ["L'affronter directement à la conférence — terrain public", "Le suivre discrètement — cartographier son réseau d'abord"],
     "choice_branch": {"0": "ch5_confront_ghost", "1": "ch5_follow_ghost"}},

    # ── Branche : Confronter le Fantôme ───────────────────────────────────────
    {"id": "ch5_confront_ghost",
     "bg": "parlement", "rain": False, "transition": "iris",
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La conférence. Grand hall. Cent diplomates et juristes. Viktor Selg est à la tribune. Rasé de près. Sourire de façade. Et il me voit entrer."},

    {"id": "ch5_confront_ghost_2",
     "bg": "parlement", "rain": False,
     "char": "ghost", "expr": 3, "side": "right",
     "name": "VIKTOR SELG",
     "cg": "cg_19_fantôme",
     "text": "Détective Raven. Ça faisait longtemps que j'attendais cette rencontre. Vous avez fait un excellent travail sur l'Architecte. Vraiment."},

    {"id": "ch5_confront_ghost_3",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Viktor Selg. Connu aussi sous le nom de Fantôme. Je suis prêt à énumérer vos crimes devant cette assemblée si vous préférez les mondanités."},

    {"id": "ch5_confront_ghost_4",
     "bg": "parlement", "rain": False,
     "char": "ghost", "expr": 2, "side": "right",
     "name": "VIKTOR SELG",
     "text": "Vous avez un talent pour le dramatique. Bien. Mais vous n'avez pas de preuves exploitables contre moi. Juste un bras droit qui s'est volatilisé ce matin."},

    {"id": "ch5_confront_ghost_5",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 8, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Pas de preuves. Mais j'ai votre nom. Et dans dix minutes, Natasha Mori publiera votre photo avec le mot 'Fantôme' en titre de une internationale."},

    # ── Branche : Suivre le Fantôme ───────────────────────────────────────────
    {"id": "ch5_follow_ghost",
     "bg": "parlement", "rain": False, "transition": "iris",
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On observe. Viktor Selg pense contrôler la conférence. Qu'il continue de penser ça. Mira photographie ses contacts. Sato relève les immatriculations."},

    {"id": "ch5_follow_ghost_2",
     "bg": "parlement", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Selg rencontre sept personnes en aparté. Sourires. Poignées de main. Et à chaque fois, le même geste : il glisse quelque chose. Une carte. Un badge. Un objet."},

    {"id": "ch5_follow_ghost_3",
     "bg": "parlement", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "J'ai identifié trois des sept. Un commissaire européen. Un chef d'état-major de l'OTAN retraité. Et une directrice de fonds d'investissement souverain."},

    {"id": "ch5_follow_ghost_4",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ce n'est pas un réseau criminel. C'est un gouvernement parallèle. Fonctionnel. Opérationnel. Qui existe depuis trente ans en pleine lumière.",
     "evidence": ("Serveur miroir", "Accès validé — données Synarchie complètes depuis 1994")},

    {"id": "ch5_follow_ghost_5",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On tient son réseau. Maintenant on peut le couper. Branche par branche. Jusqu'à lui."},

    # ── ACTE 3 Ch5 : Le serveur miroir ────────────────────────────────────────
    {"bg": "sous_sol", "rain": False, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "",
     "text": "Le contact anonyme nous a donné une adresse. Un sous-sol à Wedding, quartier de Berlin. Derrière une blanchisserie fermée depuis huit ans."},

    {"bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Des serveurs. Des racks entiers. Des câbles qui partent dans toutes les directions. Et une interface qui tourne en continu depuis... 1994."},

    {"bg": "sous_sol", "rain": False,
     "char": "mira", "expr": 3, "side": "right",
     "name": "MIRA VOSS",
     "text": "C'est le serveur miroir. Il contient tout. Chaque décision de la Synarchie. Chaque transaction. Chaque ordre. Trente ans d'histoire criminelle."},

    {"bg": "sous_sol", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "L'Accord de Berlin. Il est là. Signé par six chefs d'État. Le pacte fondateur de tout ça. C'est une preuve judiciaire irréfutable.",
     "evidence": ("Témoin protégé", "Notre contact anonyme — ex-bras droit Selg, prêt à témoigner")},

    # ── Choix L ────────────────────────────────────────────────────────────────
    {"bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "On a le serveur. On a les preuves. Mais on est dans illégalité totale. Qu'est-ce qu'on fait de tout ça ?",
     "choices": ["Tout brûler — extraire les données et détruire le serveur", "Tout garder — le serveur intact est la preuve la plus solide"],
     "choice_branch": {"0": "ch5_burn", "1": "ch5_keep"}},

    # ── Branche : Détruire ─────────────────────────────────────────────────────
    {"id": "ch5_burn",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On extrait tout. Copies chiffrées sur quatre supports différents. Puis le serveur brûle. Rien ne doit rester qui puisse être utilisé contre nous."},

    {"id": "ch5_burn_2",
     "bg": "sous_sol", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Si ce serveur disparaît, Selg sait qu'on était là. Il va tout accélérer. On a peut-être 48 heures avant qu'il contre-attaque."},

    {"id": "ch5_burn_3",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "48 heures. C'est largement assez. J'ai attendu plus longtemps avec moins."},

    # ── Branche : Garder le serveur ───────────────────────────────────────────
    {"id": "ch5_keep",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On ne touche pas au serveur. Preuve physique. Indestructible. Introuvable pour eux s'ils ne savent pas qu'on l'a trouvé. On l'utilise comme levier."},

    {"id": "ch5_keep_2",
     "bg": "sous_sol", "rain": False,
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "Selg ne sait pas que le contact nous a amenés ici. Tant qu'il croit le serveur sécurisé, il continue de s'en servir. Et chaque utilisation nous donne de nouvelles données."},

    {"id": "ch5_keep_3",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 8, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un piège qui se referme sur lui-même. C'est la meilleure sorte."},

    # ── ÉPILOGUE CH5 ───────────────────────────────────────────────────────────
    {"bg": "hotel_berlin", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Cette nuit-là à Berlin, pour la première fois depuis six mois, j'ai l'impression qu'on n'est plus à courir après quelque chose. On l'a devant nous."},

    {"bg": "hotel_berlin", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Raven. Viktor Selg vient de quitter la conférence. Destination inconnue. Le Tribune a perdu sa trace il y a une heure."},

    {"bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il sait. Pas comment. Pas quoi exactement. Mais il a senti quelque chose changer. Les gens comme lui ont cet instinct. C'est ce qui les maintient en vie."},

    {"bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La chasse reprend. Mais cette fois, c'est lui qui court."},

    {"bg": "hotel_berlin", "rain": False,
     "char": None, "side": "left",
     "name": "", "text": "─── FIN DU CHAPITRE V ───"},

    {"chapter_end": 5, "bg": "hotel_berlin", "char": None, "side": "left", "name": "", "text": ""},

    # ══════════════════════════════════════════════════════════════════════════
    # ████  CHAPITRE VI — "Parlement"  ████
    # ══════════════════════════════════════════════════════════════════════════

    {"bg": "parlement", "rain": False, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "", "text": "CHAPITRE VI — Parlement"},

    {"bg": "parlement", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Strasbourg. Deux semaines après Berlin. Viktor Selg a réapparu. Ses avocats ont déposé une plainte contre Natasha Mori pour diffamation. Il attaque."},

    # ── ACTE 1 Ch6 : Les couloirs du parlement ─────────────────────────────────
    {"bg": "parlement", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Attaquer Natasha, c'est vouloir éteindre l'incendie avec un chalumeau. Ça brûle tout. Y compris lui. Selg panique."},

    {"bg": "parlement", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "Il a nommé un sénateur comme défenseur de sa cause. Le Sénateur Arnheim. Délégué à la sécurité transnationale. Et figure tutélaire de la commission que Selg consulte."},

    {"bg": "parlement", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le Sénateur Arnheim. J'ai lu son nom dans la liste de contacts de la clé USB #2. C'est lui, l'un des trois ministres."},

    {"bg": "parlement", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Arnheim est protégé par l'immunité parlementaire. On ne peut pas le toucher directement. Mais s'il commet une erreur publique... l'immunité ne couvre pas tout."},

    {"bg": "parlement", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Alors on va l'aider à commettre cette erreur."},

    {"bg": "parlement", "rain": False,
     "char": "natasha", "expr": 0, "side": "right",
     "name": "NATASHA MORI",
     "text": "Raven. J'ai reçu quelque chose ce matin. Un enregistrement audio. Anonyme. Une séance à huis clos de la commission Arnheim. Avec Selg."},

    {"bg": "parlement", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Notre contact à Berlin. Il a continué de travailler depuis l'intérieur. En silence. Bravo."},

    {"bg": "parlement", "rain": False,
     "char": "natasha", "expr": 3, "side": "right",
     "name": "NATASHA MORI",
     "text": "Arnheim et Selg discutent de la clé USB #2. Ils savent que vous l'avez. Ils savent pour Berlin. Et ils ont un plan pour vous neutraliser. Légalement.",
     "evidence": ("Enregistrement parlement", "Arnheim + Selg — plan de neutralisation de Raven")},

    {"bg": "parlement", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Légalement. Ils vont utiliser les institutions qu'ils contrôlent pour m'inculper. Fabrication de preuves. Espionnage non autorisé. C'est élégant."},

    {"bg": "parlement", "rain": False,
     "char": "detective", "expr": 8, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Et ça ne marchera pas. Parce que moi, je suis déjà en train de les filmer."},

    {"bg": "parlement", "rain": False,
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "J'ai reconstitué les flux financiers d'Arnheim. Dix-huit ans de transactions via un compte numéroté en Lettonie. La même banque que les comptes du registre offshore de Vane.",
     "evidence": ("Compte numéroté", "Banque lettone — même réseau que registre Vane Ch1")},

    # ── Choix M ────────────────────────────────────────────────────────────────
    {"bg": "parlement", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Arnheim. Un législateur. Immunité parlementaire. Des avocats. Selg dans l'ombre. Comment frapper ?",
     "choices": ["L'attaquer par le Sénat — demander une levée d'immunité officielle", "Passer par l'underground — détruire sa réputation sans passer par les institutions"],
     "choice_branch": {"0": "ch6_senate", "1": "ch6_underground"}},

    # ── Branche : Passer par le Sénat ─────────────────────────────────────────
    {"id": "ch6_senate",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On joue dans les règles. Pour une fois. Sato contacte le groupe d'opposants au Sénat. Ceux qui cherchent quelque chose contre Arnheim depuis des années."},

    {"id": "ch6_senate_2",
     "bg": "parlement", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "J'ai trois sénateurs qui attendent depuis des mois une demande formelle de levée d'immunité. Avec vos preuves, ils peuvent la déposer demain matin."},

    {"id": "ch6_senate_3",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Une demande officielle. Publiée. Impossible à enterrer discrètement. Arnheim sera obligé de répondre en public. Et chaque réponse sera un mensonge vérifiable."},

    {"id": "ch6_senate_4",
     "bg": "parlement", "rain": False,
     "char": "mira", "expr": 0, "side": "right",
     "name": "MIRA VOSS",
     "text": "Et Selg. Pendant qu'Arnheim s'agite en surface, Selg va essayer de tout faire disparaître en sous-main. C'est là qu'il se trahira.",
     "evidence": ("Identité du Sénateur", "Arnheim — lien confirmé Synarchie, compte Lettonie")},

    # ── Branche : Underground ──────────────────────────────────────────────────
    {"id": "ch6_underground",
     "bg": "rue", "rain": True, "transition": "slide_left",
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Les institutions sont compromises. Passer par elles, c'est donner à Arnheim le temps de se préparer. On va plus vite. On va plus fort."},

    {"id": "ch6_underground_2",
     "bg": "rue", "rain": True,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Je publie l'enregistrement du parlement. Brut. Sans filtre. En exclusivité mondiale. On ne lui laisse pas quarante-huit heures. On lui laisse quarante-huit secondes."},

    {"id": "ch6_underground_3",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Et en même temps, on fait fuiter les comptes lettons à trois autres rédactions. Simultané. Chaque journal pense avoir l'exclusivité. Personne ne peut étouffer la totalité."},

    {"id": "ch6_underground_4",
     "bg": "rue", "rain": True,
     "char": "mira", "expr": 3, "side": "right",
     "name": "MIRA VOSS",
     "text": "C'est dangereux. Si Arnheim tombe trop vite, Selg coupe les liens avec lui et disparaît. On risque de perdre la cible principale.",
     "evidence": ("Identité du Sénateur", "Arnheim — exposé publiquement, lien Selg non encore prouvé")},

    {"id": "ch6_underground_5",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Selg disparaît, ou Selg réagit. Dans les deux cas, il se trahit. Je préfère une erreur commise dans la panique à une erreur commise dans le calme."},

    # ── ACTE 2 Ch6 : La nuit avant la tempête ──────────────────────────────────
    {"bg": "parlement", "rain": False, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "",
     "text": "Nuit du mardi au mercredi. Les preuves sont prêtes. Les journaux attendent le signal. Tout le monde est en position."},

    {"bg": "parlement", "rain": False,
     "char": "mira", "expr": 3, "side": "right",
     "name": "MIRA VOSS",
     "text": "Raven. Je dois vous dire quelque chose. Les dix-huit mois dans mon dossier. La lacune dont Sato vous a parlé. J'étais en protection. Témoin protégé dans une affaire connexe."},

    {"bg": "parlement", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Une affaire connexe. Liée à la Synarchie."},

    {"bg": "parlement", "rain": False,
     "char": "mira", "expr": 4, "side": "right",
     "name": "MIRA VOSS",
     "text": "Mon directeur de cabinet. Celui qui m'a licenciée. Il travaillait pour Arnheim depuis douze ans. Ce n'est pas lui qui m'a poussée dehors. C'est Arnheim lui-même."},

    {"bg": "parlement", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Arnheim vous a chassée. Et vous continuez l'enquête sur lui depuis. Ce n'est plus juste du professionnalisme. C'est personnel."},

    {"bg": "parlement", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "Et alors ? Vous enquêtez sur la Synarchie depuis que vous avez vu Marcus Vane mort dans une ruelle. Vous pensez que ce n'est pas personnel pour vous non plus ?"},

    {"bg": "parlement", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "...Juste. C'est personnel pour tout le monde dans cette pièce. C'est peut-être pour ça qu'on est encore debout."},

    # ── Choix N ────────────────────────────────────────────────────────────────
    {"bg": "parlement", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Demain, tout explose. Comment aborder ce dernier acte ?",
     "choices": ["On agit en équipe — chacun a un rôle clair et précis", "Je prends les commandes seul — pour protéger les autres si ça dérape"],
     "choice_branch": {"0": "ch6_ally", "1": "ch6_alone"}},

    # ── Branche : En équipe ────────────────────────────────────────────────────
    {"id": "ch6_ally",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 2, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On se divise. Sato surveille Arnheim. Mira surveille les flux du compte letton en temps réel. Natasha publie par séquences. Moi, je vais chercher Selg."},

    {"id": "ch6_ally_2",
     "bg": "parlement", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Enfin un plan digne de ce nom. Compris. En position à 9h00."},

    {"id": "ch6_ally_3",
     "bg": "parlement", "rain": False,
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "Si le compte letton bouge dans les trois heures suivant la publication... on sait que quelqu'un a paniqué. Et ce quelqu'un nous donne Selg.",
     "evidence": ("Dossier fantôme vol 219", "Lien confirmé — commanditaire crash 219 : Viktor Selg")},

    # ── Branche : Seul ─────────────────────────────────────────────────────────
    {"id": "ch6_alone",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je préfère que les autres soient à l'abri. Sato reste à couvert avec les preuves. Natasha publie de sa rédaction, portes fermées. Mira... elle disparaît ce soir."},

    {"id": "ch6_alone_2",
     "bg": "parlement", "rain": False,
     "char": "mira", "expr": 3, "side": "right",
     "name": "MIRA VOSS",
     "text": "Non. Je ne disparais pas. Pas après tout ça. Raven, si vous essayez de jouer les martyrs solitaires, je publie tout moi-même sans attendre votre signal."},

    {"id": "ch6_alone_3",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "...Vous l'avez prévu. Ce scénario. Depuis le début. Vous n'êtes pas juste une analyste, Mira Voss."},

    {"id": "ch6_alone_4",
     "bg": "parlement", "rain": False,
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "Non. Je suis quelqu'un qui ne supporte pas de perdre. On fait ça ensemble. Ou on ne le fait pas.",
     "evidence": ("Dossier fantôme vol 219", "Lien Selg-crash 219 — Mira a la preuve finale")},

    # ── ACTE FINAL Ch6 : L'exposition ─────────────────────────────────────────
    {"bg": "parlement", "rain": False, "transition": "iris",
     "char": None, "side": "left",
     "name": "",
     "cg": "cg_20_parlement",
     "text": "9h07 du matin. Le Tribune publie. Le Monde publie. The Guardian publie. En quarante secondes, les réseaux s'embrasent."},

    {"bg": "parlement", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Arnheim est convoqué en urgence par le président du Sénat. Selg... sa ligne téléphonique ne répond plus. Il coupe. Il fuit."},

    {"bg": "parlement", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Le compte letton. Trois virements. Déclenchés en rafale. Dix millions. Direction : trois autres banques, trois pays différents. Il essaie de purger."},

    {"bg": "parlement", "rain": False,
     "char": "mira", "expr": 3, "side": "right",
     "name": "MIRA VOSS",
     "text": "Trop tard. J'ai bloqué les virements à la source. La banque lettone a reçu une injonction judiciaire il y a vingt minutes. Sato a fait le travail hier soir."},

    {"bg": "parlement", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Selg est acculé. Ses ressources financières gelées. Son nom sur tous les écrans. Et quelque part, ce soir, il va commettre l'erreur définitive."},

    # ── Choix O ────────────────────────────────────────────────────────────────
    {"bg": "parlement", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Selg fuit. On a une dernière chance de le coincer avant qu'il passe une frontière. Comment jouer ce dernier coup ?",
     "choices": ["L'exposer en direct — diffusion live de sa fuite", "Le laisser fuir vers son bunker — et le suivre jusqu'au bout"],
     "choice_branch": {"0": "ch6_expose_live", "1": "ch6_disappear"}},

    # ── Branche : Exposer en live ──────────────────────────────────────────────
    {"id": "ch6_expose_live",
     "bg": "rue", "rain": True, "transition": "slide_left",
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Natasha. On le suit. Et on diffuse. En direct. Sa fuite est sa condamnation publique. Il ne pourra plus jamais prétendre à l'innocence d'un homme qui ne court pas."},

    {"id": "ch6_expose_live_2",
     "bg": "rue", "rain": True,
     "char": "natasha", "expr": 0, "side": "right",
     "name": "NATASHA MORI",
     "text": "Live. D'accord. Mais Raven... si on l'acule trop vite, il peut devenir dangereux. Un animal blessé..."},

    {"id": "ch6_expose_live_3",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Est déjà dangereux. La différence, c'est qu'un animal acculé ne peut plus planifier. Il réagit. Et les réactions, ça se lit."},

    # ── Branche : Suivre jusqu'au bunker ──────────────────────────────────────
    {"id": "ch6_disappear",
     "bg": "rue", "rain": True, "transition": "slide_left",
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On le laisse croire qu'il s'échappe. On pose un traceur sur son véhicule. Et on le suit à distance. Là où il va se réfugier, c'est là que se trouve le cœur du réseau."},

    {"id": "ch6_disappear_2",
     "bg": "rue", "rain": True,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "J'ai une hypothèse sur l'emplacement. Une propriété enregistrée au nom d'une fondation au Liechtenstein. Montagnes autrichiennes. Si c'est là qu'il va..."},

    {"id": "ch6_disappear_3",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Alors on finit cette histoire là où elle devrait finir. À l'endroit exact où lui pense être à l'abri.",
     "evidence": ("Coordonnées bunker", "Propriété Liechtenstein — dernier refuge de Selg")},

    # ── ÉPILOGUE CH6 ───────────────────────────────────────────────────────────
    {"bg": "toit", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Arnheim est en garde à vue. Demande de levée d'immunité en cours. Pour la première fois depuis trente ans, la Synarchie perd un pilier en pleine lumière."},

    {"bg": "toit", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Interpol a émis un mandat contre Selg. Dix-sept pays. Mais s'il atteint le Liechtenstein, ça prend du temps."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On n'aura pas besoin d'Interpol. On était là avant eux. On sera là en premier."},

    {"bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "", "text": "─── FIN DU CHAPITRE VI ───"},

    {"chapter_end": 6, "bg": "toit", "char": None, "side": "left", "name": "", "text": ""},

    # ══════════════════════════════════════════════════════════════════════════
    # ████  CHAPITRE VII — "La Décision"  ████
    # ══════════════════════════════════════════════════════════════════════════

    {"bg": "sous_sol", "rain": False, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "", "text": "CHAPITRE VII — La Décision"},

    {"bg": "sous_sol", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Alpes autrichiennes. 2200 mètres d'altitude. Une propriété qui n'existe officiellement que dans les registres d'une fondation fantôme."},

    # ── ACTE 1 Ch7 : Le bunker ─────────────────────────────────────────────────
    {"bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_21_bunker",
     "text": "Un bunker. Construit dans les années 80. Modernisé depuis. Selg a des serveurs ici. Des réserves. Une vie entière de secours."},

    {"bg": "sous_sol", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "Il n'est pas seul. Il y a trois personnes avec lui. Gardes du corps. Pas de communication sortante depuis vingt-quatre heures. Il se terre."},

    {"bg": "sous_sol", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. On a quelque chose. En fouillant les données du serveur de Berlin. Un document. Signé. Par Selg. Et par l'Architecte. Il y a dix ans."},

    {"bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Montre-moi."},

    {"bg": "sous_sol", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "C'est un testament. Le vrai. Marcus Vane l'a rédigé il y a dix ans. Il savait. Il savait depuis le début qu'il finirait dans une ruelle. Et il a tout documenté.",
     "evidence": ("Testament de Vane", "Vane savait — documentation complète depuis 10 ans")},

    {"bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vane. Il tenait deux jeux de comptes. Un pour la Synarchie. Un pour moi. Pour quelqu'un comme moi. Il a attendu que quelqu'un arrive."},

    {"bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je comprends maintenant pourquoi la clé USB était dans sa poche. Ce n'était pas un accident. C'était sa façon de demander à l'avance."},

    {"bg": "sous_sol", "rain": False,
     "char": "mira", "expr": 0, "side": "right",
     "name": "MIRA VOSS",
     "text": "Et dans ce testament, Raven. Une adresse. Un compte bancaire. Et un nom. Le vrai nom de l'Architecte. Le vrai. Pas le passeport fantôme de Genève.",
     "evidence": ("Preuve ultime", "Vrai nom Architecte + organigramme complet Synarchie depuis 1994")},

    {"bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "L'Architecte est en vie. Il n'a pas fui à Genève. Il a disparu dans sa propre légende. Et Selg est son bras opérationnel depuis le début."},

    # ── Choix P ────────────────────────────────────────────────────────────────
    {"bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Sato est avec nous. Elle a risqué sa carrière, sa vie. Ce qu'on va faire ensuite peut la brûler. Comment la protéger ?",
     "choices": ["L'intégrer pleinement — elle mérite d'être là jusqu'à la fin", "La tenir à l'écart du dernier acte — au cas où ça tourne mal"],
     "choice_branch": {"0": "ch7_trust_sato", "1": "ch7_protect_sato"}},

    # ── Branche : Intégrer Sato ────────────────────────────────────────────────
    {"id": "ch7_trust_sato",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Sato. Vous êtes dans ce dossier depuis le premier cadavre. Vous avez droit à la fin. On entre ensemble."},

    {"id": "ch7_trust_sato_2",
     "bg": "sous_sol", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "C'est ce que j'attendais d'entendre. En position."},

    # ── Branche : Protéger Sato ────────────────────────────────────────────────
    {"id": "ch7_protect_sato",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Sato. Ce qui vient est hors cadre légal. Je ne peux pas vous y emmener. Restez ici. Avec les preuves. Si je ne ressors pas, vous publiez tout."},

    {"id": "ch7_protect_sato_2",
     "bg": "sous_sol", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Vous faites ça encore. Décider seul pour me protéger. Un jour, Raven, vous allez réaliser que les gens peuvent choisir leurs propres risques."},

    {"id": "ch7_protect_sato_3",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ce jour n'est pas aujourd'hui. Restez."},

    # ── ACTE 2 Ch7 : La confrontation finale ──────────────────────────────────
    {"bg": "sous_sol", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Le bunker. Couloirs de béton. Lumières de secours. Quelqu'un nous attendait."},

    {"bg": "sous_sol", "rain": False,
     "char": "ghost", "expr": 1, "side": "right",
     "name": "VIKTOR SELG",
     "text": "Détective Raven. Je vous attendais. Entrez. Il n'y a plus aucune raison de se cacher, maintenant."},

    {"bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous fuyez tout le monde depuis une semaine. Et vous m'attendez dans un bunker en souriant. Qu'est-ce qui a changé ?"},

    {"bg": "sous_sol", "rain": False,
     "char": "ghost", "expr": 0, "side": "right",
     "name": "VIKTOR SELG",
     "text": "Ce qui a changé. Regardez derrière vous."},

    {"bg": "sous_sol", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Trois hommes. Et avec eux, une silhouette que je n'avais pas vue depuis Genève."},

    {"bg": "sous_sol", "rain": False,
     "char": "architect", "expr": 0, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Raven. Vous avez fait un travail remarquable. Vraiment. Vous avez nettoyé pour moi ce que je ne pouvais pas nettoyer moi-même."},

    {"bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "L'Architecte. Vous êtes ici. Vous n'avez jamais fui."},

    {"bg": "sous_sol", "rain": False,
     "char": "architect", "expr": 1, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Non. Genève était un sacrifice calculé. Ferrière, Selg, Arnheim. Des couches. Des pare-feux humains. Et vous, l'outil parfait pour les éliminer proprement à ma place."},

    {"bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Encore. Vous m'avez encore utilisé. Depuis le début. Depuis Vane."},

    {"bg": "sous_sol", "rain": False,
     "char": "architect", "expr": 2, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Vane voulait vous contacter. C'est moi qui ai accéléré sa mort. Pour que vous ayez une raison d'enquêter. Pour que vous nettoiez ce que je ne pouvais pas nettoyer."},

    {"bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Marcus Vane. Il est mort à cause de moi. Parce que vous saviez que je viendrais. Parce que vous m'avez choisi."},

    {"bg": "sous_sol", "rain": False,
     "char": "architect", "expr": 0, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Parce que vous êtes l'un des rares êtres dans cette ville incorruptibles. Vous ne pouvez pas être acheté. Mais vous pouvez être dirigé. C'est plus efficace."},

    {"bg": "sous_sol", "rain": False,
     "char": "mira", "expr": 3, "side": "right",
     "name": "MIRA VOSS",
     "text": "Raven. J'ai Sato en ligne. Elle nous entend. Et elle est en train d'envoyer notre position à Interpol. Depuis cinq minutes."},

    {"bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Bien. Alors il nous reste cinq minutes pour finir cette conversation correctement."},

    # ── Choix Q ────────────────────────────────────────────════════════════════
    {"bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "L'Architecte. Devant moi. Pour la première fois, sans porte de sortie. Comment terminer ça ?",
     "choices": ["Proposer un accord — sa coopération contre l'impunité partielle", "Refuser tout accord — il répond de tout, sans exception"],
     "choice_branch": {"0": "ch7_architect_deal", "1": "ch7_architect_end"}},

    # ── Branche : Accord avec l'Architecte ────────────────────────────────────
    {"id": "ch7_architect_deal",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il y a encore des noms que je n'ai pas. Des connexions que je ne vois pas. Vous me donnez tout. Chaque nom. Chaque accord. Et j'intercède pour que votre procès soit en Europe, pas extradé."},

    {"id": "ch7_architect_deal_2",
     "bg": "sous_sol", "rain": False,
     "char": "architect", "expr": 3, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Vous venez me proposer un marché. Dans mon propre bunker. Avec Interpol qui arrive. C'est vous ou la prison dans un pays que je ne contrôle pas. Clairement, vous."},

    {"id": "ch7_architect_deal_3",
     "bg": "sous_sol", "rain": False,
     "char": "architect", "expr": 1, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Très bien. Je vais vous donner quelque chose. Pas par peur. Par respect. Voici les sept noms que vous n'avez pas. Les sept qui resteront quand je serai jugé.",
     "evidence": ("Coordonnées bunker", "Architecte localisé — Interpol en route, accord partiel")},

    {"id": "ch7_architect_deal_4",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Sept noms. Les plus haut placés. Deux chefs d'État en exercice. Trois directeurs de banque centrale. Et deux juges de la Cour internationale. Je n'avais pas rêvé si haut."},

    # ── Branche : Pas d'accord ─────────────────────────────────────────────────
    {"id": "ch7_architect_end",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Non. Aucun accord. Vous répondez de Marcus Vane. Des 147 morts du vol 219. De chaque vie achetée, vendue, ou effacée depuis 1994. Sans exception."},

    {"id": "ch7_architect_end_2",
     "bg": "sous_sol", "rain": False,
     "char": "architect", "expr": 3, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Vous comprenez que si vous ne faites pas d'accord, les sept noms disparaissent avec moi. Ils seront introuvables pendant vingt ans. Vous avez pesé ce prix ?"},

    {"id": "ch7_architect_end_3",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Oui. Et j'ai décidé que Marcus Vane vaut plus que vingt ans de confort pour les sept noms que vous protégez."},

    {"id": "ch7_architect_end_4",
     "bg": "sous_sol", "rain": False,
     "char": "architect", "expr": 0, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "...C'est la première fois en trente ans que quelqu'un choisit l'honnêteté sur l'efficacité. Je ne sais pas si je dois vous admirer ou vous plaindre.",
     "evidence": ("Preuve ultime", "Architecte remis à Interpol — aucun accord — jugement complet")},

    {"id": "ch7_architect_end_5",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Les deux. Ça m'est arrivé souvent."},

    # ── ACTE FINAL Ch7 : L'épilogue ────────────────────────────────────────────
    {"bg": "sous_sol", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Interpol. Six unités. L'Architecte, Selg, les trois gardes. Tous. En trente secondes."},

    {"bg": "toit", "rain": False, "transition": "fade_white",
     "char": None, "side": "left",
     "name": "",
     "text": "Trois mois plus tard."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le procès commence en septembre. À La Haye. Dix-neuf inculpés. L'Architecte, Selg, Arnheim, et seize autres dont les noms remplissent les journaux du monde entier."},

    {"bg": "toit", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Medaille d'honneur Interpol. Offre de poste à Bruxelles. Et mon chef de brigade est en train d'expliquer à tout le monde qu'il m'a toujours soutenue."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Les chefs de brigade ont une mémoire très sélective. C'est professionnel."},

    {"bg": "toit", "rain": False,
     "char": "natasha", "expr": 2, "side": "right",
     "name": "NATASHA MORI",
     "text": "Prix Albert Londres. Annoncé ce matin. Pour la série complète. Du Vol 219 au bunker. Ils appellent ça 'le plus grand reportage du siècle'. Je préfère l'appeler 'pas encore fini'."},

    {"bg": "toit", "rain": False,
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "Et moi. Réintégrée. Avec rétroaction sur les dix-huit mois. Et une promotion que j'ai refusée. Je préfère rester sur le terrain. Vous avez de la place dans votre équipe ?"},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je travaille seul, Mira. Vous le savez."},

    {"bg": "toit", "rain": False,
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "C'est ce que vous dites. C'est ce que vous avez dit à Sato aussi. Regardez où vous en êtes."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Cette ville. Les toits, toujours. Ça ressemble à quoi, une ville propre ? Je ne saurais pas répondre. Je n'en ai jamais vu une."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mais je sais à quoi ressemble une ville moins sale. Et ce soir, depuis ce toit, elle ressemble à ça. Lumières et pluie. Comme la première fois."},

    # ── CHOIX FINAL R ──────────────────────────────────────────────────────────
    {"bg": "toit", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Un nouveau dossier vient d'arriver sur mon bureau. Une banque. Des comptes suspects. Un nom que personne ne reconnaît. Le début de quelque chose.",
     "choices": ["Reprendre — la lumière a besoin de quelqu'un", "Disparaître — et vivre enfin"],
     "choice_branch": {"0": "ch7_light", "1": "ch7_shadow"}},

    # ── Fin Lumière ────────────────────────────────────────────────────────────
    {"id": "ch7_light",
     "bg": "toit", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_22_fin_lumière",
     "text": "Je prends le dossier. Je l'ouvre. Et je commence à lire. Parce que quelqu'un doit le faire. Parce que personne d'autre ne le fera. Et parce que Marcus Vane mérite qu'on continue."},

    {"id": "ch7_light_2",
     "bg": "toit", "rain": True,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Je vois que vous avez ouvert le dossier. Je me demandais combien de temps vous tiendriez."},

    {"id": "ch7_light_3",
     "bg": "toit", "rain": True,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Douze secondes. C'est un record personnel."},

    {"id": "ch7_light_4",
     "bg": "toit", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Quelque part dans cette ville — dans toutes les villes — la lumière a besoin de quelqu'un pour la maintenir allumée. C'est un mauvais travail, mal payé, dangereux et solitaire."},

    {"id": "ch7_light_5",
     "bg": "toit", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Parfait."},

    # ── Fin Ombre ──────────────────────────────────────────────────────────────
    {"id": "ch7_shadow",
     "bg": "rue", "rain": True, "transition": "slide_left",
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_23_fin_ombre",
     "text": "Je laisse le dossier sur le bureau. Je ferme la porte à clé. Et pour la première fois depuis Vane, je descends dans la rue sans regarder par-dessus mon épaule."},

    {"id": "ch7_shadow_2",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je ne sais pas ce que ça fait, vivre. Vraiment vivre. Mais je vais apprendre. Comme on apprend tout. En commençant par le commencement."},

    {"id": "ch7_shadow_3",
     "bg": "rue", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Quelque part dans cette ville, il y a des gens qui ne savent pas que quelqu'un vient de les sauver. C'est la définition d'un travail bien fait."},

    {"id": "ch7_shadow_4",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Et peut-être que c'est assez. Pour ce soir."},

    # ── FIN ABSOLUE ────────────────────────────────────────────────────────────
    {"bg": "toit", "rain": False, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "",
     "text": "─── FIN DE NUIT SANS TÉMOIN ───\n\nMerci à Marcus Vane.\nEt à tous ceux qui n'ont pas abandonné."},

    {"chapter_end": 7, "bg": "toit", "char": None, "side": "left", "name": "", "text": ""}
]

EXAMPLE_SCRIPT_NODES = [
    {
        "id": "sc_01",
        "bg": "bureau_nuit",
        "char": "vane",
        "text": "Ce dossier ne tient pas debout.",
        # Pas de clé "transition" → FadeBlack par défaut (0.7 s)
    },
    {
        "id": "sc_02",
        "bg": "rue_pluie",
        "char": "vane",
        "text": "Dehors, la pluie efface les empreintes.",
        "transition": "slide_left",     # Déplacement spatial
    },
    {
        "id": "sc_03",
        "bg": "metro",
        "char": "narrateur",
        "text": "Trois heures plus tard…",
        "transition": "fade_black",     # Ellipse temporelle
    },
    {
        "id": "sc_04",
        "bg": "flashback_enfance",
        "char": "vane",
        "text": "Je me souviens de ce matin-là.",
        "transition": "fade_white",     # Flashback
    },
    {
        "id": "sc_05",
        "bg": "salle_interrogatoire",
        "char": "commissaire",
        "text": "Asseyez-vous, inspecteur.",
        "transition": "iris",           # Scène dramatique
    },
]
