# 音声文字起こしツール 要件定義書・実装手順書

## 1. 目的

音声ファイルまたは動画ファイルから日本語音声を文字起こしし、テキスト・字幕ファイルとして保存できるローカル実行型ツールを作成する。

主な目的は以下の通り。

* 音声・動画ファイルの文字起こし
* 日本語音声への対応
* ローカル環境での実行
* `txt` / `srt` / `json` 形式での出力
* 将来的なGUI化・バッチ処理への拡張

## 2. 使用技術

### 必須

* Python 3.10 以上
* faster-whisper
* ffmpeg

### 推奨ライブラリ

```bash
pip install faster-whisper
```

`ffmpeg` はOS側にインストールする。

Ubuntuの場合：

```bash
sudo apt install ffmpeg
```

## 3. 対象ファイル形式

入力ファイルは `ffmpeg` が読み込める形式を対象とする。

例：

* `.mp3`
* `.wav`
* `.m4a`
* `.mp4`
* `.mov`
* `.webm`

## 4. 基本要件

### 4.1 入力

ユーザーはCLIから以下を指定できること。

```bash
python main.py input.mp3
```

追加オプションとして以下を指定できること。

```bash
python main.py input.mp3 --model small --format srt --output output.srt
```

### 4.2 出力形式

以下の出力形式に対応する。

#### txt

読みやすい通常テキスト。

例：

```text
[0.00 - 3.20] こんにちは。
[3.20 - 8.50] 今日は音声認識のテストをします。
```

#### srt

字幕ファイル形式。

例：

```text
1
00:00:00,000 --> 00:00:03,200
こんにちは。

2
00:00:03,200 --> 00:00:08,500
今日は音声認識のテストをします。
```

#### json

後処理しやすい構造化形式。

例：

```json
[
  {
    "start": 0.0,
    "end": 3.2,
    "text": "こんにちは。"
  }
]
```

## 5. 非機能要件

### 5.1 実行環境

* CPUのみで動作すること
* GPU環境がある場合はGPU利用も選択可能にすること
* Windows / macOS / Linux で動作可能な構成にすること

### 5.2 モデル

初期値は `small` とする。

対応モデル：

* `tiny`
* `base`
* `small`
* `medium`
* `large-v3`

推奨設定：

| 用途          | モデル     |
| ------------- | ---------- |
| 動作確認      | `tiny`     |
| 軽量運用      | `base`     |
| 通常利用      | `small`    |
| 精度重視      | `medium`   |
| GPUあり高精度 | `large-v3` |

### 5.3 言語

初期値は日本語とする。

```python
language="ja"
```

ただし、将来的に他言語へ拡張できるよう、CLIオプションで変更可能にする。

## 6. ディレクトリ構成

以下の構成で実装する。

```text
transcription_tool/
├── main.py
├── transcriber.py
├── exporters.py
├── config.py
├── requirements.txt
├── README.md
└── output/
```

### 各ファイルの役割

| ファイル           | 役割                               |
| ------------------ | ---------------------------------- |
| `main.py`          | CLI引数処理・全体制御              |
| `transcriber.py`   | faster-whisperによる文字起こし処理 |
| `exporters.py`     | txt / srt / json 出力処理          |
| `config.py`        | デフォルト設定                     |
| `requirements.txt` | Python依存関係                     |
| `README.md`        | 使い方説明                         |
| `output/`          | 出力先                             |

## 7. 実装仕様

### 7.1 `config.py`

デフォルト設定を定義する。

```python
DEFAULT_MODEL = "small"
DEFAULT_LANGUAGE = "ja"
DEFAULT_DEVICE = "cpu"
DEFAULT_COMPUTE_TYPE = "int8"
DEFAULT_OUTPUT_FORMAT = "txt"
```

### 7.2 `transcriber.py`

`Transcriber` クラスを作成する。

要件：

* 初期化時にモデルを読み込む
* `transcribe()` メソッドで音声ファイルを文字起こしする
* セグメント情報をリスト化して返す

返却形式の例：

```python
[
    {
        "start": 0.0,
        "end": 3.2,
        "text": "こんにちは。"
    }
]
```

### 7.3 `exporters.py`

以下の関数を実装する。

```python
export_txt(segments, output_path)
export_srt(segments, output_path)
export_json(segments, output_path)
```

また、SRT用に秒数を字幕時刻形式へ変換する関数を実装する。

```python
format_srt_timestamp(seconds)
```

### 7.4 `main.py`

CLI引数を受け取る。

必須引数：

```bash
input_path
```

任意引数：

```bash
--output
--format
--model
--language
--device
--compute-type
```

実行例：

```bash
python main.py input.mp3 --format txt
python main.py input.mp3 --format srt --output subtitle.srt
python main.py input.mp4 --model medium --format json
```

## 8. CLI仕様

### 基本コマンド

```bash
python main.py <input_path>
```

### オプション

| オプション       | 初期値   | 説明                           |
| ---------------- | -------- | ------------------------------ |
| `--output`       | 自動生成 | 出力ファイル名                 |
| `--format`       | `txt`    | `txt` / `srt` / `json`         |
| `--model`        | `small`  | Whisperモデル                  |
| `--language`     | `ja`     | 音声言語                       |
| `--device`       | `cpu`    | `cpu` / `cuda`                 |
| `--compute-type` | `int8`   | `int8` / `float16` / `float32` |

## 9. エラー処理

以下のエラーを処理すること。

### 入力ファイルが存在しない

```text
Error: input file not found.
```

### 未対応の出力形式

```text
Error: unsupported output format.
```

### 文字起こし失敗

```text
Error: transcription failed.
```

### 出力ファイル書き込み失敗

```text
Error: failed to write output file.
```

## 10. 実装手順

### Step 1: プロジェクト作成

```bash
mkdir transcription_tool
cd transcription_tool
mkdir output
touch main.py transcriber.py exporters.py config.py requirements.txt README.md
```

### Step 2: 依存関係追加

`requirements.txt` に以下を記述する。

```text
faster-whisper
```

インストール：

```bash
pip install -r requirements.txt
```

### Step 3: `config.py` 作成

デフォルト設定を実装する。

### Step 4: `transcriber.py` 作成

`faster_whisper.WhisperModel` を使って文字起こし処理を実装する。

### Step 5: `exporters.py` 作成

`txt` / `srt` / `json` 出力を実装する。

### Step 6: `main.py` 作成

`argparse` でCLI引数を処理し、文字起こしから保存までを実行する。

### Step 7: 動作確認

```bash
python main.py sample.mp3
python main.py sample.mp3 --format srt
python main.py sample.mp3 --format json
```

## 11. 完了条件

以下を満たしたら完了とする。

* 音声ファイルを入力できる
* 日本語文字起こしができる
* `txt` 形式で保存できる
* `srt` 形式で保存できる
* `json` 形式で保存できる
* 入力ファイルがない場合にエラーを出せる
* READMEに使い方が書かれている

## 12. 優先度

### 必須

* CLI実行
* 日本語文字起こし
* `txt` 出力
* `srt` 出力
* `json` 出力
* エラー処理

### 後回し

* GUI
* 話者分離
* 複数ファイル一括処理
* Webアプリ化
* 文字起こし結果の編集画面
* 自動句読点補正
* 要約機能

## 13. 注意点

* 最初からGUIを作らないこと
* まずCLIで安定動作させること
* 文字起こし処理と出力処理を分離すること
* `main.py` に処理を書きすぎないこと
* 将来的なGUI化を考え、`Transcriber` クラスを再利用しやすくすること
