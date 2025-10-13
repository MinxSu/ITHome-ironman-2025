import boto3
import json
import time


class BedrockService:
    
    def __init__(self):
        self.client = boto3.client("bedrock-runtime", region_name="ap-northeast-1")

    # 公開方法
    def tarot_reading(self, system_role, prompt):
        return self.__tarot_reading(system_role, prompt)
    
    def daily_tarot_reading(self, system_role, prompt):
        return self.__daily_tarot(system_role, prompt)


    # ===== Daily Tarot =====
    def __daily_tarot(self, system_role, prompt):
        """
        呼叫 Bedrock 服務進行每日占卜
        system_role: 要提供給模型的角色設定
        prompt: 要輸入的提示詞
        """
        model_id = 'arn:aws:bedrock:ap-northeast-1:590184072539:inference-profile/apac.anthropic.claude-3-7-sonnet-20250219-v1:0'
        params = {
            "system": system_role,
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "max_tokens": 1200,
            "temperature": 0.7
        }

        print("\n[Bedrock] === Start daily tarot reading ===")
        print(f"Model: {model_id}")
        print(f"max_tokens={params['max_tokens']}, temperature={params['temperature']}")

        start_all = time.time()

        # Step 1: 準備請求
        t1 = time.time()
        body = json.dumps(params)
        t2 = time.time()

        # Step 2: 呼叫 Bedrock API
        try:
            response = self.client.invoke_model(modelId=model_id, body=body)
        except Exception as e:
            print("[Bedrock] invoke_model failed:", str(e))
            raise
        t3 = time.time()

        # Step 3: 處理回傳結果
        output = json.loads(response['body'].read())
        t4 = time.time()

        result = output['content'][0]['text']
        elapsed_total = round(t4 - start_all, 2)

        # ===== 印出詳細時間 =====
        print(f"[Bedrock] Prepare body: {round(t2 - t1, 2)}s")
        print(f"[Bedrock] Invoke API:   {round(t3 - t2, 2)}s")
        print(f"[Bedrock] Parse JSON:  {round(t4 - t3, 2)}s")
        print(f"[Bedrock] Total time:  {elapsed_total}s")
        print(f"[Bedrock] Response length: {len(result)} chars\n")

        return result


    # ===== General Tarot Reading =====
    def __tarot_reading(self, system_role, prompt):
        """
        呼叫 Bedrock 服務
        system_role: 要提供給模型的角色設定
        """
        model_id = 'arn:aws:bedrock:ap-northeast-1:590184072539:inference-profile/apac.anthropic.claude-3-7-sonnet-20250219-v1:0'
        params = {
            "system": system_role,
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }

        print("\n[Bedrock] === Start tarot reading ===")
        print(f"Model: {model_id}")
        print(f"max_tokens={params['max_tokens']}, temperature={params['temperature']}")

        start_all = time.time()

        # Step 1: 準備請求
        t1 = time.time()
        body = json.dumps(params)
        t2 = time.time()

        # Step 2: 呼叫 Bedrock API
        try:
            response = self.client.invoke_model(modelId=model_id, body=body)
        except Exception as e:
            print("[Bedrock] invoke_model failed:", str(e))
            raise
        t3 = time.time()

        # Step 3: 處理回傳結果
        output = json.loads(response['body'].read())
        t4 = time.time()

        result = output['content'][0]['text']
        elapsed_total = round(t4 - start_all, 2)

        # ===== 印出詳細時間 =====
        print(f"[Bedrock] Prepare body: {round(t2 - t1, 2)}s")
        print(f"[Bedrock] Invoke API:   {round(t3 - t2, 2)}s")
        print(f"[Bedrock] Parse JSON:  {round(t4 - t3, 2)}s")
        print(f"[Bedrock] Total time:  {elapsed_total}s")
        print(f"[Bedrock] Response length: {len(result)} chars\n")

        return result
