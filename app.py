import streamlit as st
import logging
import chardet  # 新增这个库来检测文件编码
from file_reader import read_pdf, tokenize_text
from question_generator import generate_multiple_choice_questions, generate_fill_in_the_blank_questions, generate_essay_questions
from config import OPENAI_API_KEY, BASE_URL

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.title("自动出题机器人")

# 文件上传组件
uploaded_file = st.file_uploader("上传PDF或TXT文件", type=["pdf", "txt"])

def read_txt(file):
    rawdata = file.read()
    result = chardet.detect(rawdata)
    charenc = result['encoding']
    text = rawdata.decode(charenc)
    return text

if uploaded_file is not None:
    st.write("文件已上传")
    file_type = uploaded_file.name.split('.')[-1]

    if file_type == 'pdf':
        text = read_pdf(uploaded_file)
    elif file_type == 'txt':
        text = read_txt(uploaded_file)
    else:
        st.error("不支持的文件类型。请上传PDF或TXT文件。")
        text = ""

    if text:
        st.subheader("文件内容")
        st.write(text[:500])  # 显示文件的前500个字符
        sentences = tokenize_text(text)
    else:
        st.write("未能读取文件内容。")
        sentences = []

    if sentences:
        st.subheader("生成的试题")

        if st.button("生成选择题"):
            try:
                response = generate_multiple_choice_questions(" ".join(sentences))
                if response:
                    st.write(response)
                else:
                    st.error("生成选择题时出错")
            except Exception as e:
                logger.error(f"Error generating multiple choice questions: {e}")
                st.error(f"生成选择题时出错: {e}")

        if st.button("生成填空题"):
            try:
                response = generate_fill_in_the_blank_questions(" ".join(sentences))
                if response:
                    st.write(response)
                else:
                    st.error("生成填空题时出错")
            except Exception as e:
                logger.error(f"Error generating fill in the blank questions: {e}")
                st.error(f"生成填空题时出错: {e}")

        if st.button("生成问答题"):
            try:
                response = generate_essay_questions(" ".join(sentences))
                if response:
                    st.write(response)
                else:
                    st.error("生成问答题时出错")
            except Exception as e:
                logger.error(f"Error generating essay questions: {e}")
                st.error(f"生成问答题时出错: {e}")

        if st.button("一键生成所有试题"):
            try:
                # 生成填空题
                st.write("生成填空题中...")
                fill_in_the_blank_response = generate_fill_in_the_blank_questions(" ".join(sentences))
                if fill_in_the_blank_response:
                    st.write("填空题:")
                    st.write(fill_in_the_blank_response)
                else:
                    st.error("生成填空题时出错")

                # 生成选择题
                st.write("生成选择题中...")
                multiple_choice_response = generate_multiple_choice_questions(" ".join(sentences))
                if multiple_choice_response:
                    st.write("选择题:")
                    st.write(multiple_choice_response)
                else:
                    st.error("生成选择题时出错")

                # 生成问答题
                st.write("生成问答题中...")
                essay_response = generate_essay_questions(" ".join(sentences))
                if essay_response:
                    st.write("问答题:")
                    st.write(essay_response)
                else:
                    st.error("生成问答题时出错")
            except Exception as e:
                logger.error(f"Error generating questions: {e}")
                st.error(f"生成试题时出错: {e}")

# 添加一个按钮来测试 API 连接
if st.button("测试 API 连接"):
    test_openai_api()
