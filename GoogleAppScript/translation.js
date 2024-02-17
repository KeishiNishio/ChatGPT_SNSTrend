function translateJapaneseNewsToEnglish() {
    // スプレッドシートIDを使用してスプレッドシートを開く
    var spreadsheetId = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
    var spreadsheet = SpreadsheetApp.openById(spreadsheetId);
  
    var sourceSheet = spreadsheet.getSheetByName('JapaneseNews'); // JapaneseNewsシートから読み込む
    var targetSheet = spreadsheet.getSheetByName('EnglishNews'); // 結果をEnglish Newsシートに書き込む
  
    // ソースシートを取得
    var range = sourceSheet.getDataRange();
    var values = range.getValues();
  
    var translatedValues = [];
  
    // 翻訳処理
    for (var i = 0; i < values.length; i++) {
      translatedValues[i] = [];
      for (var j = 0; j < values[i].length; j++) {
        if (values[i][j]) { // 空でないセルのみ翻訳
          var translatedText = LanguageApp.translate(values[i][j], 'ja', 'en'); // 日本語から英語に翻訳
          translatedValues[i].push(translatedText);
        } else {
          translatedValues[i].push('');
        }
      }
    }
  
    // 翻訳した内容をターゲットシートに書き込む
    targetSheet.getRange(1, 1, translatedValues.length, translatedValues[0].length).setValues(translatedValues);
  }
  