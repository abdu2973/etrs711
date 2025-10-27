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
        """
        Récupère toutes les étagères de l'utilisateur avec leurs informations complètes.
        """
        conn = sqlite3.connect("Cave.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
        # Récupérer toutes les références aux étagères pour cet utilisateur
        cur.execute("SELECT id_etagere FROM Cave WHERE id_utilisateur = ?", (self.id_utilisateur,))
        cave_refs = cur.fetchall()
    
        etageres = []
        for ligne in cave_refs:
            id_etagere = ligne['id_etagere']
            if id_etagere is not None:
                cur.execute("SELECT * FROM Etageres WHERE id_Etagere = ?", (id_etagere,))
                etagere = cur.fetchone()
                if etagere:
                    etageres.append(etagere)
    
        conn.close()
        return etageres

    
    def cave_exist(self):
        conn = sqlite3.connect("Cave.db")
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM Cave WHERE id_utilisateur = ?", (self.id_utilisateur,))
        exist = cur.fetchone()
        conn.close()
        return exist is not None
        
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
        conn.close()
        
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
            cur.execute("INSERT INTO Cave (id_utilisateur, id_etagere) VALUES (?, ?)", (self.id_utilisateur, None))
            conn.commit()
        conn.close()
        
    def associe_etagere(self, id_etagere):
        conn = sqlite3.connect("Cave.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Cave WHERE id_utilisateur = ? AND id_etagere IS NULL", (self.id_utilisateur,))
        premiere_etagere = cur.fetchone()
        if premiere_etagere:
            cur.execute("""
                UPDATE Cave 
                SET id_etagere = ? 
                WHERE id_utilisateur = ? AND id_etagere IS NULL
            """, (id_etagere, self.id_utilisateur))
        else:
            cur.execute("""
                INSERT INTO Cave (id_utilisateur, id_etagere) 
                VALUES (?, ?)
            """, (self.id_utilisateur, id_etagere))
        conn.commit()
        conn.close()



class Etageres:
    def __init__(self, nom, capacite, id_utilisateur):
        self.nom = nom
        self.capacite = capacite
        self.id_utilisateur = id_utilisateur

    def creer_etagere(self):
        try:
            db = bdd.Database()
            cur = db.conn.cursor()

            # Création de l'étagère
            cur.execute(
                "INSERT INTO Etageres (nom, stock_bouteilles, capacite, id_bouteille) VALUES (?, ?, ?, ?)",
                (self.nom, 0, self.capacite, None)
            )
            id_etagere = cur.lastrowid

            # Association de l’étagère à l’utilisateur
            cur.execute(
                "INSERT INTO Cave (id_utilisateur, id_etagere) VALUES (?, ?)",
                (self.id_utilisateur, id_etagere)
            )

            # Suppression d’éventuelles lignes orphelines
            cur.execute("DELETE FROM Cave WHERE id_etagere IS NULL")

            db.conn.commit()
            db.fin_connexion()

            return id_etagere

        except Exception as e:
            print("Erreur lors de la création d'une étagère :", e)
            return None
                
    def supprimer_etagere(self, id_etagere):
        conn = sqlite3.connect("Cave.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM Etageres WHERE id_Etagere = ?", (id_etagere,))
        cur.execute("DELETE FROM Cave WHERE id_utilisateur = ? AND id_etagere = ?", (self.id_utilisateur, id_etagere))
        conn.commit()
        conn.close()





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
        photo = Bouteilles.chemin_images_bouteilles + "\\" + self.photo
        cur.execute("""
            SELECT * FROM Bouteille WHERE
            domaine_viticole=? AND nom=? AND type_bouteilles=? AND annee=? AND region=? AND photo=? AND prix=?
        """, (self.domaine_viticole, self.nom, self.type_bouteilles, self.annee, self.region, photo, self.prix))
        existing = cur.fetchone()
        if not existing:
            cur.execute("""
                INSERT INTO Bouteille (domaine_viticole, nom, type_bouteilles, annee, region, photo, prix)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.domaine_viticole, self.nom, self.type_bouteilles, self.annee, self.region, photo, self.prix))
            conn.commit()
        conn.close()