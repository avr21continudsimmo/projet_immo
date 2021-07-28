
import pandas as pd 
import numpy as np
from sklearn import model_selection, preprocessing
from sklearn.model_selection import cross_val_predict, cross_val_score, cross_validate
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
from sklearn.metrics import mean_squared_error


#df = pd.read_csv("06 - dvf_with_equip_loyers_revenus_2020v2.csv")
df = pd.read_csv("06 - dvf_with_equip_loyers_2020.csv")

#On garde la france metropolitaine
df = df[(df["Code departement"] != 971)&
        (df["Code departement"] != 972)&
        (df["Code departement"] != 973)&
        (df["Code departement"] != 974)]

#on intègre les salaires
salaire = pd.read_csv("salaire.csv",sep=";",decimal=",",dtype = {'Code departement': int})
salaire = salaire[['SNHMO18','SNHMFO18',"Code departement"]]
df = df.merge(salaire, on = "Code departement", how = 'left')
del salaire
# data_clean = df[["Valeur fonciere",'SNHMO18','SNHMFO18']]
# cor = data_clean.corr()
# fig, ax = plt.subplots(figsize=(12,12))
# sns.heatmap(cor, ax= ax, cmap="coolwarm");
# del data_clean

#on intègre la population par commune
population = pd.read_csv("population.csv", sep =";", dtype = {'Population municipale': int,
                                                              'Population comptee a part':int,
                                                              'Population totale':int,
                                                              'Code commune INSEE':int})
population = population[["Population totale",'Code commune INSEE']]
df = df.merge(population, on = "Code commune INSEE", how = 'left')
del population

df.drop(['Unnamed: 0', 'Date mutation','Type de voie','Nombre de lots',
         'Code commune INSEE', 'Adresse', 'Prix m2','lon', 'lat', 'Code postal 5 chiffres',
         'code_iris_clean','Code departement','Commune'], axis = 1, inplace = True)


df.isna().sum(axis = 0)
df = df.fillna(0)

sns.pairplot(df, diag_kind = "hist");

objet = df[["Type local","dep_name","region_name"]]
df.drop(["Type local","dep_name","region_name"], axis = 1, inplace = True)

df = df.join(pd.get_dummies(objet))
del objet



target = df["Valeur fonciere"]
data = df.drop("Valeur fonciere",axis = 1)


X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=789)


lr = LinearRegression()
lr.fit(X_train,y_train)
y_pred = lr.predict(X_test)
print("Coefficient de détermination du modèle :", lr.score(X_train, y_train))
print('Score de l ensemble de test', lr.score(X_test,y_test))

voir = np.concatenate([pd.DataFrame(y_test),pd.DataFrame(y_pred)],axis = 1)


np.sqrt(mean_squared_error(y_test, y_pred))



