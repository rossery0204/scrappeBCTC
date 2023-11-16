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

def validate_headers(cell):
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

def bs4_scrapper(url, coname):
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    df = get_table_contents(soup, coname)
    df = df.transpose().reset_index()
    df.columns = df.iloc[0]
    df = df[1:]
    return df

def get_table_headers(soup, coname):
    headers = []
    tb_header = soup.find('table', {'id':'tblGridData'})
    row = tb_header.find('tr')
    for cell in row.find_all('td'):
        #chuẩn hóa để đẩy lên gbq
        cell = cell.text.strip()
        cell = unidecode(cell)
        cell = cell.replace('-','_')
        cell = cell.replace(' ','')
        headers.append(cell+'_'+coname)
    headers[0] = "Thoi_gian"
    return headers

def get_table_contents(soup, coname):
    tb_content = soup.find('table', {'id':'tableContent'})
    headers = get_table_headers(soup, coname)
    df = pd.DataFrame(columns = headers)
    for row in tb_content.find_all('tr'):
        row_content = []
        cell_number = 1
        for cell in row.find_all('td',{'class':'b_r_c'}):
            cell = cell.text.strip()
            if (cell_number == 1):
                cell = validate_headers(cell)
            row_content.append(unidecode(cell))
            cell_number += 1
        if row_content:
            length = len(df) + 1
            df.loc[length] = row_content 
    return df

def save_file(df, table_id, project_id):
    print('---------------')
    ## Mở ra khi cần lưu file local
    # path = 'E:/20231/DA2/DA2code/data/raw_data/cashflow/' #thư mục lưu
    # file_path = path + str(curr_year) + '.csv'
    # if os.path.exists(file_path):
    #     print("File da ton tai!")
    #     os.remove(file_path)
    # df.to_csv(file_path, index=False, encoding='utf-8-sig')
    # print(df)
    pandas_gbq.to_gbq(df, table_id, project_id=project_id,if_exists='append')
    print("Đã lưu", table_id)

def scrape_link(url, years,table_id, project_id, coname):
    driver = webdriver.Chrome()
    driver.get(url)
    for i in range(years):
        count = 0
        df = bs4_scrapper(driver.current_url, coname)
        # print(df)
        # print("Column headers from list(df.columns.values):",list(df.columns.values))
        save_file(df, table_id, project_id)
        while (count < 4):
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Sau')]"))
            )   
            element.click()  
            count += 1
    driver.quit()

try:
    project_id = 'rawbctc'
    years = 3 #số năm muốn lấy dữ liệu

    coname = 'VNM'
    # # Danh sách link dùng  
    # # 1. Lưu chuyển tiền tệ - Cashflow
    url = 'https://s.cafef.vn/bao-cao-tai-chinh/vnm/cashflow/2020/4/8/0/luu-chuyen-tien-te-gian-tiep-.chn'
    table_id='cashflow.'+coname
    scrape_link(url, years,table_id, project_id, coname)
    # # 2. Kết quả kinh doanh - Profit and loss
    url = 'https://s.cafef.vn/bao-cao-tai-chinh/vnm/incsta/2020/4/0/0/luu-chuyen-tien-te-gian-tiep-.chn'
    table_id='pnl.'+coname
    scrape_link(url, years,table_id, project_id, coname)

    coname = 'MCM'
    # # Danh sách link dùng  
    # # 1. Lưu chuyển tiền tệ - Cashflow
    url = 'https://s.cafef.vn/bao-cao-tai-chinh/mcm/cashflow/2020/4/0/0/luu-chuyen-tien-te-gian-tiep-.chn'
    table_id='cashflow.'+coname
    scrape_link(url, years,table_id, project_id, coname)
    # # 2. Kết quả kinh doanh - Profit and loss
    url = 'https://s.cafef.vn/bao-cao-tai-chinh/mcm/incsta/2020/4/0/0/ket-qua-hoat-dong-kinh-doanh-.chn'
    table_id='pnl.'+coname
    scrape_link(url, years,table_id, project_id, coname)
    
except Exception as e:
    raise e
    
    



