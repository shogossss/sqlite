from flask import(
Blueprint,render_template,request
)
import tweepy,time
from userdb import get_db,close_db

def like_tweepy(userid,query,cnt,api,posts):
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
               db = get_db()
               db.execute("INSERT INTO tweet (id,created_at,user_id,text,fav,retweet,action) values(?,?,?,?,?,?,?)", (userid,post["created_at"],post["user_id"],post["text"], post["fav"],post["retweet"],post["select"]))
               db.commit()
               close_db()

        except Exception as e:
                print(e)

    return posts

def follow_tweepy(userid,query,cnt,api,posts):
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
               db = get_db()
               db.execute("INSERT INTO tweet (id,created_at,user_id,text,fav,retweet,action) values(?,?,?,?,?,?,?)", (userid,post["created_at"],post["user_id"],post["text"], post["fav"],post["retweet"],post["select"]))
               db.commit()
               close_db()

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
               db = get_db()
               db.execute("INSERT INTO tweet (id,created_at,user_id,text,fav,retweet,action) values(?,?,?,?,?,?,?)", (userid,post["created_at"],post["user_id"],post["text"], post["fav"],post["retweet"],post["select"]))
               db.commit()
               close_db()

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
