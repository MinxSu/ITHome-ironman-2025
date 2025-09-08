import random
from cards import major_arcana, minor_arcana 

from bedrock_service import BedrockService 

def lambda_handler(event, context):
    cards = []
    while len(cards) < 3:
        deck = major_arcana + minor_arcana
        shuffled = shuffle(deck)
        card = draw_card(shuffled)
        if not card in cards:
            cards.append((card, position()))
        return cards
    #　bedrock = BedrockService()
    # response = bedrock.tarot_reading()

    # return {
    #     'statusCode': 200,
    #     'body': response
    # }

# 抽牌
def draw_card(shuffled_card):
    return random.choice(shuffled_card)

# 正位/逆位
def position():
    return random.choice(['Upright', 'Reversed'])

# 洗牌
def shuffle(deck):
    shuffled = deck[:]       
    random.shuffle(shuffled)
    return shuffled