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
        pyPredImmo est un outil qui propose les fonctionnalités suivantes :
        - **Analyse des annonces 2021** : analyse les prix de vente relevés en Octobre 2021 sur un site d'annonces immobilières (à ce jour dans les départements 13, 33 et 69)
        - **Analyse des prix officiels 2020** : analyse l'historique des prix de vente des biens immobiliers en France à partir de la base DVF (Demande de Valeurs Foncières)
        - **Prédiction de prix** : prédit si le prix d'un bien immobilier est sur-évalué ou sous-évalué par rapport au marché 2020
        """
    )
