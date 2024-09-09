import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from flask_session import Session

from helpers import login_required, usd, name_intials

# Configure application
inter = Blueprint('international', __name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@inter.route("/international")
@login_required
def inter_page():
    # Extracting intials to a variable
    nameintials = name_intials()

    # Extracting the international owned by the user
    international = db.execute("SELECT * FROM international WHERE user_id = ?", session["user_id"])

    # Modifying the value to display on the webpage
    i = 1
    totalvalue = 0
    for inter in international:
        inter["total_value_of_inter"] = usd(inter["price_of_inter"] * inter["quantity"])
        totalvalue += inter["price_of_inter"] * inter["quantity"]
        inter["price_of_inter"] = usd(inter["price_of_inter"])
        inter["number"] = i
        i += 1

    # Returning international.html page
    return render_template("international.html",
                           nameintials=nameintials,
                           page_title="International",
                           international = international,
                           totalvalue=usd(totalvalue))


@inter.route("/add-inter", methods=["GET", "POST"])
@login_required
def add_inter():
    nameintials = name_intials()

    # Verifying the input by the user
    if request.method == "POST":
        if not request.form.get("intername"):
            return render_template("add-international.html",
                                   nameintials=nameintials,
                                   page_title="Add International",
                                   intername="Enter international stock name")

        if not request.form.get("quantity"):
            return render_template("add-international.html",
                                   nameintials=nameintials,
                                   page_title="Add International",
                                   quantity="Must enter the number of shares")

        if not request.form.get("priceofinter"):
            return render_template("add-international.html",
                                   nameintials=nameintials,
                                   page_title="Add International",
                                   priceofinter ="Must enter the price of stock")


        if int(request.form.get("quantity")) < 1:
            return render_template("add-international.html",
                                   nameintials=nameintials,
                                   page_title="Add International",
                                   quantity="Enter valid number of shares")

        if float(request.form.get("priceofinter")) < 0:
            return render_template("add-international.html",
                                   nameintials=nameintials,
                                   page_title="Add International",
                                   priceofinter="Enter valid price of stock")

        db.execute("INSERT INTO international (user_id, inter_name, quantity, price_of_inter) VALUES (?, ?, ?, ?)",
                   session["user_id"], request.form.get("intername"),
                   request.form.get("quantity"), request.form.get("priceofinter"))

        return redirect("/international")

    else:
        # Returning add-international.html page
        return render_template("add-international.html",
                               nameintials=nameintials,
                               page_title="Add International")


@inter.route("/delete-inter", methods=["POST"])
@login_required
def delete_inter():
    # Deleting the international from the table
    db.execute("DELETE FROM international WHERE id = ?", request.form.get("inter-id"))

    # Redirecting to International webpage
    return redirect("/international")

