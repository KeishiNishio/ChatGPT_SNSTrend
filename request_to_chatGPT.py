from openai import OpenAI
import os
from edit_csv import CSVEditor


######################
#######　概要　########
######################

'''
ニュースデータを踏まえた ChatGPT への質問クエリを作成するためのファイル
'''


class NewsQueryAssistant:
    def __init__(self, api_key, news_csv_path='latest_yahoo_en_news.csv', questions_csv_path='user_questions.csv'):
        self.client = OpenAI(api_key=api_key)
        self.csv_editor_news = CSVEditor(news_csv_path)  
        self.csv_editor_questions = CSVEditor(questions_csv_path) 

    # CSV ファイルからコンテンツの読み取り
    def read_from_csv(self, csv_editor):
        # 
        return csv_editor.read_from_csv()

    # ニュースデータを踏まえた ChatGPT の質問クエリを作成
    def query_chat_gpt(self, news_text, question_text):
        if not news_text or not question_text:
            print("No text found in the CSV files.")
            return

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": f"Given these news: {news_text}, {question_text}"
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during API request: {e}")
            return None

    # ニュース・質問が書かれたファイルを読み取り、クエリを送信
    def process_queries(self):
        news_text = self.read_from_csv(self.csv_editor_news)
        question_text = self.read_from_csv(self.csv_editor_questions)
        return self.query_chat_gpt(news_text, question_text)

if __name__ == "__main__":
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    assistant = NewsQueryAssistant(api_key)
    response = assistant.process_queries()
    if response:
        print(response)
