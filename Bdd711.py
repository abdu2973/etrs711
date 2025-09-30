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
                        id_bouteille INTEGER PRIMARY KEY,
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
            CREATE TABLE IF NOT EXISTS etageres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                stock_bouteilles INTEGER,
                capacite INTEGER,
                id_bouteille INTEGER,
                FOREIGN KEY (id_bouteille) REFERENCES Bouteille(id_bouteille)
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Cave (
                id_utilisateur INTEGER,
                id_bouteille INTEGER,
                FOREIGN KEY (id_utilisateur) REFERENCES Utilisateur(id_utilisateur),
                FOREIGN KEY (id_bouteille) REFERENCES Bouteille(id_bouteille)
            )
        """)
               
        
    def fin_connexion(self):
        self.conn.close()