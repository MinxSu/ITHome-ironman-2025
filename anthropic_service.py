import anthropic
import os

class AnthropicService:
    
    def __init__(self):
        api_key = os.environ["ANTHROPIC_KEY"]
        self.client = anthropic.Anthropic(
            api_key=api_key
        )

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

        message = self.client.messages.create(
            system = system_role,
            model="claude-3-5-sonnet-20241022",
            max_tokens=1200,
            temperature=0.7,
            messages=[
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ]
        )
        return message.content[0].text


    def __tarot_reading(self, system_role, prompt):
        """
        呼叫 Bedrock 服務
        system_role: 要提供給模型的角色設定
        """

        message = self.client.messages.create(
            system = system_role,
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ]
        )
        return message.content[0].text