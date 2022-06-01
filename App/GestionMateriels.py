# fonction statique XmlClientValide (xml : chaine) : booleen
# // Retourne un booléen Vrai si le fichier xml respecte la DTD référencée
# dans le fichier XML, Faux sinon
import PersistanceSQL, Materiels, TypeMateriel, ContratMaintenance
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import xml.dom.minidom


# On creer la classe GestionMateriels
class GestionMateriels:
    """
    donnees : PersistanceSQL (Attribut qui permet de rendre les objets métiers accessibles.)
    """
    global donnees
    donnees = PersistanceSQL.PersistanceSQL('mysql-cashcash.alwaysdata.net', 0, ' cashcash_cashcash')

    # Constructeur de la classe GestionMateriels
    def __init__(self, les_donnees):
        """
        Construit un objet GestionMateriels avec un modèle de persistance associé.
        """
        self.les_donnees = les_donnees

    # Retourne l'objet Distributeur qui possède l'identifiant idDistributeur passé en paramètre, retourne null si aucun Distributeur ne possède cet identifiant.
    def getClient(self, id_client):
        """
        Retourne l'objet Distributeur qui possède l'identifiant id_client passé en paramètre, retourne null si aucun client ne possède cet identifiant.
        """
        # Si les donnees chargee avec l'id_client en paramettre de la methode ne renvois pas None
        if self.les_donnees.chargerDepuisBase(id_client, 'Client') is not None:

            # On recupere les donnees du client 
            return self.les_donnees.chargerDepuisBase(id_client, 'Client')
        else:

            # Sinon on retourne None 
            return None
            

    # Retourne une chaîne de caractères qui représente le document XML de la liste des matériels du client passé en paramètre comme le montre l'exemple de l'annexe
    def XmlClient(self, un_client):
        """
        Retourne une chaîne de caractères qui représente le document XML de la liste des matériels du client passé en paramètre.
        """
        
        if un_client.le_contrat != None:
            liste_contrat = donnees.chargerDepuisBase(un_client.le_contrat.num_contrat, 'Contrat_Maintenance')
            un_contrat = ContratMaintenance.ContratMaintenance(liste_contrat[0][0], liste_contrat[0][1], liste_contrat[0][2])
        else:
            liste_contrat = None
            un_contrat = None
        
        liste_materiels = donnees.chargerDepuisBase(un_client.num_client, 'Materiel')
        
        xml_version = "<?xml version='1.0' encoding='UTF-8'?>"
        entete = '<listeMateriel>'
        materiel_id_client = "<materiels idClient=\'" + un_client.num_client + "\' >"
        sous_contrat = "<sousContrat>"
        materiels_sous_contrat = ""
        materiels_hors_contrat = ""
        for i in range(len(un_client.getMateriels())):
            if un_client.getMateriels()[i][5] is not None:
                liste_le_type = donnees.chargerDepuisBase(liste_materiels[i][0], 'Type_Materiel')
                le_type = TypeMateriel.TypeMateriel(liste_le_type[0][0], liste_le_type[0][1])
                un_materiel = Materiels.Materiel(liste_materiels[i][0],liste_materiels[i][1], liste_materiels[i][2],liste_materiels[i][3], liste_materiels[i][4], le_type, un_contrat)
                materiels_sous_contrat += un_materiel.xmlMateriel()
        fin_sous_contrat = "</sousContrat>"
        hors_contrat = "<horsContrat>"
        for i in range(len(un_client.getMateriels())):
            if un_client.getMateriels()[i][5] is None:
                un_materiel = Materiels.Materiel(liste_materiels[i][0],liste_materiels[i][1], liste_materiels[i][2],liste_materiels[i][3], liste_materiels[i][4], TypeMateriel.TypeMateriel(donnees.chargerDepuisBase(liste_materiels[i][0], 'Type_Materiel')[0][0], donnees.chargerDepuisBase(liste_materiels[i][0], 'Type_Materiel')[0][1]), un_contrat)
                materiels_hors_contrat += un_materiel.xmlMateriel()
        fin_hors_contrat = "</horsContrat>"
        fin_materiel_id_client = "</materiels>"
        fin = "</listeMateriel>"
        
        if len(materiels_sous_contrat) > 0 and len(materiels_hors_contrat) > 0:       
            chaine_complete = xml_version + entete + materiel_id_client + sous_contrat + materiels_sous_contrat + fin_sous_contrat + hors_contrat + materiels_hors_contrat + fin_hors_contrat + fin_materiel_id_client + fin
        elif len(materiels_sous_contrat) > 0 and len(materiels_hors_contrat) <= 0:  
            chaine_complete = xml_version + entete + materiel_id_client + sous_contrat + materiels_sous_contrat + fin_sous_contrat + fin_materiel_id_client + fin
        elif len(materiels_sous_contrat) <= 0 and len(materiels_hors_contrat) > 0: 
            chaine_complete = xml_version + entete + materiel_id_client + hors_contrat + materiels_hors_contrat + fin_hors_contrat + fin_materiel_id_client + fin
             
             
        root = ET.fromstring(chaine_complete)
        xml_p = xml.dom.minidom.parseString(tostring(root))
        pretty_xml = xml_p.toprettyxml()
        
        fichier_name = "materielClient" + str(un_client.num_client) + ".xml"
        
        with open(fichier_name, "w") as f:
            f.write(pretty_xml)
        return pretty_xml