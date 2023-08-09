from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient
from math import ceil
from urllib.parse import unquote, quote
# Flask session 객체는 기본적으로 사용자의 웹 브라우저에 쿠키 형태로 데이터를 저장하여 상태를 유지합니다.
# 이를 활용하면 각 사용자마다 로그인 상태를 감지하고, 로그인 상태에 따라 다른 페이지로 이동하거나 로그인 정보를 유지할 수 있습니다.

app = Flask(__name__)
app.secret_key = 'secret_key'

# 사용자 정보를 딕셔너리로 관리하는 대신에 MongoDB를 활용하겠습니다.

# MongoDB 연결 설정
client = MongoClient('mongodb+srv://sparta:test@cluster0.vekhvil.mongodb.net/?retryWrites=true&w=majority')
db = client.EPLgallary

# 회원 정보를 DB에 저장하고 조회하는 함수들을 정의합니다.
def save_user_info(user_id, user_pw, user_nickname):
    db.Login.insert_one({'usrId': user_id, 'password': user_pw, 'nickname': user_nickname})

def check_user_info(user_id):
    return db.Login.find_one({'usrId': user_id})

def get_user_nickname(user_id):
    user_info = db.Login.find_one({'usrId': user_id}, {'nickname': True})
    return user_info['nickname'] if user_info else None

# 홈 페이지
#  'if 'user_id' in session:'이 부분은 세션에 user_id가 있는지 확인하는 부분입니다.
#  로그인 상태를 판단하기 위해 사용합니다.
#  만약 세션에 user_id가 있다면, 사용자가 로그인한 상태라고 간주하고 홈 페이지로 리디렉션합니다.
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('home.html')


# 로그인 페이지
# session['user_id'] = user_id: 이 부분은 로그인이 성공했을 때, 세션에 user_id를 저장하는 부분입니다.
# 이렇게 하면 앞으로 사용자가 로그인한 상태를 유지할 수 있습니다.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']

        # 사용자 정보를 DB에서 조회하여 확인합니다.
        user_info = check_user_info(user_id)

        if user_info and user_info['password'] == user_pw:
            session['user_id'] = user_id
            session['user_nickname'] = user_info['nickname']  # 닉네임 정보를 세션에 저장
            return redirect(url_for('home'))
        else:
            error_message = "로그인 실패!"
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')

# 회원가입 페이지
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        user_nickname = request.form['user_nickname']

        # 이미 등록된 아이디인지 확인합니다.
        if check_user_info(user_id):
            error_message = "이미 등록된 아이디입니다."
            return render_template('register.html', error_message=error_message)

        # 회원 정보를 DB에 저장합니다.
        save_user_info(user_id, user_pw, user_nickname)
        return redirect(url_for('login'))

    return render_template('register.html')

# 로그아웃 페이지
# session.pop('user_id', None): 이 부분은 로그아웃 시 세션에서 user_id를 삭제하는 부분입니다.
#  로그아웃을 수행하면 세션에서 user_id 정보가 삭제되며, 사용자는 다시 로그인해야 합니다.
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)