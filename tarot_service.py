from bedrock_service import BedrockService

class TarotService:
    
    def __init__(self, s3_service, bucket):
        # Service
        self.bedrock_service = BedrockService()
        # 系統提示(daily)
        self.daily_system_role = s3_service.read_s3_file(bucket, "daily_prompt.txt")
        # 系統提示(提問占卜)
        self.system_role = s3_service.read_s3_file(bucket, "system_prompt.txt")
        
    def daily_tarot(self, cards_info):
        # 建構 prompt
        prompt = f"""
        請根據抽到的塔羅牌，為我解讀今日運勢：
        愛情：{cards_info[0]}
        事業：{cards_info[1]}
        財運：{cards_info[2]}
        """
        # 呼叫 Bedrock
        return self.bedrock_service.daily_tarot_reading(self.daily_system_role, prompt)
    
    def question_tarot(self, question, cards_info):
        # 建構 prompt
        prompt = f"""
        請根據抽到的塔羅牌，幫我占卜：{question}
        愛情：{cards_info[0]}
        事業：{cards_info[1]}
        財運：{cards_info[2]}
        """
        # 呼叫 Bedrock
        return self.bedrock_service.daily_tarot_reading(self.system_role, prompt)