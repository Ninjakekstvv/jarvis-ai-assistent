import sqlite3
from datetime import datetime


DB_NAME = "memory.db"



def datenbank():

    return sqlite3.connect(DB_NAME)



def init_tasks():

    conn = datenbank()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            task TEXT NOT NULL,

            status TEXT DEFAULT 'offen',

            priority TEXT DEFAULT 'normal',

            assigned_to TEXT DEFAULT 'Master',

            bereich TEXT DEFAULT 'allgemein',

            created TEXT

        )
    """)

    conn.commit()
    conn.close()



def aufgabe_erstellen(task, priority="normal"):

    if not task:
        return False


    conn = datenbank()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO tasks
        (
            task,
            status,
            priority,
            created
        )

        VALUES (?,?,?,?)
        """,
        (
            task,
            "offen",
            priority,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )
        )
    )


    conn.commit()
    conn.close()


    return True



def aufgaben_anzeigen():

    conn = datenbank()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            id,
            task,
            status,
            priority,
            created

        FROM tasks

        ORDER BY id ASC
        """
    )


    daten = cursor.fetchall()


    conn.close()


    return daten



def aufgabe_abrufen(task_id):

    conn = datenbank()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            id,
            task,
            status,
            priority,
            created

        FROM tasks

        WHERE id=?
        """,
        (task_id,)
    )


    daten = cursor.fetchone()


    conn.close()


    return daten



def aufgabe_erledigt(task_id):

    conn = datenbank()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE tasks

        SET status='erledigt'

        WHERE id=?
        """,
        (task_id,)
    )


    geändert = cursor.rowcount


    conn.commit()
    conn.close()


    return geändert > 0



def prioritaet_aendern(task_id, priority):

    conn = datenbank()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE tasks

        SET priority=?

        WHERE id=?
        """,
        (
            priority,
            task_id
        )
    )


    geändert = cursor.rowcount


    conn.commit()
    conn.close()



def aufgabe_zuweisen(task_id, person):

    conn = datenbank()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE tasks

        SET assigned_to=?

        WHERE id=?
        """,
        (
            person,
            task_id
        )
    )


    geändert = cursor.rowcount


    conn.commit()
    conn.close()


    return geändert > 0



    return geändert > 0

def bereich_aendern(task_id, bereich):

    conn = datenbank()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE tasks

        SET bereich=?

        WHERE id=?
        """,
        (
            bereich,
            task_id
        )
    )


    geändert = cursor.rowcount


    conn.commit()
    conn.close()


    return geändert > 0

def aufgabe_loeschen(task_id):

    conn = datenbank()
    cursor = conn.cursor()


    cursor.execute(
        """
        DELETE FROM tasks

        WHERE id=?
        """,
        (task_id,)
    )


    gelöscht = cursor.rowcount


    conn.commit()
    conn.close()


    return gelöscht > 0



def offene_aufgaben():

    conn = datenbank()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            id,
            task,
            priority

        FROM tasks

        WHERE status='offen'

        ORDER BY id ASC
        """
    )


    daten = cursor.fetchall()


    conn.close()


    return daten



init_tasks()