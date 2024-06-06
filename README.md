# Sistema de Gerenciamento com Python, SQLite e Tkinter

## Descrição
Este é um sistema simples de gerenciamento de tarefas com funcionalidades de login/cadastro, desenvolvido utilizando Python, banco de dados SQLite e a biblioteca Tkinter para interfaces gráficas.

## Funcionalidades
- Login e Cadastro de usuários
- Adição, visualização, atualização e exclusão de tarefas
- Registro de logins em um arquivo de texto

## Instruções de Uso
1. Clone o repositório.
2. Instale o Python (3.6+).
3. Execute o script `database.py` para configurar o banco de dados:
    ```sh
    python database.py
    ```
4. Execute o script `app.py` para iniciar a aplicação:
    ```sh
    python app.py
    ```
5. Faça login ou cadastre um novo usuário para começar a gerenciar suas tarefas.

## Estrutura do Projeto
- `database.py`: Script para configuração do banco de dados.
- `auth.py`: Classe para login e cadastro de usuários.
- `task_manager.py`: Classe para gerenciamento de tarefas.
- `app.py`: Script principal da aplicação com interface Tkinter.
- `log.txt`: Arquivo de log dos logins.
