from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize SQLite database
def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
            '''
        )
        conn.commit()

# Initialize a counter
form_count = 0

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    return render_template('donate.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data['name']
    email = data['email']

    # Save form data to database
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            (name, email)
        )
        conn.commit()

    global form_count
    form_count += 1  # Increment form count

    response = {
        'message': 'Form submitted successfully!',
        'form_count': form_count
    }
    return jsonify(response)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
