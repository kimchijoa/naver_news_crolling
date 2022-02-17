import data_normalize as nmo
import time
from datetime import date, datetime
import sys
sys.path.append("/naver_news_crolling/func/")
import mysql_conn as m_mysql
import pymysql as mysql
#시간 재는거 start : 시작 / end : 종료

def nmo_run(date) :
    file_name = "../naver_news_crolling/news_data/news_data_" + date + "/total_news_data_" + date + ".xlsx"
    data = nmo.pd.read_excel(file_name)
    data_Pre = nmo.Data_Prepro(data)
    # #긍부정 레이블 추가 및 절대값 치환 
    data_Pre_lable = nmo.add_lable(data_Pre)
    #긍부정 row count 함수 
    json_category_per_emotion = nmo.data_emotion_per_category(data_Pre_lable)
    #워드 클라우드용으로 제목만 뽑아냄
    result_Title = data_Pre_lable['기사 제목']
    #워드 클라우드 결과값 매칭을 위한 주제도 뽑아냄
    result_Tag = data_Pre_lable['기사 주제']
    #제목 리스트들을 카테고리 별로 분리한다.
    #c_dic_arr_word에는 사회일반, 경제일반, 사건사고, 정치일반 태그를 가진 기사 제목들이 각 위치에 리스트 형태로 저장된다.
    dic_arr = []
    c_dic_arr_word = [[],[],[],[]]
    c_dic_arr = ["사회일반","경제일반","사건사고","정치일반"]
    for i in range(0, len(result_Title)):
        dic_arr.append({"Category":result_Tag[i].replace(" ","") , "Title":result_Title[i]})
    
    for i in range(0, len(dic_arr)):
            if dic_arr[i]["Category"] == c_dic_arr[0]:
                c_dic_arr_word[0].append(dic_arr[i]["Title"])
            elif dic_arr[i]["Category"] == c_dic_arr[1]:
                c_dic_arr_word[1].append(dic_arr[i]["Title"])
            elif dic_arr[i]["Category"] == c_dic_arr[2]:
                c_dic_arr_word[2].append(dic_arr[i]["Title"])
            elif dic_arr[i]["Category"] == c_dic_arr[3]:
                c_dic_arr_word[3].append(dic_arr[i]["Title"])

    json_arr = []


    for i in range(0, len(c_dic_arr_word)):
        print("====================== Tag Analize [" + c_dic_arr[i] + "]========================")
        #제목만 명사 뽑아내기 + 토큰화
        #===================================================================================================================
        token_news = nmo.data_token(c_dic_arr_word[i])
        #2차원 배열 → 1차원 배열로 변환
        token_news = sum(token_news, [])
        #불용어 리스트화
        stop_words = nmo.stop_word('../naver_news_crolling/func/stopwords_Test.txt')
        #불용어 처리
        token_news = nmo.sw(token_news,stop_words)
        #Normalization
        nmo.nomalizantion_nouns(token_news, "신지", "예","신지예")
        nmo.nomalizantion_nouns(token_news, "확", "진자","확진자")
        nmo.nomalizantion_nouns(token_news, "미접", "종자","미접종자")
        nmo.nomalizantion_nouns(token_news, "위중", "증","위중증")
        nmo.nomalizantion_nouns(token_news, "부스터", "샷","부스터샷")
        nmo.nomalizantion_nouns(token_news, "보료", "건","건보료")
        nmo.nomalizantion_nouns(token_news, "이진", "곤","이진곤")
        nmo.nomalizantion_nouns(token_news, "수거", "의류","의류수거함") #애매
        nmo.nomalizantion_nouns(token_news, "자영", "업자","자영업자")
        nmo.nomalizantion_nouns(token_news, "패스", "백신","백신패스")
        nmo.nomalizantion_nouns(token_news, "선양", "국위","국위선양")
        nmo.nomalizantion_nouns(token_news, "킥", "보드","킥보드")
        nmo.nomalizantion_nouns(token_news, "방가", "고성","고성방가")
        nmo.nomalizantion_nouns(token_news, "자", "영업","자영업")
        #nmo.nomalizantion_nouns(token_news, "가동", "률","가동률") #애매
        nmo.nomalizantion_nouns(token_news, "코지", "해","해코지")
        nmo.nomalizantion_nouns(token_news, "두기", "거리","거리두기")
        #한글자는 삭제
        nmo.check_text(token_news)
         #사전화 
        tmp_dict = nmo.data_nltk_ko(token_news)
        result_key = tmp_dict.keys()

        for dic_i in result_key:
            json_arr.append({"category":c_dic_arr[i] , "keyword":dic_i, "size":tmp_dict[dic_i]})


    return json_arr, json_category_per_emotion




