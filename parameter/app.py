from flask import Flask, render_template, request, jsonify, Response
import sqlite3
import datetime
import os
import io # ★ここを追加
import csv # ★ここも追加

# Flaskアプリケーションのインスタンスを作成
# __name__ はPythonの特殊変数で、現在のモジュール名が入る
app = Flask(__name__)

# データベースファイル名
# プロジェクトのルートディレクトリに作成される
DATABASE = 'location_logs.db'

# データベースの初期化関数
# テーブルが存在しない場合に作成する
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()
    print("Database initialized or already exists.")

# ルートURL ("/") にアクセスがあったときに実行される関数
# GETリクエストを受け付ける
@app.route('/')
def index():
    # 'index.html' テンプレートをレンダリングして返す
    # render_template は 'templates' フォルダの中から指定されたファイルを探す
    return render_template('index.html')

# '/submit_location' というURLにPOSTリクエストがあったときに実行される関数
# Androidアプリから位置情報を受け取るためのAPIエンドポイントを想定
@app.route('/submit_location', methods=['POST'])
def submit_location():
    # リクエストボディがJSON形式かどうかをチェック
    if request.is_json:
        data = request.get_json() # JSONデータを取得

        device_id = data.get('device_id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        # アプリ側でタイムスタンプを生成して送るのが理想だけど、
        # ない場合はサーバー側で生成
        timestamp = data.get('timestamp', datetime.datetime.now().isoformat())

        # 必要なデータが揃っているか確認
        if not all([device_id, latitude, longitude]):
            print(f"Error: Missing data. Received: {data}")
            return jsonify({"status": "error", "message": "Missing data"}), 400

        try:
            # データベースに接続し、データを挿入
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO locations (device_id, latitude, longitude, timestamp) VALUES (?, ?, ?, ?)",
                    (device_id, latitude, longitude, timestamp)
                )
                conn.commit()
            print(f"Successfully saved location from {device_id}: Lat={latitude}, Lon={longitude}, Time={timestamp}")
            return jsonify({"status": "success", "message": "Location data received and saved."}), 200
        except Exception as e:
            # データベース操作でエラーが発生した場合
            print(f"Database operation error: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        # JSON形式でないリクエストの場合
        print("Error: Request must be JSON.")
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

# '/view_locations' というURLにアクセスがあったときに実行される関数
# データベースに保存された位置情報をHTMLで表示する
@app.route('/view_locations')
def view_locations():
    locations = []
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # データベースから全データを取得、新しいものから順に並び替え
            cursor.execute("SELECT device_id, latitude, longitude, timestamp FROM locations ORDER BY timestamp DESC")
            locations = cursor.fetchall()
            print(f"Fetched {len(locations)} locations from DB.")
    except Exception as e:
        print(f"Error fetching locations: {e}")
    # 取得した位置情報を 'locations.html' テンプレートに渡して表示
    return render_template('locations.html', locations=locations)


# '/export_locations' というURLにアクセスがあったときに実行される関数
# データベースに保存された位置情報をCSVとしてダウンロードできるようにする
@app.route('/export_locations')
def export_locations():
    output = io.StringIO()
    writer = csv.writer(output)

    # ヘッダーを書き込む
    writer.writerow(['Device ID', 'Latitude', 'Longitude', 'Timestamp'])

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT device_id, latitude, longitude, timestamp FROM locations ORDER BY timestamp DESC")
            for row in cursor:
                writer.writerow(row)
        
        output.seek(0) # ストリームの先頭に戻す
        
        # ファイル名を生成 (例: locations_20250530_153000.csv)
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"locations_{timestamp_str}.csv"
        
        # CSVファイルとしてダウンロードさせるレスポンスを返す
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        print(f"Error exporting locations: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# アプリケーションが直接実行されたときにサーバーを起動
if __name__ == '__main__':
    init_db() # データベースの初期化をここで行う
    # host='0.0.0.0' にすると、同じネットワーク内の他のデバイスからもアクセスできる
    # debug=True にすると、コードの変更が自動で反映されたり、デバッグ情報が表示される
    app.run(host='0.0.0.0', port=5000, debug=True)