# Speed Dating Project

## Presentation

Ce projet est une analyse exploratoire de donnees sur des evenements de speed dating.
L'objectif est de comprendre, de facon simple, quels facteurs semblent favoriser un match entre deux personnes.

Le rendu principal est un notebook Jupyter qui contient :

- une exploration du dataset,
- des statistiques descriptives,
- des visualisations,
- des interpretations courtes et simples.

Une application Streamlit a aussi ete ajoutee pour presenter cette analyse dans une interface plus simple a parcourir.

## Fichiers presents dans le projet

- [02-Speed_Dating_Analysis.ipynb](/Users/wissamhouzir/Desktop/FS_Projects/02_FS_Tinder_Project/02-Speed_Dating_Analysis.ipynb) : notebook principal avec l'analyse
- [app.py](/Users/wissamhouzir/Desktop/FS_Projects/02_FS_Tinder_Project/app.py) : application Streamlit de l'analyse
- [Speed_Dating_Data.csv](/Users/wissamhouzir/Desktop/FS_Projects/02_FS_Tinder_Project/Speed_Dating_Data.csv) : dataset utilise
- [requirements.txt](/Users/wissamhouzir/Desktop/FS_Projects/02_FS_Tinder_Project/requirements.txt) : dependances Python necessaires

## Environnement

Un dossier `.venv` est deja present dans le projet, mais si besoin on peut recreer un environnement virtuel propre avec :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ouvrir le notebook

```bash
jupyter notebook
```

Puis ouvrir `02-Speed_Dating_Analysis.ipynb`.

Le notebook contient deja les cellules de code, les graphiques et les sorties d'analyse.

## Lancer l'application Streamlit

```bash
streamlit run app.py
```

L'application permet de naviguer simplement entre les grandes parties de l'analyse :

- vue d'ensemble du dataset,
- variable cible `match`,
- preferences des participants,
- facteurs de decision,
- facteurs du match,
- conclusion.

## Ce que contient l'analyse

Le notebook repond aux consignes avec une approche volontairement simple autour de :

- la variable cible `match`,
- les preferences declarees par les participants,
- les criteres qui influencent un "oui",
- les variables les plus liees a un match,
- quelques facteurs complementaires comme l'ecart d'age et `samerace`.

## Resultats principaux

Les conclusions principales du projet sont les suivantes :

- le taux de match est faible, car il faut un accord mutuel,
- l'attractivite joue un role important dans la decision individuelle,
- le match depend aussi d'une bonne impression globale,
- le fun, les interets communs et l'appreciation generale comptent beaucoup,
- l'ecart d'age et `samerace` semblent avoir un effet plus limite.

## Choix du projet

Le travail a ete garde simple pour rester coherent avec une approche de data scientist debutant.
