import httpx
import logging
from config import OPENAI_API_KEY, BASE_URL

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self, api_key=OPENAI_API_KEY, base_url=BASE_URL):
        self.api_key = api_key
        self.base_url = base_url

    def generate_completion(self, messages, model="gpt-3.5-turbo", max_tokens=1000):
        try:
            logger.info(f"Sending request to OpenAI API with messages: {messages} and model: {model}")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            data = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens
            }
            response = httpx.post(f"{self.base_url}/chat/completions", headers=headers, json=data)
            response.raise_for_status()  # 如果返回了 HTTP 错误代码，抛出异常
            result = response.json()
            logger.info(f"Received response from OpenAI API: {result}")
            return result
        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
            return None
        except httpx.RequestError as exc:
            logger.error(f"Request error occurred: {exc.request.url} - {exc}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return None

# 测试生成文本的功能
if __name__ == "__main__":
    client = OpenAIClient()  # 使用从 config.py 导入的默认 API key 和 Base URL
    response = client.generate_completion(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say this is a test"}
        ],
        model="gpt-3.5-turbo",
        max_tokens=50
    )

    if response:
        print(response['choices'][0]['message']['content'])
    else:
        print("Failed to generate completion.")
