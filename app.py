from flask import Flask, request, render_template_string

app = Flask(__name__)

# 奨学金情報のデータベース
scholarships = {
    "文学部": {
        "交換留学": {
            "スイス": {
                "半年": {
                    "給付型": {
                        "併給可能": {"info": "大林財団奨学金(JASSO等のみ併給可能)、北海道大学フロンティア基金新渡戸カレッジ(海外留学) 奨学金(原則)、北海道大学・ニトリ海外留学奨学金(原則)", "link": "https://discord.gg/8hFuaqkP"},
                        "併給不可": {"info": "住友化学グローバルリーダー育成奨学金(条件あり)、JEES・石橋財団奨学金、北海道大学フロンティア基金クラーク海外留学助成奨学金", "link": "https://discord.gg/8hFuaqkP"}
                    },
                    "貸与型": {"info": "", "link": "https://discord.gg/8hFuaqkP"}
                },
                "１年": {
                    "給付型": {
                        "併給可能": {"info": "大林財団奨学金(JASSO等のみ併給可能)、北海道大学フロンティア基金新渡戸カレッジ(海外留学) 奨学金(原則)、北海道大学・ニトリ海外留学奨学金(原則)", "link": "https://discord.gg/8hFuaqkP"},
                        "併給不可": {"info": "スイス政府奨学金、JEES・石橋財団奨学金、北海道大学フロンティア基金クラーク海外留学助成奨学金", "link": "https://discord.gg/8hFuaqkP"}
                    },
                    "貸与型": {"info": "a2文学部貸与", "link": "https://discord.gg/8hFuaqkP"}
                }
            }
        }
    }
}

# 奨学金情報を取得する関数
def get_scholarship_info(w, x, y, z, s, a):
    try:
        scholarship_info = scholarships[w][x][y][z][s][a]
    except KeyError:
        scholarship_info = {"info": "指定された条件に合致する奨学金情報がありません。", "link": "https://discord.gg/8hFuaqkP"}
    return scholarship_info['info'], scholarship_info['link']

# 費用と住居の情報を取得する関数
def cost_and_accommodation(country, period):
    if country == "スイス":
        if period == "1ヶ月以内":
            cost = "月額約150,000円〜200,000円"
            accommodation = "学生寮やシェアハウスが一般的です。"
        elif period == "半年":
            cost = "月額約280,000円〜300,000円"
            accommodation = "学生寮やシェアハウスが一般的です。"
        elif period == "１年":
            cost = "月額約280,000円〜300,000円"
            accommodation = "学生寮やシェアハウスが一般的です。"
    elif country == "アメリカ":
        if period == "1ヶ月以内":
            cost = "月額約100,000円〜150,000円"
            accommodation = "ホームステイや学生寮が一般的です。"
        elif period == "半年":
            cost = "月額約120,000円〜170,000円"
            accommodation = "学生寮やシェアハウスが一般的です。"
        elif period == "１年":
            cost = "月額約110,000円〜160,000円"
            accommodation = "学生寮やシェアハウスが一般的です。"
    return cost, accommodation

# ルート設定
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        w = request.form.get('faculty')
        x = request.form.get('purpose')
        y = request.form.get('country')
        z = request.form.get('period')
        s = request.form.get('scholarship_type')
        a = request.form.get('combination')
        
        # 関数を呼び出して情報を取得
        scholarship_info, scholarship_link = get_scholarship_info(w, x, y, z, s, a)
        cost, accommodation = cost_and_accommodation(y, z)
        
        return render_template_string('''
            <h1>奨学金情報</h1>
            <p>{{ scholarship_info }}</p>
            <h1>予想される費用</h1>
            <p>{{ cost }}</p>
            <h1>住居に関するアドバイス</h1>
            <p>{{ accommodation }}</p>
            <h1>生活に関する詳細情報はこちらのリンクから</h1>
            <a href="{{ scholarship_link }}">{{ scholarship_link }}</a>
            <h1>学外奨学金についてはこちらのリンクから</h1>
            <a href="https://ryugaku.jasso.go.jp/scholarship.html">https://ryugaku.jasso.go.jp/scholarship.html</a>
            <br><br>
            <a href="/">戻る</a>
        ''', scholarship_info=scholarship_info, cost=cost, accommodation=accommodation, scholarship_link=scholarship_link)
    
    return render_template_string('''
        <form method="post">
            <label>学部を選んで下さい:</label>
            <input type="text" name="faculty"><br>
            <label>留学の目的を選んで下さい:</label>
            <input type="text" name="purpose"><br>
            <label>留学予定の国を教えて下さい:</label>
            <input type="text" name="country"><br>
            <label>期間を選んで下さい:</label>
            <input type="text" name="period"><br>
            <label>奨学金の種類を選んで下さい:</label>
            <input type="text" name="scholarship_type"><br>
            <label>併給の有無を選んで下さい:</label>
            <input type="text" name="combination"><br>
            <input type="submit" value="送信">
        </form>
    ''')

import os

# アプリの実行
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render環境用のポート設定
    app.run(host='0.0.0.0', port=port, debug=True)
