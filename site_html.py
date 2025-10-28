# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, session
import Bdd711
import class711

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

html = Flask(__name__)
html.secret_key = 'ma_clef_secrete_pour_la_session'

@html.route("/")
def index():
    conn = Bdd711.sqlite3.connect("Cave.db")
    conn.row_factory = Bdd711.sqlite3.Row # Pour accéder par nom de colonne
    cur = conn.cursor()
    cur.execute("SELECT id_bouteille, nom, annee, photo, domaine_viticole, type_bouteilles, region, prix FROM Bouteille")
    
    bouteilles_list = []
    for row in cur.fetchall():
        b_dict = dict(row)
        b_dict['note_moyenne'] = class711.Notes.calculer_note_moyenne(b_dict['id_bouteille'])
        bouteilles_list.append(b_dict)
        
    conn.close()

    est_connecte = session.get("connecte", False)
    nom_utilisateur = session.get("utilisateur_nom", None)
    return render_template("index.html", bouteilles=bouteilles_list, est_connecte=est_connecte, nom_utilisateur=nom_utilisateur)

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


@html.route("/mes-notes")
def mes_notes():
    id_utilisateur = session.get("id_utilisateur")
    if not id_utilisateur:
        flash("Vous devez être connecté pour voir les notes.", "error")
        return redirect(url_for("connexion"))
    
    notes_archivees = class711.Notes.voir_toutes_les_notes()
    
    return render_template("mes_notes.html", 
                           notes=notes_archivees,
                           est_connecte=session.get("connecte", False),
                           nom_utilisateur=session.get("utilisateur_nom", None))


@html.route("/cave", methods=["GET", "POST"])
def cave():
    id_utilisateur = session.get("id_utilisateur")
    if not id_utilisateur:
        flash("Vous devez être connecté pour accéder à votre cave.", "error")
        return redirect(url_for("connexion"))

    utilisateur = class711.Utilisateurs(id_utilisateur, None, None, None, None)
    etagere_manager = class711.Etageres(nom=None, capacite=None, id_utilisateur=id_utilisateur)

    if request.method == "POST":
        action = request.form.get("action")
        if action == "creer_cave":
            class711.Cave(id_utilisateur).cree_cave()
            flash("Votre cave a été créée avec succès.", "success")
        elif action == "ajouter_etagere":
            nom = request.form["nom"]
            capacite = request.form["capacite"]
            
            etagere_specifique = class711.Etageres(nom=nom, capacite=int(capacite), id_utilisateur=id_utilisateur)
            id_etagere = etagere_specifique.creer_etagere()
            
            flash(f"Étagère '{nom}' créée avec succès !" if id_etagere else "Erreur lors de la création de l'étagère.", "success")
        elif action == "supprimer_etagere":
            id_etagere = request.form.get("id_etagere")
            if id_etagere:
                etagere_manager.supprimer_etagere(int(id_etagere))
                flash("Étagère supprimée avec succès.", "success")
        
        elif action == "ajouter_bouteille":
            try:
                id_etagere = int(request.form["id_etagere"])
                id_bouteille = int(request.form["id_bouteille"])
                quantite = int(request.form["quantite"])
                
                if quantite <= 0:
                     flash("La quantité doit être supérieure à 0.", "error")
                else:
                    success, message = etagere_manager.ajouter_bouteille_stock(id_etagere, id_bouteille, quantite)
                    if success: flash(message, "success")
                    else: flash(message, "error")
                        
            except ValueError:
                flash("Erreur dans les données envoyées.", "error")
            except Exception as e:
                flash(f"Une erreur est survenue: {e}", "error")
                
        elif action == "retirer_bouteille":
            try:
                id_etagere = int(request.form["id_etagere"])
                id_bouteille = int(request.form["id_bouteille"])
                success, message = etagere_manager.retirer_bouteille_stock(id_etagere, id_bouteille, 1)
                
                if success: flash(message, "success")
                else: flash(message, "error")
            except Exception as e:
                flash(f"Une erreur est survenue: {e}", "error")

        elif action == "archiver_bouteille":
            try:
                id_etagere = int(request.form["id_etagere"])
                id_bouteille = int(request.form["id_bouteille"])
                note = float(request.form["note"])
                commentaire = request.form["commentaire"]

                success, message = etagere_manager.retirer_bouteille_stock(id_etagere, id_bouteille, 1)
                
                if success:
                    flash(message, "success")
                    note_obj = class711.Notes(
                        id_utilisateur=id_utilisateur,
                        id_bouteilles=id_bouteille,
                        id_notes=None,
                        notes=note,
                        commentaires=commentaire
                    )
                    success_note, message_note = note_obj.ajouter_note()
                    if success_note: flash(message_note, "success")
                    else: flash(message_note, "error")
                else:
                    flash(message, "error")
            
            except Exception as e:
                flash(f"Une erreur est survenue lors de l'archivage: {e}", "error")

        return redirect(url_for("cave"))

    sort_by = request.args.get('sort_by', 'nom_asc')

    conn = Bdd711.sqlite3.connect("Cave.db")
    conn.row_factory = Bdd711.sqlite3.Row # Pour accéder par nom de colonne
    cur = conn.cursor()
    cur.execute("SELECT id_bouteille, nom FROM Bouteille ORDER BY nom") # Juste id et nom pour le dropdown
    bouteilles_dropdown = cur.fetchall() 
    
    cur.execute("SELECT id_bouteille, nom, annee, photo, domaine_viticole, type_bouteilles, region, prix FROM Bouteille ORDER BY nom")
    bouteilles_dispo_list = []
    for row in cur.fetchall():
        b_dict = dict(row)
        b_dict['note_moyenne'] = class711.Notes.calculer_note_moyenne(b_dict['id_bouteille'])
        bouteilles_dispo_list.append(b_dict)

    conn.close()

    if not utilisateur.cave_exist():
        return render_template("cave.html", 
                               etageres=None, 
                               show_create_button=True, 
                               bouteilles_dropdown=bouteilles_dropdown, 
                               mes_notes=None, 
                               sort_by=sort_by,
                               bouteilles_disponibles=bouteilles_dispo_list)

    etageres = utilisateur.voir_cave(sort_by)
    mes_notes_personnelles = utilisateur.voir_notes()

    return render_template("cave.html", 
                           etageres=etageres, 
                           show_create_button=False, 
                           bouteilles_dropdown=bouteilles_dropdown,
                           mes_notes=mes_notes_personnelles,
                           sort_by=sort_by,
                           bouteilles_disponibles=bouteilles_dispo_list)



if __name__ == "__main__":
    html.run(debug=True, use_reloader=False)