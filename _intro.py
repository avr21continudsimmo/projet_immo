import streamlit as st


title = "pyPredImmo"
sidebar_name = "Introduction"


def run():

    # TODO: choose between one of these GIFs
    st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/1.gif")
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/2.gif")
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/3.gif")

    st.title(title)

    st.markdown("---")

    st.markdown(
        """
        pyPredImmo est un outil codé en Python qui a pour objectif de répondre à la question : **le bien immobilier que je souhaite acheter est-il une bonne affaire ?**
        
        Pour cela, nous avons développé cet outil qui propose les fonctionnalités suivantes :
        - **Analyse des annonces 2021** : visualisation des prix de vente relevés en Octobre 2021 sur un site d'annonces immobilières (à ce jour dans les départements 13, 33 et 69)
        - **Analyse de l'influence des spécificités des biens** : les descriptions des annonces font l'objet d'extraction d'entités nommées (NER), qui sont ensuite mises en relation avec le prix au m²
        - **Analyse des prix officiels 2020** : visualisation des prix de vente des biens immobiliers en France à partir de la base DVF 2020 (Demande de Valeurs Foncières)
        - **Prédiction de prix** : prédit si le prix d'un bien immobilier est sur-évalué ou sous-évalué par rapport au marché 2020
        """
    )
