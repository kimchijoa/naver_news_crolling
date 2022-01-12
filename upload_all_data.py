import os
import openpyxl
import mysql_conn as m_sql
import xls_controll as xls
import aws_s3_config as s3

def search_and_insert(dirname):
    folder_list = []
    folder_date_list = []
    total_news_xls_path = []
    graph_speed_xls_path = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        #print(full_filename)
        folder_list.append(full_filename)

        date = str(full_filename.split("_")[3])
        folder_date_list.append(date)
        total_news_xls_path.append(full_filename + "/total_news_data_" + date + ".xlsx")
        graph_speed_xls_path.append(full_filename + "/graph_speed_info_" + date + ".xlsx")
    
    # print(folder_list)
    print(folder_date_list)
    print(total_news_xls_path)
    print(graph_speed_xls_path)


    #s3에 파일 업로드 및 DB에 업로드
    #folder_path, file_name, s3_folder
    for i in range(len(total_news_xls_path)):
        folder_name = total_news_xls_path[i].split("/")[0] + "/" + total_news_xls_path[i].split("/")[1] + "/"
        total_news_data = total_news_xls_path[i].split("/")[2]
        graph_speed_info_file = graph_speed_xls_path[i].split("/")[2]

        print("=========" +  str(folder_date_list[i]) + "==========")
        print("폴더 경로 : " + str(folder_name))
        print("뉴스 엑셀 파일 명 : " + str(total_news_data))
        print("그래프 정보 엑셀 파일명 : " + str(graph_speed_info_file))
        s3.handle_upload_file(folder_name, total_news_data, "total_news/", str(folder_date_list[i]))       
        s3.handle_upload_file(folder_name, graph_speed_info_file, "total_greph_info/", str(folder_date_list[i]))
        sql_cursor, conn = m_sql.create_conn()
        m_sql.insert_total_data(conn, sql_cursor, "Sheet1", folder_name + total_news_data, str(folder_date_list[i]))


search_and_insert("news_data/")