from logging import Manager, root
from datetime import date, timedelta, datetime
import time
import datetime
import threading
import pandas as pd
import schedule
import os

#custom import
import xls_controll as xls_c
import naver_news_crolling as naver
import mysql_conn as m_sql
import aws_s3_config as s3

def main_process():
    print("h1")
    total_news_data = "total_news_data" +(date.today() - timedelta(1)).isoformat() + ".csv"
    #생성할 폴더 이름, 엑셀시트, 엑셀파일명 지정
    root_folder_name = "news_data/"
    folder_name = root_folder_name + "news_data_" +(date.today() - timedelta(1)).isoformat() + "/"
    sheet_title = "social_news"
    file_name_list = [folder_name + "naver_news_social_normal_content_" + (date.today() - timedelta(1)).isoformat() + ".xlsx", 
    folder_name + "naver_news_social_accident_content_" + (date.today() - timedelta(1)).isoformat() + ".xlsx", 
    folder_name + "naver_news_economy_normal_content_" + (date.today() - timedelta(1)).isoformat() + ".xlsx", 
    folder_name + "naver_news_politics_normal_content_" + (date.today() - timedelta(1)).isoformat() + ".xlsx"]
    graph_info_file_name = folder_name + "graph_speed_info_" + (date.today() - timedelta(1)).isoformat() + ".xlsx"
    graph_info_file = "graph_speed_info_" + (date.today() - timedelta(1)).isoformat() + ".xlsx"
    graph_sheet_title = "today_crolling_speed"
    #=======================================================================================================
    social_tab = ["사회", "사회", "경제", "정치"]
    social_tab_under = ["사회 일반","사건사고","경제 일반","정치일반"]
    #=======================================================================================================
    total_page = []
    #======================================================================================================
    begin = time.time()

    xls_c.create_folder(root_folder_name, folder_name, sheet_title, file_name_list)
    xls_c.create_graph_info_xls(graph_sheet_title, graph_info_file_name)
    


    #===============================================================================================================================================================================
    th1 = threading.Thread(target=naver.crolling_start, args=(sheet_title, file_name_list[0], social_tab[0], social_tab_under[0]))
    th2 = threading.Thread(target=naver.crolling_start, args=(sheet_title, file_name_list[1], social_tab[1], social_tab_under[1]))
    th3 = threading.Thread(target=naver.crolling_start, args=(sheet_title, file_name_list[2], social_tab[2], social_tab_under[2]))
    th4 = threading.Thread(target=naver.crolling_start, args=(sheet_title, file_name_list[3], social_tab[3], social_tab_under[3]))
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
    
    
    
    end = time.time()
    result = round(end - begin, 3)
    times = str(datetime.timedelta(seconds=result)).split(".")
    times = times[0]
    total_time = times
    print(times)

    #파일 합치기
    excel_names = file_name_list
    excels = [pd.ExcelFile(name) for name in excel_names]
    frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in excels]
    frames[1:] = [df[1:] for df in frames[1:]]
    combined = pd.concat(frames)

    #파일저장
    total_news_data = "total_news_data_" +(date.today() - timedelta(1)).isoformat() + ".xlsx"
    combined.to_excel(folder_name + total_news_data, header=False, index=False)

    #s3에 파일 업로드 및 DB에 업로드
    #folder_path, file_name, s3_folder
    s3.handle_upload_file(folder_name, total_news_data, "total_news/", (date.today() - timedelta(1)).isoformat())       
    s3.handle_upload_file(folder_name, graph_info_file, "total_greph_info/", (date.today() - timedelta(1)).isoformat())

    #메일 발송
    time.sleep(2)
    th5= threading.Thread(target=naver.send_mail, args=("today22motion@gmail.com","zlxl7707@naver.com", folder_name + total_news_data))
    # #th5= threading.Thread(target=mbc_social_new_crolling_win.send_mail, args=("today22motion@gmail.com","amsmdmfm159@naver.com", total_news_data))
    th5.start() # 쓰레드 시작
    th5.join() # 쓰레드 끝날때까지 기다리는 역할
    print("메일을 발송하였습니다.")

    # time.sleep(2)
    sql_cursor, conn = m_sql.create_conn()
    m_sql.insert_total_data(conn, sql_cursor, "Sheet1", folder_name + total_news_data, (date.today() - timedelta(1)).isoformat())
    sql_cursor, conn = m_sql.create_conn()
    m_sql.crolling_speed_info(conn, sql_cursor, "today_crolling_speed", folder_name + graph_info_file, (date.today() - timedelta(1)).isoformat())
    
#스케쥴러 확인용
#schedule.every().day.at("00:05").do(main_process)

if __name__ == "__main__":
    main_process()

        
    # root_folder_name = "news_data/"
    # folder_name = root_folder_name + "news_data_" +(date.today() - timedelta(1)).isoformat() + "/"
    # total_news_data = folder_name + "total_news_data_" +(date.today() - timedelta(1)).isoformat() + ".xlsx"
    # m_sql.insert_total_data(conn, sql_cursor, sql, "Sheet1", total_news_data, (date.today() - timedelta(1)).isoformat())
    # sql_cursor, conn = m_sql.create_conn()
    # m_sql.insert_total_data(conn, sql_cursor, "Sheet1", total_news_data, (date.today() - timedelta(1)).isoformat())
