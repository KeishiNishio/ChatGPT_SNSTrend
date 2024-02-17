// スプレッドシートを開く
function openSpreadsheet() {
    var spreadsheetId = '1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
    return SpreadsheetApp.openById(spreadsheetId);
  }
  
  // スプレッドシートのデータを読み取る
  function getSpreadsheetData() {
    var spreadsheet = openSpreadsheet();
    var sourceSheet = spreadsheet.getSheetByName('GPTresponse');
    var targetSheet = spreadsheet.getSheetByName('GPTresponseJa');
  
    var range = sourceSheet.getDataRange();
    var values = range.getValues();
    var translatedValues = [];
  
    for (var i = 0; i < values.length; i++) {
      translatedValues[i] = [];
      for (var j = 0; j < values[i].length; j++) {
        var translatedText = values[i][j] ? LanguageApp.translate(values[i][j], 'en', 'ja') : '';
        translatedValues[i].push(translatedText);
      }
    }
  
    // Write to the target sheet
    targetSheet.getRange(1, 1, translatedValues.length, translatedValues[0].length).setValues(translatedValues);
    return translatedValues;
  }
  
  // LINE Notifyを通じて通知を送る
  function sendToLine() {
    var values = getSpreadsheetData();
    var message = '';
    for (var i = 0; i < values.length; i++) {
      for (var j = 0; j < values[i].length; j++) {
        message += values[i][j] + '\t';
      }
      message += '\n';
    }
  
    var token = '85OYip08crx8yi73Zq5o7PvTUPYXf0L03blDZEXjp2e';
    var options = {
      'method' : 'post',
      'headers' : {
        'Authorization' : 'Bearer ' + token
      },
      'payload' : {
        'message' : message
      }
    };
  
    UrlFetchApp.fetch('https://notify-api.line.me/api/notify', options);
  }
  