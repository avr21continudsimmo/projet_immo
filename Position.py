import requests, json
import urllib.parse



class Position :
    """ defini une position à partir d'une adresse ou de coordonnées gps"""
    lat=0
    lgt=0
    addressName=''
    def __init__(self,addressName='', gps=[]):
        """
        affecte les coordonnees fournis ou les 
        deduit du nom de l'adresse

        Parametres:
            addressName : (optionnel) type string
                nom d'une adresse exemple : 
                2, boulevard Blaise Pascal, 93160 Noisy le Grand
            gps : (optionnel) type list 
                liste de deux float [latitude,longitude] 
                contenant les coordonnees gps 
                exemple : [46.249847, 4.894293]
        """
        self.addressName = addressName
        if addressName:
            gps=self.gpsFromAddress(addressName)
            self.lat = gps[0]
            self.lgt = gps[1]
        if gps :
            self.lat = gps[0]
            self.lgt = gps[1]

    def get_gpsCoo(self):
        """
        Renvoi les coordonnees gps d'une adresse

        renvoi:
            liste de deux float [latitude,longitude] 
            contenant les coordonnees gps 
            exemple : [46.249847, 4.894293]
        """
        # source  : # https://perso.esiee.fr/~courivad/Python/15-geo.html
        api_url = "https://api-adresse.data.gouv.fr/search/?q="
        r = requests.get(api_url + urllib.parse.quote(self.addressName))
        coo=r.content.decode('unicode_escape')
        coo = json.loads(coo)
        return [coo["features"][0]["geometry"]["coordinates"][1],coo["features"][0]["geometry"]["coordinates"][0]]
    
    @staticmethod
    def gpsFromAddress(address):
        """
        Renvoi les coordonnees gps d'une adresse

        renvoi:
            liste de deux float [latitude,longitude] 
            contenant les coordonnees gps 
            exemple : [46.249847, 4.894293]
        """
        # source  : # https://perso.esiee.fr/~courivad/Python/15-geo.html
        api_url = "https://api-adresse.data.gouv.fr/search/?q="
        r = requests.get(api_url + urllib.parse.quote(address))
        coo=r.content.decode('unicode_escape')
        coo = json.loads(coo)
        return [coo["features"][0]["geometry"]["coordinates"][1],coo["features"][0]["geometry"]["coordinates"][0]]