EMOTE_DICT = {'A_hearts': '<:A_hearts:1073878545455124571>', '2_hearts': '<:2_hearts:1073878461053161472>', 'Q_hearts': '<:Q_hearts:1073878549532004383>', 'K_hearts': '<:K_hearts:1073878548043014194>', 'J_hearts': '<:J_hearts:1073878546801508353>', '3_hearts': '<:3_hearts:1073878462512775178>', '4_hearts': '<:4_hearts:1073878463775244308>', '5_hearts': '<:5_hearts:1073878464614121523>', '6_hearts': '<:6_hearts:1073878465490731058>', '7_hearts': '<:7_hearts:1073878467332022332>', '8_hearts': '<:8_hearts:1073878541386657802>', '9_hearts': '<:9_hearts:1073878542833700864>', '10_hearts': '<:10_hearts:1073878543739662366>', '10_clubs': '<:10_clubs:1073878161495965737>', '10_diamonds': '<:10_diamonds:1073876973966852167>', '10_spades': '<:10_spades:1073877343371800616>', '2_clubs': '<:2_clubs:1073878065270231050>', '2_diamonds': '<:2_diamonds:1073866501662191626>', '2_spades': '<:2_spades:1073877181387771925>', '3_clubs': '<:3_clubs:1073878067455463454>', '3_diamonds': '<:3_diamonds:1073865772578918410>', '3_spades': '<:3_spades:1073877183069683732>', '4_clubs': '<:4_clubs:1073878068655030293>', '4_diamonds': '<:4_diamonds:1073876967671201853>', '4_spades': '<:4_spades:1073877183820464198>', '5_clubs': '<:5_clubs:1073878069674250320>', '5_diamonds': '<:5_diamonds:1073876969147617300>', '5_spades': '<:5_spades:1073877184940355594>', '6_clubs': '<:6_clubs:1073878070420832297>', '6_diamonds': '<:6_diamonds:1073876970288459857>', '6_spades': '<:6_spades:1073877185997328454>', '7_clubs': '<:7_clubs:1073878072085975121>', '7_diamonds': '<:7_diamonds:1073876971060207647>', '7_spades': '<:7_spades:1073877187431759922>', '8_clubs': '<:8_clubs:1073878158052438036>', '8_diamonds': '<:8_diamonds:1073876971433500743>', '8_spades': '<:8_spades:1073877340658073640>', '9_clubs': '<:9_clubs:1073878160086683770>', '9_diamonds': '<:9_diamonds:1073876972675006494>', '9_spades': '<:9_spades:1073877341819899924>', 'A_diamonds': '<:A_diamonds:1073866534147084348>', 'A_spades': '<:A_spades:1073877347637416038>', 'J_clubs': '<:J_clubs:1073878162670366761>', 'J_diamonds': '<:J_diamonds:1073876974797344818>', 'J_spades': '<:J_spades:1073877350015582248>', 'K_clubs': '<:K_clubs:1073878164243234823>', 'K_diamonds': '<:K_diamonds:1073877048239607828>', 'K_spades': '<:K_spades:1073877351399698503>', 'Q_clubs': '<:Q_clubs:1073878165287612447>', 'Q_diamonds': '<:Q_diamonds:1073877049078464592>', 'Q_spades': '<:Q_spades:1073877352565710918>', 'A_clubs': '<:A_clubs:1074251701952983140>'}

rank_dict = {
    12: "2",
    11: "A",
    10: "K",
    9: "Q",
    8: "J",
}

suite_dict = {
    0: 'clubs',
    1: 'diamonds',
    2: 'hearts',
    3: 'spades'
}

rank_to_num_dict = {
    "3": 0,
    "4": 1,
    "5": 2,
    "6": 3,
    "7": 4,
    "8": 5,
    "9": 6,
    "10": 7,
    "j": 8,
    "q": 9,
    "k": 10,
    "a": 11,
    "2": 12,
    "o": -1,
    "w": -1
}
def rank_to_num(rank):
    rank_lower = rank.lower()
    if rank_lower in rank_to_num_dict:
        return rank_to_num_dict[rank_lower]
    return -69
def remove_card(card, hand):
    if card["suit"] < 0 or card["rank"] < 0:
        # remove a joker, any joker
        for card in hand:
            if card["rank"] < 0:
                hand.remove(card)
                break
        return
    # hand.remove(card)
    card_to_remove = None
    for pcard in hand:
        if card["rank"] == pcard["rank"] and card["suit"] == pcard["suit"]:
            card_to_remove = pcard
            break
    hand.remove(card_to_remove)


def get_emote(card):
    if card["suit"] == -1:
        return "<:R_red:1073878240101412874>"
    if card["suit"] == -2:
        return "<:R_black:1073878238457233418>"
    emoji_string = ""
    if card['rank'] not in rank_dict.keys():
        real_value = card["rank"] + 3
        emoji_string += str(real_value)
    else:
        emoji_string += rank_dict[card['rank']]
    emoji_string += "_"
    # append suit
    if card['suit'] not in suite_dict.keys():
        return "💀"
    emoji_string += suite_dict[card['suit']]

    if emoji_string not in  EMOTE_DICT.keys():
        return "💀"
    return EMOTE_DICT[emoji_string]

def verify_play(player_hand, proposed_play):
    legal = True
    num_jokers = 0
    held_jokers = 0
    
    for p_card in player_hand:
        if p_card["rank"] < 0:
            held_jokers += 1
    for card in proposed_play:
        found = False
        if card["rank"] < 0 or card["suit"] < 0:
            num_jokers += 1
            found = True
        else:
            for p_card in player_hand:
                if p_card["rank"] == card["rank"]:
                    if p_card["suit"] == card["suit"]:
                        found = True
                        break
        if found is False:
            legal = False
            break
    print(f"player holding {held_jokers}, need {num_jokers}")
    if held_jokers >= num_jokers:
        legal = True
    return legal