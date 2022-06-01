

class Materiel:
    """
    num_serie : entier \n
    date_vente : Produit \n
    prix_vente : réel \n
    date_installation : date \n
    emplacement : chaîne \n
    le_type : TypeMateriel 
    un_contrat : ContratMaintenance
    """
    def __init__(self, num_serie, date_vente, date_installation, prix_vente, emplacement, le_type, un_contrat):
        self.num_serie = num_serie
        self.date_vente = date_vente
        self.date_installation = date_installation
        self.prix_vente = prix_vente
        self.emplacement = emplacement
        self.le_type = le_type
        self.un_contrat = un_contrat
    
    def xmlMateriel(self):
        """
        Retourne la chaîne correspondant au code XML représentant le matériel
        """
        materiel_chaine_xml = ""

        if self.un_contrat is not None:
            materiel_chaine_xml = "<materiel numSerie=\'" + str(self.num_serie) + "\'><type refInterne=\'" + str(self.le_type.reference_interne) + "\' libelle=\'" + str(self.le_type.libelle_type_materiel) + "\' /><date_vente>" + str(self.date_vente) + "</date_vente><date_installation>" + str(self.date_installation) + "</date_installation><prix_vente>" + str(self.prix_vente) + "</prix_vente><emplacement>"+ str(self.emplacement) + " </emplacement><nbJourAvantEcheance>" +str(self.un_contrat.getJoursRestants()) + "</nbJourAvantEcheance ></materiel>"
            return materiel_chaine_xml

        else:
            materiel_chaine_xml = "<materiel numSerie=\'" + str(self.num_serie) + "\'><type refInterne=\'" + str(self.le_type.reference_interne) + "\' libelle=\'" + str(self.le_type.libelle_type_materiel) + "\' /><date_vente>" + str(self.date_vente) + "</date_vente><date_installation>" + str(self.date_installation) + "</date_installation><prix_vente>" + str(self.prix_vente) + "</prix_vente><emplacement>"+ str(self.emplacement) + " </emplacement></materiel>"
            return materiel_chaine_xml
