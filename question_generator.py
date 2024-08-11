from openai_client import OpenAIClient
from config import OPENAI_API_KEY, BASE_URL
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 设置 API 密钥和基础 URL
client = OpenAIClient(api_key=OPENAI_API_KEY, base_url=BASE_URL)

def generate_questions(messages, model="gpt-3.5-turbo", max_tokens=500):
    response = client.generate_completion(messages, model=model, max_tokens=max_tokens)
    if response:
        logger.info(f"Generated questions: {response}")
        choices = response.get('choices', [])
        if choices:
            questions = choices[0].get('message', {}).get('content', '')
            return questions
    logger.error("Failed to generate questions from OpenAI API")
    return None

def generate_multiple_choice_questions(text):
    messages = [
        {"role": "system", "content": "你是一个生成多项选择题的专家。"},
        {"role": "user", "content": f"请根据以下文本生成5道多项选择题，内容应为中文：\n\n{text}"}
    ]
    return generate_questions(messages)

def generate_fill_in_the_blank_questions(text):
    messages = [
        {"role": "system", "content": "你是一个生成填空题的专家。"},
        {"role": "user", "content": f"请根据以下文本生成5道填空题，内容应为中文：\n\n{text}"}
    ]
    return generate_questions(messages)

def generate_essay_questions(text):
    messages = [
        {"role": "system", "content": "你是一个生成问答题的专家。"},
        {"role": "user", "content": f"请根据以下文本生成5道问答题，内容应为中文：\n\n{text}"}
    ]
    return generate_questions(messages)

def generate_and_evaluate_questions(text, number, subject, tone, response_json):
    messages = [
        {"role": "system", "content": f"你是一个{subject}领域的生成问题的专家。"},
        {"role": "user", "content": f"请根据以下文本生成{number}道{tone}问题，内容应为中文：\n\n{text}"}
    ]
    questions = generate_questions(messages)
    if questions:
        return questions, "Evaluation not implemented"
    return None, None
