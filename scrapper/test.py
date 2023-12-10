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

def __main__():
    try:
        #Thong tin chung
        coname = 'VIC'
        project_id = 'rawbctc'
        years = 5 #số năm muốn lấy dữ liệu
        date_range = '01/01/2018 - 31/12/2022'

        # #get price
        # url = 'https://s.cafef.vn/lich-su-giao-dich-vnindex-1.chn#data'
        # table_id='price.'+coname

        # price = gia.Price(url, date_range, table_id, project_id, coname)
        # price.scrape_link()#url, date_range, table_id, project_id, coname)

        # #get report
        # # # 1. Lưu chuyển tiền tệ - Cashflow
        # url = 'https://s.cafef.vn/bao-cao-tai-chinh/vic/cashflow/2018/4/5/0/luu-chuyen-tien-te-gian-tiep-.chn'
        # table_id='cashflow.'+coname
        # report = bctc.Report(url, years, table_id, project_id, coname)
        # report.scrape_link()
        # # 2. Kết quả kinh doanh - Profit and loss
        url = 'https://s.cafef.vn/bao-cao-tai-chinh/vic/incsta/2018/4/0/0/ket-qua-hoat-dong-kinh-doanh-.chn'
        table_id='pnl.'+coname
        report = bctc.Report(url, years, table_id, project_id, coname)
        report.scrape_link()
        
    except Exception as e:
        raise e

__main__()
    
        # coname = 'MCM'
        # # # 1. Lưu chuyển tiền tệ - Cashflow
        # url = 'https://s.cafef.vn/bao-cao-tai-chinh/mcm/cashflow/2020/4/0/0/luu-chuyen-tien-te-gian-tiep-.chn'
        # table_id='cashflow.'+coname
        # report = bctc.Report(url, years,table_id, project_id, coname)
        # report.scrape_link(url, years,table_id, project_id, coname)
        # # # 2. Kết quả kinh doanh - Profit and loss
        # url = 'https://s.cafef.vn/bao-cao-tai-chinh/mcm/incsta/2020/4/0/0/ket-qua-hoat-dong-kinh-doanh-.chn'
        # table_id='pnl.'+coname
        # report = bctc.Report(url, years,table_id, project_id, coname)
        # report.scrape_link(url, years,table_id, project_id, coname)

        # coname = 'FPT'
        # # # 1. Lưu chuyển tiền tệ - Cashflow
        # url = 'https://s.cafef.vn/bao-cao-tai-chinh/fpt/cashflow/2018/4/0/0/ket-qua-hoat-dong-kinh-doanh-.chn'
        # table_id='cashflow.'+coname
        # report = bctc.Report(url, years,table_id, project_id, coname)
        # report.scrape_link(url, years,table_id, project_id, coname)
        # # # 2. Kết quả kinh doanh - Profit and loss
        # url = 'https://s.cafef.vn/bao-cao-tai-chinh/fpt/incsta/2018/4/5/0/ket-qua-hoat-dong-kinh-doanh-.chn'
        # table_id='pnl.'+coname
        # report = bctc.Report(url, years,table_id, project_id, coname)
        # report.scrape_link(url, years,table_id, project_id, coname)

        # coname = 'CMG'
        # # # 1. Lưu chuyển tiền tệ - Cashflow
        # url = 'https://s.cafef.vn/bao-cao-tai-chinh/cmg/cashflow/2018/4/0/0/ket-qua-hoat-dong-kinh-doanh-.chn'
        # table_id='cashflow.'+coname
        # report = bctc.Report(url, years,table_id, project_id, coname)
        # report.scrape_link(url, years,table_id, project_id, coname)
        # # # 2. Kết quả kinh doanh - Profit and loss
        # url = 'https://s.cafef.vn/bao-cao-tai-chinh/cmg/incsta/2018/4/-3/0/ket-qua-hoat-dong-kinh-doanh-.chn'
        # table_id='pnl.'+coname
        # report = bctc.Report(url, years,table_id, project_id, coname)
        # report.scrape_link(url, years,table_id, project_id, coname)

        # coname = 'CMT'
        # # # 1. Lưu chuyển tiền tệ - Cashflow
        # url = 'https://s.cafef.vn/bao-cao-tai-chinh/cmt/cashflow/2018/4/0/0/ket-qua-hoat-dong-kinh-doanh-.chn'
        # table_id='cashflow.'+coname
        # report = bctc.Report(url, years,table_id, project_id, coname)
        # report.scrape_link(url, years,table_id, project_id, coname)
        # # # 2. Kết quả kinh doanh - Profit and loss
        # url = 'https://s.cafef.vn/bao-cao-tai-chinh/cmt/incsta/2018/4/-3/0/ket-qua-hoat-dong-kinh-doanh-.chn'
        # table_id='pnl.'+coname
        # report = bctc.Report(url, years,table_id, project_id, coname)
        # report.scrape_link(url, years,table_id, project_id, coname)

        # coname = 'ELC'
        # # # 1. Lưu chuyển tiền tệ - Cashflow
        # url = 'https://s.cafef.vn/bao-cao-tai-chinh/elc/cashflow/2018/4/-3/0/luu-chuyen-tien-te-gian-tiep-.chn'
        # table_id='cashflow.'+coname
        # report = bctc.Report(url, years,table_id, project_id, coname)
        # report.scrape_link(url, years,table_id, project_id, coname)
        # # # 2. Kết quả kinh doanh - Profit and loss
        # url = 'https://s.cafef.vn/bao-cao-tai-chinh/elc/incsta/2018/4/0/0/luu-chuyen-tien-te-gian-tiep-.chn'
        # table_id='pnl.'+coname
        # report = bctc.Report(url, years,table_id, project_id, coname)
        # report.scrape_link(url, years,table_id, project_id, coname)