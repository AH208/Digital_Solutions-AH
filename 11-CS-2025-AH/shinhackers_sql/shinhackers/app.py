#import necessary libraries
#import sqlite3

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

#@app.route('/attributes')
#def attributes():

if __name__ == '__main__':
    app.run(debug=True)