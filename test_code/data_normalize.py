#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import os
# national langeuage tool-kit
# nltk : 자연어 처리를 위한 파이썬 라이브러리
import nltk #check 2022-02-08
from konlpy.tag import Okt #checking
import numpy as np #check 2022-02-08
#import matplotlib.pyplot as plt
#from PIL import Image
#from wordcloud import WordCloud
#from wordcloud import ImageColorGenerator

# #폴더 생성
# def createFolder(directory):
#     try:
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#     except OSError:
#         print ('Error: Creating directory. ' +  directory)
        
#긍정 = 1, 부정 = 0
def get_lable(v):
    if v > 0 :
        lable = 1
    else:
        lable = 0
    return lable

#1차적 전처리(유효데이터 필터)
def Data_Prepro(data):
    if data.size > 0 :
        #print("if")
        df_sample = data.loc[:,['기사 주제','기사 제목','기사 내용','좋아요','훈훈해요','슬퍼요','화나요','기대 돼요']]

        #total, score 컬럼 추가
        df_sample['total'] = df_sample['좋아요'] + df_sample['훈훈해요'] + df_sample['슬퍼요'] + df_sample['화나요'] + df_sample['기대 돼요'] 

        df_sample['score'] = df_sample['좋아요'] + df_sample['훈훈해요'] - df_sample['슬퍼요'] - df_sample['화나요']

        """아래의 조건 순서대로 실행 
        1.total(총 반응수)가 10이하인 row 제거
        1)슬퍼요 + 화나요의 합이 0인경우 거르기 (0으로 나누는 경우의 수를 제거하기 위함)
        2)(좋아요+훈훈해요)/(슬퍼요+화나요)의 결과가 1인 경우 거르기

        1-1)좋아요+훈훈해요의 합이 0인경우 거르기 (0으로 나누는 경우의 수를 제거하기 위함)
        1-2)(슬퍼요+화나요)/(좋아요+훈훈해요)의 결과가 1인 경우 거르기

        2.두 데이터 합치고, 중복 제거
        """

        #1.total(총 반응수)가 10이하인 row 제거
        indexNames = df_sample[ (df_sample['total'] < 10) ].index
        df_drop = df_sample.drop(indexNames)
        #결측값(=none,null) 제거
        df_drop = df_drop.dropna(axis=0)


        #1)슬퍼요 + 화나요의 합이 0인경우 거르기 (0으로 나누는 경우의 수를 제거하기 위함)
        indexNames1_1 = df_drop[ (df_drop['슬퍼요'] + df_drop['화나요'] == 0) ].index
        df_drop1_1 = df_drop.drop(indexNames1_1)
        #display(df_drop1_1)

        #2)(좋아요+훈훈해요)/(슬퍼요+화나요)의 결과가 1인 경우 거르기
        indexNames1_2 = df_drop1_1[ ((df_drop1_1['좋아요'] + df_drop1_1['훈훈해요']) / (df_drop1_1['슬퍼요'] + df_drop1_1['화나요']) == 1) ].index
        df_drop1_2 = df_drop1_1.drop(indexNames1_2)
        #display(df_drop1_2)

        #1-1)좋아요+훈훈해요의 합이 0인경우 거르기 (0으로 나누는 경우의 수를 제거하기 위함)
        indexNames2_1 = df_drop[ (df_drop['좋아요'] + df_drop['훈훈해요'] == 0) ].index
        df_drop2_1 = df_drop.drop(indexNames2_1)
        #display(df_drop2_1)

        #1-2)(슬퍼요+화나요)/(좋아요+훈훈해요)의 결과가 1인 경우 거르기
        indexNames2_2 = df_drop2_1[ ((df_drop2_1['슬퍼요'] + df_drop2_1['화나요']) / (df_drop2_1['좋아요'] + df_drop2_1['훈훈해요']) == 1) ].index
        df_drop2_2 = df_drop2_1.drop(indexNames2_2)
        #display(df_drop2_2)

        #2.두 데이터 합치고, 중복 제거
        result1 = pd.concat([df_drop1_2,df_drop2_2])
        result_len1 = len(result1)
        #print(result_len1)
        result2 = result1.drop_duplicates(['기사 제목', '기사 내용']) # 중복된 값이 있는 행 삭제
        result3 = result2.reset_index(drop=True) #index reset
        data = result3
    
    else :
        data = "측정가능한 데이터가 존재하지 않습니다" 
        print(data)
        
    return data

#긍부정 lable 추가, score 절대값으로 치환
def add_lable(data):
    #긍부정 lable 추가
    data['lable'] = data['score'].apply(lambda v: get_lable(v))

    #score 절대값으로 치환
    data['score'] = data['score'].abs()
    
    return data

def Cnt_Good_Bad(data) : 
    #lable이 1이면 긍정(True), 0이면 부정(False)으로 카운팅
    counterFunc = data['lable'].apply(
        lambda x: True if x == 1 else False)
    numOfRows_Good = len(counterFunc[counterFunc == True].index)
    numOfRows_Bad = len(counterFunc[counterFunc == False].index)
    #print('긍정row count:', numOfRows_Good)
    #print('부정row count:', numOfRows_Bad)

def data_Good(data) :
    #긍정 데이터만 추출
    data_Good = data[data['lable'] == 1]
    data_Good = data_Good.reset_index(drop=True) #index reset
    #data_Good.to_excel('data_Good.xlsx')
    return data_Good

def data_Bad(data) :
    #부정 데이터만 추출
    data_Bad = data[data['lable'] == 0]
    data_Bad = data_Bad.reset_index(drop=True) #index reset
    #data_Bad.to_excel('data_Bad.xlsx')
    return data_Bad

#불용어 리스트화
def stop_word(stop_file_name) :
    with open(stop_file_name, 'r', encoding='UTF8') as f:
        list_stopwords = []
        for line in f:
            list_stopwords.append(line)

    # stopword도 파일로 만들어 두는게 제일 좋다
    stop_words = [l.strip() for l in list_stopwords]

    #중복제거를 위해 dict화 하였다가 다시 list로 변경
    sw_to_dict = dict.fromkeys(stop_words) # 리스트 값들을 key 로 변경  
    stop_words = list(sw_to_dict) # list(dict.fromkeys(arr)) 
    #print("#불용어리스트최종출력")
    #print(stop_words)
    
    return stop_words


def data_token(list_tit) : 
    okt = Okt()
    # 명사만 추출
    #list_title = list_tit.values.tolist()
    list_title = list_tit
    token_news = okt.nouns("테스트용 문장.")

    #리스트를 요소별로 가져와서 명사만 추출한 후 리스트로 저장
    data_word=[]
    for i in range(len(list_title)):
        try:
            data_word.append(okt.nouns(list_title[i]))
        except Exception as e:
            continue

    #명사만 추출해서 만든 리스트
    #print(data_word)

    #리스트를 token_news에 담음
    token_news = data_word
    return token_news

#필터링 함수 
#원래는 한글자인건 보통 읽기 힘들어서 제외하는데, 한글자인거 한번 필터링 걸치기 전에 이렇게 합칠 수 있는 
#단어는 합치기 위해서 다소 불편하지만 이렇게 진행. 왜냐면 두글자 두글자를 합칠 경우도 있으니까! 
#nomalization이후에! 한글자인거 한 번 더 필터링함. 그래야 에러 안날듯 
#추후 del_text가 필요 없이 단어를 치환해야하는 경우가 온다면 메소드 추가(del_text관련만 제외하면 됨)
def nomalizantion_nouns(list_name, del_text, non_word, nom_text):
    for i in list_name:
        if (i == non_word):
            list_name[list_name.index(non_word)] = nom_text
            while del_text in list_name:    
                list_name.remove(del_text) 
            #print("#")

#한글자 제거 함수            
def check_text(list_name):
    for i, data in enumerate(list_name[:]): 
        if len(data) == 1:
            #print(data)  #한글자 인쇄 
            list_name.remove(data)
            #print(list_name)
        else :
            len(data)


def sw(token_news,list_name) : 
    # 불용어 처리
    token_news_sw = [word for word in token_news if word not in list_name]
    return token_news_sw

def data_nltk_ko(to_news) : 
    # nltk 객체 생성
    ko = nltk.Text(tokens=to_news)
    #print(ko)            #  타입 : Text
    #print(ko.vocab())          #  타입 : FreqDict (빈도수를 저장하고 있는 사전)

    # most_common(10) : 빈도수 상위 10개를 추린다
    #print(ko.vocab().most_common(10))       # 타입 : 리스트

    # 빈도수 상위 500개를 리스트에 담는다 
    data_dict = ko.vocab().most_common(500)

    # ※ 리스트를 사전 형태로 만든다
    tmp_dict = dict(data_dict)
    #print(tmp_dict)
    
    return tmp_dict


# #word_cloud : color&font&size
# def color_func(word, font_size, position,orientation,random_state=None, **kwargs):
#     return("hsl({:d},{:d}%, {:d}%)".format(np.random.randint(212,313),np.random.randint(26,32),np.random.randint(45,80)))

# #word_cloud
# def word_cloud(data,dir) : 
#     lightwordcloud = WordCloud(background_color='white', 
#                           width=480, height=480,
#                           font_path ='NanumBarunGothic.ttf',
#                          color_func = color_func).generate_from_frequencies(data)

#     plt.imshow(lightwordcloud)
#     plt.axis("off")
#     plt.savefig(dir + 'WordCloud_News.png')
#     print('-finished-')