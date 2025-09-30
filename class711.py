# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 15:48:16 2025

@author: user
"""

class Utilisateurs:
    
    def __init__(self,id_utilisateur,nom,prenom,identifiant,mdp):
        self.id_utilisateur = id_utilisateur
        self.nom= nom
        self.prenom = prenom
        self.identifiant= identifiant
        self.mdp = mdp
    
class Notes:
    
    def __init__(self,id_utilisateur,id_bouteilles,id_notes,notes,commentaires):
        self.id_utilisateur=id_utilisateur
        self.id_bouteilles=id_bouteilles
        self.id_notes=id_notes
        self.notes=notes
        self.commentaires=commentaires
    


class Cave:
    
    def __init__(self,id_utilisateur,id_etageres):
        self.id_utilisateur = id_utilisateur
        self.id_etageres = id_etageres

class Etageres:
    
    def __init__(self,id_etageres,nom,id_bouteilles,stock,capacite):
        self.id_etageres = id_etageres
        self.nom = nom
        self.id_bouteilles = id_bouteilles
        self.stock = stock
        self.capacite = capacite

class Bouteilles:
    
    def __init__(self,id_bouteilles,domaine_viticole,nom,type_bouteilles,annee,region,photo,prix):
        self.id_bouteilles = id_bouteilles
        self.domaine_viticole = domaine_viticole
        self.nom = nom
        self.type_bouteilles = type_bouteilles
        self.annee = annee
        self.region = region
        self.photo = photo
        self.prix = prix
    
    def moyenne(self):
        print("ok")