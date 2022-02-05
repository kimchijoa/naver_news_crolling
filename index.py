from logging import Manager
from flask import Flask, render_template, jsonify
from datetime import date, timedelta, datetime
#===
import os
import sys
import urllib.request
import time
from flask_func import mysql_conn as mysql
sys.path.append("/naver_news_crolling/func/")
import xls_controll as xls



app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/total_data/date/<date>')
def select_date(date):
    return jsonify(mysql.select_yesterday(date))

@app.route('/check_today_status/<date>')
def show_date(date):
    return jsonify(mysql.get_yesterday_cron_job(date))

@app.route('/get_yesterday_crolling_sp_info/<date>')
def show_c_data(date):
    return jsonify(mysql.get_yesterday_crolling_sp_info(date))

@app.route('/get_yesterday_crolling_data/<date>')
def show_c_data_count(date):
    return jsonify(mysql.get_yesterday_crolling_data(date))




if __name__=='__main__':
 app.run(host='0.0.0.0', port=5000, debug=True)

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