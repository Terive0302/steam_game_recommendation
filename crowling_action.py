# 컬럼명 ['title', 'review']
# 파일명 steam_{카테고리명}.csv
#
# 크롤링 코드명 crawling_steam.py
#
# 카테고리 [ 6 ]
# 세부 카테고리 [ 7 ]
# 게임 [ 150 ] 개
# 리뷰
# 한글 [ 150 ] 개
# 영어 [ 150 ] 개

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# user_agent
options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")


# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())
# chrome driver
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

# 빈 리스트 title, review
get_title = []
get_review = []

# df_save object 빈 데이터 프레임 생성
# 컬럼 title, review
df_save = pd.DataFrame(columns=['title', 'review'])


# 1개의 페이지 당 12게임, 더보기 12번 더 누르면 150번째 나옴.

# https://store.steampowered.com/category/action/?tab=3
# url 이 세부 카테고리의 탭별로 tab 2,3,10,11,12,5,4   // 1
# 액션 어드벤쳐, 액션rpg, 아케이드, 캐쥬얼, 파이터, 오픈월드 플랫폼 , // 슈팅 1

# top sellers xpath
top_sellers = '/html/body/div[1]/div[7]/div[6]/div[4]/div/div/div/div[2]/div/div[2]/div[8]/div[2]/div[2]/div[1]/div/div[3]'

# 더보기 버튼
# /html/body/div[1]/div[7]/div[6]/div[4]/div/div/div/div[2]/div/div[2]/div[8]/div[2]/div[2]/div[2]/div[2]/div/div[13]/button
# /html/body/div[1]/div[7]/div[6]/div[4]/div/div/div/div[2]/div/div[2]/div[8]/div[2]/div[2]/div[2]/div[2]/div/div[25]/button
# /html/body/div[1]/div[7]/div[6]/div[4]/div/div/div/div[2]/div/div[2]/div[8]/div[2]/div[2]/div[2]/div[2]/div/div[37]/button
# /html/body/div[1]/div[7]/div[6]/div[4]/div/div/div/div[2]/div/div[2]/div[8]/div[2]/div[2]/div[2]/div[2]/div/div[49]/button
# https://store.steampowered.com/category/action/?flavor=contenthub_topsellers&tab=2&offset=48
# /html/body/div[1]/div[7]/div[6]/div[4]/div/div/div/div[2]/div/div[2]/div[8]/div[2]/div[2]/div[2]/div[2]/div/div[61]/button
# https://store.steampowered.com/category/action/?flavor=contenthub_topsellers&tab=2&offset=60
page=[0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144, 156]

click_game ='// *[ @ id = "SaleSection_13268"] / div[2] / div[2] / div[2] / div[2] / div / div[{}] / div / div / div / div[1] / a / div / div[2] / img'


act_category = [2, 3, 10, 11, 12, 5, 4]

# 첫번째 for 문 url 접근.
for i in range(len(act_category)):
    # act_category 의 길이만큼 반복.
    # i 는 반복 횟수의 값을 갖음
    # https: // store.steampowered.com / category / action /?tab = 3 & flavor = contenthub_topsellers
    url = 'https://store.steampowered.com/category/action/?tab={}&flavor=contenthub_topsellers'.format(act_category[i])
    driver.get(url)
    # 반복 하여 탭 이동 확인 완료.
    # 페이지 로드이후 더보기 누르기

    for r in range(len(page)):
        driver.get('{}&offset={}'.format(url, page[r]))
        print('-- 게임 목록 페이지 로드 완료--')
        time.sleep(2)
    # 상품 리스트 12개씩 페이지 접근

        time.sleep(2)
        for twelve in range(1,13):
            try:
                game_title = driver.find_element(By.XPATH,
                                                 '//*[@id="SaleSection_13268"]/div[2]/div[2]/div[2]/div[2]/div/div[{}]/div/div/div/div[2]/div[2]/a/div'.format(twelve)).text
                time.sleep(0.5)

                game_url = driver.find_element('xpath',
                                               '// *[ @ id = "SaleSection_13268"] / div[2] / div[2] / div[2] / div[2] / div / div[{}] / div / div / div / div[2] / div[2] / a'.format(twelve)).get_attribute('href')
                time.sleep(2)
                driver.get(game_url)
                time.sleep(1)
                actions = driver.find_element(By.CSS_SELECTOR, 'body')
                time.sleep(1)
                actions.send_keys(Keys.END)
                time.sleep(3)


                all_review = driver.find_element(By.XPATH, '//*[@id="ViewAllReviewssummary"]/a')
                time.sleep(2)

                try:
                    # 모든 리뷰 보기 버튼 찾기 무한반복
                    all_review.click()
                    print('눌렀다')

                except:
                    print('못눌렀다')

                time.sleep(1)

                for review_wait in range(0,30):
                    driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)
                    time.sleep(1.5)


                print('스크롤 내리기 반복 종료')

                for rev in range(0,30):
                    try:
                        copyreview = driver.find_element(By.XPATH,
                                                         '/html/body/div[1]/div[7]/div[5]/div/div[1]/div[3]/div[1]/div[1]/div[{}]/div[2]/div[1]/div[1]/div[3]'.format(
                                                             rev)).text
                        print('text 따기 완료')
                        copyreview = re.compile('[^a-z|A-Z]').sub(' ', copyreview)
                        get_review.append(copyreview)
                        get_title.append(game_title)
                        print('리스트 저장 완료')
                        if rev == 29:
                            break

                    except NoSuchElementException:
                        pass

                driver.find_element(By.XPATH,'//*[@id="language_pulldown"]').click()
                # 딸깍
                driver.find_element(By.XPATH, '//*[@id="language_dropdown"]/div/a[4]').click()
                # 딸깎
                for review_wait in range(0,30):
                    driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)
                    time.sleep(1.5)

                for rev in range(0,30):
                    try:
                        copyreview = driver.find_element(By.XPATH,
                                                         '/html/body/div[1]/div[7]/div[5]/div/div[1]/div[3]/div[1]/div[1]/div[{}]/div[2]/div[1]/div[1]/div[3]'.format(
                                                             rev)).text
                        print('text 따기 완료')
                        copyreview = re.compile('[^가-힣]').sub(' ', copyreview)
                        get_review.append(copyreview)
                        get_title.append(game_title)
                        print('리스트 저장 완료')
                        if rev == 29:
                            break

                    except NoSuchElementException:
                        pass


                print('탈출 완료')
                df_data = pd.DataFrame({'title': get_title, 'review': get_review})
                df_data.to_csv('./data/data_{}.csv'.format(game_title), index=False)
                print('save')
                time.sleep(0.5)
                driver.back()
                driver.back()
                continue

            except:
                time.sleep(0.5)
                driver.back()
                print('연령인증')
                continue






            # 사망방지 1분슬립
            time.sleep(60)

    #마지막에 continue 로 다음번째 for문 반복 실행.













