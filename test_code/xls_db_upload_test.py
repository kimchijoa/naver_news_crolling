import os
import sys
sys.path.append("/naver_news_crolling/func/")
import aws_s3_config as s3
import mysql_conn as m_sql
import datetime

#모든 테스트 코드는 root에서 실행된다는 가정하에 환경을 설정한다.
#KST(한국시간) 기준에서 9시간을 뺀다.
print(datetime.datetime.now())
use_date = "2022-01-25"
root_folder_name = "/naver_news_crolling/news_data/"
folder_name = root_folder_name + "news_data_" + use_date + "/"
graph_info_file_name = folder_name + "graph_speed_info_" + use_date + ".xlsx"
graph_info_file = "graph_speed_info_" + use_date + ".xlsx"
total_news_data = "total_news_data_" + use_date + ".xlsx"

sql_cursor, conn = m_sql.create_conn()
m_sql.insert_total_data(conn, sql_cursor, "Sheet1", folder_name + total_news_data, use_date )
sql_cursor, conn = m_sql.create_conn()
m_sql.crolling_speed_info(conn, sql_cursor, "today_crolling_speed", folder_name + graph_info_file, use_date )