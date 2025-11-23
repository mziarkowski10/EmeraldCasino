import sqlite3


def connect_db():
    con = sqlite3.connect("backend/data/casino.db")
    cur = con.cursor()

    return con, cur

def create_db():
    con, cur = connect_db()

    cur.execute('''CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY,
        player_id INTEGER NOT NULL,
        game TEXT NOT NULL,
        bet REAL NOT NULL,
        result_amount REAL NOT NULL,
        final_balance REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

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
        return {
            "success": False,
            "message": "Player already exists"
        }

    cur.execute("INSERT INTO player(username, balance) VALUES(?, ?)", (username, balance))
    con.commit()
    player_id = get_player(username)["player_id"]
    con.close()

    return {
        "success": True,
        "message": "Player created successfully",
        "player_id": player_id
    }

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
        return None
    
    cur.execute("SELECT * FROM player WHERE username = ?", (username,))
    res = cur.fetchone()
    id, username, balance, created_at = res

    con.close()

    return {
        "player_id": id,
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

def player_exists_by_id(player_id):
    con, cur = connect_db()
    cur.execute("SELECT id FROM player")
    res = cur.fetchall()

    for id in res:
        if id[0] == player_id:
            return True

    return False

def get_player_by_id(player_id):
    con, cur = connect_db()

    if not player_exists_by_id(player_id):
        return None

    cur.execute("SELECT * from player WHERE id = ?", (player_id,))
    res = cur.fetchone()
    id, username, balance, created_at = res

    con.close()

    return {
        "player_id": id,
        "username": username,
        "balance": balance,
        "created_at": created_at
    }

def clear_players():
    con, cur = connect_db()
    cur.execute("DELETE FROM player")
    con.commit()
    con.close()

def add_history(player_id, game, bet, result_amount, final_balance):    
    if not isinstance(player_id, int):
        return {
            "success": False,
            "message": "player_id must be integer"
        }

    if not isinstance(game, str) or not game:
        return {
            "success": False,
            "message": "game must be non-empty string"
        }

    if not isinstance(bet, float) or bet < 0:
        return {
            "success": False,
            "message": "bet must be non-negative"
        }
    
    if not isinstance(result_amount, float):
        return {
            "success": False,
            "message": "result_amount must be number"
        }

    if not isinstance(final_balance, float) or final_balance < 0:
        return {
            "success": False,
            "message": "final_balance must be non-negative"
        }

    if not player_exists_by_id(player_id):
        return {
            "success": False,
            "message": "Player not found"
        }

    con, cur = connect_db()
    cur.execute("INSERT INTO history(player_id, game, bet, result_amount, final_balance) VALUES(?, ?, ?, ?, ?)", (player_id, game, bet, result_amount, final_balance))
    con.commit()
    con.close()

    return {
        "success": True,
        "message": "History added successfully"
    }

def get_history(player_id):
    con, cur = connect_db()

    if not player_exists_by_id(player_id):
        return []

    cur.execute("SELECT * FROM history WHERE player_id = ?", (player_id,))
    res = cur.fetchall()
    con.close()

    if not res:
        return []

    result = []

    for row in res:
        history_id, pid, game, bet, result_amount, final_balance, timestamp = row
        result.append({
            "id": history_id,
            "player_id": pid,
            "game": game,
            "bet": bet,
            "result_amount": result_amount,
            "final_balance": final_balance,
            "timestamp": timestamp
        })

    return result

def clear_history():
    con, cur = connect_db()
    cur.execute("DELETE FROM history")
    con.commit()
    con.close()