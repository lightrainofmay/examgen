from openai import OpenAI
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate_completion(self, messages, model="gpt-3.5-turbo", max_tokens=1000):
        try:
            logger.info(f"Sending request to OpenAI API with messages: {messages} and model: {model}")
            response = self.client.chat.completions.create(
                messages=messages,
                model=model,
                max_tokens=max_tokens
            )
            logger.info(f"Received response from OpenAI API: {response}")
            return response
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return N
        
    generate_completion(self , messages="Hello", model="gpt-3.5-turbo", max_tokens=1000)