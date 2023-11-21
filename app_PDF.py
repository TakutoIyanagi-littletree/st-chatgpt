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
#FAISS_DB_DIR = os.environ["FAISS_DB_DIR"]

st.title("StreamlitのChatGPTサンプル")

# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"

user_msg = st.chat_input("ここにメッセージを入力")

model = ChatOpenAI(model="gpt-3.5-turbo-16k-0613", temperature=0.9, client=openai.ChatCompletion)
faiss_db = FAISS.load_local("faiss_index/", embeddings=OpenAIEmbeddings(client=openai.ChatCompletion))

# LLMによる回答の生成
qa = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=faiss_db.as_retriever())
query = f"あなたはHakkyについての質問に答えるChatBotです。次の質問に答えてください。:{user_msg}"

# チャットログを保存したセッション情報を初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if user_msg:
    # 以前のチャットログを表示
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])

    # 最新のメッセージを表示
    with st.chat_message(USER_NAME):
        st.write(user_msg)
  
    # アシスタントのメッセージを表示
    response = qa.run(query)
    with st.chat_message(ASSISTANT_NAME):
        st.write(user_msg)
        '''assistant_msg = ""
        assistant_response_area = st.empty()
        for chunk in response:
            # 回答を逐次表示
            tmp_assistant_msg = chunk["choices"][0]["delta"].get("content", "")
            assistant_msg += tmp_assistant_msg
            assistant_response_area.write(assistant_msg)'''

    # セッションにチャットログを追加
    st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})
