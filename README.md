# Chat GPT APIを使用したニュース分析

# プロジェクト概要

このプロジェクトでは、Pythonと Google App script 、Chat GPT APIを活用して、ニュースの分析を行います。具体的には、ログイン時のセッション情報を利用して、Twitterのトレンド情報を取得し、そのトレンドワードに関連する記事をYahooニュースから取得。その後、当該記事をChatGPTに読み込ませ、今後の経済への影響について、推測させます。

## 技術スタック

- Python
- Java script (Google App Script)
- Burp suite (通信のモニタリングツール)

## 実装した機能

1. Twitterのニュースタブにおける上位トレンドワードを取得するためのHTTPリクエストを送信
    
    <aside>
    💡 **注意！：TwitterはXに変わってから、Webスクレイピングに関する規約が変更され、利用が推奨されない可能性があるため、コードを流用する場合は、規約を確認した上でクローンしてください
    
    URL:** [https://twitter.com/robots.txt](https://twitter.com/robots.txt)
    
    </aside>
    
2. Yahoo Japanニュースにて、トレンドワードを検索、上位の記事の内容をテキストで出力、ローカルのCSVファイルに保存
    
    <aside>
    💡 Yahoo のニュースサイトは構成が変化する可能性があります。
    
    </aside>
    
3. Chat GPT APIを利用し、ニュースデータを含めた質問クエリに対する回答をLINE botにより、配信
    
    <aside>
    💡 Chat GPT APIは日本語ベースよりも、英語ベースの方がコストが低いため、Google Cloud Platformを使用し、英語に翻訳したニュースデータを使用。以下はその手順である。
    
    </aside>
    
    1. CSVファイルをクラウドベースのGoogle Driveスプレッドシートに転送
    2. スプレッドシートに書かれたテキストデータをGoogle App Scriptを使用して、英訳
    3. Chat GPT APIを使用し、英語ベースのニュースに対する経済への影響を推測させる質問クエリを構成
    4. 返答をLINE Notifyを使用し、LINEに配信

処理概念図

![スクリーンショット 2024-02-17 20.15.59.png](Chat%20GPT%20API%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%9F%E3%83%8B%E3%83%A5%E3%83%BC%E3%82%B9%E5%88%86%E6%9E%90%205a934a20b58e46468cad0061a37f2c05/%25E3%2582%25B9%25E3%2582%25AF%25E3%2583%25AA%25E3%2583%25BC%25E3%2583%25B3%25E3%2582%25B7%25E3%2583%25A7%25E3%2583%2583%25E3%2583%2588_2024-02-17_20.15.59.png)

## 挙動

![IMG_9544.PNG](Chat%20GPT%20API%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%9F%E3%83%8B%E3%83%A5%E3%83%BC%E3%82%B9%E5%88%86%E6%9E%90%205a934a20b58e46468cad0061a37f2c05/IMG_9544.png)

### 主なクラス構成

### **1. CSVEditor クラス**

このクラスはCSVファイルの読み書きを行う機能を提供します。具体的には、CSVファイルに新しい内容を追加（**`write_to_csv`**メソッド）、CSVファイルの内容をクリア（**`clear_csv`**メソッド）、CSVファイルから内容を読み取る（**`read_from_csv`**メソッド）の3つの機能があります。

### **2. ConfigManager クラス**

**`ConfigManager`**クラスは、設定ファイル（**`sns_settings.ini`**）からTwitter APIの設定情報を読み込むために使用されます。これには、認証トークンやヘッダー情報などが含まれます。

### **3. TwTrendsFetcher クラス**

Twitter APIを使用して現在のトレンドを取得するためのクラスです。トレンドは、**`fetch_trends`**メソッドによって取得されます。

### **4. YahooNewsFetcher クラス**

トレンドに基づいてYahooニュースから記事を取得するためのクラスです。**`fetch_yahoo_news_links_and_titles`**メソッドは検索クエリに基づいてニュースのリンクとタイトルを取得し、**`fetch_article_text_from_json`**メソッドはニュース記事のテキストを取得します。

### **5. NewsQueryAssistant クラス**

Yahooニュースのデータを基にした質問をChatGPTに送信し、回答を取得するためのクラスです。**`process_queries`**メソッドはニュースデータとユーザーからの質問を読み取り、ChatGPTに質問を行い、その回答を処理します。

### **使用方法**

1. 必要なパッケージと設定ファイルを準備します。
2. スクリプトを実行する前に、**`sns_settings.ini`**にTwitter APIの設定情報を、**`support_account_key.json`**にGoogle APIの認証情報の設定、Chat GPTのAPIキーを設定してください。Twitterの認証情報に関しては、Burp suiteなどのモニタリングツールを使用し、ログイン時のセッション情報を取得してください。Google APIに関しては、GCPによってアカウントを開設してください。
    
    ![スクリーンショット 2024-02-17 23.23.52.png](Chat%20GPT%20API%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%9F%E3%83%8B%E3%83%A5%E3%83%BC%E3%82%B9%E5%88%86%E6%9E%90%205a934a20b58e46468cad0061a37f2c05/%25E3%2582%25B9%25E3%2582%25AF%25E3%2583%25AA%25E3%2583%25BC%25E3%2583%25B3%25E3%2582%25B7%25E3%2583%25A7%25E3%2583%2583%25E3%2583%2588_2024-02-17_23.23.52.png)
    

### 開発環境

- Mac OS M1 sonoma 14.11
- python　3.11.4
- pip　23.3.2
- 各モジュールのバージョン
    - pipversion.txt参照