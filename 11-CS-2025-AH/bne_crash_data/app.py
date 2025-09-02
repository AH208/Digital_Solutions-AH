from flask import Flask, render_template, g, request, redirect, url_for, session
import sqlite3
import folium
from folium.plugins import MarkerCluster
from werkzeug.security import generate_password_hash, check_password_hash

#NEED LOGIN/REGISTER ASAP

app = Flask(__name__)
CRASH_DB = 'crashes.db'
AUTH_DB = 'auth.db'

app.secret_key = "framework13pro"

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
def home():
    if 'user' in session:
        user = session['user']
        # safe suburbs
        db = get_crash_db()
        cur = db.execute("""
            SELECT Loc_Suburb, COUNT(*) as crash_count
            FROM crashes 
            WHERE Crash_Year = 2024
            AND Loc_Suburb IS NOT NULL
            GROUP BY Loc_Suburb
            HAVING crash_count <= 5
            ORDER BY crash_count ASC
            LIMIT 10
        """)
        safe_suburbs = cur.fetchall()
        return render_template('index.html', user=user, safe_suburbs=safe_suburbs)
    return redirect(url_for('login'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    conn = get_auth_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    conn.commit()
#user = cursor.fetchone()
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    conn = get_auth_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    if user:
        session['user'] = user[1]
        print(user)
        return redirect(url_for('home'))
    return 'login Failed'

@app.route('/signout')
def signout():
    session.pop('user', None)
    return redirect(url_for('login'))

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

    # folium tutorial time
    leaflet = folium.Map()
    cluster = MarkerCluster().add_to(leaflet)
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

    return render_template("map.html", map=leaflet.get_root()._repr_html_())


@app.route('/lookup', methods=['GET', 'POST'])
def search():
    suburbs = []
    crashes = []
    if request.method == 'GET':
        # Get unique suburbs for dropdown
        db = get_crash_db()
        cur = db.execute("SELECT DISTINCT Loc_Suburb FROM crashes ORDER BY Loc_Suburb")
        suburbs = [row['Loc_Suburb'] for row in cur.fetchall()]

    if request.method == 'POST':
        suburb = request.form.get('suburb')
        db = get_crash_db()
        cur = db.execute("""
            SELECT Loc_Suburb, Crash_Nature, Crash_Type, Crash_Severity, Crash_Year
            FROM crashes
            WHERE Loc_Suburb = ?
            ORDER BY Crash_Year DESC
            LIMIT 100
        """, [suburb])
        crashes = cur.fetchall()

    return render_template('lookup.html', suburbs=suburbs, crashes=crashes)

if __name__ == '__main__':
    app.run(debug=True)
