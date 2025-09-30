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
                    CREATE TABLE IF NOT EXISTS Utilisateurs (
                        id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT,
                        prenom TEXT,
                        identifiant TEXT,
                        mdp TEXT,
                    )""")
        
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Bouteilles (
                        id_bouteilles INTEGER PRIMARY KEY,
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
            CREATE TABLE IF NOT EXISTS demande (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                FOREIGN KEY (usager_id) REFERENCES usager(id),
            )
        """)
                    
    def fin_connexion(self):
        self.conn.close()