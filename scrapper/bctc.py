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
import logging
from datetime import datetime

class Report:
    def __init__(self, url, years, table_id, project_id, coname):
        self.url = url
        self.years = years
        self.table_id = table_id
        self.project_id = project_id
        self.coname = coname

    def validate_header(self, cell):
        self.cell = cell
        cell = re.sub("[0-9]", '', cell)
        cell = re.sub("[+]", '', cell)
        cell = cell.replace('.','')
        cell = cell.replace(',','')
        cell = cell.replace('-','')
        cell = cell.replace('=','')
        cell = cell.replace(')','')
        cell = cell.replace('(','')
        cell = cell.replace('I','')
        cell = cell.replace(':','_')
        cell = cell.replace('{','')
        cell = cell.replace('}','')
        cell = cell.replace('*','')
        cell = cell.strip()
        cell = cell.replace(' ','_')
        return cell

    def bs4_scrapper(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text,'html.parser')
        df = self.get_table_contents(soup)
        df = df.transpose().reset_index()
        df.columns = df.iloc[0]
        df = df[1:]
        return df

    def get_table_headers(self, soup:BeautifulSoup):
        headers = []
        tb_header = soup.find('table', {'id':'tblGridData'})
        row = tb_header.find('tr')
        for cell in row.find_all('td'):
            #chuẩn hóa để đẩy lên gbq
            cell = cell.text.strip()
            cell = unidecode(cell)
            cell = cell.replace('-','_')
            cell = cell.replace(' ','')
            headers.append(cell+'_'+self.coname)
        headers[0] = "Thoi_gian"
        return headers

    def get_table_contents(self, soup:BeautifulSoup):
        tb_content = soup.find('table', {'id':'tableContent'})
        headers = self.get_table_headers(soup)
        df = pd.DataFrame(columns = headers)
        rows = tb_content.find_all('tr')
        for row in rows:
            row_content = []
            cell_number = 1
            for cell in row.find_all('td',{'class':'b_r_c'}):
                cell = cell.text.strip()
                if (cell_number == 1):
                    cell = self.validate_header(cell)
                row_content.append(unidecode(cell))
                cell_number += 1
            if row_content:
                length = len(df) + 1
                df.loc[length] = row_content
        #Them ngay lay du lieu
        special_row = ['Ngay_lay_du_lieu']
        for i in range(len(headers)-1):
            special_row.append(datetime.today().strftime('%d/%m/%y'))
        length = len(df) + 1
        df.loc[length] = special_row
        return df

    def save_file(self, df):
        ## Mở ra khi cần lưu file local
        # path = 'E:/20231/DA2/DA2code/data/raw_data/cashflow/' #thư mục lưu
        # file_path = path + str(curr_year) + '.csv'
        # if os.path.exists(file_path):
        #     print("File da ton tai!")
        #     os.remove(file_path)
        # df.to_csv(file_path, index=False, encoding='utf-8-sig')
        # print(df)
        pandas_gbq.to_gbq(df, self.table_id, project_id=self.project_id,if_exists='append')

    def scrape_link(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        for i in range(self.years):
            count = 0
            df = self.bs4_scrapper(driver.current_url)
            # print(df)
            # print("Column headers from list(df.columns.values):",list(df.columns.values))
            self.save_file(df)
            while (count < 4):
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Sau')]"))
                )   
                element.click()  
                count += 1
        driver.quit()



    
    




