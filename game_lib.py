import card_lib
import random
class Game:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.state = GameState(None, [])
        self.deck = []
        self.gaming = False
    def shuffle(self, num_decks = 1, num_jokers = 2):
        deck = []
        for d in range(num_decks):
            for i in range(4):
                for j in range(13):
                    deck.append(card_lib.Card(i, j))
        jokerToggle = True
        for i in range(num_jokers):
            if jokerToggle:
                deck.append(card_lib.Card(0,-1))
                jokerToggle = False
            else:
                deck.append(card_lib.Card(2,-2))
                jokerToggle = True
        random.shuffle(deck)
        # for card in deck:
        #     print(card)
        self.deck = deck
    def deal(self):
        for player in self.state.players:
            player.hand = []
        while(len(self.deck)>=len(self.state.players)):
            for player in self.state.players:
                card = self.deck.pop(0)
                player.hand.append(card)
        for player in self.state.players:
            player.hand.sort()
        self.gaming = True
class Player:
    def __init__(self, player_id, username):
        self.player_id = player_id
        self.username = username
        self.hand = []
        
def find_game(id, game_list):
    for g in game_list:
        if g.channel_id == id:
            return g
    return False

def find_player(player_id, game):
    players = game.players
    for p in players:
        if p.player_id == player_id:
            return p
    return False

class GameState:
    def __init__(self, current_player, players):
        self.current_player = current_player
        self.players = players
        self.last_played_cards = []
        self.is_jackback = False
        self.is_suitlock = False
        self.num_revolutions = 0
    def check_play_valid(self, proposed_play):
        return True
