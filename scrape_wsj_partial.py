import requests
from bs4 import BeautifulSoup
import csv
import os

# THIS COOKIE IS PRIVATE INFO BUT IS NECESSARY TO MAKE REQUEST (potentially not legal lol)
cookie_string= 'wsjregion=na%2Cus; gdprApplies=false; dnsDisplayed=undefined; signedLspa=undefined; _sp_su=false; AMCVS_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1; ajs_anonymous_id=9cdfa25e-a647-4709-8dc1-66979c535152; _fbp=fb.1.1712855760394.2024270424; _meta_facebookTag_sync=1712855760394; _scid=aa8e585f-9d15-4a26-ad1c-90408ca37731; cX_P=luvi3fagbn0fg7di; _gcl_au=1.1.1646356090.1712855760; s_cc=true; _fbp=fb.1.1712855760394.2024270424; _scor_uid=6de05452572d404a951c8493e531b95f; cX_G=cx%3A1ndwsq11xfjl62qtmkzmswr0ln%3A3ivh8v1ofqxdh; permutive-id=2c7138ce-6a8e-44a8-99eb-3fe8a0f99a01; _cls_v=2d1b4361-8500-4288-8b5b-c335d4448772; G_ENABLED_IDPS=google; djvideovol=1; djcs_route=f27af014-f569-4c47-934f-16d234cfa626; ab_uuid=c94b8072-42dd-448a-9a23-19d5b8470a39; _lr_env_src_ats=true; _ncg_id_=; utag_main__sn_1=undefined; utag_main_vapi_domain_wsj.com=undefined; utag_main_vapi_domain=wsj.com; utag_main__sn=2; s_vnum=1744391842358%26vn%3D2; s_vmonthnum=1714536000358%26vn%3D2; optimizelyEndUserId=oeu1712859809392r0.056143696420396516; _clck=9by76l%7C2%7Cfku%7C0%7C1562; sub_type=WSJ-SUB; _pubcid=1ed9f5a3-c7d0-4660-8f71-a14e485e4451; _dj_sp_id=5832f4b9-037b-4a1d-9a8c-709b8e194911; _pcid=%7B%22browserId%22%3A%22lv2vp64cmn3fyq9i%22%7D; _ga=GA1.1.432402834.1712859810; _ga_LXHX716KXJ=GS1.1.1713400849.1.0.1713400853.0.0.0; ccpaApplies=false; _lr_geo_location_state=PA; _lr_geo_location=US; AMCV_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1585540135%7CMCIDTS%7C19832%7CMCMID%7C09667904061678781184008459329605529796%7CMCAAMLH-1714166459%7C7%7CMCAAMB-1714166459%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1713568859s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; _ncg_sp_ses.5378=*; _dj_ses.9183=*; _sctr=1%7C1713499200000; vcdpaApplies=false; regulationApplies=gdpr%3Afalse%2Ccpra%3Afalse%2Cvcdpa%3Afalse; _lr_sampling_rate=100; ResponsiveConditional_initialBreakpoint=md; ca_rt=lHuLMQp-C9RAtrp06nWW9A.nOlbQwQDtSmIounrvLUmtRB1vw4Gzjt8Z66NxnL7Iselng2zQNfngABOGgCuLUoBtTWvniOu45oI7l1WqX26f1ZiBQCtrlVYcIM9RMX-U14; ca_id=eJxNkNtOg0AQQP9ln4GWLnvrkzSgwdTW1KoPxpBhd7GrQBtYRNP4725pE32bOXPmkjmiN_Opm7yBWqM5SqAxukIeKqE21fcfdkjXYCqXKFCjdTXsoLX7JugPumkCrXon9b1RzmFShJhL4WuCsR-JqfSBSvBDVUrKmIikJM62LciPsWFGCEQzHnEVCQFcC0qp07iUXEFIJCZMRVO3elZqhgsqJANVhIXmJCppcRrW7ivdofkLut6k6Sa98bNVkj1lyWO8dNXnh1s_u4-TSxivks06S_JtvFim2wu8Wy-yZXpO0KuHoLe73JrTC0IWYkIpnmIPyVaD1SoH6zjFOOSMMOEhM4J_ov46nIEQfASmcweinbWHbj6ZDMMQDN17IPf1RFZGNxb9_AI063QY.C9UuHSA2jFMJGnwHuk1jyiUdCOBkQh0LpH6ZNYR7wO3IwTEilo0PANuysgtyPLj4Y4R94I-uzZ7NXJEUb-O6Ol4ILSHG1UPQPUqlZGuOKXvDwADAtjpHMPFQrMnMHcAzSoL5FsmufyQRe8So-bwYN6OMGC3LMzC1bJFuR6Z3JTQ5A6S27H-mQI1xMf8fWQUjcgEfLCkz6oqZr4Bo-PNhbJXP3cWpDEbGdSfqzJb-Mne-U89UGQ5m9Jv8cgafapSeY_-yoky-0pRBSI3Q1Eat9ppQkmKpRUvbogLOLTrdTkysvc6wC2zXtHqVPm4QCzdSrvldz1Ofp8YivbU49dU-rKML-h805RwqRQg2b-boGMvvT-Wp5PkzGHI0pt5JVp0R4GFFNdcvGiNM6bMfESfdQ-9mDqXEk6XpfLxK6C_EEIVvbZksew5xkgAIe7mfO0e1bjHF2-pSPjsYVifWfBHXoVTP4KAXlin1aBC4THRWEuvrF773XVcgy2pTG1KoKlG0qDvNrhTrBApOiY3IdO8c7Fxqlt2ap2vm5qkKBE1jN6AvCXNwcQI8Ls-LoM2TvjiWhXMW_8i1cK_S0KyrIyUNEvC3TyCtJaUX6HiAI7DUNvcRYiTnDrE8o3NiPGPz9u0lfA28ywCXibwmfXpfkKHkm0jZvFq_B34JC4z5wiu3csE; usr_prof_v2=eyJpYyI6NX0%3D; DJSESSION=country%3Dus%7C%7Ccontinent%3Dna%7C%7Cregion%3Dpa%7C%7Czip%3D19104; s_sq=djglobal%3D%2526c.%2526a.%2526activitymap.%2526page%253DWSJ_Article_Markets_Netflix%252520Dealt%252520With%252520the%252520Freeloaders.%252520Its%252520Next%252520Act%252520Will%252520Be%252520Tougher.%2526link%253DOpinion%25253A%252520You%252520Don%2525E2%252580%252599t%252520Need%252520to%252520Be%252520a%252520Millionaire%252520to%252520Retire%2526region%253D__next%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%26djcommercedev%3D%2526c.%2526a.%2526activitymap.%2526page%253DDWSJN_Commerce_CAJ_Thank_You%2526link%253DEXPLORE%252520WSJ%2526region%253Dmain%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253DDWSJN_Commerce_CAJ_Thank_You%2526pidt%253D1%2526oid%253Dfunctiontn%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DSUBMIT; _ncg_g_id_=a5b76468-8c71-434a-87b0-b44f577d9351.3.1712859190.1776639764197; dicbo_id=%7B%22dicbo_fetch%22%3A1713567764451%7D; _pubcid_cst=TyylLI8srA%3D%3D; utag_main=v_id:018ece5cdb25001691a5e295c2a505075001406d009dc$_sn:5$_se:28$_ss:0$_st:1713569567890$vapi_domain:wsj.com$ses_id:1713561659045%3Bexp-session$_pn:22%3Bexp-session$_prevpage:WSJ_Article_Money%20%26%20Investing_Currency%20Traders%20Likely%20to%20Stay%0ASidelined%20as%20Y2K%20Fears%20Linger%3Bexp-1h; _pctx=%7Bu%7DN4IgrgzgpgThIC5QCYCsqCGAWZAOLuAJlgJwka5QkBstA7CQQMZNEYCMqTAzKncQAZCGQsgBmUOtwBG1Ekzojp7aVFyosY6tNTAA7hABWAX0SgADjChiAlgA9EIA4ZAAaEABcAnuaiOAwgAaIMbG7pCwAMoeGB6QjhgAdgD2iW4gEDYeUACShI4kyEXc7LjU7NzqyARyAgIhQA; _rdt_uuid=1713301873074.b76858e0-2e3c-4de6-82c5-105745dea33b; _scid_r=aa8e585f-9d15-4a26-ad1c-90408ca37731; _ncg_domain_id_=.0.1713567768061.1776639768061; _uetsid=b7862e00fe9211eebab81d157650efa2; _uetvid=5c7a671094a511ee9f69afff670a2b45; __gads=ID=861acff7b65e134a:T=1712855767:RT=1713567768:S=ALNI_MZD16mWwZgmdFCcSjEl2SSp5Jv_Gw; __gpi=UID=00000a1c6a78a477:T=1712855767:RT=1713567768:S=ALNI_Ma2KLPnend_BG4usy_TIX2nq-P9yg; __eoi=ID=95fe04e813b3c0c4:T=1712855767:RT=1713567768:S=AA-Afjbd-lXPkUdVVQ_bbAWUu4YU; s_tp=10114; s_ppv=WSJ_Article_Money%2520%2526%2520Investing_Currency%2520Traders%2520Likely%2520to%2520Stay%250ASidelined%2520as%2520Y2K%2520Fears%2520Linger%2C12%2C12%2C1223; datadome=Dx7Q7St9NzSdl670qOy1NNmOJwqGX8UTPu~rnDLAGJAaYZD51rGrOG5eqyZHPoxjcVVWjdTN0X~TDIGzQnGMQtMBDtjzSIRJ0XVL0GzqBgGqX~_98kGn4M6lyp4jIHqu'
cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_string.split('; ')}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Referer': 'https://www.wsj.com/news/archive/2000/01/03?page=1',
}

def scrape_article_text(article_url):
    response = requests.get(article_url, headers=headers, cookies=cookies)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p', class_='css-k3zb6l-Paragraph e1e4oisd0')
        article_text = ' '.join(paragraph.text for paragraph in paragraphs)
        return article_text
    else:
        print(response.status_code)
        print('Failed to retrieve the article at: ' + article_url)
        return None

input_filename = 'fx_only.csv' 
output_filename = 'wsj_fx_articles.csv'

# Read the existing field names from the input CSV and add the 'text' field
with open(input_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames + ['text']

# Open the output CSV file in append mode
with open(output_filename, 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # If you're running this for the first time, write the header
    # If the script may run multiple times, check if the file is empty to avoid duplicating the header
    csvfile.seek(0, os.SEEK_END)  # Seek to the end of the file
    if csvfile.tell() == 0:  # If file is empty, write the header
        writer.writeheader()

    # Process each article URL from the input CSV
    with open(input_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Scrape the text for the current article URL
                text = scrape_article_text(row['url'])
                if text:  # Only write to the CSV if text scraping was successful
                    row['text'] = text
                    writer.writerow(row)
            except Exception as e:
                print(f"Error scraping {row['url']}: {e}")
