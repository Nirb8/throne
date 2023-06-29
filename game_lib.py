import card_lib
import random
from enum import Enum

class MoveStatus(Enum):
    Normal = 0
    One_Player_Out = 1
    All_Out = 2
    Eight_Cut = 3
    Jackback = 4
    Revolution = 5
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
        me = self.state.players[0]
        me.hand.append(card_lib.Card(0, 5))
        me.hand.append(card_lib.Card(1, 5))
        me.hand.append(card_lib.Card(2, 5))
        me.hand.append(card_lib.Card(3, 5))
        
        me.hand.append(card_lib.Card(0, 8))
        me.hand.append(card_lib.Card(1, 8))
        me.hand.append(card_lib.Card(2, 8))
        me.hand.append(card_lib.Card(3, 8))
        
        me.hand.append(card_lib.Card(1,0))
        me.hand.append(card_lib.Card(2,0))
        me.hand.append(card_lib.Card(3,0))
        
        me.hand.sort()
        
    def make_move(self, player, played_cards):
        move_status_message = ""
        self.state.last_played_cards = played_cards
        self.state.last_played_player = player
        for card in played_cards:
            player.hand.remove(card)
        self.state.advance_turn()
        move_status_message += self.do_special_effects(played_cards, player)
        # game ender
        if player.hand == [] and self.get_num_players_remaining() == 2:
            self.state.win_order.append(player)
            player.is_active = False
            last_player = self.get_last_remaining_player()
            self.state.win_order.append(last_player)
            if self.state.biggest_loser is not None:
                self.state.win_order.append(self.state.biggest_loser)
            self.assign_titles()
            move_status_message += f"{player} has played all their cards and is now out of the game.\n"
            move_status_message += f"Game is over, standings: \n{self.get_player_titles()}\n"
            return move_status_message
        if player.hand == []:
            self.state.win_order.append(player)
            player.is_active = False
            move_status_message += f"{player} has played all their cards and is now out of the game.\n"
            if self.state.current_player == player:
                self.state.advance_turn() # turn order the next person if the player went out on an 8 or joker
                self.state.turn_ordered = self.state.current_player
            return move_status_message
        if move_status_message != "":
            return move_status_message
        return "ok"
    def do_special_effects(self, played_cards, player):
        hand_effective_rank = card_lib.get_hand_value(played_cards, self.state.is_revolution())
        special_effect_status_string = ""
        if hand_effective_rank == 5:
            self.state.last_played_cards = []
            self.state.current_player = player
            self.state.is_jackback = False
            special_effect_status_string += f"{player} played an Eight-valued hand, triggering an 8-Stop!\n"
        if hand_effective_rank == -1:
            self.state.last_played_cards = []
            self.state.current_player = player
            self.state.is_jackback = False
            special_effect_status_string += f"{player} played a Joker-valued hand, auto-passing to their next turn...\n"
        if hand_effective_rank == 8:
            self.state.is_jackback = not self.state.is_jackback
            special_effect_status_string += f"{player} played a Jack-valued hand, Jackback is now active! (Card values are reversed until the end of this trick!)\n"
        if card_lib.same_rank_hand(played_cards) and len(played_cards) == 4:
            self.state.num_revolutions += 1
            if self.state.num_revolutions == 1:
                special_effect_status_string += f"{player} played a 4-of-a-kind, Revolution has started! (Card values are reversed until the end of this game!)\n"
            num_counters = self.state.num_revolutions - 1
            counter_string = ""
            for i in range(0, num_counters):
                counter_string += "Counter-"
            counter_revolution_string = f"{player} played a 4-of-a-kind, triggering a {counter_string}Revolution!!\n"
            if self.state.num_revolutions % 2 == 0:
                counter_revolution_string += "(Card values are back to normal!)"
            if self.state.num_revolutions % 2 == 1:
                counter_revolution_string += "(Card values are reversed again!)"
            if self.state.num_revolutions > 1:
                special_effect_status_string += counter_revolution_string
        return special_effect_status_string
    # return True if everyone else passed and a new trick is started, and False otherwise
    def make_pass(self):
        self.state.advance_turn()
        if self.state.last_played_player == self.state.current_player or self.state.last_played_player.is_active is False and self.state.turn_ordered == self.state.current_player:
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
        self.turn_ordered = None

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