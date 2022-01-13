def features_map(extra_features):
    
    # Initialisation des paramètres
    Exposition_Sud = 0
    Lumineux = 0
    Calme = 0
    Volume = 0
    Standing = 0
    Charme = 0
    Mezzanine = 0 
    Avec_Ascenseur = 0 
    Sans_Ascenseur = 0
    Duplex = 0
    Dernier_etage = 0 
    Premier_etage = 0
    Deuxieme_etage = 0
    Troisieme_etage = 0
    Quatrieme_etage = 0
    Cinquieme_etage = 0
    Sixieme_etage = 0
    Septieme_etage = 0
    Huitieme_etage = 0
    RDC = 0
    Design = 0 
    Terrasse = 0
    Parfait_etat = 0
    Travaux = 0
    Proche_commodites = 0 
    Vue_degagee = 0
    Securise = 0
    Emplacement = 0 
    Atypique = 0
    Nature = 0
    Meuble = 0
    Cave = 0
    Parking = 0
    Cuisine_americaine = 0
    Investissement_locatif = 0
    Proche_ecoles = 0
    Dressing = 0
    Plain_Pied = 0
    Garage = 0
    Grange = 0
    Buanderie = 0
    Dependance = 0
    
    # Calcul de la valeur des paramètres
    
    if "Exposition Sud" in extra_features:
        Exposition_Sud = 1    
    if "Lumineux" in extra_features:
        Lumineux = 1
    if "Calme" in extra_features:
        Calme = 1
    if "Beaux volumes" in extra_features:
        Volume = 1
    if "Standing" in extra_features:
        Standing = 1
    if "Charme" in extra_features:
        Charme = 1
    if "Mezzanine" in extra_features:
        Mezzanine = 1
    if "Avec Ascenseur" in extra_features:
        Avec_Ascenseur = 1
    if "Sans Ascenseur" in extra_features:
        Sans_Ascenseur = 1
    if "Duplex" in extra_features:
        Duplex = 1
    if "Dernier étage" in extra_features:
        Dernier_etage = 1
    if "Premier étage" in extra_features:
        Premier_etage = 1
    if "Deuxième étage" in extra_features:
        Deuxieme_etage = 1
    if "Troisième étage" in extra_features:
        Troisieme_etage = 1
    if "Quatrième étage" in extra_features:
        Quatrieme_etage = 1
    if "Cinquième étage" in extra_features:
        Cinquieme_etage = 1
    if "Sixième étage" in extra_features:
        Sixieme_etage = 1
    if "Septième étage" in extra_features:
        Septieme_etage = 1
    if "Huitième étage" in extra_features:
        Huitieme_etage = 1
    if "RDC" in extra_features:
        RDC = 1
    if "Design" in extra_features:
        Design = 1
    if "Terrasse" in extra_features:
        Terrasse = 1
    if "Parfait état" in extra_features:
        Parfait_etat = 1
    if "Travaux à prévoir" in extra_features:
        Travaux = 1
    if "Proche commodités" in extra_features:
        Proche_commodites = 1
    if "Vue dégagée" in extra_features:
        Vue_degagee = 1
    if "Sécurisé" in extra_features:
        Securise = 1
    if "Emplacement" in extra_features:
        Emplacement = 1
    if "Atypique" in extra_features:
        Atypique = 1
    if "Proche de la nature" in extra_features:
        Nature = 1
    if "Meublé" in extra_features:
        Meuble = 1
    if "Cave" in extra_features:
        Cave = 1
    if "Parking" in extra_features:
        Parking = 1
    if "Cuisine américaine" in extra_features:
        Cuisine_americaine = 1
    if "Investissement locatif" in extra_features:
        Investissement_locatif = 1
    if "Proche écoles" in extra_features:
        Proche_ecoles = 1
    if "Dressing" in extra_features:
        Dressing = 1
    if "Plain Pied" in extra_features:
        Plain_Pied = 1
    if "Garage" in extra_features:
        Garage = 1
    if "Grange" in extra_features:
        Grange = 1
    if "Buanderie" in extra_features:
        Buanderie = 1
    if "Dépendance" in extra_features:
        Dependance = 1
    
    return Exposition_Sud, Lumineux, Calme, Volume, Standing, Charme, Mezzanine, Avec_Ascenseur, Sans_Ascenseur, Duplex, Dernier_etage, Premier_etage, Deuxieme_etage, Troisieme_etage, Quatrieme_etage, Cinquieme_etage, Sixieme_etage, Septieme_etage, Huitieme_etage, RDC, Design, Terrasse, Parfait_etat, Travaux, Proche_commodites, Vue_degagee, Securise, Emplacement, Atypique, Nature, Meuble, Cave, Parking, Cuisine_americaine, Investissement_locatif, Proche_ecoles, Dressing, Plain_Pied, Garage, Grange, Buanderie, Dependance