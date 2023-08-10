from flask import Flask, render_template, request, jsonify, flash
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.bko1xj3.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('join.html')

@app.route("/join", methods=["POST", "GET"])
def join_post():
    if request.method == "GET":
        return render_template("join.html")

    else:
        name_receive = request.form['name_give']
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']
        pw2_receive = request.form['pw2_give']
        nickname_receive = request.form['nickname_give']

        existing_user = db.join.find_one({'id': id_receive})
        existing_nickname = db.join.find_one({'nickname': nickname_receive})

        if existing_user:
            return jsonify({'msg': '중복된 아이디 입니다'})
        elif existing_nickname:
            return jsonify({'msg': '중복된 닉네임 입니다'})


        doc = {
            'name': name_receive, 
            'id' : id_receive,
            'pw' : pw_receive,
            'pw2' : pw2_receive,
            'nickname' : nickname_receive   
        }
        db.join.insert_one(doc)
        return jsonify({'msg': '회원가입이 되었습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)