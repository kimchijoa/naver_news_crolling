import os
import sys
#custom import
sys.path.append("/naver_news_crolling/func/")
import mysql_conn as m_sql

test_date = '2022-02-15'
sql_cursor, conn = m_sql.create_conn()

#m_sql.news_keyword(conn, sql_cursor, test_date) #실행하면 카테고리별 keyword 삽입된다.
#m_sql.news_emotion(conn, sql_cursor, test_date) #실행하면 카테고리별 감정 카운트 삽입된다.