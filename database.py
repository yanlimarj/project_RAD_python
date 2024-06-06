import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('gerenciamento.db')
        self.cursor = self.conn.cursor()
        self.init_db()
    
    def init_db(self):
        # Tabela de usuários
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        ''')
        
        # Tabela de tarefas
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT DEFAULT 'Pendente',
            FOREIGN KEY(user_id) REFERENCES usuarios(id)
        )
        ''')
        
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()

