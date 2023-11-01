
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

service = ChromeService(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

home_url = 'https://store.steampowered.com/category/rpg_jrpg/'
jrpg_url = 'https://store.steampowered.com/category/rpg_jrpg/?flavor=contenthub_topsellers'
rogue_url = 'https://store.steampowered.com/category/rogue_like_rogue_lite/?flavor=contenthub_topsellers'
action_url = 'https://store.steampowered.com/category/rpg_action/?flavor=contenthub_topsellers'
adventure_url = 'https://store.steampowered.com/category/adventure_rpg/?flavor=contenthub_topsellers'
strategy_url = 'https://store.steampowered.com/category/rpg_strategy_tactics/?flavor=contenthub_topsellers'
turn_url = 'https://store.steampowered.com/category/rpg_turn_based/?flavor=contenthub_topsellers'
party_url = 'https://store.steampowered.com/category/rpg_party_based/?flavor=contenthub_topsellers'

urls = [
    'https://store.steampowered.com/category/rpg_jrpg/?flavor=contenthub_topsellers',
    'https://store.steampowered.com/category/rogue_like_rogue_lite/?flavor=contenthub_topsellers',
    'https://store.steampowered.com/category/rpg_action/?flavor=contenthub_topsellers',
    'https://store.steampowered.com/category/adventure_rpg/?flavor=contenthub_topsellers',
    'https://store.steampowered.com/category/rpg_strategy_tactics/?flavor=contenthub_topsellers',
    'https://store.steampowered.com/category/rpg_turn_based/?flavor=contenthub_topsellers',
    'https://store.steampowered.com/category/rpg_party_based/?flavor=contenthub_topsellers'
]

df_steam = pd.DataFrame()
title = []
review = []

driver.get(home_url)
time.sleep(1)
driver.find_element('xpath', '/html/body/div[1]/div[7]/div[1]/div/div[3]/div/span').click()
print("언어 클릭됨")
time.sleep(1)
driver.find_element('xpath', '/html/body/div[1]/div[7]/div[1]/div/div[3]/div/div/div/a[4]').click()
print("한국어 변경")
time.sleep(2)

for url in urls:
    driver.get(url)
    print("최고 인기 제품")
    time.sleep(2)

    # actions = driver.find_element(By.CSS_SELECTOR, 'body')
    # actions.send_keys(Keys.END)
    # time.sleep(0.1)

    count = 0
    flag = 0
    no_checker = 0

    for page in range(1, 150):
        title = []
        review = []
        driver.get(url+'&offset={}'.format(page))
        time.sleep(2) # 오프셋 1씩 증가
        try:
            game_url = driver.find_element('xpath', '//*[@id="SaleSection_13268"]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[2]/a').get_attribute('href')
            game_title = driver.find_element('xpath', '//*[@id="SaleSection_13268"]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div[2]/a').text
            if '/' in game_title:
                game_title = game_title.replace('/', ' ')
            print(game_title)
            # try:
            #     driver.find_element(By.CLASS_NAME, 'gamehover_ReviewScoreCount_1Deyv')
            # except:
            #     continue
            # else:
            #     pass
            driver.get(game_url) # 1번째 링크 들어가기
            while driver.execute_script("return document.readyState") != "complete":
                time.sleep(1) # 로딩 될 때까지 대기
            actions = driver.find_element(By.CSS_SELECTOR, 'body')
            actions.send_keys(Keys.END) # End키 누르기
            # driver .execute_script("window.scrollBy(0, 30000);")
            time.sleep(3) # 로딩되는 거 잠깐 기다림
        except:
            print(f"{page}번째 게임 오류")
            continue
        try:
            actions = driver.find_element(By.CSS_SELECTOR, 'body')
            actions.send_keys(Keys.END) # 한 번더 End키 누르기
            time.sleep(2)
            driver.find_element('xpath', '/html/body/div[1]/div[7]/div[6]/div[3]/div[2]/div[1]/div[6]/div/div/div[16]/div/div[4]/a').click()
            time.sleep(2) # 모든 평가 보기 클릭
        except:
            print("모든 평가 보기 없음")
            time.sleep(1)
            continue

        # 불건전한 리뷰 스킵
        try:
            driver.find_element(By.CLASS_NAME, 'contentcheck_header')
        except:
            pass
        else:
            continue

        current_url = driver.current_url
        current_url = current_url + "&filterLanguage=english"
        driver.get(current_url) # 영어 리뷰로 바꾸기
        time.sleep(3)

        count = 0
        flag = 0
        no_checker = 0
        for first in range(1, 101):  # div[first]/div[]/div[] # 1 ~ 100까지 증가
            if no_checker > 50:
                break
            if flag == 1:
                break
            actions = driver.find_element(By.CSS_SELECTOR, 'body')
            actions.send_keys(Keys.END)  # End키 누르기
            time.sleep(2)  # 로딩되는 거 잠깐 기다림
            for second in range(1, 10):  # div[]/div[second]/div[] # 1 ~ 10까지 증가
                if flag == 1:
                    break
                for third in range(2, 6):  # div[]/div[]/div[third] # 2 ~ 5까지 증가
                    if flag == 1:
                        break
                    if count > 150:
                        flag = 1
                    try:
                        rv = driver.find_element('xpath',
                                                 f'/html/body/div[1]/div[7]/div[5]/div/div[1]/div[3]/div[1]/div[{first}]/div[{second}]/div[{third}]/div[1]/div[1]/div[3]').text
                        rv = re.compile('[^가-힣|a-z|A-Z]').sub(' ', rv)
                        print(rv)
                        title.append(game_title)
                        review.append(rv)
                        count = count + 1
                        print('영어-count {}'.format(count))
                        no_checker = 0
                    except:
                        # pass
                        print(f"ENG error : {first}_{second}_{third}")
                        no_checker = no_checker + 1
                        print('영어-no_more 체커 {}'.format(no_checker))

        current_url = driver.current_url
        current_url = current_url + "&filterLanguage=koreana"
        driver.get(current_url) # 한국어 리뷰로 바꾸기
        time.sleep(3)

        count = 0
        flag = 0
        no_checker = 0
        for first in range(1, 101):  # div[first]/div[]/div[] # 1 ~ 100까지 증가
            if no_checker > 50:
                break
            if flag == 1:
                break
            actions = driver.find_element(By.CSS_SELECTOR, 'body')
            actions.send_keys(Keys.END)  # End키 누르기
            time.sleep(2)  # 로딩되는 거 잠깐 기다림
            for second in range(1, 10):  # div[]/div[second]/div[] # 1 ~ 10까지 증가
                if flag == 1:
                    break
                for third in range(2, 6):  # div[]/div[]/div[third] # 2 ~ 5까지 증가
                    if flag == 1:
                        break
                    if count > 150:
                        flag = 1
                    try:
                        rv = driver.find_element('xpath',
                                                 f'/html/body/div[1]/div[7]/div[5]/div/div[1]/div[3]/div[1]/div[{first}]/div[{second}]/div[{third}]/div[1]/div[1]/div[3]').text
                        rv = re.compile('[^가-힣|a-z|A-Z]').sub(' ', rv)
                        print(rv)
                        title.append(game_title)
                        review.append(rv)
                        count = count + 1
                        print('한글-count {}'.format(count))

                        no_checker = 0
                    except:
                        # pass
                        print(f"KOR error : {first}_{second}_{third}")
                        no_checker = no_checker + 1
                        print('한글-no_more 체커 {}'.format(no_checker))

        count = 0
        current_url = driver.current_url
        current_url = current_url + "&filterLanguage=english"
        driver.get(current_url) # 영어 리뷰로 바꾸기
        time.sleep(3)

        print(title)
        print(review)

        df_steam = pd.DataFrame({'title':title, 'review':review})
        df_steam.to_csv('./crawling_data/steam_{}_{}.csv'.format(page, game_title), index=False)

