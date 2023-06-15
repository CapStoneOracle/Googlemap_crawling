import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

SEARCH = '노원구 동일로 공릉곱창'
TIMEOUT = 5


# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메시지 삭제
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# GPU 사용 X
chrome_options.add_argument('disable-gpu') 

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.google.co.kr/maps/")

def search_bulit():
    df = pd.read_csv('D:\\노원구음식점_가공.csv', encoding='utf-8')
    food_city = df['도로명주소']
    food_code = df['사업장명']
    search_name = []
    for i in range(len(food_city)):
            name = food_city[i] + " " + str(food_code[i]) + " 음식점" 
            search_name.append(name)
    return search_name, food_code

def wait_input(driver):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tactile-searchbox-input"))
        ) #입력창이 뜰 때까지 대기
    finally:
        pass

def input_funtion(n,driver,search_name):
    """
    열린 구글맵에서 검색할 단어 검색
    """
    print(search_name[n])
    search_box = driver.find_element_by_id("searchboxinput")
    search_box.send_keys(search_name[n])
    search_box.send_keys(Keys.ENTER)

def main_search(number,food_names,food_codes,error_search,food_code,driver,search_name):
    #for값으로 크롤링 개수 조절
    for n in range(0, number):
        input_funtion(n,driver,search_name)
        time.sleep(5)
        while True:
            try:
                state = driver.find_element_by_id("ppdPk-Ej1Yeb-LgbsSe-tJiF1e").get_attribute('disabled')
            except:
                error_search.append(search_name[n])
                break
                
            if state != True:
                try:
                    #검색 결과로 나타나는 scroll-bar 포함한 div 잡고 스크롤 내리기
                    scroll_div = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]')
                    driver.execute_script("arguments[0].scrollBy(0,2000)", scroll_div)
                    time.sleep(0.9)
                    driver.execute_script("arguments[0].scrollBy(0,2000)", scroll_div)
                    time.sleep(0.9)
                    driver.execute_script("arguments[0].scrollBy(0,2000)", scroll_div)

                    #한 칸 전체 데이터 가져오기
                    elements = driver.find_elements_by_class_name('CJY91c-jRmmHf-aVTXAb-haAclf-HSrbLb')
                    for i in range(20):
                        try:
                            food_codes.append(food_code[n])
                            food_names.append(elements[i].text)
                        except:
                            break

                    next_button = driver.find_element_by_id('ppdPk-Ej1Yeb-LgbsSe-tJiF1e')
                    next_button.click()
                    time.sleep(2.8)
                except:
                    break
            else:
                break
                
        try:
            driver.find_element_by_class_name("sbcb_a").click()
        except:
            pass

    return food_names, food_codes