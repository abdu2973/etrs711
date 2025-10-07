# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 15:48:16 2025

@author: user
"""
import sqlite3
import Bdd711 as bdd



class Utilisateurs:
    
    def __init__(self,id_utilisateur,nom,prenom,identifiant,mdp):
        self.id_utilisateur = id_utilisateur
        self.nom= nom
        self.prenom = prenom
        self.identifiant= identifiant
        self.mdp = mdp
    
    def cree_cave(self):
        conn = sqlite3.connect("Cave.db")
        cur= conn.cursor()
        id_utilisateur = self.id_utilisateur
        id_etagere = None
        sql = "INSERT INTO Cave (id_utilisateur, id_etagere) VALUES (?, ?)"
        cur.execute(sql, (id_utilisateur, id_etagere))
        conn.commit()
        
    def ajouter_utilisateur(self):
        conn = sqlite3.connect("Cave.db")
        cur= conn.cursor()
        nom = self.nom
        prenom = self.prenom
        identifiant = self.identifiant
        mdp = self.mdp
        sql = """
            INSERT INTO Utilisateur (nom, prenom, identifiant, mdp)
            VALUES (?, ?, ?, ?)
        """
        cur.execute(sql, (nom, prenom, identifiant, mdp))
        conn.commit()

    
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
        

test = bdd.Database()