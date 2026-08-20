import psycopg2
import random

# =============================
# This is from GeeksforGeeks
# =============================

# connection establishment
conn = psycopg2.connect(
   database="players_testing",
    user='postgres',
    password='password',
    host='localhost',
    port= '5432'
)

conn.autocommit = True


def create_new_player(username="Cornball", color="white"):

    # Creating a cursor object
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
            connection.rollback()
            continue


def update_username(uid, username):
    cursor = conn.cursor()
    update_username = "UPDATE players SET username = %s WHERE uid = %s;"
    cursor.execute(update_username, (username, uid))
    conn.close()

def update_color(uid, color):
    cursor = conn.cursor()
    update_color = "UPDATE players SET color = %s WHERE uid = %s;"
    cursor.execute(update_color, (color, uid))
    conn.close()

def update_elo(uid, elo):
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
