import sqlite3
from datetime import datetime

class Auth:
    def __init__(self):
        self.conn = sqlite3.connect('gerenciamento.db')
        self.cursor = self.conn.cursor()
        self.create_table()


    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        
    def login(self, username, password):
        self.cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, password))
        user = self.cursor.fetchone()
        if user:
            self.log_login(username)
            return user[0]
        else:
            return None
    
    def register(self, username, password):
        try:
            self.cursor.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def log_login(self, username):
        with open('log.txt', 'a') as f:
            f.write(f'{datetime.now()} - {username} logado\n')

    def __del__(self):
        self.conn.close()
