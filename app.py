import time
import streamlit as st
import logging
import httpx
from dotenv import load_dotenv
import os
from PIL import Image
import io

# 加载环境变量
load_dotenv()

# 从环境变量中获取 API 密钥和 BASE_URL
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.openai.com/v1")

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义一个用于与 OpenAI API 交互的类
class RateLimitedOpenAIClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.last_request_time = 0

    def call_openai_api(self, messages, model="gpt-4o-mini", max_tokens=1000):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < 0.2:  # 1秒内最多5次请求
            time.sleep(0.2 - time_since_last_request)

        self.last_request_time = time.time()

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
            timeout = httpx.Timeout(60.0, connect=30.0)
            response = httpx.post(f"{self.base_url}/chat/completions", headers=headers, json=data, timeout=timeout)
            response.raise_for_status()
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

# 初始化API客户端
client = RateLimitedOpenAIClient(api_key=OPENAI_API_KEY, base_url=BASE_URL)

# Streamlit应用程序标题
st.title("智能互动教学系统")

# 自定义CSS用于美化界面
st.markdown("""
    <style>
    .chat-container {
        max-width: 700px;
        margin: 0 auto;
    }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
        background-color: #ECECEC;
    }
    .user-bubble {
        background-color: #DCF8C6;
        align-self: flex-end;
    }
    .ai-bubble {
        background-color: #ECECEC;
        align-self: flex-start;
    }
    .chat-input {
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
        margin-top: 10px;
    }
    .send-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .upload-button {
        width: 150px;
        margin-top: 10px;
        margin-right: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 初始化会话状态中的聊天记录
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 显示聊天记录
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for chat in st.session_state.chat_history:
    if chat['role'] == 'user':
        st.markdown(f'<div class="chat-bubble user-bubble">你: {chat["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble ai-bubble">AI: {chat["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 用户输入问题
user_input = st.text_input("输入你的问题：", "", key="chat_input")


# 发送按钮
if st.button("发送", key="send_button"):
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
            st.rerun()  # 重新渲染页面以更新聊天记录
        else:
            st.error("生成回复时出错")

# 按钮清除聊天记录
if st.button("清除聊天记录"):
    st.session_state.chat_history = []
    st.rerun()
