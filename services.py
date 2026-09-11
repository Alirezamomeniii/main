import sqlite3
from models import Ticket


class Database:

    def __init__(self):
        self.connection = sqlite3.connect("database.db", check_same_thread=False)
        self.create_tables()

    def create_tables(self):

        self.connection.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,username TEXT)""")

        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,
            title TEXT,description TEXT,status TEXT,created_at TEXT)""")

        self.connection.commit()


class UserService:

    def __init__(self, database):
        self.database = database

    def add_user(self, telegram_id, username):

        user = self.database.connection.execute("SELECT * FROM users WHERE telegram_id = ?",(telegram_id,)).fetchone()

        if user is None:

            self.database.connection.execute("INSERT INTO users (telegram_id, username) VALUES (?, ?)",(telegram_id, username))

            self.database.connection.commit()


class TicketService:

    def __init__(self, database):
        self.database = database

    def create_ticket(self, user_id, title, description):

        cursor = self.database.connection.execute("""INSERT INTO tickets(user_id, title, description, status, created_at)
            VALUES (?, ?, ?, ?, datetime('now'))""",(user_id, title, description, "OPEN"))

        self.database.connection.commit()

        return self.get_ticket(cursor.lastrowid)

    def get_user_tickets(self, user_id):

        rows = self.database.connection.execute(
            "SELECT * FROM tickets WHERE user_id = ?",(user_id,)).fetchall()

        tickets = []

        for row in rows:

            tickets.append(Ticket(row[0],row[1],row[2],row[3],row[4],row[5]))

        return tickets

    def get_ticket(self, ticket_id):

        row = self.database.connection.execute("SELECT * FROM tickets WHERE id = ?",(ticket_id,)).fetchone()

        if row is None:
            return None

        return Ticket(row[0],row[1],row[2],row[3],row[4],row[5])