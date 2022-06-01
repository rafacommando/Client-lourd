class TypeMateriel:
    """
    reference_interne : chaine \n
    libelle_type_materiel : chaine
    """
    def __init__(self, reference_interne, libelle_type_materiel):
        self.reference_interne = reference_interne
        self.libelle_type_materiel = libelle_type_materiel

    def getReferenceInterne(self):
        """
        Retourne la reference_interne du materiel.
        """
        return self.reference_interne

    def getLibelleTypeMateriel(self):
        """
        Retourne la reference_interne du materiel.
        """
        return self.libelle_type_materiel
