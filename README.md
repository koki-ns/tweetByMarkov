# tweetByMarkov
テキストファイルのデータを読み込んでmecabによる形態素への分割とmarkovifyによるマルコフ連鎖モデル、文章の生成を行い、自動ツイート及び自動返信をする。  

**Twitter APIの有料化に伴い、現在使用不可**

### 元となるテキスト
`src/texts/`配下に元となるテキストファイルを配置する。  
初回実行時にはそれらのファイルをまとめmarkovifyで扱えるようにしたものが`src/split_text/data.txt`として出力される。  
以後は`src/texts/`配下のファイルではなく`data.txt`を読み込んでツイートするようになる。  
元となるデータを更新したい場合には、`data.txt`を削除してプログラムを実行することでテキストファイルからの再生成を行う。 
  
  
### 認証
twitter apiへはOauth1.0aで認証を行う。  
その際、アクセストークン等は以下の形式の`src/keys.json`から読み込む。  
  
**keys.json**
```json:keys.json
{
    "consumerKey" : "XXXXXXXXXXX",
    "consumerSecret" : "XXXXXXXXXXX",
    "accessToken" : "XXXXX-XXXXXX",
    "accessSecret" : "XXXXXXXXXXX",
    "BearerToken" : "XXXXXXXXXXX"
}
```

