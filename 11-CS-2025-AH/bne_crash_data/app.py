from flask import Flask, render_template, g
#import os
import sqlite3
import folium
from folium.plugins import HeatMap, MarkerCluster
from werkzeug.security import generate_password_hash, check_password_hash

#NEED LOGIN/REGISTER ASAP

app = Flask(__name__)
CRASH_DB = 'crashes.db'
AUTH_DB = 'auth.db'

#app.secret_key = this is not a secret

def get_crash_db():
    db = getattr(g, 'crash_db', None)
    if db is None:
        db = g._database = sqlite3.connect(CRASH_DB)
        db.row_factory = sqlite3.Row
    return db

def get_auth_db():
    db = getattr(g, 'auth_db', None)
    if db is None:
        db = g._database = sqlite3.connect(AUTH_DB)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connections(exception):
    for attr in ('crash_db', 'auth_db'):
        db = getattr(g, attr, None)
        if db is not None:
            db.close()

def init_auth_db():
    conn = sqlite3.connect('AUTH_DB')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
        ''')
    conn.commit()
    conn.close()

#@app.before_first_request
#def _setup():
#    init_auth_db()


@app.route('/')
def index():
    return render_template("index.html")
#    , user=session.get('user'))

    @app.route('/register', methods=['POST'])
    def register():
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('num_database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def login_post():
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('crashing.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user'] = user[1]
            print(user)
            return redirect(url_for('welcome'))
        return 'login Failed'


@app.route('/heatmap')
def heatmap():
    db = get_crash_db()
    cur = db.execute("""
        SELECT Crash_Latitude, Crash_Longitude, Crash_Severity, Crash_Nature, Crash_Type
        FROM crashes
        WHERE Crash_Year = 2024
        AND Crash_Latitude IS NOT NULL
        AND Crash_Longitude IS NOT NULL
    """)
    rows = cur.fetchall()

    # Heatmap data
    heat_data = [(row["Crash_Latitude"], row["Crash_Longitude"]) for row in rows]
    HeatMap(heat_data, radius=8, blur=6, max_zoom=13)



    # folium tutorial time
    cluster = MarkerCluster()
    for row in rows:
        severity = str(row["Crash_Severity"]).lower()
        if "fatal" in severity or "hospitalisation" in severity:
            color = "red"
        else:
            color = "green"
        folium.CircleMarker(
            location=[row["Crash_Latitude"], row["Crash_Longitude"]],
            radius=3,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{row['Crash_Severity']}<br>{row['Crash_Nature']} - {row['Crash_Type']}"
        ).add_to(cluster)


    return render_template("map.html")


if __name__ == '__main__':
    app.run(debug=True)
