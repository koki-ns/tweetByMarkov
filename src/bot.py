from concurrent.futures import thread
import json
import sys
import glob
import re
import os
import threading
import time
import schedule
import requests
from requests_oauthlib import OAuth1Session
import markovify
import genJapanese

##ベアラートークンの認証はヘッダーに、ルールはjsonで追加？

def postTweet(text, reply=None):
    data = {}
    data['text'] = text

    if reply:
        data['reply'] = { "in_reply_to_tweet_id": str(reply) }

    twitter = OAuth1Session(consumerKey, consumerSecret, accessToken, accessSecret)
    res = twitter.post(postTweetPoint, json=data)
    return res

def autoReply():
    res3 = requests.get(getStreamPoint, headers=bearerHeader, stream=True)
    print(res3.status_code)
    #print(res3.text)
    if res3.status_code == 200:
        print('自動返信を開始')
        for response_line in res3.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                target = json_response['data']['id']
            
                #リプライを生成
                for i in range(10):
                    generated = textModel.make_sentence()
                    if generated:
                        generated = re.sub(' ','' , generated)
                        break

                if generated is None:
                    print("エラー:文章生成に失敗")
                    continue

                res = postTweet(generated, target)
                print('autoReply:' + str(res.status_code) + '\n' + str(res.text))

def postGenerated():
    for i in range(10):
        generated = textModel.make_sentence()
        if generated:
            generated = re.sub(' ','' , generated)
            break

    if generated is None:
        print("エラー:文章生成に失敗")
    else:
        res = postTweet(generated)
        print('Tweeted:' + str(res.status_code) + '\n' + str(res.text))


def tweetRegularly():
    while True:
        schedule.run_pending()
        time.sleep(1)


##########
current = os.path.dirname(__file__)

keysPath = current + '/keys.json'
with open(keysPath) as keys_json:
    keys_dict = json.load(keys_json)
    consumerKey = keys_dict['consumerKey']
    consumerSecret = keys_dict['consumerSecret']
    accessToken = keys_dict['accessToken']
    accessSecret = keys_dict['accessSecret']
    bearerToken = keys_dict['BearerToken']

postRulesPoint = 'https://api.twitter.com/2/tweets/search/stream/rules'
getRulesPoint = 'https://api.twitter.com/2/tweets/search/stream/rules'
getStreamPoint = 'https://api.twitter.com/2/tweets/search/stream'
postTweetPoint = 'https://api.twitter.com/2/tweets'

rules = { 'add' : [
    {'value' : 'to:_____alterego_', 'tag' : 'replys'},
]}

bearerHeader = {
    'Authorization': 'Bearer ' + bearerToken
}


#############################ここからテキストモデル生成用#############################
##文章生成用ディレクトリのパス
splitdirPath = current + '/split_text'
textdirPath = current + '/texts'
##

##ファイル本体のパス
splitPath = current + '/split_text/data.txt'
paths = current + '/texts/*.txt'
##

if not os.path.isdir(splitdirPath):
    os.mkdir(splitdirPath)

if not os.path.isdir(textdirPath):
    os.mkdir(textdirPath)

if os.path.isfile(splitPath):
    with open(splitPath) as f:
        splitText = f.read()
else:
    textList = glob.glob(paths)
    if not bool(textList):
        print("エラー:テキストファイルが存在しません")
        sys.exit()
    texts = genJapanese.loadFiles(textList)
    splitText = genJapanese.splitForMarkov(texts)
    with open(splitPath, mode='w') as f:
        f.write(splitText)

##テキストモデル生成完了
textModel = markovify.NewlineText(splitText, state_size=2)
#################################################################################


#############################ここからルール設定用#############################
res1 = requests.post(postRulesPoint, headers=bearerHeader, json=rules)
print(res1.status_code)
print(res1.text)
if res1.status_code != 201:
    print('エラー:ルール設定に失敗')
    sys.exit()
else:
    print('ルール設定に成功')

res2 = requests.get(getRulesPoint, headers=bearerHeader)
print(res2.status_code)
print(res2.text)
if res2.status_code != 200:
    print('エラー:ルール取得に失敗')
    sys.exit()
else:
    print('ルール取得に成功')
###########################################################################

schedule.every().day.at("00:00").do(postGenerated)
schedule.every().day.at("06:00").do(postGenerated)
schedule.every().day.at("12:00").do(postGenerated)
schedule.every().day.at("18:00").do(postGenerated)

thread1 = threading.Thread(target=autoReply)
thread2 = threading.Thread(target=tweetRegularly)

thread1.start()
thread2.start()

