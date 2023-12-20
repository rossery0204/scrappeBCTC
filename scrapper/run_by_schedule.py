from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import os
import pandas_gbq
from unidecode import unidecode
import re
import time
from selenium.webdriver.common.action_chains import ActionChains
import gia
import bctc
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from datetime import datetime

def __main__():
    #get today date and format
    today = datetime.today().strftime('%d/%m/%Y - %d/%m/%Y')

    # #initialize the log settings
    # formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # logger = logging.getLogger('RotatingFileHandler')

    # # Split log on Sunday everyweek
    # handler = TimedRotatingFileHandler('scrapper\\log\\time_log_file.log', when="w6", interval=1)
    # handler.setFormatter(formatter)
    # handler.setLevel(logging.DEBUG)
    # logger.addHandler(handler)

    logging.basicConfig(filename='E:\\20231\\DA2\\DA2code\\scrapper\\log\\log_da2.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    #Thong tin chung
    project_id = 'rawbctc'

    try:
        #Input cac cong ty muon theo doi gia hang ngay
        coname_list = ['FPT', 'CMG', 'ELC']
        url = 'https://s.cafef.vn/lich-su-giao-dich-vnindex-1.chn#data'
        for coname in coname_list:
            table_id='price.'+coname
            price = gia.Price(url, today, table_id, project_id, coname)
            price.scrape_link()        
        logging.info("Succeed in scrapping price today")
    except:
        logging.error("Fail to scrappe price today")

__main__()