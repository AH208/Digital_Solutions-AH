import random

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
        guess = random.randint(min_guess, max_guess)  # Computed Random Guess between min and max (0 and 100)
        attempt += 1  # Attempt counter

        #  If the guess is too high or too low, the min_guess and max_guess are updated
        if guess > number:
            # print("Too high!")
            max_guess = guess
        elif guess < number:
            # print("Too low!")
            min_guess = guess

#   Dictionary to store the number and the attempts after the loop ends
    guesses.append({"number": number, "attempts": attempt})

#  finding Fastest and Slowest game in dictionary using python functions (and x = dictionary)
fastest = min(guesses, key=lambda x: x["attempts"])
slowest = max(guesses, key=lambda x: x["attempts"])
#   lambda returns a function that takes x as an argument and returns the key being attempts in this case

# Printing the results to user
print("Fastest game: Number", fastest['number'], "with", fastest['attempts'], "attempts")
print("Slowest game: Number", slowest['number'], "with", slowest['attempts'], "attempts")

# Writing the results to .txt file
with open("num__gen_data.txt", "w") as file:
    file.write(str(guesses))
