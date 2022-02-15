import os
import sys
#custom import
sys.path.append("/naver_news_crolling/func/")
import mysql_conn as m_sql

test_date = '2022-02-14'
sql_cursor, conn = m_sql.create_conn()
#nmo.nmo_run(test_date)
m_sql.news_keyword(conn, sql_cursor, test_date)