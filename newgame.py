import random

# Define the snakes and ladders using a dictionary
snakes_and_ladders = {
    # Ladders
    2: 38,
    7: 14,
    8: 31,
    15: 26,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    78: 98,
    87: 94,

    # Snakes
    16: 6,
    46: 25,
    49: 11,
    62: 19,
    64: 60,
    74: 53,
    89: 68,
    92: 88,
    95: 75,
    99: 80
}

# Function to roll the dice
def roll_dice():
    return random.randint(1, 6)

# Function to move the player
def move_player(player, current_position):
    dice_roll = roll_dice()
    print(f"{player} rolled a {dice_roll}.")
    new_position = current_position + dice_roll

    # Check if the new position is on a ladder or snake
    if new_position in snakes_and_ladders:
        new_position = snakes_and_ladders[new_position]
        if new_position > current_position + dice_roll:
            print(f"{player} climbed a ladder to {new_position}!")
        else:
            print(f"{player} got bitten by a snake and fell to {new_position}!")

    # Ensure the player doesn't go beyond 100
    if new_position > 100:
        print(f"{player} cannot move beyond 100. Staying at {current_position}.")
        return current_position

    return new_position

# Main game function
def play_game():
    players = ["Player 1", "Player 2"]
    positions = {player: 0 for player in players}

    while True:
        for player in players:
            input(f"{player}, press Enter to roll the dice...")
            positions[player] = move_player(player, positions[player])
            print(f"{player} is now at position {positions[player]}.\n")

            if positions[player] == 100:
                print(f"{player} wins!")
                return

# Start the game
play_game()