import re
import sqlite3
from datetime import date
from flask import (Flask, render_template, request, redirect,
                   url_for, flash, g, jsonify)

app = Flask(__name__)
app.config["SECRET_KEY"] = "changez-moi"
BASE = "restaurant.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(BASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def fermer_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with open("schema.sql", encoding="utf-8") as f:
            db.executescript(f.read())
        db.commit()


@app.route("/")
def accueil():
    return render_template("index.html")


@app.route("/menu")
def menu():
    plats = get_db().execute(
        "SELECT nom, categorie, prix FROM plats ORDER BY categorie, prix"
    ).fetchall()
    return render_template("menu.html", plats=plats)


@app.route("/reserver", methods=["GET", "POST"])
def reserver():
    if request.method == "POST":
        nom = request.form.get("nom", "").strip()
        tel = request.form.get("telephone", "").replace(" ", "")
        jour = request.form.get("date", "")
        service = request.form.get("service", "")
        personnes = request.form.get("personnes", "")

        erreurs = []
        if not nom:
            erreurs.append("Le nom est obligatoire.")
        if not re.fullmatch(r"6\d{8}", tel):
            erreurs.append("Numéro invalide : 9 chiffres commençant par 6.")
        if service not in ("midi", "soir"):
            erreurs.append("Service inconnu.")
        if not personnes.isdigit() or not 1 <= int(personnes) <= 20:
            erreurs.append("Le nombre de personnes doit être entre 1 et 20.")
        try:
            if date.fromisoformat(jour) < date.today():
                erreurs.append("La date est déjà passée.")
        except ValueError:
            erreurs.append("Date invalide.")

        if erreurs:
            for e in erreurs:
                flash(e, "erreur")
            return render_template("reserver.html", donnees=request.form), 400

        db = get_db()
        db.execute(
            "INSERT INTO reservations (nom, telephone, date, service, personnes) "
            "VALUES (?, ?, ?, ?, ?)",
            (nom, tel, jour, service, int(personnes)))
        db.commit()
        flash(f"Merci {nom}, votre table est réservée pour le {jour} ({service}).",
              "succes")
        return redirect(url_for("reserver"))

    return render_template("reserver.html", donnees={})


@app.route("/reservations")
def reservations():
    lignes = get_db().execute(
        "SELECT * FROM reservations ORDER BY date, service").fetchall()
    return render_template("reservations.html", reservations=lignes)


@app.route("/reservations/<int:id_resa>/annuler", methods=["POST"])
def annuler(id_resa):
    db = get_db()
    db.execute("DELETE FROM reservations WHERE id = ?", (id_resa,))
    db.commit()
    flash("Réservation annulée.", "succes")
    return redirect(url_for("reservations"))


@app.route("/api/menu")
def api_menu():
    plats = get_db().execute("SELECT nom, categorie, prix FROM plats").fetchall()
    return jsonify([dict(p) for p in plats])


if __name__ == "__main__":
    app.run(debug=True)