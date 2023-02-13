EMOTE_LIST = ["<:A_hearts:1073878545455124571>", "<:2_hearts:1073878461053161472>", "<:Q_hearts:1073878549532004383>", "<:K_hearts:1073878548043014194>", "<:J_hearts:1073878546801508353>", "<:3_hearts:1073878462512775178>", "<:4_hearts:1073878463775244308>", "<:5_hearts:1073878464614121523>", "<:6_hearts:1073878465490731058>", "<:7_hearts:1073878467332022332>", "<:8_hearts:1073878541386657802>", "<:9_hearts:1073878542833700864>", "<:10_hearts:1073878543739662366>", "<:10_clubs:1073878161495965737>", "<:10_diamonds:1073876973966852167>", "<:10_spades:1073877343371800616>", "<:2_clubs:1073878065270231050>", "<:2_diamonds:1073866501662191626>", "<:2_spades:1073877181387771925>", "<:3_clubs:1073878067455463454>", "<:3_diamonds:1073865772578918410>", "<:3_spades:1073877183069683732>", "<:4_clubs:1073878068655030293>", "<:4_diamonds:1073876967671201853>", "<:4_spades:1073877183820464198>", "<:5_clubs:1073878069674250320>", "<:5_diamonds:1073876969147617300>", "<:5_spades:1073877184940355594>", "<:6_clubs:1073878070420832297>", "<:6_diamonds:1073876970288459857>", "<:6_spades:1073877185997328454>", "<:7_clubs:1073878072085975121>", "<:7_diamonds:1073876971060207647>", "<:7_spades:1073877187431759922>", "<:8_clubs:1073878158052438036>", "<:8_diamonds:1073876971433500743>", "<:8_spades:1073877340658073640>", "<:9_clubs:1073878160086683770>", "<:9_diamonds:1073876972675006494>", "<:9_spades:1073877341819899924>", "<:A_diamonds:1073866534147084348>", "<:A_spades:1073877347637416038>", "<:J_clubs:1073878162670366761>", "<:J_diamonds:1073876974797344818>", "<:J_spades:1073877350015582248>", "<:K_clubs:1073878164243234823>", "<:K_diamonds:1073877048239607828>", "<:K_spades:1073877351399698503>", "<:Q_clubs:1073878165287612447>", "<:Q_diamonds:1073877049078464592>", "<:Q_spades:1073877352565710918>", "<:A_clubs:1074251701952983140>"]

#TODO: make a rank -> Emote Rank and Suite -> Emote Suite Dict

def get_emote(card):
    if card["suit"] == -1:
        return "<:R_red:1073878240101412874>"
    if card["suit"] == -2:
        return "<:R_black:1073878238457233418>"
    emoji_string = ""
    if card["rank"] == 12:
        emoji_string += "2"
    if card["rank"] == 11:
        emoji_string += "A"
    if card ["rank"] == 10:
        emoji_string += "K"
    if card["rank"] == 9:
        emoji_string += "Q"
    if card["rank"] == 8:
        emoji_string += "J"
    if card["rank"] < 8:
        real_value = card["rank"] + 3
        emoji_string += str(real_value)
    emoji_string += "_"
    # append suit
    if card["suit"] == 0:
        emoji_string += "clubs"
    if card["suit"] == 1:
        emoji_string += "diamonds"
    if card["suit"] == 2:
        emoji_string += "hearts"
    if card["suit"] == 3:
        emoji_string += "spades"

    for card_emote in EMOTE_LIST:
        if emoji_string in card_emote:
            return card_emote
    return "💀"
