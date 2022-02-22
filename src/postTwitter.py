import json
import sys
import glob
import re
import os
from requests_oauthlib import OAuth1Session
import markovify
import genJapanese


current = os.path.dirname(__file__)
##ディレクトリのパス
splitdirPath = current + '/split_text'
textdirPath = current + '/texts'
##

##ファイルのパス
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

textModel = markovify.NewlineText(splitText, state_size=2)

for i in range(10):
    generated = textModel.make_sentence()
    if generated:
        generated = re.sub(' ','' , generated)
        break

if generated is None:
    print("エラー:文章生成に失敗")
    sys.exit()

data = {"text": generated}


keysPath = current + '/keys.json'
with open(keysPath) as keys_json:
    keys_dict = json.load(keys_json)
    consumerKey = keys_dict['consumerKey']
    consumerSecret = keys_dict['consumerSecret']
    accessToken = keys_dict['accessToken']
    accessSecret = keys_dict['accessSecret']

endpoint = 'https://api.twitter.com/2/tweets'

twitter = OAuth1Session(consumerKey, consumerSecret, accessToken, accessSecret)
res = twitter.post(endpoint, json=data)

print(res.status_code)
