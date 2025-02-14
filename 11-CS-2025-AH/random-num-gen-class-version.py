#   Random target generation
#   Guessing algorithm
#   Feedback mechanic - number of guesses
#   Data collection - simulate games
#   Data analysis - compute averages
#   Data Presentation - sort and print results
import random
def binary_search_guess(target, low=1, high=100):
    # This function implements a binary search algorithm to guess the target number.
    # It returns the number of guesses it took to find the target number.
    guesses = 0
    while low <= high:
        # make a guess using the midpoint
        guess = (low + high) // 2
        print("Guess is: ", guess) # Print the guess for testing purpose
        guesses += 1

        if guess == target:
            return guesses
        elif guess < target:
            low = guess + 1
        else:
            high = guess - 1
    return guesses

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
        total, count = results[target]  #   Get the total number of guesses and count of games for the target number
        results[target] = (total + num_guesses, count + 1)  #   Update the results dictionary with the new values
        print(results)  #   Print the results dictionary for testing
    return results  #   Return the results dictionary

def compute_averages(results):
    '''  Compute the average number of guesses for each target number.
         Returns a dictionary with target numbers as keys and average number of guesses as values.
         This function computes the average number of guesses for each target number
         by dividing the total number of guesses by the count of games for that target number.
    '''
    averages = {}
    for number, (total_guesses, count) in results.items():
        if count > 0:
            averages[number] = total_guesses / count
        else:
            averages[number] = None # Set average to None if no games were played for that target number
    return averages # Return the dictionary of average guesses

def main():
    #   The main function runs the simulation, computes averages, sorts them for easier review and prints the results.
    num_games = 1000
    results = simulate_games(num_games)
    averages = compute_averages(results)

    def sorting_key(item):
        return item[1] if item[1] is not None else float('inf')

    sorted_averages = dict(sorted(averages.items(), key=sorting_key))

    print("Average number of guesses for each target number (1-100 over {} game:".format(num_games))
    for number, avg in sorted_averages.items():
        if avg is not None:
            print("Number: {}: {:.2f} guesses".format(number, avg))
        else:
            print("Number: {}: No games played with this number".format(number))

if __name__ == "__main__":
    main()
    #  Call the main function if the script is run directly
