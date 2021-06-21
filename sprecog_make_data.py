#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 14:57:02 2020

@author: chenjunze
"""

import speech_recognition as sr
import pyaudio
import numpy as np


def Voice_To_Text():
    final_text = ['[CLS]']
    r = sr.Recognizer()
    with sr.Microphone() as source: 
        print("請開始說話:")                     # print 一個提示 提醒你可以講話了
        r.adjust_for_ambient_noise(source)     # 函數調整麥克風的噪音:
        audio = r.listen(source)
    try:
        Text = r.recognize_google(audio, language="zh-TW")
    except sr.UnknownValueError:
        Text = "無法翻譯"
    except sr.RequestError as e:
        Text = "無法翻譯{0}".format(e)
    
    final_text.extend(list(Text))  #output sentence list
    
    return final_text

def output_file(file_name, text_all, BIO_all):
    f = open(file_name,'w')
    for i in range(len(text_all)):
        for j in range(len(text_all[i])):
            f.write(text_all[i][j]+' '+str(BIO_all[i][j])+'\n')
        f.write('\n')
    f.close
    
def formatoutput(final_text):
    BIO_format = list('O'*len(final_text)) #load sentence list
   #check list
    dict_tmp ={}
    for i in range(len(final_text)):
        dict_tmp[i] = final_text[i]
    print(dict_tmp)
    
    m = input('get(0) or spend(1) money:')
    B_item = input('B-item location:')
    I_item = input('I-item end location:')
    B_money = input('B-money location:')
    I_money = input('I-money end location:')
    
    BIO_format[0] = int(m)
    BIO_format[int(B_item)] = 'B-item'
    BIO_format[int(B_item)+1 : int(I_item)+1] = ['I-item' for i in range(int(I_item) - int(B_item))]
    BIO_format[int(B_money)] = 'B-money'
    BIO_format[int(B_money)+1 : int(I_money)+1] = ['I-money' for i in range(int(I_money) - int(B_money))]
    
    return BIO_format

# make data
data_number = 24
Text_all = []
BIO_all = []
for i in range(data_number):
    c = input(str(i+1)+'th time, if ready enter any word:')

    Text = Voice_To_Text()
    print(Text)
    c = input('is this sentence correct?(y or n)')
    while c =='n':
        Text = Voice_To_Text()
        print(Text)
        c = input('is this sentence correct?(y or n)')
    Text_all.append(Text)
    
    BIO_Text = formatoutput(Text)
    BIO_all.append(BIO_Text)
    
file = 'speech_output_expense_tmp.txt'
output_file(file,Text_all,BIO_all)




