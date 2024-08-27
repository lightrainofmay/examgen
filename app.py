import time
import streamlit as st
import logging
import httpx
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 获取API密钥和基本URL
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.openai.com/v1")

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义与OpenAI API交互的类
class RateLimitedOpenAIClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.last_request_time = 0

    def call_openai_api(self, messages, model="gpt-3.5-turbo", max_tokens=1000):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < 0.2:  # 1秒最多5次请求
            time.sleep(0.2 - time_since_last_request)

        self.last_request_time = time.time()

        try:
            logger.info(f"发送请求到OpenAI API，消息: {messages}，模型: {model}")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            data = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens
            }
            timeout = httpx.Timeout(60.0, connect=30.0)
            response = httpx.post(f"{self.base_url}/chat/completions", headers=headers, json=data, timeout=timeout)
            response.raise_for_status()
            result = response.json()
            logger.info(f"从OpenAI API接收到的响应: {result}")
            return result
        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTP错误: {exc.response.status_code} - {exc.response.text}")
            return None
        except httpx.RequestError as exc:
            logger.error(f"请求错误: {exc.request.url} - {exc}")
            return None
        except Exception as e:
            logger.error(f"意外错误: {e}")
            return None

# 初始化API客户端
client = RateLimitedOpenAIClient(api_key=OPENAI_API_KEY, base_url=BASE_URL)

# Streamlit应用标题
st.title("智能教学互动问答助手")

# 初始化会话状态中的聊天记录
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 显示聊天记录
for chat in st.session_state.chat_history:
    if chat['role'] == 'user':
        st.markdown(f"**你**: {chat['content']}")
    else:
        st.markdown(f"**AI**: {chat['content']}")

# 用户输入
user_input = st.text_input("输入你的问题：")

if st.button("发送"):
    if user_input:
        # 保存用户的问题到聊天记录
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # 调用OpenAI API生成回复
        messages = st.session_state.chat_history
        response = client.call_openai_api(messages)
        
        if response:
            ai_reply = response['choices'][0]['message']['content']
            # 保存AI的回复到聊天记录
            st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
        else:
            st.error("生成回复时出错")

# 按钮清除聊天记录
if st.button("清除聊天记录"):
    st.session_state.chat_history = []
