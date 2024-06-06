import sqlite3

class TaskManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.conn = sqlite3.connect('gerenciamento.db')
        self.cursor = self.conn.cursor()
    
    def add_task(self, titulo, descricao):
        self.cursor.execute('INSERT INTO tarefas (user_id, titulo, descricao) VALUES (?, ?, ?)', (self.user_id, titulo, descricao))
        self.conn.commit()
    
    def get_tasks(self):
        self.cursor.execute('SELECT * FROM tarefas WHERE user_id = ?', (self.user_id,))
        return self.cursor.fetchall()
    
    def update_task(self, task_id, titulo, descricao):
        self.cursor.execute('UPDATE tarefas SET titulo = ?, descricao = ? WHERE id = ?', (titulo, descricao, task_id))
        self.conn.commit()
    
    def delete_task(self, task_id):
        self.cursor.execute('DELETE FROM tarefas WHERE id = ?', (task_id,))
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()
