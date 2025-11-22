from backend.db import connect_db, create_db, add_player, player_exists, get_player, change_balance, clear_players, clear_history, add_history
import os
import sqlite3
import pytest


create_db()

def test_clear_players():
    add_player("Maelle")
    clear_players()
    res = get_player("Maelle")

    assert res["exist"] == False

def test_db_exists():
    assert os.path.exists("casino.db")

    clear_players()

def test_connect_db():
    con, cur = connect_db()

    assert isinstance(con, sqlite3.Connection)
    assert isinstance(cur, sqlite3.Cursor)

    clear_players()

def test_add_player():
    add_player("Maks", 1500)
    con, cur = connect_db()

    cur.execute("SELECT username, balance FROM player WHERE username = ?", ("Maks",))
    res = cur.fetchone()
    username, balance = res

    assert balance == 1500
    assert username == "Maks"

    cur.execute("DELETE FROM player")
    con.commit()
    con.close()

def test_add_player_exists():
    add_player("Maks", 1500)
    res = add_player("Maks", 1500)

    assert res == False

    clear_players()

def test_player_exists():
    add_player("Maks", 1500)

    assert player_exists("Maks")
    assert player_exists("Max") == False

    clear_players()

def test_get_player():
    add_player("Maks", 1500)
    res1 = get_player("Max")
    res2 = get_player("Maks")

    assert res1 == {"exist": False}
    assert res2["username"] == "Maks"
    assert res2["exist"] == True
    assert res2["balance"] == 1500

    clear_players()

def test_change_balance():
    cases = [
        ("Gustav", 2000, -6000, False, 2000),
        ("Verso", 2000, 2000, True, 4000),
        ("Lune", 2000, -100, True, 1900)
    ]

    res = change_balance("Oskar", 500)

    assert res["success"] == False
    assert res["balance"] == 0

    for username, balance, amount, expected_success, expected_balance in cases:
        add_player(username, balance)
        res = change_balance(username, amount)
        assert res["success"] == expected_success
        assert res["balance"] == expected_balance

    clear_players()

def test_clear_history():
    clear_history()
    add_history("Maks", "spin", 100, 0, 900)
    clear_history()

    con, cur = connect_db()
    cur.execute("SELECT * from history")
    rows = cur.fetchall()
    con.close()

    assert not rows

def test_add_history_loss():
    clear_history()
    add_history("Maks", "spin", 100, 0, 900)

    con, cur = connect_db()
    cur.execute("SELECT * from history WHERE username = ?", ("Maks",))
    res = cur.fetchone()
    id, username, game, bet, result_amount, final_balance, timestamp = res
    con.close()

    assert id == 1
    assert username == "Maks"
    assert game == "spin"
    assert bet == 100
    assert result_amount == 0
    assert final_balance == 900

def test_add_history_win():
    clear_history()
    add_history("Maks", "spin", 100, 200, 1100)

    con, cur = connect_db()
    cur.execute("SELECT * FROM history WHERE username = ?", ("Maks",))
    res = cur.fetchone()
    id, username, game, bet, result_amount, final_balance, timestamp = res
    con.close()

    assert id == 1
    assert username == "Maks"
    assert game == "spin"
    assert bet == 100
    assert result_amount == 200
    assert final_balance == 1100