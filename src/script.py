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

# ═══════════════════════════════════════════════════════════════════════════════
# NUIT SANS TÉMOIN — script.py v2.0 — Édition Complète
# ═══════════════════════════════════════════════════════════════════════════════
#
# LORE OFFICIEL
# ─────────────────────────────────────────────────────────────────────────────
# LA SYNARCHIE :
#   Fondée en 1947 dans les décombres de l'Europe d'après-guerre, la Synarchie
#   est née de l'obsession d'une poignée d'idéologues qui refusaient l'idée
#   que le IIIe Reich avait échoué sur le fond. Pour eux, l'échec était
#   tactique, pas idéologique. L'Europe fragmentée était une plaie ; une Europe
#   unifiée sous une seule main — la bonne — serait la réparation.
#
#   Leur plan, qu'ils appellent en interne "Viertes Reich" (le Quatrième),
#   est simple dans sa brutalité :
#     1. Infiltrer les institutions européennes (Parlement, Commission, Interpol)
#     2. Faire voter une réforme constitutionnelle fondant les États membres
#        en une seule entité souveraine — les "États-Unis d'Europe"
#     3. Placer un de leurs membres à la tête de cet État
#     4. Éliminer méthodiquement tout détracteur, journaliste, juge ou
#        politicien susceptible de bloquer le processus
#
#   La Synarchie ne se présente pas comme néo-nazie. Elle se présente comme
#   un cercle de "réformateurs européens" pro-fédéralistes. Ses membres
#   publics sont respectables, philanthropes, diplômés. Les archives de ses
#   fondateurs, enfouies dans des bunkers suisses, raconteraient une autre
#   histoire.
#
#   Elle finance ses opérations via un réseau bancaire off-shore (Lettonie,
#   Luxembourg, Chypre) qui existe depuis 1952. Marcus Vane en était le
#   comptable secondaire pour l'Europe de l'Ouest.
#
# ─────────────────────────────────────────────────────────────────────────────
# PERSONNAGES — LORE COMPLET
# ─────────────────────────────────────────────────────────────────────────────
#
# RAVEN (prénom : Élie, il ne s'en sert jamais) :
#   38 ans. Né à Strasbourg, d'un père alsacien et d'une mère d'origine
#   japonaise. A grandi entre deux langues, deux cultures, deux versions de
#   l'histoire européenne. Son père, professeur d'histoire, était obsédé par
#   la montée des fascismes — il lui a légué cette obsession comme un héritage.
#   Mort dans un accident de voiture à Raven avait 17 ans. Accident qui
#   n'en était peut-être pas un : son père travaillait sur un article liant
#   des fonds de reconstruction d'après-guerre à des réseaux d'extrême droite.
#   Raven ne l'a jamais prouvé. Il n'a jamais arrêté d'y penser.
#   Devenu flic par idéalisme, inspecteur par acharnement, privé parce qu'il
#   ne supportait plus la hiérarchie. Il doit six mois de loyer. Il dort
#   trop peu et boit trop de café. Il n'a pas eu de relation stable depuis
#   trois ans. Il fait ce travail parce qu'il ne sait pas faire autre chose,
#   et parce que quelque part il espère encore que la vérité sert à quelque chose.
#
# OFF. LEILA SATO :
#   33 ans. Née à Lyon, parents franco-japonais. Elle et Raven se connaissent
#   depuis l'académie de police — elle a terminé 1ère de promo, lui 3ème.
#   Elle est restée dans la police là où il est parti. Elle croit aux
#   institutions parce qu'elle sait ce qu'il en coûte de les laisser pourrir.
#   Elle couvre Raven plus souvent qu'à son tour, pas par faiblesse mais par
#   calcul : il voit des choses qu'elle ne voit pas, elle a l'autorité qu'il
#   n'a plus. Leur relation est une collaboration intense, jamais romantique,
#   parfois orageuse. Elle a une fille de 5 ans dont elle ne parle jamais
#   au travail.
#
# MARCUS VANE (mort avant le début du jeu) :
#   42 ans. Comptable discret, né à Bordeaux, installé à Paris depuis 20 ans.
#   Il tenait les livres de compte de la Synarchie pour l'Europe de l'Ouest
#   depuis 12 ans. Ce qu'on ne sait pas jusqu'au chapitre VII : il documentait
#   tout en parallèle. Pas par héroïsme — par peur. Il savait qu'un jour ils
#   l'élimineraient. Il voulait une assurance-vie. Il est mort avant de pouvoir
#   s'en servir, mais il avait tout prévu pour que quelqu'un d'autre le fasse.
#
# FERRIÈRE (Capitaine Luc Ferrière) :
#   51 ans. Capitaine de la Brigade Criminelle, Paris. Membre de la Synarchie
#   depuis 18 ans. C'est lui qui a coordonné l'élimination de Vane.
#   Pas un idéologue — un opportuniste. Il croit à l'ordre, à la hiérarchie,
#   à l'argent. La Synarchie lui donne les trois. Il justifie tout avec
#   le même mot : "nécessité".
#
# NATASHA MORI :
#   36 ans. Journaliste d'investigation, correspondante pour un réseau de
#   presse européen indépendant. Née à Osaka, installée à Paris depuis 8 ans.
#   Elle enquêtait sur les réseaux d'influence dans les institutions
#   européennes quand les dossiers de Vane ont croisé son radar. Elle n'est
#   ni une alliée facile ni une ennemie — elle a ses propres objectifs,
#   qui convergent avec ceux de Raven sans être identiques. Elle veut
#   publier. Il veut condamner. La tension entre ces deux buts structure
#   une grande partie de leurs échanges.
#
# TARO MITSUKI :
#   44 ans. Informateur de longue date, mi-flic mi-criminel. Né à Marseille,
#   d'une famille de la diaspora japonaise. Il a travaillé pour cinq
#   organisations criminelles différentes et pour la police deux fois plus.
#   Il connaît Raven depuis dix ans. Il l'aime bien et en a peur. Il sait
#   toujours plus qu'il ne dit.
#
# L'ARCHITECTE (Dr. Heinrich Voss, connu publiquement comme philanthrope) :
#   68 ans. Né à Vienne en 1958. Docteur en sciences politiques, ex-conseiller
#   de trois présidents de la Commission Européenne. En public : fondateur
#   de l'Institut Voss pour la Coopération Européenne, donateur d'universités,
#   figure du dialogue interculturel. En privé : chef opérationnel de la
#   Synarchie depuis 1991. Il croit sincèrement au projet. Il n'est pas
#   cynique — il est convaincu. C'est ce qui le rend dangereux.
#
# VIKTOR SELG (dit "Le Fantôme") :
#   55 ans. Né à Leipzig, ex-officier de la Stasi reconverti dans le
#   "conseil en sécurité". Il est le bras armé de l'Architecte, son numéro
#   deux opérationnel depuis 1994 (l'Accord de Berlin). Il n'existe sur
#   aucun registre officiel sous ce nom. Il a six identités différentes.
#
# MIRA VOSS :
#   34 ans. Nièce de Heinrich Voss — elle ne l'a appris qu'à 28 ans, quand
#   il l'a recrutée. Ex-analyste de la DGSI, licenciée dans des circonstances
#   floues. Elle travaille nominalement comme consultante en cybersécurité.
#   En réalité elle a passé quatre ans à collecter des preuves contre son
#   oncle. Elle attend le bon moment. Raven et elle se croisent au chapitre IV.
#
# ARNHEIM (Sénateur Klaus Arnheim) :
#   71 ans. Sénateur européen, Allemagne. Façade démocrate-chrétienne,
#   membre de la Synarchie depuis 1988. C'est lui qui pilote les réformes
#   institutionnelles de l'intérieur du Parlement.
#
# ─────────────────────────────────────────────────────────────────────────────
# STRUCTURE DU SCRIPT COMPLET
# ─────────────────────────────────────────────────────────────────────────────
#   Chapitre I    — La Nuit sans Témoin (étendu)
#   Chapitre II   — Le Prix de la Vérité (étendu)
#   Chapitre III  — L'Architecte (étendu)
#   [NOUVEAU] Ch. III-B — Terrain (enquête de terrain, témoins, lore)
#   [NOUVEAU] Ch. III-C — Mémoire (flashbacks Raven, repos, ancrage)
#   Chapitre IV   — L'Héritage (étendu)
#   Chapitre V    — Le Fantôme (étendu)
#   Chapitre VI   — Parlement (étendu)
#   Chapitre VII  — La Décision (étendu)
# ═══════════════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════
# Chapitre I — La Nuit sans Témoin
# ══════════════════════════════════════════════════════════════════════
SCRIPT_I = [
    # ══════════════════════════════════════════════════════════════════════════
    # ████  CHAPITRE I — "La Nuit sans Témoin"  ████
    # ══════════════════════════════════════════════════════════════════════════

    # ── ACTE 0 : Prologue — La mémoire de Raven ────────────────────────────────
    {"bg": "bureau", "rain": False,
     "char": None, "side": "left",
     "name": "", "text": "Mon père disait que l'Europe avait été bâtie sur des ruines. Il avait raison. Ce qu'il ne disait pas, c'est que certains avaient gardé les plans."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je m'appelle Élie Raven. Je n'utilise jamais mon prénom. Trop doux pour ce métier."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Privé depuis quatre ans. Avant : Brigade Criminelle, Paris. Avant encore : l'académie, les espoirs, la certitude que la vérité servait à quelque chose."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mon père est mort dans un accident de voiture quand j'avais dix-sept ans. Il travaillait sur un article. Des fonds d'après-guerre. Des réseaux qui n'auraient pas dû exister."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "L'enquête a conclu à un accident. J'ai seize ans de police derrière moi et je sais ce qu'est un accident. Ce que j'ai vu dans ce dossier n'en était pas un."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mais ce soir, ce n'est pas ça qui m'occupe. Ce soir, mon téléphone sonne. Et une voix que je connais depuis dix ans me dit qu'il y a un mort à Chinatown."},

    # ── ACTE 1 : La scène de crime ─────────────────────────────────────────────
    {"bg": "scene_de_crime", "rain": True, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "", "text": "2h37 du matin. La pluie n'a pas cessé depuis trois jours."},

    {"bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_01_ruelle",
     "text": "Encore une nuit blanche. Encore un mort que personne ne réclame."},

    {"bg": "scene_de_crime", "rain": True,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. Vous avez mis le temps. La victime : Marcus Vane, 42 ans, comptable. Aucun antécédent officiel."},

    {"bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un comptable dans une ruelle de Chinatown. Ça sent le règlement de comptes.",
     "evidence": ("Dossier Vane", "Victime : M.Vane, 42 ans, comptable, aucun casier")},

    {"bg": "scene_de_crime", "rain": True,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Deux impacts. Arme de gros calibre, professionnelle. Pas d'arme sur place, pas de douilles. Quelqu'un a nettoyé."},

    {"bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Pas un crime de rue. Un crime organisé avec des moyens institutionnels. Le nettoyage prend du temps, ça suppose une coordination."},

    {"bg": "scene_de_crime", "rain": True,
     "char": "policiere", "expr": 0, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Pas d'arme sur place. Mais on a trouvé ça dans sa poche intérieure, cousue sous la doublure..."},

    {"bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_02_cle_usb",
     "text": "Une clé USB. Cryptée. Il avait pris la peine de la cacher. Il savait qu'on chercherait.",
     "evidence": ("Clé USB", "Données cryptées — dissimulée dans la doublure de veste")},

    {"bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il avait peur. Et il avait planifié. Deux choses qui ne vont pas souvent ensemble chez les victimes ordinaires."},

    {"bg": "scene_de_crime", "rain": True,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "La RC arrive dans vingt minutes. Si Ferrière prend l'affaire, cette clé disparaît."},

    {"bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ferrière. Son nom dans ce contexte... intéressant. Vous avez une raison de le mentionner ?"},

    {"bg": "scene_de_crime", "rain": True,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Une intuition. Rien de plus. Faites vite."},

    # CHOIX 1 ──────────────────────────────────────────────────────────────────
    {"bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Vingt minutes. Que faire en priorité ?",
     "choices": ["Interroger les témoins de la rue", "Examiner la scène centimètre par centimètre"],
     "choice_branch": {"0": "interro_ext_01", "1": "scene_ext_01"}},

    # Branche : examiner la scène ──────────────────────────────────────────────
    {"id": "scene",
     "bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je scrute chaque centimètre. Des traces de pneus dans la ruelle adjacente. Pneus larges, pas des pneumatiques civils."},

    {"bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ces empattements correspondent à des véhicules de service. Fourgonnettes de surveillance ou voitures banalisées de la RC.",
     "evidence": ("Trace de pneus", "Véhicule lourd — pneus service, empattement institutionnel")},

    {"bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vane a été conduit ici. Pas tué ici. Les éclaboussures sont trop propres, trop concentrées. C'est une mise en scène."},

    {"bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un meurtre commis ailleurs, un corps déposé ici. Quelqu'un qui connaissait les rotations de patrouille de ce quartier. Un initié."},

    # Branche : interroger ─────────────────────────────────────────────────────
    {"id": "interrogation",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un homme dans l'ombre d'un porche. La soixantaine, vêtements mouillés, le regard d'un homme qui a vu quelque chose et qui le regrette."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ne fuis pas. J'ai juste quelques questions. Tu seras rentré avant l'aube."},

    {"bg": "rue", "rain": True,
     "char": None, "side": "left",
     "name": "VIEILLARD",
     "text": "J'ai rien vu. Rien du tout. C'est ce que je dirai aux flics aussi."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Tu as tout vu. La façon dont tu regardes par-dessus mon épaule me le dit. Ils sont partis depuis vingt minutes."},

    {"bg": "rue", "rain": True,
     "char": None, "side": "left",
     "name": "VIEILLARD",
     "text": "... Une voiture noire. Deux hommes. Ils ont sorti le corps du coffre. Vite et précis. Comme des militaires."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La plaque ?",
     "evidence": ("Témoignage rue", "Corps sorti d'un coffre — deux hommes, professionnels, voiture noire")},

    {"bg": "rue", "rain": True,
     "char": None, "side": "left",
     "name": "VIEILLARD",
     "text": "Partiellement effacée. Mais j'ai eu le temps de voir les deux premières lettres. FP. Et l'autocollant Ile-de-France."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "FP. Flics ou fonctionnaires. Dans les deux cas... merde.",
     "evidence": ("Trace de pneus", "Plaque partielle : FP — Ile-de-France, véhicule institutionnel")},

    # Convergence des deux branches ─────────────────────────────────────────────
    {"bg": "salle_interrogatoire", "rain": False, "transition": "fade_black",
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "On a un second témoin. Taro Mitsuki. Il était dans le quartier cette nuit-là. Il refuse de parler, mais il a vu quelque chose."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Taro. Ça fait deux ans. Il est encore dans le coin ?"},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "policiere", "expr": 0, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Il est toujours 'dans le coin'. C'est son état naturel. Vous le connaissez ?"},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On a une longue et inconfortable histoire. Je vais lui parler."},

    # ── Mini-jeu interrogatoire : Taro Mitsuki ─────────────────────────────────
    {"id": "interro_minigame_taro",
     "type": "interrogation",
     "suspect": "taro",
     "time_limit": 90,
     "on_success": "interro_taro_ok",
     "on_failure": "interro_taro_fail"},

    # Résultat succès ───────────────────────────────────────────────────────────
    {"id": "interro_taro_ok",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "evidence": ("Enregistrement Taro", "Aveu : rendez-vous de Vane avec un homme de la Synarchie"),
     "text": "Il a craqué. Vane avait rendez-vous cette nuit-là. Un homme avec un badge. Une liste de noms. Une liste qui ne devait jamais être retrouvée."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "taro", "expr": 2, "side": "right",
     "name": "TARO MITSUKI",
     "text": "Ces gens-là, Raven... ils ne jouent pas. J'ai vu ce qu'ils font à ceux qui parlent. Vous vous souvenez de l'affaire Henric, en 2019 ?"},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Henric. Le journaliste. Classé suicide. Vous me dites que ce n'en était pas un."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "taro", "expr": 1, "side": "right",
     "name": "TARO MITSUKI",
     "text": "Je vous dis de faire attention à votre café le matin. Et à vos sorties nocturnes. C'est tout ce que je vous dis."},

    # Résultat échec ────────────────────────────────────────────────────────────
    {"id": "interro_taro_fail",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "taro", "expr": 1, "side": "right",
     "name": "TARO MITSUKI",
     "text": "J'ai rien vu, j'ai rien entendu, j'étais nulle part. C'est ma version et elle ne changera pas."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Rien. Il tient bon. Mais cette peur dans ses yeux — elle est réelle. Il sait, et quelqu'un le tient."},

    # ── ACTE 2 : La rue, la nuit ─────────────────────────────────────────────────
    {"bg": "rue", "rain": True, "transition": "fade_black",
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je retourne dans la rue. La pluie efface les traces, mais pas les mensonges."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vane avait peur. Il avait caché la clé. Il avait des rendez-vous secrets. Un comptable ordinaire ne prend pas ces précautions."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il comptait l'argent de quelqu'un d'autre. Et cet argent était sale. Assez sale pour en mourir."},

    # ── ACTE 3 : Le bureau — décryptage ────────────────────────────────────────
    {"bg": "bureau", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_03_bureau_nuit",
     "text": "3h du matin. La clé USB tourne. J'ai des logiciels que je n'ai pas le droit d'avoir. C'est pratique."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Premier fichier décrypté. Des noms. Des montants. Des pays. Luxembourg, Lettonie, Chypre. Le circuit classique du blanchiment institutionnel."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vane ne comptait pas des feuilles de paie. Il comptait les flux financiers d'une organisation dont je reconnais le nom dans les trois derniers fichiers.",
     "evidence": ("Fichiers Synarchie", "Registre financier — flux offshore, 47 noms codés")},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La Synarchie. J'ai ce nom une seule autre fois dans ma vie. Dans les notes de mon père. 1994. Il les avait classées 'danger'."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il avait raison."},

    {"bg": "bureau", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. Il est 4h du matin. J'ai reçu un message de Ferrière. Il veut vous voir demain. Il dit que vous avez pris des preuves sur sa scène de crime."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ferrière sait que j'ai la clé. Ça veut dire qu'il surveille la scène depuis avant mon arrivée. Ou qu'un de ses hommes m'a vu."},

    {"bg": "bureau", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven, faites attention. Ces gens-là font disparaître plus que des preuves."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je sais. C'est pour ça que j'ai copié les fichiers en triple et envoyé une copie cryptée à une boîte mail que Ferrière ne connaît pas."},

    {"bg": "bureau", "rain": False,
     "char": "policiere", "expr": 0, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Vous êtes toujours aussi paranoïaque."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ce n'est pas de la paranoïa si c'est vrai."},

    # CHOIX 2 ──────────────────────────────────────────────────────────────────
    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Ferrière sera là demain. Comment jouer cette partie ?",
     "choices": ["Agir seul — ne rien montrer à personne", "Faire confiance à Sato — travailler en binôme"],
     "choice_branch": {"0": "solo", "1": "team"}},

    # ── Branche SOLO (étendue) ────────────────────────────────────────────────
    {"id": "solo",
     "bg": "toit", "rain": False, "transition": "slide_left",
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Cette ville. Elle ne dort jamais. Et moi non plus. C'est notre point commun."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Travailler seul, c'est la seule façon dont je sache vraiment travailler. Pas de témoin de mes erreurs. Pas d'otage non plus."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Sato est compétente. Peut-être même brillante. Mais l'amener dans ça, c'est mettre sa carrière et sa vie en jeu. Elle a une fille."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je ne lui ai pas demandé son prénom. Je m'appelle Raven, pas héros de roman."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Seul, alors. Comme toujours. Je vais voir Ferrière demain et je vais mentir avec le sourire. C'est mon talent principal."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Papa, si tu m'entends... la Synarchie. Tu avais trouvé quelque chose en 1994. Ça m'a pris vingt ans pour arriver au même endroit que toi. Je ne vais pas m'arrêter là."},

    # ── Branche ÉQUIPE (étendue) ──────────────────────────────────────────────
    {"id": "team",
     "bg": "toit", "rain": False, "transition": "slide_left",
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "On fait équipe, alors. Je couvre vos arrières, vous couvrez les miens."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Avant que vous disiez oui définitivement — vous savez ce qu'il y a sur cette clé. Ces gens n'hésitent pas."},

    {"bg": "toit", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "J'ai passé douze ans dans la police, Raven. Je sais évaluer un risque. Ce dossier, si on ne le prend pas, quelqu'un d'autre le noiera. Ferrière, ou quelqu'un comme lui."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous l'avez évalué, le risque ?"},

    {"bg": "toit", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Haut. Très haut. J'accepte. Qu'est-ce qu'on fait pour Ferrière demain ?"},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On lui ment avec deux sources cohérentes au lieu d'une. C'est plus solide."},

    {"bg": "toit", "rain": False,
     "char": "policiere", "expr": 0, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "C'est la définition de votre méthode de travail habituelle ?"},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Globalement, oui."},

    # ── ACTE FINAL Ch1 : Le toit ───────────────────────────────────────────────
    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Les toits de Paris la nuit. C'est l'endroit où je réfléchis depuis que j'ai commencé ce métier."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mon père avait un carnet. Il y notait ses trouvailles. Des noms, des dates, des liens. La Synarchie apparaît quatre fois dans les soixante dernières pages."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_04_toit",
     "text": "Je n'ai jamais su pourquoi il avait arrêté de noter. Maintenant je sais. Il avait arrêté parce qu'ils l'avaient arrêté, lui."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Marcus Vane. Mon père. Deux hommes qui ont vu la même chose et qui en sont morts. Je ne mourrai pas sans l'avoir nommée."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Et moi, je la trouverai. C'est ma promesse à Vane. À mon père. À tous ceux que cette ville a avalés sans témoin."},

    {"bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "", "text": "─── FIN DU CHAPITRE I ───"},

    {"chapter_end": 1, "bg": "toit", "char": None, "side": "left",
     "name": "", "text": ""},
]

# ══════════════════════════════════════════════════════════════════════
# Chapitre II — Le Prix de la Vérité
# ══════════════════════════════════════════════════════════════════════
SCRIPT_II = [


 # ══════════════════════════════════════════════════════════════════════════
    # ████  CHAPITRE II — "Le Prix de la Vérité"  ████
    # ══════════════════════════════════════════════════════════════════════════

    {"bg": "bureau", "rain": False, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "", "text": "CHAPITRE II — Le Prix de la Vérité"},

    # ── ACTE 1 : Ferrière ──────────────────────────────────────────────────────
    {"bg": "salle_interrogatoire", "rain": False, "transition": "slide_left",
     "char": "ferriere", "expr": 1, "side": "right",
     "name": "CAPITAINE FERRIÈRE",
     "text": "Raven. Ça fait longtemps. J'entends dire que vous avez passé la nuit à Chinatown."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je passais dans le coin. Un mort de plus dans Paris, je me suis dit que ça vous ferait plaisir d'avoir un témoin de bonne volonté."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "ferriere", "expr": 0, "side": "right",
     "name": "CAPITAINE FERRIÈRE",
     "text": "Vous avez pris quelque chose sur la scène. On a des images."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 8, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Des images d'un homme qui examine une scène de crime publique. Ce que je fais tous les mardis soirs."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "ferriere", "expr": 1, "side": "right",
     "name": "CAPITAINE FERRIÈRE",
     "text": "Raven. Cet homme — Vane — n'était personne. Un comptable. Un dossier ouvert, classé dans six semaines. Ne rendez pas ça compliqué."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un comptable qu'on a pris la peine d'exécuter proprement, de nettoyer la scène et de déposer le corps en pleine nuit. On se donne tout ce mal pour 'personne' ?"},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "ferriere", "expr": 3, "side": "right",
     "name": "CAPITAINE FERRIÈRE",
     "text": "Je vous dis ça comme un conseil, Raven. Pas comme une menace."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je note la différence. Au revoir, Capitaine."},

    # ── Scène de repos : bureau, lendemain matin ────────────────────────────────
    {"bg": "bureau", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ferrière est nerveux. Les gens nerveux font des erreurs. C'est pour ça que je ne le suis pas — nerveux."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je mens à moi-même. Je suis nerveux depuis la nuit dernière. Depuis que j'ai vu le mot 'Synarchie' sur cette clé USB."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mon père m'a appris deux choses : ne jamais abandonner une piste, et toujours savoir quand une piste vous abandonne. Je ne sais pas encore laquelle s'applique ici."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Les fichiers Synarchie. J'ai passé trois heures à les décortiquer. Ce n'est pas un réseau criminel classique. C'est une organisation qui a des ministres, des banquiers, des juges. Elle n'est pas dans les institutions — elle les habite."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Et leur plan — j'ai trouvé deux références obliques dans les fichiers — leur plan passe par l'Union Européenne. Pas par sa destruction. Par sa transformation."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ils veulent une Europe unifiée sous un seul gouvernement. Ce qu'ils ne disent pas en public : ce gouvernement doit être le leur."},

    # ── ACTE 2 : Natasha ───────────────────────────────────────────────────────
    {"bg": "rue", "rain": True, "transition": "fade_black",
     "char": "natasha", "expr": 0, "side": "right",
     "name": "NATASHA MORI",
     "text": "Raven. Je vous attendais. Ça fait trois heures que je surveille votre immeuble."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Impressionnant. Et dérangeant. Natasha Mori. Vous écrivez pour qui, maintenant ?"},

    {"bg": "rue", "rain": True,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Pour un réseau de presse indépendant européen. Et je vous offre quelque chose que vous n'avez pas : un contexte."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Continuez."},

    {"bg": "rue", "rain": True,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Marcus Vane n'était pas votre comptable anonyme. J'enquêtais sur lui depuis dix-huit mois. Il était le trésorier de l'Europe de l'Ouest pour la Synarchie.",
     "evidence": ("Registre Offshore", "Vane — trésorier EU pour la Synarchie, 18 mois d'enquête Mori")},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je sais ça. Ce que je veux savoir, c'est ce que vous savez que je ne sais pas encore."},

    {"bg": "rue", "rain": True,
     "char": "natasha", "expr": 2, "side": "right",
     "name": "NATASHA MORI",
     "text": "La Synarchie recrute dans les grandes écoles depuis les années 80. Sciences Po, ENA, Polytechnique. Pas les marginaux — les brillants. Les futurs ministres."},

    {"bg": "rue", "rain": True,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Leur idéologie est simple et terrifiante : une Europe fédérale construite sur un modèle autoritaire centralisé. Ils appellent ça 'efficience démocratique'. L'Architecte a écrit un essai là-dessus en 1987 sous pseudonyme."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "L'Architecte. Ce nom revient dans les fichiers de Vane. Qui est-il ?"},

    {"bg": "rue", "rain": True,
     "char": "natasha", "expr": 3, "side": "right",
     "name": "NATASHA MORI",
     "text": "Ça, c'est ce que je cherche depuis deux ans. Et si vous m'aidez à le trouver, je vous donne ce que j'ai."},

    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un échange d'informations avec une journaliste. Ma journée se complique."},

    # CHOIX A ──────────────────────────────────────────────────────────────────
    {"bg": "rue", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Natasha propose un partenariat. Quelle posture adopter ?",
     "choices": ["Faire confiance — travailler avec elle", "Résister — garder l'enquête pour soi"],
     "choice_branch": {"0": "ch2_trust_ext_01", "1": "ch2_resist_ext_01"}},

    # ── BRANCHE TRUST (étendue) ───────────────────────────────────────────────
    {"id": "ch2_trust",
     "bg": "bureau", "rain": False, "transition": "fade_black",
     "char": "natasha", "expr": 2, "side": "right",
     "name": "NATASHA MORI",
     "text": "Bien. Voici ce que j'ai : Ferrière n'est pas seul. Il y a une taupe au niveau judiciaire. Un nom de code — Le Gardien. Je n'ai pas son identité réelle."},

    {"id": "ch2_trust_2",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Une taupe judiciaire. Ça explique pourquoi les dossiers proches de la Synarchie s'évaporent avant jugement."},

    {"bg": "bureau", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Depuis 2003, huit affaires liées aux réseaux que je trace ont été classées sans suite. Huit. Dont deux impliquaient des témoins qui ont changé de version du jour au lendemain."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous avez les noms des témoins ?"},

    {"bg": "bureau", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Deux sur huit. Le troisième est mort d'une overdose six semaines après la clôture du dossier. Il ne consommait pas."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le Fantôme. C'est le nom qui revient dans les fichiers de Vane pour les opérations terrain. Une identité fantôme qui circule à travers six pays."},

    {"bg": "bureau", "rain": False,
     "char": "natasha", "expr": 3, "side": "right",
     "name": "NATASHA MORI",
     "text": "Le Fantôme... j'ai une photo. Floue, prise de loin. Un homme avec un badge d'accréditation officielle à l'entrée d'un ministère. En 2018.",
     "evidence": ("Photo du Fantôme", "Silhouette avec badge officiel — ministère, 2018")},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ce badge. La coupe de veste. La carrure. Ça ressemble à Ferrière il y a cinq ans."},

    {"bg": "bureau", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "C'est ce que je pense aussi. Mais une ressemblance floue n'est pas une preuve. On a besoin de quelque chose de plus solide."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On a besoin du Loft 7. Vane y faisait des versements mensuels. C'est son adresse opérationnelle. Si on trouve quelque chose là-bas..."},

    {"bg": "bureau", "rain": False,
     "char": "natasha", "expr": 2, "side": "right",
     "name": "NATASHA MORI",
     "text": "Je connais l'adresse. J'attendais juste quelqu'un qui soit prêt à y entrer sans invitation."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je suis le moins qualifié pour entrer dans un endroit sans invitation. Allons-y."},

    # ── BRANCHE RESIST (étendue) ──────────────────────────────────────────────
    {"id": "ch2_resist",
     "bg": "rue", "rain": True, "transition": "fade_black",
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je n'ai pas besoin de partenaire pour l'instant, Mori. Mais gardez mes coordonnées."},

    {"id": "ch2_resist_2",
     "bg": "rue", "rain": True,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Vous allez commettre une erreur. Les gens qui travaillent seuls sur ce genre de dossier finissent... seuls, définitivement."},

    {"id": "ch2_resist_3",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je prends note. Au revoir, Mori."},

    {"bg": "bureau", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Elle a raison et je le sais. Mais la confiance dans ce métier est une ressource qui se recharge lentement."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Les fichiers de Vane mentionnent un 'Loft 7' comme point de transit. Des paiements réguliers. Une adresse dans le 10e arrondissement."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Si la Synarchie coordonne ses opérations depuis là, il y aura des preuves. Et je n'ai besoin de personne pour aller regarder.",
     "evidence": ("Photo du Fantôme", "Silhouette non-identifiée — badge officiel, dossier Vane")},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Travailler seul a un avantage : personne ne peut me trahir. Travailler seul a un inconvénient : personne ne peut me sauver non plus."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "C'est acceptable. Je vais au Loft 7."},

    # ── ACTE 3 : Le Loft 7 (convergence) ─────────────────────────────────────
    {"bg": "archives", "rain": False, "transition": "iris",
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Loft 7. Entrepôt reconverti, arrière-cour du 10e. Deux caméras, une porte avec code à quatre chiffres. Le code de Vane : 1944."},

    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "1944. La fin de la Seconde Guerre mondiale. Ou le début de ce que ces gens appellent 'la longue reconstruction'. Leur sens de l'humour est glacial.",
     "evidence": ("Clé du Loft 7", "Code 1944 — adresse opérationnelle Synarchie")},

    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Des serveurs. Des dossiers. Des cartes géographiques avec des cercles rouges sur Bruxelles, Berlin, Paris, Rome. Et un organigramme.",
     "evidence": ("Rapport interne", "Organigramme partiel Synarchie — 7 cellules actives EU")},

    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Sept cellules actives dans sept capitales européennes. Chacune avec un responsable politique, un financier, et un opérationnel. La structure d'un gouvernement fantôme."},

    # CHOIX B ──────────────────────────────────────────────────────────────────
    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Des voix dans le couloir. On approche. Quelle réaction ?",
     "choices": ["S'infiltrer plus profond — trouver les noms", "Faire pression — sortir et confronter celui qui arrive"],
     "choice_branch": {"0": "ch2_infiltrate", "1": "ch2_press"}},

    # ── BRANCHE INFILTRATE (étendue) ──────────────────────────────────────────
    {"id": "ch2_infiltrate",
     "bg": "archives", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je me planque derrière une rangée de serveurs. Les voix se rapprochent. Deux hommes. Un accent que je reconnais."},

    {"id": "ch2_infiltrate_2",
     "bg": "archives", "rain": False,
     "char": "ferriere", "expr": 1, "side": "right",
     "name": "CAPITAINE FERRIÈRE",
     "text": "L'opération Vane est close. Les fichiers sont sur la clé. Si Raven a décrypté quelque chose, il faut l'avoir avant qu'il transmette."},

    {"id": "ch2_infiltrate_3",
     "bg": "archives", "rain": False,
     "char": None, "side": "left",
     "name": "INCONNU",
     "text": "Et la journaliste japonaise ? Mori ?"},

    {"id": "ch2_infiltrate_4",
     "bg": "archives", "rain": False,
     "char": "ferriere", "expr": 1, "side": "right",
     "name": "CAPITAINE FERRIÈRE",
     "text": "Elle est surveillée. L'Architecte a dit qu'on attend. Elle pourrait nous amener à des sources qu'on n'a pas identifiées."},

    {"id": "ch2_infiltrate_5",
     "bg": "archives", "rain": False,
     "char": None, "side": "left",
     "name": "INCONNU",
     "text": "L'Architecte a aussi dit que la réforme est pour juin. Ça fait cinq mois. On ne peut pas se permettre de fuites."},

    {"id": "ch2_infiltrate_6",
     "bg": "archives", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Juin. Cinq mois. Ils ont une échéance. Et une réforme. Je dois savoir laquelle."},

    # ── BRANCHE PRESS (étendue) ───────────────────────────────────────────────
    {"id": "ch2_press",
     "bg": "archives", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je sors dans le couloir. Un homme en costume. La quarantaine. Il me regarde comme si je lui avais volé son café."},

    {"id": "ch2_press_2",
     "bg": "archives", "rain": False,
     "char": None, "side": "right",
     "name": "HOMME AU BADGE",
     "text": "Qui êtes-vous ? Ce site est interdit au public."},

    {"id": "ch2_press_3",
     "bg": "archives", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Détective Raven. Je travaille sur la mort de Marcus Vane. Vous le connaissiez ?"},

    {"id": "ch2_press_4",
     "bg": "archives", "rain": False,
     "char": None, "side": "right",
     "name": "HOMME AU BADGE",
     "text": "Je... non. Je ne connais pas ce nom. Ce local est une propriété privée. Partez ou j'appelle la police."},

    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il ment. Mais il a peur. Et la peur me donne plus d'informations que ses mots. Il connaît ce nom."},

    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Son badge. Accréditation temporaire, numéro de série. Je le mémorise avant de partir. Je peux remonter jusqu'à lui.",
     "evidence": ("Rapport interne", "Badge accréditation temporaire — numéro mémorisé, Loft 7")},

    # ── Convergence branche B, ACTE 4 ─────────────────────────────────────────
    {"bg": "toit", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je ressors du Loft 7 avec plus de questions que de réponses. C'est toujours le signe qu'on est au bon endroit."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Juin. Cinq mois — ou peut-être moins. La Synarchie a une échéance. Une réforme. Dans les institutions européennes."},

    {"bg": "toit", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. J'ai fait vérifier le véhicule. Les plaques FP reviennent à une flotte de services internes de la Préfecture. Mais la voiture n'est pas logguée cette nuit-là."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Quelqu'un a effacé le log. Depuis l'intérieur. Ce niveau d'accès... ça ne laisse pas beaucoup de candidats."},

    {"bg": "toit", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Ferrière a accès au système depuis sa position. Mais prouver qu'il a manipulé un log... il faut une trace numérique. Et ces traces-là ne survivent pas longtemps."},

    # CHOIX C ──────────────────────────────────────────────────────────────────
    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Ferrière doit être neutralisé. Comment ?",
     "choices": ["Trahir — l'exposer publiquement avec ce qu'on a", "Protéger — garder les preuves pour plus tard"],
     "choice_branch": {"0": "ch2_betray", "1": "ch2_protect"}},

    # ── BRANCHE BETRAY (étendue) ──────────────────────────────────────────────
    {"id": "ch2_betray",
     "bg": "bureau", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On l'expose. Maintenant. Avec ce qu'on a : le badge du Loft 7, le log effacé, la photo du Fantôme. Pas assez pour le condamner, mais assez pour le déstabiliser."},

    {"id": "ch2_betray_2",
     "bg": "bureau", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Si on l'expose trop tôt, il détruit les preuves et disparaît. Et on perd la Synarchie avec lui."},

    {"id": "ch2_betray_3",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ou il panique et commet une erreur. Les hommes comme Ferrière — habitués au contrôle — quand ils perdent le contrôle, ils font des choses stupides."},

    {"id": "ch2_betray_4",
     "bg": "bureau", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Je peux publier quelque chose de ciblé. Pas tout. Juste assez pour le forcer à réagir. Et on regarde vers qui il se retourne."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Faites-le. Et on surveille."},

    # ── BRANCHE PROTECT (étendue) ─────────────────────────────────────────────
    {"id": "ch2_protect",
     "bg": "bureau", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On garde tout en réserve. Ferrière est une pièce de l'échiquier, pas le roi. On le laisse se croire en sécurité pendant qu'on remonte la chaîne."},

    {"id": "ch2_protect_2",
     "bg": "bureau", "rain": False,
     "char": "policiere", "expr": 0, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Ça veut dire travailler avec quelqu'un qui sait où vous êtes, qui vous surveille, et qui pourrait décider à tout moment de faire le ménage."},

    {"id": "ch2_protect_3",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ça veut dire travailler dans des conditions qui ressemblent à ce que je fais depuis vingt ans. Je m'y connais."},

    {"id": "ch2_protect_4",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On construit le dossier. Lentement. Soigneusement. Jusqu'à ce qu'il soit assez solide pour résister à n'importe quel avocat de la Synarchie."},

    # ── ACTE FINAL Ch2 ─────────────────────────────────────────────────────────
    {"bg": "geneve", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Les preuves pointent vers Genève. Vane y faisait des transferts réguliers. Et l'adresse de livraison sur l'un des fichiers cryptés : Institut Voss pour la Coopération Européenne."},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "L'Architecte. Il a un nom, maintenant. Ou du moins une façade."},

    {"bg": "geneve", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Institut Voss. Heinrich Voss. C'est une figure publique — des universités, des prix Nobel, des présidents de commission qui lui serrent la main."},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ce sont exactement les hommes que la Synarchie recrute. Le visage présentable en façade. La mécanique dissimulée derrière."},

    {"bg": "geneve", "rain": False,
     "char": "natasha", "expr": 2, "side": "right",
     "name": "NATASHA MORI",
     "text": "Voss. C'est le nom que je cherchais depuis deux ans. C'était devant tout le monde."},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "C'est toujours le cas. Les monstres les plus dangereux ne se cachent pas. Ils organisent des galas."},

    {"bg": "geneve", "rain": False,
     "char": None, "side": "left",
     "name": "", "text": "─── FIN DU CHAPITRE II ───"},

    {"chapter_end": 2, "bg": "geneve", "char": None, "side": "left",
     "name": "", "text": ""},
]

# ══════════════════════════════════════════════════════════════════════
# Chapitre III — L'Architecte
# ══════════════════════════════════════════════════════════════════════
SCRIPT_III = [


 # ══════════════════════════════════════════════════════════════════════════
    # ████  CHAPITRE III — "L'Architecte"  ████
    # ══════════════════════════════════════════════════════════════════════════

    {"bg": "geneve", "rain": False, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "", "text": "CHAPITRE III — L'Architecte"},

    # ── Scène de repos : Raven seul à Genève ──────────────────────────────────
    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Genève sous la pluie. Tout semble propre ici. Trop propre. C'est le genre de propreté qui dissimule quelque chose."},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je pense à mon père. Il était venu ici en 1993, l'année avant sa mort. Il cherchait des archives sur des fonds d'après-guerre mal documentés."},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Dans son carnet, une note : 'Institut Voss — voir avec H.' Il connaissait quelqu'un à l'Institut. Quelqu'un dont il ne notait que l'initiale."},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "H. Voss. Heinrich Voss. Il avait rencontré l'Architecte. Et six mois plus tard il était mort dans un accident."},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je ne suis pas objectif sur ce dossier. Je le sais. Ça ne change rien — je suis le seul à avoir toutes les pièces."},

    # ── ACTE 1 : Confrontation ────────────────────────────────────────────────
    {"bg": "geneve", "rain": False,
     "char": "architect", "expr": 0, "side": "right",
     "name": "DR. HEINRICH VOSS",
     "cg": "cg_10_architecte",
     "text": "Détective Raven. Je m'attendais à vous voir, d'une façon ou d'une autre. Votre père était un homme curieux. La curiosité est héréditaire, apparemment."},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous connaissiez mon père."},

    {"bg": "geneve", "rain": False,
     "char": "architect", "expr": 1, "side": "right",
     "name": "DR. HEINRICH VOSS",
     "text": "Très brièvement. Il cherchait des archives que nous n'avions pas. Du moins, c'est ce que je lui ai dit."},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il est mort six mois après cette visite. Dans un accident."},

    {"bg": "geneve", "rain": False,
     "char": "architect", "expr": 0, "side": "right",
     "name": "DR. HEINRICH VOSS",
     "text": "Ces choses arrivent. Raven, je vais vous dire quelque chose que vous n'attendez pas : je respecte ce que vous faites. Vraiment."},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Continuez."},

    {"bg": "geneve", "rain": False,
     "char": "architect", "expr": 1, "side": "right",
     "name": "DR. HEINRICH VOSS",
     "text": "L'Europe est fragmentée, faible, divisée par des nationalismes d'un autre siècle. Elle a besoin d'une direction unifiée. Ce que je construis n'est pas le chaos. C'est l'ordre."},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "L'ordre que vous voulez construire a déjà été essayé. En 1939. Le résultat vous est peut-être familier."},

    {"bg": "geneve", "rain": False,
     "char": "architect", "expr": 2, "side": "right",
     "name": "DR. HEINRICH VOSS",
     "text": "Les méthodes étaient mauvaises. Pas l'objectif. Une Europe forte, une Europe unifiée — c'est la seule réponse aux crises qui viennent. Les nationalistes le détruiront. Nous le sauverons."},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous vous entendez parler ? 'Méthodes mauvaises'. Vane est mort parce que votre comptabilité devenait inconvéniente. Mon père..."},

    {"bg": "geneve", "rain": False,
     "char": "architect", "expr": 1, "side": "right",
     "name": "DR. HEINRICH VOSS",
     "text": "Votre père a fait un choix. Comme tout le monde doit choisir. De quel côté de l'histoire veut-on être ?"},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Du côté de la vérité. C'est vieux jeu, je sais."},

    # CHOIX D ──────────────────────────────────────────────────────────────────
    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Voss est là, devant moi. Les preuves sont partielles. Comment jouer ?",
     "choices": ["Confronter directement — exposer ce qu'on sait", "Observer dans l'ombre — attendre plus de preuves"],
     "choice_branch": {"0": "ch3_confront", "1": "ch3_shadow"}},

    # ── BRANCHE CONFRONT (étendue) ────────────────────────────────────────────
    {"id": "ch3_confront",
     "bg": "geneve", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je pose les fichiers sur le bureau. Imprimés, annotés. Vingt ans de flux financiers. Le Loft 7. Le Fantôme. Votre signature sur un accord de 1994.",
     "evidence": ("Accord Secret", "Signature Voss — accord non-déclaré, 1994, six gouvernements")},

    {"id": "ch3_confront_2",
     "bg": "geneve", "rain": False,
     "char": "architect", "expr": 3, "side": "right",
     "name": "DR. HEINRICH VOSS",
     "text": "Impressionnant. Vraiment. Vous avez reconstitué beaucoup plus que je ne pensais possible."},

    {"id": "ch3_confront_3",
     "bg": "geneve", "rain": False,
     "char": "architect", "expr": 1, "side": "right",
     "name": "DR. HEINRICH VOSS",
     "text": "Mais ces documents — sans contexte officiel, sans chaîne de garde légale — ne valent rien devant un tribunal. Et les tribunaux que vous connaissez ont des oreilles qui m'appartiennent."},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Interpol. Il y a encore des gens là-dedans qui vous sont étrangers. Et Natasha Mori a des copies. Déjà transmises."},

    {"bg": "geneve", "rain": False,
     "char": "architect", "expr": 3, "side": "right",
     "name": "DR. HEINRICH VOSS",
     "text": "Raven..."},

    {"bg": "geneve", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous avez tué mon père. Vous avez tué Vane. Je suis toujours là. C'est votre erreur principale — vous sous-estimez la persistance."},

    # ── BRANCHE SHADOW (étendue) ───────────────────────────────────────────────
    {"id": "ch3_shadow",
     "bg": "geneve", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je souris. Je lui dis que je suis venu pour des informations de routine. Je mens bien. C'est mon superpouvoir."},

    {"id": "ch3_shadow_2",
     "bg": "geneve", "rain": False,
     "char": "architect", "expr": 0, "side": "right",
     "name": "DR. HEINRICH VOSS",
     "text": "Je suis ravi de vous avoir reçu, Raven. Si vous avez d'autres questions, mon équipe est disponible."},

    {"id": "ch3_shadow_3",
     "bg": "geneve", "rain": True, "transition": "fade_black",
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je pars. Je le laisse croire qu'il a gagné. La prochaine fois qu'on se verra, ce sera devant un tribunal."},

    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "J'avais une caméra sur ma veste. Ses réactions, ses micro-expressions au moment où j'ai mentionné les fichiers. De la peur sous le contrôle.",
     "evidence": ("Accord Secret", "Enregistrement vidéo — réaction Voss aux fichiers, preuve comportementale")},

    # ── ACTE 2 : L'aéroport (convergence) ────────────────────────────────────
    {"bg": "aeroport_jetpack", "rain": False, "transition": "slide_left",
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Raven. Selg est à l'aéroport. Le Fantôme. Il prend un vol pour Berlin dans quarante minutes."},

    {"bg": "aeroport_jetpack", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_08_aeroport",
     "text": "Viktor Selg. C'est le nom sur le passeport. Mais ce n'est pas le sien. Il en a six."},

    {"bg": "aeroport_jetpack", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Si Selg fuit, on perd le lien opérationnel entre Voss et les meurtres. Voss est trop bien protégé sans Selg."},

    {"bg": "aeroport_jetpack", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On ne peut pas l'arrêter légalement. Pas encore. Mais on peut lui faire savoir qu'on sait."},

    # CHOIX E ──────────────────────────────────────────────────────────────────
    {"bg": "aeroport_jetpack", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Selg s'apprête à partir. Comment l'arrêter ?",
     "choices": ["Exposer — transmettre les preuves à Interpol maintenant", "Négocier — le contacter directement avant qu'il embarque"],
     "choice_branch": {"0": "ch3_expose", "1": "ch3_negotiate"}},

    # ── BRANCHE EXPOSE (étendue) ──────────────────────────────────────────────
    {"id": "ch3_expose",
     "bg": "aeroport_jetpack", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "J'appelle le contact Interpol que Sato m'a donné il y a trois ans et que je n'ai jamais utilisé. Jusqu'à maintenant.",
     "evidence": ("Enregistrement final", "Transmission Interpol — Selg/Voss, preuves partielles, flagrant délit tentative de fuite")},

    {"id": "ch3_expose_2",
     "bg": "aeroport_jetpack", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Ils ont bloqué l'embarquement. Selg est retenu aux douanes. On a vingt minutes avant que ses avocats arrivent."},

    {"id": "ch3_expose_3",
     "bg": "salle_interrogatoire", "rain": False, "transition": "iris",
     "char": "ghost", "expr": 1, "side": "right",
     "name": "VIKTOR SELG",
     "text": "Vingt minutes. Vingt et une, et mes avocats détruisent tout ce que vous pensez avoir."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "J'ai enregistré votre voix au Loft 7. 'L'Architecte a dit que la réforme est pour juin.' Cette voix, ce contenu. C'est vous."},

    {"bg": "salle_interrogatoire", "rain": False,
     "char": "ghost", "expr": 3, "side": "right",
     "name": "VIKTOR SELG",
     "text": "..."},

    # ── BRANCHE NEGOTIATE (étendue) ───────────────────────────────────────────
    {"id": "ch3_negotiate",
     "bg": "aeroport_jetpack", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je l'approche à la porte d'embarquement. Seul. Sans arme visible."},

    {"id": "ch3_negotiate_2",
     "bg": "aeroport_jetpack", "rain": False,
     "char": "ghost", "expr": 1, "side": "right",
     "name": "VIKTOR SELG",
     "text": "Raven. Vous êtes courageux ou stupide. Peut-être les deux."},

    {"id": "ch3_negotiate_3",
     "bg": "aeroport_jetpack", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "J'ai les fichiers. J'ai votre voix au Loft 7. J'ai une photo qui vous place à Genève la nuit de l'accord. Vous pouvez embarquer — mais l'Architecte saura que vous avez laissé passer votre seule chance de négocier."},

    {"bg": "aeroport_jetpack", "rain": False,
     "char": "ghost", "expr": 3, "side": "right",
     "name": "VIKTOR SELG",
     "text": "Qu'est-ce que vous voulez ?"},

    {"bg": "aeroport_jetpack", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La date de la réforme. Le nom du vote au Parlement. Et votre témoignage en échange d'une réduction.",
     "evidence": ("Enregistrement final", "Selg — témoignage conditionnel, date vote Parlement révélée")},

    # ── ACTE FINAL Ch3 ─────────────────────────────────────────────────────────
    {"bg": "geneve", "rain": True, "transition": "fade_black",
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_09_geneve",
     "text": "Genève. Je repars sans Voss dans les menottes. Mais avec plus qu'à l'arrivée."},

    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le Schéma du Réseau. Sept cellules, vingt-trois noms, une date. Juin. La réforme constitutionnelle européenne. Un vote au Parlement.",
     "evidence": ("Schéma du Réseau", "Organigramme Synarchie — 7 cellules, 23 noms, vote juin")},

    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "L'Identité de l'Architecte. Dr. Heinrich Voss. Né à Vienne en 1958. Conseiller de trois présidents de Commission. Fondateur de l'Institut Voss.",
     "evidence": ("Identité de l'Architecte", "Dr. Heinrich Voss — fondateur Institut Voss, ex-conseiller Commission EU")},

    {"bg": "geneve", "rain": True,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Le Passeport Fantôme. Viktor Selg. Six identités confirmées, rattachées à l'accord de Berlin de 1994.",
     "evidence": ("Passeport Fantôme", "Selg — 6 identités, présent accord Berlin 1994, co-signataire Synarchie")},

    # CHOIX F ──────────────────────────────────────────────────────────────────
    {"bg": "geneve", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "", "text": "Selg est vulnérable. Le moment critique approche.",
     "choices": ["Se sacrifier — rester comme cible pour protéger Sato", "Fuir — mettre les preuves en sécurité hors de portée"],
     "choice_branch": {"0": "ch3_sacrifice", "1": "ch3_escape"}},

    # ── BRANCHE SACRIFICE (étendue) ───────────────────────────────────────────
    {"id": "ch3_sacrifice",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_11_sacrifice",
     "text": "Je transmets tout à Mori. Je transmets tout à Sato. Et je reste visible. Je suis le paratonnerre."},

    {"id": "ch3_sacrifice_2",
     "bg": "geneve", "rain": True,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. Vous ne pouvez pas rester là. Ils vont envoyer quelqu'un."},

    {"id": "ch3_sacrifice_3",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je sais. C'est l'idée. Pendant qu'ils s'occupent de moi, vous avez le temps de transmettre aux bonnes mains."},

    {"id": "ch3_sacrifice_4",
     "bg": "geneve", "rain": True,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven, il y a d'autres façons..."},

    {"id": "ch3_sacrifice_5",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Leila. Votre fille a besoin d'une mère. Moi, je n'ai besoin que d'une chose : que cette affaire aboutisse. Allez."},

    {"id": "ch3_sacrifice_6",
     "bg": "geneve", "rain": True,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Papa. Si tu m'entends... j'espère que c'est la bonne décision. Je ne saurai peut-être pas si ça a fonctionné."},

    # ── BRANCHE ESCAPE (étendue) ──────────────────────────────────────────────
    {"id": "ch3_escape",
     "bg": "aeroport_jetpack", "rain": True, "transition": "slide_left",
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_12_fuite",
     "text": "Les preuves d'abord. Toujours. Je ne sers à rien mort ou en cellule."},

    {"id": "ch3_escape_2",
     "bg": "aeroport_jetpack", "rain": True,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "J'ai les copies. Trois serveurs différents. Deux dans des pays que la Synarchie ne contrôle pas encore."},

    {"id": "ch3_escape_3",
     "bg": "aeroport_jetpack", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Bien. On part. Paris d'abord, puis on voit. Ils vont mettre du temps à comprendre qu'on a disparu."},

    {"id": "ch3_escape_4",
     "bg": "aeroport_jetpack", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "J'ai toujours été meilleur à fuir qu'à me battre frontalement. Ce soir, c'est une qualité."},

    # ── ÉPILOGUE CH3 ────────────────────────────────────────────────────────────
    {"bg": "toit", "rain": False, "transition": "fade_white",
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "cg": "cg_13_epilogue",
     "text": "Paris. Les toits. Je reviens toujours ici pour réfléchir."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Voss est libre. Selg est quelque part entre deux identités. Ferrière continue à porter son badge. Mais les preuves existent. Et quelque chose a changé."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ils savent que je suis là. Ils vont mettre plus de pression. Ça veut dire que j'approche."},

    {"bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "", "text": "─── FIN DU CHAPITRE III ───\n\nNUIT SANS TÉMOIN — L'histoire continue..."},

    # ── Marqueur fin de chapitre III → carte narrative ───────────────────────
    {"chapter_end": 3, "bg": "toit", "char": None, "side": "left",
     "name": "", "text": ""},
]


# ══════════════════════════════════════════════════════════════════════
# Chapitre IV — L'Héritage
# ══════════════════════════════════════════════════════════════════════
SCRIPT_IV = [
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
]

# ══════════════════════════════════════════════════════════════════════
# Chapitre V — Le Fantôme
# ══════════════════════════════════════════════════════════════════════
SCRIPT_V = [

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
     "text": "Le Fantôme. Son identité complète : Viktor Selg. Diplomate suédois, attaché culturel officiel. Conseiller non officiel de trois commissions européennes — et l'homme derrière l'accord de Berlin.",
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
]

# ══════════════════════════════════════════════════════════════════════
# Chapitre VI — Parlement
# ══════════════════════════════════════════════════════════════════════
SCRIPT_VI = [

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
]

# ══════════════════════════════════════════════════════════════════════
# Chapitre VII — La Décision
# ══════════════════════════════════════════════════════════════════════
SCRIPT_VII = [

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

    {"chapter_end": 7, "bg": "toit", "char": None, "side": "left", "name": "", "text": ""},
]


SCRIPT_I_EXT = [

    # ════════════ EXTENSION BRANCHE "interrogation" ════════════════════════════
    # Le joueur a choisi d'interroger les témoins plutôt qu'examiner la scène.
    # Ces nœuds s'insèrent après "interro_taro_ok" et avant le tronc commun.

    {"id": "interro_ext_01",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il reste trois témoins dans la zone de sécurité. Le flic de faction les a regroupés sous un auvent : une femme d'une cinquantaine d'années, un coursier, un jeune homme qui tremble."},

    {"id": "interro_ext_02",
     "bg": "salle_interrogatoire", "rain": True,
     "char": "policiere", "expr": 0, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "La dame, c'est Mme Yong. Elle tient l'épicerie du coin depuis vingt ans. Elle a vu quelque chose mais elle dit qu'elle ne parle qu'à un 'vrai policier'."},

    {"id": "interro_ext_03",
     "bg": "salle_interrogatoire", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je sors ma carte de presse. Je lui montre. Elle la lit deux fois. 'Privé. Ça compte quand même ?' Oui, madame. Ça compte quand même."},

    {"id": "interro_ext_04",
     "bg": "salle_interrogatoire", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Mme Yong — petite, manteau imperméable, parapluie violet fermé qu'elle n'a pas lâché — parle lentement, en choisissant chaque mot."},

    {"id": "interro_ext_05",
     "bg": "salle_interrogatoire", "rain": True,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "MME YONG",
     "text": "Une voiture. Grise. Elle attendait depuis au moins deux heures avant le coup de feu. Moteur allumé. Personne ne fait ça. Pas ici. Pas à cette heure."},

    {"id": "interro_ext_06",
     "bg": "salle_interrogatoire", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous avez vu la plaque ? Ou au moins la couleur exacte ?"},

    {"id": "interro_ext_07",
     "bg": "salle_interrogatoire", "rain": True,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "MME YONG",
     "text": "Grise métallisée. Comme la fourchette de ma belle-mère. Le premier chiffre, c'était un sept. Et les deux lettres du milieu, WK. J'ai une bonne mémoire pour les chiffres. C'est mon métier.",
     "evidence": ("Plaque partielle WK", "Véhicule gris — 2h stationnement — fuite après coup de feu")},

    {"id": "interro_ext_08",
     "bg": "salle_interrogatoire", "rain": True,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "C'est une plaque d'entreprise. La série WK, c'est une flotte de location. Pas un particulier. Quelqu'un qui ne veut pas qu'on remonte à lui."},

    {"id": "interro_ext_09",
     "bg": "salle_interrogatoire", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Le coursier, ensuite. Vingt-deux ans, veste réfléchissante, écouteur encore dans l'oreille droite. Il a les yeux d'un homme qui a vu quelque chose qu'il ne voulait pas voir."},

    {"id": "interro_ext_10",
     "bg": "salle_interrogatoire", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous êtes passé par là à quelle heure exactement ?"},

    {"id": "interro_ext_11",
     "bg": "salle_interrogatoire", "rain": True,
     "char": "taro", "expr": 0, "side": "right",
     "name": "COURSIER — PIERRE",
     "text": "2h12. J'ai regardé mon téléphone juste avant. Ma livraison était en retard. Il y avait un type — pas Vane, l'autre — qui regardait vers le haut de la ruelle. Vers les fenêtres."},

    {"id": "interro_ext_12",
     "bg": "salle_interrogatoire", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un guetteur. Ils avaient un guetteur. C'est une opération coordonnée. Pas un crime spontané."},

    {"id": "interro_ext_13",
     "bg": "salle_interrogatoire", "rain": True,
     "char": "taro", "expr": 1, "side": "right",
     "name": "COURSIER — PIERRE",
     "text": "Il portait un imperméable noir. Environ quarante ans. Un truc sur son oreille — une oreillette. Comme les gardes du corps. J'ai pensé que c'était un bodyguard. Alors j'ai pas regardé plus longtemps.",
     "evidence": ("Description du guetteur", "Homme ~40 ans, imperméable noir, oreillette — 2h12")},

    {"id": "interro_ext_14",
     "bg": "salle_interrogatoire", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Le troisième témoin refuse de parler. Il fixe ses chaussures. Ses mains tremblent. Ce n'est pas de la peur ordinaire — c'est de la reconnaissance. Il a vu quelqu'un qu'il connaît."},

    {"id": "interro_ext_15",
     "bg": "salle_interrogatoire", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je ne lui pose pas de question. Je lui laisse ma carte. Et je lui dis : 'Vous n'avez rien à prouver ce soir. Mais si ça change, je réponds toujours.' Parfois, attendre est un acte d'enquête."},

    {"id": "interro_ext_16",
     "bg": "scene_de_crime", "rain": True,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Bilan : une plaque, une description. C'est mince. Mais c'est plus que ce qu'on avait il y a vingt minutes."},

    {"id": "interro_ext_17",
     "bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "C'est assez pour commencer. Une flotte de location avec WK dans la plaque, dans un rayon de deux kilomètres. Ça se rétrécit vite."},

    # Rejoindre le tronc commun (choix solo/team)
    {"id": "interro_ext_merge",
     "bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "",
     "text": "La pluie redouble. Il reste quarante minutes avant que Ferrière n'arrive et ne ferme la scène. Il faut décider comment utiliser ce temps.",
     "choices": ["Continuer seul — garder l'avance sur la hiérarchie", "Appeler du renfort — cette affaire est trop grande pour un seul homme"],
     "choice_branch": {"0": "solo", "1": "team"}},

    # ════════════ EXTENSION BRANCHE "scene" ════════════════════════════════════
    # Le joueur a choisi d'examiner la scène plutôt qu'interroger les témoins.

    {"id": "scene_ext_01",
     "bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je commence par la périphérie. Toujours. Les criminels se concentrent sur le centre, oublient les bords. C'est là qu'ils laissent des traces."},

    {"id": "scene_ext_02",
     "bg": "scene_de_crime", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Contre le mur nord : une marque. Pas une égratignure. Un tracé délibéré, fait avec quelque chose de pointu. Deux lettres entrelacées : V et S."},

    {"id": "scene_ext_03",
     "bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "VS. Vane avait un complice ? Ou un témoin ? Ou quelqu'un qui était là avant lui et a voulu signer quelque chose ?",
     "evidence": ("Marque VS", "Lettres gravées dans la ruelle — auteur inconnu — avant le meurtre")},

    {"id": "scene_ext_04",
     "bg": "scene_de_crime", "rain": True,
     "char": "policiere", "expr": 0, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. Venez voir. Le béton sous la victime. Il y a une empreinte de chaussure. Pointure 43, semelle de course. Et il n'a pas bougé. Il était debout quand il a été touché."},

    {"id": "scene_ext_05",
     "bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Debout. Face à quelqu'un. Il n'essayait pas de fuir. Il attendait. Vane avait un rendez-vous. Et son interlocuteur a décidé que c'était le dernier."},

    {"id": "scene_ext_06",
     "bg": "scene_de_crime", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "À dix mètres du corps, dans une fissure du mur : un téléphone prépayé écrasé. Volontairement. La carte SIM a été retirée mais la coque a survécu. Dessous, griffonné au marqueur : une suite de chiffres."},

    {"id": "scene_ext_07",
     "bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Sept chiffres. Une fréquence radio ? Non — un code postal. Luxembourg. Et une date. Dans six jours.",
     "evidence": ("Téléphone écrasé", "Code postal Luxembourg + date — rendez-vous prévu")},

    {"id": "scene_ext_08",
     "bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vane avait prévu de disparaître. Il avait prévu de fuir vers le Luxembourg dans six jours. Quelqu'un l'a su avant lui. Et a devancé ce plan."},

    {"id": "scene_ext_09",
     "bg": "scene_de_crime", "rain": True,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Il y a une autre chose. Son manteau — il porte un revers intérieur cousu. Quelqu'un a essayé de l'ouvrir et s'est arrêté. La couture est à moitié défaite."},

    {"id": "scene_ext_10",
     "bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ils cherchaient quelque chose. Ils n'ont pas eu le temps de finir. Ou ils ont été interrompus. La clé USB était dans la poche intérieure — ils ne l'ont pas trouvée."},

    {"id": "scene_ext_11",
     "bg": "scene_de_crime", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Je prends le téléphone dans une pochette de preuve. Je prends des photos du tracé VS. Je mesure les distances. Je travaille méthodiquement, comme mon père m'a appris à lire : mot par mot, sans sauter de ligne."},

    {"id": "scene_ext_12",
     "bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mon père. Il aurait aimé ça. Cette ruelle. Cette énigme. Il aurait sorti son carnet et il aurait commencé à noter avant même d'avoir compris pourquoi."},

    {"id": "scene_ext_13",
     "bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je ne note plus. Je mémorise. Les carnets se perdent. Les carnets peuvent être saisis. Ce que j'ai dans la tête, personne ne peut me le prendre."},

    {"id": "scene_ext_14",
     "bg": "scene_de_crime", "rain": True,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "J'ai récupéré l'historique des appels du fixe de Vane pour le mois dernier. Douze appels vers le même numéro masqué. Réguliers. Un contact habitual. Pas quelqu'un de nouveau."},

    {"id": "scene_ext_15",
     "bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un numéro masqué régulier. C'est un handler. Quelqu'un qui le guidait. Ou quelqu'un qui le surveillait. Deux lectures très différentes du même fait."},

    {"id": "scene_ext_16",
     "bg": "scene_de_crime", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "",
     "text": "La pluie redouble. La scène de crime ne va pas rester ouverte encore longtemps. Il faut décider de la suite.",
     "choices": ["Continuer seul — garder l'avance sur la hiérarchie", "Appeler du renfort — cette affaire est trop grande pour un seul homme"],
     "choice_branch": {"0": "solo", "1": "team"}},
]


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION B : EXTENSIONS DES BRANCHES CH2
#  ch2_trust / ch2_resist → ~18 nœuds exclusifs chacune avant convergence
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_II_EXT = [

    # ════════════ EXTENSION BRANCHE ch2_trust ══════════════════════════════════

    {"id": "ch2_trust_ext_01",
     "bg": "bureau", "rain": False,
     "char": "natasha", "expr": 0, "side": "right",
     "name": "NATASHA MORI",
     "text": "Je vous transmets ce que j'ai sur la Synarchie. Mais d'abord — pourquoi vous faites confiance à une journaliste ? Vous détestez la presse. Tout le monde sait ça."},

    {"id": "ch2_trust_ext_02",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je ne fais pas confiance à la presse. Je fais confiance aux preuves. Et vous en avez. Ce n'est pas pareil."},

    {"id": "ch2_trust_ext_03",
     "bg": "bureau", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Le registre offshore. Banque de Riga, compte ouvert en 1952. Dormant pendant trente ans. Réactivé en 1982. Depuis lors, cent douze versements. Montants échelonnés pour rester sous les seuils de déclaration.",
     "evidence": ("Registre Offshore", "Compte Riga 1952 — 112 versements — identités masquées")},

    {"id": "ch2_trust_ext_04",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "1952. L'année de la fondation selon les archives que Vane avait. Ce compte existe depuis le début. C'est le nerf financier de toute l'organisation."},

    {"id": "ch2_trust_ext_05",
     "bg": "bureau", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Trois des bénéficiaires sont des entités morales. Deux fondations et un think tank. Je les ai retracés. Ils ont tous le même agent fiscal déclaré à Chypre. Un certain... Heinrich Voss."},

    {"id": "ch2_trust_ext_06",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "L'Architecte. On revient toujours à lui. Il est la colonne vertébrale. Ferrière, Vane, les comptes — ce sont des organes. Lui, c'est le squelette."},

    {"id": "ch2_trust_ext_07",
     "bg": "bureau", "rain": False,
     "char": "natasha", "expr": 2, "side": "right",
     "name": "NATASHA MORI",
     "text": "J'ai essayé de le contacter officiellement il y a six mois. Par l'intermédiaire de son institut. Quarante-huit heures plus tard, ma voiture était sabotée. Câble de frein partiellement sectionné."},

    {"id": "ch2_trust_ext_08",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ils ne menacent pas. Ils agissent. Comme avec mon père. Câble de frein — même méthode."},

    {"id": "ch2_trust_ext_09",
     "bg": "bureau", "rain": False,
     "char": "natasha", "expr": 3, "side": "right",
     "name": "NATASHA MORI",
     "text": "Votre père. Vous pensez que l'accident..."},

    {"id": "ch2_trust_ext_10",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je pense depuis dix ans. Ce n'est pas le moment d'en parler. Si vous voulez collaborer, j'ai besoin du dossier complet sur les réformes constitutionnelles européennes liées à Voss."},

    {"id": "ch2_trust_ext_11",
     "bg": "bureau", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Réforme de Lisbonne bis. Soumise discrètement à trois commissions. Texte de 400 pages. Clause 77, alinéa 4 : permet la fusion de la souveraineté budgétaire de douze États sans référendum public."},

    {"id": "ch2_trust_ext_12",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Sans référendum. C'est le coup d'État légal qu'ils préparent. Une Europe unifiée sous une seule main — la bonne — sans que personne ait voté pour."},

    {"id": "ch2_trust_ext_13",
     "bg": "bureau", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Le vote en commission est prévu dans quatre mois. Si la réforme passe, la clause 77 entre en application. À ce moment-là, plus rien n'est révocable sans un consensus unanime des douze États. C'est irréversible."},

    {"id": "ch2_trust_ext_14",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Quatre mois. On travaille ensemble. On partage tout. Et si l'un de nous disparaît, l'autre publie immédiatement. Accord ?"},

    {"id": "ch2_trust_ext_15",
     "bg": "bureau", "rain": False,
     "char": "natasha", "expr": 0, "side": "right",
     "name": "NATASHA MORI",
     "text": "Accord. Mais je publie quoi qu'il arrive quand j'estime que le moment est venu. Même si vous n'êtes pas d'accord. Ce point n'est pas négociable."},

    {"id": "ch2_trust_ext_16",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je peux vivre avec ça. On commence maintenant. Le Loft 7 — qu'est-ce que vous savez exactement ?",
     "choices": ["Infiltrer le Loft 7 avec Natasha", "Contacter la presse internationale en parallèle"],
     "choice_branch": {"0": "ch2_infiltrate", "1": "ch2_press"}},

    # ════════════ EXTENSION BRANCHE ch2_resist ═════════════════════════════════

    {"id": "ch2_resist_ext_01",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je travaille seul parce que c'est plus propre. Moins d'exposition. Moins de surfaces d'attaque. Natasha Mori a ses propres objectifs. Sa publication. Son nom dans les journaux."},

    {"id": "ch2_resist_ext_02",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je l'observe à distance. Je lis ses articles. Elle est précise, rigoureuse, courageuse. Mais elle ne sait pas qu'elle est déjà repérée. Sa ligne téléphonique est probablement sous écoute."},

    {"id": "ch2_resist_ext_03",
     "bg": "bureau", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "Trois nuits seul avec les dossiers de Vane. Café froid. Fenêtres fermées. Un fil rouge accroché au mur, des punaises, des photocopies. C'est comme ça que mon père travaillait."},

    {"id": "ch2_resist_ext_04",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il y a un nom qui revient dans toutes les transactions de Vane. Pas un prénom, pas une raison sociale. Un sobriquet : 'L'Ingénieur'. Il reçoit 3% de chaque virement. Depuis 1994."},

    {"id": "ch2_resist_ext_05",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "L'Ingénieur. Pas l'Architecte. Un échelon en dessous. Quelqu'un qui implémente. Quelqu'un qui connaît les détails techniques. Peut-être quelqu'un qui peut parler."},

    {"id": "ch2_resist_ext_06",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je croise le sobriquet avec les anciens dossiers de la DGSI que j'ai pu récupérer par mes contacts. Rien. Ce nom n'existe pas officiellement. Ce qui signifie qu'il est protégé au plus haut niveau."},

    {"id": "ch2_resist_ext_07",
     "bg": "bureau", "rain": True,
     "char": "taro", "expr": 1, "side": "right",
     "name": "TARO MITSUKI",
     "text": "Raven. Tu m'appelles à 4h du matin pour me demander qui est 'L'Ingénieur'. C'est soit une question très idiote, soit une question très dangereuse. Laquelle c'est ?"},

    {"id": "ch2_resist_ext_08",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La deuxième. Tu sais quelque chose ?"},

    {"id": "ch2_resist_ext_09",
     "bg": "bureau", "rain": True,
     "char": "taro", "expr": 3, "side": "right",
     "name": "TARO MITSUKI",
     "text": "J'entends des rumeurs depuis dix ans. L'Ingénieur, c'est le surnom d'un ex-officier de la Stasi reconverti. Il conçoit les 'accidents'. Il modélise les risques. Il prédit les comportements des enquêteurs."},

    {"id": "ch2_resist_ext_10",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Stasi. Est-ce qu'il a un vrai nom ?"},

    {"id": "ch2_resist_ext_11",
     "bg": "bureau", "rain": True,
     "char": "taro", "expr": 1, "side": "right",
     "name": "TARO MITSUKI",
     "text": "Viktor Selg. Ou c'est ce que disent ceux qui sont encore en vie pour en parler. Et ils sont pas nombreux. Je te donne ça, Raven, mais tu ne m'as jamais appelé. Tu n'as jamais eu ce nom.",
     "evidence": ("Viktor Selg — dit le Fantôme", "Ex-Stasi — bras armé de la Synarchie depuis 1994")},

    {"id": "ch2_resist_ext_12",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Viktor Selg. Le Fantôme. C'est lui qui a modélisé la mort de mon père. J'en suis presque certain maintenant."},

    {"id": "ch2_resist_ext_13",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je reste seul. Mais avec ce nom, je ne suis plus aveugle. Je sais ce que je cherche. Je sais vers quoi je me dirige."},

    {"id": "ch2_resist_ext_14",
     "bg": "bureau", "rain": True,
     "char": None, "side": "left",
     "name": "",
     "text": "La nuit passe. Je ne dors pas. Je croise Viktor Selg avec tous les dossiers d'accidents non résolus en Europe depuis 1994. Douze correspondances. Douze 'accidents'. Dont celui de mon père."},

    {"id": "ch2_resist_ext_15",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vingt-et-un ans. J'ai mis vingt-et-un ans à mettre un nom sur ce que je savais déjà. La fatigue que je ressens là n'est pas physique. C'est quelque chose d'autre."},

    {"id": "ch2_resist_ext_16",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "",
     "text": "L'aube. Il faut choisir la prochaine étape.",
     "choices": ["Infiltrer le Loft 7 — seul, sans couverture", "Contacter la presse — Natasha Mori est la seule qui comprend"],
     "choice_branch": {"0": "ch2_infiltrate", "1": "ch2_press"}},
]


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION C : CHAPITRE III-B — "TERRAIN"
#  Enquête de terrain entre ch3 et ch4 — témoins mineurs, micro-indices, lore
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_IIIB = [

    # ── Titre et accroche ──────────────────────────────────────────────────────
    {"bg": "rue", "rain": False, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "",
     "text": "CHAPITRE III-B — Terrain"},

    {"bg": "rue", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Après Genève, avant que la poussière ne retombe. La Synarchie est officiellement 'démantelée'. Trois membres arrêtés. Sept en fuite. Et quelque chose que personne n'a encore dit tout haut : ce n'est pas fini."},

    {"bg": "rue", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ferrière est en détention préventive. L'Architecte a disparu entre l'arrestation et le transfert. Disparu. Comme si quelqu'un avait ouvert une porte qu'il n'aurait pas dû pouvoir ouvrir."},

    {"bg": "rue", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. Je sais ce que vous pensez. Arrêtez. La Préfecture a déclenché une alerte internationale. Interpol est dans la boucle. Votre travail ici est terminé."},

    {"bg": "rue", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mon travail n'est jamais terminé quand quelqu'un s'est évadé. Surtout pas celui-là."},

    # ── ACTE 1 Ch3-B : Rue de Chinatown revisitée ──────────────────────────────
    {"bg": "scene_de_crime", "rain": False, "transition": "slide_left",
     "char": None, "side": "left",
     "name": "",
     "text": "La ruelle de Chinatown. Six semaines après la mort de Vane. Le ruban de sécurité a disparu. Un restaurant a rouvert à l'angle. La ville a déjà recouvert la trace."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je reviens toujours sur les scènes de crime. Pas par nostalgie. Par méthode. Les lieux parlent différemment selon le moment de la journée, selon la lumière, selon qu'on est pressé ou non."},

    {"bg": "scene_de_crime", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Une vieille dame balaye devant son commerce. Elle s'arrête quand elle me voit. Elle me reconnaît — j'étais là la nuit du meurtre. Elle n'a pas été interrogée."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "policiere", "expr": 0, "side": "right",
     "name": "MME CHEN",
     "text": "Vous êtes le type du journal ? Non ? Le flic en civil. J'ai quelque chose pour vous. J'attendais que quelqu'un revienne. Six semaines. Personne n'est revenu."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je suis revenu. Qu'est-ce que vous avez vu ?"},

    {"bg": "scene_de_crime", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "MME CHEN",
     "text": "Pas vu. Entendu. Avant le coup de feu — dix minutes avant — une conversation. Dans la ruelle. Deux voix. L'une disait : 'Le Viertes Reich ne tolère pas les hésitants.' L'autre n'a rien répondu.",
     "evidence": ("Témoignage Chen", "Phrase 'Viertes Reich' entendue 10 min avant le meurtre de Vane")},

    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Viertes Reich. Le Quatrième Reich. Ils utilisent ce nom en interne. Ce n'est pas une métaphore ou une hyperbole de journaliste. C'est leur terme. C'est ce qu'ils croient être en train de bâtir."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vane a hésité. C'est pour ça qu'il est mort. Pas parce qu'il allait parler — parce qu'il a hésité. Pour eux, l'hésitation est la trahison."},

    # ── ACTE 2 Ch3-B : Le train ────────────────────────────────────────────────
    {"bg": "train", "rain": False, "transition": "slide_left",
     "char": None, "side": "left",
     "name": "",
     "text": "Je reprends la piste du Luxembourg. Le rendez-vous que Vane n'a jamais pu honorer. Quelqu'un l'attendait là-bas. Peut-être quelqu'un qui ne sait pas encore que Vane est mort."},

    {"bg": "train", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Thalys. Cinq heures de trajet. Je prends le billet au guichet, en liquide. Je n'utilise pas ma carte depuis trois jours. Vieille habitude."},

    {"bg": "train", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Dans le wagon-restaurant, un homme lit le Financial Times. Il a l'air de lire mais ses yeux ne bougent pas. Je connais ce regard. C'est le regard de quelqu'un qui surveille."},

    {"bg": "train", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il est seul. Costard, pas de cravate. Cinquante ans environ. Il a un léger accent à Salzbourg si je devais deviner — la façon dont il dit 'merci' à la serveuse. Autrichien."},

    {"bg": "train", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je m'assieds à la table voisine. Je commande un café. Je ne le regarde pas. Je le laisse me regarder. Après six minutes, il se lève et s'en va sans avoir commencé son journal."},

    {"bg": "train", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Il laisse le journal sur la table. Coincé dans les pages : une carte de visite vierge. Au dos, écrit au stylo bille : 'Arrêtez. Ils ont déjà vos photos.' Rien d'autre."},

    {"bg": "train", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mes photos. Pas mon nom — mes photos. Ce qui signifie qu'ils ont de quoi m'identifier sans document officiel. Ils ont infiltré quelque chose de proche.",
     "evidence": ("Carte vierge — train", "Avertissement anonyme — 'ils ont vos photos' — auteur inconnu")},

    {"bg": "train", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je pense à Mme Chen. Au coursier Pierre. Au troisième témoin qui n'a pas voulu parler. À tous ceux qui savent quelque chose et qui vivent avec le poids de ce savoir."},

    {"bg": "train", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je n'ai rien fait de courageux. J'ai juste continué. Parfois c'est la même chose. Parfois ce ne l'est pas."},

    # ── ACTE 3 Ch3-B : Archives Luxembourg ─────────────────────────────────────
    {"bg": "archives", "rain": False, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "",
     "text": "Luxembourg-Ville. Les Archives centrales du Parlement Européen. J'entre avec de faux papiers de journaliste que Natasha m'a fait parvenir. Elle est plus utile en alliée qu'en adversaire."},

    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je cherche la Réforme de Lisbonne bis. Clause 77. Elle est là, dans les archives consultables, mais classée 'document de travail non finalisé'. Personne ne la cherche. Personne ne la lit."},

    {"bg": "archives", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "L'archiviste — une femme d'une trentaine d'années, lorgnons, efficace — pose la boîte sur ma table sans commentaire. Quatre cents pages. Technocratie dense."},

    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La clause 77. Alinéa 4. Les mots sont neutres, juridiques, presque ennuyeux. Mais ce qu'ils disent est simple : douze États peuvent décider ensemble de transférer leur souveraineté à un organe central. Sans consultation populaire. Par vote parlementaire simple."},

    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ils n'ont pas besoin d'un coup d'État violent. Ils n'ont pas besoin de tanks. Ils ont besoin de 78 votes dans trois commissions parlementaires et d'un bon avocat. Voss est les deux.",
     "evidence": ("Clause 77 — Réforme de Lisbonne bis", "Fusion souveraineté 12 États — sans référendum — vote commission")},

    {"bg": "archives", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Je photographie les pages pertinentes. L'archiviste revient. 'Monsieur, les appareils photo sont interdits dans cette salle.' Je referme le livre. Je souris. 'Je prends des notes mentales.' Elle ne me croit pas. Elle a raison."},

    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je sors avec les photos. Et avec quelque chose que je n'attendais pas : une date tamponnée sur la première page. Ce document a été consulté quatre fois au cours du dernier mois. Par deux personnes différentes. Selon le registre des consultations."},

    {"bg": "archives", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "L'une de ces personnes utilisait le badge diplomatique de la délégation allemande. Arnheim. Le Sénateur. Il est venu vérifier que son texte était toujours là. Intact. Attendant."},

    # ── Marqueur fin Ch3-B ──────────────────────────────────────────────────────
    {"bg": "train", "rain": True, "transition": "fade_black",
     "char": None, "side": "left",
     "name": "",
     "text": "─── FIN DU CHAPITRE III-B ───"},

    {"chapter_end": 3, "bg": "train", "char": None, "side": "left",
     "name": "", "text": ""},
]


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION D : CHAPITRE III-C — "MÉMOIRE"
#  Repos, flashbacks, character building — pas de choix majeurs
#  Renforce l'attachement avant les chapitres plus lourds (IV-VII)
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_IIIC = [

    # ── Titre ──────────────────────────────────────────────────────────────────
    {"bg": "bureau", "rain": False, "transition": "fade_white",
     "char": None, "side": "left",
     "name": "",
     "text": "CHAPITRE III-C — Mémoire"},

    {"bg": "bureau", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Retour à Paris. Mon bureau. Il est 23h14. La fenêtre est ouverte malgré le froid. J'aime entendre la ville — ça me rappelle que le monde continue de tourner même quand j'ai l'impression de tenir le seul fil qui l'empêche de s'effondrer."},

    # ── ACTE 1 Ch3-C : Raven seul, nuit, fil rouge ─────────────────────────────
    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je n'ai pas dormi depuis... Je ne sais plus. Le temps s'est aplati. Il y a des affaires qui font ça — elles absorbent le temps comme du papier buvard absorbe l'encre. Il ne reste plus rien."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ma mère appelait ça 'être hanté'. Elle disait que mon père était hanté par certaines questions. Que c'est ce qui l'avait rendu capable d'écrire des choses que personne d'autre n'aurait écrites. Et que c'est ce qui l'avait tué."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je regarde le mur. Le fil rouge. Les punaises. Les photos. Il y a des nœuds que je ne comprends pas encore. Des connexions qui manquent. Ça me dérange moins qu'avant. Les trous font partie de l'image."},

    # ── FLASHBACK : Strasbourg, 1987 ───────────────────────────────────────────
    {"bg": "bureau", "rain": False, "transition": "fade_white",
     "char": None, "side": "left",
     "name": "",
     "text": "Strasbourg. 1987. J'ai huit ans."},

    {"bg": "scene_de_crime", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Mon père range ses papiers dans une mallette. Vieille, en cuir marron, une fermeture éclair qui grince toujours au même endroit. Je connais ce son par cœur — c'est le son du départ."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "JEUNE ÉLIE (voix intérieure)",
     "text": "Papa. Tu travailles sur quoi ?"},

    {"bg": "scene_de_crime", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "Il s'arrête. Il pose la mallette. Il s'accroupit à ma hauteur. Il fait ça toujours — se mettre à ma hauteur, ne jamais me parler d'en haut. J'ai mis des années à comprendre que c'était rare."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "taro", "expr": 1, "side": "right",
     "name": "PAUL RAVEN (voix souvenir)",
     "text": "Je travaille sur quelque chose de difficile. Sur de l'argent qui vient de très loin et qui va vers des endroits où il ne devrait pas aller. Tu comprends ?"},

    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "JEUNE ÉLIE (voix intérieure)",
     "text": "C'est comme de la contrebande ? Comme dans les films ?"},

    {"bg": "scene_de_crime", "rain": False,
     "char": "taro", "expr": 2, "side": "right",
     "name": "PAUL RAVEN (voix souvenir)",
     "text": "Un peu. Mais plus compliqué. Parce que ceux qui font ça sont des gens en costume qui vont dans des dîners. Des gens qui font des discours sur l'avenir de l'Europe."},

    {"bg": "scene_de_crime", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "JEUNE ÉLIE (voix intérieure)",
     "text": "Et toi, tu vas les arrêter ?"},

    {"bg": "scene_de_crime", "rain": False,
     "char": "taro", "expr": 0, "side": "right",
     "name": "PAUL RAVEN (voix souvenir)",
     "text": "Je vais écrire la vérité sur eux. Et après, d'autres personnes pourront les arrêter. C'est comme ça que ça marche. Si tu veux changer les choses, tu commences par dire ce qui est vrai."},

    # ── Retour au présent ──────────────────────────────────────────────────────
    {"bg": "bureau", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il avait raison. Il avait aussi tort. Écrire la vérité ne suffit pas quand ceux à qui vous l'envoyez ont été achetés avant que vous n'ayez terminé d'écrire."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mon père a été tué dix mois après cette conversation. Le dossier a disparu. L'article n'a jamais été publié. Et moi, j'ai mis un uniforme et j'ai décidé que j'allais 'arrêter les gens' plutôt qu'écrire sur eux."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je les ai arrêtés, oui. Pendant seize ans. Des petits criminels, des dealers, des escrocs locaux. Pendant ce temps, ceux en costume continuaient leurs dîners."},

    # ── ACTE 2 Ch3-C : Un appel de Sato ───────────────────────────────────────
    {"bg": "bureau", "rain": True, "transition": "slide_left",
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. Je sais qu'il est minuit passé. Je sais que vous ne dormez pas. Je sais aussi que vous êtes en train de vous faire du mal tout seul dans votre bureau. Arrêtez."},

    {"bg": "bureau", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous m'appelez pour me dire d'arrêter. C'est touchant, Sato."},

    {"bg": "bureau", "rain": True,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Je vous appelle parce que ma fille a demandé qui était le monsieur avec le chapeau qui était venu nous voir. Je lui ai dit que c'était un ami. Elle a dit qu'il avait l'air triste."},

    {"bg": "bureau", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Les enfants ont un radar pour ça."},

    {"bg": "bureau", "rain": True,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Elle m'a aussi demandé si le monsieur triste allait aller mieux. J'ai dit oui. Ne me faites pas mentir à ma fille, Raven."},

    {"bg": "bureau", "rain": True,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je vais faire de mon mieux. C'est tout ce que je peux promettre."},

    {"bg": "bureau", "rain": True,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Elle m'a aussi demandé si le monsieur avec le chapeau était un héros. Je lui ai dit que les héros ça n'existe pas dans la vraie vie. Elle m'a dit que je me trompais."},

    {"bg": "bureau", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Votre fille est plus intelligente que nous deux réunis."},

    {"bg": "bureau", "rain": True,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Oui. C'est ce qui m'inquiète le plus pour son avenir. Bonne nuit, Raven. Et dormez."},

    # ── ACTE 3 Ch3-C : Raven, l'aube, résolution ──────────────────────────────
    {"bg": "bureau", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "5h23. La pluie s'est arrêtée. La fenêtre est toujours ouverte. Quelque chose s'est changé dans l'air — cette légèreté particulière qui précède l'aube, comme si la nuit reprenait son souffle."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mon père disait que la vérité n'a pas besoin d'être défendue. Elle a besoin d'être dite. Si tu la dis assez fort, assez souvent, à assez de personnes, elle finit par tenir debout toute seule."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je pense qu'il avait tort. La vérité ne tient debout que si quelqu'un la soutient. Et parfois, ce quelqu'un paie pour ça. Il l'a payé. Marcus Vane l'a payé."},

    {"bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La question n'est pas de savoir si ça vaut le prix. La question est de savoir si quelqu'un est prêt à le payer. Et depuis Genève, depuis cette nuit dans la ruelle, j'ai ma réponse."},

    {"bg": "toit", "rain": False, "transition": "fade_white",
     "char": None, "side": "left",
     "name": "",
     "text": "Le toit de mon immeuble. Je monte rarement. Ce matin, je monte. Paris s'étale sous la lumière naissante — grise, froide, belle comme seules les villes épuisées peuvent être belles."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je ne suis pas un héros. Je suis quelqu'un qui ne sait pas s'arrêter. C'est peut-être la même chose. C'est peut-être très différent. Je m'en fiche."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il reste un Architecte en liberté. Un Fantôme quelque part en Europe. Un sénateur qui vote des lois dans un parlement que je n'ai pas encore trouvé comment toucher. Et moi, sur ce toit, avec un café froid."},

    {"bg": "toit", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "C'est suffisant pour commencer. C'est toujours suffisant pour commencer."},

    # ── Marqueur fin Ch3-C → transition vers Ch4 ──────────────────────────────
    {"bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "─── FIN DU CHAPITRE III-C ───"},

    {"chapter_end": 3, "bg": "toit", "char": None, "side": "left",
     "name": "", "text": ""},
]

# ═══════════════════════════════════════════════════════════════════════════════
# NUIT SANS TÉMOIN — script_extension_ch4567.py
# Extensions Chapitres IV, V, VI & VII — 40+ nœuds par chapitre
# Interrogatoires structurés, choix relationnels, déductions, ancrage émotionnel
# ═══════════════════════════════════════════════════════════════════════════════
#
# CONVENTIONS :
#   type: "interrogation"  → mini-jeu interrogatoire (géré par interrogation.py)
#   "rel_choice"           → choix à impact relationnel (modifie réputation)
#   "deduction"            → nœud de déduction (combine preuves)
#   "note"         → entrée automatique dans le journal de Raven
#   rep_change             → dict {perso: delta}
#   time                   → horloge diégétique HH:MM
#
# USAGE :
#   Ajouter en bas de script.py :
#     SCRIPT_EXT_CH4567 = SCRIPT_IV_EXT + SCRIPT_V_EXT + SCRIPT_VI_EXT + SCRIPT_VII_EXT
#     SCRIPT = SCRIPT + SCRIPT_EXT_CH4567
# ═══════════════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════
# CHAPITRE IV — Extensions (~48 nœuds)
# Interrogatoires : Mira (approfondi), l'archiviste, l'homme du train
# Choix relationnels : Sato / Mira / Natasha
# ══════════════════════════════════════════════════════════════════════

SCRIPT_IV_EXT = [

    # ─── ACTE 0 : Retombées de Genève ───────────────────────────────────────────

    {"id": "ch4_ext_00",
     "bg": "appartement", "rain": False, "transition": "fade_black",
     "time": "07:15",
     "char": None, "side": "left",
     "name": "",
     "text": "CHAPITRE IV — Extension : L'Héritage (approfondissement)"},

    {"id": "ch4_ext_01",
     "bg": "appartement", "rain": False,
     "time": "07:15",
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Six mois. Ferrière est en préventive. L'Architecte a disparu de sa cellule en quarante-cinq minutes chrono. Quarante-cinq. Quelqu'un a eu ce temps pour ouvrir une porte sécurisée."},

    {"id": "ch4_ext_02",
     "bg": "appartement", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Interpol parle de 'fuite organisée de l'intérieur'. Sato parle de 'procédure en cours'. Moi, j'appelle ça ce que c'est : il y a encore au moins un homme à eux dans la hiérarchie policière."},

    {"id": "ch4_ext_03",
     "bg": "appartement", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "note": "L'Architecte libre. Source interne confirmée. Chercher qui a autorisé le transfert sans escorte.",
     "text": "J'ai noté ça dans le journal. Pas pour moi — pour la trace. Un vieux réflexe de flic que je n'ai jamais réussi à perdre."},

    # ─── Interrogatoire : Taro, reprise de contact ──────────────────────────────

    {"id": "ch4_ext_04",
     "bg": "salle_interrogatoire", "rain": False, "transition": "iris",
     "time": "11:00",
     "char": "taro", "expr": 1, "side": "right",
     "name": "TARO MITSUKI",
     "text": "Raven. Vous n'êtes pas censé me contacter. Ferrière avait mes coordonnées. Si ses amis ont récupéré son téléphone..."},

    {"id": "ch4_ext_05",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "J'ai appelé depuis une cabine. Il en reste une au boulevard de Clichy. Les vieux réflexes ont du bon."},

    {"id": "ch4_ext_06",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "taro", "expr": 0, "side": "right",
     "name": "TARO MITSUKI",
     "text": "Qu'est-ce que vous voulez savoir que vous ne savez pas déjà ?"},

    # ── Choix d'interrogatoire Taro ──────────────────────────────────────────────
    {"id": "ch4_ext_07",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "",
     "text": "Taro sait quelque chose sur la fuite de l'Architecte. Il choisit ses mots avec soin. Comment l'amener à parler ?",
     "choices": [
         "Lui rappeler ce qu'il nous doit — il a survécu grâce à notre silence",
         "Lui proposer une protection formelle — en faire un témoin officiel",
         "Ne rien demander directement — attendre qu'il donne ce qu'il veut donner"
     ],
     "choice_branch": {"0": "ch4_taro_pression", "1": "ch4_taro_officiel", "2": "ch4_taro_attente"}},

    # ── Branche : Pression ─────────────────────────────────────────────────────
    {"id": "ch4_taro_pression",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"taro": -10},
     "text": "Il y a six mois, j'aurais pu transmettre votre nom à Ferrière. Je ne l'ai pas fait. Cette dette ne se prescrit pas."},

    {"id": "ch4_taro_pression_2",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "taro", "expr": 3, "side": "right",
     "name": "TARO MITSUKI",
     "text": "...C'est la première fois que vous utilisez ça contre moi. Je vois. Bien. Le transfert de l'Architecte — la voiture qui le conduisait était réquisitionnée sous un faux bon de commande. Signé par quelqu'un de la Direction."},

    {"id": "ch4_taro_pression_3",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "J'entends l'amertume dans sa voix. Je n'aurais pas dû utiliser ça. Mais il a parlé. Et l'info tient."},

    # ── Branche : Protection officielle ───────────────────────────────────────
    {"id": "ch4_taro_officiel",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"taro": 15},
     "text": "Sato peut vous sortir du registre actif. Nouveau nom, nouvelle ville si vous voulez. Mais pour ça, il faut un vrai témoignage. Pas des rumeurs. Des faits."},

    {"id": "ch4_taro_officiel_2",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "taro", "expr": 2, "side": "right",
     "name": "TARO MITSUKI",
     "text": "Vous me proposez ça pour de vrai ? Raven... Je vais réfléchir. Mais voici ce que je peux vous donner gratuitement, maintenant : le bon de commande de la voiture était signé 'Commandant Bertier'. Ce nom n'existe pas à la Préfecture."},

    {"id": "ch4_taro_officiel_3",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un nom fantôme. Encore. Ils ont leur propre répertoire de fausses identités à l'intérieur des services. C'est plus profond que ce qu'on pensait.",
     "evidence": ("Bon de commande — Bertier", "Fausse identité dans les services — transfert Architecte autorisé")},

    # ── Branche : Attente passive ──────────────────────────────────────────────
    {"id": "ch4_taro_attente",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"taro": 5},
     "text": "Je ne dis rien. Je pose mon café sur la table. Je regarde par la fenêtre. Taro déteste le silence. Toujours."},

    {"id": "ch4_taro_attente_2",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "taro", "expr": 1, "side": "right",
     "name": "TARO MITSUKI",
     "text": "...Vous faites quoi, là ? Vous dormez les yeux ouverts ou quoi ? Bon. Très bien. Le chauffeur qui conduisait la voiture de transfert — il s'appelle Rémi Cazes. Il a arrêté de répondre au téléphone il y a trois semaines."},

    {"id": "ch4_taro_attente_3",
     "bg": "salle_interrogatoire", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Cazes. Disparu ou effacé. La Synarchie nettoie ses outils après utilisation. Ce homme sait trop. S'il est encore vivant, c'est parce qu'ils n'ont pas encore trouvé où il se cache.",
     "evidence": ("Chauffeur Cazes", "Dernier lien vivant avec la fuite de l'Architecte — localisation inconnue")},

    # ─── Interrogatoire structuré : Mira (profondeur) ───────────────────────────

    {"id": "ch4_ext_mira_00",
     "bg": "parking", "rain": False, "transition": "fade_black",
     "time": "18:30",
     "char": "mira", "expr": 0, "side": "right",
     "name": "MIRA VOSS",
     "text": "Je vous ai tout dit sur les archives. Mais vous continuez à me regarder comme si j'avais une deuxième couche à éplucher."},

    {"id": "ch4_ext_mira_01",
     "bg": "parking", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Tout le monde a une deuxième couche. C'est un fait humain. Ce qui varie, c'est si cette couche est dangereuse ou non."},

    # ── Mini-jeu interrogatoire Mira ─────────────────────────────────────────
    {"id": "ch4_interro_mira",
     "type": "interrogation",
     "suspect": "mira",
     "time_limit": 120,
     "on_success": "ch4_mira_ok",
     "on_failure": "ch4_mira_fail"},

    {"id": "ch4_mira_ok",
     "bg": "parking", "rain": False,
     "char": "mira", "expr": 3, "side": "right",
     "name": "MIRA VOSS",
     "rep_change": {"mira": 20},
     "text": "Bien. Vous avez trouvé la fissure. Les dix-huit mois. Je n'étais pas en protection. J'étais en infiltration. La DGSI m'avait envoyée dans le réseau pour documenter de l'intérieur. J'ai rempli ma mission. Et ils m'ont coupée."},

    {"id": "ch4_mira_ok_2",
     "bg": "parking", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Infiltrée. Dans la Synarchie. Vous avez été à l'intérieur pendant dix-huit mois."},

    {"id": "ch4_mira_ok_3",
     "bg": "parking", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "Sous couverture. Un poste d'analyste contractuelle dans une filiale de l'Institut Voss. J'ai vu comment ils fonctionnent de l'intérieur. Comment ils recrutent. Comment ils effacent les gens."},

    {"id": "ch4_mira_ok_4",
     "bg": "parking", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Et quand ils vous ont licenciée, c'était parce qu'ils avaient découvert que vous étiez infiltrée ?"},

    {"id": "ch4_mira_ok_5",
     "bg": "parking", "rain": False,
     "char": "mira", "expr": 4, "side": "right",
     "name": "MIRA VOSS",
     "text": "Non. Ils ne l'ont jamais su. Ils m'ont licenciée parce qu'Arnheim a jugé que j'avais posé de trop bonnes questions sur les comptes lettons. Ironie : ils m'ont chassée avant que je puisse les trahir.",
     "evidence": ("Couverture Mira — 18 mois", "Infiltration confirmée — DGSI — données internes Synarchie")},

    {"id": "ch4_mira_fail",
     "bg": "parking", "rain": False,
     "char": "mira", "expr": 0, "side": "right",
     "name": "MIRA VOSS",
     "text": "Je vous ai dit ce que j'avais à dire. Si vous cherchez à me déstabiliser avec des questions en miroir, vous perdez votre temps. J'ai été formée à ça aussi."},

    {"id": "ch4_mira_fail_2",
     "bg": "parking", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Elle tient. Soit elle dit vrai, soit elle est très bien préparée. Dans les deux cas, elle ne fléchit pas. Je note l'opacité et j'avance."},

    # ─── Moment relationnel : Raven et Sato ──────────────────────────────────────

    {"id": "ch4_ext_rel_sato_00",
     "bg": "bureau", "rain": True, "transition": "fade_black",
     "time": "22:45",
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. Vous avez mangé aujourd'hui ?"},

    {"id": "ch4_ext_rel_sato_01",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "J'ai eu un café à 11h et deux biscuits qui traînaient depuis la semaine dernière. C'est nutritif."},

    {"id": "ch4_ext_rel_sato_02",
     "bg": "bureau", "rain": True,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "C'est pathétique. J'ai des restes dans une boîte. Je vous les apporte. Et vous allez les manger."},

    # ── Choix relationnel Sato ────────────────────────────────────────────────
    {"id": "ch4_ext_rel_sato_03",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "",
     "text": "Sato propose quelque chose de simple. Un geste qui dit : je vous vois, pas seulement le dossier. Comment répondre ?",
     "choices": [
         "Accepter — et reconnaître qu'on a besoin l'un de l'autre",
         "Refuser poliment — garder la distance professionnelle",
         "Détourner — parler du dossier pour esquiver le reste"
     ],
     "choice_branch": {"0": "ch4_sato_accept", "1": "ch4_sato_refuse", "2": "ch4_sato_esquive"}},

    {"id": "ch4_sato_accept",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"sato": 15},
     "text": "Oui. Merci. Ce n'est pas souvent que quelqu'un me demande ça. Apportez ce que vous avez. Et si vous voulez, racontez-moi quelque chose qui n'a rien à voir avec la Synarchie."},

    {"id": "ch4_sato_accept_2",
     "bg": "bureau", "rain": True,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Ma fille a remporté un concours de dessin cette semaine. Elle a peint un chien avec six pattes parce que, je cite, 'les chiens normaux c'est ennuyeux'. Médaille d'or de l'originalité discutable."},

    {"id": "ch4_sato_accept_3",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 2, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Six pattes. Elle a raison, c'est plus stable. Si je renaissais en chien, je voudrais six pattes. Juste pour l'efficacité."},

    {"id": "ch4_sato_refuse",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"sato": -5},
     "text": "Non. Je gère. Vous n'avez pas à vous occuper de mes habitudes alimentaires. Concentrons-nous sur Cazes."},

    {"id": "ch4_sato_refuse_2",
     "bg": "bureau", "rain": True,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "D'accord. Cazes. J'ai retrouvé une transaction à son nom il y a dix jours. Un loyer payé en liquide. Rue de Ménilmontant. Il est toujours à Paris."},

    {"id": "ch4_sato_esquive",
     "bg": "bureau", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Cazes. Si il est encore vivant, il est peut-être la clé du bon de commande. Vous avez une adresse ?"},

    {"id": "ch4_sato_esquive_2",
     "bg": "bureau", "rain": True,
     "char": "policiere", "expr": 0, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "...Vous avez une façon de ne jamais répondre à ce qui n'est pas une question de dossier, vous savez ça ? Rue de Ménilmontant. J'apporte les restes quand même."},

    # ─── Interrogatoire : Rémi Cazes ──────────────────────────────────────────

    {"id": "ch4_ext_cazes_00",
     "bg": "appartement", "rain": False, "transition": "slide_left",
     "time": "14:00",
     "char": None, "side": "left",
     "name": "",
     "text": "Ménilmontant. Immeuble des années 70. Boîte aux lettres au nom de 'R. Cazes'. Il est là."},

    {"id": "ch4_ext_cazes_01",
     "bg": "appartement", "rain": False,
     "char": "taro", "expr": 0, "side": "right",
     "name": "RÉMI CAZES",
     "text": "Qui êtes-vous ? Je vais crier."},

    {"id": "ch4_ext_cazes_02",
     "bg": "appartement", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Non, vous n'allez pas crier. Vous allez me faire entrer. Parce que si vous criez, les deux hommes qui surveillent votre immeuble depuis ce matin entendent aussi."},

    {"id": "ch4_ext_cazes_03",
     "bg": "appartement", "rain": False,
     "char": "taro", "expr": 3, "side": "right",
     "name": "RÉMI CAZES",
     "text": "...Comment vous savez pour eux ?"},

    {"id": "ch4_ext_cazes_04",
     "bg": "appartement", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je les surveille depuis une heure. Ils ne savent pas que je suis là. Mais dans vingt minutes, leur relève arrive. C'est maintenant ou c'est trop tard."},

    # ── Mini-jeu interrogatoire Cazes ─────────────────────────────────────────
    {"id": "ch4_interro_cazes",
     "type": "interrogation",
     "suspect": "taro",
     "time_limit": 90,
     "on_success": "ch4_cazes_ok",
     "on_failure": "ch4_cazes_fail"},

    {"id": "ch4_cazes_ok",
     "bg": "appartement", "rain": False,
     "char": "taro", "expr": 1, "side": "right",
     "name": "RÉMI CAZES",
     "text": "Le bon de commande... c'était Ferrière qui me l'a donné. Mais il y avait une deuxième signature. Quelqu'un que j'avais jamais vu. Une femme. Brune, quarantaine, badge de la Direction des Affaires Spéciales."},

    {"id": "ch4_cazes_ok_2",
     "bg": "appartement", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Une femme. Direction des Affaires Spéciales. C'est une unité qui n'est pas censée intervenir dans les transferts de détenus."},

    {"id": "ch4_cazes_ok_3",
     "bg": "appartement", "rain": False,
     "char": "taro", "expr": 1, "side": "right",
     "name": "RÉMI CAZES",
     "text": "Elle a dit que c'était 'une procédure parallèle'. Moi j'ai juste conduit. Je savais pas ce que j'emmenais. Enfin... j'aurais dû m'en douter. Mais j'ai conduit.",
     "evidence": ("Deuxième signature — DAS", "Femme inconnue — Direction Affaires Spéciales — complice fuite Architecte")},

    {"id": "ch4_cazes_fail",
     "bg": "appartement", "rain": False,
     "char": "taro", "expr": 1, "side": "right",
     "name": "RÉMI CAZES",
     "text": "J'ai rien fait de mal. J'ai suivi des ordres signés. Si quelque chose de pas légal s'est passé, je suis pas au courant. Partez."},

    {"id": "ch4_cazes_fail_2",
     "bg": "appartement", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il ne cède pas. Peut-être trop peur. Peut-être vraiment innocent des détails. Dans les deux cas, je n'ai pas le temps. Je laisse ma carte et je sors avant la relève."},

    # ─── Déduction : Photo + Badge ────────────────────────────────────────────

    {"id": "ch4_ext_deduction_01",
     "bg": "bureau", "rain": False, "transition": "fade_black",
     "time": "23:00",
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Photo de surveillance + Badge magnétique. La photo montre quelqu'un qui connaît les angles morts de mon appartement. Le badge montre un accès Parlement. Ce ne sont pas deux opérations distinctes. C'est une surveillance institutionnelle."},

    {"id": "ch4_ext_deduction_02",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "evidence": ("Déduction : Surveillance institutionnelle", "Photo + Badge → quelqu'un du Parlement me surveille depuis l'intérieur"),
     "text": "Quelqu'un du Parlement m'a mis sous surveillance avant que je ne sache que le Parlement était impliqué. Ils me regardaient venir."},

    # ─── Déduction : Clé USB #2 + Fichiers Synarchie ──────────────────────────

    {"id": "ch4_ext_deduction_03",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Clé USB #2 + Fichiers Synarchie Ch1. Le modèle est identique. Vane utilisait ce modèle comme standard. La personne qui m'a envoyé la clé #2 était dans le réseau de Vane. Ou avait accès à son matériel."},

    {"id": "ch4_ext_deduction_04",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "evidence": ("Déduction : Le successeur prévu", "Clé USB #2 → même réseau que Vane → quelqu'un continue son travail"),
     "text": "Vane avait prévu sa propre mort. Et il avait prévu quelqu'un pour continuer. Ce successeur m'a contacté. La question est : est-ce Mira ? Ou quelqu'un d'autre que je n'ai pas encore vu ?"},

    # ─── Moment relationnel : Raven et Natasha ───────────────────────────────

    {"id": "ch4_ext_rel_natasha_00",
     "bg": "rue", "rain": True, "transition": "slide_left",
     "time": "16:00",
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Mon rédacteur en chef veut que je mette ce dossier en pause. Il dit que les pressions juridiques de Selg mettent le journal en danger. Il a raison. Je vais continuer quand même."},

    {"id": "ch4_ext_rel_natasha_01",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ce n'est pas une décision anodine. Si votre journal vous lâche, vous n'avez plus de couverture légale."},

    {"id": "ch4_ext_rel_natasha_02",
     "bg": "rue", "rain": True,
     "char": "natasha", "expr": 2, "side": "right",
     "name": "NATASHA MORI",
     "text": "Je sais. J'ai des copies chez trois confrères à l'étranger. Et je travaille sous protection de source. C'est prévu depuis le début."},

    # ── Choix relationnel : Natasha ────────────────────────────────────────────
    {"id": "ch4_ext_rel_natasha_03",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "",
     "text": "Natasha a tout risqué pour ce dossier. Ce qu'elle vient de dire mérite une réponse vraie — pas juste professionnelle.",
     "choices": [
         "Lui dire ce qu'on pense vraiment — elle a le droit de savoir le niveau de danger",
         "La rassurer — minimiser les risques pour qu'elle continue",
         "Lui proposer une sortie — elle n'est pas obligée d'aller jusqu'au bout"
     ],
     "choice_branch": {"0": "ch4_natasha_vrai", "1": "ch4_natasha_rassure", "2": "ch4_natasha_sortie"}},

    {"id": "ch4_natasha_vrai",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"natasha": 20},
     "text": "Le niveau de danger est élevé. Très élevé. Ils ont saboté votre voiture à un moment où vous n'aviez rien publié encore. Maintenant vous êtes sur leurs écrans en permanence."},

    {"id": "ch4_natasha_vrai_2",
     "bg": "rue", "rain": True,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Je sais. Merci de ne pas me l'avoir caché. C'est ce que les gens font d'habitude — ils édulcorent pour me protéger. Je préfère savoir ce dans quoi je suis."},

    {"id": "ch4_natasha_vrai_3",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous et Sato. Vous méritez toutes les deux mieux que mes instincts de protection maladroits."},

    {"id": "ch4_natasha_rassure",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"natasha": -5},
     "text": "Selg est acculé. Les menaces juridiques, c'est le signe qu'il n'a plus les moyens de l'extrajudiciaire. Vous êtes moins en danger maintenant qu'il y a six mois."},

    {"id": "ch4_natasha_rassure_2",
     "bg": "rue", "rain": True,
     "char": "natasha", "expr": 3, "side": "right",
     "name": "NATASHA MORI",
     "text": "C'est gentil de me dire ça. C'est aussi faux. Mais c'est gentil."},

    {"id": "ch4_natasha_sortie",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"natasha": 10},
     "text": "Vous n'avez pas à aller jusqu'au bout. Vous avez déjà publié plus que la plupart. Ce que vous avez fait compte. La suite, d'autres peuvent la prendre."},

    {"id": "ch4_natasha_sortie_2",
     "bg": "rue", "rain": True,
     "char": "natasha", "expr": 2, "side": "right",
     "name": "NATASHA MORI",
     "text": "Je sais que vous pensez ça sincèrement. Mais non. C'est mon histoire autant que la vôtre. J'y suis depuis le début. Je finis ce que j'ai commencé."},

    # ─── Épilogue étendu Ch4 ──────────────────────────────────────────────────

    {"id": "ch4_ext_epilogue_00",
     "bg": "toit", "rain": False, "transition": "fade_black",
     "time": "03:20",
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Récapitulatif de nuit. Cazes a confirmé une deuxième signature sur le bon de commande. Une femme. DAS. Je ne sais pas encore qui c'est."},

    {"id": "ch4_ext_epilogue_01",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mira a été infiltrée dans la Synarchie. Dix-huit mois. Ce qu'elle a vu de l'intérieur est précieux. Ce qu'elle n'a pas vu l'est peut-être encore plus."},

    {"id": "ch4_ext_epilogue_02",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je pense à Vane. Il a mis dix ans à préparer sa propre mort. À encoder les preuves. À choisir le format de la clé USB. Il savait que quelqu'un arriverait. Il savait que ce serait quelqu'un comme moi."},

    {"id": "ch4_ext_epilogue_03",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "note": "Marcus Vane savait. Tout. Depuis dix ans. Il n'a pas fui parce qu'il espérait que quelqu'un récupère le flambeau après lui.",
     "text": "C'est peut-être la chose la plus triste et la plus digne que quelqu'un puisse faire. Préparer la suite pour qu'elle existe même si on n'est plus là pour la voir."},

    {"id": "ch4_ext_epilogue_04",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je ne veux pas finir dans une ruelle. Mais si c'est le cas — au moins que quelqu'un arrive après. C'est tout ce qu'on peut espérer dans ce métier."},

    {"id": "ch4_ext_fin",
     "bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "─── FIN DU CHAPITRE IV — EXTENSION ───"},
]


# ══════════════════════════════════════════════════════════════════════
# CHAPITRE V — Extensions (~45 nœuds)
# Interrogatoires : le contact anonyme, Viktor Selg (face-à-face), le serveur
# Choix relationnels : Mira (les 18 mois), Sato (la décision), l'équipe Berlin
# ══════════════════════════════════════════════════════════════════════

SCRIPT_V_EXT = [

    # ─── ACTE 0 : Le train, la nuit avant Berlin ──────────────────────────────

    {"id": "ch5_ext_00",
     "bg": "train", "rain": True, "transition": "fade_black",
     "time": "23:47",
     "char": None, "side": "left",
     "name": "",
     "text": "CHAPITRE V — Extension : Le Fantôme (approfondissement)"},

    {"id": "ch5_ext_01",
     "bg": "train", "rain": True,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le train roule. Compartiment seul. Verre de whisky que je n'ai pas bu depuis vingt minutes. Ce genre de nuit, je lis les dossiers jusqu'à ce que les lettres se mettent à bouger."},

    {"id": "ch5_ext_02",
     "bg": "train", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je pense à la première conversation avec Taro, il y a presque un an. 'Ces gens ne jouent pas.' Il avait raison. Et moi je jouais à quoi au juste ?"},

    {"id": "ch5_ext_03",
     "bg": "train", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Au policier qui peut encore changer les choses. C'est naïf. Mais c'est le seul moteur que j'ai. Les moteurs naïfs tiennent souvent plus longtemps que les autres."},

    # ─── Interrogatoire : le contact anonyme ──────────────────────────────────

    {"id": "ch5_ext_contact_00",
     "bg": "hotel_berlin", "rain": False, "transition": "iris",
     "time": "23:00",
     "char": "ghost", "expr": 0, "side": "right",
     "name": "LE CONTACT",
     "text": "Vous avez l'habitude de rencontrer des gens dans des hôtels à minuit ?"},

    {"id": "ch5_ext_contact_01",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "C'est mon horaire de travail habituel. Vous avez dit que vous connaissiez le vrai nom du Fantôme. Prouvez-le."},

    # ── Choix d'interrogatoire : Contact anonyme ──────────────────────────────
    {"id": "ch5_ext_contact_choix",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "",
     "text": "Cet homme veut sortir. Il a quelque chose. Mais il n'est pas venu par amour de la justice. Comment lire ses motivations ?",
     "choices": [
         "L'attaquer directement — chercher à le déstabiliser pour voir sa réaction",
         "Jouer la compréhension — lui montrer qu'on comprend sa position",
         "Le laisser diriger — voir où il veut en venir avant d'intervenir"
     ],
     "choice_branch": {"0": "ch5_contact_attaque", "1": "ch5_contact_empathie", "2": "ch5_contact_attente"}},

    {"id": "ch5_contact_attaque",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous travaillez pour Selg depuis combien de temps ? Et qu'est-ce qui vous a fait décider que le bon moment pour trahir, c'était maintenant et pas il y a dix ans ?"},

    {"id": "ch5_contact_attaque_2",
     "bg": "hotel_berlin", "rain": False,
     "char": "ghost", "expr": 3, "side": "right",
     "name": "LE CONTACT",
     "text": "Vingt-deux ans. Et ce qui a tout changé : le vol 219. Je savais pour les morts. Je n'avais pas compris jusqu'à combien ils iraient. Cent quarante-sept. C'est un nombre que je ne peux pas continuer à porter."},

    {"id": "ch5_contact_attaque_3",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Cent quarante-sept. Et il a fallu dix ans pour que ce nombre devienne insupportable. Mais je ne dis rien. Ce n'est pas le moment d'être juge."},

    {"id": "ch5_contact_empathie",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"ghost_contact": 15},
     "text": "Vous êtes venu ici seul. Vous avez pris le risque de me contacter. Ça, c'est déjà une décision difficile. Je vous écoute à votre rythme."},

    {"id": "ch5_contact_empathie_2",
     "bg": "hotel_berlin", "rain": False,
     "char": "ghost", "expr": 1, "side": "right",
     "name": "LE CONTACT",
     "text": "Le vol 219. J'ai vu les listes de passagers avant le départ. J'ai reconnu deux des noms — des gens qui auraient dû vivre. Et j'ai fermé les yeux. C'est ça que je ne supporte plus."},

    {"id": "ch5_contact_empathie_3",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il ne cherche pas l'absolution. Il cherche juste à que quelque chose change grâce à ce qu'il sait. C'est une motivation que je comprends."},

    {"id": "ch5_contact_attente",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je ne dis rien. Je sors les photos du serveur de Berlin. Je les pose sur la table sans commentaire."},

    {"id": "ch5_contact_attente_2",
     "bg": "hotel_berlin", "rain": False,
     "char": "ghost", "expr": 3, "side": "right",
     "name": "LE CONTACT",
     "text": "Vous avez déjà trouvé le serveur. Selg ne le sait pas encore. Dans ce cas... il faut que je vous dise quelque chose. Quelque chose que même le serveur ne contient pas."},

    {"id": "ch5_contact_attente_3",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Silence et patience — les seuls outils qui n'ont jamais déçu."},

    # ─── Suite : révélation du contact ────────────────────────────────────────

    {"id": "ch5_ext_contact_rev_00",
     "bg": "hotel_berlin", "rain": False,
     "char": "ghost", "expr": 1, "side": "right",
     "name": "LE CONTACT",
     "text": "Le vote au Parlement. La date que vous cherchez. Le 14 juin. Mais ce n'est pas un vote. C'est une confirmation. La réforme a déjà été approuvée en sous-main par neuf des douze États."},

    {"id": "ch5_ext_contact_rev_01",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Déjà approuvée. Le vote est une mise en scène. Une formalité publique pour légitimer ce qui est déjà décidé."},

    {"id": "ch5_ext_contact_rev_02",
     "bg": "hotel_berlin", "rain": False,
     "char": "ghost", "expr": 1, "side": "right",
     "name": "LE CONTACT",
     "text": "Trois chefs d'État ont signé sous pression. Des dossiers compromettants. Selg les a depuis dix ans. C'est son assurance vie et son levier simultanément.",
     "evidence": ("Accord de Berlin — Chantage institutionnel", "Selg détient dossiers sur 3 chefs d'État — signatures extorquées")},

    {"id": "ch5_ext_contact_rev_03",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ce n'est plus de la corruption. C'est du chantage d'État. À l'échelle de trois gouvernements."},

    # ─── Moment relationnel : Mira — les 18 mois ──────────────────────────────

    {"id": "ch5_ext_rel_mira_00",
     "bg": "hotel_berlin", "rain": False, "transition": "fade_black",
     "time": "01:30",
     "char": "mira", "expr": 0, "side": "right",
     "name": "MIRA VOSS",
     "text": "Vous n'avez pas dormi. Et vous continuez à me regarder comme si j'avais quelque chose à vous donner que je n'ai pas encore donné."},

    {"id": "ch5_ext_rel_mira_01",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Dans ces dix-huit mois d'infiltration — vous avez rencontré Selg ?"},

    {"id": "ch5_ext_rel_mira_02",
     "bg": "hotel_berlin", "rain": False,
     "char": "mira", "expr": 4, "side": "right",
     "name": "MIRA VOSS",
     "text": "Une fois. À une réunion de la commission consultative. Il était présenté sous un autre nom. Mais j'ai reconnu sa façon de parler — cette précision chirurgicale dans les mots. Comme si chaque phrase était une pièce dans un mécanisme."},

    {"id": "ch5_ext_rel_mira_03",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il vous a regardée ?"},

    {"id": "ch5_ext_rel_mira_04",
     "bg": "hotel_berlin", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "Il regarde tout le monde de la même façon. Avec un intérêt poli qui cache une évaluation constante. Il calcule les utilités. Vous aussi il l'a fait avec vous, vous savez."},

    # ── Choix relationnel : comprendre Mira ───────────────────────────────────
    {"id": "ch5_ext_rel_mira_choix",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "",
     "text": "Mira parle de Selg avec une précision qui vient de la proximité. Elle le connaît d'une façon que je ne connais pas. Comment naviguer dans cette conversation ?",
     "choices": [
         "Lui demander comment elle s'en est sortie psychologiquement — 18 mois c'est long",
         "Se concentrer sur le renseignement — ce qu'elle a vu qui peut être utile maintenant",
         "Lui dire qu'on lui fait confiance, sans condition"
     ],
     "choice_branch": {"0": "ch5_mira_psy", "1": "ch5_mira_intel", "2": "ch5_mira_trust"}},

    {"id": "ch5_mira_psy",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"mira": 15},
     "text": "Dix-huit mois à jouer un rôle chez des gens qui tuent. Comment on revient de ça ? Est-ce qu'on revient ?"},

    {"id": "ch5_mira_psy_2",
     "bg": "hotel_berlin", "rain": False,
     "char": "mira", "expr": 4, "side": "right",
     "name": "MIRA VOSS",
     "text": "On ne revient pas. On devient quelqu'un qui a fait ça. Et qui vit avec. Certains jours c'est acceptable. D'autres c'est... moins. Mais vous ne voulez pas vraiment entendre ça maintenant."},

    {"id": "ch5_mira_psy_3",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Si. Je le veux. Pas parce que c'est utile pour l'enquête. Parce que c'est important de savoir à qui on demande de prendre des risques."},

    {"id": "ch5_mira_psy_4",
     "bg": "hotel_berlin", "rain": False,
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "...C'est la première fois depuis un an que quelqu'un me dit ça. Merci. Maintenant on peut parler de Selg si vous voulez."},

    {"id": "ch5_mira_intel",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Les réunions de la commission. Quels étaient les sujets qui revenaient systématiquement ? Qu'est-ce qui les obsédait ?"},

    {"id": "ch5_mira_intel_2",
     "bg": "hotel_berlin", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "Deux obsessions : la date du vote et l'exposition médiatique. Ils avaient une peur panique que quelqu'un publie avant le 14 juin. Tout le reste était secondaire.",
     "evidence": ("Obsession date vote — Synarchie", "14 juin est la date limite absolue — après, le vote est irréversible")},

    {"id": "ch5_mira_trust",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"mira": 25},
     "text": "Mira. Je vous fais confiance. Sans condition, sans réserve, et sans avoir besoin de comprendre les dix-huit mois dans le détail. Ce que vous avez fait, vous l'avez fait."},

    {"id": "ch5_mira_trust_2",
     "bg": "hotel_berlin", "rain": False,
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "Raven... personne ne m'a jamais dit quelque chose comme ça aussi directement. C'est presque déstabilisant."},

    {"id": "ch5_mira_trust_3",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Habituez-vous. On va finir ce dossier ensemble et j'ai besoin que vous soyez là jusqu'au bout."},

    # ─── Face-à-face avec Viktor Selg (interrogatoire diplomatique) ───────────

    {"id": "ch5_ext_selg_00",
     "bg": "parlement", "rain": False, "transition": "iris",
     "time": "10:30",
     "char": "ghost", "expr": 0, "side": "right",
     "name": "VIKTOR SELG",
     "text": "Raven. Vous vous promenez dans une conférence diplomatique sans invitation. C'est techniquement une violation du protocole de sécurité internationale."},

    {"id": "ch5_ext_selg_01",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 8, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Heureusement que je ne travaille plus pour l'État. Les violations de protocole sont mon domaine de prédilection."},

    # ── Mini-jeu interrogatoire Selg ──────────────────────────────────────────
    {"id": "ch5_interro_selg",
     "type": "interrogation",
     "suspect": "ghost",
     "time_limit": 120,
     "on_success": "ch5_selg_ok",
     "on_failure": "ch5_selg_fail"},

    {"id": "ch5_selg_ok",
     "bg": "parlement", "rain": False,
     "char": "ghost", "expr": 3, "side": "right",
     "name": "VIKTOR SELG",
     "text": "Vous avez trouvé la fissure. Impressionnant. Oui. La femme de la DAS — c'est moi qui l'ai nommée. Votre Commandant Bertier, c'est Élise Moran. Direction des Affaires Spéciales. Elle était à moi depuis huit ans."},

    {"id": "ch5_selg_ok_2",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Élise Moran. Un nom. Une identité réelle. Pour la première fois depuis le début, vous me donnez quelque chose de vrai."},

    {"id": "ch5_selg_ok_3",
     "bg": "parlement", "rain": False,
     "char": "ghost", "expr": 2, "side": "right",
     "name": "VIKTOR SELG",
     "text": "Parce que dans dix minutes votre journaliste publie ma photo. Et Moran est la seule pièce que je peux sacrifier sans me noyer. Calculez.",
     "evidence": ("Élise Moran — DAS", "Taupe institutionnelle — 8 ans au service de Selg — fuite Architecte confirmée")},

    {"id": "ch5_selg_fail",
     "bg": "parlement", "rain": False,
     "char": "ghost", "expr": 1, "side": "right",
     "name": "VIKTOR SELG",
     "text": "Vous êtes décevant, Raven. Vraiment. J'attendais plus. Allez. Partez. Je vous reverrai à des conditions moins favorables."},

    {"id": "ch5_selg_fail_2",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il me congédie comme un stagiaire. Ce n'est pas un échec — c'est une information sur lui. Il a besoin de dominer. Ça veut dire qu'il a peur."},

    # ─── Déduction : Identité Fantôme + Accord Berlin ─────────────────────────

    {"id": "ch5_ext_deduction_00",
     "bg": "hotel_berlin", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Viktor Selg + Accord de Berlin 1994. Selg était à la table de fondation. Pas un exécutant — un co-fondateur. Il n'a pas rejoint la Synarchie. Il l'a créée avec l'Architecte."},

    {"id": "ch5_ext_deduction_01",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "evidence": ("Déduction : Le Fantôme est l'architecte adjoint", "Selg co-fondateur 1994 — opérationnel et idéologique"),
     "text": "Ce n'est pas le bras droit de l'Architecte. C'est son égal. Genève n'a éliminé qu'une moitié. Selg, c'est l'autre moitié que personne n'a vue venir."},

    # ─── Moment d'équipe : nuit avant l'opération ────────────────────────────

    {"id": "ch5_ext_team_00",
     "bg": "hotel_berlin", "rain": False, "transition": "slide_left",
     "time": "22:00",
     "char": None, "side": "left",
     "name": "",
     "text": "La chambre d'hôtel. Quatre personnes. Une bouteille d'eau plate et un plan dessiné sur du papier d'hôtel."},

    {"id": "ch5_ext_team_01",
     "bg": "hotel_berlin", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Demain, si on touche le serveur, Selg le sait dans l'heure. On a un créneau. Exactement un."},

    {"id": "ch5_ext_team_02",
     "bg": "hotel_berlin", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Mon contact à Berlin confirme que Selg part pour Vienne après-demain. Si on rate la fenêtre..."},

    {"id": "ch5_ext_team_03",
     "bg": "hotel_berlin", "rain": False,
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "On ne la rate pas. J'ai les codes d'accès du sous-sol. Ils ont changé depuis mon infiltration, mais le système de rotation est prévisible. Je peux calculer le nouveau code."},

    {"id": "ch5_ext_team_04",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "",
     "text": "Une équipe. Quatre personnes avec quatre compétences complémentaires. Et une nuit pour décider de ce qu'on fait du serveur quand on l'a.",
     "choices": [
         "Décision collective — tout le monde vote sur la stratégie",
         "Raven décide seul — prendre la responsabilité pour protéger les autres"
     ],
     "choice_branch": {"0": "ch5_team_vote", "1": "ch5_team_solo"}},

    {"id": "ch5_team_vote",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"sato": 10, "natasha": 10, "mira": 10},
     "text": "Cette décision n'est pas la mienne seule. On est quatre. On vote."},

    {"id": "ch5_team_vote_2",
     "bg": "hotel_berlin", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Conserver le serveur intact. On le protège et on s'en sert comme levier pour forcer la levée d'immunité d'Arnheim. Majorité ? Trois pour. Natasha ?"},

    {"id": "ch5_team_vote_3",
     "bg": "hotel_berlin", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Je suis pour détruire après extraction. Mais je m'incline devant la majorité. À condition qu'on ait les copies avant de sortir du sous-sol. Sinon c'est non."},

    {"id": "ch5_team_solo",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"sato": -5, "mira": -5},
     "text": "Je prends la décision. On garde le serveur intact. Si ça tourne mal, c'est sur moi. Pas sur vous."},

    {"id": "ch5_team_solo_2",
     "bg": "hotel_berlin", "rain": False,
     "char": "policiere", "expr": 3, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. On en a déjà parlé. Arrêtez de décider pour nous. Mais soit. Cette fois. Serveur conservé. Et si ça tourne mal, on en parle tous ensemble."},

    # ─── Épilogue étendu Ch5 ──────────────────────────────────────────────────

    {"id": "ch5_ext_epilogue_00",
     "bg": "hotel_berlin", "rain": False, "transition": "fade_black",
     "time": "06:15",
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Aube de Berlin. Lumière grise et froide. Dehors il y a des gens qui vont au travail, qui emmènent leurs enfants à l'école. Ils ne savent pas que dans un sous-sol de cette ville, quelqu'un vient de décider qui contrôlera leur continent."},

    {"id": "ch5_ext_epilogue_01",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Ce qui me frappe, ce n'est pas la monstruosité du plan. C'est sa banalité. Des réunions. Des comptes. Des signatures. L'Europe est en train de se faire acheter une ligne de budget à la fois."},

    {"id": "ch5_ext_epilogue_02",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "note": "Viktor Selg : co-fondateur, pas exécutant. L'Architecte était le visage. Selg est le moteur. Arnheim est la courroie de transmission.",
     "text": "Je réécris la cartographie dans ma tête. Ce n'est pas une organisation pyramidale. C'est une roue. Enlève un rayon, la roue tient. Enlève l'essieu, tout s'effondre."},

    {"id": "ch5_ext_epilogue_03",
     "bg": "hotel_berlin", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Selg est l'essieu. L'Architecte était la jante. Arnheim est les rayons. Pour casser la roue, il faut toucher l'essieu. Pas les bords."},

    {"id": "ch5_ext_fin",
     "bg": "hotel_berlin", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "─── FIN DU CHAPITRE V — EXTENSION ───"},
]


# ══════════════════════════════════════════════════════════════════════
# CHAPITRE VI — Extensions (~46 nœuds)
# Interrogatoires : Arnheim (à distance), Élise Moran, Natasha sous pression
# Choix relationnels : Mira révèle tout, Raven et la culpabilité, le plan B
# ══════════════════════════════════════════════════════════════════════

SCRIPT_VI_EXT = [

    # ─── ACTE 0 : Strasbourg, couloirs du parlement ───────────────────────────

    {"id": "ch6_ext_00",
     "bg": "parlement", "rain": False, "transition": "fade_black",
     "time": "08:00",
     "char": None, "side": "left",
     "name": "",
     "text": "CHAPITRE VI — Extension : Parlement (approfondissement)"},

    {"id": "ch6_ext_01",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Strasbourg. Je n'ai jamais aimé cette ville. Trop propre pour dissimuler quelque chose d'aussi sale. La saleté préfère le maquillage des grandes capitales."},

    {"id": "ch6_ext_02",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le Parlement. Des couloirs qui sentent la moquette neuve et l'ambition ancienne. Des badges de sécurité partout. Et quelque part dans ce bâtiment, un sénateur qui vote des lois le matin et ment au peuple l'après-midi."},

    # ─── Observation : Arnheim en coulisses ───────────────────────────────────

    {"id": "ch6_ext_arnheim_00",
     "bg": "parlement", "rain": False,
     "char": "senator", "expr": 0, "side": "right",
     "name": "SÉNATEUR ARNHEIM",
     "text": "— (Il parle à un collaborateur, ignorant qu'on l'observe) — La commission vote jeudi. Aucune fuite avant. Si Selg m'appelle encore ce soir, je décroche pas."},

    {"id": "ch6_ext_arnheim_01",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il se coupe de Selg. La panique commence à se fissurer. Quelqu'un lui a dit de prendre ses distances avec le Fantôme. Quelqu'un à l'intérieur."},

    {"id": "ch6_ext_arnheim_02",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Un sénateur qui se distance de son opérationnel trois jours avant le vote. Soit il a peur. Soit il a trouvé quelqu'un d'autre à qui parler. Et ce quelqu'un d'autre, c'est peut-être nous.",
     "evidence": ("Arnheim — rupture avec Selg", "Arnheim coupe les communications — 3 jours avant vote — signal de fragilité")},

    # ─── Interrogatoire : Élise Moran ─────────────────────────────────────────

    {"id": "ch6_ext_moran_00",
     "bg": "parking", "rain": False, "transition": "iris",
     "time": "14:30",
     "char": "mira", "expr": 3, "side": "right",
     "name": "ÉLISE MORAN — DAS",
     "text": "Comment vous avez eu cette adresse ? Je suis en protection. Il n'y a que deux personnes qui la connaissent."},

    {"id": "ch6_ext_moran_01",
     "bg": "parking", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "La troisième, c'est quelqu'un du réseau de Selg qui ne lui est plus loyal. Ça arrive, quand le bateau prend l'eau."},

    # ── Mini-jeu interrogatoire Moran ─────────────────────────────────────────
    {"id": "ch6_interro_moran",
     "type": "interrogation",
     "suspect": "mira",
     "time_limit": 100,
     "on_success": "ch6_moran_ok",
     "on_failure": "ch6_moran_fail"},

    {"id": "ch6_moran_ok",
     "bg": "parking", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "ÉLISE MORAN — DAS",
     "text": "D'accord. Je vais tout vous donner. Pas par idéalisme — parce que Selg m'a dit hier que si les choses tournaient mal, je serais la première à tomber. Vingt ans de service. Et je suis la variable d'ajustement."},

    {"id": "ch6_moran_ok_2",
     "bg": "parking", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je connais ce sentiment. Être l'outil qu'on range quand il est encombrant."},

    {"id": "ch6_moran_ok_3",
     "bg": "parking", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "ÉLISE MORAN — DAS",
     "text": "Le bon de commande. Cazes ne savait pas tout. La voiture avait un deuxième occupant. Un homme que j'avais fait entrer avec un badge de transfert médical. C'est cet homme qui a extrait l'Architecte.",
     "evidence": ("Élise Moran — témoignage complet", "Second homme — badge médical — extraction Architecte confirmée à deux agents")},

    {"id": "ch6_moran_ok_4",
     "bg": "parking", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le nom de l'homme avec le badge médical."},

    {"id": "ch6_moran_ok_5",
     "bg": "parking", "rain": False,
     "char": "mira", "expr": 0, "side": "right",
     "name": "ÉLISE MORAN — DAS",
     "text": "Stefan Krause. Médecin légiste attaché à la Préfecture. Et depuis quinze ans, membre passif de la cellule parisienne de la Synarchie.",
     "evidence": ("Stefan Krause — médecin légiste", "Membre cellule Paris — extraction Architecte — dossier à Interpol")},

    {"id": "ch6_moran_fail",
     "bg": "parking", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "ÉLISE MORAN — DAS",
     "text": "Vous êtes moins bon que ce que disait Selg. Il m'avait prévenue que vous étiez redoutable. Je suis déçue. Bonne journée."},

    {"id": "ch6_moran_fail_2",
     "bg": "parking", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Elle part. Mais elle n'a pas dit 'je ne sais rien'. Elle a dit 'vous êtes moins bon'. Elle sait. Elle attend une meilleure offre. Je reviendrai avec une."},

    # ─── Moment relationnel : Mira révèle tout ────────────────────────────────

    {"id": "ch6_ext_rel_mira_00",
     "bg": "parlement", "rain": False, "transition": "fade_black",
     "time": "19:00",
     "char": "mira", "expr": 4, "side": "right",
     "name": "MIRA VOSS",
     "text": "Raven. Il y a quelque chose que je ne vous ai pas dit. Sur Arnheim. Sur moi. Et sur pourquoi ils m'ont licenciée vraiment."},

    {"id": "ch6_ext_rel_mira_01",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je vous écoute."},

    {"id": "ch6_ext_rel_mira_02",
     "bg": "parlement", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "Arnheim est mon père biologique. Il ne le sait pas. Ma mère a eu une liaison avec lui en 1988. Elle est morte quand j'avais douze ans. Elle ne m'a jamais dit son nom."},

    {"id": "ch6_ext_rel_mira_03",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Arnheim. Vous enquêtez sur votre père biologique."},

    {"id": "ch6_ext_rel_mira_04",
     "bg": "parlement", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "Je l'ai appris il y a trois ans. En croisant son dossier DAS. Une photo de 1988 dans ses archives personnelles. Ma mère était dessus. J'ai fait faire un test ADN. C'est confirmé."},

    {"id": "ch6_ext_rel_mira_05",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Et ça a changé quoi, dans votre enquête ?"},

    {"id": "ch6_ext_rel_mira_06",
     "bg": "parlement", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "Rien. Tout. Rien sur l'objectif. Tout sur le poids que ça représente. Je dépose mon père biologique. Et je le fais quand même. Parce que ce qu'il a fait est indéfendable."},

    # ── Choix : comment répondre à Mira ────────────────────────────────────────
    {"id": "ch6_ext_rel_mira_choix",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "",
     "text": "Mira vient de partager quelque chose d'immense. Quelque chose qui ne concerne pas l'enquête — et qui la concerne entièrement. Comment répondre ?",
     "choices": [
         "Reconnaître le courage que ça représente — sans minimiser",
         "Lui demander si elle est sûre de vouloir continuer dans ces conditions",
         "Lui rappeler qu'elle n'est pas seule pour porter ça"
     ],
     "choice_branch": {"0": "ch6_mira_courage", "1": "ch6_mira_question", "2": "ch6_mira_soutien"}},

    {"id": "ch6_mira_courage",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"mira": 20},
     "text": "Ce que vous faites — identifier votre père, construire le dossier contre lui, continuer malgré tout — c'est la chose la plus difficile que j'ai vue faire à quelqu'un depuis longtemps."},

    {"id": "ch6_mira_courage_2",
     "bg": "parlement", "rain": False,
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "Je n'attends pas d'éloge. Mais merci. Vraiment."},

    {"id": "ch6_mira_question",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Mira. Est-ce que vous êtes certaine que vous pouvez aller jusqu'au bout ? Sans que ça vous brise quelque chose d'irréparable ?"},

    {"id": "ch6_mira_question_2",
     "bg": "parlement", "rain": False,
     "char": "mira", "expr": 3, "side": "right",
     "name": "MIRA VOSS",
     "text": "Non. Je ne suis certaine de rien. Mais arrêter maintenant me briserait davantage. C'est un calcul. Et pour l'instant, continuer gagne."},

    {"id": "ch6_mira_soutien",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"mira": 15},
     "text": "Vous n'êtes pas seule pour porter ça. Sato sait rester discrète. Natasha aussi. Et moi... j'ai enquêté sur la mort de mon père pendant vingt ans. Je sais ce que ça fait."},

    {"id": "ch6_mira_soutien_2",
     "bg": "parlement", "rain": False,
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "Vous et moi. Deux enfants dont les pères ont croisé la même organisation. Vingt ans d'écart. C'est une coïncidence que j'aurais trouvée romanesque si elle n'était pas si lourde à porter."},

    # ─── Natasha sous pression légale ──────────────────────────────────────────

    {"id": "ch6_ext_natasha_00",
     "bg": "rue", "rain": True, "transition": "slide_left",
     "time": "11:00",
     "char": "natasha", "expr": 3, "side": "right",
     "name": "NATASHA MORI",
     "text": "J'ai reçu une convocation ce matin. Le cabinet juridique de Selg demande une saisie conservatoire de mes archives personnelles. Ils ont trois jours pour convaincre un juge."},

    {"id": "ch6_ext_natasha_01",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Trois jours. C'est calculé pour être avant le vote du 14. Si vos archives sont saisies, les preuves que vous gardez disparaissent dans le circuit légal pendant des mois."},

    {"id": "ch6_ext_natasha_02",
     "bg": "rue", "rain": True,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "J'ai déjà transmis des copies à mes trois confrères étrangers. Mais les copies numériques d'une source originale ne valent pas grand chose si la source elle-même est contestée."},

    # ── Choix : comment soutenir Natasha ──────────────────────────────────────
    {"id": "ch6_ext_natasha_choix",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "",
     "text": "Natasha est dans l'étau juridique. Selg a calculé son coup. Quelle est la bonne réponse ?",
     "choices": [
         "Accélérer la publication avant la saisie — tout sortir maintenant",
         "Chercher un juge de rechange — trouver quelqu'un d'incorruptible dans le circuit",
         "Lui proposer de porter les originaux en sécurité hors de France"
     ],
     "choice_branch": {"0": "ch6_natasha_accele", "1": "ch6_natasha_juge", "2": "ch6_natasha_exfil"}},

    {"id": "ch6_natasha_accele",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"natasha": 5},
     "text": "On publie maintenant. Tout. La saisie devient sans objet si les preuves sont déjà dans l'espace public. Légalement, ils ne peuvent pas 'désublier' un article."},

    {"id": "ch6_natasha_accele_2",
     "bg": "rue", "rain": True,
     "char": "natasha", "expr": 0, "side": "right",
     "name": "NATASHA MORI",
     "text": "C'est risqué. On perd l'effet de surprise coordonné. Mais vous avez raison — une saisie judiciaire d'archive, ça peut paralyser un journal pendant six mois. On publie. Demain matin. Coordination avec les trois autres rédactions."},

    {"id": "ch6_natasha_juge",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"sato": 5},
     "text": "Sato. Elle connaît un juge d'instruction indépendant — quelqu'un qui n'est pas dans le circuit de la Synarchie. Si on dépose les preuves dans ses mains en priorité, la saisie devient contestable."},

    {"id": "ch6_natasha_juge_2",
     "bg": "rue", "rain": True,
     "char": "natasha", "expr": 2, "side": "right",
     "name": "NATASHA MORI",
     "text": "Un juge indépendant. Ça pourrait fonctionner. Mais si ce juge est corruptible aussi — on vient de livrer les originaux directement. C'est un risque double."},

    {"id": "ch6_natasha_exfil",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"natasha": 10},
     "text": "Vos archives papier. Vous me les donnez ce soir. Je les passe la frontière suisse demain matin. Dans un coffre hors juridiction française. La saisie ne peut pas suivre."},

    {"id": "ch6_natasha_exfil_2",
     "bg": "rue", "rain": True,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Vous allez passer une frontière avec des preuves compromettantes dans un sac. Vous avez réalisé à quel point c'est exactement le genre de chose qu'on vous reprochera dans le procès de Selg ?"},

    {"id": "ch6_natasha_exfil_3",
     "bg": "rue", "rain": True,
     "char": "detective", "expr": 8, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je noterai ça dans ma liste de problèmes potentiels. Juste après 'ne pas laisser la Synarchie contrôler l'Europe'."},

    # ─── Déduction : Enregistrement Parlement + Accord Secret ─────────────────

    {"id": "ch6_ext_deduction_00",
     "bg": "bureau", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Enregistrement parlement + Accord Secret de 1994. La voix d'Arnheim dans l'enregistrement cite des clauses précises de l'accord. Clauses qui n'ont jamais été rendues publiques. Il était à la table de 1994."},

    {"id": "ch6_ext_deduction_01",
     "bg": "bureau", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "evidence": ("Déduction : Corruption au sommet de l'UE", "Arnheim co-signataire 1994 — corruption institutionnelle confirmée sur 30 ans"),
     "text": "Arnheim n'est pas un recrutement tardif. Il est un pilier d'origine. Trente ans de corruption au cœur d'une institution censée protéger les citoyens européens."},

    # ─── Raven et la culpabilité ──────────────────────────────────────────────

    {"id": "ch6_ext_culpa_00",
     "bg": "toit", "rain": False, "transition": "fade_black",
     "time": "02:00",
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je pense à Vane encore. L'Architecte a accéléré sa mort parce qu'il savait que je viendrais. Vane est mort parce que j'existe. Parce que j'étais le bon profil."},

    {"id": "ch6_ext_culpa_01",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Est-ce que je continue parce que c'est juste ? Ou est-ce que je continue pour ne pas avoir été l'instrument de rien ? La différence compte. Elle change tout à la façon dont on travaille."},

    {"id": "ch6_ext_culpa_02",
     "bg": "toit", "rain": False,
     "char": "policiere", "expr": 0, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. Il est 2h du matin et vous vous auto-flagellez sur le toit. Je vous entends depuis votre fenêtre ouverte."},

    {"id": "ch6_ext_culpa_03",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je n'avais pas prévu de public."},

    {"id": "ch6_ext_culpa_04",
     "bg": "toit", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Vane vous aurait remercié d'être venu. C'est ce qu'on ne sait jamais des morts — ce qu'ils auraient voulu dire. Mais si j'avais préparé mon propre piège depuis dix ans pour que quelqu'un continue à ma place... je voudrais que cette personne arrête de culpabiliser et finisse le travail."},

    {"id": "ch6_ext_culpa_05",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous savez que vous êtes meilleure que moi à presque tout, Sato."},

    {"id": "ch6_ext_culpa_06",
     "bg": "toit", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Je sais. Allez dormir."},

    # ─── Plan B — si le vote passe quand même ────────────────────────────────

    {"id": "ch6_ext_planb_00",
     "bg": "parlement", "rain": False, "transition": "slide_left",
     "time": "16:00",
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "Hypothèse de travail : le vote passe quand même le 14. La réforme entre en application. Qu'est-ce qu'on fait ?"},

    {"id": "ch6_ext_planb_01",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "On n'a pas de plan B. On a un plan A qu'on réussit. Le plan B c'est perdre, et perdre sur ce dossier n'est pas une option que j'ai envisagée."},

    {"id": "ch6_ext_planb_02",
     "bg": "parlement", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Moi si. Hypothèse : vote adopté le 14. La réforme est irréversible par les voies institutionnelles. Il reste la voie judiciaire internationale. Si on a le serveur et les preuves du chantage..."},

    {"id": "ch6_ext_planb_03",
     "bg": "parlement", "rain": False,
     "char": "natasha", "expr": 2, "side": "right",
     "name": "NATASHA MORI",
     "text": "La Cour de Justice de l'UE. Ça prend des années. Mais une réforme adoptée sous chantage peut être annulée. Le précédent juridique existe — traités signés sous contrainte."},

    {"id": "ch6_ext_planb_04",
     "bg": "parlement", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Des années, c'est réaliste. La Synarchie a misé sur le fait que personne ne voudrait passer dix ans en procès pour défaire un traité européen. Mais si les preuves de chantage sont irréfutables..."},

    {"id": "ch6_ext_planb_05",
     "bg": "parlement", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le plan B existe. Je l'entends. Mais le plan A est pour maintenant. Le reste, ce sera pour ceux qui viendront après nous si on échoue."},

    # ─── Épilogue étendu Ch6 ──────────────────────────────────────────────────

    {"id": "ch6_ext_epilogue_00",
     "bg": "toit", "rain": False, "transition": "fade_black",
     "time": "04:30",
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Onze jours avant le vote. Les publications ont déclenché une onde de choc dans les médias européens. Arnheim est convoqué. Selg est introuvable. Mais quelque chose me gêne."},

    {"id": "ch6_ext_epilogue_01",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Quelque chose me gêne depuis Berlin. Le contact anonyme — il nous a tout donné trop facilement. Le serveur. Moran. Selg. C'est trop propre. Les gens qui trahissent après vingt ans gardent toujours quelque chose pour eux."},

    {"id": "ch6_ext_epilogue_02",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Qu'est-ce qu'il gardait pour lui ? Et est-ce que ça nous manquera au moment crucial ?"},

    {"id": "ch6_ext_epilogue_03",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "note": "Le contact anonyme a peut-être gardé quelque chose. Vérifier : Accord Berlin 1994, signataire manquant.",
     "text": "Dans l'Accord de Berlin de 1994, il y a six signataires. On en a cinq. Le sixième n'a jamais été nommé. Ni dans le serveur. Ni dans les archives de Mira. Ni par Selg."},

    {"id": "ch6_ext_epilogue_04",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le sixième signataire. C'est le trou dans le dossier. C'est ce que le contact nous a caché. Et d'une façon ou d'une autre, ce sixième nom est encore debout. Encore actif."},

    {"id": "ch6_ext_fin",
     "bg": "toit", "rain": False,
     "char": None, "side": "left",
     "name": "",
     "text": "─── FIN DU CHAPITRE VI — EXTENSION ───"},
]


# ══════════════════════════════════════════════════════════════════════
# CHAPITRE VII — Extensions (~47 nœuds)
# Interrogatoires : l'Architecte (ultime), le sixième signataire, épilogue à choix
# Choix relationnels : Raven + chaque membre de l'équipe, décision finale sur Mira
# ══════════════════════════════════════════════════════════════════════

SCRIPT_VII_EXT = [

    # ─── ACTE 0 : Montée vers le bunker ──────────────────────────────────────

    {"id": "ch7_ext_00",
     "bg": "sous_sol", "rain": False, "transition": "fade_black",
     "time": "05:00",
     "char": None, "side": "left",
     "name": "",
     "text": "CHAPITRE VII — Extension : La Décision (approfondissement)"},

    {"id": "ch7_ext_01",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Alpes autrichiennes. 2200 mètres. 5h du matin. L'air est froid et sec comme il ne l'est jamais à Paris. Dans cet air, les erreurs ont moins d'endroit où se cacher."},

    {"id": "ch7_ext_02",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je pense à Marcus Vane. Il a passé dix ans à construire le piège dans lequel la Synarchie vient de tomber. Et il est mort sans voir si ça marcherait."},

    {"id": "ch7_ext_03",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "C'est une des formes les plus solitaires du courage. Construire quelque chose qu'on ne verra pas."},

    # ─── Le sixième signataire ────────────────────────────────────────────────

    {"id": "ch7_ext_sixieme_00",
     "bg": "sous_sol", "rain": False, "transition": "iris",
     "time": "05:45",
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le serveur de Berlin. Avant de partir pour l'Autriche, j'ai demandé à Mira de chercher le sixième signataire. Elle a trouvé quelque chose."},

    {"id": "ch7_ext_sixieme_01",
     "bg": "sous_sol", "rain": False,
     "char": "mira", "expr": 3, "side": "right",
     "name": "MIRA VOSS",
     "text": "Le sixième signataire. Dans l'accord de Berlin de 1994, la sixième signature était codée. Un numéro. J'ai croisé ce numéro avec les registres bancaires du compte letton."},

    {"id": "ch7_ext_sixieme_02",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Et ?"},

    {"id": "ch7_ext_sixieme_03",
     "bg": "sous_sol", "rain": False,
     "char": "mira", "expr": 1, "side": "right",
     "name": "MIRA VOSS",
     "text": "Le sixième bénéficiaire du compte letton s'appelait Franz Bertier. Pas Commandant Bertier — un titre de façade. Franz Bertier, ex-directeur de la Direction des Affaires Spéciales. Il est à la retraite depuis quatre ans.",
     "evidence": ("Franz Bertier — 6e signataire", "Ex-directeur DAS — fondateur occulte — retraite dorée depuis 4 ans")},

    {"id": "ch7_ext_sixieme_04",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Bertier. Le Commandant Bertier du bon de commande de Cazes. La même fausse identité. Il s'est servi de son propre nom de guerre. La vanité comme erreur."},

    {"id": "ch7_ext_sixieme_05",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Et Bertier est retraité à Salzburg. À deux heures de route d'ici. Ce n'est pas une coïncidence. Il est là pour superviser la fin du plan. Pour voir le résultat de trente ans de travail.",
     "evidence": ("Bertier à Salzburg", "6e signataire en déplacement — supervision finale — 2h du bunker")},

    # ─── Interrogatoire ultime : l'Architecte, face-à-face vrai ──────────────

    {"id": "ch7_ext_architecte_00",
     "bg": "sous_sol", "rain": False, "transition": "fade_black",
     "time": "07:30",
     "char": "architect", "expr": 0, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Raven. Il y a quelque chose que je veux vous demander. Sans calculer la réponse. Vraiment."},

    {"id": "ch7_ext_architecte_01",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Demandez."},

    {"id": "ch7_ext_architecte_02",
     "bg": "sous_sol", "rain": False,
     "char": "architect", "expr": 1, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Si vous saviez depuis le début que le procès n'aboutirait à rien — que mes avocats auraient raison, que les sept noms disparaîtraient, que dans vingt ans quelqu'un rebâtirait ce que vous venez de détruire... vous auriez quand même fait tout ça ?"},

    # ── Choix d'interrogatoire — question philosophique ───────────────────────
    {"id": "ch7_ext_architecte_choix",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "",
     "text": "L'Architecte pose une question qui n'attend pas une stratégie d'interrogatoire. Il veut une vraie réponse. Comment répondre ?",
     "choices": [
         "Oui — même si rien ne change durablement, ça valait le coup",
         "Non — sans résultat réel, ça n'aurait pas de sens",
         "Je ne sais pas — et cette incertitude est honnête"
     ],
     "choice_branch": {"0": "ch7_archi_oui", "1": "ch7_archi_non", "2": "ch7_archi_saispa"}},

    {"id": "ch7_archi_oui",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Oui. Marcus Vane méritait que quelqu'un vienne. Mon père méritait que quelqu'un continue. Les 147 du vol 219 méritaient que quelqu'un nomme ce qui leur est arrivé. Même si personne d'autre n'entend jamais."},

    {"id": "ch7_archi_oui_2",
     "bg": "sous_sol", "rain": False,
     "char": "architect", "expr": 3, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "...Vous le pensez vraiment. C'est ça qui vous rend dangereux, Raven. Pas votre intelligence. Votre conviction."},

    {"id": "ch7_archi_non",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Non. Sincèrement non. Je fais ça parce que je crois que ça peut changer quelque chose. Si j'étais certain que ça ne servirait à rien, je serais peut-être moins là."},

    {"id": "ch7_archi_non_2",
     "bg": "sous_sol", "rain": False,
     "char": "architect", "expr": 1, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "Honnête. Et plus humain que je ne le pensais. Vous avez des doutes. C'est bien."},

    {"id": "ch7_archi_saispa",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"architect_respect": 5},
     "text": "Je ne sais pas. C'est la réponse honnête. Peut-être oui. Peut-être que je ferais la même chose par réflexe ou par obstination. Peut-être que ça n'a plus rien à voir avec le résultat."},

    {"id": "ch7_archi_saispa_2",
     "bg": "sous_sol", "rain": False,
     "char": "architect", "expr": 2, "side": "right",
     "name": "L'ARCHITECTE",
     "text": "C'est la seule réponse qui me touche. Vraiment. Parce que moi aussi, après trente ans, je ne sais plus si je crois encore au résultat. Ou si je continue par inertie."},

    {"id": "ch7_archi_saispa_3",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Alors peut-être qu'on est plus similaires qu'on ne l'admettra jamais. Et c'est pour ça que je ne peux pas vous laisser partir."},

    # ─── Moment relationnel : Sato — avant le dénouement ─────────────────────

    {"id": "ch7_ext_rel_sato_00",
     "bg": "sous_sol", "rain": False, "transition": "fade_black",
     "time": "06:30",
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Raven. Je veux vous dire quelque chose. Avant qu'on entre."},

    {"id": "ch7_ext_rel_sato_01",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Allez."},

    {"id": "ch7_ext_rel_sato_02",
     "bg": "sous_sol", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Ma fille m'a encore parlé de vous cette semaine. Elle vous a dessiné. Avec le chapeau. Et six pattes. Parce que, dit-elle, les héros normaux c'est ennuyeux."},

    {"id": "ch7_ext_rel_sato_03",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 2, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Elle m'a donné des pattes supplémentaires. C'est utile pour un terrain montagneux."},

    # ── Choix : répondre à Sato avant l'action ────────────────────────────────
    {"id": "ch7_ext_rel_sato_choix",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 0, "side": "left",
     "name": "",
     "text": "Sato vient de partager quelque chose de doux dans un moment qui ne l'est pas. Comment répondre ?",
     "choices": [
         "Lui dire ce qu'on pense vraiment d'elle — maintenant, avant qu'il soit trop tard",
         "Garder l'humour — c'est ce qui les a maintenus debout jusqu'ici",
         "Lui dire qu'on reviendra — et que cette fois on le pense"
     ],
     "choice_branch": {"0": "ch7_sato_sincere", "1": "ch7_sato_humour", "2": "ch7_sato_promesse"}},

    {"id": "ch7_sato_sincere",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"sato": 25},
     "text": "Sato. Leila. Vous êtes la personne la plus compétente et la plus courageuse que j'aie connue dans ce métier. Et je n'aurais pas pu finir ce dossier sans vous. Je voulais vous le dire."},

    {"id": "ch7_sato_sincere_2",
     "bg": "sous_sol", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "...C'est la première fois que vous utilisez mon prénom. Allez. On rentre là-dedans."},

    {"id": "ch7_sato_humour",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"sato": 10},
     "text": "Dites à votre fille que je garde les six pattes pour l'escalade en haute montagne. Ça aide."},

    {"id": "ch7_sato_humour_2",
     "bg": "sous_sol", "rain": False,
     "char": "policiere", "expr": 2, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Je lui dirai. Allez, detective-six-pattes. On y va."},

    {"id": "ch7_sato_promesse",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "rep_change": {"sato": 20},
     "text": "On ressort d'ici. Je vous le promets. Et cette fois ce n'est pas une formule."},

    {"id": "ch7_sato_promesse_2",
     "bg": "sous_sol", "rain": False,
     "char": "policiere", "expr": 1, "side": "right",
     "name": "OFF. LEILA SATO",
     "text": "Je vous tiens pour responsable de cette promesse. Votre seule qualité fiable, c'est de tenir vos engagements. Même les inconfortables."},

    # ─── Franz Bertier : le sixième homme ─────────────────────────────────────

    {"id": "ch7_ext_bertier_00",
     "bg": "sous_sol", "rain": False, "transition": "slide_left",
     "time": "08:00",
     "char": None, "side": "left",
     "name": "",
     "text": "Dans le bunker, après l'arrestation de l'Architecte et de Selg. Une pièce qu'on n'avait pas vu. Derrière une porte codée."},

    {"id": "ch7_ext_bertier_01",
     "bg": "sous_sol", "rain": False,
     "char": "taro", "expr": 0, "side": "right",
     "name": "FRANZ BERTIER",
     "text": "Vous avez trouvé la pièce. Je n'espérais plus vous voir arriver. Ou je l'espérais trop."},

    {"id": "ch7_ext_bertier_02",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Franz Bertier. Le sixième signataire. L'homme dont même Selg ne prononçait pas le nom."},

    {"id": "ch7_ext_bertier_03",
     "bg": "sous_sol", "rain": False,
     "char": "taro", "expr": 1, "side": "right",
     "name": "FRANZ BERTIER",
     "text": "À 74 ans, Raven, on n'a plus grand chose à perdre et tout à raconter. Je savais que ce jour viendrait. En 1994, j'ai cru au projet. En 2009, après le vol 219, j'ai arrêté d'y croire. En 2024, je suis là."},

    # ── Mini-jeu interrogatoire Bertier ───────────────────────────────────────
    {"id": "ch7_interro_bertier",
     "type": "interrogation",
     "suspect": "taro",
     "time_limit": 150,
     "on_success": "ch7_bertier_ok",
     "on_failure": "ch7_bertier_fail"},

    {"id": "ch7_bertier_ok",
     "bg": "sous_sol", "rain": False,
     "char": "taro", "expr": 2, "side": "right",
     "name": "FRANZ BERTIER",
     "text": "Vous avez trouvé la clé. La vraie. Vane et moi, on se connaissait. C'est moi qui lui ai demandé de construire l'assurance-vie. C'est moi qui ai dit qu'un jour quelqu'un comme vous viendrait."},

    {"id": "ch7_bertier_ok_2",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 7, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous... vous êtes le commanditaire de la clé USB. Pas l'Architecte."},

    {"id": "ch7_bertier_ok_3",
     "bg": "sous_sol", "rain": False,
     "char": "taro", "expr": 1, "side": "right",
     "name": "FRANZ BERTIER",
     "text": "L'Architecte voulait éliminer Vane proprement. Moi j'ai orchestré sa mort de façon à ce qu'elle laisse des traces. Les traces que vous avez suivies. Je vous ai mis sur la piste depuis le premier soir.",
     "evidence": ("Testament de Vane — vérité complète", "Bertier orchestrateur — Vane complice volontaire — piège conçu à deux pour dix ans")},

    {"id": "ch7_bertier_ok_4",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vane est mort en sachant que vous aviez construit son piège. Et il a accepté."},

    {"id": "ch7_bertier_ok_5",
     "bg": "sous_sol", "rain": False,
     "char": "taro", "expr": 2, "side": "right",
     "name": "FRANZ BERTIER",
     "text": "Il a dit : 'Si ça marche, ça aura valu le coup. Si ça ne marche pas, au moins j'aurai essayé.' C'est tout. Marcus Vane était un homme simple avec une conviction extraordinaire."},

    {"id": "ch7_bertier_fail",
     "bg": "sous_sol", "rain": False,
     "char": "taro", "expr": 1, "side": "right",
     "name": "FRANZ BERTIER",
     "text": "Vous ne trouverez pas la fissure de ce côté. Je suis vieux mais pas fragile. Ce que j'ai à dire, je le dirai devant un tribunal. Pas avant."},

    {"id": "ch7_bertier_fail_2",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il tient. Bien. Il survivra au procès. Et devant un tribunal, ce qu'il a à dire sera peut-être la pièce finale. Je le laisse venir."},

    # ─── Déduction finale : Testament + Schéma ────────────────────────────────

    {"id": "ch7_ext_deduction_00",
     "bg": "sous_sol", "rain": False, "transition": "fade_black",
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Testament de Vane + Schéma du Réseau + déclaration de Bertier. Les pièces sont complètes. Vane tenait deux jeux de comptes non pas par peur — mais parce que Bertier lui avait demandé de construire la preuve parfaite."},

    {"id": "ch7_ext_deduction_01",
     "bg": "sous_sol", "rain": False,
     "char": "detective", "expr": 3, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "evidence": ("Déduction : Vane savait depuis le début", "Vane + Bertier — plan décennal — suicide organisé comme transmission de preuves"),
     "text": "Ce n'est pas une victime. C'est un agent volontaire qui a sacrifié sa vie pour que les preuves arrivent intact. L'héroïsme le moins visible qui soit."},

    # ─── Moment relationnel : Raven seul face à l'épilogue ───────────────────

    {"id": "ch7_ext_solo_00",
     "bg": "toit", "rain": False, "transition": "fade_white",
     "time": "18:00",
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Le bunker. Interpol. Les menottes. La route du retour. Tout ça est derrière maintenant. Je suis sur le toit de mon immeuble à Paris. Le seul endroit où je sais réfléchir."},

    {"id": "ch7_ext_solo_01",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Six personnages. Un réseau. Un plan de trente ans. Et Marcus Vane, tout seul dans une ruelle, qui a attendu que quelqu'un lise sa clé USB."},

    {"id": "ch7_ext_solo_02",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je pense à lui. Je pense à mon père. À tous les gens qui ont su des choses et qui ont décidé que ça valait la peine de les dire. Même au prix le plus élevé."},

    {"id": "ch7_ext_solo_03",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il y a quelque chose de reposant dans le fait d'avoir fini. Pas de victoire éclatante. Pas de discours. Juste : c'est fait. Ça aura été fait. Et c'est assez."},

    # ─── Épilogue relationnel : les adieux ou les retrouvailles ──────────────

    {"id": "ch7_ext_epilogue_mira",
     "bg": "toit", "rain": False, "transition": "slide_left",
     "time": "21:00",
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "J'ai assisté à l'audience préliminaire ce matin. Arnheim a pâli quand le procureur a cité la filiation biologique. Il ne savait pas. Il ne sait toujours pas que c'est moi."},

    {"id": "ch7_ext_epilogue_mira_2",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Est-ce que vous avez l'intention de lui dire ?"},

    {"id": "ch7_ext_epilogue_mira_3",
     "bg": "toit", "rain": False,
     "char": "mira", "expr": 0, "side": "right",
     "name": "MIRA VOSS",
     "text": "Non. Ce n'est pas nécessaire. Ce qui est nécessaire, c'est le procès. Le reste... je vivrai avec."},

    {"id": "ch7_ext_epilogue_mira_4",
     "bg": "toit", "rain": False,
     "char": "detective", "expr": 1, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Vous avez fait quelque chose que peu de gens auraient pu faire. Et vous êtes encore debout."},

    {"id": "ch7_ext_epilogue_mira_5",
     "bg": "toit", "rain": False,
     "char": "mira", "expr": 2, "side": "right",
     "name": "MIRA VOSS",
     "text": "Je suis encore debout. C'est déjà beaucoup. Et votre équipe... si jamais vous avez besoin d'une analyste pour la suite... je suis là. Pour de vrai, cette fois."},

    {"id": "ch7_ext_epilogue_natasha",
     "bg": "rue", "rain": False, "transition": "fade_black",
     "time": "22:00",
     "char": "natasha", "expr": 2, "side": "right",
     "name": "NATASHA MORI",
     "text": "Prix Albert Londres confirmé. Remise en novembre. Mes trois confrères partagent la récompense. Mon rédacteur en chef m'a appelé pour s'excuser d'avoir voulu mettre le dossier en pause."},

    {"id": "ch7_ext_epilogue_natasha_2",
     "bg": "rue", "rain": False,
     "char": "detective", "expr": 6, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Je suppose que vous lui avez dit que vous acceptiez ses excuses avec grâce et magnanimité."},

    {"id": "ch7_ext_epilogue_natasha_3",
     "bg": "rue", "rain": False,
     "char": "natasha", "expr": 1, "side": "right",
     "name": "NATASHA MORI",
     "text": "Je lui ai dit que la prochaine fois qu'il essayait de me faire mettre en pause une investigation, je publie dans un journal concurrent. Ça ressemble à de la magnanimité pour quelqu'un qui me connaît."},

    # ─── Fin étendue : Raven, la dernière question ────────────────────────────

    {"id": "ch7_ext_fin_00",
     "bg": "toit", "rain": True, "transition": "fade_black",
     "time": "02:00",
     "char": "detective", "expr": 9, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Franz Bertier vient de signer sa déposition complète. Vingt-deux pages. Trente ans. Chaque décision de la Synarchie, chaque crime, chaque nom. Il a tout donné."},

    {"id": "ch7_ext_fin_01",
     "bg": "toit", "rain": True,
     "char": "detective", "expr": 4, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Il m'a demandé une seule chose : que le nom de Marcus Vane soit mentionné dans le dossier d'accusation. Pas comme victime. Comme source. Comme l'homme qui a tout rendu possible."},

    {"id": "ch7_ext_fin_02",
     "bg": "toit", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "J'ai dit oui. J'ai appelé le procureur. Il a dit que c'était inhabituel. J'ai dit que l'habituel ne m'intéressait pas. Et que Marcus Vane méritait au moins son nom dans les archives."},

    {"id": "ch7_ext_fin_03",
     "bg": "toit", "rain": True,
     "char": "detective", "expr": 0, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "note": "Marcus Vane. Source principale. Architecte de la chute de la Synarchie. Ce qui compte n'est pas toujours ce qu'on voit.",
     "text": "Marcus Vane, né à Bordeaux le 3 mars 1982, mort à Chinatown le 14 janvier de cette année. Source principale dans l'affaire Synarchie. Quarante-deux ans. Seul. Et pourtant pas."},

    {"id": "ch7_ext_fin_04",
     "bg": "toit", "rain": True,
     "char": "detective", "expr": 5, "side": "left",
     "name": "DÉTECTIVE RAVEN",
     "text": "Parce que dix ans plus tôt, il avait décidé que quelqu'un viendrait. Et quelqu'un est venu. Ce n'était pas rien. Ce n'est jamais rien."},

    {"id": "ch7_ext_fin_05",
     "bg": "toit", "rain": False, "transition": "fade_white",
     "char": None, "side": "left",
     "name": "",
     "text": "─── FIN DU CHAPITRE VII — EXTENSION ───\n\nNUIT SANS TÉMOIN — Édition complète"},
]



# ═══════════════════════════════════════════════════════════════════════════════
# ASSEMBLAGE FINAL — SCRIPT = SCRIPT_I + SCRIPT_II + ... + SCRIPT_VII
# ═══════════════════════════════════════════════════════════════════════════════

SCRIPT = (
    SCRIPT_I
    + SCRIPT_I_EXT
    + SCRIPT_II
    + SCRIPT_II_EXT
    + SCRIPT_III
    + SCRIPT_IIIB
    + SCRIPT_IIIC
    + SCRIPT_IV
    + SCRIPT_IV_EXT
    + SCRIPT_V
    + SCRIPT_V_EXT
    + SCRIPT_VI
    + SCRIPT_VI_EXT
    + SCRIPT_VII
    + SCRIPT_VII_EXT
)