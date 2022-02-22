# tweetByMarkov
テキストファイルのデータを読み込んでmecabによる形態素への分割とmarkovifyによるマルコフ連鎖モデル、文章の生成を行い、ツイートする。  

# 元となるテキスト
`src/texts/`配下に元となるテキストファイルを配置する。  
初回実行時にはそれらのファイルをまとめmarkovifyで扱えるようにしたものが`src/split_text/data.txt`として出力される。  
以後は`src/texts/`配下のファイルではなく`data.txt`を読み込んでツイートするようになる。  
元となるデータを更新したい場合には、`data.txt`を削除してプログラムを実行することでテキストファイルからの再生成を行う。 

# 認証
twitter apiへはOauth1.0aで認証を行う。  
その際、アクセストークン等は以下の形式のsrc/keys.jsonから読み込む。  
  
**keys.json**
```json:keys.json
{
    "consumerKey" : "XXXXXXXXXXX",
    "consumerSecret" : "XXXXXXXXXXX",
    "accessToken" : "XXXXX-XXXXXX",
    "accessSecret" : "XXXXXXXXXXX"
}
```

