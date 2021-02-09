# octoprint_api

OctoPrint REST API の薄い Python ラッパーです。

<br/>

# 動作確認環境

- Raspberry Pi 3 Model B
- Raspbian GNU/Linux 9.9 (stretch)
- OctoPrint Version 1.3.9
- Python 3.5.3

<br/>

# OctoPrint の REST API キー取得

ブラウザでラズパイにインストールした OctoPrint にアクセス

[Settings] (画面右上の方のスパナアイコン) をクリック

[API] をクリックすると API キーが表示されるのでコピーしてローカルでファイルに保存
(ファイル名は任意)

<br/>

# Python で Octoprint の API にアクセス

OctoPrint をインストールしたラズパイは USB ケーブルで 3D プリンターに接続した状態で始めてます

<br/>

## OctoPrint クラスをインポート

```
>>> from octoprint_api import OctoPrint
```

<br/>

## OctoPrint オブジェクト作成

ダウンロードした API キーファイルの指定は必須です。必要に応じて OctoPrint をインストールしたラズパイの
IP アドレスとポート番号も指定します。

- OctoPrint をインストールしたラズパイの IP アドレスとポート番号を指定する場合

  ```
  >>> op = OctoPrint('/some/where/octop_apikey', '192.168.0.1', 5012)
  ```

- ポート番号が標準の 5000番の場合は省略が可能

  ```
  >>> op = OctoPrint('/some/where/octop_apikey', '192.168.0.1')
  ```

- OctoPrint をインストールしたラズパイの Python で OctoPrint API (localhost の 5000番ポート) にアクセスする場合

  ```
  >>> op = OctoPrint('/some/where/octop_apikey')
  ```

<br/>

## OctoPrint を 3D プリンターに接続

```
>>> op.connect_w()
```

<br/>

## 基本的な API へのアクセス方法

[[OctoPrint の REST API ドキュメント](https://docs.octoprint.org/en/master/api/)] に API の説明があります。

例えば、ベッドの状態取得は `GET /api/printer/bed` なので以下のように get() すると現在の温度が 22.5℃ であることがわかります。

```
>>> op.get('/api/printer/bed')
{'bed': {'actual': 22.5, 'offset': 0, 'target': 0.0}}
```

3D プリンターに G Code を送る場合は `POST /api/printer/command` なので例えば Auto Home (G28) の場合は以下の通りです。

```
>>> op.post('/api/printer/command', command='G28')
```

<br/>

## 3D プリンターのヘッドを移動

ヘッドの移動は `POST /api/printer/printhead` で x, y, z を mm 単位で指定しますが、マイクロメートル単位で指定できるように jog() メソッドを用意しています。

3D プリンターの絶対座標で z=20000 (20mm) に移動

```
op.jog(z=20000)
```

3D プリンターの絶対座標で x=30000 (30mm)、y=50000 (50mm) に移動

```
op.jog(x=30000, y=50000)
```

ヘッドの現在位置からの相対位置で指定する場合は absolute=False とします

```
op.jog(x=10000, y=40000, absolute=False)
```

<br/>

## OctoPrint を 3D プリンターから切断

```
>>> op.disconnect_w()
```
