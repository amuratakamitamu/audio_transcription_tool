from __future__ import annotations

import argparse
import sys
from pathlib import Path

from config import (
    DEFAULT_COMPUTE_TYPE,
    DEFAULT_DEVICE,
    DEFAULT_LANGUAGE,
    DEFAULT_MODEL,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_OUTPUT_FORMAT,
)
from exporters import export_json, export_srt, export_txt
from transcriber import Transcriber


SUPPORTED_FORMATS = {"txt", "srt", "json"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audio/video transcription tool")
    parser.add_argument("input_path", help="Path to an input audio/video file")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--format", default=DEFAULT_OUTPUT_FORMAT, help="txt / srt / json")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Whisper model name")
    parser.add_argument("--language", default=DEFAULT_LANGUAGE, help="Language code")
    parser.add_argument("--device", default=DEFAULT_DEVICE, help="cpu / cuda")
    parser.add_argument("--compute-type", default=DEFAULT_COMPUTE_TYPE, dest="compute_type", help="int8 / float16 / float32")
    return parser


def default_output_path(input_path: Path, output_format: str) -> Path:
    return Path(DEFAULT_OUTPUT_DIR) / f"{input_path.stem}.{output_format}"


def export_segments(segments: list[dict], output_path: Path, output_format: str) -> None:
    if output_format == "txt":
        export_txt(segments, output_path)
    elif output_format == "srt":
        export_srt(segments, output_path)
    elif output_format == "json":
        export_json(segments, output_path)
    else:
        raise ValueError("unsupported output format")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_path = Path(args.input_path)
    if not input_path.exists():
        print("Error: input file not found.", file=sys.stderr)
        return 1

    output_format = str(args.format).lower()
    if output_format not in SUPPORTED_FORMATS:
        print("Error: unsupported output format.", file=sys.stderr)
        return 1

    output_path = Path(args.output) if args.output else default_output_path(input_path, output_format)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        transcriber = Transcriber(
            model_name=args.model,
            device=args.device,
            compute_type=args.compute_type,
        )
        segments = transcriber.transcribe(input_path, language=args.language)
    except Exception:
        print("Error: transcription failed.", file=sys.stderr)
        return 1

    try:
        export_segments(segments, output_path, output_format)
    except Exception:
        print("Error: failed to write output file.", file=sys.stderr)
        return 1

    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

