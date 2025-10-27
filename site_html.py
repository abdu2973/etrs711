# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, session
import Bdd711
import class711

# Initialisation des bouteilles (si elles n'existent pas déjà)
test = Bdd711.Database()

rose = class711.Bouteilles(None, "Chateau la Coste", "Grand Vin Rose", "rose", 2022, "La Provence", "rose.jpg", 50.0)
rose.ajoute_bouteille()

bourgogne = class711.Bouteilles(None, "Cave d'aze", "Rouge Bourgogne", "rouge", 2025, "Bourgogne", "bourgogne.png", 80.0)
bourgogne.ajoute_bouteille()

bourgogne2 = class711.Bouteilles(None, "Non précisé", "La Vilageoise", "rose", 2025, "Languedoc", "la_villageoise.jpg", 3.0)
bourgogne2.ajoute_bouteille()

romanee_conti = class711.Bouteilles(None, "Romanée-Conti", "Romanée-Conti", "rouge", 2017, "Cote-D'Or", "romanee.jpg", 15417.0)
romanee_conti.ajoute_bouteille()

marquis = class711.Bouteilles(None, "Château / Domaine : Marquis des Lèves ", "Marquis des Lèves", "blanc", 2025, "Bordeaux", "marquis_des_leves.jpg", 5.90)
marquis.ajoute_bouteille()

# Flask
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

        utilisateur = class711.Utilisateurs(None, nom, prenom, identifiant, mdp)
        utilisateur.ajouter_utilisateur()
        flash("Inscription réussie ! Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for("connexion"))
    return render_template("formulaire_inscription.html")

@html.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        identifiant = request.form["identifiant"]
        mdp = request.form["mdp"]

        utilisateur = class711.Utilisateurs(None, None, None, identifiant, mdp)
        if utilisateur.connexion():
            session["id_utilisateur"] = utilisateur.id_utilisateur
            session["utilisateur_nom"] = utilisateur.nom
            session["connecte"] = True
            flash("Connexion réussie !", "success")
            return redirect(url_for("index"))
        else:
            flash("Identifiant ou mot de passe incorrect.", "error")
    return render_template("connexion.html")



@html.route("/cave", methods=["GET", "POST"])
def cave():
    id_utilisateur = session.get("id_utilisateur")
    if not id_utilisateur:
        flash("Vous devez être connecté pour accéder à votre cave.", "error")
        return redirect(url_for("connexion"))

    utilisateur = class711.Utilisateurs(id_utilisateur, None, None, None, None)

    if request.method == "POST":
        action = request.form.get("action")
        if action == "creer_cave":
            class711.Cave(id_utilisateur).cree_cave()
            flash("Votre cave a été créée avec succès.", "success")
        elif action == "ajouter_etagere":
            nom = request.form["nom"]
            capacite = request.form["capacite"]
            id_etagere = class711.Etageres(nom=nom, capacite=int(capacite), id_utilisateur=id_utilisateur).creer_etagere()
            flash(f"Étagère '{nom}' créée avec succès !" if id_etagere else "Erreur lors de la création de l'étagère.", "success")
        elif action == "supprimer_etagere":
            id_etagere = request.form.get("id_etagere")
            if id_etagere:
                class711.Etageres(None, None, id_utilisateur).supprimer_etagere(int(id_etagere))
                flash("Étagère supprimée avec succès.", "success")
        return redirect(url_for("cave"))

    conn = Bdd711.sqlite3.connect("Cave.db")
    cur = conn.cursor()
    cur.execute("SELECT nom, annee, photo, domaine_viticole, type_bouteilles, region, prix FROM Bouteille")
    bouteilles = cur.fetchall()
    conn.close()

    if not utilisateur.cave_exist():
        return render_template("cave.html", etageres=None, show_create_button=True, bouteilles=bouteilles)

    return render_template("cave.html", etageres=utilisateur.voir_cave(), show_create_button=False, bouteilles=bouteilles)



if __name__ == "__main__":
    html.run(debug=True, use_reloader=False)
