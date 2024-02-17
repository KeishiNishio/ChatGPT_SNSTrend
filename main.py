import csv
import configparser
import os
import time
from TrendResearch.search_tw_yahoo_news import ConfigManager, TwTrendsFetcher, YahooNewsFetcher
from edit_csv import CSVEditor
from spreadsheet_manager import SpreadsheetManager,CSVFileManager
from request_to_chatGPT import NewsQueryAssistant


def main():
    csv_editor = CSVEditor()
    csv_editor.clear_csv()  # Clears the CSV file

    config_manager = ConfigManager('sns_settings.ini')
    Tw_config = config_manager.get_Tw_config()

    # TwTrendsFetcherとYahooNewsFetcherを初期化
    Tw_fetcher = TwTrendsFetcher(Tw_config)
    yahoo_fetcher = YahooNewsFetcher()

    # トレンドを取得
    trends = Tw_fetcher.fetch_trends()

    # 各トレンドに対してニュースを取得
    num_of_trends = 3 # 最初の3つのトレンドを処理
    for trend in trends[:num_of_trends]:  
        print(f"Fetching news for trend: {trend}")
        links_and_titles = yahoo_fetcher.fetch_yahoo_news_links_and_titles(trend)
        if links_and_titles:
            for link, title in links_and_titles[:1]:  # トレンドごとに最初のニュースのみを処理
                news_content = yahoo_fetcher.fetch_article_text_from_json(link)
                # 結果をCSVに書き込み
                csv_editor.write_to_csv([ news_content]) # title, link, news_content
                print(f"Title: {title}\nLink: {link}\nContent: {news_content}")
                print('--------------------')
        else:
            print(f"No news found for trend: {trend}")
            print('--------------------')
    
    # After writing news to CSV
    spreadsheet_manager = SpreadsheetManager('support_account_key.json', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    
    # Read the CSV file data
    csv_file = 'latest_yahoo_ja_news.csv'
    csv_data = CSVFileManager.read_csv_data(csv_file)

    # Write data to Google Sheets
    spreadsheet_manager.write_sheet_data(csv_data, 'JapaneseNews!A1')  # Adjust the range as needed
    print("Send Data to Google sheets (JapaneseNews)")
    time.sleep(1) # 
    
    # 英語ニュースをスプレッドシートからCSVに転送
    english_news_data = spreadsheet_manager.read_sheet_data('EnglishNews!A1:D5')
    CSVFileManager.write_csv_data('data_csv/latest_yahoo_en_news.csv', english_news_data)
    print("Data written to LatestYahoo_En_news.csv")

    # Chat GPTへヤフーニュースを踏まえた、市場動向予測をリクエスト
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    assistant = NewsQueryAssistant(api_key)
    response = assistant.process_queries()
    if response:
        print(response)
    
    time.sleep(1) # 
    
    # Write the responses to a CSV file
    csv_editor = CSVEditor('data_csv/response_from_chatGPT.csv')
    csv_editor.write_to_csv([response])

    # Read the CSV file data
    csv_data = CSVFileManager.read_csv_data('data_csv/response_from_chatGPT.csv')

    # Write data to Google Sheets
    spreadsheet_manager.write_sheet_data(csv_data, 'GPTresponse!A1:D5')  # Adjust the range as needed
    print("Responses sent to Google Sheets (GPTresponse)")

    
    
if __name__ == "__main__":
    main()
