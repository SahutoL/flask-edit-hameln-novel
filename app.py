from flask import Flask, request, jsonify, render_template
from DrissionPage import ChromiumOptions, ChromiumPage
from flask_socketio import SocketIO, emit
import threading, time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


last_request_time = 0
RATE_LIMIT = 10

def login(page, userId, password):
    try:
        page.get("https://syosetu.org/")
        page.ele("@value=ログインページへ").click()
        time.sleep(2)
        page.ele("@name=id").input(userId)
        page.ele("@name=pass").input(password)
        page.ele("@value=ログイン").click()
        time.sleep(2)
    except Exception as e:
        print(f"ログインエラー: {e}")
        page.quit()
        return

def get_favorites(page):
    novels = list()
    try:
        page.get("https://syosetu.org/?mode=favo")
        novel_num = int(page.ele(".heading").text[3:-1])
        if novel_num % 10 == 0:
            page_num = novel_num // 10
        else:
            page_num = (novel_num // 10) + 1
        for i in range(int(page_num)):
            page.get(f'https://syosetu.org/?mode=favo&page={i+1}')
            links = page.eles("@name=multi_id")
            novels.extend([link.attr('value') for link in links])
            time.sleep(3)
            socketio.emit('progress', {'data': f'小説情報取得中：{i*10} / {novel_num}'})
        return novels, novel_num
    except Exception as e:
        print(f"お気に入り小説取得エラー: {e}")
        return novels, 0

def register_details(page, novels, no_note, no_tag, novel_num):
    for idx, novel in enumerate(novels, start=1):
        try:
            url = f'https://syosetu.org/?mode=favo_input&nid={novel}'
            page.get(url)
            author = page.ele(".section3").ele('tag:h3').text.split('）(')[0].split('（作者：')[1]
            title = page.ele(f'@href=https://syosetu.org/novel/{novel}/').text

            if not no_note:
                textfield = page.ele("#text")
                text_to_input = f'作品名：{title}\n作者名：{author}'
                existing_text = textfield.text
                if text_to_input.split('\n')[0] not in existing_text.split(' ') or text_to_input.split('\n')[1] not in existing_text.split(' '):
                    textfield.input(text_to_input)

            if not no_tag:
                script = f"""
                    var ul = document.querySelector('ul.tagit.ui-widget.ui-widget-content.ui-corner-all');
                    var exists = Array.from(ul.children).some(li => li.childNodes[0].textContent === '{title}');
                    if (!exists) {{
                        document.getElementById('singleFieldTags2').value += ',{title}'
                    }}
                """
                page.run_js(script)

            time.sleep(1)
            page.ele("@value=詳細内容登録").click()
            time.sleep(2)

            # 進捗をクライアントに送信
            progress = f'小説情報編集中：{idx} / {novel_num}'
            socketio.emit('progress', {'data': progress})
        except Exception as e:
            print(f'対象の小説は削除されているか或は非公開に設定されています。\n https://www.google.com/search?q=site:syosetu.org%20nid={novel} にて該当作品の情報が見つかるかもしれません')
    time.sleep(1)
    socketio.emit('progress', {'data': '処理が完了しました'})
    page.quit()


@app.route('/', methods=['GET', 'POST'])
def index():
    global last_request_time

    if request.method == 'POST':
        userId = request.form['userId']
        password = request.form['password']
        no_note = 'no_note' in request.form
        no_tag = 'no_tag' in request.form

        # レート制限チェック
        current_time = time.time()
        if current_time - last_request_time < RATE_LIMIT:
            return jsonify({"error": "リクエストが多すぎます。少し待ってから再試行してください。"})

        last_request_time = current_time

        co = ChromiumOptions()
        co.incognito()
        co.headless()
        co.set_argument('--no-sandbox')
        co.set_argument('--guest')

        page = ChromiumPage()

        login(page, userId, password)
        novels, novel_num = get_favorites(page)
        if novels:
            threading.Thread(target=register_details, args=(page, novels, no_note, no_tag, novel_num)).start()
        else:
            page.quit()

        return jsonify({"message": "処理が開始されました。進捗はリアルタイムで表示されます。"})

    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == "__main__":
    socketio.run(app, debug=False, allow_unsafe_werkzeug=False)
