class Client:
    """
    num_client : chaine \n
    raison_sociale : chaîne \n
    siren : chaîne \n
    code_ape : chaîne \n
    adresse : chaîne \n
    tel_client : chaîne \n
    email : chaîne \n
    duree_deplacement : entier \n
    distance_km : entier \n
    Numero_Agence : string \n 
    les_materiels : Collection de <Materiel>  (Tous les matériels du client.) \n
    le_contrat : ContratMaintenance (peut être nul si le client ne possède pas de contrat)
    """
    def __init__(self, num_client, raison_sociale, siren, code_ape, adresse, tel_client, email, duree_deplacement, distance_km, Numero_Agence, les_materiels, le_contrat):
        self.num_client = num_client
        self.raison_sociale = raison_sociale
        self.siren = siren
        self.code_ape = code_ape
        self.adresse = adresse
        self.tel_client = tel_client
        self.email = email
        self.duree_deplacement = duree_deplacement
        self.distance_km = distance_km
        self.Numero_Agence = Numero_Agence
        self.les_materiels = les_materiels
        self.le_contrat = le_contrat
        
    def getMateriels(self):
        """
        Retourne l'ensemble des matériels du client
        """
        return self.les_materiels
        
        
    def getMaterielsSousContrat(self):
        """
        Retourne l'ensemble des matériels pour lesquels le client a souscrit un contrat de maintenance qui est encore valide (la date du jour est entre la date de signature et la date d’échéance)
        """
        liste = []
        for i in self.les_materiels:
            if i[5] is not None:
                liste.append(i)
        return liste
        
    def estAssure(self):
        """
        Retourne vrai si le client est assuré, faux sinon
        """
        if len(self.getMaterielsSousContrat()) == len(self.getMateriels()):
            return True
        else:
            return False
        
