CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO tasks (title, done)
SELECT * FROM (VALUES
    ('Buy milk', FALSE),
    ('Walk dog', FALSE),
    ('Write report', TRUE)
) AS seed(title, done)
WHERE NOT EXISTS (SELECT 1 FROM tasks);