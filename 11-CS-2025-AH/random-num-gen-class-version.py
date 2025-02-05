#   Random target generation
#   Guessing algorithm
#   Feedback mechanic - number of guesses
#   Data collection - simulate games
#   Data analysis - compute averages
#   Data Presentation - sort and print results
import random
def binary_search_guesss(target)
def simulate_games(num_games):
    """
    Simulate the guessing game for a given number of games.
    Returns a dictionary with target numbers as keys and tuple of total guesses and count of games as values.
    This function simulates the guessing game for a given number of games and keeps track of the total number of guesses
    and count of games for each target number.
    """
results  = {n: (0,0) for n in range(1,101)}
#   Initialize results dictionary with target numbers as keys
print(type(results))

for _ in range(num_games):  #   Use _ as a throwaway variable since we don't need the loop index
    target = random.randint(1,100)  #   Choose a random target number between 1 and 100
    print("Target is: ", target)    #   Print the target number for each game for testing
    num_guesses = binary_search_guess(target)   #   Call the binary_search_guess function to guess the target number
    total, count = results(target)  #   Get the total number of guesses and count of games for the target number
    results[target] = (total + num_guesses, count + 1)  #   Update the results dictionary with the new values
    print(results)  #   Print the results dictionary for testing


def main():
    #   The main function runs the simulation, computes averages, sorts them for easier review and prints the results.
    num_games = 1000
    results = simulate_games(num_games)