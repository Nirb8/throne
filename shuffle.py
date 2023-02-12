import random
#This code was written by ChatGPT
def shuffle_and_deal(num_players, num_jokers = 2):
    deck = ['Ace of Spades', '2 of Spades', '3 of Spades', '4 of Spades', '5 of Spades', '6 of Spades', '7 of Spades',
            '8 of Spades', '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades', 'King of Spades',
            'Ace of Hearts', '2 of Hearts', '3 of Hearts', '4 of Hearts', '5 of Hearts', '6 of Hearts', '7 of Hearts',
            '8 of Hearts', '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts', 'King of Hearts',
            'Ace of Diamonds', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds', '5 of Diamonds', '6 of Diamonds',
            '7 of Diamonds', '8 of Diamonds', '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds',
            'Queen of Diamonds', 'King of Diamonds', 'Ace of Clubs', '2 of Clubs', '3 of Clubs', '4 of Clubs',
            '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', '9 of Clubs', '10 of Clubs', 'Jack of Clubs',
            'Queen of Clubs', 'King of Clubs']
    deck = deck + ["Joker"] * num_jokers

    random.shuffle(deck)

    num_cards_per_player = len(deck) // num_players
    hands = []
    for i in range(num_players):
        hand = deck[i * num_cards_per_player: (i + 1) * num_cards_per_player]
        hands.append(hand)

    leftover = deck[num_players * num_cards_per_player:]

    return hands, leftover


# if __name__ == '__main__':
#     hands, leftover = shuffle_and_deal(3)
#     for hand in hands:
#         print(f"{hand} \n{len(hand)}")
#     print(f"Leftover: {leftover}")


def get_shuffled_deck_numeric(num_jokers):
    decktionary = {}
    card_id = 0
    for i in range(4):
        for j in range(13):
            decktionary[card_id] = {"suit": i, "rank" : j}
            card_id += 1
    jokerSuit = -1
    for k in range(num_jokers):
        decktionary[card_id] = {"suit":jokerSuit, "rank":-1}
        if jokerSuit == -1:
            jokerSuit = -2
        else:
            jokerSuit = -1
        card_id += 1
    random.shuffle(decktionary)
    print(decktionary)
    return decktionary
