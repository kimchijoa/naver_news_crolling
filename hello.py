from logging import Manager
from flask import Flask, render_template
import mbc_social_new_crolling as mbc
from datetime import date, timedelta, datetime
#===
import os
import sys
import urllib.request
import time
import xls_controll as xls


app = Flask(__name__)

@app.route('/')
def hello_world():
    #return render_template("index.html", data='전달데이터')
    graph_info = xls.read_grap_speed("today_crolling_speed", "news_data/news_data_2021-12-31/graph_speed_info_2021-12-31.xlsx")
    return render_template("index.html", data= graph_info)

@app.route('/sample')
def sample():
    #return render_template("index.html", data='전달데이터')
    return render_template("d3_sample.html")


# @app.route('/social')
# def hello_social():
#     print("############# Plz Wait ##################")
#     #driver = mp.setting_driver()
#     sheet_title = "social_news"
#     file_name = "save_new_content_" + date.today().isoformat() + ".xlsx"

#     mbc.crolling_start(sheet_title, file_name)
#     time.sleep(5)
    
#     mbc.send_mail("today22motion@gmail.com","zlxl7707@naver.com", file_name)
    
#     return "Test End"

# def naver_news_crolling():
    
#     client_id = "KcsN0LqKQjM7axAVg8qZ"
#     client_secret = " jHkdd8d8j1"
#     encText = urllib.parse.quote("코로나")
#     #url = "https://openapi.naver.com/v1/search/news.json?query=" + encText + "&display=10" # json 결과
#     url = "https://openapi.naver.com/v1/search/news.json?query=" + encText + "&display=100" # json 결과
#     #url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText + "&display=30" # xml 결과
#     #url = "https://openapi.naver.com/v1/search/blog.xml?display=30" # xml 결과
#     request = urllib.request.Request(url)
#     request.add_header("X-Naver-Client-Id",client_id)
#     request.add_header("X-Naver-Client-Secret",client_secret)
#     response = urllib.request.urlopen(request)
#     rescode = response.getcode()
#     if(rescode==200):
#         response_body = response.read()
#         print(response_body.decode('utf-8')) #print(response_body.decode('utf-8'))
#         print("===========================##########===========================")
#     else:
#         print("Error Code:" + rescode)