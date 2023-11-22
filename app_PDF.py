import os

from dotenv import load_dotenv
import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate


load_dotenv()

# APIキーの設定
openai.api_key = os.environ["OPENAI_API_KEY"]
#FAISS_DB_DIR = os.environ["FAISS_DB_DIR"]

st.set_page_config(page_title="TokAI 2.0",
                       page_icon="🤖")
st.title("TokAI2.0 🤖")

# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"

user_msg = st.chat_input("ここにメッセージを入力")

### FAISS vectorのロード
vectoreStore = FAISS.load_local("faiss_index/", OpenAIEmbeddings())
## Retriever
retriever = vectoreStore.as_retriever(search_type="similarity", search_kwargs={"k":3})

### プロンプト(Q&A)
qa = RetrievalQA.from_chain_type(
  llm=ChatOpenAI(
    temperature=0.9, 
    model_name="gpt-3.5-turbo-16k", 
    streaming=True,
  ), 
  chain_type="stuff", 
  retriever=retriever, 
  return_source_documents=False
)
query = f"あなたは東海大学情報理工学部についての質問に答えるアシスタントです。次の質問に答えてください。:{user_msg}"

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
        st.markdown(response)

    # セッションにチャットログを追加
    st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": response})
