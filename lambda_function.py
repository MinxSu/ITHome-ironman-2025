import json
import random
from deck import DeckService
from s3_service import S3Service
from cards import tarot_deck

from bedrock_service import BedrockService 

bucket = "ithome-ironman-2025"
key = "tarot.json"
test="測試檔案篩選"

def lambda_handler(event, context):

     # 初始化 S3 Service
    s3_service  = S3Service()
    # 取得完整的塔羅牌 ID 清單
    deck = tarot_deck.copy()
    # 從 S3 讀取完整塔羅牌資訊
    info = s3_service.read_s3_file(bucket, key)
    # 為塔羅牌建立索引，方便搜尋
    # read_s3_file() 會回傳 JSON 字串，所以用 json.loads() 把字串轉成 list
    tarot_by_id = {o['id']: o for o in json.loads(info)}
    # 檢查是否 78 張牌都能正確讀取塔羅牌資訊
    missing = [c['id'] for c in tarot_deck if c['id'] not in tarot_by_id]
    if missing:
        raise ValueError(f"找不到塔羅牌: {missing}")
    print(f"驗證通過，共 {len(tarot_deck)} 張牌，每張皆有對應資料")

    # ===== 加入洗牌機制 =====
    deckService = DeckService()
    # 洗牌
    deck = deckService.shuffle(deck)
    # 抽牌
    cards = deckService.draw_card(deck, 3) # 抽隨機三張
    # ===== 取得塔羅牌資訊 =====
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
    print(f"cards_info={cards_info}")

    # ===== 呼叫 Bedrock =====
    system_role = s3_service.read_s3_file(bucket, "system_prompt.txt")
    bedrock_service = BedrockService()
    response = bedrock_service.tarot_reading(system_role, cards_info)
    return response
    

# 洗牌
def shuffle(deck):
    shuffled = deck[:]       
    random.shuffle(shuffled)
    return shuffled

# For Local Test
if __name__ == "__main__":
    """
    本地端測試入口。
    AWS Lambda 會呼叫 lambda_handler，但開發階段可直接執行 main 以測試程式邏輯。
    """

    # 初始化 S3 Service
    s3_service  = S3Service()
    # 取得完整的塔羅牌 ID 清單
    deck = tarot_deck.copy()
    # 從 S3 讀取完整塔羅牌資訊
    info = s3_service.read_s3_file(bucket, key)
    # 為塔羅牌建立索引，方便搜尋
    # read_s3_file() 會回傳 JSON 字串，所以用 json.loads() 把字串轉成 list
    tarot_by_id = {o['id']: o for o in json.loads(info)}
    # 檢查是否 78 張牌都能正確讀取塔羅牌資訊
    missing = [c['id'] for c in tarot_deck if c['id'] not in tarot_by_id]
    if missing:
        raise ValueError(f"找不到塔羅牌: {missing}")
    print(f"驗證通過，共 {len(tarot_deck)} 張牌，每張皆有對應資料")

    # ===== 加入洗牌機制 =====
    deckService = DeckService()
    # 洗牌
    deck = deckService.shuffle(deck)
    # 抽牌
    cards = deckService.draw_card(deck, 3) # 抽隨機三張
    # ===== 取得塔羅牌資訊 =====
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
    print(f"cards_info={cards_info}")

    # ===== 呼叫 Bedrock =====
    system_role = s3_service.read_s3_file(bucket, "system_prompt.txt")
    bedrock_service = BedrockService()
    response = bedrock_service.tarot_reading_local(system_role, cards_info)
    print(f"解讀結果={response}")
    