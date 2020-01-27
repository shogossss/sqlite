from flask import(
Blueprint,render_template,request
)
import tweepy

from userdb import get_db,close_db
global id
id = 0
bp = Blueprint('users', __name__)
@bp.route('/')
def index():
    # db = get_db()
    # alldata = db.execute('SELECT * FROM user').fetchall()
    # print(alldata)
    message="あなたのAPIを入力してね"
    return render_template('index.html', message=message)

@bp.route('/tweet', methods = ["GET" , "POST"])
def tweet():
    if request.method == 'POST':
        try:
            db = get_db()
            global CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_SECRET

            CONSUMER_KEY  = request.form['a']
            CONSUMER_SECRET = request.form['b']
            ACCESS_TOKEN = request.form['c']
            ACCESS_SECRET = request.form['d']
            db.execute("INSERT INTO api (ck,cs,at,ats) values(?,?,?,?)", (CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_SECRET))
            #tweepy
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


            #グローバル変数
            global api
            #APIインスタンスを作成
            api = tweepy.API(auth)
            db.commit()
            close_db()
        # index.html をレンダリングする
            return render_template('base.html')

        except Exception as e:
            print(e)
            messages = "適切な文字を入力してください"
            title = "API認証"
            return render_template(
            'check.html',
            message = messages,
            title = title
            )
    else:
        return render_template('base.html')
