import os

from dotenv import load_dotenv
import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

load_dotenv()

# APIキーの設定
openai.api_key = os.environ["OPENAI_API_KEY"]

st.title("StreamlitのChatGPTサンプル")

# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"


def response_chatgpt(
    user_msg: str,
):
    """ChatGPTのレスポンスを取得

    Args:
        user_msg (str): ユーザーメッセージ。
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_msg},
        ],
        stream=True,
    )
    return response


# チャットログを保存したセッション情報を初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []


user_msg = st.chat_input("ここにメッセージを入力")
if user_msg:
    # 以前のチャットログを表示
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])

    # 最新のメッセージを表示
    with st.chat_message(USER_NAME):
        st.write(user_msg)

    # アシスタントのメッセージを表示
    response = response_chatgpt(user_msg)
    with st.chat_message(ASSISTANT_NAME):
        assistant_msg = ""
        assistant_response_area = st.empty()
        for chunk in response:
            # 回答を逐次表示
            tmp_assistant_msg = chunk["choices"][0]["delta"].get("content", "")
            assistant_msg += tmp_assistant_msg
            assistant_response_area.write(assistant_msg)

    # セッションにチャットログを追加
    st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})
