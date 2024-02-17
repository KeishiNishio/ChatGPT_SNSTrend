import requests
import json
import configparser
from bs4 import BeautifulSoup
import re

######################
#######　概要　########
######################

'''
1. Twitterからニューストレンドワードを取得するためのHTTPSリクエストを送信
2. 取得したトレンドワードから、をYahooニュースにて取得し、コマンドラインに出力
'''

# SNS_settings.iniファイルに書き込まれた、必要なヘッダー情報、クッキー情報の読み込み
class ConfigManager:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding='utf-8')

    def get_Tw_config(self):
        return {
            'auth_token': self.config.get('COOKIE', 'AUTHTOKEN'),
            'ct0': self.config.get('COOKIE', 'CTO'),
            'csrf_token': self.config.get('HEADER', 'CSRFTOKEN'),
            'authorization': self.config.get('HEADER', 'AUTHORIZATION')
        }

class TwTrendsFetcher:
    SEARCH_URI = 'https://twitter.com/i/api/2/guide.json?include_page_configuration=true&initial_tab_id=news_unified'

    def __init__(self, config):
        self.headers = {
            'Authorization': config['authorization'],
            'Tw-Csrf-Token': config['csrf_token']
        }
        self.cookies = {
            'auth_token': config['auth_token'],
            'ct0': config['ct0']
        }
    
    # セッション情報を使用し、トレンドワードに関するHTTPSリクエストを送信
    def fetch_trends(self):
        response = requests.get(url=self.SEARCH_URI, headers=self.headers, cookies=self.cookies)
        if response.status_code == 200:
            return self._extract_trend_names(response.json())
        else:
            return []

    # レスポンスから所望の情報（トレンドワード）を取得
    def _extract_trend_names(self, jsonData):
        trend_names = []
        entries = jsonData['timeline']['instructions'][1]['addEntries']['entries']
        for entry in entries:
            if 'timelineModule' in entry['content']:
                items = entry['content']['timelineModule']['items']
                for item in items:
                    if 'trend' in item['item']['content']:
                        trend_name = item['item']['content']['trend']['name']
                        trend_names.append(self._remove_special_chars(trend_name))
        return trend_names

    @staticmethod
    #　特殊文字を削除し、文章を整形する関数
    def _remove_special_chars(textWithSpecialChars):
        textWithSpecialChars = textWithSpecialChars.replace('\n', '')
        return re.sub(r'[^\w\s、。？:]', '', textWithSpecialChars) # 句読点以外の特殊文字を削除

class YahooNewsFetcher:
    def __init__(self):
        pass

    # Yahooニュースで指定された検索語に基づいてリンクとタイトルを検索し、それらをリストとして返す
    def fetch_yahoo_news_links_and_titles(self, search_query):
        url = 'https://news.yahoo.co.jp/search'
        params = {'p': search_query}
        response = requests.get(url, params=params)
        html_content = response.text
        
        # print(html_content)
        
        soup = BeautifulSoup(html_content, 'html.parser')
        items = soup.find_all('li', class_='newsFeed_item')
        
        # for mono in items:
        #     print(mono)
        #     print()
            
        Links_and_Titles = []
        for item in items:
            link_tag = item.find('a', class_='newsFeed_item_link') #　ページの構造変化によりクラス名修正
            title_tag = item.find('div', class_='newsFeed_item_title')
            if link_tag and title_tag:
                href = link_tag.get('href')
                title = title_tag.text.strip()
                Links_and_Titles.append((href, title))
        # print(Links_and_Titles)
        return Links_and_Titles
    
    # Yahooニュースの記事URLからJSON形式の記事テキストを取得
    def fetch_article_text_from_json(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', string=re.compile(r'window\.__PRELOADED_STATE__'))
        if not script_tag:
            return "JSON data not found!!!"
        json_data = json.loads(re.search(r'window\.__PRELOADED_STATE__ = (\{.*\})', script_tag.string).group(1))
        paragraphs = json_data.get('articleDetail', {}).get('paragraphs', {})
        article_text = ''
        for paragraph in paragraphs:
            article_text += paragraph.get('textDetails', {})[0].get('text', '') + ' '
        return TwTrendsFetcher._remove_special_chars(article_text)
    
    
if __name__ == "__main__":
    config_manager = ConfigManager('sns_settings.ini')
    Tw_config = config_manager.get_Tw_config()

    Tw_fetcher = TwTrendsFetcher(Tw_config)
    trends = Tw_fetcher.fetch_trends()
    
    yahoo_fetcher = YahooNewsFetcher()
    
    NumOfTrend = 3
    for trend in trends[:NumOfTrend]:  # 最初のNumOfTrend個のトレンドに対して処理
        print(f"Fetching news for trend: {trend}")
        links_and_titles = yahoo_fetcher.fetch_yahoo_news_links_and_titles(trend)
        if links_and_titles:
            first_news_link, first_news_title = links_and_titles[0]
            news_content = yahoo_fetcher.fetch_article_text_from_json(first_news_link)
            print(f"Title: {first_news_title}\nLink: {first_news_link}\nContent: {news_content}\n")
            print('--------------------')
        else:
            print(f"No news found for trend: {trend}\n")
            print('--------------------')