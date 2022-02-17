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

# [특정날짜] 뉴스데이터를 모두 리턴함
def get_news_data(date):
    sql_cursor, conn = create_conn()
    sql = "SELECT * FROM today_news_data WHERE news_date=" + "'" + date  + "';"
    cursor = conn.cursor(mysql.cursors.DictCursor)
    cursor.execute(sql)
    #result = json.dumps(cursor.fetchall())
    result = cursor.fetchall()
    return result

#[특정날짜] DB(뉴스데이터), XLS(뉴스데이터) row 갯수와 해당 날짜의 파일(S3) 경로를 리턴
def get_news_data_state(date):
    sql_cursor, conn = create_conn()
    sql01 = "SELECT COUNT(*) as db_news_cnt FROM today_news_data WHERE news_date=" + "'" + date  + "';"
    sql02 = "SELECT COUNT(*) as c_info_cnt FROM crolling_speed_info WHERE update_date=" + "'" + date  + "';"
    sql03 = "SELECT s3_file_name, s3_file_size FROM s3_info WHERE update_date=" + "'" + date  + "';"
    cursor = conn.cursor(mysql.cursors.DictCursor)
    cursor.execute(sql01)
    #해당 날짜 크롤링 정보 row 갯수
    db_news_row_cnt =  cursor.fetchall()
    #해당 날자 크롤링 속도 기록 row 갯수
    cursor.execute(sql03)
    db_s3_info =  cursor.fetchall()
    cursor.close()
    local_news_row_cnt = {"local_news_cnt": xls.load_local_total_news_info(date)}
    return db_news_row_cnt, local_news_row_cnt, db_s3_info

#[특정날짜] 크롤링 작업 정보 데이터를 리턴함
def get_crolling_job_data(date):
    sql_cursor, conn = create_conn()
    #sql = "SELECT idx, cost_time FROM crolling_speed_info WHERE update_date=" + "'" + date  + "';"
    sql = "SELECT @rownum := @rownum+1 AS RNUM , cost_time FROM crolling_speed_info, (SELECT @rownum := 0) R WHERE update_date=" + "'" +  date + "';"
    cursor = conn.cursor(mysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
 
    return result

#[특정날짜] 뉴스데이터를 카테고리별로 정렬하여 갯수만 리턴
def get_news_data_count_by_category(date):
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

def get_keyword_data(date, category):
    category_num_origin = [{"c1":"사회 일반","c2":"사건사고","c3":"경제 일반","c4":"정치일반"}]
    
    if(category =="none"):
        sql01 = "SELECT n_category, keyword, count FROM news_keyword WHERE update_date=" + "'" +  date + "' AND count >= 20 ORDER BY count DESC;"
        sql02 ="SELECT n_category, n_title, (n_e_like + n_e_good + n_e_sad + n_e_angry + n_e_expect) AS e_sum FROM today_news_data where news_date='" + date + "' ORDER BY e_sum DESC limit 5;"
        sql03 = "SELECT SUM(e_good) as e_good, SUM(e_bad) as e_bad FROM news_emotion_count WHERE update_date='" + date + "';"
    else:
        category_re = category_num_origin[0][category].replace(" ","")
        sql01 = "SELECT n_category, keyword, count FROM news_keyword WHERE update_date=" + "'" +  date + "'AND n_category='" + category_re + "' ORDER BY count DESC;"
        sql02 ="SELECT n_category, n_title, n_link, (n_e_like + n_e_good + n_e_sad + n_e_angry + n_e_expect) AS e_sum FROM today_news_data where news_date='" + date + "' AND n_category='" + category_num_origin[0][category] + "'ORDER BY e_sum DESC limit 5;"
        sql03 = "SELECT e_good, e_bad FROM news_emotion_count WHERE update_date='" + date + "' AND n_category='" + category_re +"';"

    sql_cursor, conn = create_conn()
    
    cursor = conn.cursor(mysql.cursors.DictCursor)
    cursor.execute(sql01)
    result = cursor.fetchall()

    
    cursor.execute(sql02)
    top5_news = cursor.fetchall()

    cursor.execute(sql03)
    emotion = cursor.fetchall()
    cursor.close()
 
    return result, top5_news, emotion

create_conn()

