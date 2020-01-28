from flask import(
Blueprint,render_template,request
)
import tweepy,time
from userdb import get_db,close_db
global id
id = 0



bp = Blueprint('users', __name__)
@bp.route('/')
def index():
    # db = get_db()
    # alldata = db.execute('SELECT * FROM user').fetchall()
    # print(alldata)
    return render_template('login.html')

@bp.route('/tweet', methods = ["GET" , "POST"])
def tweet():
    if request.method == 'POST':
        try:
            db = get_db()
            d = db.cursor()
            pass1=[]
            user1=[]
            username  = request.form['username']
            password = request.form['pass']
            d.execute("select id,username,password from user")
            for d1 in d:
                pass1.append(str(d1["password"]))
                user1.append(str(d1["username"]))
                if(str(d1["username"])==username):
                    id = d1["id"]


            if(password in pass1 and username in user1):
                d.execute('select id,ck,cs,at,ats from api')
                for d2 in d:
                    if(d2["id"]==id):
                        ck = str(d2["ck"])
                        cs = str(d2["cs"])
                        at = str(d2["at"])
                        ats = str(d2["ats"])
                #tweepy
                auth = tweepy.OAuthHandler(ck, cs)
                auth.set_access_token(at, ats)
                #APIインスタンスを作成
                global api
                api = tweepy.API(auth)
                db.commit()
                close_db()
            # index.html をレンダリングする
                return render_template('base.html')

            else :
                message2='パスワードかusernameが間違っております'
                return render_template(
                'login.html',
                message2=message2
                )

        except Exception as e:
            print(e)
            message2 = "usernameが間違っております"
            return render_template(
            'login.html',
            message2 = message2
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

@bp.route('/tweetaction', methods =["GET","POST"])
def tweetaction():
    if request.method == 'POST':
       query = request.form['query']# formのname = "query"を取得
       cnt = int(request.form['count'])
       button = request.form['button']
       posts = []
       try:
           if button == "like":
               posts = like_tweepy(query,cnt,api,posts)
           if button == "retweet":
               posts = retweet_tweepy(query,cnt,api,posts)
           if button == "follow":
               posts = follow_tweepy(query,cnt,api,posts)
           # grouped_df = get_grouped_df(tweets_df)
           # sorted_df = get_sorted_df(tweets_df)
           # 送られてきたものを返すしなきゃ返されない
           return render_template(
               'index.html',
               query = query,
               count = cnt,
               # profile=get_profile(user_id),
               posts = posts
               # grouped_df = grouped_df,
               # sorted_df = sorted_df
               )
       except:
            messages = "APIが違います"
            title = "APIエラー"
            return render_template(
            'recheck.html',
            message = messages,
            title = title,
            CONSUMER_KEY = CONSUMER_KEY,
            CONSUMER_SECRET = CONSUMER_SECRET,
            ACCESS_TOKEN = ACCESS_TOKEN,
            ACCESS_SECRET = ACCESS_SECRET
            )

    else:
            return render_template('index.html')

def like_tweepy(query,cnt,api,posts):
    search_results = api.search(q=query, count=cnt)
    for tweet in search_results:
        post = {}
        try:
            if not "RT @" in tweet.text: #3
               tweet_id = tweet.id
               api.create_favorite(tweet_id) #ファボする
               post["created_at"] = tweet.created_at
               post["user_id"] = tweet.user.screen_name
               post["text"] = tweet.text.replace('\n','')
               post["fav"] = tweet.favorite_count
               post["retweet"] = tweet.retweet_count
               post["select"] = "いいね"
               posts.append(post)
               time.sleep(2)

        except Exception as e:
                print(e)

    return posts

def follow_tweepy(query,cnt,api,posts):
    search_results = api.search(q=query, count=cnt)
    for tweet in search_results:
        post = {}
        try:
            if not "RT @" in tweet.text: #3
               user_id = tweet.user._json['id']
               api.create_friendship(user_id) #ファボする #ファボする
               post["created_at"] = tweet.created_at
               post["user_id"] = tweet.user.screen_name
               post["text"] = tweet.text.replace('\n','')
               post["fav"] = tweet.favorite_count
               post["retweet"] = tweet.retweet_count
               post["select"] = "フォロー"
               posts.append(post)
               time.sleep(1)

        except Exception as e:
            print(e)

    return posts

def retweet_tweepy(query,cnt,api,posts):
    search_results = api.search(q=query, count=cnt)
    for tweet in search_results:
        post = {}
        try:
            if not "RT @" in tweet.text: #3
               tweet_id = tweet.id
               api.retweet(tweet_id) #ファボする
               post["created_at"] = tweet.created_at
               post["user_id"] = tweet.user.screen_name
               post["text"] = tweet.text.replace('\n','')
               post["fav"] = tweet.favorite_count
               post["retweet"] = tweet.retweet_count
               post["select"] = "リツイート"
               posts.append(post)
               time.sleep(1)

        except Exception as e:
            print(e)

    return posts

def get_profile(user_id):
   user = api.get_user(screen_name= user_id) #1
   profile = { #2
       "id": user.id,
       "user_id": user_id,
       "image": user.profile_image_url,
       "description": user.description # 自己紹介文の取得
   }
   return profile #3

def get_grouped_df(tweets_df):
   grouped_df = tweets_df.groupby(tweets_df.created_at.dt.date).sum().sort_values(by="created_at", ascending=False)
   return grouped_df

def get_sorted_df(tweets_df):
   sorted_df = tweets_df.sort_values(by="retweets", ascending=False)
   return sorted_df
