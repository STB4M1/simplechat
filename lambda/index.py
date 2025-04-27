# lambda/index.py

import json
import os
import urllib.request

# 自分のngrok URL
API_URL = "https://6db8-35-198-213-242.ngrok-free.app/predict"

def lambda_handler(event, context):
    try:
        # リクエストボディをパース
        body = json.loads(event['body'])
        message = body['message']

        # APIサーバーに送るデータ
        payload = json.dumps({
            "message": message
        }).encode('utf-8')

        # HTTPリクエスト作成
        req = urllib.request.Request(
            API_URL,
            data=payload,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        # リクエスト送信 & レスポンス受信
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode('utf-8')
            response_data = json.loads(response_body)

        # レスポンスからアシスタント応答を取り出す
        assistant_response = response_data.get("response", "")

        # 成功レスポンスを返す
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
                "conversationHistory": [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": assistant_response}
                ]
            })
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(e)
            })
        }
