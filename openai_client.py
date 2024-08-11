import httpx
import logging
import json
import time

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        logger.info(f"Initialized OpenAIClient with base_url: {self.base_url}")

    def generate_completion(self, messages, model="gpt-3.5-turbo", max_tokens=1000, retries=3):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens
        }
        
        for attempt in range(retries):
            try:
                logger.info(f"Sending request to OpenAI API with messages: {messages} and model: {model}")
                response = httpx.post(f"{self.base_url}/chat/completions", headers=headers, json=data, timeout=10.0)
                response.raise_for_status()  # Raise an exception for HTTP errors
                result = response.json()
                logger.info(f"Received response from OpenAI API: {result}")
                return result
            except httpx.HTTPStatusError as exc:
                logger.error(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
            except httpx.RequestError as exc:
                logger.error(f"Request error occurred: {exc.request.url} - {exc}")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
            
            logger.info(f"Retrying... ({attempt + 1}/{retries})")
            time.sleep(2)  # Wait for 2 seconds before retrying
        
        return None
