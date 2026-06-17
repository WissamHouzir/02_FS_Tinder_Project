from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


st.set_page_config(page_title="Speed Dating Analysis", layout="wide")
sns.set_theme(style="whitegrid")


@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "Speed_Dating_Data.csv"
    df = pd.read_csv(data_path, encoding="latin1")
    df["gender_label"] = df["gender"].map({0: "Femme", 1: "Homme"})
    df["age_gap"] = (df["age"] - df["age_o"]).abs()
    return df


def make_barplot(data, x, y, hue=None, title="", xlabel="", ylabel="", palette="Set2", rotation=0):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=data, x=x, y=y, hue=hue, palette=palette, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=rotation)
    if hue is None and ax.legend_ is not None:
        ax.legend_.remove()
    return fig


def make_countplot(data, x, title, labels, palette):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=data, x=x, hue=x, legend=False, palette=palette, ax=ax)
    ax.set_title(title)
    ax.set_xlabel("")
    ax.set_ylabel("Nombre")
    ax.set_xticks([0, 1], labels)
    return fig


df = load_data()

st.title("Speed Dating Analysis")
st.write(
    "Cette application reprend l'analyse du notebook de facon simple pour comprendre "
    "ce qui semble favoriser un match lors d'un speed dating."
)

st.sidebar.header("Navigation")
section = st.sidebar.radio(
    "Aller a une section",
    [
        "Vue d'ensemble",
        "Variable cible",
        "Preferences",
        "Decision individuelle",
        "Facteurs du match",
        "Facteurs complementaires",
        "Conclusion",
    ],
)

if section == "Vue d'ensemble":
    st.header("Vue d'ensemble du dataset")

    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre de lignes", f"{df.shape[0]}")
    col2.metric("Nombre de colonnes", f"{df.shape[1]}")
    col3.metric("Nombre de waves", f"{df['wave'].nunique()}")

    st.subheader("Apercu des donnees")
    st.dataframe(df.head())

    st.subheader("Colonnes les plus incompletes")
    missing = (df.isna().mean() * 100).sort_values(ascending=False).head(15).round(1)
    missing_df = missing.reset_index()
    missing_df.columns = ["colonne", "missing_pct"]
    st.dataframe(missing_df, use_container_width=True)

    fig = make_barplot(
        missing_df,
        x="colonne",
        y="missing_pct",
        title="Top 15 des colonnes avec valeurs manquantes",
        xlabel="Colonne",
        ylabel="% de valeurs manquantes",
        palette="rocket",
        rotation=65,
    )
    st.pyplot(fig)

    st.info(
        "Le dataset contient beaucoup de variables. Pour garder une analyse simple, "
        "on se concentre sur celles qui aident le plus a comprendre les decisions et les matches."
    )

elif section == "Variable cible":
    st.header("Comprendre la variable cible : match")

    col1, col2, col3 = st.columns(3)
    col1.metric("Taux de match", f"{df['match'].mean() * 100:.2f}%")
    col2.metric("Taux de oui", f"{df['dec'].mean() * 100:.2f}%")
    col3.metric("Taux de oui partenaire", f"{df['dec_o'].mean() * 100:.2f}%")

    left, right = st.columns(2)
    with left:
        st.pyplot(make_countplot(df, "match", "Repartition des matches", ["Non", "Oui"], "Set2"))
    with right:
        st.pyplot(make_countplot(df, "dec", "Repartition des decisions individuelles", ["Non", "Oui"], "Set1"))

    st.info(
        "Le match est rare, car il faut un accord mutuel. Dire oui seul est plus frequent que reussir a obtenir un match."
    )

elif section == "Preferences":
    st.header("Que recherchent les participants ?")

    preference_cols = ["attr1_1", "sinc1_1", "intel1_1", "fun1_1", "amb1_1", "shar1_1"]
    preferences = (
        df.groupby("gender_label")[preference_cols]
        .mean()
        .round(2)
        .T
        .rename(columns={"Femme": "Femmes", "Homme": "Hommes"})
    )

    st.dataframe(preferences, use_container_width=True)

    pref_plot = preferences.reset_index().rename(columns={"index": "critere"})
    pref_plot = pref_plot.melt(id_vars="critere", var_name="groupe", value_name="importance")

    st.pyplot(
        make_barplot(
            pref_plot,
            x="critere",
            y="importance",
            hue="groupe",
            title="Preferences declarees selon le genre",
            xlabel="Critere",
            ylabel="Importance moyenne",
            palette="Set2",
            rotation=20,
        )
    )

    st.info(
        "Les hommes declarent donner plus d'importance a l'attractivite. "
        "Les femmes declarent donner un peu plus d'importance a l'intelligence, "
        "a la sincerite et a l'ambition."
    )

elif section == "Decision individuelle":
    st.header("Qu'est-ce qui pousse une personne a dire oui ?")

    rating_cols = ["attr", "sinc", "intel", "fun", "amb", "shar", "like", "prob"]
    decision_means = df.groupby("dec")[rating_cols].mean().round(2)
    decision_means.index = ["A dit non", "A dit oui"]
    st.dataframe(decision_means, use_container_width=True)

    decision_plot = df.groupby("dec")[["attr", "sinc", "intel", "fun", "amb", "shar"]].mean().T.reset_index()
    decision_plot.columns = ["critere", "A dit non", "A dit oui"]
    decision_plot = decision_plot.melt(id_vars="critere", var_name="decision", value_name="score")
    st.pyplot(
        make_barplot(
            decision_plot,
            x="critere",
            y="score",
            hue="decision",
            title="Notes moyennes selon la decision individuelle",
            xlabel="Critere",
            ylabel="Note moyenne",
            palette="Set1",
        )
    )

    corr_dec = df[rating_cols + ["dec"]].corr(numeric_only=True)["dec"].sort_values(ascending=False)
    st.subheader("Correlation avec la decision")
    st.dataframe(corr_dec.to_frame("correlation"), use_container_width=True)

    st.info(
        "Quand une personne dit oui, toutes les notes sont plus elevees. "
        "L'attractivite ressort fortement, mais le fun, l'intelligence, la sincerite "
        "et les interets communs comptent aussi."
    )

elif section == "Facteurs du match":
    st.header("Qu'est-ce qui favorise un match ?")

    rating_cols = ["attr", "sinc", "intel", "fun", "amb", "shar", "like", "prob"]
    match_means = df.groupby("match")[rating_cols].mean().round(2)
    match_means.index = ["Pas de match", "Match"]
    st.dataframe(match_means, use_container_width=True)

    match_plot = df.groupby("match")[["attr", "sinc", "intel", "fun", "amb", "shar"]].mean().T.reset_index()
    match_plot.columns = ["critere", "Pas de match", "Match"]
    match_plot = match_plot.melt(id_vars="critere", var_name="statut", value_name="score")
    st.pyplot(
        make_barplot(
            match_plot,
            x="critere",
            y="score",
            hue="statut",
            title="Notes moyennes selon la presence d'un match",
            xlabel="Critere",
            ylabel="Note moyenne",
            palette="viridis",
        )
    )

    corr_match = df[rating_cols + ["match"]].corr(numeric_only=True)["match"].sort_values(ascending=False)
    st.subheader("Correlation avec le match")
    st.dataframe(corr_match.to_frame("correlation"), use_container_width=True)

    st.info(
        "Les matches apparaissent surtout quand la rencontre est bien notee sur plusieurs dimensions. "
        "L'appreciation globale, l'attractivite, le fun et les interets communs sont parmi les facteurs les plus visibles."
    )

elif section == "Facteurs complementaires":
    st.header("Deux facteurs complementaires")

    left, right = st.columns(2)

    with left:
        st.subheader("Ecart d'age")
        age_gap = df.groupby("match")["age_gap"].mean().round(2)
        age_gap.index = ["Pas de match", "Match"]
        st.dataframe(age_gap.to_frame("age_gap_moyen"), use_container_width=True)

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df, x="match", y="age_gap", hue="match", legend=False, palette="pastel", ax=ax)
        ax.set_title("Ecart d'age selon le match")
        ax.set_xlabel("Match")
        ax.set_ylabel("Ecart d'age")
        ax.set_xticks([0, 1], ["Non", "Oui"])
        st.pyplot(fig)

    with right:
        st.subheader("Variable samerace")
        same_race = df.groupby("samerace", dropna=True)["match"].mean().round(3).reset_index()
        st.dataframe(same_race, use_container_width=True)

        fig = make_barplot(
            same_race,
            x="samerace",
            y="match",
            title="Taux de match selon samerace",
            xlabel="Same race",
            ylabel="Taux de match",
            palette="Set2",
        )
        fig.axes[0].set_xticks([0, 1], ["Non", "Oui"])
        st.pyplot(fig)

    st.info(
        "Un ecart d'age plus faible semble legerement aider. "
        "La variable samerace semble aussi jouer un petit role, mais plus faible que les notes donnees pendant le date."
    )

else:
    st.header("Conclusion")

    st.markdown(
        """
Les idees principales a retenir sont :

1. Le taux de match est faible car il faut deux reponses positives.
2. Les preferences declarees changent un peu selon le genre.
3. L'attractivite joue un role important dans la decision individuelle.
4. Le match depend surtout d'une bonne impression globale.
5. Le fun, les interets communs et l'appreciation generale sont tres importants.
6. L'ecart d'age et `samerace` semblent avoir un effet plus limite.
"""
    )

    st.success(
        "En resume, ce qui cree un match n'est pas seulement le physique. "
        "La qualite globale de l'interaction semble tres importante."
    )
