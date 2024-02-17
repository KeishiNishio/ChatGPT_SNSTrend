import csv

######################
#######　概要　########
######################

'''
CSVファイル周りの処理を記載したクラス
'''

class CSVEditor:
    def __init__(self, default_filename='data_csv/latest_yahoo_ja_news.csv'):
        self.default_filename = default_filename

    # コンテンツを CSV ファイルに書き込む
    def write_to_csv(self, content, filename=None, mode='a'):
        if filename is None:
            filename = self.default_filename
        with open(filename, mode=mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(content if isinstance(content, list) else [content])

    # CSV ファイルの内容をクリア
    def clear_csv(self, filename=None):
        if filename is None:
            filename = self.default_filename
        open(filename, 'w').close()
    
    # CSV ファイルからコンテンツを読み込む
    def read_from_csv(self, filename=None):
        if filename is None:
            filename = self.default_filename
        news_text = ''
        try:
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    news_text += ' '.join(row) + ' '
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None
        return news_text
