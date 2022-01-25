import os
import sys
#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append("/naver_news_crolling/func/")
import aws_s3_config as s3
import mysql_conn as m_sql
import datetime

#모든 테스트 코드는 root에서 실행된다는 가정하에 환경을 설정한다.
#KST(한국시간) 기준에서 9시간을 뺀다.
print(datetime.datetime.now())
use_date = "2022-03-24"
root_folder_name = "/naver_news_crolling/news_data/"
folder_name = root_folder_name + "news_data_" + use_date + "/"
graph_info_file_name = folder_name + "graph_speed_info_" + use_date + ".xlsx"
graph_info_file = "graph_speed_info_" + use_date + ".xlsx"
total_news_data = "total_news_data_" + use_date + ".xlsx"
#없는 파일을 업로드 시도해보기
#s3.handle_upload_file(folder_name, graph_info_file, "total_greph_info/", use_date)
#folder_path, file_name, s3_folder
s3.handle_upload_file(folder_name, total_news_data, "total_news/", use_date)       
s3.handle_upload_file(folder_name, graph_info_file, "total_greph_info/", use_date)