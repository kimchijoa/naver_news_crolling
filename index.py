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
