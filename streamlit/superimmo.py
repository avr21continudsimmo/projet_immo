import streamlit as st
import requests
import pandas as pd
import seaborn as sns

# selection du jeu de données
dep = st.sidebar.selectbox("Location : ", options=(69,33,13))
st.title("Analyse d'annonces immoblières ")
st.write("Obtenues sur le site superimmo.com le 8 octobre 2021 pour le département : "+str(dep))

if dep :
    # recupération des données
    df = pd.read_csv('../datas/superimmo/20211008/superimmo_20211008_'+str(dep)+'.csv',index_col=0)

    # formatage des données : prix
    df = df[-(df.prix.isna())]
    df.prix = df.prix.apply(lambda x: int(float(str(x).replace('€','').replace(' ','').replace(',','.'))))
    df.prix = df.prix.astype(int)

    # formatage des données : surface
    df = df[-(df.surface.isna())]
    df.surface = df.surface.apply(lambda x: str(x).replace(' ','').replace(',','.'))
    df.surface = df.surface.astype(float)

    # calcul du prix au mettre carré
    df['pm2']=df['prix']/df['surface']

    # selection par location (alias code postal)
    loc = st.sidebar.selectbox("Location : ", options=[""]+df.location.value_counts().index.to_list())
    if loc:
        df = df[(df.location==loc)]
    else :
        # Affichage global de la répartition des biens par location si non saisie
        st.write('Répartition par code postal : ')
        st.write(df.location.value_counts())

        # Affichage global de la répartition des prix au mettre carré par location si non saisie
        st.write('Appartement prix moyen au m carré : ')
        st.write(df[(df.type=='appartement')].groupby('location').describe()['pm2'])

    # selection par type de bien
    type = st.sidebar.selectbox("type : ", options=[""]+df.type.value_counts().index.to_list())
    if type:
        df = df[(df.type==type)]
    else :
        # Répartition des biens par type si non saisie
        st.write('Répartition par type de bien ')
        st.write(df.type.value_counts())


    # affichage des données globales ou suivant filtres saisie
    st.write('Répartition par type et par code postal : ')
    st.write(pd.crosstab(df.location,df.type))

    # affichage des données globales ou suivant filtres saisie
    st.write('Détails des annonces : ')
    st.write(df)

    # Nuage de points des biens par location (si saisie) et par type (si saisie)
    st.write('Nuage de points des biens par code postal (si saisie) et par type de bien (si saisie) ')
    sns.set(rc={'figure.figsize':(30,30)})
    sns.lmplot( x="surface", y="prix", data=df, hue='type')
    st.pyplot()


