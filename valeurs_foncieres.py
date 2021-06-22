import pandas as pd
import numpy as np
from Position import Position as pos

# Chargement du jeu de données
df=pd.read_csv('datas/valeursfoncieres-2020.txt',sep="|",decimal=",")
#df.head()
#print(df.columns)

# focus on the address datas
ad=df[['No voie', 'Type de voie', 'Voie', 'Code postal','Commune']]

# restriction a quelques elements pour test
test = ad.sample(n=3)

# cast (les codes postaux sont vus comme des float)
#   une premiere etape consiste à le transformer en int
#   puis en str pour rajouter les zeros 
#   pour les codes postaux commençant par 0 comme 012345
#   (fait avec la fonction zfill)
test['Code postal']=test['Code postal'].astype(int).astype(str)

# format addresses
# tools functions : nan values management
def escapeNan(row):
    val = str(row)
    if val == 'nan':
        val=''
    val=val.replace('.0','') # if from float values
    return val

# get addressName
test['addressName']=test.apply(lambda row: 
    escapeNan(row['No voie'])+' ' 
    +escapeNan(row['Type de voie'])+' '        
    +row['Voie']+' '
    +row['Code postal'].zfill(5)+' ' # pour respecter le format des codes postaux
    +str(row['Commune'])
    , axis = 1)

print(test)

test['gps']=test.apply(lambda row: 
    pos.gpsFromAddress(row['addressName'])
    , axis = 1)

print(test)