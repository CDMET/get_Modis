import os
import sys
import glob
import zipfile
import time
import argparse
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def load_msg(msg,freq=0.3):
    for i in range(4):
        str_update  = '.'*i + '|'*(3-i) 
        str_msg = f'\r{str_update} {msg}'
        sys.stdout.write(str_msg)
        time.sleep(freq)
    return

def get_modis(date, output='./'):
    chrome_options = webdriver.ChromeOptions()
    preferences = {"download.default_directory": output,
                   "directory_upgrade": True,
                   "safebrowsing.enable": True}
    chrome_options.add_experimental_option("prefs", preferences)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    link = f'https://wvs.earthdata.nasa.gov/?LAYERS=MODIS_Terra_CorrectedReflectance_TrueColor,Reference_Features_15m&CRS=EPSG:4326&TIME={date}&COORDINATES=-15.5,-78.5,-11.2,-72.1&FORMAT=image/png&WORLDFILE=true&AUTOSCALE=TRUE&RESOLUTION=250m'
    
    driver.get(link)
    
    xpath_dwnld = '//*[@id="button-download"]'
    button_dwnld = driver.find_element_by_xpath(xpath_dwnld)
    button_dwnld.click()
    time.sleep(1)
    
    zip_file = f"snapshot-{date}.zip"
    while True:
        if glob.glob(f'{zip_file}.crdownload'):
            load_msg(f'Descargando -> [{zip_file}]')
        elif glob.glob(zip_file):
            print("\n\n-= Descarga completada =-")
            with zipfile.ZipFile(zip_file, 'r') as zfile:
                zfile.extractall('./')
                print(f"[+] {zip_file} -> Decomprimido\n")
            return

def main(args):
    parser = argparse.ArgumentParser(description = __doc__,
                                     epilog = "Report bugs or suggestions to <cdavila@senamhi.gob.pe>",)
    parser.add_argument('date', metavar='DATE', help="Date '2022-05-05'")
    parser.add_argument('-o',
                        '--output',
                        type=str,
                        help='Output directory',
                        default=os.path.dirname(os.path.abspath(__file__)))
    args = parser.parse_args()
    get_modis(args.date, args.output)

if __name__ == '__main__':
    # path = os.path.dirname(os.path.abspath(__file__))
    # date = datetime.today().strftime('%Y-%m-%d')
    # get_modis(date, path)
    sys.exit(main(sys.argv))