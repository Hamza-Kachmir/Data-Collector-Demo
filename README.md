# Data Collector

Une application web de démonstration pour interroger l'API France Travail en temps réel, développée avec Python et NiceGUI.

---

### 🚀 Contexte du Projet

Cette application est une démonstration technique simplifiée issue d'un projet plus vaste nommé **Data Collector**.

**Data Collector** est un outil de collecte et d'analyse de données massives sur le marché de l'emploi. Dans sa version complète, il a permis d'extraire et de traiter plus de **480 000 offres d'emploi** directement depuis l'API de France Travail.

### 🎯 L'Objectif Final

La collecte de ces données est la première étape d'un projet ambitieux : la création d'une plateforme destinée à cartographier le paysage des métiers en France.

L'objectif de cette future plateforme est de :
1.  **Répertorier** un maximum de métiers, qu'ils soient manuels, intellectuels, et quel que soit le niveau de qualification requis.
2.  **Analyser** les descriptions de poste pour extraire et structurer les compétences fondamentales de chaque profession.
3.  **Lister** de manière claire pour chaque métier :
    * Les **Hard Skills** (les savoir-faire techniques).
    * Les **Soft Skills** (les savoir-être et compétences humaines).

En bref, ce projet vise à offrir une vision claire et basée sur la donnée des compétences requises pour chaque métier aujourd'hui.

### 🛠️ À propos de cette Démo

Cette application web est une interface légère qui démontre la brique "collecte de données" du projet. Plutôt que de stocker les offres, elle interroge l'API France Travail en direct.

Elle permet de :
* Rechercher des offres par métier ou par code ROME.
* Filtrer les résultats par type de contrat (CDI, CDD, Intérim).
* Affiner la recherche par département.
* Choisir le nombre de résultats à afficher (10, 20, 30).

---

### ⚙️ Technologies Utilisées

* **Langage :** Python
* **Framework Web / UI :** NiceGUI
* **Appels API :** Requests