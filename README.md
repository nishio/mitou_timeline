# 未踏タイムライン

未踏ソフトウェア創造事業関係の話題を追い駆けたい時に、Twitterで「未踏」を検索しても、コロプラとか自然冷媒エアコンとか書籍や劇団がヒットして困るので、それらをフィルタリングする。

## 単なるユーザ向け解説
- crawl.py 未踏 OR #mitou OR #mitoh で検索して取れるだけすべて（7日分）のツイートを収集しファイルに書きだす
- filter.py 7日間のデータをフィルタリングしてoutput.htmlを出力する
- secret.py TwitterのAPIトークンなどを入れる。これはリポジトリに入っていないのでユーザ各自が作る。

```python
consumer_key='7FZ4...YHTb'
consumer_secret='kIoK...xKqR'
access_token_key='3520...qoa0'
access_token_secret='1dVl...ycD1'
```

## 実装に興味があるユーザ向け解説

- features.py: 機械学習の前段階としての手書きルール
- filter.py: ロジスティック回帰の前段として手書きルールを元に解析を行う
 - find_neutral: 手書きルールがヒットしなかったデータを出力する
 - sort_with_score: 手書きルールでスコア付けして並べることで「判定が困難なデータ」を洗い出す
- lr.py: ロジスティック回帰の実装。特徴ベクトルの作成など。 
 -  make_feature_matrix: 特徴ベクトルの作成、今は手書きルールの判定結果を特徴ベクトルにしている
 -  learn: 学習
 -  feature_compression: L1正則化を掛けて特徴の圧縮を行う。将来的には有用な特徴だけ抜き出してモデルを小さくし、LRによる判定をJS上でやったりする。

## raw_20160126*.txt

中高生向け未踏説明会後のクロール結果。text, ユーザ名、IDに加えてRT数、Fav数、RTしたツイートのID(なければ0)、が付け加えられている。
この期間、nishioがまめにRTしたので、RTされてるものを正例として使える。


## 今後の予定

今は手元でスクリプトを実行して1週間分のフィルタ結果が得られる仕組みだが、APIトークンを取得したりとかしないでも特定のURLに行くとそこでみられるって形にしたいな。
