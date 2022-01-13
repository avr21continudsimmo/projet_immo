import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

import folium
from streamlit_folium import folium_static
import re

title = "Analyse du prix des annonces"
sidebar_name = "1. Analyse des annonces"


def run():

    st.title(title)

    st.write('Les prix indiqués dans la cartographie ci-dessous correspondent à des prix issus d\'annonces immobilières qui incluent la plupart du temps les frais d\'agence')
    st.write('Le relevé a été réalisé en Octobre 2021 dans les départements 13, 33 et 69.')    
    
    st.write('Sélectionnez un département pour visualiser les prix moyens au m² des annonces immobilières : ')    
    
    dep = st.selectbox('Choix du département: ', [13, 33, 69])
    
    df = pd.read_csv('../../databases/superimmo/superimmo_20211008_' + str(dep) + '.csv')
    
    if dep == 13:
        coord_center = [43.646288, 5.0681464]
    elif dep == 33:
        coord_center = [44.837789, -0.57918]
    elif dep == 69:
        coord_center = [45.769928, 4.8292246]
    
    m = folium.Map(location = coord_center, zoom_start = 9)

    
    
    def getcp(location):
    # print(location)
        result = re.search(r".*\((.*)\)", location)
        # print(result)
        if result:
            return result.group(1)
        

    df['Code_postal'] = df.location.apply(lambda x: getcp(str(x)))
    df[(df['Code_postal'].isna())][['location','Code_postal','titre']]
    df = df[-(df['Code_postal'].isna())]

    coo=pd.read_csv('../../databases/laposte_hexasmal.csv',sep=";")
    coo.Code_postal = coo.Code_postal.astype('str')
    cpcoo={}
    for cp,coo in zip (coo['Code_postal'].to_list(),coo['coordonnees_gps'].to_list()) :
        cpcoo[cp]=coo

    def getcoo(x,cpcoo):       
        try :
            return cpcoo[x];
        except :
             return'0,0';
        
    df['gps']=df.Code_postal.apply(lambda x: getcoo(str(x),cpcoo))
    
    df = df[(df.type=='appartement')]

    df = df[-(df.prix.isna())]
    df.prix = df.prix.apply(lambda x: int(float(str(x).replace('€','').replace(' ','').replace(',','.'))))
    df.prix = df.prix.astype(int)
    
    df = df[-(df.surface.isna())]
    df.surface = df.surface.apply(lambda x: str(x).replace(' ','').replace(',','.'))
    df.surface = df.surface.astype(float)
    
    df['pm2']=df['prix']/df['surface']
    
    
    # as a folium carte
    df = df[-(df.Code_postal=='33')]
    tmp = df.groupby('Code_postal').agg({'pm2' : ['mean'],'gps':['min'],'location':['min']})
    #tmp.columns.set_levels(['pm2_mean', 'gps', 'location'], level=1, inplace = True)
    
        
    gradient40 = ['#fafa6e','#faf568','#f9f063', '#f9eb5d','#f8e658', '#f8e153','#f7dc4d','#f7d748','#f6d243','#f6cd3f','#f5c83a','#f4c335','#f4bd30','#f3b82c',
'#f2b327','#f1ae23','#f0a91f','#efa41b','#ee9e16','#ed9912','#ec940e','#eb8e0a','#ea8906','#e88303','#e77e01','#e67800','#e47300','#e36d00','#e16700','#df6100',
'#de5b00','#dc5501','#da4f02','#d84804','#d64105','#d43a07','#d23209','#d0290b','#cd1e0d','#cb0f0f']
    
    for gps,location,pm2 in zip (tmp['gps']['min'].to_list(),tmp['location']['min'].to_list(),tmp['pm2']['mean'].to_list()) :
        folium.CircleMarker(
        location=gps.split(','),
        radius=10,
        popup=location+" : "+str(pm2),
        color=gradient40[int((pm2-500)/(12000)*40)],
        fill=True,
        fill_color=gradient40[int((pm2-500)/(12000)*40)],
        ).add_to(m)
        
    folium_static(m) 
    