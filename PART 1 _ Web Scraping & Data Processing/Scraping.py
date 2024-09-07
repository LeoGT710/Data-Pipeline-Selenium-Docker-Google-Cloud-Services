from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from google.cloud import logging_v2
from google.oauth2 import service_account
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import time
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery
#import pandas_gbq
import os
import openpyxl
from selenium.webdriver import ActionChains
from datetime import datetime, timedelta
import glob
import json

os.environ['TZ']='Asia/Ho_Chi_Minh'
current_date_momo = datetime.now().strftime("%d_%m_%G")
current_date_grab = datetime.now().strftime("%G-%m-%d")
# Function for web scraping and data cleaning
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument("user-agent=your-custom-user-agent")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--start-fullscreen")
chrome_options.add_argument("--window-size=1920,1080")
#chrome_options.add_argument("--download_default_directory=/Users/hungle/Python Project")

file_path = '/app/accounting_sale_detail.xlsx'
key_path = '/app/Key_1.json'
thuchi_path = '/app/cash_in_cash_out_report.xlsx'
ketca_path = '/app/list_shift_report.xlsx'
momo_path = f'/app/Transaction_report_{current_date_momo}.csv'
grab_path = f'/app/Transaction_Store_{current_date_grab}_to_{current_date_grab}_*.csv'
spf_path = '/app/merchant_order_report_*.xlsx'

clean_file = ['/app/*.csv','/Users/hungle/Python Project/*.csv','/app/*.xlsx','/Users/hungle/Python Project/*.xlsx']

for i in clean_file:
    print(i)
    try:
        csv_files = None
        csv_files = glob.glob(i)
        for file in csv_files:
            os.remove(file)
    except Exception as e:
        print(e)

def ipos_sales():
    print("Running ipos_sale()")
    max_reties = 3
    retry_delay = 30
    for attempt in range(max_reties):
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options= chrome_options)
                      
            #Navigate to the website
            driver.get("******")
            print(driver.title)
            # Wait until the page is fully loaded
            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            # Find the input fields by name
            username_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div[2]/div/div[2]/form/div[1]/input')
            username_input.send_keys("******")
            time.sleep(5)
            password_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div[2]/div/div[2]/form/div[2]/div/input')
            password_input.send_keys("******")
            time.sleep(5)
          
           # Add WebDriverWait for each step after page navigation
            login_element = '/html/body/div/div/div[1]/div[2]/div/div[2]/div/div[2]/form/div[3]/button'
            baocao_element = '/html/body/div/div[1]/div[4]/div/div/div[1]/div[8]/div/img'
            baocaoketoan_element = '/html/body/div/div[2]/div/div/div[4]/div[1]/div[1]/span'
            d05_element = '/html/body/div/div[2]/div/div/div[4]/div[2]/div/div[5]/a/div/span'
            xuatbaocao_element = '/html/body/div/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/div/div[2]'
            xuatbaocaoall_element = '/html/body/div/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/div/div[2]/ul/li[2]/a'

            wait.until(EC.element_to_be_clickable((By.XPATH, login_element))).click()
            time.sleep(15)
            print(driver.title)
            x = wait.until(EC.element_to_be_clickable((By.XPATH, baocao_element)))
            x.click()
            time.sleep(15)
            print('baocao_element'+ driver.title)
            wait.until(EC.element_to_be_clickable((By.XPATH, baocaoketoan_element))).click()
            time.sleep(15)
            print('baocaoketoan_element'+driver.title)

            wait.until(EC.element_to_be_clickable((By.XPATH,d05_element))).click()
            print('d05_element'+driver.title)
            time.sleep(15)

            x = wait.until(EC.element_to_be_clickable((By.XPATH, xuatbaocao_element)))
            x.click()
            #driver.execute_script("arguments[0].click();", x)
            time.sleep(15)

            print('xuatbaocao_element'+driver.title)
            y = wait.until(EC.element_to_be_clickable((By.XPATH,xuatbaocaoall_element)))
            driver.execute_script("arguments[0].click();", y)
            time.sleep(60)
            print('xuatbaocaoall_element'+driver.title)
            
            driver.quit()

            file_content = pd.read_excel(file_path,sheet_name= 'Tất cả cửa hàng',skiprows=1)
            df = file_content[0:-1]
            new_column = ['CUA_HANG','MA_HANG','TEN_HANG','NHOM_MON','LOAI_MON','PTTT','NGUON','BAN','HOA_DON','SO_HOA_DON','NGAY','GIO','SO_LUONG','DON_VI_TINH','GIA','GIA_BAN','THANH_TIEN','GIAM_GIA','CHIET_KHAU','PHI_HO_TRO_MKT','PHIEU_GIAM_GIA','PHI_DICH_VU','VAT','THUE','GIAM_GIA_VAT','PHI_SHIP','TONG_TIEN_KHONG_VAT','HOA_HONG','TONG_TIEN_BAO_GOM_HOA_HONG','TEN_CTKM','MA_VOUCHER','TEN_KHACH','SO_KHACH','SO_DIEN_THOAI','TONG_TIEN']
            df.columns = new_column
            df.loc[:,'SO_HOA_DON'] = df.loc[:,'SO_HOA_DON'].astype(str)
            df.loc[:,'TEN_CTKM':'SO_DIEN_THOAI']= df.loc[:,'TEN_CTKM':'SO_DIEN_THOAI'].astype(str)
            df.loc[:,'NGAY'] = pd.to_datetime(df.loc[:,'NGAY'],dayfirst=True)#.dt.strftime('%d/%m/%Y')
            try:
                os.remove(file_path)
                print('File deleted successfully')
            except OSError as e:
                print(f'Error deleting the file: {e}')
            print(df)
            return df
        except Exception as e: 
            if attempt <max_reties - 1: 
                print(f'Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds')
                time.sleep (retry_delay)
            else: 
                print(f'Failed after {max_reties} attemps: {e}')
                
def ipos_thuchi():
    print("Running ipos_thuchi()")
    max_reties = 1
    retry_delay = 30
    for attempt in range(max_reties):
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options= chrome_options)          
            #Navigate to the website
            driver.get("****")
            print(driver.title)
            # Wait until the page is fully loaded
            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            # Find the input fields by name
            username_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div[2]/div/div[2]/form/div[1]/input')
            username_input.send_keys("*****")
            time.sleep(5)
            password_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div[2]/div/div[2]/form/div[2]/div/input')
            password_input.send_keys("*****")
            time.sleep(5)
           # Add WebDriverWait for each step after page navigation
            login_element = '/html/body/div/div/div[1]/div[2]/div/div[2]/div/div[2]/form/div[3]/button'
            baocao_element = '/html/body/div/div[1]/div[4]/div/div/div[1]/div[8]/div/img'
            baocaoketoan_element = '/html/body/div/div[2]/div/div/div[4]/div[1]/div[1]/span'
            d03_element = '/html/body/div/div[2]/div/div/div[4]/div[2]/div/div[3]/a/div/span'
            xuatbaocao_element = '/html/body/div/div[3]/div[1]/div[1]/div[1]/div[1]/div/div/div/div[7]/button'
            xuatbaocaoall_element = '/html/body/div/div[3]/div[1]/div[1]/div[1]/div[1]/div/div/div/div[7]/ul/li[2]/a'

            wait.until(EC.element_to_be_clickable((By.XPATH, login_element))).click()
            time.sleep(15)
            print(driver.title)
            x = wait.until(EC.element_to_be_clickable((By.XPATH, baocao_element)))
            x.click()
            time.sleep(15)
            print('baocao_element'+ driver.title)
            wait.until(EC.element_to_be_clickable((By.XPATH, baocaoketoan_element))).click()
            time.sleep(15)
            print('baocaoketoan_element'+driver.title)

            wait.until(EC.element_to_be_clickable((By.XPATH,d03_element))).click()
            print('d05_element'+driver.title)
            time.sleep(15)

            x = wait.until(EC.element_to_be_clickable((By.XPATH, xuatbaocao_element)))
            x.click()
            time.sleep(15)

            print('xuatbaocao_element'+driver.title)
            y = wait.until(EC.element_to_be_clickable((By.XPATH,xuatbaocaoall_element)))
            driver.execute_script("arguments[0].click();", y)
            time.sleep(60)
            print('xuatbaocaoall_element'+driver.title)
            
            driver.quit()
            
            dummy_table = {'MA_CA':'','NHAN_VIEN':'','THOI_GIAN':'','LOAI':'','NGHIEP_VU':'','PTTT':'','GHICHU':'','SO_TIEN':'','STORE':''}
            thuchi = pd.DataFrame()
            
            try:
                
                excel_file = pd.ExcelFile(thuchi_path)
                sheetname = excel_file.sheet_names
                for sheet in sheetname:
                    df = excel_file.parse(sheet,skiprows=1)
                    df = df[:-2]
                    df['STORE']=sheet
                    thuchi=pd.concat([thuchi,df])
                new_column = ['MA_CA','NHAN_VIEN','THOI_GIAN','LOAI','NGHIEP_VU','PTTT','GHICHU','SO_TIEN','STORE']
                thuchi.columns=new_column
                #thuchi.loc[:,'THOI_GIAN'] = pd.to_datetime(thuchi.loc[:'THOI_GIAN'],dayfirst=True)
                thuchi.loc[:,'THOI_GIAN']=pd.to_datetime(thuchi.loc[:,'THOI_GIAN'],dayfirst=True)
                
                #thuchi.to_csv('THUCHI.CSV')
                os.remove(thuchi_path) 
            except (FileNotFoundError, pd.errors.ParserError, KeyError, PermissionError, OSError) as e:
                print(f"An error occurred: {e}")
            
            return thuchi

        except Exception as e: 
            if attempt <max_reties - 1: 
                print(f'Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds')
                time.sleep (retry_delay)
            else: 
                print(f'Failed after {max_reties} attemps: {e}')

def ipos_ketca():
    print("Running ipos_ketca")
    max_reties = 3
    retry_delay = 30
    for attempt in range(max_reties):
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options= chrome_options)          
            #Navigate to the website
            driver.get("*****")
            print(driver.title)
            # Wait until the page is fully loaded
            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            # Find the input fields by name
            username_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div[2]/div/div[2]/form/div[1]/input')
            username_input.send_keys("******")
            time.sleep(5)
            password_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div[2]/div/div[2]/form/div[2]/div/input')
            password_input.send_keys("******")
            time.sleep(5)
           # Add WebDriverWait for each step after page navigation
            login_element = '/html/body/div/div/div[1]/div[2]/div/div[2]/div/div[2]/form/div[3]/button'
            baocao_element = '/html/body/div/div[1]/div[4]/div/div/div[1]/div[8]/div/img'
            baocaokiemsoat_element = '//*[@id="accordionMenu"]/div[3]/div[1]/div[1]/span'
            c02_element = '/html/body/div/div[2]/div/div/div[3]/div[2]/div/div[2]/a/div/span'
            xuatbaocao_element = '/html/body/div/div[3]/div[1]/div[1]/div[1]/div[1]/div/div/div/div[4]/button'
                                #/html/body/div/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/div/div[2]/button
            xuatbaocaoall_element = '/html/body/div/div[3]/div[1]/div[1]/div[1]/div[1]/div/div/div/div[4]/ul/li[2]'
            

            wait.until(EC.element_to_be_clickable((By.XPATH, login_element))).click()
            time.sleep(15)
            print(driver.title)
            x = wait.until(EC.element_to_be_clickable((By.XPATH, baocao_element)))
            x.click()
            time.sleep(15)
            print('baocao_element'+ driver.title)
            wait.until(EC.element_to_be_clickable((By.XPATH, baocaokiemsoat_element))).click()
            time.sleep(15)
            print('baocaoketoan_element'+driver.title)

            wait.until(EC.element_to_be_clickable((By.XPATH,c02_element))).click()
            print('d05_element'+driver.title)
            time.sleep(15)

            x = wait.until(EC.element_to_be_clickable((By.XPATH, xuatbaocao_element)))
            x.click()
            #driver.execute_script("arguments[0].click();", x)
            time.sleep(15)

            print('xuatbaocao_element'+driver.title)
            y = wait.until(EC.element_to_be_clickable((By.XPATH,xuatbaocaoall_element)))
            y.click()
            time.sleep(60)
            print('xuatbaocao_all_element'+driver.title)
            
            driver.quit()
            
            #dummy_table = {'MA_CA':'','NHAN_VIEN':'','SO_DU_DAU_CA':'','DOANH_THU_NET':'','TONG_TIEN_NHAN':'','TONG_HOA_DON':'','THOI_GIAN_MO_CUA':'','THOI_GIAN_DONG_CUA':''}
            ketca = pd.DataFrame()
            
            try:
                
                excel_file = pd.ExcelFile(ketca_path)
                sheetname = excel_file.sheet_names
                for sheet in sheetname:
                    df = excel_file.parse(sheet,skiprows=1)
                    df = df[:-1]
                    df['STORE']=sheet
                    ketca=pd.concat([ketca,df])
                new_column = ['MACA','NHAN_VIEN','SO_DU_DAU_CA','SO_DU_CUOI_CA','DOANH_THU_NET','TONG_TIEN_NHAN','TONG_HOA_DON','THOI_GIAN_MO_CUA','THOI_GIAN_DONG_CUA','STORE']
                ketca.columns=new_column
                #thuchi.loc[:,'THOI_GIAN'] = pd.to_datetime(thuchi.loc[:'THOI_GIAN'],dayfirst=True)
                try:
                    ketca.loc[:,'THOI_GIAN_MO_CUA']=pd.to_datetime(ketca.loc[:,'THOI_GIAN_MO_CUA'],dayfirst=True)
                except Exception as e:
                    print(e)
                     
                try:    
                    ketca.loc[:,'THOI_GIAN_DONG_CUA']=pd.to_datetime(ketca.loc[:,'THOI_GIAN_DONG_CUA'],dayfirst=True)
                except Exception as e:
                    print(e)
                ketca['TONG_TIEN_NHAN'] = None
                    
                #ketca.to_csv('KETCA.CSV')
                os.remove(ketca_path) 
            except (FileNotFoundError, pd.errors.ParserError, KeyError, PermissionError, OSError) as e:
                print(f"An error occurred: {e}")
            
            return ketca

        except Exception as e: 
            if attempt <max_reties - 1: 
                print(f'Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds')
                time.sleep (retry_delay)
            else: 
                print(f'Failed after {max_reties} attemps: {e}')

def momo():
    print("Running momo()")
    max_reties = 3
    retry_delay = 30
    for attempt in range(max_reties):
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options= chrome_options)     
            #Navigate to the website
            driver.get("*****")
            print(1,driver.title)
            # Wait until the page is fully loaded
            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            user_name = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/div/main/div/div[2]/div/div/div[2]/div[2]/div/form/div/div/div[1]/div/div/input')))
            user_name.send_keys('*****')
            time.sleep(3)
            print(2,driver.title)
            pass_word = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div/div/div/main/div/div[2]/div/div/div[2]/div[2]/div/form/div/div/div[2]/div/div/input')))[0]
            pass_word.send_keys('******')
            time.sleep(3)
            print(3,driver.title)
            dang_nhap = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div/div/div/main/div/div[2]/div/div/div[2]/div[2]/div/form/div/button/span')))[0]
            dang_nhap.submit()
            time.sleep(3)
            print(4,driver.title)
            locator_ttbc = (By.XPATH, "//div[contains(text(), 'Trung tâm báo cáo')]")
            trung_tam_bao_cao = wait.until(EC.element_to_be_clickable(locator_ttbc))

            # Click the element
            trung_tam_bao_cao.click()       
            time.sleep(5)
            

            locator_bcgd = (By.XPATH, "//div[contains(text(), 'Báo cáo giao dịch')]")
            bao_cao_giao_dich = wait.until(EC.element_to_be_clickable(locator_bcgd))
            bao_cao_giao_dich.click()
            time.sleep(10)
            print(6,driver.title)
            
            locator_filter = (By.XPATH, "//span[contains(@class, 'material-icons') and text()='filter_alt_outlined']")
            filter_icon = wait.until(EC.element_to_be_clickable(locator_filter))
            filter_icon.click()
            print(777,driver.title)
            time.sleep(10)

            locator_apply_button = (By.XPATH, "//span[contains(@class, 'material-icons') and text()='search']")
            #locator_apply_button = (By.XPATH, "//span[@class='material-icons'][text()='search']")
            apply_button = wait.until(EC.element_to_be_clickable(locator_apply_button))
            apply_button.click()
            print(888, driver.title)
            time.sleep(5)
            
            locator_export_button = (By.XPATH, "//button[contains(@class, 'MuiLoadingButton-root')][contains(text(), 'Xuất Báo Cáo')]")
            export_button = wait.until(EC.element_to_be_clickable(locator_export_button))
            export_button.click()
            time.sleep(15)

            print(7,driver.title)
            
    
            locator_csv_menu_item = (By.XPATH, "//li[contains(text(), 'csv')]")
            csv_menu_item = wait.until(EC.element_to_be_clickable(locator_csv_menu_item))
            csv_menu_item.click()
            #csv = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[2]/div[3]/ul/li[2]')))[0] #/html/body/div[2]/div[3]/ul/li[2]
            
            #csv.click()
            print(driver.title)
            time.sleep(15)
            
            
            

            driver.quit()

            momo_report = pd.read_csv(momo_path)
            column_name = ['THOI_GIAN','MA_DON_HANG','MA_DON_HANG_GOC','MA_GIAO_DICH','TRANG_THAI','TEN_KHACH_HANG','SO_DIEN_THOAI','LOAI_GIAO_DICJ','SO_TIEN','SO_TIEN_GIAM','SO_TIEN_CASHBACK','SO_TIEN_THE_TRA_TRUOC','KENH_THANH_TOAN','PTTT','NGUON_TIEN','MO_TA_GIAO_DICH','MA_CUA_HANG','TEN_CUA_HANG']
            momo_report.columns = column_name
            momo_report.loc[:,'THOI_GIAN'] = pd.to_datetime(momo_report.loc[:,'THOI_GIAN'],dayfirst=True)
            
            try:
                os.remove(momo_path)
                print('File deleted successfully')
            except OSError as e:
                print(f'Error deleting the file: {e}')
            print(momo_report)
            return momo_report
        except Exception as e: 
            if attempt <max_reties - 1: 
                print(f'Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds')
                time.sleep (retry_delay)
            else: 
                print(f'Failed after {max_reties} attemps: {e}')

def grab():
    print("Running grab()")
    max_reties = 2
    retry_delay = 30
    for attempt in range(max_reties):
        grab_report = pd.DataFrame()
        try:
            username = [******]
            for i in range(len(username)):
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options= chrome_options)
                time.sleep(10)          
                #Navigate to the website
                driver.get("******")
                    
                print("step1",driver.title)
                time.sleep(15)

                # Wait until the page is fully loaded
                wait = WebDriverWait(driver, 60)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                # Find the input fields by name
                
                locator_username = (By.XPATH, "//input[@id='username']")
                username_input = wait.until(EC.element_to_be_clickable(locator_username))
                username_input.submit()
                
                #login = (By.CSS_SELECTOR, "[data-test='Báo cáo giao dịch']")
                #username_input = driver.find_element(login)
                username_input.send_keys(username[i])
                time.sleep(5)
                
                locator_password = (By.XPATH, "//input[@id='password']")
                password_input = wait.until(EC.element_to_be_clickable(locator_password))
                password_input.submit()
                password_input.send_keys("********")
                time.sleep(5)
                
                time.sleep(5)
                password_input.send_keys(Keys.TAB)
                time.sleep(5)
                password_input.send_keys(Keys.RETURN)
                
                try:
                    
                    other_device_element = '/html/body/div[3]/div/div[2]/div/div[2]/div/div[2]/button[2]/span'
                    y = wait.until(EC.element_to_be_clickable((By.XPATH, other_device_element)))
                    y.click()
                except Exception as e:
                    print(f"No other devices login: {e}")
                
                try: 
                    web_tour_element = '/html/body/div[5]/div/div[2]/div/div[2]/div/div/div/div[3]/button[1]'
                    a = wait.until(EC.element_to_be_clickable((By.XPATH, web_tour_element)))
                    a.click()
                except Exception as e:
                    print(f"No web tour: {e}")
                
                time.sleep(10)    
                    
                finance_element = '/html/body/div[1]/div/div/div[1]/aside/div[1]/div[1]/ul/li[5]/div/span[2]'
                z = wait.until(EC.element_to_be_clickable((By.XPATH, finance_element)))
                z.click()
                z.click()
                time.sleep(30)
                
                
                #download_element = '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/div[1]/div/div/div[3]/div/span/button'
                download_element = ['/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/div[1]/div/div/div[3]/div/span/button','/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/div[1]/div/div/div[3]/span/button/span[2]/span']
                b = wait.until(EC.element_to_be_clickable((By.XPATH, download_element[i])))
                b.click()
                time.sleep(30)
                
                try: 
                    pick_element = '/html/body/div[7]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div/div[2]/div/label/span/span'
                    c = wait.until(EC.element_to_be_clickable((By.XPATH, pick_element)))
                    c.click()
                    time.sleep(5)                    
                    download_button = '/html/body/div[7]/div/div[2]/div/div/div/div/div[1]/div[3]/button'
                    d = wait.until(EC.element_to_be_clickable((By.XPATH, download_button)))  
                    d.click()  
                    time.sleep(30)
                except Exception as e:
                    print(f"No pop up: {e}")
                
                time.sleep(5)
                
                driver.quit()
                
                try:

                    filename = glob.glob(grab_path)[0]
                    print(filename)
                    
                    df = pd.read_csv(filename)
                    try:
                        df = df.drop('Compensation Voucher (Merchant-Funded)', axis=1)
                    except Exception as e:
                        print(e)
                    column_name = ['Merchant_Name','MerchantID','StoreName','StoreID','UpdatedOn','CreatedOn','Type','Category','Subcategory','Status','Transaction_ID','LinkedTransactionID','PartnertransactionID1','Partner_transaction_ID_2','Long_Order_ID','Short_Order_ID','Booking_ID','Order_Channel','Order_Type','Payment_Method','Terminal_ID','Channel','Offer_Type','Grab_Fee_Percent','Points_Multiplier','Points_Issued','Settlement_ID','Transfer_Date','Amount','Tax_on_Order_Value','Restaurant_Packaging_Charge','Non_Member_Fee','Restaurant_Service_Charge','Offer','Discount_Merchant_Funded','Delivery_Fee_Discount_MerchantFunded','Delivery_Charge_Grab_Online_Store','Delivery_Charge_Merchant_Delivery','GrabExpress_Delivery_Service_Fee','Net_Sales','Net_MDR','Tax_on_MDR','Grab_Fee','Delivery_Commission','Channel_Commission','Order_Commission','GrabFood_GrabMart_Other_Commission','Marketing_success_fee','GrabKitchen_Commission','GrabKitchen_Other_Commission','Withholding_Tax','Total','Tax_on_MDR_Percent','Delivery_Commission_Percent','Channel_Commission_Percecnt','Order_Commission_Percent','Tax_on_GrabFood_GrabMart_Commission_Adjustments_Ads','Tax_on_Total_GrabKitchen_Commission','Cancellation_Reason','Cancelled_by','Reason_for_Refund','Description','Incident_group','Incident_alias','Customer_refund_Item','Appeal_link','Appeal_status']
                    df.columns = column_name
                    try:
                        df.loc[:,'CreatedOn']=pd.to_datetime(df.loc[:,'CreatedOn'])
                        #df.loc[:, 'CreatedOn'] = df['CreatedOn'].dt.strftime('%Y-%m-%d %H:%M:%S')
                    except Exception as e: 
                        print(e)
                    try:    
                        df.loc[:,'UpdatedOn']=pd.to_datetime(df.loc[:,'UpdatedOn'])
                        #df.loc[:, 'UpdatedOn'] = df['UpdatedOn'].dt.strftime('%Y-%m-%d %H:%M:%S')
                    except Exception as e:
                        print(e)
                    
                    grab_report = pd.concat([df,grab_report])
                    os.remove(filename)
                    print('File deleted successfully')
                    #momo_report.loc[:,'THOI_GIAN'] = pd.to_datetime(momo_report.loc[:,'THOI_GIAN'],dayfirst=True)
                except Exception as e:
                    print(f'Error deleting the file: {e}')

            #grab_report.to_csv('GRAB.csv')
            return grab_report            
        except Exception as e: 
            if attempt <max_reties - 1: 
                print(f'Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds')
                time.sleep (retry_delay)
            else: 
                print(f'Failed after {max_reties} attemps: {e}')

def spf():
    print("Running spf()")
    max_reties = 3
    retry_delay = 30
    for attempt in range(max_reties):
        try:
            today = datetime.today()
            today = today.replace(hour=0, minute=0, second=0, microsecond=0)    
            spf_report = pd.DataFrame()
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options= chrome_options)        
            driver.get("*******")
            time.sleep(20)
            print(driver.title)
            with open('cookies.txt','r') as file: cookies = json.load(file)
            
            for cookie in cookies: 
                driver.add_cookie(cookie)
            print("Loaded Cookies")
            time.sleep(10)
            
            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            # Find the input fields by name
            username_input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[1]/form/div/div/div[1]/div/input')
            username_input.send_keys("*****")
            time.sleep(5)
            password_input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[1]/form/div/div/div[2]/div/input')
            password_input.send_keys("*******")
            time.sleep(5)
            
            login_element = '/html/body/div[1]/div/div/div/div/div[1]/form/div/div/button/div'
            tieptuc_element = '/html/body/div[1]/div/div/div[2]/button/div'
            TP_element = '/html/body/div[1]/div/div[2]/div/div[3]/div/div[1]/div/div[2]/div[1]/div/div[1]/div/div'
            quanlydonhang_element = '/html/body/div/div/div/div/section/section/aside/div/ul/li[8]/div/span'
            xuatbaocao_element = '/html/body/div/div/div/div/section/section/aside/div/ul/li[8]/ul/li[3]/span/a'
            xuatbaocao_button = '/html/body/div[1]/div/div/div/section/section/div[2]/div/div/div/div/div/div/div[1]/section/div[1]/div/div/div[4]/button'
            taixuon_element = '/html/body/div[1]/div/div/div/section/section/div[2]/div/div/div/div/div/div/div[1]/section/div[2]/div[1]/table/tbody/tr[1]/td[6]/button'
                
            wait.until(EC.element_to_be_clickable((By.XPATH, login_element))).click()
            time.sleep(15)
            print(driver.title)
            
            wait.until(EC.element_to_be_clickable((By.XPATH, tieptuc_element))).click()
            time.sleep(20)
            print(driver.title)
            
            wait.until(EC.element_to_be_clickable((By.XPATH, TP_element))).click()
            time.sleep(20)
            print(driver.title)
            
            wait.until(EC.element_to_be_clickable((By.XPATH, quanlydonhang_element))).click()
            time.sleep(20)
            print(driver.title)
            
            wait.until(EC.element_to_be_clickable((By.XPATH, xuatbaocao_element))).click()
            time.sleep(30)
            print(driver.title)
            
            wait.until(EC.element_to_be_clickable((By.XPATH, xuatbaocao_button))).click()
            time.sleep(30)
            print(driver.title)
            
            try:    
                wait.until(EC.element_to_be_clickable((By.XPATH, taixuon_element))).click()
                time.sleep(30)
                print(driver.title)

                spf_glob = glob.glob(spf_path)[0]
                df = pd.read_excel(spf_glob)
                
                new_column = ['STT','TEN_CUA_HANG','TRANG_THAI_POS','MA_DON_HANG','NGAY_DAT_HANG','GIO_DAT_HANG','TEN_NGUOI_NHAN','SO_DIEN_THOAI_NGUOI_NHAN','DIA_CHI_NHAN_HANG','TEN_SAN_PHAM','SO_LUONG_SAN_PHAM','GIA_BAN_SAN_PHAM','GIA_GOC_SAN_PHAM','THANH_TIEN_DOANH_THU_GIAGOC_SOLUONG','CK','NOTE','CUA_HANG_GHI_CHU','MA_KHUYEN_MAI','SO_TIEN_GIAM','TINH_TRANG_THANH_TOAN','VAT','PTTT','NGAY_HOAN_TAT','LY_DO_HUY']
                df.columns = new_column
                df.loc[:,'NGAY_DAT_HANG'] = pd.to_datetime(df.loc[:,'NGAY_DAT_HANG'])#.dt.strftime('%d/%m/%Y')
                df.loc[:,'NGAY_HOAN_TAT'] = pd.to_datetime(df.loc[:,'NGAY_HOAN_TAT'])
                df = df[df.loc[:,'NGAY_DAT_HANG']==today]
                spf_report = pd.concat([df,spf_report])
                os.remove(spf_glob)
            except Exception as e: 
                print(e)
            driver.quit()
            time.sleep(10)
            
            
            print("Start scpaping An_SPF")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options= chrome_options)        
            driver.get("*******")
            time.sleep(20)
            print(driver.title)
            with open('cookies.txt','r') as file: cookies = json.load(file)
            print("Loaded Cookies")  
            for cookie in cookies: 
                driver.add_cookie(cookie)
            time.sleep(10)
            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            # Find the input fields by name
            username_input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[1]/form/div/div/div[1]/div/input')
            username_input.send_keys("******")
            time.sleep(5)
            password_input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[1]/form/div/div/div[2]/div/input')
            password_input.send_keys("*****")
            time.sleep(5)
            
            login_element = '/html/body/div[1]/div/div/div/div/div[1]/form/div/div/button/div'
            tieptuc_element = '/html/body/div[1]/div/div/div[2]/button/div'
            TS_element = '/html/body/div[1]/div/div[2]/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div[1]/div/div'
            quanlydonhang_element = '/html/body/div/div/div/div/section/section/aside/div/ul/li[8]/div/span'
            xuatbaocao_element = '/html/body/div/div/div/div/section/section/aside/div/ul/li[8]/ul/li[3]/span/a'
            xuatbaocao_button = '/html/body/div[1]/div/div/div/section/section/div[2]/div/div/div/div/div/div/div[1]/section/div[1]/div/div/div[4]/button'
            taixuon_element = '/html/body/div[1]/div/div/div/section/section/div[2]/div/div/div/div/div/div/div[1]/section/div[2]/div[1]/table/tbody/tr[1]/td[6]/button'
            
            wait.until(EC.element_to_be_clickable((By.XPATH, login_element))).click()
            time.sleep(15)
            print(driver.title)
            
            wait.until(EC.element_to_be_clickable((By.XPATH, tieptuc_element))).click()
            time.sleep(20)
            print(driver.title)
            
            wait.until(EC.element_to_be_clickable((By.XPATH, TS_element))).click()
            time.sleep(20)
            print(driver.title)
            
            wait.until(EC.element_to_be_clickable((By.XPATH, quanlydonhang_element))).click()
            time.sleep(20)
            print(driver.title)
            
            
            wait.until(EC.element_to_be_clickable((By.XPATH, xuatbaocao_element))).click()
            time.sleep(30)
            print(driver.title)
                
            wait.until(EC.element_to_be_clickable((By.XPATH, xuatbaocao_button))).click()
            time.sleep(30)
            print('x',driver.title)
            
            try:    
                wait.until(EC.element_to_be_clickable((By.XPATH, taixuon_element))).click()
                time.sleep(30)
                print(driver.title)
            
                spf_glob = glob.glob(spf_path)[0]
                df = pd.read_excel(spf_glob)
                
                new_column = ['STT','TEN_CUA_HANG','TRANG_THAI_POS','MA_DON_HANG','NGAY_DAT_HANG','GIO_DAT_HANG','TEN_NGUOI_NHAN','SO_DIEN_THOAI_NGUOI_NHAN','DIA_CHI_NHAN_HANG','TEN_SAN_PHAM','SO_LUONG_SAN_PHAM','GIA_BAN_SAN_PHAM','GIA_GOC_SAN_PHAM','THANH_TIEN_DOANH_THU_GIAGOC_SOLUONG','CK','NOTE','CUA_HANG_GHI_CHU','MA_KHUYEN_MAI','SO_TIEN_GIAM','TINH_TRANG_THANH_TOAN','VAT','PTTT','NGAY_HOAN_TAT','LY_DO_HUY']
                df.columns = new_column
                
                df.loc[:,'NGAY_DAT_HANG'] = pd.to_datetime(df.loc[:,'NGAY_DAT_HANG'])
                df.loc[:,'NGAY_HOAN_TAT'] = pd.to_datetime(df.loc[:,'NGAY_HOAN_TAT'])
                df = df[df.loc[:,'NGAY_DAT_HANG']==today]
                spf_report = pd.concat([df,spf_report])
                #spf_report.to_csv('SPF.csv')
                os.remove(spf_glob)
            except Exception as e: 
                print(e)
            driver.quit()
            print(spf_report)
            return spf_report
            
        except Exception as e: 
            if attempt <max_reties - 1: 
                print(f'Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds')
                time.sleep (retry_delay)
            else: 
                print(f'Failed after {max_reties} attemps: {e}')
        
def setup_credentials(key_path):
    credentials = service_account.Credentials.from_service_account_file(
        key_path
    )
    print(credentials)    
    # Create a BigQuery client
    #
    return credentials 

def write_data_to_bigquery(df, project_id, dataset_id, table_name, credentials):
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    
    # Construct a full BigQuery table identifier
    table_id = f"{project_id}.{dataset_id}.{table_name}"
    
    # Create a job_config
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",  # Specify write disposition
    )
    
    # Load the DataFrame to BigQuery
    job = client.load_table_from_dataframe(
        df, table_id, job_config=job_config
    )
    
    # Make an API request and wait for the job to complete
    job.result()
    
    print(f"Loaded dataframe into {table_id}")
    
    # Return a success message
    return f"Data loaded successfully into {table_id}"
   
def fetch_job_logs(credentials):
    # Set up the Cloud Logging client with the provided credentials
    logging_client = logging_v2.Client(credentials=credentials)

    # Define the project ID and the Cloud Run job name
    project_id = '******'  # Replace with your Google Cloud project ID


    # Define the query filter to fetch logs for the Cloud Run job
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)

    # Format the timestamps for the query
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    filter_str = (
        f'logName="projects/{project_id}/logs/run.googleapis.com%2Fstdout" '
        f'resource.type="cloud_run_job" '
        f'severity=DEFAULT '
        f'AND timestamp >= "{start_time_str}" '
        f'AND timestamp <= "{end_time_str}"'
        #f'timestamp<="{date}T24:00:00Z"'  # Note the change here
    )

    print(f"Filter string: {filter_str}")  # Print filter string for debugging

    # Fetch the logs using the Cloud Logging API
    entries = logging_client.list_entries(filter_=filter_str)

    # Process the logs and extract the relevant information
    log_messages = []
    for entry in entries:
        if entry.payload and entry.payload != '':
            log_messages.append(entry.payload)

    
    send_email(log_messages)

def send_email(log_messages):
    # Create an email message
    msg = MIMEMultipart()
    msg['From'] = '*****'  # Replace with sender's email address
    msg['To'] = '*****'  # Replace with recipient's email address
    msg['Subject'] = '******'

    # Add the log messages to the email body
    body = '\n'.join(log_messages)
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = '******'  # Replace with your email address
    password = '******'  # Replace with your email password

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

def main():   
    credentials = setup_credentials(key_path)
    data = [ipos_sales(),
            momo()#,
            ipos_thuchi(),
            ipos_ketca()
            ,
            grab()
            ,
            spf()
            ]

    # Write data to BigQuery
    project_id = '*****'
    dataset_id = '******'
    table_name = ['All_store_daily_sales'
                  ,'momo_daily','daily_thuchi','ketca_daily',
                  'grab_daily',
                  'spf_daily'
                  ]


    for i in range(len(data)):
        try:
            write_data_to_bigquery(data[i], project_id, dataset_id, table_name[i], credentials) 
        except Exception as e:
            print(e)
    
    fetch_job_logs(credentials)
    
if __name__ == "__main__":
    main()   


                

 


