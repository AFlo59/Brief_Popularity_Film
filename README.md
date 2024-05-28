# Brief_Popularity_Film
https://docs.google.com/document/d/1h7zXfZPCQWwzGSPq86XTDMQ9EpuFU0KU2U-AwzIBp-Y/edit
https://www.canva.com/design/DAGDOPbUcKw/nE3kDhMeCVzk78CB65xq0g/edit

Prédire la popularité d’un film - Projet Simplon DEV IA Valenciennes
Contexte

Le cinéma "New is always better" souhaite développer un outil d’aide à la décision pour sélectionner les films à projeter. Actuellement, le gérant sélectionne les films en se basant sur des festivals et son intuition. Pour automatiser ce processus, une application utilisant l'intelligence artificielle (IA) sera mise en place pour estimer la fréquentation des films lors de leur première semaine de sortie.
Objectif

Développer un outil permettant de prédire le nombre de spectateurs pour les nouvelles sorties cinématographiques, afin d'optimiser la programmation hebdomadaire et maximiser les revenus du cinéma.
Fonctionnalités Clés de l’Application

    Estimation du potentiel des films :
        Estimer le nombre d'entrées nationales pour chaque film.
        Calculer le potentiel d’audience du cinéma en utilisant une règle de 1/2000ème.

    Sélection et programmation des films :
        Le film avec l’estimation d’audience la plus élevée est alloué à la salle 1 (120 places).
        Le second film à la salle 2 (80 places).

    Calcul de la recette et de l’audience quotidienne :
        Estimation des recettes hebdomadaires en multipliant le nombre d'entrées par le prix moyen d'une place (10 euros).
        Prise en compte des frais fixes hebdomadaires (4900 euros).

    Interface utilisateur :
        Tableau de bord affichant les prévisions et les films sélectionnés.
        Statistiques financières et taux d’occupation des salles.
        Historique des prédictions et comparaison avec les chiffres réels.

Technologies Utilisées

    Langages : Python, Django
    Frameworks : FastAPI, Django, Tailwind CSS
    Outils de gestion : Jira, MLflow, Azure Machine Learning Studio
    Scraping : Scrapy
    Automatisation : Airflow, Cronjob
    Conteneurisation : Docker

Architecture de l'Application

    Modèle de Machine Learning :
        Algorithme de régression pour prédire les entrées des films.
        Utilisation de features tels que le genre, la renommée des acteurs/réalisateurs, les occurrences sur les réseaux sociaux, etc.
        Gestion des expériences avec MLflow.

    Backend :
        API de machine learning exposée avec FastAPI.
        Base de données transactionnelle pour le fonctionnement de l'application et une base de données analytique pour les données du modèle.

    Frontend :
        Application web avec Django, affichant les prévisions, les films sélectionnés et les statistiques financières.

Gestion de Projet Agile

    Méthodologie Agile :
        4 sprints de 1 semaine chacun.
        Rituels agiles : daily meetings, sprint reviews, rétrospectives.
        Jira pour le suivi des user stories et synchronisation avec GitHub.

    Rôles dans l’équipe :
        Scrum Master : Garant des processus agiles, organise les rituels.
        Product Owner : Représente les intérêts du client, gère le Product Backlog, rédige le cahier des charges fonctionnel.
        Développeurs : Mise en œuvre technique, alternance des rôles de Scrum Master et Product Owner chaque sprint.

Livrables

    Cahier des charges fonctionnel.
    Modèle de machine learning.
    Exploration des données (EDA).
    API exposant le modèle.
    Application web (dashboard).
    Code source versionné sur GitHub.
    Support de présentation.

Critères de Performance

    Précision des prédictions du modèle.
    Qualité de l’implémentation de l’API et de l’application web.
    Respect des exigences fonctionnelles, méthodologiques et techniques.
    Interaction avec le client et respect des délais.

Planning des Sprints

    Sprint 1 :
        Cahier des charges fonctionnel.
    Sprint 2 :
        Modèle de machine learning.
    Sprint 3 :
        Première version de l’outil.
    Sprint 4 :
        Présentation finale de l’outil.

Conclusion

Ce projet vise à automatiser et optimiser la sélection des films pour un cinéma grâce à l’intelligence artificielle, en utilisant une approche agile pour garantir la qualité et l’adaptabilité du développement. Les technologies choisies et les méthodologies mises en œuvre permettront d'atteindre les objectifs fixés tout en assurant une gestion efficace du projet.
