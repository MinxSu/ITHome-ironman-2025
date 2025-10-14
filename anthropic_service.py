import anthropic
import os
import time

model_id = "claude-3-7-sonnet-latest"
# model_id = "claude-3-5-haiku-latest"

class AnthropicService:
    
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ["ANTHROPIC_KEY"]
        )

    def tarot_reading(self, system_role, prompt):
        return self.__tarot_reading(system_role, prompt)
    
    def daily_tarot_reading(self, system_role, prompt):
        return self.__daily_tarot(system_role, prompt)
    

    def __daily_tarot(self, system_role, prompt):
        """
        呼叫AI服務進行每日占卜
        system_role: 要提供給模型的角色設定
        prompt: 要輸入的提示詞
        """
        print("[Anthropic] === Start daily tarot reading ===")
        print(f"Model: {model_id}")
        print(f"max_tokens=800, temperature=0.7")

        t_start = time.perf_counter()
        t_prep = time.perf_counter()

        body = {
            "system": system_role,
            "model": model_id,
            "max_tokens": 800,
            "temperature": 0.7,
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ]
        }

        t_before_invoke = time.perf_counter()
        print(f"[Anthropic] Prepare body: {t_before_invoke - t_prep:.2f}s")

        # === 呼叫 API ===
        message = self.client.messages.create(**body)

        t_after_invoke = time.perf_counter()
        print(f"[Anthropic] Invoke API:   {t_after_invoke - t_before_invoke:.2f}s")

        # === 處理回傳結果 ===
        result = message.content[0].text
        t_end = time.perf_counter()

        print(f"[Anthropic] Parse JSON:  {t_end - t_after_invoke:.2f}s")
        print(f"[Anthropic] Total time:  {t_end - t_start:.2f}s")
        print(f"[Anthropic] Response length: {len(result)} chars")

        return result


    def __tarot_reading(self, system_role, prompt):
        """
        呼叫AI服務
        system_role: 要提供給模型的角色設定
        """
        print("[Anthropic] === Start tarot reading ===")
        print(f"Model: {model_id}")
        print(f"max_tokens=1200, temperature=0.7")

        t_start = time.perf_counter()
        t_prep = time.perf_counter()

        body = {
            "system": system_role,
            "model": model_id,
            "max_tokens": 1200,
            "temperature": 0.7,
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ]
        }

        t_before_invoke = time.perf_counter()
        print(f"[Anthropic] Prepare body: {t_before_invoke - t_prep:.2f}s")

        message = self.client.messages.create(**body)

        t_after_invoke = time.perf_counter()
        print(f"[Anthropic] Invoke API:   {t_after_invoke - t_before_invoke:.2f}s")

        result = message.content[0].text
        t_end = time.perf_counter()

        print(f"[Anthropic] Parse JSON:  {t_end - t_after_invoke:.2f}s")
        print(f"[Anthropic] Total time:  {t_end - t_start:.2f}s")
        print(f"[Anthropic] Response length: {len(result)} chars")

        return result
