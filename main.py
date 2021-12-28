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

total_news_data = "total_news_data" +(date.today() - timedelta(1)).isoformat() + ".xlsx"
total_time = "will start this process"

#생성할 폴더 이름, 엑셀시트, 엑셀파일명 지정
root_folder_name = "news_data/"
folder_name = root_folder_name + "news_data_" +(date.today() - timedelta(1)).isoformat() + "/"
sheet_title = "social_news"
file_name_list = ["naver_news_social_normal_content_" + (date.today() - timedelta(1)).isoformat() + ".xlsx", 
"naver_news_social_accident_content_" + (date.today() - timedelta(1)).isoformat() + ".xlsx", 
"naver_news_economy_normal_content_" + (date.today() - timedelta(1)).isoformat() + ".xlsx", 
"naver_news_politics_normal_content_" + (date.today() - timedelta(1)).isoformat() + ".xlsx"]
#=======================================================================================================
social_tab = ["사회", "사회", "경제", "정치"]
social_tab_under = ["사회 일반","사건사고","경제 일반","정치일반"]
#=======================================================================================================
total_page = []
 #======================================================================================================



# def go_schedule_crolling():
#     sheet_title = "social_news"
#     #file_name = "save_new_content_" + date.today().isoformat() + ".xlsx"
#     file_name01 = "naver_news_social_normal_content_" + date.today().isoformat() + ".xlsx"
#     file_name02 = "naver_news_social_accident_content_" + date.today().isoformat() + ".xlsx"
#     file_name03 = "naver_news_economy_normal_content_" + date.today().isoformat() + ".xlsx"
#     file_name04 = "naver_news_politics_normal_content_" + date.today().isoformat() + ".xlsx"
#     #social_tab, social_tab_under


    
#     begin = time.time()


    # mbc.create_xls(sheet_title, file_name01)
    # mbc.create_xls(sheet_title, file_name02)
    # mbc.create_xls(sheet_title, file_name03)
    # mbc.create_xls(sheet_title, file_name04)

    # th1 = threading.Thread(target=mbc_social_new_crolling_win.crolling_start, args=(sheet_title, file_name01, social_tab[0], social_tab_under[0]))
    # th2 = threading.Thread(target=mbc_social_new_crolling_win.crolling_start, args=(sheet_title, file_name02, social_tab[0], social_tab_under[1]))
    # th3 = threading.Thread(target=mbc_social_new_crolling_win.crolling_start, args=(sheet_title, file_name03, social_tab[1], social_tab_under[2]))
    # th4 = threading.Thread(target=mbc_social_new_crolling_win.crolling_start, args=(sheet_title, file_name04, social_tab[2], social_tab_under[3]))
    # th1.start() # 쓰레드 시작
    # th2.start() # 쓰레드 시작
    # th2.join() # 쓰레드 끝날때까지 기다리는 역할
    # print("쓰레드2 종료")
    # time.sleep(10)
    # print("=======쓰레드3 시작============")
    # th3.start() # 쓰레드 시작
    # th3.join() # 쓰레드 끝날때까지 기다리는 역할
    # print("쓰레드3 종료")
    # time.sleep(10)
    # th4.start() # 쓰레드 시작
    # th4.join() # 쓰레드 끝날때까지 기다리는 역할

    # th1.join() # 쓰레드 끝날때까지 기다리는 역할
    # print("쓰레드1 종료")
    
    
    
    # end = time.time()
    # result = round(end - begin, 3)
    # times = str(datetime.timedelta(seconds=result)).split(".")
    # times = times[0]
    # total_time = times
    # print(times)

    # #파일 합치기
    # excel_names = [file_name01, file_name02, file_name03, file_name04]
    # excels = [pd.ExcelFile(name) for name in excel_names]
    # frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in excels]
    # frames[1:] = [df[1:] for df in frames[1:]]
    # combined = pd.concat(frames)

    # #파일저장
    # total_news_data = "total_news_data_" +(date.today() - timedelta(1)).isoformat() + ".xlsx"
    # combined.to_excel(total_news_data, header=False, index=False)
    
    # #메일 발송은 time 2초 정도 주기
    # time.sleep(2)
    # th5= threading.Thread(target=mbc_social_new_crolling_win.send_mail, args=("today22motion@gmail.com","zlxl7707@naver.com", total_news_data))
    # #th5= threading.Thread(target=mbc_social_new_crolling_win.send_mail, args=("today22motion@gmail.com","amsmdmfm159@naver.com", total_news_data))
    # th5.start() # 쓰레드 시작
    # th5.join() # 쓰레드 끝날때까지 기다리는 역할
    # print("메일을 발송하였습니다.")
    # #mbc.send_mail("today22motion@gmail.com","zlxl7707@naver.com",total_news_data)


if __name__ == "__main__": 
    xls_c.create_folder(root_folder_name, folder_name, sheet_title, file_name_list)
    #go_schedule_crolling()
    for i in range(len(social_tab)):
        driver = naver.setting_driver()
        #마지막 파라미터가 1이라면 이전날짜 데이터를 조회한다.
        page_len = naver.move_end_content_return_total(driver, social_tab[i], social_tab_under[i], 1)
        print("종료 및 결과값 : " + str(page_len))
        total_page.append(int(page_len))
        driver.quit()
    
    print("결과값 : ")
    print(total_page)

    print("최적 경로 계산...")

    #리스트 원소중 제일 큰 값을 0 위치에 둔다 0 값이 제일 크다면 0을 max로 설정!
    max_page = 0
    for i in range(len(total_page)):
        if total_page[0] < total_page[i]:
            temp = total_page[0]
            total_page[0] = total_page[i]
            total_page[i] = temp
        else:
            max_page = total_page[0]

    #리스트 원소중 제일 큰 값을 제외한 리스트를 오름차순으로 비교하고 맨 앞에 제일 큰값을 삽입한다.
    del total_page[0]
    total_page.sort()
    total_page.insert(0, max_page)

    print("최적 경로 계산 완료 : ")
    print(total_page)
    mm_total = 0
    mm = 0
    for i in range(1,len(total_page)):
        mm = mm + total_page[i]

        if total_page[0] < mm:
            print("마지막 쓰레드를 분할합니다.")
            mmm = (mm - total_page[0])
            print("마지막 쓰레드는" + str(total_page[len(total_page)-1]) + "에서" + str(mmm)  + "까지 분할 실행됩니다.")
            print("마지막 쓰레드는" + str(mmm-1) + "에서" + str(1)  + "까지 분할 실행됩니다.")

    mm_total = mm


    if total_page[0] > mm_total:
        print("첫번째 쓰레드를 분할합니다.")
        mmm = total_page[0] - mm
        print("첫번째 쓰레드는" + str(mm_total) + "에서" + str(1)  + "까지 분할 실행됩니다.")
        

    



# while 1:
#     print("hi")
#     time.sleep(3)

#schedule.every().day.at("15:55").do(go_schedule_crolling)

# while 1:

#     schedule.run_pending()
#     time.sleep(10)
#     os.system("clear")
#     print("======== waitng for crolling... It will start 15:55 ========")
#     print("==== end time : " + total_time)

