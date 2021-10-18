DROP TABLE IF EXISTS project;

CREATE TABLE project (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT UNIQUE NOT NULL,
    project_description TEXT
);