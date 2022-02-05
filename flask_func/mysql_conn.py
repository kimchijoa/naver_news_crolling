import pymysql as mysql
import openpyxl
import time
import json
import sys
sys.path.append("/naver_news_crolling/func/")
import xls_controll as xls

def create_conn():
    try:
        conn = mysql.connect(
            user='kkh', 
            passwd='rnjrnjwm12', 
            host='172.19.0.2', 
            db='today_emotion', 
            charset='utf8',
            port=3306
        )
        sql_cursor = conn.cursor()
        print("DB 연결 : 172.19.0.2")
    except:
        conn = mysql.connect(
        user='kkh', 
        passwd='rnjrnjwm12', 
        host='172.19.0.3', 
        db='today_emotion', 
        charset='utf8',
        port=3306
        )
        sql_cursor = conn.cursor()
        print("DB 연결 : 172.19.0.3")

    
    return sql_cursor, conn

def select_date(date):
    sql_cursor, conn = create_conn()
    sql = "SELECT * FROM today_news_data WHERE news_date = " + "'" + date  + "'"
    return sql_cursor.execute(query=sql)
    

def select_yesterday(date):
    sql_cursor, conn = create_conn()
    sql = "SELECT * FROM today_news_data WHERE news_date=" + "'" + date  + "';"
    cursor = conn.cursor(mysql.cursors.DictCursor)
    cursor.execute(sql)
    #result = json.dumps(cursor.fetchall())
    result = cursor.fetchall()


    return result

def get_yesterday_cron_job(date):
    sql_cursor, conn = create_conn()
    sql01 = "SELECT COUNT(*) as db_news_cnt FROM today_news_data WHERE news_date=" + "'" + date  + "';"
    sql02 = "SELECT COUNT(*) as c_info_cnt FROM crolling_speed_info WHERE update_date=" + "'" + date  + "';"
    sql03 = "SELECT s3_file_name, s3_file_size FROM s3_info WHERE update_date=" + "'" + date  + "';"
    cursor = conn.cursor(mysql.cursors.DictCursor)
    cursor.execute(sql01)
    #해당 날짜 크롤링 정보 row 갯수
    db_news_row_cnt =  cursor.fetchall()
    #해당 날자 크롤링 속도 기록 row 갯수
    #cursor.execute(sql02)
    #db_c_info_row_cnt =  cursor.fetchall()
    cursor.execute(sql03)
    db_s3_info =  cursor.fetchall()
    cursor.close()

    local_news_row_cnt = {"local_news_cnt": xls.load_local_total_news_info(date)}
    #local_c_info_row_cnt = {"local_c_info_row_cnt": xls.load_local_c_speed_info(date)}
 
    return db_news_row_cnt, local_news_row_cnt, db_s3_info

def get_yesterday_crolling_data(date):
    sql_cursor, conn = create_conn()
    sql = "SELECT COUNT(CASE WHEN n_category = '사회 일반' THEN 1 END) as c_s_normal, COUNT(CASE WHEN n_category = '사건사고' THEN 1 END) as c_accident, "
    sql = sql + "COUNT(CASE WHEN n_category = '경제 일반' THEN 1 END) as c_e_normal, "
    sql = sql + "COUNT(CASE WHEN n_category = '정치일반' THEN 1 END) as c_p_normal "
    sql = sql + "FROM today_news_data WHERE news_date=" + "'" + date + "';"
    cursor = conn.cursor(mysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    json_arr = [];
    json_arr.append({"category":"사회일반", "cnt" : result[0]['c_s_normal']})
    json_arr.append({"category":"사건사고", "cnt" : result[0]['c_accident']})
    json_arr.append({"category":"경제일반", "cnt" : result[0]['c_e_normal']})
    json_arr.append({"category":"정치일반", "cnt" : result[0]['c_p_normal']})
    
    return json_arr

def get_yesterday_crolling_sp_info(date):
    sql_cursor, conn = create_conn()
    sql = "SELECT idx, cost_time FROM crolling_speed_info WHERE update_date=" + "'" + date  + "';"
    cursor = conn.cursor(mysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
 
    return result

create_conn()

