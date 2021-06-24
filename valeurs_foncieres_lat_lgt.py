import pandas as pd
import numpy as np
from Position import Position as pos

# ajoute les coordonnées gps au df des valeurs foncières

# Chargement du jeu de données
#df=pd.read_csv('datas/valeursfoncieres-2020.csv') # fichier qui contient les addressName 
df=pd.read_csv('datas/valeursfoncieres-2020_gps_lat_lgt.csv')

"""
# à lancer une première fois au debut pour definir les colonnes lat et lgt
# initialisation creation de la colonne gps
df['lat']=0.0
df['lgt']=0.0
df.to_csv('datas/valeursfoncieres-2020_gps_lat_lgt.csv')
"""

# dataframe filtrer à partir de df centrée des données que l'on cherche à calculer
tmp=df[-df.addressName.isna()] # retire les elements qu'on ne pourra pas calculer
tmp=tmp[tmp.lat==0.0] # permet de ne pas refaire le calcul si deja fait

#df.info()
#tmp.info()

l=5000
# regroupement les calcul par addressName
cnt = tmp.addressName.value_counts()
#cnt = tmp.addressName.value_counts() # si on veut le faire en une fois
#print(cnt)
i=0
j=0
for x in cnt.index:
    i=i+1
    print(j,i,l)
    print(x) # affiche l'adresse 
    p=pos.gpsFromAddress(x) # calcul de la localistion gps
    print(p) # affiche les coordonnées gps trouvees
    if p : # il arrive que l'on en trouve pas 
        df.loc[df['addressName']==x,'lat']=p[0]
        df.loc[df['addressName']==x,'lgt']=p[1]

        print(df[df['addressName']==x]) # observation des endroits où la sasie s'applique

    # enregistrement des resultats
    if i>=l:
        df.to_csv('datas/valeursfoncieres-2020_gps_lat_lgt.csv')
        j=j+1
        i=0
