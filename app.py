import tkinter as tk
from tkinter import messagebox
from auth import Auth
from task_manager import TaskManager
import os
import datetime
from database import Database

def limpar_log_mensal():
    if os.path.exists('log.txt'):
        modificacao = datetime.datetime.fromtimestamp(os.path.getmtime('log.txt'))
        agora = datetime.datetime.now()
        if (agora - modificacao).days >= 30:
            os.remove('log.txt')
            open('log.txt', 'w').close()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login/Cadastro")
        self.geometry("300x200")
        
        self.auth = Auth()
        
        self.create_login_screen()
    
    def create_login_screen(self):
        self.clear_screen()
        
        tk.Label(self, text="Username").pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        tk.Label(self, text="Password").pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        tk.Button(self, text="Login", command=self.login).pack()
        tk.Button(self, text="Cadastrar", command=self.open_register_window).pack()
    
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        user_id = self.auth.login(username, password)
        
        if user_id:
            self.open_main_window(user_id)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")
    
    def open_register_window(self):
        self.register_window = tk.Toplevel(self)
        self.register_window.title("Cadastrar")
        self.register_window.geometry("300x200")
        
        tk.Label(self.register_window, text="Username").pack()
        self.entry_register_username = tk.Entry(self.register_window)
        self.entry_register_username.pack()

        tk.Label(self.register_window, text="Password").pack()
        self.entry_register_password = tk.Entry(self.register_window, show="*")
        self.entry_register_password.pack()

        tk.Button(self.register_window, text="Cadastrar", command=self.register).pack()
    
    def register(self):
        username = self.entry_register_username.get()
        password = self.entry_register_password.get()
        
        if self.auth.register(username, password):
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso")
            self.register_window.destroy()
        else:
            messagebox.showerror("Erro", "Usuário já existe")
    
    def open_main_window(self, user_id):
        self.main_window = tk.Toplevel(self)
        self.main_window.title("Gerenciador de Tarefas")
        self.main_window.geometry("600x400")
        
        self.task_manager = TaskManager(user_id)
        
        tk.Label(self.main_window, text="Registrar Tarefas", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(self.main_window, text="Título da Tarefa").pack()
        self.entry_titulo = tk.Entry(self.main_window, width=50)
        self.entry_titulo.pack()

        tk.Label(self.main_window, text="Descrição da Tarefa").pack()
        self.entry_descricao = tk.Entry(self.main_window, width=50)
        self.entry_descricao.pack()

        tk.Button(self.main_window, text="Adicionar Tarefa", command=self.add_task).pack(pady=10)
        
        self.frame_tarefas = tk.Frame(self.main_window)
        self.frame_tarefas.pack(pady=10)
        
        self.load_tasks()
    
    def add_task(self):
        titulo = self.entry_titulo.get()
        descricao = self.entry_descricao.get()
        self.task_manager.add_task(titulo, descricao)
        self.entry_titulo.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.load_tasks()
    
    def load_tasks(self):
        for widget in self.frame_tarefas.winfo_children():
            widget.destroy()
        
        tarefas = self.task_manager.get_tasks()
        for tarefa in tarefas:
            frame = tk.Frame(self.frame_tarefas)
            frame.pack(fill="x", pady=5)

            label = tk.Label(frame, text=f"Título: {tarefa[2]}\nDescrição: {tarefa[3]}\nStatus: {tarefa[4]}", justify=tk.LEFT, anchor="w")
            label.pack(side="left", fill="x", expand=True)

            btn_editar = tk.Button(frame, text="Editar", command=lambda t=tarefa: self.edit_task(t))
            btn_editar.pack(side="right")

            btn_excluir = tk.Button(frame, text="Excluir", command=lambda t=tarefa: self.confirm_delete_task(t))
            btn_excluir.pack(side="right")
    
    def edit_task(self, tarefa):
        self.edit_window = tk.Toplevel(self)
        self.edit_window.title("Editar Tarefa")
        self.edit_window.geometry("300x200")
        
        tk.Label(self.edit_window, text="Título da Tarefa").pack()
        self.entry_edit_titulo = tk.Entry(self.edit_window, width=50)
        self.entry_edit_titulo.insert(0, tarefa[2])
        self.entry_edit_titulo.pack()

        tk.Label(self.edit_window, text="Descrição da Tarefa").pack()
        self.entry_edit_descricao = tk.Entry(self.edit_window, width=50)
        self.entry_edit_descricao.insert(0, tarefa[3])
        self.entry_edit_descricao.pack()

        tk.Button(self.edit_window, text="Salvar Alterações", command=lambda: self.save_task(tarefa[0])).pack(pady=10)
    
    def save_task(self, task_id):
        titulo = self.entry_edit_titulo.get()
        descricao = self.entry_edit_descricao.get()
        self.task_manager.update_task(task_id, titulo, descricao)
        self.edit_window.destroy()
        self.load_tasks()
    
    def confirm_delete_task(self, tarefa):
        confirm = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir esta tarefa?")
        if confirm:
            self.delete_task(tarefa)
    
    def delete_task(self, tarefa):
        self.task_manager.delete_task(tarefa[0])
        self.load_tasks()

if __name__ == '__main__':
    try:
        limpar_log_mensal()
        Database()
        app = Application()
        app.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
