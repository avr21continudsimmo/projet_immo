import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as img


title = "Prix moyen au m² selon les propriétés des biens"
sidebar_name = "2. Prix selon les features"


def run():

    st.title('Prix moyen au m² selon les propriétés des biens')
    st.write("A partir du scraping des annonces immobilières, nous avons cherché à connaître l'influence de chaque propriété mentionnée dans l'annonce sur le prix moyen au m²")
    st.write('Les propriétés sont identifiées sous forme de NER à partir des descriptions des annonces. S\'agissant de propriétés déclarées, le bien peut bénéficier de certaines propriétés bien que non mentionnées dans l\'annonce.')
    st.write('Par exemple, une agence qui met en vente un bien n\'indiquera pas nécessairement que l\'immeuble du bien à vendre est sans ascenseur.')

    st.write('Exemple de traitement de description d\'annonce :')
    
    image = img.imread('../../models/exemple_NER.png')
    st.image(image, width = 750)
    
    st.subheader('Prix moyen au m² selon les propriétés et le type de bien :')
    
    recap_annonces = pd.read_csv('../../models/recap_annonces.csv')
    liste_features = sorted(list(set(recap_annonces['feature'])))
        
    for i, c in enumerate(liste_features):
        
        fig, ax = plt.subplots()

        st.subheader(c)    
        
        for j, b in enumerate(['Tous Biens', 'Appartements', 'Maisons']):            
            
            df_recap = recap_annonces[(recap_annonces['feature'] == c) & (recap_annonces['type_local'] == b)]
            
            plt.subplot(1, 3, j + 1)
            plt.title(b)
            plt.yticks([])
            plt.ylabel('Prix moyen au m²')
            plt.bar(df_recap['feature_binary'], df_recap['prix_m2'])
            plt.ylim(ymax = 1.25 * max(df_recap['prix_m2']))
    
            for k, v in enumerate(df_recap['prix_m2']):
                plt.text(k - 0.25, v + max(df_recap['prix_m2']) / 20, round(v, 0), fontsize = 10, fontweight = 'bold')
                
            st.write(df_recap.drop(columns = {'Unnamed: 0'}))

        st.pyplot(fig)
    
