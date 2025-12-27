from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import requests
import threading
import time
import tls_client
import json
from datetime import datetime, timedelta

def reloadconfig():
    try:
        with open("config.json", "r", encoding='utf-8-sig') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

latest_data_tsr = None
latest_data_mb = None
session_mb = tls_client.Session(client_identifier="chrome_124", random_tls_extension_order=True)

def fetch_data_mb():
    global latest_data_mb
    while True:
        try:
            mbapi = reloadconfig()['mbapi']
            if not mbapi:
                print("Failed to load config, skipping data fetch.")
                continue

            time1 = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
            time2 = datetime.now().strftime("%d/%m/%Y")
            accountNo = mbapi["accountNo"]
            sessionId = mbapi["sessionId"]
            refNo = accountNo + '-' + datetime.now().strftime("%Y%m%d%H%M%S") + '00'
            deviceIdCommon = mbapi["deviceIdCommon"]

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
                'Authorization': 'Basic RU1CUkVUQUlMV0VCOlNEMjM0ZGZnMzQlI0BGR0AzNHNmc2RmNDU4NDNm',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json; charset=UTF-8',
                'Deviceid': deviceIdCommon,
                'Origin': 'https://online.mbbank.com.vn',
                'RefNo': refNo,
                'Referer': 'https://online.mbbank.com.vn/information-account/source-account',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'X-Request-Id': refNo,
                'elastic-apm-traceparent': '00-9b4ee430b955c44fb47f4fc719b62fc1-d6aee1a9f85676cb-01',
                'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            json_data = {
                'accountNo': accountNo,
                'fromDate': time1,
                'toDate': time2,
                'sessionId': sessionId,
                'refNo': refNo,
                'deviceIdCommon': deviceIdCommon,
            }

            response = session_mb.post(
                'https://online.mbbank.com.vn/api/retail-transactionms/transactionms/get-account-transaction-history',
                headers=headers,
                json=json_data,
            )

            latest_data_mb = response.json()
            socketio.emit('update_mb', latest_data_mb)
        except: None
        time.sleep(1)

@app.route('/mbapiserver', methods=['GET'])
def mbapiserver():
    global latest_data_mb
    return jsonify(latest_data_mb)

@socketio.on('connect')
def handle_connect():
    global latest_data_mb
    if latest_data_mb:
        emit('update_mb', latest_data_mb)

if __name__ == '__main__':
    
    mb_thread = threading.Thread(target=fetch_data_mb)
    mb_thread.daemon = True
    mb_thread.start()

    socketio.run(app, port=8888, debug=False)
