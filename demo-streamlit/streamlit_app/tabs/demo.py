import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as img

from joblib import load

import streamlit as st

from tabs.functions.features_map import features_map

title = "demo"
sidebar_name = "4. Démo du modèle"

def run():

    st.title('pyPredImmo - Votre futur bien immobilier est-il une bonne affaire ?')
    
    
    # Applique-t-on le bonus/malus ?
    application_bonus = 1    # On décide de le désactiver car les résultats ne sont pas OK
                             # La prédiction ne sera alors basée que sur le modèle A
                             # Il est toutefois possible de l'activer pour voir ce que cela donne
                             
    image = img.imread('models/demo.png')
    
    
    
    # Renseigner ici les propriétés du bien
    # st.subheader("Propriétés du bien")
    
    form = st.form("Propriétés du bien")
    
    prix_annonce = form.number_input("Prix du bien (hors frais d'agence) en euros : ", value = 399000, min_value = 0, max_value = 2000000, step = 5000)
    
    rue = form.text_input("Nom de la rue :", value = 'rue Montaigne')
    cp = form.number_input("Code postal à 5 chiffres:", value = 33170, min_value = 1000, max_value = 99000)
    ville = form.text_input("Ville:", value = "Gradignan")
    
    surface = form.number_input("Surface du bien (m²): ", value = 114, min_value = 0, max_value = 5000, step = 5)
    surface_terrain = form.number_input("Surface du terrain (m²): ", value = 846, min_value = 0, max_value = 100000, step = 100, help = "Indiquer 0 si appartement ou pas de terrain")
    type_local_str = form.radio('Type de bien :', options = ['Appartement', 'Maison'])
    
    nb_pieces = form.number_input("Nombre de pièces : ", value = 5, min_value = 1, max_value = 20, step = 1)
    nb_chambres = form.number_input("Nombre de chambres : ", value = 4, min_value = 0, max_value = 20, step = 1)
    mer_str = form.radio('Le bien est-il près de la mer (< 20 kms) :', options = ['Oui', 'Non'])
    
    date_construction = form.number_input("Quand a été construit le bien ?", value = 1987, min_value = 1800, max_value = 2022)
    conso_energie = form.number_input("Quelle est la consommation énergétique du bien ?", value = 187, min_value = 0, max_value = 2000, help = 'de < 50 (classe A économe) à > 450 (classe G énergivore)')
    estim_ges = form.number_input("Quelle est la note GES du bien (kg eq. CO2 / m² / an) ?", value = 6, min_value = 0, max_value = 500, help = 'de <=5 (faible émission GES) à > 80 (forte émission GES)')
    
    extra_features = form.multiselect("Quelles sont les spécificités du bien ?", 
                                    help = "Vous pouvez sélectionner aucune, une ou plusieurs spécificités",
                                    options = ['Exposition Sud', 'Lumineux', 'Calme', 'Beaux volumes', 
                                               'Standing', 'Charme', 'Mezzanine', 'Avec Ascenseur', 
                                               'Sans Ascenseur', 'Duplex', 'Dernier étage', 'Premier étage', 'Deuxième étage', 'Troisième étage', 
                                               'Quatrième étage', 'Cinquième étage', 'Sixième étage', 'Septième étage', 'Huitième étage', 'RDC', 'Design', 
                                               'Terrasse', 'Parfait état', 'Travaux à prévoir', 'Proche commodités', 'Vue dégagée', 'Sécurisé', 'Emplacement', 
                                               'Atypique', 'Proche de la nature', 'Meublé', 'Cave', 'Parking', 'Cuisine américaine', 'Investissement locatif', 
                                               'Proche écoles', 'Dressing', 'Plain Pied', 'Garage', 'Grange', 'Buanderie', 'Dépendance'])
    
                                    
    form.form_submit_button("Valider")
    
    # Retraitement des features
    
    if date_construction > 2021:
        anciennete = 0
    else: 
        anciennete = 2021 - date_construction
    
    if (str(cp)[0:2] == "75") & (len(str(cp)) == 5):
        paris = 1
    else:
        paris = 0
    
    if mer_str == "Oui":
        mer = 1
    else:
        mer = 0
    
    if type_local_str == "Appartement":
        type_local = 0
    else:
        type_local = 1
    
    
    # Chargement des modèles A
    model_A_all = load('../../models/model_rf_all.pkl')
    model_A_appart_province = load('../../models/model_rf_1_appart_province.pkl')
    model_A_appart_paris = load('../../models/model_rf_2_appart_paris.pkl')
    model_A_maison_province = load('../../models/model_rf_3_maison_province.pkl')
    model_A_all_XGB = load('../../models/model_xgb_all.pkl')
    model_A_all_Linear = load('../../models/model_lr_all.pkl')
    
    
    # Chargement de la liste des features requis pour faire tourner le modèle
    df_feat = pd.read_csv('../../models/features_list_for_model_A.csv', index_col = 0)
    
    
    # Complétion des informations
    
    from geopy.geocoders import Nominatim
    
    adresse = rue + " " + str(cp) + " " + ville
    code_dep = str(cp)[0:2]
    
    geolocator = Nominatim(user_agent="pyPredImmo")
    
    try:
        location = geolocator.geocode(adresse, country_codes = 'fr', timeout = 5)
        lon = round(location.longitude, 2)
        lat = round(location.latitude, 2)
        #st.write(adresse + " ===> " + str(lat) + "," + str(lon))
    
    except:
        st.write('L\'adresse du bien n\'a pas été trouvée')
    
    prix_m2_commune = pd.read_csv('../../models/prix_m2_commune.csv', dtype = {'Code postal': int})
    prix_m2_gps = pd.read_csv('../../models/prix_m2_gps.csv')
    
    prix_m2_commune_bien = prix_m2_commune[(prix_m2_commune['Code postal'] == cp) & (prix_m2_commune['Type local'] == type_local_str)]
    prix_m2_commune_bien_val = prix_m2_commune_bien['Prix m2'].iloc[0]
    #st.write(prix_m2_commune_bien_val)
    
    prix_m2_gps_bien = prix_m2_gps[(prix_m2_gps['lon_2'] == lon) & (prix_m2_gps['lat_2'] == lat) & (prix_m2_gps['Type local'] == type_local_str)]
    prix_m2_gps_bien_val = prix_m2_gps_bien['Prix m2'].iloc[0]
    #st.write(prix_m2_gps_bien_val)
    
    # Recherche du loyer, population et revenus
    df_other_feat = pd.read_csv('../../models/loy_rev_pop.csv', dtype = {'Code postal': int}, index_col = 0)
    df_other_feat_bien = df_other_feat[(df_other_feat['Code postal'] == cp) & (df_other_feat['Type local'] == type_local_str)]
    #st.write(df_other_feat_bien)
    loyer = df_other_feat_bien['loyer'].iloc[0]
    pop = df_other_feat_bien['Population totale'].iloc[0]
    SNHMO18 = df_other_feat_bien['SNHMO18'].iloc[0]
    SNHMFO18 = df_other_feat_bien['SNHMFO18'].iloc[0]
    
    
    # Récupération du code IRIS et des équipements du quartier IRIS
    iris = pd.read_csv('../../databases/inter/02 - export_gps_iris_ALL_2020.csv')
    possible_iris = iris[(iris['Adresse'].str.contains(rue.upper())) & (iris['Adresse'].str.contains(ville.upper()))
                        & (-iris['code_iris_clean'].isna())]
    
    if possible_iris.shape[0] == 0:
        possible_iris = iris[iris['Adresse'].str.contains(ville.upper()) & (-iris['code_iris_clean'].isna())]
    
    iris_annonce = int(possible_iris['code_iris_clean'].iloc[0])
    
    bpe = pd.read_csv('../../databases/inter/03A - equipements_nb_clean.csv')
    
    if iris_annonce == 0:
        college_lycee = 0
        creche = 0
        ecole = 0
        ecole_sup = 0
        gare = 0
        hotels = 0
        info_tour = 0
        police = 0
        salle_sport = 0
    else:    
        college_lycee = int(bpe[bpe['code_iris_clean'] == iris_annonce]['Collège ou lycée'])
        creche = int(bpe[bpe['code_iris_clean'] == iris_annonce]['Crèche'])
        ecole = int(bpe[bpe['code_iris_clean'] == iris_annonce]['Ecole mat et primaire'])
        ecole_sup = int(bpe[bpe['code_iris_clean'] == iris_annonce]['Ecole sup'])
        gare = int(bpe[bpe['code_iris_clean'] == iris_annonce]['Gare'])
        hotels = int(bpe[bpe['code_iris_clean'] == iris_annonce]['Hotels'])
        info_tour = int(bpe[bpe['code_iris_clean'] == iris_annonce]['Info touristique'])
        police = int(bpe[bpe['code_iris_clean'] == iris_annonce]['Police ou gendarmerie'])
        salle_sport = int(bpe[bpe['code_iris_clean'] == iris_annonce]['Salle multisport'])
    
    
    # Récap des propriétés du bien pour prédiction du modèle A et calcul des prédictions
    
    annonce_proprietes_A = [surface_terrain, surface, type_local, nb_pieces, paris, mer, prix_m2_commune_bien_val, 
                            prix_m2_gps_bien_val, college_lycee, creche, ecole, ecole_sup, gare, hotels, info_tour, police, 
                            salle_sport, anciennete, conso_energie, estim_ges, loyer, SNHMO18, SNHMFO18, pop]
    
    annonce_proprietes_A = np.array(annonce_proprietes_A).reshape(1, df_feat.shape[0])
    
    pred_model_A_all = int(model_A_all.predict(annonce_proprietes_A))
    pred_model_A_appart_province = int(model_A_appart_province.predict(annonce_proprietes_A))
    pred_model_A_appart_paris = int(model_A_appart_paris.predict(annonce_proprietes_A))
    pred_model_A_maison_province = int(model_A_maison_province.predict(annonce_proprietes_A))
    pred_model_A_all_XGB = int(model_A_all_XGB.predict(annonce_proprietes_A))
    pred_model_A_all_Linear = int(model_A_all_Linear.predict(annonce_proprietes_A))
    
    
    if paris == 1:
        prix_base_A = pred_model_A_appart_paris
    elif type_local == 1:
        prix_base_A = pred_model_A_maison_province
    elif type_local == 0:
        prix_base_A = pred_model_A_appart_province
    else:
        prix_base_A = pred_model_A_all


    # Calcul du bonus / malus du modèle B
    
    # Chargement des modèles B
    model_B_maison = load('../../models/model_features_maison.pkl')
    model_B_appart = load('../../models/model_features_appart.pkl')
    
    # Chargement de la liste des features requis pour faire tourner le modèle
    df_feat_b = pd.read_csv('../../models/features_list_for_model_B.csv', index_col = 0)
    
    # Remplissage des paramètres à partir du multi-select extra_features
    Exposition_Sud, Lumineux, Calme, Volume, Standing, Charme, Mezzanine, Avec_Ascenseur, Sans_Ascenseur, Duplex, Dernier_etage, Premier_etage, Deuxieme_etage, Troisieme_etage, Quatrieme_etage, Cinquieme_etage, Sixieme_etage, Septieme_etage, Huitieme_etage, RDC, Design, Terrasse, Parfait_etat, Travaux, Proche_commodites, Vue_degagee, Securise, Emplacement, Atypique, Nature, Meuble, Cave, Parking, Cuisine_americaine, Investissement_locatif, Proche_ecoles, Dressing, Plain_Pied, Garage, Grange, Buanderie, Dependance = features_map(extra_features)   
    
    annonce_proprietes_B = [type_local,
       Exposition_Sud, Lumineux, Calme, Volume, Standing, Charme,
       Mezzanine, Avec_Ascenseur, Sans_Ascenseur, Duplex,
       Dernier_etage, Premier_etage, Deuxieme_etage, Troisieme_etage,
       Quatrieme_etage, Cinquieme_etage, Sixieme_etage, Septieme_etage,
       Huitieme_etage, RDC, Design, Terrasse, Parfait_etat,
       Travaux, Proche_commodites, Vue_degagee, Securise,
       Emplacement, Atypique, Nature, Meuble, Cave, Parking,
       Cuisine_americaine, Investissement_locatif, Proche_ecoles,
       Dressing, Plain_Pied, Garage, Grange, Buanderie,
       Dependance]
    annonce_proprietes_B = np.array(annonce_proprietes_B).reshape(1, df_feat_b.shape[0])

    if type_local == 1:
        bonus_malus_B = model_B_maison.predict(annonce_proprietes_B)
    else:
        bonus_malus_B = model_B_appart.predict(annonce_proprietes_B)
    
    if bonus_malus_B > 0:
        bonus_malus_B_str = "+" + "{0:.2%}".format(float(bonus_malus_B))
    else:
        bonus_malus_B_str = "{0:.2%}".format(float(bonus_malus_B))
    
    if application_bonus == 1:
        prix_predict_final = prix_base_A * (1 + (bonus_malus_B))
    else:
        prix_predict_final = prix_base_A


    # Fonction qui détermine la jauge affichée en fonction de la différence entre prédiction et prix de l'annonce
    
    def analyse_prix(prix_annonce, prix_predict_final):
        
        diff = prix_annonce / prix_predict_final - 1
    
        if diff > 0.1:
            st.image('../../models/jauge_1.png')
        elif diff > 0.05:
            st.image('../../models/jauge_2.png')
        elif diff > -0.05:
            st.image('../../models/jauge_3.png')
        elif diff > -0.1:
            st.image('../../models/jauge_4.png')
        else:
            st.image('../../models/jauge_5.png')

    
    # Affichage des résultats
    
    st.subheader('Analyse du prix du bien')
    
    st.write("Prix de l'annonce :", int(prix_annonce), "€", "(prix au m² : ", round(int(prix_annonce) / surface, 0), "€)")
    st.write("Prédiction de prix :", int(prix_predict_final), "€", "(prix au m² : ", round(int(prix_predict_final) / surface, 0), "€)")
    st.write('\n')
    st.write("Résultat :")
    analyse_prix(prix_annonce, prix_predict_final)

    st.subheader('Décomposition de la prédiction de prix')
    st.write("Prédiction du prix de base (modèle basé sur la base DVF): ", prix_base_A, "€")
    st.write("Prédiction du bonus/malus basé sur les spécificités du bien (modèle basé sur les annonces immo): ", bonus_malus_B_str)


    
    st.subheader('Comparaison des modèles de prédiction')
    
    fig, ax = plt.subplots()
    model_list = ['Random Forest Général (RF)', 'RF Appartement Province)', 'RF (Appartement Paris)', 'RF (Maison Province)', 'XGBoost', 'Régression Linéaire']
    pred_list = [pred_model_A_all, pred_model_A_appart_province, pred_model_A_appart_paris, pred_model_A_maison_province, pred_model_A_all_XGB, pred_model_A_all_Linear]
    
    ax.bar(model_list, pred_list, orientation = "vertical")
    plt.xlabel('Modèle utilisé')
    plt.ylabel('Prédiction de prix (€)')
    plt.xticks(fontsize = 8, rotation = 'vertical')
    plt.yticks(fontsize = 8)
    plt.ylim(ymax = max(pred_list) + 0.1 * max(pred_list))
    
    for i, v in enumerate(pred_list):
        plt.text(i - .35, v + max(pred_list) / 100, str(v))
    
    st.pyplot(fig)
   
    
        
        