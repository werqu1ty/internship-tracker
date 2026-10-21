import sqlite3

DB_PATH = "tracker.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_connection()
    with open("schema.sql") as f:
        sql = f.read()
        conn.executescript(sql)
        conn.commit()
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Database ready")
