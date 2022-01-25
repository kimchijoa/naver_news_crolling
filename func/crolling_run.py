from logging import Manager, root
from datetime import date, timedelta, datetime
import time
import datetime
import threading
import pandas as pd
import schedule
import os
import sys
#custom import
sys.path.append("/naver_news_crolling/func/")
import xls_controll as xls_c
import naver_news_crolling as naver
import mysql_conn as m_sql
import aws_s3_config as s3

#해당 파일은 crontab 용으로 만들어진 크롤링 스크립트 입니다.
#기존(KST)에는 이전날의 정보를 크롤링하기위해 의도적으로 날짜를 -1 하였지만, 
#crontab에서 KST가 되지 않아 UST 시간대로 정보를 크롤링하기위해 날짜를 -1 하지않습니다.

def main_process():
    print("날짜설정")
    print(datetime.datetime.now())
    use_date = date.today().isoformat()
    #생성할 폴더 이름, 엑셀시트, 엑셀파일명 지정
    root_folder_name = "/naver_news_crolling/news_data/" #crontab 테스트의 경우 news_data 대신 test_news_data 사용
    folder_name = root_folder_name + "news_data_" + use_date + "/"smf di
    sheet_title = "social_news"
    file_name_list = [folder_name + "naver_news_social_normal_content_" + use_date + ".xlsx", 
    folder_name + "naver_news_social_accident_content_" + use_date + ".xlsx", 
    folder_name + "naver_news_economy_normal_content_" + use_date + ".xlsx", 
    folder_name + "naver_news_politics_normal_content_" + use_date + ".xlsx"]
    graph_info_file_name = folder_name + "graph_speed_info_" + use_date + ".xlsx"
    graph_info_file = "graph_speed_info_" + use_date + ".xlsx"
    graph_sheet_title = "today_crolling_speed"
    #=======================================================================================================
    social_tab = ["사회", "사회", "경제", "정치"]
    social_tab_under = ["사회 일반","사건사고","경제 일반","정치일반"]
    #=======================================================================================================
    total_page = []
    #======================================================================================================
    begin = time.time()
    print("폴더 생성 준비")
    xls_c.create_folder(root_folder_name, folder_name, sheet_title, file_name_list)
    xls_c.create_graph_info_xls(graph_sheet_title, graph_info_file_name)
    print("폴더 생성")
    
    #===============================================================================================================================================================================
    print("쓰레드 시작")
    th1 = threading.Thread(target=naver.crolling_start, args=(sheet_title, graph_sheet_title, file_name_list[0], social_tab[0], social_tab_under[0], graph_info_file_name, use_date))
    th2 = threading.Thread(target=naver.crolling_start, args=(sheet_title, graph_sheet_title, file_name_list[1], social_tab[1], social_tab_under[1], graph_info_file_name, use_date))
    th3 = threading.Thread(target=naver.crolling_start, args=(sheet_title, graph_sheet_title, file_name_list[2], social_tab[2], social_tab_under[2], graph_info_file_name, use_date))
    th4 = threading.Thread(target=naver.crolling_start, args=(sheet_title, graph_sheet_title, file_name_list[3], social_tab[3], social_tab_under[3], graph_info_file_name, use_date))
    th1.start() # 쓰레드 시작
    th2.start() # 쓰레드 시작
    th3.start() # 쓰레드 끝날때까지 기다리는 역할
    th2.join()
    print("쓰레드2 종료")
    th3.join() # 쓰레드 끝날때까지 기다리는 역할
    print("쓰레드3 종료")
    time.sleep(3)
    th4.start() # 쓰레드 시작
    th1.join() # 쓰레드 끝날때까지 기다리는 역할
    print("쓰레드1 종료")
    th4.join() # 쓰레드 끝날때까지 기다리는 역할
    print("쓰레드4 종료")
    
    
    #크롤링 소요 시간 입력
    end = time.time()
    result = round(end - begin, 3)
    times = str(datetime.timedelta(seconds=result)).split(".")
    times = times[0]
    #파일 합치기
    excel_names = file_name_list
    excels = [pd.ExcelFile(name) for name in excel_names]
    frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in excels]
    frames[1:] = [df[1:] for df in frames[1:]]
    combined = pd.concat(frames)

    #파일저장
    total_news_data = "total_news_data_" + use_date + ".xlsx"
    combined.to_excel(folder_name + total_news_data, header=False, index=False)

    #s3에 파일 업로드 및 DB에 업로드
    folder_path, file_name, s3_folder
    s3.handle_upload_file(folder_name, total_news_data, "total_news/", use_date)       
    s3.handle_upload_file(folder_name, graph_info_file, "total_greph_info/", use_date)

    #메일 발송
    time.sleep(2)
    th5= threading.Thread(target=naver.send_mail, args=("today22motion@gmail.com","zlxl7707@naver.com", folder_name + total_news_data))
    #th5= threading.Thread(target=mbc_social_new_crolling_win.send_mail, args=("today22motion@gmail.com","amsmdmfm159@naver.com", total_news_data))
    th5.start() # 쓰레드 시작
    th5.join() # 쓰레드 끝날때까지 기다리는 역할
    print("메일을 발송하였습니다.")

    time.sleep(2)
    sql_cursor, conn = m_sql.create_conn()
    m_sql.insert_total_data(conn, sql_cursor, "Sheet1", folder_name + total_news_data, use_date )
    sql_cursor, conn = m_sql.create_conn()
    m_sql.crolling_speed_info(conn, sql_cursor, "today_crolling_speed", folder_name + graph_info_file, use_date )

    #크롤링 소요 시간 출력
    print(times)

#=======================================================================================================================================

if __name__ == "__main__":
    main_process()
