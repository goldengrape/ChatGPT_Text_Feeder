import streamlit as st
from revChatGPT.Unofficial import Chatbot
import time 

def init(email,password,paid=False):
    print("Initiating chatbot...")
    chatbot = Chatbot(config={"email": email,"password": password,"paid": paid})
    Init_prompt = 'You will read the following content, I will give you what you need to read in several times, each time when you finish reading, you answer and only need to answer "OK", after all of them, I will say "THAT IS ALL", then you should You should return to "ALL received". Here is what I will give you to read.'
    answer=chatbot.ask(Init_prompt,)
    return answer,chatbot

def read_text(text_file,max_length=4096*3):
    text = text_file.getvalue().decode("utf-8")
    text_list = []    
    for i in range(0, len(text), max_length):
        text_list.append(text[i:i+max_length])
    return text_list

def feed_text_to_chatGPT(text_list,chatbot,threshold_time=60):
    err_time=0
    last_time=time.time()
    for i in range(len(text_list)):
        text=text_list[i]
        answer = chatbot.ask(text)
        now_time=time.time()
        if now_time-last_time<threshold_time:
            time.sleep(threshold_time-(now_time-last_time))
        last_time=time.time()    
        persent=i/len(text_list)
        progress_bar.progress(persent)
        # print(f"finished {100*persent:.2f}%")
    answer=chatbot.ask('THAT IS ALL')
    progress_bar.progress(100)
    return answer

st.title("ChatGPT Text Feeder")
st.markdown("This site uses the [Reverse engineered ChatGPT API](https://github.com/acheong08/ChatGPT) of acheong08. This site does not record your email and password, and in theory the Reverse engineered ChatGPT API does not record your email and password. However, we do not exclude the possibility that your email and password may be compromised and recommend that you use a separate email and password.")
st.markdown("__Use this at your own risk!__")
st.write("\n")
st.markdown("If the file is too large (maybe >20KB), it is likely to fail")
text_file = st.file_uploader("Upload a text file for ChatGPT to read", type="txt")
if text_file is not None:
    text_list = read_text(text_file)
    chat_title=text_file.name.split(".")[0]

# input email and password
col1,col2=st.columns(2)
email = col1.text_input("ChatGPT Email")
password = col2.text_input("ChatGPT Password", type="password")
paid = st.checkbox("Paid User")
login_button = st.button("Login & Feed Text")
st.markdown("After you click the button, please wait for a while (very slow), the progress bar will show the progress of the text feed. After the progress bar is full, you can click the link below to check the text feeded to the model.")
progress_bar = st.progress(0)

if login_button and email != "" and password != "":
    answer,chatbot=init(email,password,paid)
    ID = answer['conversation_id']
    chatbot.change_title(id=ID,title=chat_title)

    with st.spinner(text=f"ChatGPT: {answer['message']}"):
        answer=feed_text_to_chatGPT(text_list,chatbot)
    st.success(f"ChatGPT: {answer['message']}")
    st.markdown(f"Please goto [ChatGPT](https://chat.openai.com/chat/{ID}) to check your text feeded model.")
