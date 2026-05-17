from flask import Flask, render_template, request, redirect, session, jsonify

from config import Config
from database.db import db
from database.models import Client
from database.crud import (
    create_client,
    get_all_clients
)

app = Flask(__name__)
app.secret_key = "your-secret-key"
app.config.from_object(Config)

db.init_app(app)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    clients = get_all_clients()

    return render_template(
        "home.html",
        clients=clients
    )


@app.route("/add", methods=["POST"])
def add_client():
    name = request.form.get("name")
    number = request.form.get("number")
    bouquet = request.form.get("bouquet")

    create_client(name, number, bouquet)

    return redirect("/")


@app.route("/save-data", methods=["POST"])
def save_data():
    data = request.get_json()

    session["product"] = {
        "name": data.get("name"),
        "price": data.get("price"),
        "count": data.get("count"),
        "img": data.get("img"),
        "tags": data.get("tags")
    }

    return jsonify({"success": True})

@app.route("/save-order", methods=["POST"])
def save_order():
    data = request.get_json()

    session["product"] = {
        "name": data.get("name"),
        "price": data.get("price"),
        "count": data.get("count"),
        "user": data.get("user"),
        "phone": data.get("phone")
    }

    return jsonify({"success": True})


@app.route("/bouquets")
def bouquets():
    product = session.get("product")

    return render_template("bouquets.html", product=product)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="192.168.0.102"
    )