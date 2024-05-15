import requests
from bs4 import BeautifulSoup
import csv
import os

# THIS COOKIE IS PRIVATE INFO BUT IS NECESSARY TO MAKE REQUEST (potentially not legal lol)
cookie_string = "djvideovol=1; wsjregion=na%2Cus; gdprApplies=false; dnsDisplayed=undefined; signedLspa=undefined; _sp_su=false; AMCVS_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1; ajs_anonymous_id=9cdfa25e-a647-4709-8dc1-66979c535152; _fbp=fb.1.1712855760394.2024270424; _meta_facebookTag_sync=1712855760394; cX_P=luvi3fagbn0fg7di; _gcl_au=1.1.1646356090.1712855760; s_cc=true; _fbp=fb.1.1712855760394.2024270424; cX_G=cx%3A1ndwsq11xfjl62qtmkzmswr0ln%3A3ivh8v1ofqxdh; permutive-id=2c7138ce-6a8e-44a8-99eb-3fe8a0f99a01; G_ENABLED_IDPS=google; djvideovol=1; djcs_route=f27af014-f569-4c47-934f-16d234cfa626; ab_uuid=c94b8072-42dd-448a-9a23-19d5b8470a39; _lr_env_src_ats=true; optimizelyEndUserId=oeu1712859809392r0.056143696420396516; _clck=9by76l%7C2%7Cfku%7C0%7C1562; sub_type=WSJ-SUB; _ga=GA1.1.432402834.1712859810; ca_rt=lHuLMQp-C9RAtrp06nWW9A.nOlbQwQDtSmIounrvLUmtRB1vw4Gzjt8Z66NxnL7Iselng2zQNfngABOGgCuLUoBtTWvniOu45oI7l1WqX26f1ZiBQCtrlVYcIM9RMX-U14; _sctr=1%7C1715486400000; ca_id=eJxFkFtPgzAUgP9Ln2Gj9L4nWUCDmZuZUx-MIaUtrgpsgSIa43-3Y0t8O-c737nk_IA3-2naopWNAQuQytaaGgSgko2tv_-xR6aRtvaJlnqyrsa97NyhnQ1H07YzowcvDYPV3mFKQMSVCA1BKMQiUqGkSoZQV4oyJrBSxNuuk-pjaogJkTjmmGsshORGUEq9xpXiWkKiEGEaR351XBmGSioUk7qEpeEEV7Q8DesOtenB4gVcb7Nsm92E-TrNn_L0MVn56vPDbZjfJ-klTNbpdpOnxS5ZrrLdBd5tlvkqOyfgNQBycPvC2dMLIIOIUIoiFADVGemMLqTznCIEOSNMBMBOgEGCBY1J5D_2dTwDEfMJ2N4fCPbOHfvFfD6O42zs32fq0MxVbU3rwO8fNW50GQ.TwhYBU1Y-w9ly42CyEEqnMACRkCYD21wTmokXuzHHjqADfM_eVANWhWGeycHTGwav4-lRlIBNALoH7Ka1eVyG50m_uB4HuAICN9i1mIW6yrq20wKjw-Z3631oUOKFo9eFJVHcTuMrRW4U36zaKw93wvoTiDDBTfJI53XSBmOWzVZJBI7za86uPoIaVDHoXO3wLaaWoFKfnrZlWel505W8kKGeJnO-mKb6Gy-afePMXqk4y2WOEcCY4ffW8gq7Txc1OPj6XZdr-66-nsCDdQuoC9oZwBhMr6YhGuIr6B6EQ8Muj8ZP_GvzlMCymZ_csvVhrSer_jQqDdilSFOuBVSyQgIRDUPaSbSLREH9rp3f9_WuPDTLc53uyLGaSkw6FW-n7GnAogQ-4TnI5Rd9CLT1_VySnWK9XVAeQEssAMQcYcpKlcgYk-C0LE3RLV1KkUP3Y3vU_y3Uq3E8tqaH_Uisp82DtMPd-GMb-onb1IOOI47lrD-LYsF8c1XbRrQN_Ol3PQ7gYz82NlSEGhKuDKBghS687UIu0I1BGlO46I6z5U6UMrmk5CUSXtb48646fSLLyUho-O09V_ExYFqFiJHx-vxkqh6XwObTIuabxUKtoMr6P44tWvgg2vxaYYTEKwS_b9dzZpHJPAyawAjrY4ufZivZmID6ZL7yG9IYPaz1Q8; TR=V2-255a42848d499a8e96667948cc8da15c357d40dad2fe73b69c7adb1be854f6b5; s_vnum=1744391842358%26vn%3D4; s_vmonthnum=1717214400584%26vn%3D2; _pubcid=b586e447-e65d-469e-bfd9-9d5d712663f1; _scid=96962f3b-0f71-4026-bd4f-032615115281; _pcid=%7B%22browserId%22%3A%22lw4frycu9tfpbrlr%22%7D; _dj_sp_id=abf6b75f-1ef2-47bc-bc27-bfbd4af39a04; _ncg_domain_id_=a47edf26-19ff-4366-87a3-a1ce1f0082cc.1.1715572844100.1778644844100; _ncg_g_id_=a5b76468-8c71-434a-87b0-b44f577d9351.3.1715572844.1778644844100; _pin_unauth=dWlkPU9HVmhNR05oT0dRdFlqTXhOUzAwWVRoakxUbGxaRGd0TTJSbU5EVXlOR1kxWXpneg; _lr_sampling_rate=100; usr_bkt=q85AaJVP78; _scor_uid=bef3c4b4b0c34fc0b5a0dba8160124e5; ccpaApplies=false; _lr_geo_location_state=PA; _lr_geo_location=US; ResponsiveConditional_initialBreakpoint=md; AMCV_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1585540135%7CMCIDTS%7C19857%7CMCMID%7C09667904061678781184008459329605529796%7CMCAAMLH-1716303846%7C7%7CMCAAMB-1716303846%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1715706246s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; _dj_ses.9183=*; _ncg_sp_ses.5378=*; DJSESSION=country%3Dus%7C%7Ccontinent%3Dna%7C%7Cregion%3Dpa%7C%7Czip%3D19104; vcdpaApplies=false; regulationApplies=gdpr%3Afalse%2Ccpra%3Afalse%2Cvcdpa%3Afalse; _meta_cross_domain_id=69f0ce6a-6ab4-4fb1-9835-e21239b9c137; _meta_cross_domain_recheck=1715699048434; __gads=ID=1b3901aff3e0f661:T=1715572844:RT=1715699048:S=ALNI_MZzAfdiEZW4RE4o4G7SqwPDMYBfqw; __gpi=UID=00000a26727c4a7f:T=1715572844:RT=1715699048:S=ALNI_MYsF2OdVxWj3NJib-26KBIDEo-pOA; __eoi=ID=c75ab46ef49d0421:T=1715572844:RT=1715699048:S=AA-AfjZP-8qcAPqVfxhBZpW-KAtj; _ncg_id_=; _pubcid_cst=TyylLI8srA%3D%3D; dicbo_id=%7B%22dicbo_fetch%22%3A1715699414183%7D; usr_prof_v2=eyJwIjp7InBzIjowLjAyLCJxIjowLjM3fSwiYSI6eyJlZCI6InRydWUiLCJyIjoiMjAyNC0wNC0xMVQwMDowMDowMC4wMDBaIiwiZSI6IjIwMjgtMDktMjZUMDA6MDA6MDAuMDAwWiIsInMiOiIyMDI0LTA0LTExVDAwOjAwOjAwLjAwMFoiLCJzYiI6IkVkdWNhdGlvbmFsIiwiZiI6IjIgWWVhciIsIm8iOiJTdHVkZW50IERpZ2l0YWwgUGFjayIsImF0IjoiU1RVREVOVCIsInQiOjF9LCJjcCI6eyJlYyI6Ikdyb3dpbmciLCJwYyI6MC4wNDcyNywicHNyIjowLjIzMjM0LCJ0ZCI6MzEsImFkIjozLCJxYyI6NzEsInFvIjo3OCwic2NlbiI6eyJjaGUiOjAuMDQ1ODksImNobiI6MC4wNDgyNywiY2hhIjowLjA1Nzg5LCJjaHAiOjAuMDUyNTd9fSwiaWMiOjV9; utag_main=v_id:018f701c24a9001c4aefa253811d05075002b06d009dc$_sn:7$_se:28$_ss:0$_st:1715701356761$vapi_domain:wsj.com$ses_id:1715699046519%3Bexp-session$_pn:28%3Bexp-session$_prevpage:WSJ_Article_Real%20Estate_New%20Florida%20Law%20Roils%20Its%20Condo%20Market%20Three%20Years%20After%20Surfside%20Collapse%3Bexp-1715703156765; _pctx=%7Bu%7DN4IgrgzgpgThIC5QCYCsqCGAWZAOLuAJlgJwka5QkBstA7CQQMZNEYCMqTAzKncQAZCGQsgBmUOtwBG1Ekzojp7aVFyosY6tNTAA7hABWAX0SgADjChiAlgA9EIA4ZAAaEABcAnuaiOAwgAaIMbG7pCwAMoeGB6QjhgAdgD2iW4gEDYeUACShI4kyEXc7LjU7NzqyARyAgIhQA; _dj_id.9183=.1715699060.0.1715699557..90bc05e8-50a9-41ce-9e48-d8ebc22a4bd3; _scid_r=96962f3b-0f71-4026-bd4f-032615115281; _rdt_uuid=1715572843990.e2a2e494-e937-4335-93e5-382b6e7bf40a; _uetsid=5f10f2e010dd11ef931c3fffa87f6be8; _uetvid=5f11339010dd11ef8c2789eaa288807b; datadome=xHa9T5eJRmk12tixHg9DQ9KWhH57Z4aeOq9Q1DVTLeYDBjhvPFSzvT~ihHCPLV_JM1ElhfZ7llI2ANLH~pqIIunLugSKnN0r74Iv6lNPetF85MnqLrVhNbvvhOAGlyjV; _ncg_sp_id.5378=.1715699288.1.1715699558..fcc57d25-4b10-477d-8c5c-f6e8b45483e6..41d57460-1f1b-4060-952b-5f479abf75fa.1715699556925.7; s_tp=15751; s_ppv=WSJ_Article_Real%2520Estate_New%2520Florida%2520Law%2520Roils%2520Its%2520Condo%2520Market%2520Three%2520Years%2520After%2520Surfside%2520Collapse%2C8%2C8%2C1223"
cookies = {cookie.split('=')[0]: cookie.split('=')[1]
           for cookie in cookie_string.split('; ')}

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
        paragraphs = soup.find_all(
            'p', class_='css-k3zb6l-Paragraph e1e4oisd0')
        article_text = ' '.join(paragraph.text for paragraph in paragraphs)
        return article_text
    elif response.status_code == 403:
        raise Exception("403 Forbidden Error")
    else:
        print(
            f"Failed to retrieve the article with status code: {response.status_code}")
        return None


input_filename = 'extracted_themes.csv'
output_filename = 'wsj_full_articles_pt2.csv'

# Read the existing field names from the input CSV and add the 'text' field
with open(input_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames + ['text']

# Open the output CSV file in append mode
with open(output_filename, 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    csvfile.seek(0, os.SEEK_END)
    if csvfile.tell() == 0:
        writer.writeheader()

    with open(input_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                if row['date'] <= '2020-07-08':
                    continue

                text = scrape_article_text(row['url'])
                if text:  
                    row['text'] = text
                    writer.writerow(row)
            except Exception as e:
                if "403 Forbidden Error" in str(e):
                    print("403 Forbidden Error encountered. Stopping execution.")
                    break
                print(f"Error scraping {row['url']}: {e}")
