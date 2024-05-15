import csv
import logging
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import pickle

# to login, need to run EXPORT on macOS

# Configure logging
logging.basicConfig(
    format="%(asctime)s, %(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.INFO,
    stream=sys.stdout,
)

URL = "https://www.wsj.com/articles/SB977436609838587596"
ARG_WINDOW_SIZE = "--window-size=1920,1080"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Referer': 'https://www.wsj.com/news/archive/2023/01/01?page=1',
}

class SeleniumScraper:
    def __init__(self):
        self.url = URL
        self.driver = self.create_driver()

    def _create_options(self):
        # Set Chrome browser options
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument(ARG_WINDOW_SIZE)
        options.add_argument("--disable-blink-features")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        return options

    def create_driver(self):
        # Create Chrome browser options
        options = self._create_options()
        # Create webdriver
        # Correctly instantiate Service
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'})
        driver.get(self.url)
        return driver

    def wait(self, secs=2):
        time.sleep(secs)


class ScrapeFlow(SeleniumScraper):
    def __init__(self):
        super().__init__()
        self.user = os.environ.get("USER")
        self.pw = os.environ.get("PASS")
        self._prep_output_file("wsj_fx_articles.csv")

    def main(self):
        self.wait(100)
        self.signin()


        self.session = requests.Session()
        for cookie in self.cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])
        # self.driver.quit()

        # input_filename = 'fx_only.csv' 
        # output_filename = 'wsj_fx_articles.csv' 
        # paragraph_class = 'css-k3zb6l-Paragraph e1e4oisd0'  
        
        # articles_data = []
        # with open(input_filename, newline='') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     for row in reader:
        #         try:
        #             text = self.scrape_article_text(row['url'], paragraph_class)
        #             row['text'] = text
        #             articles_data.append(row)
        #         except Exception as e:
        #             print(f"Error scraping {row['url']}: {e}")

        # with open(output_filename, 'w', newline='') as csvfile:
        #     fieldnames = reader.fieldnames + ['text']  # Original fields plus the text
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     writer.writeheader()
        #     writer.writerows(articles_data)

        

    def _prep_output_file(self, filename):
        self.csv_file = open(filename, "w", encoding="utf-8", newline="")
        self.writer = csv.writer(self.csv_file)

    def signin(self):
        sign_in_link = self.driver.find_element(By.LINK_TEXT, "Sign In")
        sign_in_link.click()
        self.wait(2)
        username = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        username.send_keys(self.user)

        cont_button = self.driver.find_element(
            By.XPATH, "//button[@type='button' and contains(@class, 'solid-button') and contains(@class, 'continue-submit')]")
        cont_button.click()


        password = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "password-login-password"))
        )
        password.send_keys(self.pw)

        submit_button = self.driver.find_elements(
            By.XPATH, "//button[@type='submit' and contains(@class, 'solid-button') and contains(@class, 'basic-login-submit') and .//span[contains(text(), 'Sign In')]]")
        submit_button[1].click()
        self.cookies = self.driver.get_cookies()

    def scrape_article_text(self, url, paragraph_class):
        response = self.session.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all paragraphs
            paragraphs = soup.find_all('p', class_='css-k3zb6l-Paragraph e1e4oisd0')

            article_text = ' '.join(paragraph.text for paragraph in paragraphs)

            return article_text
        else:
            print(response.status_code)
            print('Failed to retrieve the article')



        # self.driver.get(url)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, paragraph_class)))
        # paragraphs = self.driver.find_elements(By.CLASS_NAME, paragraph_class)
        # article_text = ' '.join([para.text for para in paragraphs])
        # return article_text


if __name__ == "__main__":
    start_time = time.time()
    sf = ScrapeFlow()
    sf.main()
    logging.info(f'{time.time() - start_time} sec to scrape articles')


# import requests
# from bs4 import BeautifulSoup

# # THIS COOKIE IS PRIVATE INFO BUT IS NECESSARY TO MAKE REQUEST (potentially not legal lol)
# cookie_string= 'wsjregion=na%2Cus; gdprApplies=false; dnsDisplayed=undefined; signedLspa=undefined; _sp_su=false; AMCVS_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1; ajs_anonymous_id=9cdfa25e-a647-4709-8dc1-66979c535152; _fbp=fb.1.1712855760394.2024270424; _meta_facebookTag_sync=1712855760394; _scid=aa8e585f-9d15-4a26-ad1c-90408ca37731; cX_P=luvi3fagbn0fg7di; _gcl_au=1.1.1646356090.1712855760; s_cc=true; _fbp=fb.1.1712855760394.2024270424; _scor_uid=6de05452572d404a951c8493e531b95f; cX_G=cx%3A1ndwsq11xfjl62qtmkzmswr0ln%3A3ivh8v1ofqxdh; permutive-id=2c7138ce-6a8e-44a8-99eb-3fe8a0f99a01; _sctr=1%7C1712808000000; _cls_v=2d1b4361-8500-4288-8b5b-c335d4448772; G_ENABLED_IDPS=google; djvideovol=1; djcs_route=f27af014-f569-4c47-934f-16d234cfa626; ab_uuid=c94b8072-42dd-448a-9a23-19d5b8470a39; _lr_env_src_ats=true; _ncg_id_=; utag_main__sn_1=undefined; utag_main_vapi_domain_wsj.com=undefined; utag_main_vapi_domain=wsj.com; utag_main__sn=2; s_vnum=1744391842358%26vn%3D2; s_vmonthnum=1714536000358%26vn%3D2; optimizelyEndUserId=oeu1712859809392r0.056143696420396516; _ga=GA1.2.432402834.1712859810; _clck=9by76l%7C2%7Cfku%7C0%7C1562; sub_type=WSJ-SUB; ResponsiveConditional_initialBreakpoint=lg; _lr_geo_location_state=PA; _lr_geo_location=US; _lr_sampling_rate=0; ca_rt=2_njeOe8lms7ubTDWIWyxQ.o5RptxqzLRJwOE96DZ9nWRLjECb_rtCDPRMmdLoy4diFhqInLINZd2DkbfWUz0S3HOY8pYbqC5ixGHghOSM62TPEsCfW595dkECpysH60PE; ca_id=eJxNkNtOg0AQQP9ln4F2WdhLn6QBDaZWU6s-GEOG3cWuAm1gEY3x393SJvo2c-bMJfONXs2HbosWGo0WKIXW6Bp5qILG1F9_2CHdgKldokBN1sW4g87u22A46LYNtBqcNAxGOYdJgQmXwtcxIX4k5tIHKsHHqpKUMRFJGTvbdiDfp4YwjiEKecRVJARwLSilTuNScgU4liRmKpq71WGlGSmpkAxUiUvN46ii5XFYt691jxbP6HKTZZvsys_Xaf6Ypw_JylWf7q_9_C5Jz2GyTje3eVpsk-Uq257hze0yX2WnBL14CAa7K6w5vgAzTMgccxp6SHYarFYFWMcpIZizmAkPmQn8E_Xn4QQYIRMwvTsQ7aw99IvZbBzHYOzfArlvZrI2urXo5xcyWnQP.REBwmzXtnOrCgpJKmRJkLmJPL602Qk3ulPcWxz-gX-bu7Y0ULaaN7aca_GG3cXH8ow0Lh8u6nCcTxos24HA-yuRQkk-sNQokQYIdX-cKz74TEkEp9wn2YB1HFUQv0-_5NpzDefWo8ffYkR5KDSjfOUGOLYcqrzo-TJcA_RTjHleCY-XZss70J_FaMBASKbyzGDffXuZS1-DZvRn6_spwdnF-vGnMsc69zkCqpIUHvSOPyOMtKJ_ysD95Uj1Z5JIoWT_NZLFreNtQ5P9RA-lofDpL94cc1i-NmIzHS5BMM7wJ5dXuxMnJeFmkTdWvmtBVZoR8iQ1g4c16PFLuiAlXcpp48jLhbkvYMWqbObFy2gF4ebTp-5V5gpFe2VNkb_qWpL4_K5aAL6qMgaSxIufpeX7fT2qqqFHbvR8KujTuzsoEpzNG5bsfREskOcEV--luOB2aFeuR_fmrvfoXQd_PhOEeEHFMYsZxzbsRaFAbVsfcIhUADO46Sm4k03lBEDARFif0WksUstTPOK41_RCFf3_dfFIBwRfG2eQgADYaw4QtWkS8O6E-tkRN1Gono7rDvsbeqwu28PHHHKYumUJsDATyhfbDK8aT9TOw3Xc1Sp8DFB_EAEsZvgc_FWs0QrGgXfifDiE_QbXgRQBEmVUYjRGxoK1nQGRPIwhb8PbinmI; s_sq=djcommercedev%3D%2526c.%2526a.%2526activitymap.%2526page%253DDWSJN_Commerce_CAJ_Thank_You%2526link%253DEXPLORE%252520WSJ%2526region%253Dmain%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253DDWSJN_Commerce_CAJ_Thank_You%2526pidt%253D1%2526oid%253Dfunctiontn%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DSUBMIT; _pubcid=1ed9f5a3-c7d0-4660-8f71-a14e485e4451; _dj_sp_id=5832f4b9-037b-4a1d-9a8c-709b8e194911; _pcid=%7B%22browserId%22%3A%22lv2vp64cmn3fyq9i%22%7D; _dj_ses.9183=*; AMCV_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1585540135%7CMCIDTS%7C19830%7CMCMID%7C09667904061678781184008459329605529796%7CMCAAMLH-1713913975%7C7%7CMCAAMB-1713913975%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1713316375s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; _ncg_sp_ses.5378=*; _ncg_g_id_=a5b76468-8c71-434a-87b0-b44f577d9351.3.1712859190.1776383889197; usr_prof_v2=eyJwIjp7InBzIjowLjcyLCJxIjowLjc0fSwiYSI6eyJlZCI6InRydWUiLCJyIjoiMjAyNC0wNC0xMVQwMDowMDowMC4wMDBaIiwiZSI6IjIwMjgtMDktMjZUMDA6MDA6MDAuMDAwWiIsInMiOiIyMDI0LTA0LTExVDAwOjAwOjAwLjAwMFoiLCJzYiI6IkVkdWNhdGlvbmFsIiwiZiI6IjIgWWVhciIsIm8iOiJTdHVkZW50IERpZ2l0YWwgUGFjayIsImF0IjoiU1RVREVOVCIsInQiOjB9LCJjcCI6eyJlYyI6Ikdyb3dpbmciLCJwYyI6MC4xMDAyMSwicHNyIjowLjE2NTM4LCJ0ZCI6NCwiYWQiOjEsInFjIjo3OSwicW8iOjk0LCJzY2VuIjp7ImNoZSI6MC4wOTg5NiwiY2huIjowLjEwMDc0LCJjaGEiOjAuMTA1OTgsImNocCI6MC4xMDAyMn19LCJpYyI6NX0%3D; _pubcid_cst=TyylLI8srA%3D%3D; DJSESSION=country%3Dus%7C%7Ccontinent%3Dna%7C%7Cregion%3D%7C%7Czip%3D19104; ccpaApplies=true; vcdpaApplies=true; regulationApplies=gdpr%3Afalse%2Ccpra%3Atrue%2Cvcdpa%3Atrue; utag_main=v_id:018ece5cdb25001691a5e295c2a505075001406d009dc$_sn:3$_se:46$_ss:0$_st:1713315672745$vapi_domain:wsj.com$ses_id:1713309175617%3Bexp-session$_pn:44%3Bexp-session$_prevpage:WSJ_Article_Tech_Twitter%20Sued%20Over%20Rent%20Payment%20in%20San%20Francisco%3Bexp-1713317472749; _pctx=%7Bu%7DN4IgrgzgpgThIC5QCYCsqCGAWZAOLuAJlgJwka5QkBstA7CQQMZNEYCMqTAzKncQAZCGQsgBmUOtwBG1Ekzojp7aVFyosY6tNTAA7hABWAX0SgADjChiAlgA9EIA4ZAAaEABcAnuaiOAwgAaIMbG7pCwAMoeGB6QjhgAdgD2iW4gEDYeUACShI4kyEXc7LjU7NzqyARyAgIhQA; _rdt_uuid=1713301873074.b76858e0-2e3c-4de6-82c5-105745dea33b; _dj_id.9183=.1713313873.0.1713313873..434a0d92-d9bd-4c7d-9937-2ccca26eb338; _uetsid=c7d612f0fc3511ee946a1f7704905b9d; _uetvid=5c7a671094a511ee9f69afff670a2b45; _scid_r=aa8e585f-9d15-4a26-ad1c-90408ca37731; dicbo_id=%7B%22dicbo_fetch%22%3A1713313872960%7D; __gads=ID=861acff7b65e134a:T=1712855767:RT=1713313873:S=ALNI_MZD16mWwZgmdFCcSjEl2SSp5Jv_Gw; __gpi=UID=00000a1c6a78a477:T=1712855767:RT=1713313873:S=ALNI_Ma2KLPnend_BG4usy_TIX2nq-P9yg; __eoi=ID=95fe04e813b3c0c4:T=1712855767:RT=1713313873:S=AA-Afjbd-lXPkUdVVQ_bbAWUu4YU; datadome=cha0ZdG_nvAxXNw0dZEgU_yq6db0a4tPhQyakW_VSTAC_KyTo5gbtitmx8WS8siQ4Ww0U4YYgWG9QmCxWPwdwBZQRfJmFCdc8p2MQt2JoMYZ2TYAPQGs15rA1TzKLpfD; s_tp=7791; s_ppv=WSJ_Article_Tech_Twitter%2520Sued%2520Over%2520Rent%2520Payment%2520in%2520San%2520Francisco%2C10%2C10%2C752'
# cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_string.split('; ')}



# # base url of article to scrape
# article_url = 'https://www.wsj.com/articles/twitter-sued-over-rent-payment-in-san-francisco-11672622435'

# response = requests.get(article_url, headers=headers, cookies=cookies)

# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Extract all paragraphs
#     paragraphs = soup.find_all('p', class_='css-k3zb6l-Paragraph e1e4oisd0')

#     article_text = ' '.join(paragraph.text for paragraph in paragraphs)

#     print(article_text)
# else:
#     print(response.status_code)
#     print('Failed to retrieve the article')
