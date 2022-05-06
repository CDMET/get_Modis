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

def get_modis(date, output='./'):
    chrome_options = webdriver.ChromeOptions()
    preferences = {"download.default_directory": output,
                   "directory_upgrade": True,
                   "safebrowsing.enable": True}
    chrome_options.add_experimental_option("prefs", preferences)
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    #  https://wvs.earthdata.nasa.gov/?LAYERS=MODIS_Terra_CorrectedReflectance_TrueColor,Reference_Features_15m&CRS=EPSG:4326&TIME=2022-05-02&COORDINATES=-13.790639,-78.665789,-10.465943,-73.199342&FORMAT=image/png&WORLDFILE=true&AUTOSCALE=TRUE&RESOLUTION=500m
    link = f'https://wvs.earthdata.nasa.gov/?LAYERS=MODIS_Terra_CorrectedReflectance_TrueColor,Reference_Features_15m&CRS=EPSG:4326&TIME={date}&COORDINATES=-15.5,-78.5,-11.2,-72.1&FORMAT=image/png&WORLDFILE=true&AUTOSCALE=TRUE&RESOLUTION=250m'
    
    driver.get(link)
    
    xpath_dwnld = '//*[@id="button-download"]'
    button_dwnld = driver.find_element_by_xpath(xpath_dwnld)
    button_dwnld.click()
    time.sleep(1)
    
    zip_file = f"snapshot-{date}.zip"
    while True:
        if glob.glob(f'{zip_file}.crdownload'):
            print('DESCARGANDO...')
        elif glob.glob(zip_file):
            with zipfile.ZipFile(zip_file, 'r') as zfile:
                zfile.extractall('./')
            return

if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    date = datetime.today().strftime('%Y-%m-%d')
    get_modis(date, path)