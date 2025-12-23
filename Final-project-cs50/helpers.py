import requests

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

def registred():
    """Render message to inform user is registrer."""
    return render_template("registered.html")


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def lookup(symbol):
    """Look up quote for symbol."""
    url = f"https://finance.cs50.io/quote?symbol={symbol.upper()}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        quote_data = response.json()
        return {
            "name": quote_data["companyName"],
            "price": quote_data["latestPrice"],
            "symbol": symbol.upper()
        }
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


from datetime import date
from cs50 import SQL

db = SQL("sqlite:///schema.db")


def create_today_if_not_exists(user_id):
    today = date.today().isoformat()

    rows = db.execute(
        "SELECT id_days FROM days WHERE user_id = ? AND date = ?",
        user_id,
        today
    )

    if rows:
        return rows[0]["id_days"]

    db.execute(
        "INSERT INTO days (user_id, date) VALUES (?, ?)",
        user_id,
        today
    )

    rows = db.execute(
        "SELECT id_days FROM days WHERE user_id = ? AND date = ?",
        user_id,
        today
    )

    return rows[0]["id_days"]

def get_active_tasks(user_id):
    rows = db.execute(
        """
        SELECT id_task, categorie, name, points, point_type, note, link
                FROM tasks
                        WHERE user_id = ? AND active = 1
                                ORDER BY categorie, id_task
        """,
        user_id
    )

    tasks = {}

    for row in rows:
        categorie = row["categorie"]
        if categorie not in tasks:
            tasks[categorie] = []

        tasks[categorie].append({
            "id_task": row["id_task"],
            "name": row["name"],
            "points": row["points"],
            "point_type": row["point_type"],
            "categorie": row["categorie"],
            "note": row["note"],
            "link": row["link"]
        })

    return tasks

def get_day_completions(day_id):
    rows = db.execute(
        """
        SELECT id_task
        FROM completions
        WHERE id_days = ? AND completed = 1
        """,
        day_id
    )

    completed_tasks = []

    for row in rows:
        completed_tasks.append(row["id_task"])

    return completed_tasks


def calculate_day_score(day_id):

    # 1️⃣ DAILY INPUTS — MAX (dès la définition)
    rows_inputs_def = db.execute(
        """
        SELECT max_value
        FROM input_definitions
        WHERE count_in_main = 1
        AND type = 'scale'
        AND active = 1
        """
    )

    inputs_max = sum(row["max_value"] or 0 for row in rows_inputs_def)


    # 2️⃣ DAILY INPUTS — DONE (réponses du jour)
    rows_inputs_done = db.execute(
        """
        SELECT di.value
        FROM daily_inputs di
        JOIN input_definitions d
            ON d.id_input_def = di.id_input_def
        WHERE di.id_days = ?
        AND d.count_in_main = 1
        AND d.type = 'scale'
        """,
        day_id
    )

    inputs_done = sum(int(row["value"]) for row in rows_inputs_done if row["value"] is not None)


    # 3️⃣ TASKS MAIN — DONE
    rows_main_done = db.execute(
        """
        SELECT SUM(tasks.points) AS total
        FROM completions
        JOIN tasks ON completions.id_task = tasks.id_task
        WHERE completions.id_days = ?
        AND completions.completed = 1
        AND tasks.point_type = 'main'
        AND tasks.active = 1
        """,
        day_id
    )

    main_tasks_done = rows_main_done[0]["total"] or 0


    # 4️⃣ TASKS MAIN — MAX
    rows_main_max = db.execute(
        """
        SELECT SUM(points) AS total
        FROM tasks
        WHERE point_type = 'main'
        AND active = 1
        """
    )

    main_tasks_max = rows_main_max[0]["total"] or 0


    # 5️⃣ BONUS
    rows_bonus = db.execute(
        """
        SELECT SUM(tasks.points) AS total
        FROM completions
        JOIN tasks ON completions.id_task = tasks.id_task
        WHERE completions.id_days = ?
        AND completions.completed = 1
        AND tasks.point_type = 'bonus'
        AND tasks.active = 1
        """,
        day_id
    )

    bonus = rows_bonus[0]["total"] or 0


    # 6️⃣ TOTALS
    main_done = main_tasks_done + inputs_done
    main_max = main_tasks_max + inputs_max
    total = main_done + bonus


    # 7️⃣ SAVE
    db.execute(
        """
        UPDATE days
        SET main_score = ?, bonus_score = ?, total_score = ?
        WHERE id_days = ?
        """,
        main_done, bonus, total, day_id
    )

    return {
        "main_done": main_done,
        "main_max": main_max,
        "bonus": bonus,
        "total": total
    }




def toggle_completion(day_id, task_id):
    rows = db.execute(
        """
        SELECT completed
        FROM completions
        WHERE id_days = ? AND id_task = ?
        """,
        day_id,
        task_id
    )

    if not rows:
        # Aucune entrée → on coche
        db.execute(
            """
            INSERT INTO completions (id_days, id_task, completed)
            VALUES (?, ?, 1)
            """,
            day_id,
            task_id
        )
    else:
        # Entrée existante → on inverse
        current_state = rows[0]["completed"]
        new_state = 0 if current_state == 1 else 1

        db.execute(
            """
            UPDATE completions
            SET completed = ?
            WHERE id_days = ? AND id_task = ?
            """,
            new_state,
            day_id,
            task_id
        )


def get_daily_inputs(user_id, day_id):
    return db.execute(
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
            ON di.id_input_def = d.id_input_def
            AND di.id_days = ?
        WHERE d.user_id = ?
        AND d.active = 1
        ORDER BY d.id_input_def
        """,
        day_id,
        user_id
    )


def save_daily_inputs(day_id, form):
    for key in form:
        if key.startswith("input_"):
            input_def_id = int(key.split("_")[1])
            value = form.get(key)

            if value == "":
                continue

            db.execute(
                """
                INSERT OR REPLACE INTO daily_inputs
                (id_days, id_input_def, value)
                VALUES (?, ?, ?)
                """,
                day_id,
                input_def_id,
                int(value)
            )

def calculate_daily_input_score(day_id):
    rows = db.execute(
        """
        SELECT r.score_delta
        FROM daily_inputs di
        JOIN input_rules r
            ON r.id_input_def = di.id_input_def
            AND r.value = di.value
        WHERE di.id_days = ?
        """,
        day_id
    )

    return sum(row["score_delta"] for row in rows)



def load_journal_data(day_id, user_id):
    sections = db.execute(
        """
        SELECT id_section, name
        FROM sections
        WHERE user_id = ? AND active = 1
        ORDER BY position
        """,
        user_id
    )

    categories = db.execute(
        """
        SELECT id_category, name, id_section
        FROM categories
        WHERE user_id = ?
        ORDER BY name
        """,
        user_id
    )

    tasks = db.execute(
        """
        SELECT *
        FROM tasks
        WHERE user_id = ? AND active = 1
        """,
        user_id
    )

    completed = db.execute(
        """
        SELECT id_task
        FROM completions
        WHERE id_days = ? AND completed = 1
        """,
        day_id
    )

    completed_tasks = {row["id_task"] for row in completed}

    daily_inputs = db.execute(
        """
        SELECT *
        FROM daily_inputs
        WHERE id_days = ?
        """,
        day_id
    )

    return sections, categories, tasks, completed_tasks, daily_inputs
