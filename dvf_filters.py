import pandas as pd
import numpy as np
#import seaborn as sns
#import matplotlib.pyplot as plt

##Import des données
df_2020 = pd.read_csv('valeursfoncieres-2020.txt', sep="|", decimal=',')
dep_reg = pd.read_csv("departements-region.csv",sep=",")
communes_littorales = pd.read_csv("communes_littorales_2019.csv", sep=";")

##DVF
#filtres
df = df_2020[(df_2020["Type local"] == "Appartement") | 
             (df_2020["Type local"] == "Maison")|
             (df_2020["Nature mutation"]=="Vente")]

#colonnes inutiles
df.drop(["Code service CH","Reference document","1 Articles CGI",
              "2 Articles CGI","3 Articles CGI","4 Articles CGI",
              "5 Articles CGI"],axis = 1, inplace=True)

#suppression des lignes dublons
df.drop_duplicates(subset = None, inplace = True)
df = df.drop_duplicates(subset = ["Date mutation","Valeur fonciere","Code postal"], keep = False)

#on enleve les prix qui sont aberrants
outliers_max = df["Valeur fonciere"].quantile(0.95)
outliers_min = df["Valeur fonciere"].quantile(0.01)
df_clean = df[(df["Valeur fonciere"] < outliers_max) & (df["Valeur fonciere"] > outliers_min) ]

#supression des surfaces aberrantes
outliers_surface_max = df_clean["Surface reelle bati"].quantile(0.9999)
outliers_surface_min = df_clean["Surface reelle bati"].quantile(0.001)
df_clean = df_clean[(df_clean["Surface reelle bati"] < outliers_surface_max) & (df_clean["Surface reelle bati"] > outliers_surface_min)]

#calcul du prix au m2
df_clean["Prix m2"] = df_clean["Valeur fonciere"]/df_clean["Surface reelle bati"]

#gestion des arrondissements de Paris, Lyon et Marseille
df_clean["Commune2"] = df_clean["Commune"]
dico = {"Commune2":{"PARIS 01":"PARIS","PARIS 02":"PARIS",
                              "PARIS 03":"PARIS",
                              "PARIS 04":"PARIS",
                              "PARIS 05":"PARIS",
                              "PARIS 06":"PARIS",
                              "PARIS 07":"PARIS",
                              "PARIS 08":"PARIS",
                              "PARIS 09":"PARIS",
                              "PARIS 10":"PARIS",
                              "PARIS 11":"PARIS",
                              "PARIS 12":"PARIS",
                              "PARIS 13":"PARIS",
                              "PARIS 14":"PARIS",
                              "PARIS 15":"PARIS",
                              "PARIS 16":"PARIS",
                              "PARIS 17":"PARIS",
                              "PARIS 18":"PARIS",
                              "PARIS 19":"PARIS",
                              "PARIS 20":"PARIS",
                              "MARSEILLE 1ER":"MARSEILLE",
                              "MARSEILLE 2EME":"MARSEILLE",
                              "MARSEILLE 3EME":"MARSEILLE",
                              "MARSEILLE 4EME":"MARSEILLE",
                              "MARSEILLE 5EME":"MARSEILLE",
                              "MARSEILLE 6EME":"MARSEILLE",
                              "MARSEILLE 7EME":"MARSEILLE",
                              "MARSEILLE 8EME":"MARSEILLE",
                              "MARSEILLE 9EME":"MARSEILLE",
                              "MARSEILLE 10EME":"MARSEILLE",
                              "MARSEILLE 11EME":"MARSEILLE",
                              "MARSEILLE 12EME":"MARSEILLE",
                              "MARSEILLE 13EME":"MARSEILLE",
                              "MARSEILLE 14EME":"MARSEILLE",
                              "MARSEILLE 15EME":"MARSEILLE",
                              "LYON 1ER":"LYON",
                              "LYON 2EME":"LYON",
                              "LYON 2EME":"LYON",
                              "LYON 3EME":"LYON",
                              "LYON 4EME":"LYON",
                              "LYON 5EME":"LYON",
                              "LYON 6EME":"LYON",
                              "LYON 7EME":"LYON",
                              "LYON 8EME":"LYON",
                              "LYON 9EME":"LYON"}}
df_clean = df_clean.replace(dico)

# prix au m2 aberrants
outliers_prix = df_clean["Prix m2"].quantile(0.9999)
df_clean = df_clean[df_clean["Prix m2"] < outliers_prix]

df_clean["Paris"]= df_clean["Commune2"].apply(lambda x : 1 if x == "PARIS" else 0)

##Ajout des régions via le code département
dep_reg = dep_reg.rename(columns = {"num_dep":"Code departement"})
dico2 = {"Code departement":{"2A":"20","2B":"20"}}
dep_reg = dep_reg.replace(dico2)
dep_reg["Code departement"] = dep_reg["Code departement"].astype('int32')
df_clean = df_clean.replace(dico2)
df_clean["Code departement"] = df_clean["Code departement"].astype('int32')
df_clean = df_clean.merge(right = dep_reg , on = 'Code departement', how = 'left')

## Ajout des communes possédant une surface maritime
communes_littorales = communes_littorales.drop_duplicates(keep ="first")
df_clean = df_clean.merge(right = communes_littorales , on = 'Commune', how = 'left')
dummies = pd.get_dummies(df_clean["Classement"])
df_clean = pd.concat([df_clean, dummies],axis =1)
df_clean["Mer"] = df_clean["Mer"] .astype("object")
dico3 = {"Mer":{"1":"OUI","0":"NON"}}
df_clean = df_clean.replace(dico3)
df_clean.drop("Classement", axis = 1, inplace = True)

del communes_littorales, dep_reg, df, df_2020, dico, dico2, dico3, dummies
del outliers_max, outliers_min, outliers_prix, outliers_surface_max, outliers_surface_min
