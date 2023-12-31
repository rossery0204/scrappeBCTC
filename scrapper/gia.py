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
import logging
from datetime import datetime

class Price :
    def __init__(self, url, date_range, table_id, project_id, coname):
        self.url = url
        self.date_range = date_range
        self.table_id = table_id
        self.project_id = project_id
        self.coname = coname

    # #define headers
    # def get_table_headers(): 
    #     headers = ['maCK', 'ngay', 'gia_dong_nghinVND', 'gia_dieu_chinh_nghinVND', 'thay_doi', 'GDKL_khoiluong', 'GDKL_giatri_tyVND', 'GDTT_khoiluong', 'GDTT_giatri_tyVND', 'gia_mo_nghinVND', 'gia_cao_nhat_nghinVND', 'gia_thap_nhat_nghinVND']
    #     df = pd.DataFrame(columns = headers)
    #     return df

    #get content of table and define headers
    def get_table_contents(self, driver, df):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        tb_content = soup.find('tbody', {'id':'render-table-owner'})
        for row in tb_content.find_all('tr'):
            row_content = []
            row_content.append(self.coname)
            for cell in row.find_all('td'):
                cell = cell.text.strip()
                row_content.append(cell)
            row_content.append(datetime.today().strftime('%d/%m/%Y'))
            if row_content:
                length = len(df) + 1
                df.loc[length] = row_content 
        return df

    #get html
    def select_data (self, driver): 
        #input company name
        input_coname = driver.find_element(By.XPATH, "//input[@id = 'ContentPlaceHolder1_ctl00_acp_inp_disclosure']")
        input_coname.send_keys(self.coname)

        #input date range
        input_daterange = driver.find_element(By.XPATH, "//input[@id = 'date-inp-disclosure']")
        input_daterange.send_keys(self.date_range)
        date_selection = driver.find_element(By.XPATH, "//button[@class = 'applyBtn btn btn-sm btn-primary']")
        date_selection.click()
        
        #click find button
        find_button = driver.find_element(By.XPATH, "//div[@id = 'owner-find']")
        find_button.click()
        return driver

    def save_file(self, df):#, table_id, project_id):
        pandas_gbq.to_gbq(df, self.table_id, project_id=self.project_id, if_exists='append')

    def bs4_scrapper(self): #, url, coname, date_range):
        driver = webdriver.Chrome()
        driver.get(self.url)
        #df = self.get_table_headers()
        headers = ['maCK', 'ngay', 'gia_dong_nghinVND', 'gia_dieu_chinh_nghinVND', 'thay_doi', 'GDKL_khoiluong', 'GDKL_giatri_tyVND', 'GDTT_khoiluong', 'GDTT_giatri_tyVND', 'gia_mo_nghinVND', 'gia_cao_nhat_nghinVND', 'gia_thap_nhat_nghinVND', 'Ngay_lay_du_lieu']
        df = pd.DataFrame(columns = headers)
        driver = self.select_data(driver)
        time.sleep(2)
        while (True):
            df = self.get_table_contents(driver, df)
            next_page = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//i[@id = 'paging-right']"))
            )   
            next_page.click()
            if driver.find_elements(By.XPATH, "//i[@class = 'fa fa-chevron-right enable']"):
                df = self. get_table_contents(driver, df)
                break
        driver.quit()
        return df
        
    def scrape_link(self): #, url, date_range, table_id, project_id, coname):  
        df = self.bs4_scrapper()#url, coname, date_range)
        self.save_file(df) #, table_id, project_id)





