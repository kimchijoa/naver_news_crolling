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
import data_normalization_run as nmo

#함수명은 상세히 직관적으로 작성한다. 따라 읽으면 한글로 뜻을 이해할정도로
#api route는 반드시 crolling 으로 시작한다.
#수집한 데이터를 조회시 data로
#수집 작업에 대한 데이터 조회시 job으로
#모든 작업은 명사단위로 쪼갠다.
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/crolling/data/data_state/<date>')
def show_data01(date):
    return jsonify(mysql.get_news_data_state(date))
    
@app.route('/crolling/data/category/count/<date>')
def show_date02(date):
    return jsonify(mysql.get_news_data_count_by_category(date))

@app.route('/crolling/job/info/<date>')
def show_data03(date):
    return jsonify(mysql.get_crolling_job_data(date))

@app.route('/crolling/data/wordcloud/<date>')
def show_data04(date):
    return jsonify(nmo.nmo_run(date))




if __name__=='__main__':
 app.run(host='0.0.0.0', port=5000, debug=True)
