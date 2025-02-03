import random
import sqlite3
import os

# History of guesses will be stored in a database and initialised
# 'random' generates a random number between 1 and 100
# Too high or too low will be printed depending on the user's input
# User enters number to guess the random number
# Attempts will be counted with f-strings {attempts +1} and will be printed
# More than and Less than will decide if number is too high or too low and print that
# ValueError will be printed if the user enters a non-integer and I believe the program...
# will not to run if that is not there
# continue, skips the rest of the loop if the input is out of range
# If the user inputs a number less than 1 or more than 100...
# The user will be prompted to enter a number within the range
# When the user guesses the correct number, "You win!" will be printed
# The user will be prompted to run the program again


# repeat likes to break on me
repeat = "yes"
while repeat == "yes":
    conn = sqlite3.connect('num_gen_database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create a table to store the guesses
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS guesses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attempt INTEGER,
        guess INTEGER,
        FOREIGN KEY (game_id) REFERENCES games (game_id)
    )
    ''')

    print("Welcome!")

    number = random.randint(1, 100)
    guess = 0
    attempt = 0

    while guess != number:
        try:
            guess = int(input(f"Attempt {attempt +1}: Enter a number between 1 and 100: "))
            if guess < 1 or guess > 100:
                print("Please enter a number within the range!")
                continue
            attempt += 1

            cursor.execute('INSERT INTO guesses (attempt, guess) VALUES (?, ?)', (attempt, guess))
            conn.commit()

            if guess > number:
                print("Too high!")
            elif guess < number:
                print("Too low!")
        except ValueError:
            print("Please enter a valid number!")

    print(f"You a winner! You guessed in {attempt} attempts!")

    repeat = input("would you like to run the program again (Yes/No): ").lower().strip()
    os.system('cls')
conn.close()
print("Exiting the program.")
