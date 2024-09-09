import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid

from flask import redirect, render_template, session
from functools import wraps
from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")



def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def usd(value):
    """Format value as USD."""
    if value == None:
        return "$0.00"
    # if the value is in decimal then don't round off the value
    if isinstance(value, float):
        return f"${value}"

    return f"${value:,.2f}"

def name_intials():
    # Extracting intials to a variable
    name = db.execute("SELECT first_name, last_name FROM users WHERE id = ?", session["user_id"])
    nameintials = (name[0]["first_name"][0] + name[0]["last_name"][0]).upper()

    return nameintials
