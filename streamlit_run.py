import streamlit as st
from revChatGPT.Unofficial import Chatbot
import time 
import json
import re 
import os 
from backend import init,read_text,feed_text_to_chatGPT
from backend import ask

st.title("ChatGPT Text Feeder")
warnings=st.markdown("""
    This site uses the [Reverse engineered ChatGPT API](https://github.com/acheong08/ChatGPT) of acheong08. 
    This site does not record your email and password, 
    and in theory the Reverse engineered ChatGPT API does not record your email and password. 
    However, we do not exclude the possibility that your email and password may be compromised 
    and recommend that you use a separate email and password.
    
    __Use this at your own risk!__

    If the file is too large (maybe >20KB), it is likely to fail
    """)

## pre-learning material 
text_file = st.file_uploader("Upload a text file for ChatGPT to read", type="txt")
if text_file is not None:
    text_list = read_text(text_file)
    chat_title=text_file.name.split(".")[0]
    pre_learning_filename=f"{chat_title}.json"

## login part
# input email and password
col1,col2=st.columns(2)
login={}
login["email"] = col1.text_input("ChatGPT Email")
login["password"] = col2.text_input("ChatGPT Password", type="password")
login["paid"] = st.checkbox("Paid User")
login_button = st.button("Login")
pre_learning_button = st.button("Feed Text and Pre-Learn")
pre_learning_warning = st.markdown("After you click the button, please wait for a while (very slow), the progress bar will show the progress of the text feed. After the progress bar is full, you can click the link below to check the text feeded to the model.")
progress_bar = st.progress(0)
question= st.text_input("Question")
ask_button = st.button("Ask")
answer_text= st.write("")

if login_button and login["email"] != "" and login["password"] != "":
    answer,chatbot=init(login)
    ID = answer['conversation_id']
    chatbot.change_title(id=ID,title=chat_title)

## Pre-learning part 
if 'chatbot' in locals() and pre_learning_button:
    with st.spinner(text=f"ChatGPT: {answer['message']}"):
        summarize_dict=feed_text_to_chatGPT(text_list,chatbot,progress_bar)
        with open(pre_learning_filename,"w") as f:
            json.dump(summarize_dict,f)
    st.success(f"Pre learning Finished!")

# check pre_learning_file exists
if 'chatbot' in locals() and os.path.exists(pre_learning_filename):
    with open(pre_learning_filename) as json_file:
        summarized_data = json.load(json_file)
    
    if ask_button and question != "":
        answer=ask(question,summarized_data,chatbot)
        answer_text.write(answer)

