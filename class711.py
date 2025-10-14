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
    
    def voir_cave(self):
        conn = sqlite3.connect("Cave.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM Cave WHERE id_utilisateur = ?", (self.id_utilisateur,))
        cave = cur.fetchone()

        conn.close()
        return cave  

        
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
        
    def connexion(self):
        conn = sqlite3.connect("Cave.db")
        cur = conn.cursor()
        sql = "SELECT * FROM Utilisateur WHERE identifiant = ? AND mdp = ?"
        cur.execute(sql, (self.identifiant, self.mdp))
        result = cur.fetchone()
        conn.close()
        if result:
            self.id_utilisateur = result[0]  
            self.nom = result[1]
            self.prenom = result[2]
            return True
        else:
            return False
    
class Notes:
    
    def __init__(self,id_utilisateur,id_bouteilles,id_notes,notes,commentaires):
        self.id_utilisateur=id_utilisateur
        self.id_bouteilles=id_bouteilles
        self.id_notes=id_notes
        self.notes=notes
        self.commentaires=commentaires
    


class Cave:
    
    def __init__(self,id_utilisateur):
        self.id_utilisateur = id_utilisateur
        self.id_etagere = None   
        
    def cree_cave(self):
        conn = sqlite3.connect("Cave.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM Cave WHERE id_utilisateur = ?", (self.id_utilisateur,))
        exist = cur.fetchone()

        if not exist:
            cur.execute("INSERT INTO Cave (id_utilisateur, id_etagere) VALUES (?, ?)", (self.id_utilisateur, self.id_etagere))
            conn.commit()

        conn.close()

class Etageres:
    
    def __init__(self,id_etageres,nom,id_bouteilles,stock,capacite):
        self.id_etageres = id_etageres
        self.nom = nom
        self.id_bouteilles = id_bouteilles
        self.stock = stock
        self.capacite = capacite

class Bouteilles:
    
    chemin_images_bouteilles = r"D:\Users\user\Desktop\etrs711-main\static\images"
    
    
    
    def __init__(self,id_bouteilles,domaine_viticole,nom,type_bouteilles,annee,region,photo,prix):
        self.id_bouteilles = id_bouteilles
        self.domaine_viticole = domaine_viticole
        self.nom = nom
        self.type_bouteilles = type_bouteilles
        self.annee = annee
        self.region = region
        self.photo = photo
        self.prix = prix
    
    
    def ajoute_bouteille(self):
        conn = sqlite3.connect("Cave.db")
        cur = conn.cursor()
    
        # Chemin complet
        photo = Bouteilles.chemin_images_bouteilles + "\\" + self.photo
    
        # Vérifier si la bouteille existe déjà
        cur.execute("""
            SELECT * FROM Bouteille WHERE
            domaine_viticole=? AND nom=? AND type_bouteilles=? AND annee=? AND region=? AND photo=? AND prix=?
        """, (self.domaine_viticole, self.nom, self.type_bouteilles, self.annee, self.region, photo, self.prix))
    
        existing = cur.fetchone()
    
        if not existing:
            # Si elle n'existe pas, on l'ajoute
            cur.execute("""
                INSERT INTO Bouteille (domaine_viticole, nom, type_bouteilles, annee, region, photo, prix)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.domaine_viticole, self.nom, self.type_bouteilles, self.annee, self.region, photo, self.prix))
            conn.commit()
    
        conn.close()
        
               
    

