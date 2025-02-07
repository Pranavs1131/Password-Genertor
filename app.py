from flask import Flask, render_template, request, redirect, url_for
import random
import sqlite3
import os

app = Flask(__name__)

db_dir = 'C:/Users/PRANAV SINGH/Desktop/project_08-Nov-23'
# Define the path to your SQLite database
db_file = os.path.join(app.root_path, 'project.db')

# Function to create an SQLite database and table if they don't exist
def create_database():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("SQLite error:", e)

# Function to insert a single password into the database
def insert_password(password):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO passwords (password) VALUES (?)', (password,))
    conn.commit()
    conn.close()

# Function to generate a random password
def generate_random_password(length):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-=[]{}|;:,.<>?'
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_password', methods=['POST'])
def generate_password():
    password_length = int(request.form['password_length'])
    num_combinations = int(request.form['num_combinations'])

    create_database()

    generated_passwords = []
    for _ in range(num_combinations):
        password = generate_random_password(password_length)
        insert_password(password)
        generated_passwords.append(password)

    return render_template('results.html', generated_passwords=generated_passwords)

@app.route('/saved_passwords')
def saved_passwords():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM passwords')
    passwords = cursor.fetchall()
    conn.close()

    password_list = [password[0] for password in passwords]

    return render_template('saved_passwords.html', passwords=password_list)

if __name__ == "__main__":
    app.run(debug=True)
