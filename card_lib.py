from enum import Enum


class Suit(Enum):
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3
    JOKER_RED = 4
    JOKER_BLACK = 5
    # TODO add an additional option suit for staircase option cards

class Card:
    def __init__(self, suit, rank):
        self.suit = Suit(suit)
        self.rank = rank

    def __str__(self):
        if self.suit == 4:
            return "R_red"
        if self.suit == 5:
            return "R_black"
        return f"{self.get_rank_string()}_{self.suit.name.lower()}"

    def __lt__(self, other):
        # handle joker sort
        if self.rank < 0 and other.rank < 0:
            return self.rank < other.rank
        if self.rank < 0 and other.rank >= 0:
            return False
        if self.rank >= 0 and other.rank < 0:
            return True
        if self.rank == other.rank:
            return self.suit.value < other.suit.value
        return self.rank < other.rank

    def get_rank_string(self):
        rank_dict = {
            12: "2",
            11: "A",
            10: "K",
            9: "Q",
            8: "J",
            -1: "R_black",
            -2: "R_red"
        }
        if self.rank not in rank_dict.keys():
            real_value = self.rank + 3
            return str(real_value)
        else:
            return rank_dict[self.rank]

    def get_emote(self):
        EMOTE_DICT = {'A_hearts': '<:A_hearts:1073878545455124571>', '2_hearts': '<:2_hearts:1073878461053161472>', 'Q_hearts': '<:Q_hearts:1073878549532004383>', 'K_hearts': '<:K_hearts:1073878548043014194>', 'J_hearts': '<:J_hearts:1073878546801508353>', '3_hearts': '<:3_hearts:1073878462512775178>', '4_hearts': '<:4_hearts:1073878463775244308>', '5_hearts': '<:5_hearts:1073878464614121523>', '6_hearts': '<:6_hearts:1073878465490731058>', '7_hearts': '<:7_hearts:1073878467332022332>', '8_hearts': '<:8_hearts:1073878541386657802>', '9_hearts': '<:9_hearts:1073878542833700864>', '10_hearts': '<:10_hearts:1073878543739662366>', '10_clubs': '<:10_clubs:1073878161495965737>', '10_diamonds': '<:10_diamonds:1073876973966852167>', '10_spades': '<:10_spades:1073877343371800616>', '2_clubs': '<:2_clubs:1073878065270231050>', '2_diamonds': '<:2_diamonds:1073866501662191626>', '2_spades': '<:2_spades:1073877181387771925>', '3_clubs': '<:3_clubs:1073878067455463454>', '3_diamonds': '<:3_diamonds:1073865772578918410>', '3_spades': '<:3_spades:1073877183069683732>', '4_clubs': '<:4_clubs:1073878068655030293>', '4_diamonds': '<:4_diamonds:1073876967671201853>', '4_spades': '<:4_spades:1073877183820464198>', '5_clubs': '<:5_clubs:1073878069674250320>', '5_diamonds': '<:5_diamonds:1073876969147617300>',
                      '5_spades': '<:5_spades:1073877184940355594>', '6_clubs': '<:6_clubs:1073878070420832297>', '6_diamonds': '<:6_diamonds:1073876970288459857>', '6_spades': '<:6_spades:1073877185997328454>', '7_clubs': '<:7_clubs:1073878072085975121>', '7_diamonds': '<:7_diamonds:1073876971060207647>', '7_spades': '<:7_spades:1073877187431759922>', '8_clubs': '<:8_clubs:1073878158052438036>', '8_diamonds': '<:8_diamonds:1073876971433500743>', '8_spades': '<:8_spades:1073877340658073640>', '9_clubs': '<:9_clubs:1073878160086683770>', '9_diamonds': '<:9_diamonds:1073876972675006494>', '9_spades': '<:9_spades:1073877341819899924>', 'A_diamonds': '<:A_diamonds:1073866534147084348>', 'A_spades': '<:A_spades:1073877347637416038>', 'J_clubs': '<:J_clubs:1073878162670366761>', 'J_diamonds': '<:J_diamonds:1073876974797344818>', 'J_spades': '<:J_spades:1073877350015582248>', 'K_clubs': '<:K_clubs:1073878164243234823>', 'K_diamonds': '<:K_diamonds:1073877048239607828>', 'K_spades': '<:K_spades:1073877351399698503>', 'Q_clubs': '<:Q_clubs:1073878165287612447>', 'Q_diamonds': '<:Q_diamonds:1073877049078464592>', 'Q_spades': '<:Q_spades:1073877352565710918>', 'A_clubs': '<:A_clubs:1074251701952983140>', 'R_red': '<:R_red:1073878240101412874>', 'R_black': '<:R_black:1073878238457233418>'}
        return EMOTE_DICT[str(self)]

    def get_human_readable(self):
        CARD_NAME_DICT = {'A_hearts': 'Ace of Hearts', '2_hearts': 'Two of Hearts', '3_hearts': 'Three of Hearts', '4_hearts': 'Four of Hearts', '5_hearts': 'Five of Hearts', '6_hearts': 'Six of Hearts', '7_hearts': 'Seven of Hearts', '8_hearts': 'Eight of Hearts', '9_hearts': 'Nine of Hearts', '10_hearts': 'Ten of Hearts', 'J_hearts': 'Jack of Hearts', 'Q_hearts': 'Queen of Hearts', 'K_hearts': 'King of Hearts', 'A_diamonds': 'Ace of Diamonds', '2_diamonds': 'Two of Diamonds', '3_diamonds': 'Three of Diamonds', '4_diamonds': 'Four of Diamonds', '5_diamonds': 'Five of Diamonds', '6_diamonds': 'Six of Diamonds', '7_diamonds': 'Seven of Diamonds', '8_diamonds': 'Eight of Diamonds', '9_diamonds': 'Nine of Diamonds', '10_diamonds': 'Ten of Diamonds', 'J_diamonds': 'Jack of Diamonds', 'Q_diamonds': 'Queen of Diamonds',
                          'K_diamonds': 'King of Diamonds', 'A_clubs': 'Ace of Clubs', '2_clubs': 'Two of Clubs', '3_clubs': 'Three of Clubs', '4_clubs': 'Four of Clubs', '5_clubs': 'Five of Clubs', '6_clubs': 'Six of Clubs', '7_clubs': 'Seven of Clubs', '8_clubs': 'Eight of Clubs', '9_clubs': 'Nine of Clubs', '10_clubs': 'Ten of Clubs', 'J_clubs': 'Jack of Clubs', 'Q_clubs': 'Queen of Clubs', 'K_clubs': 'King of Clubs', 'A_spades': 'Ace of Spades', '2_spades': 'Two of Spades', '3_spades': 'Three of Spades', '4_spades': 'Four of Spades', '5_spades': 'Five of Spades', '6_spades': 'Six of Spades', '7_spades': 'Seven of Spades', '8_spades': 'Eight of Spades', '9_spades': 'Nine of Spades', '10_spades': 'Ten of Spades', 'J_spades': 'Jack of Spades', 'Q_spades': 'Queen of Spades', 'K_spades': 'King of Spades', 'R_red': 'Red Joker', 'R_black': 'Black Joker'}
        return CARD_NAME_DICT[str(self)]
    
# these weren't working as @classmethod so they are orphaned util functions until they find a better home
def hand_as_emotes(hand: list):
    emote_string = ""
    for card in hand:
        emote_string += card.get_human_readable()

 # Checks if a play is a legal move(not if it also beats the current play)
def is_play_legal(self, proposed_play: list):
    rank_to_match = proposed_play[0].rank
    is_same_rank = True
    for card in proposed_play:
        if card.rank != rank_to_match:
            is_same_rank = False
