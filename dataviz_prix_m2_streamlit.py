# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import streamlit as st
import os

st.title('Prix au m2 par Commune')

df = pd.read_csv('valeursfoncieres-2020.txt',sep="|", decimal=",", 
                 dtype = {'Code departement': 'str', 'Code commune': 'str', "Code postal": 'str',
                         'Code voie': 'str', 'No Volume': 'str', '1er lot': 'str', '2eme lot': 'str', '3eme lot': 'str', 
                         'Nature culture speciale': 'str'})

# ------ Traitement du dataframe Valeurs Foncieres ------

# Suppression des colonnes inutiles
df = df.drop(columns = {'Code service CH', '1 Articles CGI', '2 Articles CGI', '3 Articles CGI', '4 Articles CGI', 
                   '5 Articles CGI', 'Nature culture', 'Nature culture speciale', 'Prefixe de section', 
                   'Section', 'No plan', 'No Volume', '1er lot', 'Surface Carrez du 1er lot', '2eme lot', 
                        'Surface Carrez du 2eme lot', '3eme lot', 'Surface Carrez du 3eme lot', '4eme lot', 
                        'Surface Carrez du 4eme lot', '5eme lot', 'Surface Carrez du 5eme lot', 'Nombre de lots',})

# On ne conserve que les Ventes de Maison et Appartement
df = df[df['Nature mutation'] == "Vente"]
df = df[(df['Type local'] == "Maison") | (df['Type local'] == "Appartement")]

# Suppression des lignes duplicates
df = df.drop_duplicates()

# Suppression des transactions identifiées comme doublon (1 transaction à 12M€ par exemple répétée plusieurs fois car plusieurs signataires d'un même bien)
df = df.drop_duplicates(subset = ["Date mutation","Valeur fonciere","Code postal"], keep = False)

# Suppression des transactions supérieures à 5M€
df = df[df['Valeur fonciere'] < 5000000]

# Ajout des 0 manquants aux codes communes et création du champ "DEPCOM" (Code Commune INSEE à 5 chiffres)
df['Code commune'] = df['Code commune'].apply(lambda x: x.zfill(3))
df['DEPCOM'] = df['Code departement'] + df['Code commune']
df.head()


# ------ Calcul du prix moyen au m2 ------

# Calcul du prix moyen au m2
df['prix_m2'] = df['Valeur fonciere'] / df['Surface reelle bati']

# Suppression des lignes sans prix_m2
df = df[-df['prix_m2'].isna()]

type_bien = st.radio('', options = ['Maisons', 'Appartements', 'Maisons et Appartements'])
dep = st.text_input('Département', value = '75')
dep = str(dep)

# Maison only
if type_bien == "Maisons": 
    prix_moyen_commune = df[df['Type local'] == "Maison"].groupby(['DEPCOM', 'Code postal', 'Commune'])['prix_m2'].mean().reset_index()

# Appartement only
elif type_bien == "Appartements":
    prix_moyen_commune = df[df['Type local'] == "Appartement"].groupby(['DEPCOM', 'Code postal', 'Commune'])['prix_m2'].mean().reset_index()

# Maison ET Appartement
elif type_bien == "Maisons et Appartements":
    prix_moyen_commune = df.groupby(['DEPCOM', 'Code postal', 'Commune'])['prix_m2'].mean().reset_index()

# Suppression des valeurs aberrantes
prix_moyen_commune = prix_moyen_commune[-prix_moyen_commune['prix_m2'].isna()]
prix_moyen_commune = prix_moyen_commune[prix_moyen_commune['prix_m2'] < 20000]
prix_moyen_commune = prix_moyen_commune[prix_moyen_commune['prix_m2'] > 100]

#st.write('Communes du département ' + dep + ' avec les prix au m2 les plus élevés :')
#st.write(prix_moyen_commune[prix_moyen_commune['DEPCOM'].str.startswith(dep)].sort_values(by = 'prix_m2', ascending = False))







# ------ Création de la cartographie ------

# Import des coordonnées GPS par département pour centrer la cartographie
gps_dep = pd.read_csv('GPS_departement.csv', sep = ";")
dep_latitude = gps_dep[gps_dep['Code departement'] == dep]['Latitude']
dep_longitude = gps_dep[gps_dep['Code departement'] == dep]['Longitude']
dep_nom = gps_dep[gps_dep['Code departement'] == dep]['Nom departement']

st.write('Prix au m² des communes du département ' + dep_nom + ' (' + dep + ')')

import folium
from folium.features import GeoJson, GeoJsonTooltip, GeoJsonPopup
from streamlit_folium import folium_static
import geojson, geopandas

# Lecture des données géographiques par commune
c = geopandas.read_file("communes-20210101.shp")
c = c.drop(columns = {'wikipedia'})

# Ajout des arrondissements de Paris, Lyon et Marseille
a_all = geopandas.read_file("arrondissements-millesimes0.shp", encoding='utf-8')
a_all = a_all[['code_insee', 'superficie', 'nom_com', 'geometry']]
a_all = a_all.rename(columns = {'code_insee' : 'insee', 'superficie': 'surf_ha', 'nom_com': 'nom'})
a_all = a_all.reindex(columns=['insee','nom','surf_ha','geometry'])

# Concaténation des deux dataframes géographiques
c = pd.concat([a_all, c], axis = 0, ignore_index=True)
c = c.rename(columns = {'insee' : 'DEPCOM'})

# Suppression des codes communes correspondant à Paris, Marseille et Lyon
c = c[c['DEPCOM'] != '13055']
c = c[c['DEPCOM'] != '69123']
c = c[c['DEPCOM'] != '75056']

# Ajout du prix_m2 au dataframe
c = c.merge(prix_moyen_commune, on = "DEPCOM", how = "left")

# Arrondi du prix
c['prix_m2'] = c['prix_m2'].round(0)

# Filtre sur département choisi par l'utilisateur
c_selec = c[c['DEPCOM'].str.startswith(dep)]
c_selec.head()

with open("c_selec.geojson", "w") as f:
    geojson.dump(c_selec, f)
    
# Map

coords = (dep_latitude,dep_longitude)

f = folium.Figure(width=680, height=750)

map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=9).add_to(f)

popup = GeoJsonPopup(
    fields=['Commune','prix_m2'],
    aliases=['Commune',"Prix au m² : "], 
    localize=True,
    labels=True,
    style="background-color: yellow;",
)

tooltip = GeoJsonTooltip(
    fields=['Commune','prix_m2'],
    aliases=['Commune',"Prix au m² : "],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 1px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)

g = folium.Choropleth(
    geo_data = 'c_selec.geojson',
    name = 'choropleth',
    data = c_selec,
    columns = ['DEPCOM', 'prix_m2'], # data key/value pair
    key_on = 'feature.properties.DEPCOM', # corresponding layer in GeoJSON
    #threshold_scale = [0, 2000, 4000, 6000, 8000, 10000, 20000],
    fill_color = 'OrRd',
    fill_opacity = 0.8,
    line_opacity = 0.2,
    legend_name = 'prix_m2'
).add_to(map)

folium.GeoJson(
    'c_selec.geojson',
    style_function=lambda feature: {
        'fillColor': '#ffff00',
        'color': 'black',
        'weight': 0.2,
        'dashArray': '5, 5'
    },
    tooltip=tooltip,
    popup=popup).add_to(g)

map.save(outfile = 'map.html')

folium_static(map)
