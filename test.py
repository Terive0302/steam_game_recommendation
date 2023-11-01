from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
import time


df_game = pd.DataFrame()
category = ('/sim_building_automation/', '/sim_farming_crafting/', '/sim_physics_sandbox/', '/sim_life/',
            '/sim_dating/', '/sim_space_flight/', '/sim_hobby_sim/')
for i in range(len(category)):
    page = 0
    df_game.to_csv('./crawling_data/steam_{}_{}.csv'.format(category[i][1:-1], page))
