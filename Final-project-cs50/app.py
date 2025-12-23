from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

from helpers import apology, login_required, create_today_if_not_exists, get_active_tasks, get_day_completions, calculate_day_score, toggle_completion, get_daily_inputs, save_daily_inputs, calculate_daily_input_score, load_journal_data

# Configure application
app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///schema.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# HOME
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user = db.execute(
        "SELECT username FROM users WHERE id = ?",
        session["user_id"]
    )[0]

    return render_template(
        "index.html",
        username=user["username"]
    )

#Index

#LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("missing credentials", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            username
        )

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username/password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("login.html")


#LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


#REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        nom = request.form.get("nom")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not nom or not username or not password:
            return apology("missing fields")

        if password != confirmation:
            return apology("passwords do not match")

        hash_pw = generate_password_hash(password)

        try:
            db.execute(
                "INSERT INTO users (nom, username, hash) VALUES (?, ?, ?)",
                nom, username, hash_pw
            )
        except ValueError:
            return apology("username already exists", 400)

        return redirect("/login")

    return render_template("register.html")

#ADMIN
@app.route("/admin")
@login_required
def admin():
    users = db.execute("SELECT id, nom, username FROM users")
    return render_template("admin.html", users=users)

#DELETE USER
@app.route("/delete_user", methods=["POST"])
@login_required
def delete_user():
    user_id = request.form.get("id")

    if not user_id:
        return apology("invalid user id")

    db.execute("DELETE FROM users WHERE id = ?", user_id)
    return redirect("/admin")




#Journal principal

@app.route("/journal", methods=["GET", "POST"])
@login_required
def journal():
    user_id = session["user_id"]
    today = date.today().isoformat()
    day_id = create_today_if_not_exists(user_id)

    #Scores existants
    scores = calculate_day_score(day_id)

    if request.method == "POST":
        #Toggle task
        task_id = request.form.get("task_id")
        if task_id:
            toggle_completion(day_id, int(task_id))
            calculate_day_score(day_id)

        #Sauvegarde daily inputs personnalisés
        save_daily_inputs(day_id, request.form)

        return redirect("/journal")

    tasks = get_active_tasks(user_id)
    completed_tasks = get_day_completions(day_id)

    categories = db.execute(
        """
        SELECT id_category, name
        FROM categories
        WHERE user_id = ?
        ORDER BY name
        """,
        user_id
    )

    custom_inputs = get_daily_inputs(user_id, day_id)

    return render_template(
        "journal.html",
        editable=True,
        today=today,
        tasks=tasks,
        completed_tasks=completed_tasks,
        categories=categories,
        scores=scores,
        custom_inputs=custom_inputs
    )


@app.route("/add_task", methods=["POST"])
@login_required
def add_task():
    user_id = session["user_id"]

    name = request.form.get("name")
    categorie = request.form.get("categorie")
    points = request.form.get("points")
    point_type = request.form.get("point_type")
    note = request.form.get("note")
    link = request.form.get("link")

    if not name or not categorie or not points or not point_type:
        return redirect("/journal")

    db.execute(
        """
        INSERT INTO tasks (user_id, categorie, name, points, point_type, note, link)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        user_id,
        categorie,
        name.strip(),
        float(points),
        point_type,
        note.strip() if note else None,
        link.strip() if link else None
    )

    return redirect("/journal")


@app.route("/delete_task", methods=["POST"])
@login_required
def delete_task():
    user_id = session["user_id"]
    task_id = request.form.get("task_id")

    if not task_id:
        return redirect("/journal")

    db.execute(
        """
        DELETE FROM tasks
        WHERE id_task = ? AND user_id = ?
        """,
        task_id,
        user_id
    )

    return redirect("/journal")\

@app.route("/add_category", methods=["POST"])
@login_required
def add_category():
    user_id = session["user_id"]
    name = request.form.get("name")

    if not name:
        return redirect("/journal")

    try:
        db.execute(
            """
            INSERT INTO categories (user_id, name)
            VALUES (?, ?)
            """,
            user_id,
            name.strip()
        )
    except Exception:
        pass

    return redirect("/journal")

@app.route("/delete_category", methods=["POST"])
@login_required
def delete_category():
    user_id = session["user_id"]
    category_id = request.form.get("category_id")
    confirm = request.form.get("confirm")

    if not category_id:
        return redirect("/journal")

    #Recupere la catégorie
    row = db.execute(
        "SELECT id_category, name FROM categories WHERE id_category = ? AND user_id = ?",
        category_id,
        user_id
    )

    if not row:
        return redirect("/journal")

    category_name = row[0]["name"]

    if confirm != "yes":
        return render_template(
            "confirm_delete_category.html",
            category_id=category_id,
            category_name=category_name
        )

    db.execute(
        "DELETE FROM tasks WHERE categorie = ? AND user_id = ?",
        category_name,
        user_id
    )

    db.execute(
        "DELETE FROM categories WHERE id_category = ? AND user_id = ?",
        category_id,
        user_id
    )

    return redirect("/journal")

@app.route("/edit_task", methods=["POST"])
@login_required
def edit_task():
    user_id = session["user_id"]

    task_id = request.form.get("task_id")
    name = request.form.get("name")
    categorie = request.form.get("categorie")
    points = request.form.get("points")
    point_type = request.form.get("point_type")
    note = request.form.get("note")
    link = request.form.get("link")

    link = link.strip() if link else None
    note = note.strip() if note else None

    if not task_id or not name or not categorie or not points or not point_type:
        return redirect("/journal")

    db.execute(
        """
        UPDATE tasks
        SET name = ?, categorie = ?, points = ?, point_type = ?, note = ?, link = ?
        WHERE id_task = ? AND user_id = ?
        """,
        name.strip(),
        categorie,
        float(points),
        point_type,
        note,
        link,
        task_id,
        user_id
    )

    return redirect("/journal")


#section 2


@app.route("/add_daily_input", methods=["POST"])
@login_required
def add_daily_input():
    user_id = session["user_id"]

    name = request.form.get("name")
    type_ = request.form.get("type")
    min_value = request.form.get("min_value")
    max_value = request.form.get("max_value")
    description = request.form.get("description")
    count_in_main = 1 if request.form.get("count_in_main") else 0

    if not name or not type_:
        return redirect("/journal")

    db.execute(
        """
        INSERT INTO input_definitions
        (user_id, name, type, min_value, max_value, description, count_in_main, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        """,
        user_id,
        name.strip(),
        type_,
        int(min_value) if min_value else None,
        int(max_value) if max_value else None,
        description.strip() if description else None,
        count_in_main
    )

    return redirect("/journal")

@app.route("/delete_daily_input", methods=["POST"])
@login_required
def delete_daily_input():
    user_id = session["user_id"]
    input_def_id = request.form.get("input_def_id")

    if not input_def_id:
        return redirect("/journal")

    db.execute(
        """
        DELETE FROM input_definitions
        WHERE id_input_def = ? AND user_id = ?
        """,
        input_def_id,
        user_id
    )

    return redirect("/journal")

@app.route("/update_daily_input", methods=["POST"])
@login_required
def update_daily_input():
    user_id = session["user_id"]
    day_id = create_today_if_not_exists(user_id)

    input_def_id = request.form.get("input_def_id")
    value = request.form.get("value")

    if not input_def_id:
        return ("", 204)

    #valeur vide = on supprime la réponse
    if value == "":
        db.execute(
            """
            DELETE FROM daily_inputs
            WHERE id_days = ? AND id_input_def = ?
            """,
            day_id,
            input_def_id
        )
        return ("", 204)

    #sinon = upsert
    db.execute(
        """
        INSERT OR REPLACE INTO daily_inputs
        (id_days, id_input_def, value)
        VALUES (?, ?, ?)
        """,
        day_id,
        input_def_id,
        value
    )

    return ("", 204)


#Historique


from collections import defaultdict


@app.route("/old_journals")
@login_required
def old_journals():
    days = db.execute(
        """
        SELECT date, total_score, main_score, bonus_score
        FROM days
        WHERE user_id = ?
        ORDER BY date DESC
        """,
        session["user_id"]
    )

    # valeurs factices pour satisfaire le template
    fake_day = {"date": None}

    return render_template(
        "old_journal.html",
        mode="list",
        days=days,
        day=fake_day,
        categories=[],
        tasks={},
        completed_tasks=set(),
        daily_inputs=[],
    )


@app.route("/old_journal/<date>")
@login_required
def old_journal(date):

    rows = db.execute(
        """
        SELECT *
        FROM days
        WHERE user_id = ? AND date = ?
        """,
        session["user_id"],
        date
    )

    if not rows:
        return redirect("/old_journals")

    day = rows[0]

    categories = db.execute(
        """
        SELECT id_category, name
        FROM categories
        WHERE user_id = ?
        ORDER BY name
        """,
        session["user_id"]
    )

    raw_tasks = db.execute(
        """
        SELECT *
        FROM tasks
        WHERE user_id = ? AND active = 1
        """,
        session["user_id"]
    )

    grouped_tasks = defaultdict(list)
    for task in raw_tasks:
        grouped_tasks[task["categorie"]].append(task)

    completed = db.execute(
        """
        SELECT id_task
        FROM completions
        WHERE id_days = ? AND completed = 1
        """,
        day["id_days"]
    )
    completed_tasks = {row["id_task"] for row in completed}

    daily_inputs = db.execute(
        """
        SELECT
            d.id_input_def,
            d.name,
            d.type,
            d.min_value,
            d.max_value,
            d.description,
            di.value,
            di.note
        FROM input_definitions d
        LEFT JOIN daily_inputs di
            ON d.id_input_def = di.id_input_def
           AND di.id_days = ?
        WHERE d.user_id = ?
          AND d.active = 1
        ORDER BY d.id_input_def
        """,
        day["id_days"],
        session["user_id"]
    )

    return render_template(
        "old_journal.html",
        mode="detail",
        days=[],
        day=day,
        categories=categories,
        tasks=grouped_tasks,
        completed_tasks=completed_tasks,
        daily_inputs=daily_inputs,
    )
