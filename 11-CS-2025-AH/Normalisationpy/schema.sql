
app = flask(__Name__)

def init_db():
    if not os.path.excists('my_database.db'):
        create_db()
    print("Database initialized successfully.")

def create_db():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    with open ('schema.sql', 'r') as file:
        schema_sql = file.read()

    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()