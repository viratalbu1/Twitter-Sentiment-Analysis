import re

import bcrypt as bcrypt
from flask import Flask, render_template, request, jsonify, sessions, redirect, url_for
import tweepy
from textblob import TextBlob
from forms import RegistrationForm,LoginForm
import pymysql


consumer_key = 'z6eNxUUQPMwC8Z7222jyn87sT'
consumer_secret = 'cedM9qVCLzqXQesoTPXCfoXPHATof3MDAKHDpQ09kPY6pgakbD'

access_token = '1114969877780082688-9syQfdRSaL4u22fVK1TAan5MVDW0qR'
access_token_secret = 'T5q43Oi9nHQcZxfeGVPjHIekTlxoNbzWXTsC6pOnthGre'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

app = Flask(__name__)

db = pymysql.connect("localhost", "root", "", "twitter_user")

@app.route("/")
def hello():
    return render_template('index.html')



@app.route("/register" ,methods=['POST','GET'])
def register():
    if request.method=='POST':
        FirstName= request.form['FirstName']
        LastName = request.form['LastName']
        UserName = request.form['UserName']
        Email = request.form['Email']
        Password = request.form['pass']

        cur=db.cursor()
        cur.execute("INSERT INTO user(FirstName,LastName,UserName,Email,Password) VALUES(%s,%s,%s,%s,%s)",(FirstName,LastName,UserName,Email,Password))
        db.commit()
        return render_template('Userlogin.html')



    return  render_template('RegisterUser.html')

@app.route("/UserLogin" ,methods=['POST','GET'])
def UserLogin():
    if request.method == 'POST':
        UserName=request.form['username']
        Password=request.form['pass']

        cur = db.cursor(pymysql.cursors.DictCursor)

        cur.execute("SELECT * FROM user where UserName=%s ",(UserName))
        user=cur.fetchone()
        cur.close()
        if len(user)>0:
           if user['Password']==Password:
               return render_template('SentimentHome.html')
           else:
               return 'Username Or Password Is Not Correct Please Go back And Try Again'
    return render_template('UserLogin.html')


@app.route('/home')
def home():
    return render_template('SentimentHome.html')

@app.route("/Analyse")
def Analyse():
    return render_template('Analyse.html')

@app.route("/Graph" ,methods = ['POST', 'GET'])
def Graph():
    if request.method == 'POST':
     search_tweet=request.form.get("search_tweet")
     t = []
     cpolarity = 0
     positive = 0
     wpositive = 0
     spositive = 0
     negative = 0
     wnegative = 0
     snegative = 0
     neutral = 0

     tweets = api.search(q=search_tweet + " " + "-filter:retweets", count=100, lang='en', tweet_mode='extended',
                         result_type='recent', show_user='true')
     for tweet in tweets:
         polarity=(TextBlob( ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.full_text).split())).sentiment.polarity)
         subjectivity=(TextBlob(tweet.full_text).sentiment.subjectivity)
         cpolarity+=1
         if (polarity == 0):  # adding reaction of how people are reacting to find average later
             neutral += 1
         elif (polarity > 0 and polarity <= 0.3):
             wpositive += 1
         elif (polarity > 0.3 and polarity <= 0.6):
             positive += 1
         elif (polarity > 0.6 and polarity <= 1):
             spositive += 1
         elif (polarity > -0.3 and polarity <= 0):
             wnegative += 1
         elif (polarity > -0.6 and polarity <= -0.3):
             negative += 1
         elif (polarity > -1 and polarity <= -0.6):
             snegative += 1


     return render_template('graph.html',positive=positive,spositive=spositive,negative=negative,snegative=snegative,neutral=neutral,notcategory=100-(positive+spositive+negative+snegative+neutral),search_tweet=search_tweet)





@app.route("/result",methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
       search_tweet = request.form.get("analyse")

       t = []
       subjectivity=[]
       polarity=[]
       tweets = api.search(q=search_tweet+" "+"-filter:retweets",rpp=100,lang='en', tweet_mode='extended',result_type='recent',show_user='true')
       for tweet in tweets:
           polarity.append(TextBlob(tweet.full_text).sentiment.polarity)
           subjectivity.append(TextBlob(tweet.full_text).sentiment.subjectivity)
           t.append(""+( ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.full_text).split())))


       return render_template('result.html',tweet=t,search_tweet=''+search_tweet,polarity=polarity,subjectivity=subjectivity)




if __name__=='__main__':
    app.run(debug=True)