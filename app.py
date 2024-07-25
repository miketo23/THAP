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
                email TEXT UNIQUE NOT NULL,
                amount REAL
            )
            '''
        )
        conn.commit()
init_db()

# Initialize a counter
form_count = 0

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donate', methods=['POST'])
def donate():
    global form_count
    if request.method == 'POST':
            data = request.json
            name = data['name']
            email = data['email']
            amount = data['amount']

             # Insert into SQLite database
            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (name, email, amount) VALUES (?, ?, ?)',
                    (name, email, amount)
                )
                conn.commit()

            form_count +=1

            # Process data and respond with JSON
            # Insert into database, etc.

            response = {
                'message': 'Form submitted successfully!',
                'form_count': form_count,
                'success': True
            }

    return jsonify(response)


    return render_template('donate.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/users', methods= ['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, amount, email FROM users' )
    users = cursor.fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

