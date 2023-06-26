import card_lib
import random
from enum import Enum

class Game:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.state = GameState(None, [])
        self.deck = []
        self.gaming = False

    def shuffle(self, num_decks=1, num_jokers=2):
        deck = []
        for d in range(num_decks):
            for i in range(4):
                for j in range(13):
                    deck.append(card_lib.Card(i, j))
        jokerToggle = True
        for i in range(num_jokers):
            if jokerToggle:
                deck.append(card_lib.Card(4, -1))
                jokerToggle = False
            else:
                deck.append(card_lib.Card(5, -2))
                jokerToggle = True
        random.shuffle(deck)
        # for card in deck:
        #     print(card)
        self.deck = deck

    def deal(self):
        for player in self.state.players:
            player.hand = []
            player.is_active = True
        while len(self.deck) >= len(self.state.players):
            for player in self.state.players:
                card = self.deck.pop(0)
                player.hand.append(card)
        for player in self.state.players:
            player.hand.sort()
        self.gaming = True
        self.state.current_player = self.state.players[0]

    def deal_paltry(self):
        for player in self.state.players:
            player.hand = []
            player.is_active = True
        card_counter = 0
        for player in self.state.players:
            player.hand.append(card_lib.Card(0, card_counter))
            card_counter += 1
            self.gaming = True
            self.state.current_player = self.state.players[0]

    def make_move(self, player, played_cards):
        self.state.last_played_cards = played_cards
        self.state.last_played_player = player
        for card in played_cards:
            player.hand.remove(card)
        self.state.advance_turn()
        self.do_special_effects(played_cards, player)
        # game ender
        if player.hand == [] and self.get_num_players_remaining() == 2:
            self.state.win_order.append(player)
            player.is_active = False
            last_player = self.get_last_remaining_player()
            self.state.win_order.append(last_player)
            if self.state.biggest_loser is not None:
                self.state.win_order.append(self.state.biggest_loser)
            self.assign_titles()
            self.state.trading_phase = True
            return 2
        if player.hand == []:
            self.state.win_order.append(player)
            player.is_active = False
            return 1
        return 0  # TODO replace with enums
    def do_special_effects(self, played_cards, player):
        hand_effective_rank = card_lib.get_hand_value(played_cards, self.state.is_revolution)
        if hand_effective_rank == 5 or hand_effective_rank == -1:
            self.state.last_played_cards = []
            self.state.current_player = player
        
    # return True if everyone else passed and a new trick is started, and False otherwise
    def make_pass(self):
        self.state.advance_turn()
        if self.state.last_played_player == self.state.current_player:
            self.state.last_played_cards = []
            return True
        return False

    def get_num_players_remaining(self):
        num_players = 0
        for player in self.state.players:
            if player.is_active:
                num_players += 1
        return num_players

    def get_last_remaining_player(self):
        if self.get_num_players_remaining() > 1:
            return None
        for player in self.state.players:
            if player.is_active:
                return player
    def assign_titles(self):
        first = self.state.win_order.pop(0)
        last = self.state.win_order.pop(len(self.state.win_order)-1)
        first.title = Title.PRESIDENT
        first.is_trading = True
        last.title = Title.BIGGEST_LOSER
        last.is_trading = True
        if len(self.state.win_order) > 1:
            second = self.state.win_order.pop(0)
            second.title = Title.VICE_PRESIDENT
            second.is_trading = True
            second_to_last = self.state.win_order.pop(len(self.state.win_order)-1)
            second_to_last.title = Title.POOR
            second_to_last.is_trading = True
        for player in self.state.win_order: 
            player.title = Title.THE_GUY
            player.is_trading = False
    def get_player_titles(self):
        title_string = ""
        for player in self.state.players:
            if player.title == Title.PRESIDENT:
                title_string += f"👑 {player.get_title_string()}\n"
        for player in self.state.players:
            if player.title == Title.VICE_PRESIDENT:
                title_string += f"🥈 {player.get_title_string()}\n"
        for player in self.state.players:
            if player.title == Title.THE_GUY:
                title_string += f"👨 {player.get_title_string()}\n"
        for player in self.state.players:
            if player.title == Title.POOR:
                title_string += f"😢 {player.get_title_string()}\n"
        for player in self.state.players:
            if player.title == Title.BIGGEST_LOSER:
                title_string += f"😭 {player.get_title_string()}\n"
        return title_string
    def find_trading_recipient(self, source_player):
        target_title = Title("President")
        if source_player.title == Title("President"):
            target_title = Title("Biggest Loser")
        if source_player.title == Title("Vice President"):
            target_title = Title("Poor")
        if source_player.title == Title("Poor"):
            target_title = Title("Vice President")
        target_player = self.get_player_by_title(target_title)
        return target_player
    def get_player_by_title(self, title):
        for player in self.state.players:
            if player.title == title:
                return player
    def is_trading_happening(self):
        for player in self.state.players:
            if player.is_trading:
                return True
        return False
class Title(Enum):
    PRESIDENT = "President"
    VICE_PRESIDENT = "Vice President"
    THE_GUY = "*The Guy*"
    POOR = "Poor"
    BIGGEST_LOSER = "Biggest Loser"
class Player:
    def __init__(self, player_id, username):
        self.player_id = player_id
        self.username = username
        self.hand = []
        self.is_active = False
        self.title = Title.THE_GUY
        self.is_trading = False

    def __str__(self):
        return self.username
    def get_title_string(self):
        return f"[{self.title.value}] {self.username}"

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
        self.win_order = []
        self.biggest_loser = None

    def is_revolution(self):
        is_revolution = self.num_revolutions % 2 > 0
        if self.is_jackback:
            is_revolution = not is_revolution
        return is_revolution

    def check_play_valid(self, proposed_play):
        if (
            len(proposed_play) != len(self.last_played_cards)
            and len(self.last_played_cards) > 0
        ):
            return f"Your play of {len(proposed_play)} card(s) does not match number of cards in the current trick ({len(self.last_played_cards)} card(s))"
        is_revolution = self.is_revolution()
        beats_current_play = card_lib.compare_hands(
            proposed_play, self.last_played_cards, is_revolution
        )
        if not beats_current_play:
            return f"Your play of {card_lib.hand_as_emotes(proposed_play)} does not beat the current trick ({card_lib.hand_as_emotes(self.last_played_cards)})"
        return "ok"

    def advance_turn(self):
        current_player_index = self.players.index(self.current_player)
        new_player_index = (current_player_index + 1) % len(self.players)
        self.current_player = self.players[new_player_index]
        if self.current_player.is_active is False:
            self.advance_turn()

    def get_turn_order_string(self):
        turn_order_string = ""
        for player in self.players:
            turn_order_string += f"{player.username}\n"
        return turn_order_string