import boto3
import json

class BedrockService:
    
    def __init__(self):
        self.client = boto3.client("bedrock-runtime", region_name="ap-northeast-1")

    def tarot_reading(self, system_role, prompt):
        return self.__tarot_reading(system_role, prompt)
    
    def daily_tarot_reading(self, system_role, prompt):
        return self.__daily_tarot(system_role, prompt)
    
    def __daily_tarot(self, system_role, prompt):
        """
        呼叫 Bedrock 服務進行每日占卜
        system_role: 要提供給模型的角色設定
        prompt: 要輸入的提示詞
        """

        body = {
            "system": system_role,
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "max_tokens": 1200,
            "temperature": 0.7
        }

        response = self.client.invoke_model(
            modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
            body=json.dumps(body)
        )

        output = json.loads(response['body'].read())
        return output['content'][0]['text']


    def __tarot_reading(self, system_role, prompt):
        """
        呼叫 Bedrock 服務
        system_role: 要提供給模型的角色設定
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

        response = self.client.invoke_model(
            modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
            body=json.dumps(body)
        )

        output = json.loads(response['body'].read())
        return output['content'][0]['text']