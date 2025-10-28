# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 16:20:18 2025

@author: user
"""

import sqlite3

class Database : 
    
    def __init__(self,db_name="Cave.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
        
        
    
    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute(""" 
                    CREATE TABLE IF NOT EXISTS Utilisateur (
                        id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT,
                        prenom TEXT,
                        identifiant TEXT,
                        mdp TEXT
                    )""")
        
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Bouteille (
                        id_bouteille INTEGER PRIMARY KEY AUTOINCREMENT,
                        domaine_viticole TEXT,
                        nom TEXT,
                        type_bouteilles TEXT,
                        annee INTEGER,
                        region TEXT,
                        photo TEXT,
                        prix REAL
                       

                        )
                    """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Etageres (
                id_Etagere INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                capacite INTEGER
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS StockEtagere (
                id_etagere INTEGER,
                id_bouteille INTEGER,
                quantite INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (id_etagere, id_bouteille),
                FOREIGN KEY (id_etagere) REFERENCES Etageres(id_Etagere) ON DELETE CASCADE,
                FOREIGN KEY (id_bouteille) REFERENCES Bouteille(id_bouteille)
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Cave (
                id_utilisateur INTEGER,
                id_etagere INTEGER,
                FOREIGN KEY (id_utilisateur) REFERENCES Utilisateur(id_utilisateur),
                FOREIGN KEY (id_etagere) REFERENCES Etageres(id_etagere)
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Notes (
                id_utilisateur INTEGER,
                id_bouteille INTEGER,
                notes REAL CHECK(notes >= 0 AND notes <= 20),
                commentaires TEXT CHECK(LENGTH(commentaires) <= 150),
                id_commentaires INTEGER PRIMARY KEY AUTOINCREMENT,
                FOREIGN KEY (id_utilisateur) REFERENCES Utilisateur(id_utilisateur),
                FOREIGN KEY (id_bouteille) REFERENCES Bouteille(id_bouteille)            )
        """)

        self.conn.commit()
        
    def fin_connexion(self):
        self.conn.close()