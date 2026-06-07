"""
deductions.py — Système de combinaison de preuves
==================================================

Chaque combinaison est définie par un frozenset de deux noms de preuves
(ce qui la rend symétrique : A+B == B+A).

Structure d'une déduction :
    {
        "title":   str,   # Nom court de la déduction
        "text":    str,   # Texte de révélation (affiché dans la boîte)
        "insight": str,   # Icône / label court pour le panneau de déductions
    }

API publique :
    engine = DeductionEngine()
    result = engine.try_combine("Clé USB", "Fichiers Synarchie")
    # → dict si nouvelle déduction, None si déjà connue ou combinaison inconnue

    engine.all_deductions()   # list[dict] — toutes les déductions débloquées
"""

from __future__ import annotations
from typing import Optional

# ── Table des combinaisons ─────────────────────────────────────────────────────
# Clé : frozenset de deux noms de preuves (exactement comme dans script.py)
# Valeur : déduction débloquée

COMBINATION_TABLE: dict[frozenset, dict] = {

    # ── Chapitre I ─────────────────────────────────────────────────────────────

    frozenset({"Dossier Vane", "Clé USB"}): {
        "title":   "Double comptabilité",
        "text":    (
            "Vane tenait deux jeux de comptes : un officiel pour ses clients, "
            "un crypté sur la clé USB pour la Synarchie. Il était à la fois "
            "complice et témoin gênant."
        ),
        "insight": "💡 Vane — comptable & otage",
    },

    frozenset({"Clé USB", "Fichiers Synarchie"}): {
        "title":   "La clé de tout",
        "text":    (
            "Les fichiers Synarchie sur la clé USB ne sont pas une simple liste "
            "de noms : c'est un registre de chantage. Chaque virement est assorti "
            "d'une compromission. Vane n'était pas un exécutant — il était le "
            "garant de l'équilibre de la terreur."
        ),
        "insight": "💡 Registre de chantage",
    },

    frozenset({"Trace de pneus", "Dossier Vane"}): {
        "title":   "La voiture de l'exécuteur",
        "text":    (
            "Les pneus larges correspondent à un véhicule de fonction policier. "
            "Vane a été conduit sur la scène de crime par quelqu'un qui connaissait "
            "les rotations de patrouille — un initié."
        ),
        "insight": "💡 Véhicule de service impliqué",
    },

    frozenset({"Trace de pneus", "Fichiers Synarchie"}): {
        "title":   "Logistique intégrée",
        "text":    (
            "La Synarchie dispose d'un accès logistique aux véhicules officiels. "
            "Le meurtre de Vane n'est pas un crime de rue : c'est une opération "
            "planifiée avec des ressources institutionnelles."
        ),
        "insight": "💡 Crime institutionnel",
    },

    # ── Chapitre II ────────────────────────────────────────────────────────────

    frozenset({"Registre Offshore", "Fichiers Synarchie"}): {
        "title":   "Le circuit de blanchiment",
        "text":    (
            "Les sociétés offshore du registre correspondent exactement aux "
            "lignes cryptées de la clé de Vane. L'argent entre par des fondations "
            "culturelles, sort via des mandataires politiques. La Synarchie n'est "
            "pas criminelle — elle EST la structure."
        ),
        "insight": "💡 Blanchiment institutionnalisé",
    },

    frozenset({"Photo du Fantôme", "Enregistrement Taro"}): {
        "title":   "Identification Ferrière",
        "text":    (
            "La silhouette avec badge de la photo correspond à la carrure et à la "
            "démarche de Ferrière. La voix sur l'enregistrement confirme : c'est "
            "lui qui a ordonné l'élimination de Vane depuis un téléphone prépayé "
            "acheté à Belleville."
        ),
        "insight": "💡 Ferrière = commanditaire",
    },

    frozenset({"Photo du Fantôme", "Clé du Loft 7"}): {
        "title":   "Le QG du fantôme",
        "text":    (
            "La silhouette avec badge fréquentait le Loft 7 régulièrement. "
            "Il n'était pas qu'un exécutant : il supervisait les opérations "
            "locales de la Synarchie depuis cet entrepôt."
        ),
        "insight": "💡 Ferrière — agent de terrain",
    },

    frozenset({"Enregistrement Taro", "Registre Offshore"}): {
        "title":   "La commission de Ferrière",
        "text":    (
            "Sur l'enregistrement, Ferrière mentionne un 'arrangement habituel'. "
            "Dans le registre offshore, une ligne récurrente de 8 000 € mensuels "
            "vers une holding luxembourgeoise correspond exactement à son salaire "
            "parallèle."
        ),
        "insight": "💡 Ferrière — 8k€/mois Synarchie",
    },

    frozenset({"Clé du Loft 7", "Rapport interne"}): {
        "title":   "Nœud opérationnel",
        "text":    (
            "Le Loft 7 n'est pas qu'un entrepôt : c'est le nœud de coordination "
            "régionale de la Synarchie. Le rapport interne liste 6 opérations "
            "planifiées depuis ce site au cours des 18 derniers mois, dont deux "
            "impliquant des magistrats."
        ),
        "insight": "💡 Loft 7 = centre de commande",
    },

    # ── Chapitre III ───────────────────────────────────────────────────────────

    frozenset({"Passeport Fantôme", "Schéma du Réseau"}): {
        "title":   "L'Architecte multinational",
        "text":    (
            "Les identités multiples du passeport correspondent aux nœuds du "
            "schéma réseau : l'Architecte se déplace physiquement entre les "
            "capitales pour superviser chaque branche. Il n'existe nulle part "
            "— et partout à la fois."
        ),
        "insight": "💡 L'Architecte — présence physique globale",
    },

    frozenset({"Schéma du Réseau", "Registre Offshore"}): {
        "title":   "L'épine dorsale financière",
        "text":    (
            "Chaque nœud du schéma correspond à une holding dans le registre "
            "offshore. La Synarchie n'est pas un réseau criminel classique : "
            "c'est une multinationale de la corruption, avec actionnaires, "
            "dividendes et conseil d'administration fantôme."
        ),
        "insight": "💡 Synarchie SA — multinationale",
    },

    frozenset({"Accord Secret", "Enregistrement final"}): {
        "title":   "L'aveu contractuel",
        "text":    (
            "L'accord secret signé par six gouvernements et l'enregistrement "
            "des aveux de l'Architecte se recoupent parfaitement : les clauses "
            "de l'accord correspondent mot pour mot aux décisions politiques "
            "citées dans l'enregistrement. C'est la preuve irréfutable d'une "
            "gouvernance parallèle légalisée."
        ),
        "insight": "💡 Preuve irréfutable — gouvernance fantôme",
    },

    frozenset({"Identité de l'Architecte", "Passeport Fantôme"}): {
        "title":   "Le masque final",
        "text":    (
            "Le nom réel de l'Architecte correspond à une personnalité publique "
            "de premier plan — philanthrope reconnu, conseiller de plusieurs "
            "gouvernements. Le passeport fantôme révèle qu'il opère sous sept "
            "identités depuis trente ans. La respectabilité était son arme "
            "principale."
        ),
        "insight": "💡 L'Architecte — identité publique révélée",
    },

    frozenset({"Identité de l'Architecte", "Schéma du Réseau"}): {
        "title":   "L'organigramme complet",
        "text":    (
            "En combinant le nom de l'Architecte et le schéma réseau, Raven peut "
            "reconstituer la hiérarchie complète de la Synarchie. Pour la première "
            "fois, chaque case est remplie — des exécutants de terrain jusqu'au "
            "sommet. C'est assez pour démanteler toute l'organisation."
        ),
        "insight": "💡 Synarchie — organigramme complet",
    },

    frozenset({"Enregistrement final", "Rapport interne"}): {
        "title":   "Opérations confirmées",
        "text":    (
            "Les opérations listées dans le rapport interne sont toutes mentionnées "
            "dans l'enregistrement final. L'Architecte les revendique explicitement. "
            "Ce croisement transforme des soupçons en preuves judiciaires "
            "incontestables pour douze chefs d'inculpation."
        ),
        "insight": "💡 12 chefs d'inculpation confirmés",
    },

    # ── Combinaisons transversales (Chap I-II et II-III) ──────────────────────

    frozenset({"Clé USB", "Accord Secret"}): {
        "title":   "Le fil directeur",
        "text":    (
            "De la clé USB de Vane à l'accord secret de Genève : c'est le même "
            "réseau, la même main invisible. Vane ne comptait pas l'argent sale "
            "d'un criminel local — il gérait la trésorerie d'un pacte entre États. "
            "Sa mort était une nécessité comptable."
        ),
        "insight": "💡 Vane — victime géopolitique",
    },

    frozenset({"Dossier Vane", "Identité de l'Architecte"}): {
        "title":   "De la ruelle au sommet",
        "text":    (
            "Marcus Vane, comptable anonyme d'une ruelle de Chinatown, et "
            "l'Architecte, conseiller de gouvernements : le même réseau relie "
            "ces deux extrêmes. La mort de Vane n'était pas un règlement de "
            "comptes — c'était une décision stratégique prise au plus haut niveau."
        ),
        "insight": "💡 Vane — maillon d'une chaîne globale",
    },
        # Ch4
    frozenset({"Photo de surveillance", "Badge magnétique"}): {
        "title":   "Surveillance institutionnelle",
        "text":    "Quelqu'un avec un accès officiel surveille Raven "
        "depuis l'intérieur des institutions. Ce n'est pas "
        "un criminel de rue. C'est quelqu'un qui a un bureau et un badge.",
        "insight": "💡 Raven surveillé de l'intérieur",
    },
    frozenset({"Clé USB #2", "Fichiers Synarchie"}): {
        "title":   "Le successeur prévu",
        "text":    "Les données de la clé #2 complètent exactement "
        "les fichiers de Vane. Ils ont été conçus ensemble. "
        "La Synarchie avait planifié sa propre chute comme dispositif de survie.",
        "insight": "💡 Chute planifiée — successeur désigné",
    },
    frozenset({"Liste de contacts", "Identité de l'Architecte"}): {
        "title":   "Réseau survivant",
        "text":    "Trois des noms codés de la liste correspondent "
        "aux initiales confirmées dans le dossier de l'Architecte. "
        "La Synarchie a trois ministres en exercice protégés.",
        "insight": "💡 3 ministres actifs — réseau vivant",
    },
    frozenset({"Dossier Mira", "Photo de surveillance"}): {
        "title":   "Mira — actif ou double jeu ?",
        "text":    "Mira a été surveillée en même temps que Raven. "
        "Soit elle est aussi une cible, soit elle est un vecteur "
        "conscient utilisé pour attirer Raven dans un périmètre contrôlé.",
        "insight": "💡 Mira — cible ou leurre ?",
    },
    # Ch5
    frozenset({"Identité du Fantôme", "Accord de Berlin"}): {
        "title":   "L'architecte adjoint",
        "text":    "Viktor Selg apparaît dans l'Accord de Berlin de 1994 comme co-signataire. Il n'est pas le successeur de l'Architecte. Il a toujours été son numéro deux. Depuis le début.",
        "insight": "💡 Selg — numéro 2 depuis 1994",
    },
    frozenset({"Serveur miroir", "Clé USB #2"}): {
        "title":   "Les données ne meurent pas",
        "text":    "La clé USB #2 et le serveur miroir contiennent des données complémentaires. Vane a délibérément séparé les informations pour qu'aucune capture unique ne donne tout. Il avait prévu qu'on trouverait les deux.",
        "insight": "💡 Vane — architecture de sécurité en deux parties",
    },
    frozenset({"Témoin protégé", "Enregistrement Taro"}): {
        "title":   "Chaîne de commandement",
        "text":    "Le témoignage du contact et l'enregistrement de Taro se recoupent sur les mêmes noms dans le même ordre. La hiérarchie de commandement de la Synarchie est désormais complète sur trois niveaux.",
        "insight": "💡 Hiérarchie Synarchie — 3 niveaux confirmés",
    },
    # Ch6
    frozenset({"Enregistrement parlement", "Accord Secret"}): {
        "title":   "Corruption au sommet de l'UE",
        "text":    "L'enregistrement de la commission Arnheim cite mot pour mot des clauses de l'Accord Secret de Genève. Les institutions européennes ne surveillent pas la Synarchie. Elles l'abritent.",
        "insight": "💡 UE — institution hôte, pas contrôlante",
    },
    frozenset({"Compte numéroté", "Registre Offshore"}): {
        "title":   "Même banque, vingt ans",
        "text":    "La banque lettone d'Arnheim est la même qui apparaît dans le registre offshore du chapitre I. La Synarchie utilise le même réseau bancaire depuis vingt ans. Invisible parce que légal.",
        "insight": "💡 Continuité bancaire — 20 ans d'impunité",
    },
    frozenset({"Identité du Sénateur", "Liste de contacts"}): {
        "title":   "Le législateur est la Synarchie",
        "text":    "Arnheim figure dans la liste de contacts de la clé USB #2. Il ne protège pas la Synarchie depuis le Sénat. Il en est membre depuis dix-huit ans. Les lois qu'il a votées ont protégé le réseau.",
        "insight": "💡 Arnheim — législateur-criminel depuis 18 ans",
    },
    # Ch7
    frozenset({"Testament de Vane", "Dossier Vane"}): {
        "title":   "Vane savait depuis le début",
        "text":    "Le testament croise exactement le dossier Vane du chapitre I. Marcus Vane documentait la Synarchie depuis dix ans. Il attendait quelqu'un d'assez obstiné pour ne pas s'arrêter. Il avait préparé toutes les pièces. Il manquait juste quelqu'un pour les assembler.",
        "insight": "💡 Vane — préparait ça depuis 10 ans",
    },
    frozenset({"Preuve ultime", "Schéma du Réseau"}): {
        "title":   "L'organigramme complet",
        "text":    "En combinant la preuve ultime et le schéma du réseau du chapitre III, chaque case de l'organigramme est remplie. De Vane, comptable de ruelle, jusqu'à l'Architecte, conseiller de gouvernements. La chaîne est entière.",
        "insight": "💡 Synarchie — organigramme intégral Ch1 à Ch7",
    },
    frozenset({"Coordonnées bunker", "Passeport Fantôme"}): {
        "title":   "L'Architecte n'a jamais fui",
        "text":    "Les coordonnées du bunker correspondent à une propriété liée à l'une des identités du passeport fantôme de Genève. L'Architecte ne s'est jamais enfui. Il s'est replié vers un plan prévu de longue date. Il attendait.",
        "insight": "💡 L'Architecte — a toujours su qu'on viendrait",
    },
}

# ── Moteur de déductions ───────────────────────────────────────────────────────

class DeductionEngine:
    def __init__(self) -> None:
        self._unlocked: list[dict] = []          # déductions débloquées
        self._unlocked_keys: set[frozenset] = set()

    # ── Combinaison ────────────────────────────────────────────────────────────

    def try_combine(self, name_a: str, name_b: str) -> Optional[dict]:
        """
        Tente de combiner deux preuves.
        - Retourne le dict de déduction si la combinaison est nouvelle et connue.
        - Retourne None si inconnue ou déjà débloquée.
        """
        key = frozenset({name_a, name_b})
        if key in self._unlocked_keys:
            return None
        result = COMBINATION_TABLE.get(key)
        if result is not None:
            self._unlocked_keys.add(key)
            entry = dict(result)
            entry["from"] = (name_a, name_b)
            self._unlocked.append(entry)
            return entry
        return None

    # ── Accesseurs ─────────────────────────────────────────────────────────────

    def all_deductions(self) -> list[dict]:
        return list(self._unlocked)

    def count(self) -> int:
        return len(self._unlocked)

    # ── Sérialisation (pour save_manager) ─────────────────────────────────────

    def to_list(self) -> list[dict]:
        """Sérialise pour JSON (remplace frozenset par liste)."""
        out = []
        for d in self._unlocked:
            entry = dict(d)
            entry["from"] = list(d.get("from", []))
            out.append(entry)
        return out

    def from_list(self, data: list[dict]) -> None:
        """Restaure depuis JSON."""
        self._unlocked.clear()
        self._unlocked_keys.clear()
        for entry in data:
            pair = entry.get("from", [])
            if len(pair) == 2:
                key = frozenset(pair)
                self._unlocked_keys.add(key)
            self._unlocked.append(dict(entry))
