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


def create_new_player(username="cornball", color="white"):
    # Creating a cursor object
    cursor = conn.cursor()

    uid = random.randint(1000, 9999)
    # %s does not mean 'string' it is a substitude
    add_player = "INSERT INTO players (uid, username, color, elo) VALUES (%s, %s, %s, %s);"

    # executing the sql
    cursor.execute(add_player, (uid, username, color, 500))

    # Closing the connection
    conn.close()

def change_username(uid, username):
    cursor = conn.cursor()
    change_username = "UPDATE players SET username = %s WHERE uid = %s;"
    cursor.execute(change_username, (username, uid))
    conn.close()

def change_color(uid, color):
    cursor = conn.cursor()
    change_username = "UPDATE players SET color = %s WHERE uid = %s;"
    cursor.execute(change_username, (color, uid))
    conn.close()

change_color(8662, "green")

def delete_player(uid):

    cursor = conn.cursor()
    delete_player = "DELETE FROM players WHERE uid = %s;"

    # where uid has to be a tuple
    cursor.execute(delete_player, (uid,))

    conn.close()

