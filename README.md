# Projet Speed Dating

## Présentation

Dans ce projet, j'ai analysé un jeu de données sur des événements de speed dating.
L'objectif était de mieux comprendre ce qui peut influencer un match entre deux personnes.

J'ai travaillé principalement dans un notebook Jupyter, avec des visualisations et quelques conclusions simples. J'ai aussi ajouté une petite application Streamlit pour rendre l'analyse plus claire à parcourir.

## Contenu du projet

- `02-Speed_Dating_Analysis.ipynb` : notebook principal avec l'analyse
- `app.py` : application Streamlit
- `Speed_Dating_Data.csv` : jeu de données utilisé
- `requirements.txt` : dépendances Python

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancer le notebook

```bash
jupyter notebook
```

Ouvrir ensuite `02-Speed_Dating_Analysis.ipynb`.

## Lancer l'application

```bash
streamlit run app.py
```

Application déployée sur Hugging Face Spaces :
https://huggingface.co/spaces/WissamH/Speed_Dating_Dashboard

## Résumé de l'analyse

Je me suis concentré sur la variable `match`, les préférences des participants et les critères qui influencent la décision finale.

Les résultats montrent que le taux de match reste assez faible, car les deux personnes doivent dire oui. L'attractivité, l'impression générale, le fun et les intérêts communs semblent jouer un rôle important. D'autres éléments comme l'écart d'âge ou `samerace` ont l'air d'avoir un effet plus limité.
