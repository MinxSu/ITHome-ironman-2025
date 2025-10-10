import boto3
import json

class BedrockService:

    def tarot_reading_local(self, system_role, cards):
        session = boto3.Session(profile_name="dev-call-bedrock")
        client = session.client("bedrock-runtime", region_name="ap-northeast-1")
        return self.__tarot_reading(client, system_role, cards)

    def tarot_reading(self, system_role, cards):
        client = boto3.client("bedrock-runtime", region_name="ap-northeast-1")
        return self.__tarot_reading(client, system_role, cards)

    def __tarot_reading(self, client, system_role, cards):
        """
        從本地端呼叫 Bedrock 服務
        system_role: 要提供給模型的角色設定
        """

        prompt = f"""
        請根據抽到的塔羅牌，解讀近三個月的財務運勢。
        {cards}
        """
        print(prompt)

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
            modelId="arn:aws:bedrock:ap-northeast-1:590184072539:inference-profile/apac.anthropic.claude-3-7-sonnet-20250219-v1:0",
            body=json.dumps(body)
        )

        output = json.loads(response['body'].read())
        return output['content'][0]['text']