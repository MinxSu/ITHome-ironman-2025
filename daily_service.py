import json

from bedrock_service import BedrockService
from deck import DeckService
from s3_service import S3Service
from cards import tarot_deck

class DailyService:
    
    def __init__(self, bucket, key):
        # Service
        s3_service  = S3Service()
        self.deckService = DeckService()
        self.bedrock_service = BedrockService()
        # 塔羅牌
        self.deck = tarot_deck.copy()
        info = s3_service.read_s3_file(bucket, key)
        self.tarot_by_id = {o['id']: o for o in json.loads(info)}
        # 系統提示
        self.system_role = s3_service.read_s3_file(bucket, "daily_prompt.txt")
        
    def daily_tarot(self):
        self.deck = self.deckService.shuffle(self.deck)
        cards = self.deckService.draw_card(self.deck, 3) # 抽隨機三張
        # ===== 取得塔羅牌資訊 =====
        cards_info = self.__get_tarot_infos(cards)
        # 建構 prompt
        prompt = f"""
        請根據抽到的塔羅牌，為我解讀今日運勢：
        愛情：{cards_info[0]}
        事業：{cards_info[1]}
        財運：{cards_info[2]}
        """
        # 呼叫 Bedrock
        return self.bedrock_service.daily_tarot_reading(self.system_role, prompt)

    
    
    def __get_tarot_infos(self, cards):
        card_info = []
        for i in range(3):
            card_info = self.tarot_by_id.get(cards[i]['id'])
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

            card_info.append(card)
        return card_info