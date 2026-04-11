from flask import Flask, render_template_string, request, redirect
import sqlite3
import os
import socket
from datetime import datetime

app = Flask(__name__)
DB_FILE = '/data/todos.db'

# HTML шаблон (прямо в коде для простоты)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DevOps ToDo</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 700px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin: 0 0 20px 0;
            font-size: 2.5em;
        }}
        .server-info {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            font-size: 14px;
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            border: 1px solid #e9ecef;
        }}
        .server-info span {{
            color: #667eea;
            font-weight: bold;
        }}
        form {{
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }}
        input[type="text"] {{
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }}
        input[type="text"]:focus {{
            outline: none;
            border-color: #667eea;
        }}
        button {{
            padding: 15px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: background 0.3s;
        }}
        button:hover {{
            background: #5a67d8;
        }}
        .todo-list {{
            list-style: none;
            padding: 0;
        }}
        .todo-item {{
            display: flex;
            align-items: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            margin-bottom: 10px;
            border: 1px solid #e9ecef;
            transition: transform 0.2s;
        }}
        .todo-item:hover {{
            transform: translateX(5px);
        }}
        .todo-item.completed {{
            background: #e8f5e9;
            border-color: #c8e6c9;
        }}
        .todo-item.completed .task-text {{
            text-decoration: line-through;
            color: #4caf50;
        }}
        .task-text {{
            flex: 1;
            font-size: 16px;
            color: #333;
        }}
        .todo-actions {{
            display: flex;
            gap: 5px;
        }}
        .btn-complete, .btn-delete {{
            padding: 8px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }}
        .btn-complete {{
            background: #4caf50;
            color: white;
        }}
        .btn-complete:hover {{
            background: #43a047;
        }}
        .btn-delete {{
            background: #f44336;
            color: white;
        }}
        .btn-delete:hover {{
            background: #e53935;
        }}
        .empty-state {{
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 18px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 DevOps ToDo</h1>
        <div class="server-info">
            <span>🖥️ Сервер:</span> {{ hostname }} | 
            <span>⏰ Время:</span> {{ timestamp }} | 
            <span>🐳 Контейнер:</span> {{ container_id }}
        </div>
        
        <form method="POST" action="/add">
            <input type="text" name="task" placeholder="Введите новую задачу..." required>
            <button type="submit">➕ Добавить</button>
        </form>
        
        {% if todos %}
            <ul class="todo-list">
            {% for todo in todos %}
                <li class="todo-item {% if todo[2] == 1 %}completed{% endif %}">
                    <span class="task-text">{{ todo[1] }}</span>
                    <div class="todo-actions">
                        {% if todo[2] == 0 %}
                        <a href="/complete/{{ todo[0] }}"><button class="btn-complete">✓</button></a>
                        {% endif %}
                        <a href="/delete/{{ todo[0] }}"><button class="btn-delete">✗</button></a>
                    </div>
                </li>
            {% endfor %}
            </ul>
        {% else %}
            <div class="empty-state">
                ✨ Пока нет задач. Создай первую!
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS todos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  task TEXT NOT NULL,
                  completed INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Главная страница"""
    # Получаем список задач
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, task, completed FROM todos ORDER BY id DESC')
    todos = c.fetchall()
    conn.close()
    
    # Информация о сервере
    hostname = socket.gethostname()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    container_id_full = open('/etc/hostname', 'r').read().strip() if os.path.exists('/etc/hostname') else 'unknown'
    container_id = container_id_full[:12]  # Обрезаем до 12 символов
    
    return render_template_string(
        HTML_TEMPLATE,
        todos=todos,
        hostname=hostname,
        timestamp=timestamp,
        container_id=container_id
    )

@app.route('/add', methods=['POST'])
def add():
    """Добавление новой задачи"""
    task = request.form.get('task', '').strip()
    if task:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT INTO todos (task) VALUES (?)', (task,))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/complete/<int:todo_id>')
def complete(todo_id):
    """Отметить задачу как выполненную"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE todos SET completed = 1 WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    """Удалить задачу"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    # Создаем директорию для БД если её нет
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
