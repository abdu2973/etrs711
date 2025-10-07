# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 15:59:22 2025

@author: user
"""
from flask import Flask, render_template, request, redirect, url_for,flash
import Bdd711
import class711

html = Flask(__name__)
html.secret_key = 'ma_clef_secrete_pour_la_session'

@html.route("/")
def index():
    return render_template("index.html")

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
            return redirect(url_for("index"))
        else:
            flash("Identifiant ou mot de passe incorrect.")
            return render_template("connexion.html")
    return render_template("connexion.html")




if __name__ == "__main__":
    html.run(debug=True)