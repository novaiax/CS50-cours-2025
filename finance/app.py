import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    rows = db.execute(
        """
        SELECT symbol, SUM(shares) AS shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING shares > 0
        """,
        session["user_id"]
    )

    portfolio = []
    total_stock_value = 0

    for row in rows:
        if row["shares"] <= 0:
            continue

        stock = lookup(row["symbol"])
        price = stock["price"]
        total = price * row["shares"]
        total_stock_value += total

        portfolio.append({
            "symbol": row["symbol"],
            "shares": row["shares"],
            "price": price,
            "total": total

        })

    cash = db.execute(
        "SELECT cash FROM users WHERE id = ?",
        session["user_id"]
    )[0]["cash"]

    grand_total = total_stock_value + cash

    return render_template(
        "index.html",
        portfolio=portfolio,
        cash=cash,
        grand_total=grand_total
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")

    symbol = request.form.get("symbol")
    shares = request.form.get("shares")

    try:
        shares = int(shares)
        if shares <= 0:
            return apology("Positive number required")
    except ValueError:
        return apology("Positive number required")

    if not symbol:
        return apology("symbol required")

    stock = lookup(symbol)

    if stock is None:
        return apology("invalid symbol")

    price = stock["price"]
    total_cost = price * shares
    rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = rows[0]["cash"]

    if cash < total_cost:
        return apology("can't afford")

    db.execute(
        """
        INSERT INTO transactions (user_id, symbol, shares, price, timestamp)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
        session["user_id"],
        stock["symbol"],
        shares,
        price
    )

    db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total_cost, session["user_id"])

    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute(
        """
        SELECT symbol, shares, price, timestamp
        FROM transactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
        """,
        session["user_id"]
    )

    return render_template("history.html", transactions=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    symbol = request.form.get("symbol")

    if not symbol:
        return apology("symbol required")

    stock = lookup(symbol)

    if stock is None:
        return apology("invalid symbol")

    return render_template("quoted.html", stock=stock)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username").strip()

        if not username:
            return apology("username invalid")

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not password or not confirmation:
            return apology("password required")

        if password != confirmation:
            return apology("passwords do not match")

        hashed_password = generate_password_hash(password)

        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                hashed_password
            )
            return render_template("registered.html")
        except ValueError:
            return apology("username already exists", 400)

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "GET":
        stocks = db.execute(
            """
            SELECT symbol, SUM(shares) AS total_shares
            FROM transactions
            WHERE user_id = ?
            GROUP BY symbol
            HAVING total_shares > 0
            """,
            session["user_id"]
        )

        return render_template("sell.html", stocks=stocks)

    symbol = request.form.get("symbol")
    shares = request.form.get("shares")

    if not symbol:
        return apology("symbol required")

    try:
        shares = int(shares)
        if shares <= 0:
            return apology("positive number required")
    except ValueError:
        return apology("positive number required")

    rows = db.execute(
        """
        SELECT SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ? AND symbol = ?
        """,
        session["user_id"],
        symbol
    )

    if rows[0]["total_shares"] is None or rows[0]["total_shares"] < shares:
        return apology("too many shares")

    stock = lookup(symbol)
    price = stock["price"]
    total_gain = price * shares

    db.execute(
        """
        INSERT INTO transactions (user_id, symbol, shares, price, timestamp)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
        session["user_id"],
        symbol,
        -shares,
        price
    )

    rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = rows[0]["cash"]

    db.execute(
        "UPDATE users SET cash = ? WHERE id = ?",
        cash + total_gain,
        session["user_id"]
    )

    return redirect("/")

# ADMIN


@app.route("/admin")
def admin():
    users = db.execute("SELECT id, username, cash FROM users")
    return render_template("admin.html", users=users)


@app.route("/delete_user", methods=["POST"])
def delete_user():
    user_id = request.form.get("id")

    if not user_id:
        return apology("invalid user id")

    db.execute("DELETE FROM users WHERE id = ?", user_id)

    return redirect("/admin")
