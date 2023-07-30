# ==============================================================================
# ----- モジュールのインポート -----
from flask import *
from datetime import datetime
import random
import csv
import pandas as pd
import logging
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from datetime import datetime,timedelta
import os
# ==============================================================================
# ----- Faskインスタンスを生成する -----
app = Flask(__name__)
# ==============================================================================
# ===== ビューを定義する =====
# ------------------------------------------------------------------------------
# ----- トップページ -----

practice_result=[]
experiment_result=[]
impression_result=[]
quationnaire_result=[]

load_dotenv()
client = boto3.client('s3')

connect_df=pd.read_csv("subject/target_ans_connect.csv" ,encoding="utf-8")



#挨拶と参加者IDを取得
@app.route( "/" )
def index():
    return( render_template( "index.html", title="hello", name="") )

#音声大きさチェック
@app.route( "/sound_test", methods=['POST'])
def sound_test():
    global name
    name = request.form["name"]
    return( render_template( "sound_test.html", title="CocktailParty", name=name) )



#練習実験1回目
@app.route( "/practice1")
def practice1():
    global practice_trial,name,ans
    practice_trial=0
    practice_trial+=1
    df=pd.read_csv("subject/practice.csv", encoding='utf-8', header=None)
    practice_animal = df.iloc[practice_trial][4]

    #練習問題の解答を表示させるもの
    practice_animal_ans = df.iloc[practice_trial][5]
    return( render_template( "practice1.html", title="CocktailParty", name=name, trial=practice_trial,animal=practice_animal, animal_ans=practice_animal_ans) )



#練習実験2回目~10回目
@app.route( "/practice2", methods=['POST'])
def practice2():
    global practice_trial,name,ans
    
    #ansとtime（解答時間）のPOST
    ans = request.form["face"]
    time = request.form["time"]

    #ターゲットと実際の回答をつなげて正解か不正解かを判定
    #ans_targetに実験者の回答を修正
    practice_target = connect_df[connect_df['ans'] == ans].iloc[0][0]
    df=pd.read_csv("subject/practice.csv", encoding='utf-8', header=None)
    if df.iloc[practice_trial][5] == practice_target:
        correct="True"
    else:
        correct="False"

    #結果の追加
    practice_result.append([ans,time,correct])

    #練習問題の解答を表示させるもの
    

    #実験に必要な変数の準備
    practice_trial+=1
    practice_animal_ans = df.iloc[practice_trial][5]
    practice_animal = df.iloc[practice_trial][4]
    return( render_template( "practice2.html", title="CocktailParty", name=name, trial=practice_trial, result=practice_result, animal=practice_animal, animal_ans=practice_animal_ans) )

#練習実験終了後結果
@app.route( "/practice_finish", methods=['POST'])
def practie_finish():
    global practice_trial,name,ans
    ans = request.form["face"]
    time = request.form["time"]

    #ターゲットと実際の回答をつなげて正解か不正解かを判定
    #ans_targetに実験者の回答を修正
    practice_target = connect_df[connect_df['ans'] == ans].iloc[0][0]
    df=pd.read_csv("subject/practice.csv", encoding='utf-8', header=None)
    if df.iloc[practice_trial][5] == practice_target:
        correct="True"
    else:
        correct="False"

    #結果の追加
    practice_result.append([ans,time,correct])

    return( render_template( "practice_finish.html", title="CocktailParty", name=name, trial=practice_trial, result=practice_result) )

#本番実験1回目
@app.route( "/experiment1")
def experiment1():
    global experiment_trial,name
    experiment_trial=0
    experiment_trial+=1
    df=pd.read_csv("subject/experiment/{}-cond.csv".format(name), encoding='utf-8', header=None)
    experiment_animal = df.iloc[experiment_trial][4]
    sound = df.iloc[experiment_trial][1]
    return( render_template( "experiment1.html", title="CocktailParty", name=name, trial=experiment_trial, animal=experiment_animal, sound=sound) )


#本番実験2回目~110回目
@app.route( "/experiment2", methods=['POST'])
def experiment2():
    global experiment_trial,name,ans

    #ansとtime（解答時間）のPOST
    ans = request.form["face"]
    time = request.form["time"]

    #ターゲットと実際の回答をつなげて正解か不正解かを判定
    #ans_targetに実験者の回答を修正
    experiment_target = connect_df[connect_df['ans'] == ans].iloc[0][0]

    #実験者の結果等を読み取り，正解不正解を判定
    df=pd.read_csv("subject/experiment/{}-cond.csv".format(name), encoding='utf-8', header=None)
    if df.iloc[experiment_trial][5] == experiment_target:
        correct="True"
    else:
        correct="False"

    time=datetime.strptime(time,'%M:%S.%f')

    total_seconds = timedelta(minutes=time.minute, seconds=time.second, milliseconds=time.microsecond/1000).total_seconds()


    #結果の追加
    experiment_result.append([experiment_trial, experiment_target,total_seconds,correct])

    #実験に必要な変数の準備
    experiment_trial+=1
    experiment_animal = df.iloc[experiment_trial][4]
    sound = df.iloc[experiment_trial][1]


    return( render_template( "experiment2.html", title="CocktailParty", name=name, trial=experiment_trial, result=experiment_result, animal=experiment_animal, sound=sound) )

#本番実験終了後結果
@app.route( "/experiment_finish", methods=['POST'])
def experiment_finish():
    global experiment_trial,name,ans
    ans = request.form["face"]
    time = request.form["time"]
    #ターゲットと実際の回答をつなげて正解か不正解かを判定
    #ans_targetに実験者の回答を修正
    experiment_target = connect_df[connect_df['ans'] == ans].iloc[0][0]

    #実験者の結果等を読み取り，正解不正解を判定
    df=pd.read_csv("subject/experiment/{}-cond.csv".format(name), encoding='utf-8', header=None)
    if df.iloc[experiment_trial][5] == experiment_target:
        correct="True"
    else:
        correct="False"

    time=datetime.strptime(time,'%M:%S.%f')

    total_seconds = timedelta(minutes=time.minute, seconds=time.second, milliseconds=time.microsecond/1000).total_seconds()



    #結果の追加
    experiment_result.append([experiment_trial, experiment_target ,total_seconds,correct])

    #結果の結合
    df=pd.read_csv("subject/experiment/{}-cond.csv".format(name), encoding='utf-8')    
    complete_df = pd.DataFrame(experiment_result, columns=['TrialNo','Answer','Time','correct'])
    df = pd.merge(df,complete_df, on='TrialNo', how='inner')

    df.to_csv("result/experiment/experiment_{}.csv".format(name),encoding='cp932',index=False)
    Filename = "result/experiment/experiment_{}.csv".format(name)
    Bucket = 'cocktailparty'
    Key = "result/experiment/experiment_{}.csv".format(name)
    client.upload_file(Filename, Bucket, Key)
    return( render_template( "experiment_finish.html", title="CocktailParty", name=name, trial=experiment_trial, result=experiment_result) )

#音声印象実験1回目
@app.route( "/quationnaire1")
def quationnaire1():
    global impression_trial,name
    impression_trial=0
    impression_trial+=1
    df=pd.read_csv("subject/impression/{}-Impcond.csv".format(name), encoding='utf-8', header=None)
    sound = df.iloc[impression_trial][1]
    return( render_template( "quationnaire1.html", title="CocktailParty", name=name, trial=impression_trial, sound=sound) )


#音声印象実験2回目~21回目
@app.route( "/quationnaire2", methods=['POST'])
def quationnaire2():
    global impression_trial,name,ans
    attractive = request.form["attractive"]
    imitate = request.form["imitate"]
    familiarity = request.form["familiarity"]
    confidence = request.form["confidence"]
    clear = request.form["clear"]
    impression_result.append([impression_trial, attractive,imitate,familiarity,confidence,clear])

    #次の実験の準備
    impression_trial+=1
    df=pd.read_csv("subject/impression/{}-Impcond.csv".format(name), encoding='utf-8', header=None)
    sound = df.iloc[impression_trial][1]
    return( render_template( "quationnaire2.html", title="CocktailParty", name=name, trial=impression_trial, sound=sound) )

@app.route( "/quationnaire_ex", methods=['POST'])
def quationnaire_ex():
    global name,ans,df,impression_trial
    attractive = request.form["attractive"]
    imitate = request.form["imitate"]
    familiarity = request.form["familiarity"]
    confidence = request.form["confidence"]
    clear = request.form["clear"]
    impression_result.append([impression_trial, attractive,imitate,familiarity,confidence,clear])

    #結果の結合
    df=pd.read_csv("subject/impression/{}-Impcond.csv".format(name), encoding='utf-8')    
    complete_df = pd.DataFrame(impression_result, columns=['TrialNo','声が魅力的に感じるか','自分の声だと感じるか','声に親しみを感じるか','自信がある声に感じるか','聞き取りやすい声か'])
    df = pd.merge(df,complete_df, on='TrialNo', how='inner')

    df.to_csv("result/impression/impression_{}.csv".format(name) ,encoding='cp932',index=False)
    Filename = "result/impression/impression_{}.csv".format(name)
    Bucket = 'cocktailparty'
    Key = "result/impression/impression_{}.csv".format(name)
    client.upload_file(Filename, Bucket, Key)
    return( render_template( "quationnaire_ex.html", title="CocktailParty", name=name) )


#音声印象実験終了後
@app.route( "/quationnaire_finish", methods=['POST'])
def quationnaire_finish():
    global name
    quationnaire1 = request.form["quationnaire1"]
    quationnaire2 = request.form["quationnaire2"]
    quationnaire3 = request.form["quationnaire3"]
    quationnaire_result.append([name,quationnaire1,quationnaire2,quationnaire3])
    df = pd.DataFrame(quationnaire_result,columns=['実験者','SNS投稿', '声の録音', '読書中の幻聴'])
    df.to_csv("result/quationnaire/quationnaire_{}.csv".format(name) ,encoding='cp932',index=False)
    Filename = "result/quationnaire/quationnaire_{}.csv".format(name)
    Bucket = 'cocktailparty'
    Key = "result/quationnaire/quationnaire_{}.csv".format(name)
    client.upload_file(Filename, Bucket, Key)
    return( render_template( "quationnaire_finish.html", title="CocktailParty", name=name, trial=impression_trial) )


@app.route("/integrated_voice/<path:filename>")
def play(filename):
    return send_from_directory("integrated_voice", filename)

# ==============================================================================
# ----- メイン・スクリプト -----
if __name__ == "__main__":
    # ----- Faskインスタンスで，Fask開発用wsgiサーバを起動する -----
    # -----    IPアドレス: 起動したPCのもの(外部からアクセス可能) -----
    # -----                もちろん，127.0.0.1(localhost)も使うことができる ----
    # -----    ポート番号: 80 (ポート番号指定は省略できる) -----
    # -----    デバッグ・モード: OFF -----
    # -----    同時プロセス/スレッド実行: OFF -----
    app.run(host='0.0.0.0', port=8080)
# ==============================================================================
