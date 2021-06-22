import pandas as pd
import numpy as np

# Chargement du jeu de données
df=pd.read_csv('datas/valeursfoncieres-2020.txt',sep="|",decimal=",")
#df.head()
#print(df.columns)

# get adressses
ad=df[['No voie', 'Type de voie', 'Voie', 'Code postal','Commune']]

# format addresses
# tools functions : nan values management
# escape nan values
def escapeNan(row):
    val = str(row)
    if val == 'nan':
        val=''
    val=val.replace('.0','') # if from float values
    return val

# restriction quelques elements pour test
test = ad.sample(n=3)

# cast
test['Code postal']=test['Code postal'].astype(int).astype(str)

test['addressName']=test.apply(lambda row: 
    escapeNan(row['No voie'])+' ' 
    +escapeNan(row['Type de voie'])+' '        
    +row['Voie']+' '
    +row['Code postal'].zfill(5)+' '
    +str(row['Commune'])
    , axis = 1)

print(test)
