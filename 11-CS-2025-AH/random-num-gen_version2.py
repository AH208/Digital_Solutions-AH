import random
import json

#   LisT
guesses = []

#   loop de loop x1000
for i in range(1000):
    number = random.randint(1, 100)  # Target Number
    #  Variables
    guess = 0
    attempt = 0
    min_guess = 1
    max_guess = 100

#   while loop running until the target number is found (!=number)
    while guess != number:
        guess = (min_guess + max_guess) // 2  # Mathematical Midpoint
        attempt += 1  # Attempt counter

        #  If the guess is too high or too low, the min_guess and max_guess are updated
        if guess > number:
            # print("Too high!")
            max_guess = guess - 1
        elif guess < number:
            # print("Too low!")
            min_guess = guess + 1

#   Dictionary to store the number and the attempts after the loop ends
    guesses.append({"number": number, "attempts": attempt})

def get_attempts(x):
    return x["attempts"]

#  finding Fastest and Slowest game in dictionary using python functions
fastest = min(guesses, key=get_attempts)
slowest = max(guesses, key=get_attempts)
#   return function used instead of lambda
#   average_attempts using divide function, for statement and dictionary
total_attempts = sum(get_attempts(a) for a in guesses)
average_attempts = total_attempts / len(guesses)

# Printing the results to user
print("Fastest game: Number", fastest['number'], "with", fastest['attempts'], "attempts")
print("Slowest game: Number", slowest['number'], "with", slowest['attempts'], "attempts")
print("Average number of attempts:", average_attempts)

# Writing the results to .txt file (It overwrites)
guesses.sort(key=get_attempts)
with open("num__gen_data.txt", "w") as file:
    json.dump(guesses, file, indent=4)
#   with open("num__gen_data.txt", "w") as file:
#        file.write(str(guesses))
