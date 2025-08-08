from flask import render_template, render_template_string, Flask, g
import sqlite3
import pandas as pd


app = Flask(__name__)
DATABASE = 'shinhackers.db'

# Things to do:
# A. Details of all games played in April.
# B. The names of teams that we have defeated.
# C. Details of all games
# D. The date of the game and the name of the opposition team for all games played in May that resulted in a draw.
# E. The scores of games against the Bellyfloppers or the Kneeknockers.
# F. The number of games we have won.
# G. Our biggest winning margin.
# H. Details (*) of all games in the order

#AND

# A. How many games have we played so far, and what are the total points scored by us and against us?
# B. What teams have beaten us by 10 points or more?
# C. List details of all matches, in order of points scored by us, with our highest score first.
# D. What were the results in the second half of April?
# E. Name all the teams we have played so far.

def get_db():
   db = getattr(g, '_database', None)
   if db is None:
       db = g.database = sqlite3.connect(DATABASE)
   return db

@app.teardown_appcontext
def close_connection(exception):
   db = getattr(g, '_database', None)
   if db is not None:
       db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/april_games')
def april_games():
    db = get_db()
    cur = db.execute("SELECT * FROM Games WHERE Month = 4")
    april_games = cur.fetchone()[0]
    return (f"Number of games played in april: {april_games}<br>"
    f"<a href='/'>Back to Home</a>")

#Still has brackets, come back to this one
@app.route('/games_won_teams')
def games_won_teams():
    db = get_db()
    cur = db.execute("SELECT Team FROM Games WHERE Ours > Theirs")
    won_games_teams = cur.fetchall()
    return (f"Teams won against: {won_games_teams}<br>"
    f"<a href='/'>Back to Home</a>")


@app.route('/games')
def games():
    db = get_db()
    cur = db.execute("SELECT * FROM Games")
    games = cur.fetchone()[0]
    return (f"Total Number of games played is: {games}<br>"
    f"<a href='/'>Back to Home</a>")

# Joining part - learnt from AI - The joins are: fetchall then numbered put into a list and a result is returned
@app.route('/may_games')
def may_games():
    db = get_db()
    cur = db.execute("SELECT Day, Month, Team FROM Games WHERE Month = 5")
    may_games = cur.fetchall()
    result = "<br>".join([f"Day: {game[0]}, Month: {game[1]}, Team: {game[2]}" for game in may_games])
    return (f"Details for the game played in May: {result}<br>"
    f"<a href='/'>Back to Home</a>")


@app.route('/scores_teams')
def scores_teams():
    db = get_db()
    cur = db.execute("SELECT Team, Ours, Theirs FROM Games WHERE Team IN ('Bellyfloppers', 'Kneeknockers')")
    scores = cur.fetchall()
    result = "<br>".join([f"{game[0]}: Us {game[1]} - Them {game[2]}" for game in scores])
    return (f"Scores against Bellyfloppers and Kneeknockers:<br>{result}<br>"
            f"<a href='/'>Back to Home</a>")

@app.route('/games_won')
def games_won():
    db = get_db()
    cur = db.execute("SELECT COUNT(*) FROM Games WHERE Ours > Theirs")
    won_games = cur.fetchone()[0]
    return (f"Number of games we won: {won_games}<br>"
    f"<a href='/'>Back to Home</a>")

@app.route('/max_winning_margin')
def max_winning_margin():
    db = get_db()
    cur = db.execute("SELECT max(Ours-Theirs) FROM Games")
    max_margin = cur.fetchone()[0]
    return (f"Our biggest winning margin: {max_margin}<br>"
    f"<a href='/'>Back to Home</a>")

@app.route('/ordered_games')
def ordered_games():
    db = get_db()
    cur = db.execute("SELECT * FROM Games ORDER BY Month, Day")
    ordered_games = cur.fetchall()
    result = "<br>".join([f"Day: {game[0]}, Month: {game[1]}, Team: {game[2]}, Ours: {game[3]}, Theirs: {game[4]}" for game in ordered_games])
    return (f"Details of all games in order:<br>{result}<br>"
            f"<a href='/'>Back to Home</a>")

@app.route('/ordered_games_table')
def ordered_games_table():
    db = get_db()
    cur = db.execute("SELECT * FROM Games ORDER BY Month, Day")
    ordered_games_table = cur.fetchall()

    # Create a DataFrame from the fetched data
    columns = ["Day", "Month", "Team", "Ours", "Theirs"]
    df = pd.DataFrame(ordered_games_table, columns=columns)

    # Convert the DataFrame to an HTML table
    table_html = df.to_html(index=False)

    # Render the HTML template with the table
    return render_template_string('''
        <!doctype html>
        <html>
        <head>
            <title>Ordered Games</title>
        </head>
        <body>
            <h1>Details of all games in order:</h1>
            {{ table_html|safe }}
            <br>
            <a href='/'>Back to Home</a>
        </body>
        </html>
    ''', table_html=table_html)

#Part 2
#AI also showed me this way, which is better to understand than the joining f string way...
@app.route('/total_games_points')
def total_games_points():
    db = get_db()
    cur = db.execute("SELECT COUNT(*), SUM(Ours), SUM(Theirs) FROM Games")
    total_games, total_ours, total_theirs = cur.fetchone()
    return (f"Total games played: {total_games}<br>"
            f"Total points scored by us: {total_ours}<br>"
            f"Total points scored against us: {total_theirs}<br>"
            f"<a href='/'>Back to Home</a>")

@app.route('/teams_beaten_by_10')
def teams_beaten_by_10():
    db = get_db()
    cur = db.execute("SELECT Team FROM Games WHERE Theirs - Ours >= 10")
    teams = cur.fetchall()
    teams_list = [team[0] for team in teams]
    return (f"Teams that have beaten us by 10 points or more: {', '.join(teams_list)}<br>"
            f"<a href='/'>Back to Home</a>")

@app.route('/games_ordered_score')
def games_ordered_score():
    db = get_db()
    cur = db.execute("SELECT * FROM Games ORDER BY Ours")
    ordered_games = cur.fetchall()
    result = "<br>".join([f"Day: {game[0]}, Month: {game[1]}, Team: {game[2]}, Ours: {game[3]}, Theirs: {game[4]}" for game in ordered_games])
    return (f"Details of all games ordered by our score:<br>{result}<br>"
            f"<a href='/'>Back to Home</a>")

@app.route('/games_ordered_score_table')
def games_ordered_score_table():
    db = get_db()
    cur = db.execute("SELECT * FROM Games ORDER BY Ours DESC")
    games = cur.fetchall()

    # Create a DataFrame from the fetched data
    columns = ["Day", "Month", "Team", "Ours", "Theirs"]
    df = pd.DataFrame(games, columns=columns)

    # Convert the DataFrame to an HTML table
    table_html = df.to_html(index=False)

    # Render the HTML template with the table
    return render_template_string('''
        <!doctype html>
        <html>
        <head>
            <title>Games Ordered by Score</title>
        </head>
        <body>
            <h1>Games ordered by our score:</h1>
            {{ table_html|safe }}
            <br>
            <a href='/'>Back to Home</a>
        </body>
        </html>
    ''', table_html=table_html)

@app.route('/april_second_half')
def april_second_half():
    db = get_db()
    cur = db.execute("SELECT * FROM Games WHERE Month = 4 AND Day > 15")
    ordered_games_text = cur.fetchall()
    result = "<br>".join([f"Day: {game[0]}, Month: {game[1]}, Team: {game[2]}, Ours: {game[3]}, Theirs: {game[4]}" for game in ordered_games_text])
    return (f"Details of all games in the second half of April:<br>{result}<br>"
            f"<a href='/'>Back to Home</a>")

@app.route('/april_second_half_table')
def april_second_half_table():
    db = get_db()
    cur = db.execute("SELECT * FROM Games WHERE Month = 4 AND Day > 15")
    results = cur.fetchall()

    # Create a DataFrame from the fetched data
    columns = ["Day", "Month", "Team", "Ours", "Theirs"]
    df = pd.DataFrame(results, columns=columns)

    # Convert the DataFrame to an HTML table
    table_html = df.to_html(index=False)

    # Render the HTML template with the table
    return render_template_string('''
        <!doctype html>
        <html>
        <head>
            <title>April Second Half Results</title>
        </head>
        <body>
            <h1>Results in the second half of April:</h1>
            {{ table_html|safe }}
            <br>
            <a href='/'>Back to Home</a>
        </body>
        </html>
    ''', table_html=table_html)

@app.route('/teams_played')
def teams_played():
    db = get_db()
    cur = db.execute("SELECT DISTINCT Team FROM Games")
    teams = cur.fetchall()
    teams_list = [team[0] for team in teams]
    return (f"Teams we have played so far: {', '.join(teams_list)}<br>"
            f"<a href='/'>Back to Home</a>")



if __name__ == '__main__':
    app.run(debug=True)