import psycopg2
import random

# =============================
# This is from GeeksforGeeks
# =============================

# connection establishment
def connect_to_database():
    conn = psycopg2.connect(
       database="players_testing",
        user='postgres',
        password='password',
        host='localhost',
        port= '5432'
    )
    
    conn.autocommit = True

    return conn


def create_new_player(username="Cornball", color="white"):

    # Creating a cursor object
    conn = connect_to_database()
    cursor = conn.cursor()
    while True:

        # %s does not mean 'string' it is a substitude
        add_player = "INSERT INTO players (uid, username, color, elo) VALUES (%s, %s, %s, %s);"

        try:
            # Attempt to insert

            uid = random.randint(1000, 9999)
            cursor.execute(add_player, (uid, username, color, 500))
            conn.close()
            return # Success! Break the loop.

        except psycopg2.errors.UniqueViolation:
            # If a duplicate exists, rollback the error and try again
            conn.rollback()
            continue

def get_players():
    conn = connect_to_database()
    cursor = conn.cursor()

    get_players = "SELECT uid, username FROM players;"
    cursor.execute(get_players)
    rows = cursor.fetchall()

    players = [{"uid": row[0], "username": row[1]} for row in rows]

    return players

get_players()


def update_username(uid, username):
    conn = connect_to_database()
    cursor = conn.cursor()
    update_username = "UPDATE players SET username = %s WHERE uid = %s;"
    cursor.execute(update_username, (username, uid))
    conn.close()

def update_color(uid, color):
    conn = connect_to_database()
    cursor = conn.cursor()
    update_color = "UPDATE players SET color = %s WHERE uid = %s;"
    cursor.execute(update_color, (color, uid))
    conn.close()

def update_elo(uid, elo):
    conn = connect_to_database()
    cursor = conn.cursor()
    update_elo = "UPDATE players SET elo = %s WHERE uid = %s;"
    cursor.execute(update_elo, (elo, uid))
    conn.close()


def delete_player(uid):

    cursor = conn.cursor()
    delete_player = "DELETE FROM players WHERE uid = %s;"

    # where uid has to be a tuple
    cursor.execute(delete_player, (uid,))

    conn.close()
create_new_player()
