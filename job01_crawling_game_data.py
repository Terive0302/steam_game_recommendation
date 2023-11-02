from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
import time



options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


url = 'https://store.steampowered.com/category'

df_game = pd.DataFrame()
flag = 0
# category = ('/sim_building_automation/', '/sim_farming_crafting/', '/sim_physics_sandbox/', '/sim_life/',
#             '/sim_dating/', '/sim_space_flight/', '/sim_hobby_sim/')
category = '/simulation/'
# for i in range(1,len(category)):
page = 0
for _ in range(50):
    section_url = url + category + '?flavor=contenthub_topsellers&offset=' + str(page)
    driver.get(section_url)
    time.sleep(0.5)
    if flag == 0:
        flag = 1
        click_language1 = driver.find_element('xpath', '//*[@id="language_pulldown"]').click()
        click_language2 = driver.find_element('xpath', '//*[@id="language_dropdown"]/div/a[4]').click()
        time.sleep(2)
    actions = driver.execute_script('return window.pageYOffset')
    driver.execute_script('window.scrollTo(0,{})'.format(actions + 500))
    time.sleep(5)
    titles = []
    reviews = []
    for j in range(1, 13):
        time.sleep(5)
        while (True):
            try:
                game_url = driver.find_element('xpath','/html/body/div[1]/div[7]/div[6]/div[4]/div/div/div/div/div/div[2]/div[9]/div[2]/div[2]/div[2]/div[2]/div/div[{}]/div/div/div/div[2]/div[2]/a'.format(j)).get_attribute('href')
                break
            except:
                try:
                    game_url = driver.find_element('xpath','/html/body/div[1]/div[7]/div[6]/div[4]/div/div/div/div[2]/div/div[2]/div[9]/div[2]/div[2]/div[2]/div[2]/div/div[{}]/div/div/div/div[2]/div[2]/a'.format(j)).get_attribute('href')
                    break
                except:
                    print('.', end='')
                    driver.execute_script('window.scrollTo(0,{})'.format(actions + 100))
        driver.get(game_url)
        actions = driver.find_element(By.CSS_SELECTOR, 'body')
        actions.send_keys(Keys.END)
        time.sleep(5)
        try:
            click_review = driver.find_element('xpath', '//*[@id="ViewAllReviewssummary"]/a').click()
            try:
                click_review2 = driver.find_element('xpath', '//*[@id="responsive_page_template_content"]/div/div/div[2]/button[1]/span').click()
            except:
                print('',end='')
        except:
            driver.get(section_url)
            continue
        for z in range(2):
            count = 0
            for k in range(1,20):
                if count > 150:
                    break
                for x in range(1,8):
                    if count > 150:
                        break
                    actions = driver.find_element(By.CSS_SELECTOR, 'body')
                    actions.send_keys(Keys.END)
                    time.sleep(0.2)
                    for y in range(2,5):
                        try:
                            title = driver.find_element('xpath', '//*[@id="ModalContentContainer"]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]').text
                            review = driver.find_element('xpath', '/html/body/div[1]/div[7]/div[5]/div/div[1]/div[3]/div[1]/div[{}]/div[{}]/div[{}]/div[1]/div[1]/div[3]'.format(k,x,y)).text
                            review = re.compile('[^가-힣|a-z|A-Z]').sub(' ', review)
                            print('{}. {} : {}'.format(count, title, review))
                            count +=1
                            titles.append(title)
                            reviews.append(review)
                            if count > 150:
                                break
                        except:
                            print('', end='')
            try:
                click_language1 = driver.find_element('xpath', '//*[@id="filterlanguage_activeday"]').click()
                click_language2 = driver.find_element('xpath', '//*[@id="filterlanguage_option_5"]').click()
            except:
                print('..')
        driver.get(section_url)
    df_game = pd.DataFrame({'title':titles, 'review':reviews})
    df_game.to_csv('./crawling_data/steam_{}_{}.csv'.format(category[1:-1],page), index=False)
    print('save csv')
    page += 12


