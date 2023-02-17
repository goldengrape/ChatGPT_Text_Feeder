import streamlit as st
from revChatGPT.Unofficial import Chatbot
import time 
import json
import re 
import os 

def create_chatbot(login):
    chatbot = Chatbot(
        config={"email": login["email"],
                "password": login["password"],
                "paid": login["paid"]}
    )
    return chatbot

def init(login):
    print("Initiating chatbot...")
    chatbot = create_chatbot(login)
    Init_prompt = 'You will read the following content, I will give you what you need to read.'
    answer=chatbot.ask(Init_prompt,)
    return answer,chatbot

def read_text(text_file,max_length=4096*3):
    text = text_file.getvalue().decode("utf-8")
    text_list = []    
    # 步长设定成max_length的一半
    # 产生内容的重叠, 以防止内容的断裂
    for i in range(0, len(text), int(max_length/2) ):
        text_list.append(text[i:i+max_length])
    return text_list

def feed_text_to_chatGPT(text_list,chatbot,progress_bar, threshold_time=60,summarize_length=100):
    err_time=0
    last_time=time.time()
    prompt=f"Summarize the following content in {summarize_length} words.\n\n"
    summarize_dict={}
    for i in range(len(text_list)):
        text=text_list[i]
        answer = chatbot.ask(prompt+text)
        summarize_dict[i]={"text":text,"summarize":answer['message']}
        now_time=time.time()
        if now_time-last_time<threshold_time:
            time.sleep(threshold_time-(now_time-last_time))
        last_time=time.time()    
        persent=i/len(text_list)
        progress_bar.progress(persent)
        print(f"finished {100*persent:.2f}%")
    answer=chatbot.ask('THAT IS ALL')
    progress_bar.progress(100)
    return summarize_dict

def index_question(question, data):
    summarize_list=""
    for i in range(len(data)):
        summarize_list+=f"{i}: { data[str(i)]['summarize'] }\n\n"
    prompt="I have the following question:\n"
    prompt+=f"\"{question}\"\n" 
    prompt+="Estimate which materials are needed based on my question, and these materials may appear in which corresponding paragraphs of the following abstracts. please sort the number of these summaries according to the likelihood of finding the answer, from most likely to least likely, for example, the most likely answer is the 0th summary, followed by the 2nd paragraph, followed by the 4th paragraph, then return [0,2,4...]"
    prompt+="\nNote that the paragraph content may be long and the abstract may be brief in its response to the paragraph content. The answers to the questions must appear in the paragraphs corresponding to the following summaries."
    prompt+="\nIf the answer is not possible in each summarize, then return all the numbers of the summaries in []"
    prompt+="\nHere are the summaries:\n\n"
    prompt+=summarize_list
    return prompt
    
def question_in_each_paragraph(question, para_id, data):
    prompt=""
    prompt+="read the following paragraph and answer the question:\n"
    prompt+=f"\"{question}\"\n"
    prompt+="\n"
    prompt+=f"\"{data[str(para_id)]['text']}\"\n"
    return prompt
def summarize_all_answer(question, answers):
    prompt=""
    prompt+="I have the following question:\n"
    prompt+=f"\"{question}\"\n"
    prompt+="\n"
    prompt+="Here is the information you have already found:\n"
    for i in range(len(answers)):
        prompt+=f"\"{answers[i]}\"\n"
    prompt+="\n"
    prompt+="The above information is given according to some paragraphs of the whole text, each information may not be complete, please summarize the above information and give the answer to the question."
    return prompt

def ask(question,summarized_data,chatbot):
    index_prompt=index_question(question, summarized_data)
    para_id_list_answer=chatbot.ask(index_prompt)["message"]
    # print("ID answers:", para_id_list_answer)
    para_id_list_answer=re.findall(r'\d+', para_id_list_answer)
    para_id_list=[int(i) for i in para_id_list_answer]
    para_id_list = summarized_data.keys() if len(para_id_list)==0 else para_id_list


    answers=[]
    for para_id in para_id_list:
        each_para_question=question_in_each_paragraph(question, para_id, summarized_data)
        answer=chatbot.ask(each_para_question)["message"]
        # print(para_id, "answer:", answer)
        answers.append(answer)

    final_question=summarize_all_answer(question, answers)
    final_answer=chatbot.ask(final_question)["message"]
    return final_answer