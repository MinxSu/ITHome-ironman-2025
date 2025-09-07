import random

from bedrock_service import BedrockService 

def lambda_handler(event, context):
    print("測試程式更新。")
    cards = []
    while len(cards) < 3:
        card = draw_card()
        if not card in cards:
            cards.append((card, position()))
    bedrock = BedrockService()
    response = bedrock.tarot_reading()

    return {
        'statusCode': 200,
        'body': response
    }

# 22張大阿爾克納牌
major_arcana = [
  "Ⅰ 愚者 — The Fool",
  "Ⅱ 魔術師 — The Magician",
  "Ⅲ 女祭司 — The High Priestess",
  "Ⅳ 皇后 — The Empress",
  "Ⅴ 皇帝 — The Emperor",
  "Ⅵ 教宗 — The Hierophant",
  "Ⅶ 戀人 — The Lovers",
  "Ⅷ 戰車 — The Chariot",
  "Ⅸ 力量 — Strength",
  "Ⅹ 隱者 — The Hermit",
  "Ⅺ 命運之輪 — Wheel of Fortune",
  "Ⅻ 正義 — Justice",
  "ⅩⅢ 吊人 — The Hanged Man",
  "ⅩⅣ 死神 — Death",
  "ⅩⅤ 節制 — Temperance",
  "ⅩⅥ 惡魔 — The Devil",
  "ⅩⅦ 高塔 — The Tower",
  "ⅩⅧ 星星 — The Star",
  "ⅩⅨ 月亮 — The Moon",
  "ⅩⅩ 太陽 — The Sun",
  "ⅩⅪ 審判 — Judgement",
  "ⅩⅫ 世界 — The World"
]

def draw_card():
    return random.choice(major_arcana)

def position():
    return random.choice(['Upright', 'Reversed'])