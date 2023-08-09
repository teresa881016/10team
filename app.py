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

        # 빈칸 있는지 확인하기
        if not(name_receive and id_receive and pw_receive and pw2_receive and nickname_receive):
            error_msg = "입력되지 않은 정보가 있습니다."
            return render_template("join.html", error_msg=error_msg)

        
        # 비밀번호 일치 여부 확인하기
        elif pw_receive != pw2_receive:
            error_msg =  "비밀번호가 일치하지 않습니다."
            return render_template("join.html", error_msg=error_msg)

        else:
            # 이상 없으면 다음과 같은 값을 DB에 저장하기
            doc = {
                'name': name_receive, 
                'id' : id_receive,
                'pw' : pw_receive,
                'pw2' : pw2_receive,
                'nickname' : nickname_receive   
            }
            db.join.insert_one(doc)
            return jsonify({'msg': '회원가입이 되었습니다.'})

    
@app.route("/join", methods=["GET"])
def login_get():
    all_buckets = list(db.bucket.find({},{'_id':False}))
    return jsonify({'result': all_buckets })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)