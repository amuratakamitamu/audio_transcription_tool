# audio_transcription_tool

音声ファイルや動画ファイルから日本語音声を文字起こしし、`txt` / `srt` / `json` 形式で保存するローカル実行型CLIツールです。

## 必要環境

- Python 3.10以上
- `ffmpeg`
- `faster-whisper`

## セットアップ

```bash
pip install -r requirements.txt
```

`ffmpeg` はOS側でインストールしてください。

## 使い方

基本実行:

```bash
python main.py input.mp3
```

出力形式を指定:

```bash
python main.py input.mp3 --format srt
python main.py input.mp4 --format json
```

出力ファイルを指定:

```bash
python main.py input.mp3 --format srt --output subtitle.srt
```

モデルや実行環境を指定:

```bash
python main.py input.mp3 --model medium --language ja --device cpu --compute-type int8
```

## オプション

- `--output`: 出力ファイルパス
- `--format`: `txt` / `srt` / `json`
- `--model`: `tiny` / `base` / `small` / `medium` / `large-v3`
- `--language`: 言語コード。初期値は `ja`
- `--device`: `cpu` / `cuda`
- `--compute-type`: `int8` / `float16` / `float32`

## 出力例

`txt`:

```text
[0.00 - 3.20] こんにちは。
```

`srt`:

```text
1
00:00:00,000 --> 00:00:03,200
こんにちは。
```

`json`:

```json
[
  {
    "start": 0.0,
    "end": 3.2,
    "text": "こんにちは。"
  }
]
```

## エラー

- `Error: input file not found.`
- `Error: unsupported output format.`
- `Error: transcription failed.`
- `Error: failed to write output file.`
