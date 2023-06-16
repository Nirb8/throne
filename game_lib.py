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
                deck.append(card_lib.Card(4,-1))
                jokerToggle = False
            else:
                deck.append(card_lib.Card(5,-2))
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
        self.state.current_player = self.state.players[0]
    def make_move(self, player, played_cards):
        self.state.last_played_cards = played_cards
        self.state.last_played_player = player
        for card in played_cards:
            player.hand.remove(card)
        self.state.advance_turn()
    # return True if everyone else passed and a new trick is started, and False otherwise
    def make_pass(self, player):
        self.state.advance_turn()
        if self.state.last_played_player == self.state.current_player:
            self.state.last_played_cards = []
            return True
        return False
        
class Player:
    def __init__(self, player_id, username):
        self.player_id = player_id
        self.username = username
        self.hand = []
    def __str__(self):
        return self.username
        
def find_game(id, game_list):
    for g in game_list:
        if g.channel_id == id:
            return g
    return False

def find_player(player_id, game):
    players = game.state.players
    for p in players:
        if p.player_id == player_id:
            return p
    return False

class GameState:
    def __init__(self, current_player, players):
        self.current_player = current_player
        self.players = players
        self.last_played_cards = []
        self.last_played_player = None
        self.is_jackback = False
        self.is_suitlock = False
        self.num_revolutions = 0
    def is_revolution(self):
        is_revolution = self.num_revolutions % 2 > 0
        if self.is_jackback:
            is_revolution = not is_revolution
        return is_revolution
    def check_play_valid(self, proposed_play):
        if len(proposed_play) != len(self.last_played_cards) and len(self.last_played_cards) > 0:
            return f"Your play of {len(proposed_play)} card(s) does not match number of cards in the current trick ({len(self.last_played_cards)} card(s))"
        is_revolution = self.is_revolution()
        beats_current_play = card_lib.compare_hands(proposed_play, self.last_played_cards, is_revolution)
        if not beats_current_play:
            return f"Your play of {card_lib.hand_as_emotes(proposed_play)} does not beat the current trick ({card_lib.hand_as_emotes(self.last_played_cards)})"
        return "ok"
    def advance_turn(self):
        current_player_index = self.players.index(self.current_player)
        new_player_index = (current_player_index + 1) % len(self.players)
        self.current_player = self.players[new_player_index]
    def get_turn_order_string(self):
        turn_order_string = ""
        for player in self.players:
            turn_order_string += f"{player.username}\n"
        return turn_order_string
