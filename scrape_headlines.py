import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

# you'll probably need to run this in terminal first: pip install beautifulsoup4 requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
}

BASE_URL = "https://www.wsj.com/news/archive"
OUTPUT_FILE = "wsj_articles.csv"

def fetch_data(date, page=1):
    """Fetch data for a specific date and page number."""
    url = f"{BASE_URL}/{date.strftime('%Y/%m/%d')}?page={page}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_articles(html, article_date):
    """Parse HTML to extract article details including the theme and datetime."""
    soup = BeautifulSoup(html, 'html.parser')
    articles = []
    
    for article in soup.find_all('article'):
        # Extract headline 
        headline_tag = article.find('h2', class_='WSJTheme--headline--unZqjb45')
        headline = headline_tag.get_text(strip=True) if headline_tag else "No headline"

        # Extract URL
        url_tag = headline_tag.find('a') if headline_tag else None
        url = url_tag['href'].strip() if url_tag and url_tag.has_attr('href') else "No URL"

        # Extract theme
        theme_tag = article.find('div', class_='WSJTheme--articleType--34Gt-vdG')
        theme = theme_tag.get_text(strip=True) if theme_tag else "No theme"

        # Extract timestamp
        timestamp_tag = article.find('div', class_='WSJTheme--lh-timestamp--_ZCwpfk9')
        timestamp = timestamp_tag.get_text(strip=True) if timestamp_tag else "No timestamp"

        articles.append({
            'date': article_date.strftime('%Y-%m-%d'),
            'headline': headline,
            'url': url,
            'theme': theme,
            'timestamp': timestamp
        })
    
    return articles

def save_to_csv(articles, filename):
    """Save the parsed articles to a CSV file."""
    fieldnames = ["date", "headline", "url", "theme", "timestamp"]

    # check if the file is empty, if so we need a header
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            file.read(1)
    except FileNotFoundError:
        write_header = True
    except IOError:
        write_header = True
    else:
        write_header = False

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for article in articles:
            writer.writerow(article)


def main():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 4)  
    current_date = start_date
    while current_date <= end_date:
        page = 1
        while True:
            html = fetch_data(current_date, page)
            if html:
                articles = parse_articles(html, current_date)
                if articles:
                    save_to_csv(articles, OUTPUT_FILE)
                    page += 1
                else:
                    break
            else:
                break
        current_date += timedelta(days=1)

if __name__ == "__main__":
    main()
