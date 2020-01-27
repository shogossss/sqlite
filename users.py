from flask import(
Blueprint,render_template,request
)
import tweepy
from userdb import get_db,close_db
global id
global api
id = 0
bp = Blueprint('users', __name__)
@bp.route('/')
def index():
    # db = get_db()
    # alldata = db.execute('SELECT * FROM user').fetchall()
    # print(alldata)
    message="あなたのAPIを入力してね"
    return render_template('login.html', message=message)

@bp.route('/tweet', methods = ["GET" , "POST"])
def tweet():
    if request.method == 'POST':
        try:
            db = get_db()
            username  = request.form['username']
            password = request.form['pass']
            db.execute("INSERT INTO api (ck,cs,at,ats) values(?,?,?,?)", (CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_SECRET))
            #tweepy
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
            #APIインスタンスを作成
            api = tweepy.API(auth)
            db.commit()
            close_db()
        # index.html をレンダリングする
            return render_template('create_user.html')

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
        return render_template('login.html')



@bp.route('/create_user', methods = ["GET","POST"])
def create_user():
    return render_template('create_user.html')

@bp.route('/login', methods = ["GET" , "POST"])
def login():
    if request.method == 'POST':
        try:
            global username,password,CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_SECRET
            username = request.form['username']
            password = request.form['password']
            CONSUMER_KEY  = request.form['ck']
            CONSUMER_SECRET = request.form['cs']
            ACCESS_TOKEN = request.form['at']
            ACCESS_SECRET = request.form['ats']
            return render_template(
            'check.html',
            username=username,
            password=password,
            ck=CONSUMER_KEY,
            cs=CONSUMER_SECRET,
            at=ACCESS_TOKEN,
            ats=ACCESS_SECRET
            )

        except Exception as e:
            print(e)
            return render_template(
            'create_user.html'
            )
    else:
        return render_template('create_user.html')

@bp.route('/login2', methods = ["GET" , "POST"])
def login2():
    if request.method == 'POST':
        try:
            db = get_db()
            db.execute("INSERT INTO user (username,password) values(?,?)", (username,password))
            db.execute("INSERT INTO api (ck,cs,at,ats) values(?,?,?,?)", (CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_SECRET))
            # #tweepy
            # auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            # auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
            # #グローバル変数
            # global api
            # #APIインスタンスを作成
            # api = tweepy.API(auth)
            db.commit()
            close_db()
        # index.html をレンダリングする
            return render_template('login.html')

        except Exception as e:
            print(e)
            message = "そのusernameはすでに使われております"
            return render_template(
            'create_user2.html',
            message=message,
            username=username,
            password=password,
            ck=CONSUMER_KEY,
            cs=CONSUMER_SECRET,
            at=ACCESS_TOKEN,
            ats=ACCESS_SECRET
            )
    else:
        return render_template('base.html')

@bp.route('/login3', methods = ["GET" , "POST"])
def login3():
    return render_template(
    'create_user2.html',
    username=username,
    password=password,
    ck=CONSUMER_KEY,
    cs=CONSUMER_SECRET,
    at=ACCESS_TOKEN,
    ats=ACCESS_SECRET
    )
