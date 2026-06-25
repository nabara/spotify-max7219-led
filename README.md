[README.md](https://github.com/user-attachments/files/29341085/README.md)
# spotify-max7219-led

Raspberry Pi 上で、Spotify で再生中の曲名（アーティスト名 - 曲名）を
MAX7219 LED マトリクスにスクロール表示する小さな仕組みです。

15 秒ごとに「いま再生中の曲」を取得し、4 枚カスケード接続した MAX7219 の
LED マトリクスに流します。再生していないときは空白を表示します。

> Display the currently playing Spotify track on a chain of MAX7219 LED
> matrices, driven by a Raspberry Pi.

---

## 仕組み (How it works)

```
nowplaying.sh   ← メインループ（15秒ごとに実行）
   ├─ nowplaying.py    … Spotify API で再生中の曲名を取得して標準出力
   └─ view_message.py  … 受け取った文字列を MAX7219 LED にスクロール表示
```

- `nowplaying.py` … 再生中の曲を取得し `アーティスト名 - 曲名` を print する
- `view_message.py` … luma.led_matrix で MAX7219 に文字をスクロール表示する
- `toptrack.py` … （おまけ）指定アーティストのトップ 10 曲を取得して表示する

---

## 必要なもの (Hardware)

- Raspberry Pi（Raspberry Pi OS。Pi 3 / 4 など）
- MAX7219 LED ドットマトリクスモジュール ×4（カスケード接続）
- Spotify アカウント（再生状態を取得するため）

### 配線 (Wiring)

MAX7219 は SPI 接続です。Raspberry Pi の SPI ピンに接続してください。

| MAX7219 | Raspberry Pi (BCM) |
|---------|--------------------|
| VCC     | 5V                 |
| GND     | GND                |
| DIN     | GPIO10 (MOSI)      |
| CS      | GPIO8  (CE0)       |
| CLK     | GPIO11 (SCLK)      |

---

## セットアップ (Setup)

### 1. SPI を有効化

```bash
sudo raspi-config nonint do_spi 0
```

### 2. 必要なライブラリをインストール

```bash
sudo apt update
sudo apt install -y python3-pip libopenjp2-7
sudo pip3 install spotipy luma.led_matrix --break-system-packages
```

### 3. Spotify API のキーを設定

1. https://developer.spotify.com/dashboard でアプリを作成
2. Client ID と Client Secret を取得
3. Redirect URI に `http://localhost:8888/callback` を登録
4. `nowplaying.py`（と必要なら `toptrack.py`）の以下を自分の値に書き換える

```python
username  = 'YOUR_SPOTIFY_USERNAME'
my_id     = 'YOUR_CLIENT_ID'
my_secret = 'YOUR_CLIENT_SECRET'
```

### 4. LED 単体テスト

```bash
sudo python3 view_message.py -t "HELLO"
```

「HELLO」が流れれば配線・ライブラリ OK です。

> ⚠️ 表示の向きがおかしい場合は `view_message.py` の `--block-orientation`
> （0 / 90 / -90）や `--rotate`、`--cascaded`（枚数）を調整してください。

### 5. 全体テスト

Spotify で何か再生した状態で:

```bash
bash nowplaying.sh
```

曲名が流れれば成功です。`Ctrl + C` で停止します。

---

## 自動起動 (Auto-start on boot)

電源を入れたら自動で動かすには、cron に登録します。

```bash
crontab -e
```

末尾に以下を 1 行追加（パスは自分の環境に合わせてください）:

```
@reboot sleep 30 && /bin/bash /home/USERNAME/spotify-max7219-led/nowplaying.sh
```

`sleep 30` は Wi-Fi 接続が完了するのを待つためのものです。

---

## 注意 (Security note)

- API キー（Client Secret）は **絶対にコミットしないでください**。
- `.gitignore` で `.cache*`（Spotify 認証トークンのキャッシュ）を除外しています。
  これらにはアクセストークンが含まれるため、公開リポジトリに含めないでください。

---

## ライセンス (License)

MIT License. 詳細は [LICENSE](LICENSE) を参照。

`view_message.py` は Thomas Wenzlaff 氏による luma.led_matrix の
サンプルコードをベースにしています。

---

## 作者 (Author)

shuji nabara
