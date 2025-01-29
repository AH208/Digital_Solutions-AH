import random
# 'random' generates a random number between 1 and 100
# Too high or too low will be printed depending on the user's input
# When the user guesses the correct number, "You win!" will be printed
# Could improve with attempts
number = random.randint(1, 100)
guess = 0
while guess != number:
    guess = int(input("Enter a number between 1 and 100: "))
    if guess > number:
        print("Too high!")
    elif guess < number:
        print("Too low!")
print("You win!")