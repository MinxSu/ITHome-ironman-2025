import boto3
import json

class BedrockService:

    def tarot_reading(self):
        # session = boto3.Session(profile_name="dev-call-bedrock")

        # print bedrock model
        # client1 = session.client("bedrock", region_name="ap-southeast-1")
        # resp = client1.list_foundation_models()
        # print(json.dumps(resp, indent=2, ensure_ascii=False))

        # call bedrock
        client = boto3.client("bedrock-runtime", region_name="ap-northeast-1")

        # 要提供給模型的角色設定
        system_role = """
        你是一位資深的塔羅占卜師，熟悉大阿爾克納與小阿爾克納的象徵意義，能夠靈活解讀正位與逆位。你的角色不只是解牌，更擅長引導問卜者思考與覺察，讓他們在過程中獲得啟發，而不是單純給出結論。
        占卜時，請展現以下特質：
        專業：解釋每張牌的象徵、故事與潛在意涵，並連結成完整的敘事。
        引導：提出問題、引導問卜者思考，讓他們能從牌義中找到與自身相關的答案。
        同理：以溫柔、理解的語氣，避免過度武斷或消極的解釋。
        啟發：除了描述現況，也要給出正向的建議或未來可能的行動方向。
        """

        prompt = """
        請依據我抽到的牌，為我占卜我的財務運勢：
        ⅩⅪ 審判 Judgement, Upright
        ⅩⅫ 世界 The World, Reversed
        ⅩⅥ 惡魔 The Devil, Upright
        """

        body = {
            "system": system_role,
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }

        response = client.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            body=json.dumps(body)
        )

        # response['body'] 是 StreamingBody，要先讀出來
        output = json.loads(response['body'].read())

        # Claude 的回應位置
        return output['content'][0]['text']
