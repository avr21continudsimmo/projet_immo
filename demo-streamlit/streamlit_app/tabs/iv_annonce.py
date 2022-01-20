import matplotlib.image as img
import streamlit as st

title = "Annonce demo"
sidebar_name = "0. Exemple d'annonce"

def run():
    
    st.write("Nous avons sélectionné cette annonce comme exemple par défaut : ")
    image = img.imread('../../models/demo.png')
    st.image(image)

    st.markdown("""
                Nous déduisons de l'annonce les propriétés suivantes : 
                - **Exposition Sud**
                - **Lumineux**
                - **Mezzanine**
                - **Garage**
                - **Terrasse**
                - **Parking**
                - **Proche écoles**
                - **Proche commodités**
                
                D'autres propriétés pourraient être rajoutées après la visite du bien.""")   
    
        
        