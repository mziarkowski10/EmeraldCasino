import sqlite3


def connect_db():
    con = sqlite3.connect("casino.db")
    cur = con.cursor()

    return con, cur

def create_db():
    con, cur = connect_db()

    cur.execute('''CREATE TABLE IF NOT EXISTS player(
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        balance REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )   
    ''')

    con.commit()
    con.close()

def add_player(username, balance=1000):
    con, cur = connect_db()

    if player_exists(username):
        con.close()
        return False

    cur.execute("INSERT INTO player(username, balance) VALUES(?, ?)", (username, balance))
    con.commit()
    con.close()

def player_exists(username):
    con, cur = connect_db()
    res = cur.execute("SELECT username FROM player")
    res = res.fetchall()

    for name in res:
        if name[0] == username:
            con.close()
            return True
    
    con.close()

    return False

def get_player(username):
    con, cur = connect_db()

    if not player_exists(username):
        return {"exist": False}
    
    res = cur.execute("SELECT * FROM player WHERE username = ?", (username,))
    id, username, balance, created_at = res.fetchone()

    con.close()

    return {
        "id": id,
        "username": username,
        "balance": balance,
        "created_at": created_at,
        "exist": True
    }

def change_balance(username, amount):
    con, cur = connect_db()
    res = cur.execute("SELECT balance FROM player WHERE username = ?", (username,))
    res = res.fetchone()

    if res is None:
        return {
            "success": False,
            "balance": 0,
            "message": "Player does not exist"
        }

    balance = res[0]

    total = balance + amount

    if total < 0:
        return {
            "success": False,
            "balance": balance,
            "message": "Not enough balance"
        }

    cur.execute("UPDATE player SET balance = ? WHERE username = ?", (total, username))

    con.commit()
    con.close()

    return {
        "success": True,
        "balance": total,
        "message": "Balance updated successfully"
    }

def clear_players():
    con, cur = connect_db()
    cur.execute("DELETE FROM player")
    con.commit()
    con.close()