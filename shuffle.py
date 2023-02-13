import random
#This code was written by ChatGPT
def deal(num_players, deck):
    num_cards_per_player = len(deck) // num_players
    hands = []
    deck_list = list(deck.values())
    for i in range(num_players):
        hand = deck_list[i * num_cards_per_player: (i + 1) * num_cards_per_player]
        hands.append(hand)
    leftover = deck_list[num_players * num_cards_per_player:]

    return hands, leftover


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
    return decktionary
