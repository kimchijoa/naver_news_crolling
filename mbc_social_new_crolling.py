from sys import hash_info
import time
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys
import openpyxl
from datetime import datetime
#===================== 메일 발송 패키지
import os
import smtplib
from email.encoders import encode_base64
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


#드라이버 객체 반환
def setting_driver():
    chromedriver_autoinstaller.install()
    print("---chromedriver_auto install done")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920,1400')
    chrome_options.add_argument("--single-process")
    #chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    print("---chromedriver import")
    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(10)

    return driver

#엑셀 파일 저장
def setting_xls(sheet_title, file_name, list):
    wb = openpyxl.Workbook()
    sheet1 = wb.active
    sheet1.title = sheet_title
    new_file_name = file_name

    sheet1["A1"] = "기사 제목"
    sheet1["B1"] = "기사 링크"
    sheet1["C1"] = "기사 내용"
    sheet1["D1"] = "해쉬 태그"
    sheet1["E1"] = "좋아요"
    sheet1["F1"] = "대단해요"
    sheet1["G1"] = "슬퍼요"
    sheet1["H1"] = "화나요"
    sheet1["I1"] = "기대 돼요"
    sheet1["J1"] = "트래픽 양"

    sheet_num = 2
    for i in range(len(list)) : 
        sheet1["A" + str(sheet_num)] = list[i]['title']
        sheet1["B" + str(sheet_num)] = list[i]['e_content']
        sheet1["C" + str(sheet_num)] = list[i]['current_url']
        sheet1["D" + str(sheet_num)] = list[i]['hash_tag']
        sheet1["E" + str(sheet_num)] = list[i]['feel'][0]
        sheet1["F" + str(sheet_num)] = list[i]['feel'][1]
        sheet1["G" + str(sheet_num)] = list[i]['feel'][2]
        sheet1["H" + str(sheet_num)] = list[i]['feel'][3]
        sheet1["I" + str(sheet_num)] = list[i]['feel'][4]
        sheet_num += 1
        print("---엑셀화 중...")

    wb.save(new_file_name)
    print("--엑셀파일 저장 완료")
    return wb





# ==========================================================================================================

def crap_content():
    driver = setting_driver()
    new_list = []
    
    print("---Open Page")
    driver.get("https://imnews.imbc.com/pc_main.html?gnb=top")
    
    time.sleep(2)
    print("---메뉴 이동 : " + driver.find_element(By.XPATH, "//*[@id='navi']/div/div[1]/div[1]/ul/li[7]/a").text)
    driver.find_element(By.XPATH, "//*[@id='navi']/div/div[1]/div[1]/ul/li[7]/a").click()

    time.sleep(2)

    driver.execute_script("window.scrollTo(0, (document.body.scrollHeight/2));")
    time.sleep(2)

    for i in range(8):
        print("----현재 창 height : " + str(driver.execute_script('return window.scrollY')))
        driver.execute_script("window.scrollTo(window.scrollY, window.scrollY + document.body.scrollHeight/5);")
        time.sleep(2)
    driver.execute_script("window.scrollTo(0, (document.body.scrollHeight));")
    e_list = driver.find_elements(By.CLASS_NAME, "item")
    print("---탐지된 컨텐츠 수 : " + str(len(e_list)))

    #for i in range(2): #엑셀파일 저장 테스트용
    ########################################################이 줄 나중에 수정 바랍니다.
    #for i in range(len(e_list)):
    for i in range(len(e_list)):
        ActionChains(driver).key_down(Keys.CONTROL) \
            .click(e_list[i]) \
            .key_up(Keys.CONTROL) \
            .perform()

        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
        print("=================================  " +  str(i) + "  =========================================")
        print("----뉴스 제목 : " + driver.title)
        print("----뉴스 링크" + driver.current_url)
        # e_content = driver.find_element(By.XPATH, "//*[@id='content']/div/section[1]/article/div[2]/div[5]/div").text
        e_content = driver.find_element(By.CLASS_NAME, "news_txt").text
        print("----뉴스 내용" + e_content)
        hash_tag = driver.find_element(By.CLASS_NAME, "hashtag").text
        print("----해쉬 태그 : " + hash_tag)
        feel = driver.find_elements(By.CLASS_NAME, "count")
        feel_list = []
        feel_list.append(feel[0].text)
        feel_list.append(feel[1].text)
        feel_list.append(feel[2].text)
        feel_list.append(feel[3].text)
        feel_list.append(feel[4].text)
        print("----독자 반응01 : " + feel[0].text)
        print("----독자 반응02 : " + feel[1].text)
        print("----독자 반응03 : " + feel[2].text)
        print("----독자 반응04 : " + feel[3].text)
        print("----독자 반응04 : " + feel[4].text)

        news_dictionary = {}
        news_dictionary["title"] = driver.title
        news_dictionary["e_content"] = e_content
        news_dictionary["current_url"] = driver.current_url
        news_dictionary["hash_tag"] = hash_tag
        news_dictionary["feel"] = feel_list
        print("----dictionary")
        print(news_dictionary)
        new_list.append(news_dictionary)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)
    # wb.save(new_file_name)

    driver.quit()
    return new_list


def send_mail(from_mail, to_mail, attach):
    # 세션생성, 로그인
    print("메일 발송중 1")
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('today22motion@gmail.com', 'rnjrnjwm12')
    print("메일 발송중 2")
    # 제목, 본문 작성
    msg = MIMEMultipart()
    today = datetime.today().strftime("%Y-%m-%d")
    msg['Subject'] = Header(s=str(today) + '뉴스 분석데이터 발송합니다.', charset='utf-8')
    msg['From'] = from_mail
    msg['To'] = to_mail
    body = MIMEText(str(today) + '뉴스 분석데이터 발송합니다. 문제가 있을경우 개인연락 부탁드립니다.', _charset='utf-8')
    msg.attach(body)
    attach_file = attach
    print("메일 발송중 3")
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(attach_file,"rb").read())
    encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach_file))
    msg.attach(part)
    print("메일 발송중 4")
    # 메일 전송
    s.send_message(msg)
    s.quit()
    print("---send email with attach_file 'To. '" + to_mail + "'")

def crolling_start(sheet_title, file_name):
    print("##Setting Display")
    display = Display(visible=0, size=(1920, 1000))
    display.start()

    print("##Crolling_Start")

    list = crap_content()

    print("######################## 리스트 내역 출력 ##############################")
    print(list)
    display.stop()

    print("######################## 리스트 내역 엑셀화 ##############################")

    setting_xls(sheet_title, file_name, list)

    




