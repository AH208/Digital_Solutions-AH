class LinearCongruentialGenerator:
    def __init__(self, seed, a=1664525, c=1013904223, m=2**32):
        self.state = seed
        self.a = a
        self.c = c
        self.m = m

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def random(self):
        return self.next() / self.m

# Example usage:
seed = 42
prng = LinearCongruentialGenerator(seed)

# Generate and print 10 pseudorandom numbers
for _ in range(10):
    print(prng.random())


#   number = random.randint(1, 100)
# guess = 0
# attempt = 0
#
# while guess != number:
#     try:
#         guess = int(input(f"Attempt {attempt +1}: Enter a number between 1 and 100: "))
#         if guess < 1 or guess > 100:
#             print("Please enter a number within the range!")
#             continue
#         attempt += 1
#
#         if guess > number:
#             print("Too high!")
#         elif guess < number:
#             print("Too low!")
#     except ValueError:
#         print("Please enter a valid number!")
#
# print(f"You a winner! You guessed in {attempt} attempts!")
# print("Exiting the program.")