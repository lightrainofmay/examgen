import fitz  # PyMuPDF
import nltk

nltk.download('punkt')

def read_pdf(uploaded_file):
    # 使用fitz处理上传的文件
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def tokenize_text(text):
    sentences = nltk.sent_tokenize(text)
    return sentences
