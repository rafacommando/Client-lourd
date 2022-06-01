import sys
import subprocess


try:
    from datetime import datetime
except:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'datetime'])


class ContratMaintenance:
    """
    num_contrat : chaîne \n
    date_signature : date \n
    date_echeance : date \n
    les_materiels_assures : Collection de <Materiel> (Tous les matériels sous contrat de maintenance)
    """
    def __init__(self, num_contrat, date_signature, date_echeance):
        self.num_contrat = num_contrat
        self.date_signature = date_signature
        self.date_echeance = date_echeance
        self.les_materiels_assures = []


    def getJoursRestants(self):
        """
         Renvoie le nombre de jours avant que le contrat arrive à échéance
         """
        return abs((self.date_echeance - self.date_signature).days)

    def estValide(self):
        """
        indique si le contrat est valide (la date du jour est entre la date de signature et la date d’échéance)
        """

        if str(self.date_signature) <= datetime.now().strftime("%Y-%m-%d") <= str(self.date_echeance):
            return True
        return False

    def ajouteMateriel(self, un_materiel):
        """
        ajoute unMatériel à la collection les_materiels_assures si la date de signature du contrat est antérieure à la date d’installation du matériel
        """
        if self.date_signature < un_materiel.date_installation:
            self.les_materiels_assures.append(un_materiel)
