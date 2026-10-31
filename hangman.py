
import random

# ---------------------------------
# 1. WORD COLLECTION
# ---------------------------------

WORDS = [
    "python", "computer", "programming",
    "developer", "keyboard", "internet",
    "software", "technology", "database",
    "science", "hangman", "function",
    "variable", "algorithm", "education"
]

MAX_ATTEMPTS = 6


# ---------------------------------
# 2. HANGMAN ASCII ART
# ---------------------------------

HANGMAN_STAGES = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========
    """
]


# ---------------------------------
# 3. DISPLAY THE GAME
# ---------------------------------

def display_game(word, guessed_letters, attempts):

    print("\n" + "=" * 40)
    print("          HANGMAN WORD GAME")
    print("=" * 40)

    print(HANGMAN_STAGES[MAX_ATTEMPTS - attempts])

    # Display hidden and correctly guessed letters
    display_word = " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in word
    )

    print("Word:", display_word)
    print("Attempts Remaining:", attempts)

    # Display previously guessed letters
    if guessed_letters:
        print("Guessed Letters:",
              " ".join(sorted(guessed_letters)).upper())
    else:
        print("Guessed Letters: None")


# ---------------------------------
# 4. GET USER INPUT
# ---------------------------------

def get_guess():

    while True:

        guess = input("\nEnter a letter: ").lower().strip()

        if len(guess) != 1:
            print("Please enter only ONE letter.")
        
        elif not guess.isalpha() or not guess.isascii():
            print("Invalid input! Enter an English letter.")

        else:
            return guess


# ---------------------------------
# 5. MAIN GAME LOGIC
# ---------------------------------

def play_game():

    secret_word = random.choice(WORDS)

    guessed_letters = set()

    attempts = MAX_ATTEMPTS

    print("\nWelcome to the Hangman Game!")
    print("Guess the hidden word one letter at a time.")
    print("You have 6 incorrect attempts.")

    while attempts > 0:

        display_game(secret_word, guessed_letters, attempts)

        # Check whether the word has been completely guessed
        if all(letter in guessed_letters for letter in secret_word):
            print("\nCONGRATULATIONS!")
            print("You guessed the word:",
                  secret_word.upper())
            print("YOU WIN!")
            return

        guess = get_guess()

        # Prevent duplicate guesses
        if guess in guessed_letters:
            print("You already guessed that letter!")
            print("No attempt has been deducted.")
            continue

        guessed_letters.add(guess)

        # Check the guessed letter
        if guess in secret_word:
            print("\nCorrect guess!")
        else:
            attempts -= 1
            print("\nIncorrect guess!")
            print("You lost one attempt.")

    # Display final Hangman stage
    display_game(secret_word, guessed_letters, attempts)

    print("\nGAME OVER!")
    print("You ran out of attempts.")
    print("The correct word was:",
          secret_word.upper())


# ---------------------------------
# 6. REPLAY FUNCTION
# ---------------------------------

def main():

    while True:

        play_game()

        replay = input(
            "\nWould you like to play again? (yes/no): "
        ).lower().strip()

        if replay not in ("yes", "y"):
            print("\nThank you for playing Hangman!")
            print("Goodbye!")
            break


# ---------------------------------
# 7. PROGRAM STARTING POINT
# ---------------------------------

if __name__ == "__main__":
    main()
