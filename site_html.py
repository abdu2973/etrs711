# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 15:59:22 2025

@author: user
"""
from flask import Flask, render_template, request, redirect, url_for,flash,session
import Bdd711
import class711

test = Bdd711.Database()
        
rose = class711.Bouteilles(None,"Chateau la Coste", "Grand Vin Rose", "rose", 2022, "La Provence","rose.jpg", 50.0)
rose.ajoute_bouteille()

bourgogne = class711.Bouteilles(None, "Cave d'aze", "Rouge Bourgogne", "rouge", 2025, "Bourgogne","bourgogne.png" , 80.0)
bourgogne.ajoute_bouteille()

bourgogne = class711.Bouteilles(None, "Non précisé", "La Vilageoise", "rose", 2025, "Languedoc","la_villageoise.jpg" , 3.0)
bourgogne.ajoute_bouteille()

romanee_conti =class711.Bouteilles(None, "Romanée-Conti ", "Romanée-Conti", "rouge", 2017, "Cote-D'Or","romanee.jpg" , 15417.0)
romanee_conti.ajoute_bouteille()

marquis = class711.Bouteilles(None, "Château / Domaine : Marquis des Lèves ", "Marquis des Lèves", "blanc", 2025, "Bordeaux", "marquis_des_leves.jpg",5.90 )
marquis.ajoute_bouteille()

html = Flask(__name__)
html.secret_key = 'ma_clef_secrete_pour_la_session'

@html.route("/")
def index():
    conn = Bdd711.sqlite3.connect("Cave.db")
    cur = conn.cursor()
    cur.execute("SELECT nom, annee, photo, domaine_viticole, type_bouteilles, region, prix FROM Bouteille")
    bouteilles = cur.fetchall()
    conn.close()

    est_connecte = session.get("connecte", False)
    nom_utilisateur = session.get("utilisateur_nom", None)
    return render_template("index.html", bouteilles=bouteilles, est_connecte=est_connecte, nom_utilisateur=nom_utilisateur)



@html.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        identifiant = request.form["identifiant"]
        mdp = request.form["mdp"]
        id_util = None
       
        utilisateur = class711.Utilisateurs(id_util,nom, prenom, identifiant, mdp)
        utilisateur.ajouter_utilisateur()
        return redirect(url_for("index"))  

    return render_template("formulaire_inscription.html")  

@html.route("/connexion", methods=["GET", "POST"])


def connexion():
    if request.method == "POST":
        identifiant = request.form["identifiant"]
        mdp = request.form["mdp"]

        utilisateur = class711.Utilisateurs(None, None, None, identifiant, mdp)
        
        if utilisateur.connexion():
           
            session["utilisateur_id"] = utilisateur.id_utilisateur
            session["utilisateur_nom"] = utilisateur.nom
            session["connecte"] = True
            return redirect(url_for("index"))
        else:
            flash("Identifiant ou mot de passe incorrect.")
            return render_template("connexion.html")
    return render_template("connexion.html")

@html.route("/cave", methods=["GET", "POST"])
def cave():
    if not session.get("connecte"):
        flash("Vous devez être connecté pour accéder à votre cave.")
        return redirect(url_for("connexion"))

    id_utilisateur = session["utilisateur_id"]
    utilisateur = class711.Utilisateurs(id_utilisateur, None, None, None, None)

    if request.method == "POST":
        nouvelle_cave = class711.Cave(id_utilisateur)
        nouvelle_cave.cree_cave()
        flash("Votre cave a été créée avec succès.")
        return redirect(url_for("cave"))

    cave = utilisateur.voir_cave()  
    return render_template("cave.html", cave=cave)




if __name__ == "__main__":
    html.run(debug=True)
    #test

