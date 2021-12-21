import time
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys
import openpyxl
from datetime import date, timedelta, datetime

chromedriver_autoinstaller.install()
print("#chromedriver_auto install?")
display = Display(visible=0, size=(1920, 1000))
display.start()
print("#display_on")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('window-size=1920,1400')
chrome_options.add_argument("--single-process")
#chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(chrome_options=chrome_options)
print("#chromedriver is import?")
driver.set_window_position(0, 0)
driver.set_window_size(1920, 1080)
driver.implicitly_wait(10)

# https://stackoverflow.com/questions/61308799/unable-to-locate-elements-in-selenium-python

wb = openpyxl.Workbook()
sheet1 = wb.active
sheet1.title = "social_news"
new_file_name = "save_new_content_" + date.today().isoformat() + ".xlsx"

global sheet_title
global sheet_content
sheet_title = 2
sheet_content = 2

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

print("#Open Page")
driver.get("https://imnews.imbc.com/pc_main.html?gnb=top")
#driver.maximize_window()


print("메뉴 이동 : " + driver.find_element(By.XPATH, "//*[@id='navi']/div/div[1]/div[1]/ul/li[7]/a").text)
driver.find_element(By.XPATH, "//*[@id='navi']/div/div[1]/div[1]/ul/li[7]/a").click()



# ==========================================================================================================

def crap_content():
    time.sleep(2)
    e_list = driver.find_elements(By.CLASS_NAME, "item")
    print("탐지된 컨텐츠 수 : " + str(len(e_list)))
    driver.execute_script("window.scrollTo(0, (document.body.scrollHeight/2));")
    time.sleep(8)
    for i in range(2):
        print("현재 창 height : " + str(driver.execute_script('return window.scrollY')))
        driver.execute_script("window.scrollTo(window.scrollY, window.scrollY + document.body.scrollHeight/5);")
        time.sleep(2)
    driver.execute_script("window.scrollTo(0, (document.body.scrollHeight));")
    e_list = driver.find_elements(By.CLASS_NAME, "item")
    print("탐지된 컨텐츠 수 : " + str(len(e_list)))

    #for i in range(2): #엑셀파일 저장 테스트용
    for i in range(len(e_list)):
        ActionChains(driver).key_down(Keys.CONTROL) \
            .click(e_list[i]) \
            .key_up(Keys.CONTROL) \
            .perform()

        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
        print("==========================================================================")
        print("뉴스 제목 : " + driver.title)
        print("뉴스 링크" + driver.current_url)
        # e_content = driver.find_element(By.XPATH, "//*[@id='content']/div/section[1]/article/div[2]/div[5]/div").text
        e_content = driver.find_element(By.CLASS_NAME, "news_txt").text
        print("뉴스 내용" + e_content)
        hash_tag = driver.find_element(By.CLASS_NAME, "hashtag").text
        print("해쉬 태그 : " + hash_tag)
        feel = driver.find_elements(By.CLASS_NAME, "count")
        print("독자 반응01 : " + feel[0].text)
        print("독자 반응02 : " + feel[1].text)
        print("독자 반응03 : " + feel[2].text)
        print("독자 반응04 : " + feel[3].text)
        print("독자 반응04 : " + feel[4].text)

        global sheet_title
        sheet_title = sheet_title
        global sheet_content
        sheet_content = sheet_content
        sheet1["A" + str(sheet_title)] = driver.title
        sheet1["B" + str(sheet_content)] = e_content
        sheet1["C" + str(sheet_content)] = driver.current_url
        sheet1["D" + str(sheet_title)] = hash_tag
        sheet1["E" + str(sheet_title)] = feel[0].text
        sheet1["F" + str(sheet_title)] = feel[1].text
        sheet1["G" + str(sheet_title)] = feel[2].text
        sheet1["H" + str(sheet_title)] = feel[3].text
        sheet1["I" + str(sheet_title)] = feel[4].text
        print("==========================================================================")
        sheet_title += 1
        sheet_content += 1

        print(sheet_title)
        print(sheet_content)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)

    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
    time.sleep(2)
    # wb.save(new_file_name)

# ==========================================================================================================

def select_data_picker():
    # 달력 선택
    print(datetime.now().day)
    today_day = int(datetime.now().day)

    for day in range(today_day, 0, -1):
    #for day in range(1, 0, -2):
        print("======================" + str(day) + "================================")
        driver.find_element(By.CLASS_NAME, "ui-datepicker-trigger").click()
        print("달력 클릭함")
        day_list = driver.find_elements(By.CLASS_NAME, "ui-state-default")

        for j in range(len(day_list)):

            if day_list[j].text == str(day):
            # if day_list[j].text == str(7):
                print(day_list[j].text + "가 감지됨")
                time.sleep(2)
                day_list[j].click()
                break

        print("현재 페이지 데이터 수집")
        crap_content()
        #break


# ==================================================================================

crap_content()

wb.save(new_file_name)

time.sleep(5)
driver.quit()
display.stop()

# =====================================================

#select_data_picker()
