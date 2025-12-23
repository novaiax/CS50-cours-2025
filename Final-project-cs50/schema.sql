PRAGMA foreign_keys = ON;

-- USERS
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);

-- TASKS (INCHANGÉES)
CREATE TABLE tasks (
    id_task INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    categorie TEXT NOT NULL,
    name TEXT NOT NULL,
    points REAL NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    point_type TEXT NOT NULL CHECK (point_type IN ('main', 'bonus')) DEFAULT 'main',
    note TEXT,
    link TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- DAYS
CREATE TABLE days (
    id_days INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    total_score REAL DEFAULT 0,
    energy_score INTEGER CHECK (energy_score BETWEEN 1 AND 5),
    pride_score INTEGER CHECK (pride_score BETWEEN 1 AND 4),
    main_score REAL DEFAULT 0,
    bonus_score REAL DEFAULT 0,
    UNIQUE (user_id, date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- CATEGORIES (INCHANGÉES)
CREATE TABLE categories (
    id_category INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    UNIQUE (user_id, name),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- COMPLETIONS
CREATE TABLE completions (
    id_completions INTEGER PRIMARY KEY AUTOINCREMENT,
    id_days INTEGER NOT NULL,
    id_task INTEGER NOT NULL,
    completed INTEGER NOT NULL CHECK (completed IN (0,1)),
    UNIQUE (id_days, id_task),
    FOREIGN KEY (id_days) REFERENCES days(id_days) ON DELETE CASCADE,
    FOREIGN KEY (id_task) REFERENCES tasks(id_task) ON DELETE CASCADE
);

-- TAGS
CREATE TABLE tags (
    id_tags INTEGER PRIMARY KEY AUTOINCREMENT,
    id_days INTEGER NOT NULL,
    tag TEXT NOT NULL,
    FOREIGN KEY (id_days) REFERENCES days(id_days) ON DELETE CASCADE
);

-- DAILY INPUTSSec

CREATE TABLE input_definitions (
    id_input_def INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('scale', 'boolean', 'text', 'select')),
    min_value INTEGER,
    max_value INTEGER,
    active INTEGER NOT NULL DEFAULT 1,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE input_rules (
    id_rule INTEGER PRIMARY KEY AUTOINCREMENT,
    id_input_def INTEGER NOT NULL,
    value INTEGER,
    score_delta INTEGER NOT NULL,
    FOREIGN KEY (id_input_def) REFERENCES input_definitions(id_input_def) ON DELETE CASCADE
);

CREATE TABLE daily_inputs (
    id_input INTEGER PRIMARY KEY AUTOINCREMENT,
    id_days INTEGER NOT NULL,
    id_input_def INTEGER NOT NULL,
    value INTEGER,
    note TEXT,
    UNIQUE (id_days, id_input_def),
    FOREIGN KEY (id_days) REFERENCES days(id_days) ON DELETE CASCADE,
    FOREIGN KEY (id_input_def) REFERENCES input_definitions(id_input_def) ON DELETE CASCADE
);
