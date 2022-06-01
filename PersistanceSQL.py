import sys
import subprocess

try:
    import mariadb
except:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'mariadb'])


class PersistanceSQL:
    def __init__(self, ip_base, port, nom_base_donnee):
        """
        Construit un objet PersistanceSql. Cet objet permettra de charger les données depuis une base de données ou de les sauvegarder dans la base.
        """
        self.ip_base = ip_base
        self.port = port
        self.nom_base_donnee = nom_base_donnee

    def rangerDansBase(self, un_objet):
        """
        Stocke les données de l'objet dans la base de données. 
        """
        self.un_objet = un_objet

        try:
            conn = mariadb.connect(
                user="root",
                password="",
                host="127.0.0.1",
                port=3306,
                database="cashcash_cashcash"

            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        cur = conn.cursor()

        if un_objet.__class__.__name__ == 'Materiel':
            if un_objet.un_contrat != None:
                sql = "UPDATE " + un_objet.__class__.__name__ + " SET `Numero_de_Contrat` = \'" + \
                    un_objet.un_contrat.num_contrat + \
                    "\' WHERE `materiel`.`Numero_de_Serie` = \'" + un_objet.num_serie + "\'"
            else:
                sql = "UPDATE " + un_objet.__class__.__name__ + \
                    " SET `Numero_de_Contrat` = NULL WHERE `materiel`.`Numero_de_Serie` = \'" + \
                    un_objet.num_serie + "\'"

            cur.execute(sql)
            conn.commit()

    def chargerDepuisBase(self, id, nom_classe):
        """
        Retourne l’objet de la classe nom_classe dont l’identifiant est "id". Cet objet est chargé depuis la base de données, ainsi que l’ensemble de ses objets liés. Retourne NULL si aucun objet de cette classe ne possède cet identifiant.
        """
        self.id = id
        self.nom_classe = nom_classe

        try:
            conn = mariadb.connect(
                user="root",
                password="",
                host="127.0.0.1",
                port=3306,
                database="cashcash_cashcash"

            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        cur = conn.cursor()

        if nom_classe == 'Materiel':
            sql = 'SELECT * FROM ' + self.nom_classe + ' WHERE Numero_Client= ' + self.id
            cur.execute(sql)
            liste = []
            for i in cur:
                liste.append(i)
            return liste

        elif nom_classe == 'Client':
            sql = 'SELECT * FROM ' + self.nom_classe + ' WHERE Numero_Client= ' + self.id
            cur.execute(sql)
            liste = []
            for i in cur:
                liste.append(i)
            return liste

        elif nom_classe == 'Contrat_Maintenance':
            sql = "SELECT * FROM " + self.nom_classe + \
                " WHERE Numero_de_Contrat= \'" + self.id + "\'"
            cur.execute(sql)
            liste = []
            for i in cur:
                liste.append(i)
            return liste

        elif nom_classe == 'Type_Materiel':
            sql = "SELECT * FROM " + self.nom_classe + \
                " WHERE `Reference_Interne` IN (SELECT Materiel.Reference_Interne FROM Materiel WHERE Materiel.Numero_de_Serie = \'" + self.id + "\')"
            cur.execute(sql)
            liste = []
            for i in cur:
                liste.append(i)
            return liste

        elif nom_classe == 'Clients':
            sql = 'SELECT Numero_Client, Raison_Sociale FROM Client'
            cur.execute(sql)
            liste = []
            for i in cur:
                liste.append(i)
            return liste
