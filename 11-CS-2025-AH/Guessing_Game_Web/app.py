from flask import Flask, render_template, request, redirect, url_for, session
import random
#   from dotenv import load_dotenv


app = Flask(__name__)  # Create a Flask app

#   Create global variable to store game data
total_guesses = 0   # Initialize the total number of guesses
games_played = 0    # Initialize the number of games played
target_number = random.randint(1, 100)  # Generate a random number between 1 and 100
guesses = 0  # Initialize the number of guesses

#   Create a connection to the SQLite3 database
def init_db():  # a function to initialise the database and create the users table if it doesn't exist
    conn = sqlite3.connect('num_database.db')  # connects to the database named basic_flask.db
    cursor = conn.cursor()  # creates a cursor object to interact with the database using SQL commands
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        age INTEGER NOT NULL
    )
        ''')
    conn.commit()  # commits the changes to the database
    conn.close()  # closes the connection to the database to free up resources/memory

#Define the default route for the web application
@app.route('/', methods=["GET", "POST"])
def home():
    global target_number, guesses, total_guesses, games_played  # Access global variables
    if 'user' in session:
        user = session['user']
        age = session['age']
        return render_template('welcome.html', user=user, age=age)
    return redirect(url_for('login'))

    @app.route('/register', methods=['POST'])
    def register():
        username = request.form['username']  # gets the username from the form
        password = request.form['password']  # gets the passsword from the form
        conn = sqlite3.connect('num_database.db')  # connects to the database
        cursor = conn.cursor()  # creates a cursor objects to interact with the database
        # inserts the user details in the users table
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()  # commits the changes to the database
        conn.close()  # closes the connection to the database
        return redirect(url_for('login'))  # redirects the user to the login page

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def login_post():
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('basic_flask.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        #   ? is a placeholder for the values that will be passed in the execute() function
        #   (username, password) are the values that will be passed in the execute() function
        #   This is a parameterised query to prevent SQL injection attacks
        user = cursor.fetchone()
        conn.close()
        #   cursor.fetchone fetches the first row of the result
        if user:
            session['user'] = user[1]
            print(user)
            return redirect(url_for('welcome'))
        return 'login Failed'

    user_guess = int(request.form.get('guess', 0))

    if user_guess < 1 or user_guess > 100:
        message = "Invalid guess! Please enter a number between 1 and 100."
    else:
        guesses += 1

    if user_guess == target_number:
        total_guesses += guesses
        games_played += 1
        average_guesses = total_guesses / games_played
        message = f"Congratulations! You guessed the correct number in {guesses} attempts!" \
                  f" Your average number of guesses is {average_guesses:.2f}"
        guesses = 0 #   reset number
        target_number = random.randint(1, 100)
        return render_template('index.html', message=message, game_over=True)


    else:
        if user_guess < target_number:
            message = "Too low! Try again!"
        else:
            message = "Too high! Try again!"
        return render_template('index.html', message=message, user_guess=user_guess)
    return render_template('index.html')

#    if request.method == 'POST':
#        guess = int(request.form['guess'])

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode

    #   Add history
    #  ISSUES: Attempts counter does +1 when reset, User can guess negative numbers
