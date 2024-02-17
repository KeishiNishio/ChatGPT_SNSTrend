import csv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

######################
#######　概要　########
######################

'''
登録したスプレッドシートとローカルマシンのデータ通信のためのクラス（メソッド）
'''

class SpreadsheetManager:
    def __init__(self, service_account_file, spreadsheet_id):
        # グーグルドライブ上のGoogle スプレッドシートの認証情報とスプレッドシートIDを設定
        self.creds = Credentials.from_service_account_file(
            service_account_file, scopes=['https://www.googleapis.com/auth/spreadsheets'])
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.spreadsheet_id = spreadsheet_id

    def read_sheet_data(self, range_name):
        # グーグルドライブ上のスプレッドシートからデータを読み込む
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range_name
        ).execute()
        return result.get('values', [])

    def write_sheet_data(self, data, range_name):
        # グーグルドライブのスプレッドシートにデータを書き込む
        body = {'values': data}
        request = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body
        )
        response = request.execute()
        return response

class CSVFileManager:
    @staticmethod
    def read_csv_data(csv_file):
        # CSVファイルからデータを読み込む静的メソッド
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)
        return data

    @staticmethod
    def write_csv_data(csv_file, data, mode='w'):
        # CSVファイルにデータを書き込む静的メソッド
        with open(csv_file, mode=mode, encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)

def main():
    # SpreadsheetManagerとCSVFileManagerを使用し
    # Google スプレッドシートとCSVファイル間でデータを移動する処理
    spreadsheet_manager = SpreadsheetManager('support_account_key.json', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    
    # yahooニュースをCSVファイルからスプレッドシートに転送
    japanese_news_csv = 'data_csv/latest_yahoo_ja_news.csv'
    japanese_news_data = CSVFileManager.read_csv_data(japanese_news_csv)
    spreadsheet_manager.write_sheet_data(japanese_news_data, 'JapaneseNews!A1:D5')

    # スプレッドシート（GCP上で英訳されたニュース）からローカルマシン内のCSVファイルに転送
    english_news_data = spreadsheet_manager.read_sheet_data('EnglishNews!A1:D5')
    CSVFileManager.write_csv_data('data_csv/latest_yahoo_en_news.csv', english_news_data)

    print("Data written to LatestYahoo_En_news.csv")

if __name__ == "__main__":
    main()
