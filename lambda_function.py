import json
from tarot_service import TarotService
from deck import DeckService
from s3_service import S3Service
from cards import tarot_deck

bucket = "ithome-ironman-2025"
key = "tarot.json"

def lambda_handler(event, context):

    # 接收 request
    json_str = json.dumps(event)
    body = json.loads(json_str)
    question_type = body.get("question_type")
    
    # 初始化
    s3_service  = S3Service()
    deckService = DeckService()
    service = TarotService(s3_service, bucket, key)

    # 取得完整的塔羅牌 ID 清單
    deck = tarot_deck.copy()
    deck = deckService.shuffle(deck) # 洗牌
    cards = deckService.draw_card(deck, 3) # 抽隨機三張
    cards_info = __get_tarot_info(s3_service, cards)

    if question_type == "daily-tarot":
        return service.daily_tarot(cards_info)
    else:
        question = body.get("message")
        return service.question_tarot(question, cards_info)

    
# 取得塔羅牌資訊
def __get_tarot_info(s3_service, cards):
    info = s3_service.read_s3_file(bucket, key)
    # 為塔羅牌建立索引，方便搜尋
    tarot_by_id = {o['id']: o for o in json.loads(info)}
    # 檢查是否 78 張牌都能正確讀取塔羅牌資訊
    missing = [c['id'] for c in tarot_deck if c['id'] not in tarot_by_id]
    if missing:
        raise ValueError(f"找不到塔羅牌: {missing}")
    cards_info = []
    for i in range(3):
        card_info = tarot_by_id.get(cards[i]['id'])
        card = {
            'card_id': card_info['id'],
            'card_name': card_info['name_zh'],
            'story': card_info['story']
            }
        if cards[i]['position'] == '↑':
            card['position'] = 'upright'
            card['keyword'] = card_info['upright_meta']['keywords']
        else:
            card['position'] = 'reversed'
            card['keyword'] = card_info['reversed_meta']['keywords']

        cards_info.append(card)
    return cards_info