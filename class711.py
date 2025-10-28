# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 15:48:16 2025

@author: user
"""
import sqlite3
import Bdd711 as bdd
import statistics # Needed for mean calculation if done in Python

class Utilisateurs:
    
    def __init__(self,id_utilisateur,nom,prenom,identifiant,mdp):
        self.id_utilisateur = id_utilisateur
        self.nom= nom
        self.prenom = prenom
        self.identifiant= identifiant
        self.mdp = mdp
    
    def voir_cave(self, sort_by='nom_asc'):
        conn = sqlite3.connect("Cave.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        sort_map = {
            'nom_asc': 'ORDER BY B.nom ASC',
            'nom_desc': 'ORDER BY B.nom DESC',
            'annee_desc': 'ORDER BY B.annee DESC',
            'annee_asc': 'ORDER BY B.annee ASC',
            'prix_desc': 'ORDER BY B.prix DESC',
            'prix_asc': 'ORDER BY B.prix ASC',
        }
        sql_order_clause = sort_map.get(sort_by, 'ORDER BY B.nom ASC')
    
        cur.execute("SELECT id_etagere FROM Cave WHERE id_utilisateur = ? AND id_etagere IS NOT NULL", (self.id_utilisateur,))
        cave_refs = cur.fetchall()
    
        etageres_data = []
        for ligne in cave_refs:
            id_etagere = ligne['id_etagere']
            
            cur.execute("SELECT id_Etagere, nom, capacite FROM Etageres WHERE id_Etagere = ?", (id_etagere,))
            etagere_info = cur.fetchone()
            
            if etagere_info:
                etagere_dict = dict(etagere_info) 
                
                cur.execute("SELECT SUM(quantite) as total_stock FROM StockEtagere WHERE id_etagere = ?", (id_etagere,))
                stock_row = cur.fetchone()
                etagere_dict['stock_actuel'] = stock_row['total_stock'] if stock_row['total_stock'] is not None else 0
                
                query_sql = f"""
                    SELECT B.id_bouteille, B.nom, B.annee, B.photo, B.domaine_viticole, B.region, B.prix, S.quantite
                    FROM Bouteille B
                    JOIN StockEtagere S ON B.id_bouteille = S.id_bouteille
                    WHERE S.id_etagere = ?
                    {sql_order_clause}
                """
                cur.execute(query_sql, (id_etagere,))
                bouteilles_list = []
                for bouteille_row in cur.fetchall():
                    bouteille_dict = dict(bouteille_row)
                    bouteille_dict['note_moyenne'] = Notes.calculer_note_moyenne(bouteille_dict['id_bouteille'])
                    bouteilles_list.append(bouteille_dict)

                etagere_dict['bouteilles'] = bouteilles_list
                
                etageres_data.append(etagere_dict)

        conn.close()
        return etageres_data

    def voir_notes(self):
        conn = sqlite3.connect("Cave.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute("""
            SELECT B.nom, B.annee, B.photo, B.domaine_viticole, B.region, N.notes, N.commentaires
            FROM Notes N
            JOIN Bouteille B ON N.id_bouteille = B.id_bouteille
            WHERE N.id_utilisateur = ?
            ORDER BY N.id_commentaires DESC
        """, (self.id_utilisateur,))
        
        notes = cur.fetchall()
        conn.close()
        return notes

    
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

    def ajouter_note(self):
        conn = sqlite3.connect("Cave.db")
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO Notes (id_utilisateur, id_bouteille, notes, commentaires) VALUES (?, ?, ?, ?)",
                (self.id_utilisateur, self.id_bouteilles, self.notes, self.commentaires)
            )
            conn.commit()
            return True, "Note archivée avec succès."
        except Exception as e:
            conn.rollback()
            return False, f"Erreur lors de l'archivage : {e}"
        finally:
            conn.close()

    @staticmethod
    def voir_toutes_les_notes():
        conn = sqlite3.connect("Cave.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                B.id_bouteille, B.nom as bouteille_nom, B.annee, B.photo, B.domaine_viticole, B.region,
                N.notes, N.commentaires,
                U.prenom, U.nom as user_nom
            FROM Notes N
            JOIN Bouteille B ON N.id_bouteille = B.id_bouteille
            JOIN Utilisateur U ON N.id_utilisateur = U.id_utilisateur
            ORDER BY N.id_commentaires DESC
        """)
        
        notes_list = []
        for note_row in cur.fetchall():
            note_dict = dict(note_row)
            note_dict['note_moyenne'] = Notes.calculer_note_moyenne(note_dict['id_bouteille'])
            notes_list.append(note_dict)

        conn.close()
        return notes_list

    @staticmethod
    def calculer_note_moyenne(id_bouteille):
        conn = sqlite3.connect("Cave.db")
        cur = conn.cursor()
        cur.execute("SELECT AVG(notes) FROM Notes WHERE id_bouteille = ?", (id_bouteille,))
        result = cur.fetchone()
        conn.close()
        if result and result[0] is not None:
            return round(result[0], 1) # Arrondi à 1 décimale
        else:
            return None # Ou 0, ou "N/A" selon ce que tu préfères afficher


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

            cur.execute(
                "INSERT INTO Etageres (nom, capacite) VALUES (?, ?)",
                (self.nom, self.capacite)
            )
            id_etagere = cur.lastrowid

            cur.execute(
                "INSERT INTO Cave (id_utilisateur, id_etagere) VALUES (?, ?)",
                (self.id_utilisateur, id_etagere)
            )

            cur.execute("DELETE FROM Cave WHERE id_etagere IS NULL AND id_utilisateur = ?", (self.id_utilisateur,))

            db.conn.commit()
            db.fin_connexion()

            return id_etagere

        except Exception as e:
            print("Erreur lors de la création d'une étagère :", e)
            return None
                
    def supprimer_etagere(self, id_etagere):
        conn = sqlite3.connect("Cave.db")
        cur = conn.cursor()
        
        cur.execute("DELETE FROM StockEtagere WHERE id_etagere = ?", (id_etagere,))
        
        cur.execute("DELETE FROM Etageres WHERE id_Etagere = ?", (id_etagere,))
        
        cur.execute("DELETE FROM Cave WHERE id_utilisateur = ? AND id_etagere = ?", (self.id_utilisateur, id_etagere))
        
        cur.execute("SELECT 1 FROM Cave WHERE id_utilisateur = ? AND id_etagere IS NOT NULL", (self.id_utilisateur,))
        reste_etageres = cur.fetchone()
        
        if not reste_etageres:
             cur.execute("INSERT INTO Cave (id_utilisateur, id_etagere) VALUES (?, ?)", (self.id_utilisateur, None))

        conn.commit()
        conn.close()

    def ajouter_bouteille_stock(self, id_etagere, id_bouteille, quantite_a_ajouter):
        conn = sqlite3.connect("Cave.db")
        cur = conn.cursor()

        try:
            cur.execute("SELECT capacite FROM Etageres WHERE id_Etagere = ?", (id_etagere,))
            etagere = cur.fetchone()
            if not etagere:
                return (False, "Erreur : Étagère non trouvée.")
            capacite_max = etagere[0]

            cur.execute("SELECT SUM(quantite) as total_stock FROM StockEtagere WHERE id_etagere = ?", (id_etagere,))
            stock_row = cur.fetchone()
            stock_actuel = stock_row[0] if stock_row[0] is not None else 0

            if (stock_actuel + quantite_a_ajouter) > capacite_max:
                places_restantes = capacite_max - stock_actuel
                return (False, f"Action impossible : L'étagère est pleine ou n'a pas assez de place. (Reste : {places_restantes} places)")

            cur.execute("SELECT quantite FROM StockEtagere WHERE id_etagere = ? AND id_bouteille = ?", (id_etagere, id_bouteille))
            bouteille_existante = cur.fetchone()

            if bouteille_existante:
                new_quantite = bouteille_existante[0] + quantite_a_ajouter
                cur.execute("UPDATE StockEtagere SET quantite = ? WHERE id_etagere = ? AND id_bouteille = ?", (new_quantite, id_etagere, id_bouteille))
            else:
                cur.execute("INSERT INTO StockEtagere (id_etagere, id_bouteille, quantite) VALUES (?, ?, ?)", (id_etagere, id_bouteille, quantite_a_ajouter))

            conn.commit()
            return (True, f"{quantite_a_ajouter} bouteille(s) ajoutée(s) avec succès.")

        except Exception as e:
            conn.rollback()
            return (False, f"Erreur lors de l'ajout : {e}")
        finally:
            conn.close()

    def retirer_bouteille_stock(self, id_etagere, id_bouteille, quantite_a_retirer):
        conn = sqlite3.connect("Cave.db")
        cur = conn.cursor()

        try:
            cur.execute("SELECT quantite FROM StockEtagere WHERE id_etagere = ? AND id_bouteille = ?", (id_etagere, id_bouteille))
            bouteille_stock = cur.fetchone()

            if not bouteille_stock:
                return (False, "Erreur : Cette bouteille n'est pas sur l'étagère.")
            
            stock_actuel = bouteille_stock[0]

            if quantite_a_retirer > stock_actuel:
                return (False, "Erreur : Quantité à retirer supérieure au stock.")

            if quantite_a_retirer == stock_actuel:
                cur.execute("DELETE FROM StockEtagere WHERE id_etagere = ? AND id_bouteille = ?", (id_etagere, id_bouteille))
            else:
                new_quantite = stock_actuel - quantite_a_retirer
                cur.execute("UPDATE StockEtagere SET quantite = ? WHERE id_etagere = ? AND id_bouteille = ?", (new_quantite, id_etagere, id_bouteille))

            conn.commit()
            return (True, f"{quantite_a_retirer} bouteille(s) retirée(s) du stock.")

        except Exception as e:
            conn.rollback()
            return (False, f"Erreur lors du retrait : {e}")
        finally:
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