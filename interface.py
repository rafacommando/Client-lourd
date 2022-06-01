import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
import Client
import PersistanceSQL
import ContratMaintenance
import Materiels
import TypeMateriel
import GestionMateriels


# Premiere fenetre
class MainWin(tk.Tk):
    # Constructeur de la classe MainWin
    def __init__(self):
        super().__init__()

        # Configurer la fenêtre racine
        self.title('Cash-Cash')
        self.geometry('400x80')
        self.resizable(False, False)

        # Label
        self.text = tk.StringVar()
        self.text.set("Choisir un client")
        self.label = ttk.Label(self, textvariable=self.text)
        self.label.pack()

        # Text box
        # self.text_box_num_client = Text(self, height=1, width=10)
        # self.text_box_num_client.pack()
        global liste_num_client, liste_raison_sociale
        liste_num_client = []
        liste_raison_sociale = []
        liste = persist.chargerDepuisBase(0, 'Clients')
        self.comboExample = ttk.Combobox(self,
                            values=[])
        for i in range(len(liste)):
            liste_raison_sociale.append(liste[i][1])
            liste_num_client.append(liste[i][0])
        self.comboExample['values'] = liste_raison_sociale
        
        
            
        self.comboExample.pack()

        self.comboExample.bind("<<ComboboxSelected>>", self.callbackFunc)   

        # Boutton
        self.button = ttk.Button(
            self, text='Afficher', command=self.button_clicked)
        self.button.place(x=125, y=47)

        self.relance_buton = ttk.Button(
            self, text='Relance', command=self.relance)
        self.relance_buton.place(x=200, y=47)


    def callbackFunc(self, event):
        global num_client, nom_client
        nom_client = liste_raison_sociale[self.comboExample.current()]
        num_client = liste_num_client[self.comboExample.current()]

    def relance(self):
        showinfo(title='Relance',
                     message="Client relancé, prochaine relance dans 30 jours")

    # Evenement pour le bouton afficher
    def button_clicked(self):
        """
        Affiche la liste des materiels pour un numero client donné
        """
        try:

            # Si la textbox n'est pas vide et que le materiel existe bien pour le numero client donné
            if num_client != "":

                # On creer une nouvelle fenetre Materiel avec comme argument le numero client rensigner dans la text box
                Materiel().mainloop()

        except:
            showinfo(title='Invalid',
                     message="Veuillez saisir un numéro de client valide.")

# Deuxieme fenetre


class Materiel(tk.Tk):
    """
    persist : PersistanceSQL 
    """
    # On creer une variable global PersistanceSQL
    global persist
    persist = PersistanceSQL.PersistanceSQL(
        'mysql-cashcash.alwaysdata.net', 0, ' cashcash_cashcash')

    # Constructeur de la classe Materiel
    def __init__(self):
        super().__init__()

        # Configurer la fenêtre racine
        self.title(nom_client)
        self.geometry('920x300')
        self.resizable(False, False)

        # Frame
        frm = Frame(self)
        frm.pack(padx=20)

        # On recupere la liste des materiels pour le numero de client recuperer dans le constructeur
        materiels = persist.chargerDepuisBase(
            num_client, 'Materiel')

        # Treeview
        self.tv = ttk.Treeview(frm, columns=(
            1, 2, 3, 4, 5, 6, 7, 8), show='headings', height='10')
        self.tv.pack(pady=30)

        # On definit chaque colonne de la Treeview qui correspond aux colonnes de la table Materiels
        self.tv.heading(1, text='Numéro serie')
        self.tv.column(1, minwidth=0, width=100, stretch=NO)
        self.tv.heading(2, text='Date de vente')
        self.tv.column(2, minwidth=0, width=100, stretch=NO)
        self.tv.heading(3, text='Date d\'installation')
        self.tv.column(3, minwidth=0, width=110, stretch=NO)
        self.tv.heading(4, text='Prix de vente')
        self.tv.column(4, minwidth=0, width=100, stretch=NO)
        self.tv.heading(5, text='Emplacement')
        self.tv.column(5, minwidth=0, width=100, stretch=NO)
        self.tv.heading(6, text='Numéro de contrat')
        self.tv.column(6, minwidth=0, width=110, stretch=NO)
        self.tv.heading(7, text='Numéro de client')
        self.tv.column(7, minwidth=0, width=100, stretch=NO)
        self.tv.heading(8, text='Reference interne')
        self.tv.column(8, minwidth=0, width=110, stretch=NO)

        # Permet de recuperer la valeur selectionner par le curseur dans la Treeview
        self.tv.bind('<ButtonRelease-1>', self.select_item)

        # Pour chaque elements dans la liste de materiels
        for i in materiels:

            # On insert chaque element de la liste ligne par ligne
            self.tv.insert('', 'end', values=i)

        # Bouttons
        self.button_quitter = ttk.Button(
            self, text='Quitter', command=self.destroy)
        self.button_quitter.place(x=325, y=260)
        self.button_choisir = ttk.Button(self, text='Choisir')
        self.button_choisir['command'] = self.button_choisir_clicked
        self.button_choisir.place(x=400, y=260)
        self.button_generer = ttk.Button(
            self, text='Generer', command=self.genererXML)
        self.button_generer.place(x=475, y=260)

    # Evenement pour le bouton generer
    def genererXML(self):
        """
        Genere un fichier XML pour un client donné
        """

        # On creer un nouvel objet GestionMateriels avec comme argument l'objet PersistanceSQL
        gestion_materiel = GestionMateriels.GestionMateriels(persist)

        # On creer une liste de materiel avec le numero de client recuperer du constructeur
        liste_materiels = persist.chargerDepuisBase(
            num_client, 'Materiel')

        # Pour chaque elements dans allant de 0 a la taille de la liste des materiels
        for i in range(len(liste_materiels)):

            # Si le numero de contrat du materiel est different de NULL
            if liste_materiels[i][5] != None:

                # On charge dans une liste les informations concernant le contrat ayant comme numero de contrat (liste_materiels[i][5])
                liste_contrat = persist.chargerDepuisBase(
                    liste_materiels[i][5], 'Contrat_Maintenance')
                break
            else:

                # Sinon aucun materiel n'est assure donc il n'y a aucun contrat
                liste_contrat = None


        # On charge la liste des informations du client qui a comme numero de client le numero de client du constructeur
        liste_client = persist.chargerDepuisBase(
            num_client, 'Client')

        # Si la liste de contrat n'est pas vide
        if liste_contrat != None:

            # On creer un objet contrat avec les informations de la liste de contrat
            un_contrat = ContratMaintenance.ContratMaintenance(
                liste_contrat[0][0], liste_contrat[0][1], liste_contrat[0][2])
        else:

            # Sinon il n'y a aucun contrat et le contrat est NULL
            un_contrat = None

        # On creer un objet client avec les informations de la liste client, du contrat et et de la liste des materiels
        un_client = Client.Client(liste_client[0][0], liste_client[0][1], liste_client[0][2], liste_client[0][3], liste_client[0][4], liste_client[0][5], liste_client[0]
                                  [6], liste_client[0][7], liste_client[0][8], liste_client[0][9], liste_materiels, un_contrat)

        # Pour chauque element allant de 0 a la taille de la liste des materiels du client
        for i in range(len(un_client.getMateriels())):

            # Si le materiel possede un numero de contrat
            if liste_materiels[i][5] != None:

                # On creer une liste avec les informations concernant le type de materiels
                liste_le_type = persist.chargerDepuisBase(
                    liste_materiels[i][0], 'Type_Materiel')

                # On creer un objet TypeMateriel avec les informations de la liste du type de materiel
                le_type = TypeMateriel.TypeMateriel(
                    liste_le_type[0][0], liste_le_type[0][1])

                # On creer un objet Materiel avec les informations de la liste de materiels, du type et du contrat
                un_materiel = Materiels.Materiel(
                    liste_materiels[i][0], liste_materiels[i][1], liste_materiels[i][2], liste_materiels[i][3], liste_materiels[i][4], le_type, un_contrat)

                # On ajoute un materiel au contrat s'il respect les critères
                un_contrat.ajouteMateriel(un_materiel)

        # On retourne le fichier XML du client et on lance un message d'alerte pour confirmer que le fichier est bien genere
        return gestion_materiel.XmlClient(un_client), showinfo(title='Fin',
                                                               message="Votre fichier à était géneré.")

    # Evenement pour le bouton choisir
    def button_choisir_clicked(self):
        """
        Affiche les données d'un materiel selectionné
        """
        try:
            # On recupere la valeur qui correspond a la ligne selectionnee
            item = self.tv.selection()[0]

            # Si la valeur correspondant a la ligne selectionne n'est pas vide
            if item != "":

                # On creer une nouvelle fenetre Administration avec commme parammetre la liste de toutes les informations de la ligne selectionnee
                page_admin = Administration(self.tv.item(item)['values'])

                # On ferme la fenetre actuelle
                self.destroy()

                # On ouvre la fenetre Administration
                page_admin.mainloop()
            else:
                # Sinon on envois un message d'erreur
                showinfo(title='Invalid',
                            message="Veuillez selectionner un materiel.")
        except:
            showinfo(title='Invalid',
                     message="Veuillez selectionner un materiel.")

    # Fonction permettant de recuperer la valeur correspondant a une ligne
    def select_item(self, a):
        """
        a : entier \n
        Recupere la valeur selectionne avec le curseur
        """
        try:
            # Ligne cliquée
            self.tv.selection()[0]
        except:
            showinfo(title='Invalid',
                     message="Veuillez selectionner une ligne.")


# On creer une troisieme fenetre
class Administration(tk.Tk):
    """
    liste_materiel : collection de <Materiel>
    """
    # Constructeur de la classe Administration
    def __init__(self, liste_materiel):
        super().__init__()
        self.liste_materiel = liste_materiel

        # Configurer la fenêtre racine
        self.title('Administration')
        self.geometry('450x500')
        self.resizable(False, False)

        # Label premiere colonne (gauche)
        self.label_num_serie = ttk.Label(self, text="Numéro de serie ")
        self.label_num_serie.place(x=50, y=40)
        self.label_date_vente = ttk.Label(
            self, text="Date de vente " + self.liste_materiel[1])
        self.label_date_vente.place(x=50, y=80)
        self.label_date_installation = ttk.Label(
            self, text="Date d'installation ")
        self.label_date_installation.place(x=50, y=120)
        self.label_prix_de_vente = ttk.Label(self, text="Prix de vente ")
        self.label_prix_de_vente.place(x=50, y=160)
        self.label_emplacement = ttk.Label(self, text="Emplacement ")
        self.label_emplacement.place(x=50, y=200)
        self.label_num_contrat = ttk.Label(self, text="Numéro de contrat")
        self.label_num_contrat.place(x=50, y=240)
        self.label_num_client = ttk.Label(self, text="Numéro de client ")
        self.label_num_client.place(x=50, y=280)
        self.label_reference_interne = ttk.Label(
            self, text="Reference interne")
        self.label_reference_interne.place(x=50, y=320)

        # Label deuxieme colonne (droite)
        self.label_num_serie = ttk.Label(self, text=liste_materiel[0])
        self.label_num_serie.place(x=250, y=40)
        self.label_date_vente = ttk.Label(self, text=self.liste_materiel[1])
        self.label_date_vente.place(x=250, y=80)
        self.label_date_installation = ttk.Label(self, text=liste_materiel[2])
        self.label_date_installation.place(x=250, y=120)
        self.label_prix_de_vente = ttk.Label(self, text=liste_materiel[3])
        self.label_prix_de_vente.place(x=250, y=160)
        self.label_emplacement = ttk.Label(self, text=liste_materiel[4])
        self.label_emplacement.place(x=250, y=200)
        self.text_box_num_contrat = tk.Text(self, height=1, width=20)
        self.text_box_num_contrat.place(x=250, y=240)
        self.label_num_client = ttk.Label(self, text=liste_materiel[6])
        self.label_num_client.place(x=250, y=280)
        self.label_reference_interne = ttk.Label(self, text=liste_materiel[7])
        self.label_reference_interne.place(x=250, y=320)

        # Bouttons
        self.button_annuler = ttk.Button(
            self, text='Annuler', command=self.destroy)
        self.button_annuler.place(x=150, y=400)
        self.button_choisir = ttk.Button(
            self, text='Mofifier', command=self.update)
        self.button_choisir.place(x=225, y=400)

    # Evenement du bouton Modifier
    def update(self):
        """
        Mets a jour la liste de materiel apres modification
        """
        try:

            # On creer une liste avec le type de materiel avec la liste de materiel du constructeur
            liste_le_type = persist.chargerDepuisBase(
                self.liste_materiel[0], 'Type_Materiel')

            # On creer un objet TypeMateriel avec les informations de la liste du type de materiel
            le_type = TypeMateriel.TypeMateriel(
                liste_le_type[0][0], liste_le_type[0][1])

            # On recupere le numero de contrat saisi par l'utilisateur dans la textbox
            num_contrat = self.text_box_num_contrat.get("1.0", "end-1c")

            # Si le numero de contrat n'est pas vide
            if num_contrat != "":

                # On creer la liste de contrat avec le numero de contrat
                liste_contrat = persist.chargerDepuisBase(
                    num_contrat, 'Contrat_Maintenance')

            else:

                # Sinon la liste de contrat est vide
                liste_contrat = None

            # Si la liste de contrat n'est pas vide
            if liste_contrat != None:

                # On creer un contrat avec les informations de la liste de contrat
                un_contrat = ContratMaintenance.ContratMaintenance(
                    liste_contrat[0][0], liste_contrat[0][1], liste_contrat[0][2])
            else:
                # Sinon on creer un contrat qui a comme valeur NULL
                un_contrat = None

            # On creer un objet materiel avec les informations de la liste de materiel du constructeur, du type et du contrat
            un_materiel = Materiels.Materiel(
                self.liste_materiel[0], self.liste_materiel[1], self.liste_materiel[2], self.liste_materiel[3], self.liste_materiel[4], le_type, un_contrat)

            # On envois un message pour prvenir que la modification à était effectuee
            showinfo(title='Fin',
                        message="Mise à jour effectuée.")

            # On range dans la base le nouvel objet materiel, on ferme la page et on ouvre une nouvelle fenetre Materiel avec la mise a jour
            return persist.rangerDansBase(un_materiel), self.destroy(), Materiel(
                ).mainloop()

        except:
            showinfo(title='Invalid',
                     message="Numéro de contrat invalide.")


if __name__ == "__main__":
    app = MainWin()
    app.mainloop()
