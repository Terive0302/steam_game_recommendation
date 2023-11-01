
# 연도별로 작업해서 합칠게요.
# 컬럼명은 ['title', 'reviews']로 통일하겠습니다.
# 파일명은 reviews_{연도}.csv 로 하겠습니다.
# 경민님이 2013-2015
# 재희님이 2016-2023 해주세요.


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
# options.add_argument("--no-sandbox")

# options.add_argument("--disable-popup-blocking")

service = ChromeService(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

# year = 2023
# url = 'https://movie.daum.net/ranking/boxoffice/monthly?date={}01'.format(year)
# title_path = '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'
# button_score_path = '//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span'
# button_more_path = '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button'
# review_path = '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'
# button_next_path = '//*[@id="mainContent"]/div/div[1]/div[1]/div/a[2]/span'
# url = 'https://movie.daum.net/ranking/boxoffice/monthly?date={}01'


jrpg_url = 'https://store.steampowered.com/category/rpg_jrpg/?flavor=contenthub_topsellers'
rogue_url = 'https://store.steampowered.com/category/rogue_like_rogue_lite/?flavor=contenthub_topsellers'
action_url = 'https://store.steampowered.com/category/rpg_action/?flavor=contenthub_topsellers'
adventure_url = 'https://store.steampowered.com/category/adventure_rpg/?flavor=contenthub_topsellers'
strategy_url = 'https://store.steampowered.com/category/rpg_strategy_tactics/?flavor=contenthub_topsellers'
turn_url = 'https://store.steampowered.com/category/rpg_turn_based/?flavor=contenthub_topsellers'
party_url = 'https://store.steampowered.com/category/rpg_party_based/?flavor=contenthub_topsellers'

"""

"""
while(True):
    driver.get('https://store.steampowered.com/category/rpg_jrpg/?flavor=contenthub_topsellers')
    print("최고 인기 제품")
    time.sleep(5)
    driver.find_element('xpath', '/html/body/div[1]/div[7]/div[1]/div/div[3]/div/span').click()
    print("언어 클릭됨")
    time.sleep(1)
    driver.find_element('xpath', '/html/body/div[1]/div[7]/div[1]/div/div[3]/div/div/div/a[4]').click()
    print("한국어 변경")
    time.sleep(5)

    # actions = driver.find_element(By.CSS_SELECTOR, 'body')
    # actions.send_keys(Keys.END)
    # time.sleep(0.1)

    count = 0

    for page in range(0, 300):
        # count = count + 1 # 크롤링 들어가면 카운트 증가되게 넣자
        driver.get('https://store.steampowered.com/category/rpg_jrpg/?flavor=contenthub_topsellers&offset={}'.format(page))
        time.sleep(5) # 오프셋 1씩 증가
        game_url = driver.find_element('xpath', '//*[@id="SaleSection_13268"]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[2]/a').get_attribute('href')
        driver.get(game_url) # 1번째 링크 들어가기
        while driver.execute_script("return document.readyState") != "complete":
            time.sleep(1) # 로딩 될 때까지 대기
        actions = driver.find_element(By.CSS_SELECTOR, 'body')
        actions.send_keys(Keys.END) # End키 누르기
        # driver .execute_script("window.scrollBy(0, 30000);")
        time.sleep(3) # 로딩되는 거 잠깐 기다림
        try:
            actions = driver.find_element(By.CSS_SELECTOR, 'body')
            actions.send_keys(Keys.END) # 한 번더 End키 누르기
            time.sleep(2)
            driver.find_element('xpath', '/html/body/div[1]/div[7]/div[6]/div[3]/div[2]/div[1]/div[6]/div/div/div[16]/div/div[4]/a').click()
            time.sleep(5) # 모든 평가 보기 클릭
        except:
            print("모든 평가 보기 없음")
            time.sleep(1)
            continue

        for eng_review in range(0, 150):
            if count > 150:
                break
            for first in range(1, 101): # div[first]/div[]/div[] # 1 ~ 100까지 증가
                actions = driver.find_element(By.CSS_SELECTOR, 'body')
                actions.send_keys(Keys.END)  # End키 누르기
                time.sleep(1)  # 로딩되는 거 잠깐 기다림
                for second in range(1, 10): # div[]/div[second]/div[] # 1 ~ 10까지 증가
                    for third in range(2, 6): # div[]/div[]/div[third] # 2 ~ 5까지 증가
                        try:
                            rv = driver.find_element('xpath', f'/html/body/div[1]/div[7]/div[5]/div/div[1]/div[3]/div[1]/div[{first}]/div[{second}]/div[{third}]/div[1]/div[1]/div[3]').text
                            print(rv)
                            count = count + 1
                        except:
                            print(f"ENG error : {first}_{second}_{third}")
        count = 0
        actions = driver.find_element(By.CSS_SELECTOR, 'body')
        actions.send_keys(Keys.HOME)  # Home키 누르기
        time.sleep(1)  # 로딩되는 거 잠깐 기다림
        driver.find_element('xpath', '/html/body/div[1]/div[7]/div[5]/div/div[1]/div[1]/div[3]/div[8]/div[1]').click()
        time.sleep(1) # 랭귀지 클릭
        driver.find_element('xpath', '/html/body/div[1]/div[7]/div[5]/div/div[1]/div[1]/div[3]/div[9]/div[9]/div[5]').click()
        time.sleep(5) # 한국어 클릭 후 5초 기다림
        for kor_review in range(0, 150):
            if count > 150:
                break
            for first in range(1, 101): # div[first]/div[]/div[] # 1 ~ 100까지 증가
                actions = driver.find_element(By.CSS_SELECTOR, 'body')
                actions.send_keys(Keys.END)  # End키 누르기
                time.sleep(1)  # 로딩되는 거 잠깐 기다림
                for second in range(1, 10): # div[]/div[second]/div[] # 1 ~ 10까지 증가
                    for third in range(2, 6): # div[]/div[]/div[third] # 2 ~ 5까지 증가
                        try:
                            rv = driver.find_element('xpath', f'/html/body/div[1]/div[7]/div[5]/div/div[1]/div[3]/div[1]/div[{first}]/div[{second}]/div[{third}]/div[1]/div[1]/div[3]').text
                            print(rv)
                            count = count + 1
                        except:
                            print(f"KOR error : {first}_{second}_{third}")
        count = 0
        actions = driver.find_element(By.CSS_SELECTOR, 'body')
        actions.send_keys(Keys.HOME)  # Home키 누르기
        time.sleep(1)  # 로딩되는 거 잠깐 기다림
        driver.find_element('xpath', '/html/body/div[1]/div[7]/div[5]/div/div[1]/div[1]/div[3]/div[8]/div[1]').click()
        time.sleep(1) # 랭귀지 클릭
        driver.find_element('xpath', '/html/body/div[1]/div[7]/div[5]/div/div[1]/div[1]/div[3]/div[9]/div[9]/div[11]').click()
        time.sleep(5) # 영어 클릭 후 5초 기다림

        # time.sleep(5) # driver.back()쓸 필요 없음



    # while(True):
    #     try:
    #         game_url = driver.find_element('xpath', '//*[@id="SaleSection_13268"]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[2]/a').get_attribute('href')
    #         driver.get(game_url)
    #         time.sleep(0.1)
    #         actions = driver.find_element(By.CSS_SELECTOR, 'body')
    #         actions.send_keys(Keys.END)
    #         break
    #     except:
    #         print("오류")
    # actions = driver.find_element(By.CSS_SELECTOR, 'body')
    # actions.send_keys(Keys.END)
    # time.sleep(0.1)
    # while True:
    #     try:
    #         driver.find_element('xpath', '/html/body/div[1]/div[7]/div[6]/div[3]/div[2]/div[1]/div[6]/div/div/div[16]/div/div[4]/a').click()
    #         print("모든 평가보기 클릭됨")
    #         break  # 요소를 찾았으므로 반복 종료
    #     except:
    #         print("요소를 찾지 못했습니다. 다시 시도합니다.")
    # test_review = driver.find_element('xpath', '/html/body/div[1]/div[7]/div[5]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[3]').text
    # print(test_review)
    # print("----------------------")
    # time.sleep(0.1)
    # test_review = driver.find_element('xpath', '/html/body/div[1]/div[7]/div[5]/div/div[1]/div[3]/div[1]/div[1]/div[6]/div[2]/div[1]/div[1]/div[3]').text
    # print(test_review)
    # time.sleep(20)
    # driver.execute_script("window.scrollBy(0, 2000);")
    # print("스크롤 내림")
    # time.sleep(5)
    # game = driver.find_element('xpath', '//*[@id="SaleSection_13268"]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div[1]/a/div/div[2]/img').click()
    # # driver.find_element_by_link_text
    # print("게임 들어감 & 클릭함")
    # # print("게임 클릭함")
    # time.sleep(5)
    # driver.switch_to.window(driver.window_handles[-1])
    # time.sleep(1)
    # print("탭 전환됨")
    # actions = driver.find_element(By.CSS_SELECTOR, 'body')
    # actions.send_keys(Keys.END)
    # while True:
    #     try:
    #         driver.find_element('xpath', '/html/body/div[1]/div[7]/div[6]/div[3]/div[2]/div[1]/div[6]/div/div/div[16]/div/div[4]/a').click()
    #         print("모든 평가보기 클릭됨")
    #         break  # 요소를 찾았으므로 반복 종료
    #     except:
    #         print("요소를 찾지 못했습니다. 다시 시도합니다.")
    #         driver.execute_script("window.scrollBy(0, 5000);")
    # # driver.execute_script("window.scrollBy(0, 10000);")
    # # print("스크롤 내림")
    # # driver.find_element('xpath', '/html/body/div[1]/div[7]/div[6]/div[3]/div[2]/div[1]/div[6]/div/div/div[16]/div/div[4]/a').click()
    # # print("모든 평가보기 클릭됨")
    # time.sleep(5)
    # driver.close()
    # driver.switch_to.window(driver.window_handles[-1])
    # time.sleep(1)
    # game = driver.find_element('xpath', '//*[@id="SaleSection_13268"]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[1]/a/div/div[2]/img').click()
    # print("뭔가 클릭됨")

# for year in range(2013, 2024):
#     driver.get(url.format(year))
#     time.sleep(2)
#     crawled_titles = []
#     for k in range(1, 13):
#         for i in range(1, 31):
#             title = driver.find_element(By.XPATH, title_path.format(i)).text
#             if title in crawled_titles:
#                 continue
#             crawled_titles.append(title)
#             driver.find_element(By.XPATH, title_path.format(i)).click()
#             time.sleep(0.5)
#             driver.find_element(By.XPATH, button_score_path).click()
#             time.sleep(1)
#             for _ in range(5):
#                 try:
#                     driver.find_element(By.XPATH, button_more_path).click()
#                     time.sleep(1)
#                 except:
#                     print('more', '{} {}'.format(i, _))
#             reviews = []
#             titles = []
#             for j in range(1, 161):
#                 try:
#                     review = driver.find_element(By.XPATH, review_path.format(j)).text
#                     titles.append(title)
#                     reviews.append(review)
#                 except:
#                     print('review', '{} {}'.format(i, j))
#             df = pd.DataFrame({'title':titles, 'reviews':reviews})
#             try:
#                 df.to_csv('./crawling_data/reviews_{}_{}_{}.csv'.format(year, k, i), index=False)
#             except:
#                 print(title)
#             print(len(titles), len(reviews))
#             print(titles)
#             print(reviews)
#             driver.back()
#             time.sleep(0.5)
#             driver.back()
#             time.sleep(0.5)
#         driver.find_element(By.XPATH, button_next_path).click()
#         print(len(crawled_titles))
#         print(crawled_titles)
#
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
# import pandas as pd
# import re
# import time
# import datetime
# import requests
#
# options = ChromeOptions()
# user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
# options.add_argument('user-agent=' + user_agent)
# options.add_argument("lang=ko_KR")
#
# # 크롬 드라이버 최신 버전 설정
# service = ChromeService(executable_path=ChromeDriverManager().install())
#
# # chrome driver
# driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경
#
# url_base = 'https://movie.daum.net/ranking/boxoffice/monthly?date=202309'
#
# df_titles = pd.DataFrame()
#
# for year in range(13, 14):
#     if year == 13:
#         month_start, month_end = 1, 8
#     else:
#         month_start, month_end = 1, 12
#
#     for month in range(month_start, month_end + 1):
#         month_formatted = '{:02}'.format(month)
#         url = 'https://movie.daum.net/ranking/boxoffice/monthly?date=20{}{}'.format(year, month_formatted)
#         driver.get(url)
#         # time.sleep(0.5)   get()가 완전히 사이트를 로드될 때까지 기다리으로 필요없음!
#
#         title = []
#         review = []
#
#         for i in range(1, 31):
#             try:
#                 title_element = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(i)).text
#
#                 # 영화 제목 클릭
#                 driver.find_element('xpath',
#                                     '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(i)).click()
#                 if driver.current_url == 'https://movie.daum.net/moviedb/main?movieId=':
#                     driver.back()
#                     continue    # continue를 사용하여 특정 조건이 충족되었을 때 반복을 건너뛰고 다음 반복 주기로 이동할 수 있습니다.
#
#                 # 평점 클릭
#                 while(1):
#                     try:
#                         driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/div[2]/div[1]/div/div/div')
#                         break
#                     except:
#                         continue
#                 driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span').click()
#                 time.sleep(0.5)
#                 # 리뷰 더보기 5번
#                 for j in range(1, 6):
#                     try:
#                         driver.find_element('xpath', '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button').click()
#                         time.sleep(0.5)
#                     except NoSuchElementException:
#                         break
#                 for k in range(1, 161):
#                     try:
#                         review_element = driver.find_element('xpath', '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(k)).text
#                         review_element = re.compile('[^가-힣]').sub(' ', review_element)
#                         review.append(review_element)
#                         title.append(title_element)
#                     except NoSuchElementException:
#                         pass
#                         # pass는 문법적으로 무언가가 필요하지만 아무 작업을 수행할 필요가 없는 경우에 사용됩니다.
#                         # 예를 들어, 함수나 클래스를 정의할 때 구현 내용이 아직 없는 경우에 사용할 수 있습니다.
#
#                 driver.back()
#                 driver.back()
#
#             except:
#                 print('date_20{}{}_{}'.format(year, month_formatted, i))
#
#         df_data = pd.DataFrame({'title': title, 'review': review})
#         df_data.to_csv('C:/Users/wjgk0/PycharmProjects/pythonProject/crawling_data/data_{}_{}.csv'.format(year, month), index=False)
#
# print(title)
# print(review)