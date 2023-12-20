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

def do_selection_1(project_id):
    coname = input("Nhap ten cong ty: ")
    years = int(input("Nhap so nam muon lay du lieu: "))

    #cashflow
    url = input("Nhap url cashflow: ")
    table_id='cashflow.'+coname
    report = bctc.Report(url, years, table_id, project_id, coname)
    report.scrape_link()

    #pnl
    url = input("Nhap url pnl: ")
    table_id='pnl.'+coname

    logging.info('Get PNL report: Cong ty:',coname,'; So nam:',years,'; Url:',url)

    report = bctc.Report(url, years, table_id, project_id, coname)
    report.scrape_link()

def do_selection_2(project_id):
    coname = input("Nhap ten cong ty: ")
    years = int(input("Nhap so nam muon lay du lieu: "))
    date_range = input("Nhap khoang thoi gian theo dinh dang: DD/MM/YYYY - DD/MM/YYYY: ")

    #price
    url = 'https://s.cafef.vn/lich-su-giao-dich-vnindex-1.chn#data'
    table_id='price.'+coname
    price = gia.Price(url, date_range, table_id, project_id, coname)
    price.scrape_link()

    #cashflow
    url = input("Nhap url cashflow: ")
    table_id='cashflow.'+coname
    report = bctc.Report(url, years, table_id, project_id, coname)
    report.scrape_link()

    #pnl
    url = input("Nhap url pnl: ")
    table_id='pnl.'+coname
    report = bctc.Report(url, years, table_id, project_id, coname)
    report.scrape_link()
    
def __main__():

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
    print("Chon chuong trinh:")
    print("1 - Chi lay du lieu bao cao tai chinh")
    print("2 - Lay du lieu bao cao tai chinh va gia")

    while (True):
        try:
            selection = int(input("Moi chon: "))
            if (selection == 1):
                do_selection_1(project_id)    
                logging.info('Success to scrape by trigger')     
                break
            elif (selection == 2):
                do_selection_2(project_id)
                logging.info('Success to scrape by trigger')
                break
            else:
                continue
        except:
            logging.error('Fail to scrape by trigger')

__main__()

        # coname = 'VIC'
        # years = 5 #số năm muốn lấy dữ liệu
        # date_range = '01/01/2018 - 31/12/2022'

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
        # url = 'https://s.cafef.vn/bao-cao-tai-chinh/vic/incsta/2018/4/0/0/ket-qua-hoat-dong-kinh-doanh-.chn'
        # table_id='pnl.'+coname
        # report = bctc.Report(url, years, table_id, project_id, coname)
        # report.scrape_link()
    
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