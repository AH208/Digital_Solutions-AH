from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)  # Create a Flask app

#   Create global variable to store game data
total_guesses = 0   # Initialize the total number of guesses
games_played = 0    # Initialize the number of games played
target_number = random.randint(1, 100)  # Generate a random number between 1 and 100
guesses = 0  # Initialize the number of guesses

#Define the default route for the web application
@app.route('/', methods=["GET", "POST"])
def home():
    global target_number, guesses, total_guesses, games_played  # Access global variables

    user_guess = int(request.form.get('guess', 0))
    guesses += 1

    if user_guess == target_number:
        total_guesses += guesses
        games_played += 1
        average_guesses = total_guesses / games_played
        message = f"Congratulations! You guessed the correct number in {guesses} attempts!" \
                  f" Your average number of guesses is {average_guesses:.2f}"
        guesses = 0
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

    #  ISSUES: Attempts does not reset, page starts with "Too low! Try again!" showing. Game over!
