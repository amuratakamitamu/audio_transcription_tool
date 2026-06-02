from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def format_srt_timestamp(seconds: float) -> str:
    total_milliseconds = int(round(seconds * 1000))
    hours, remainder = divmod(total_milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, milliseconds = divmod(remainder, 1_000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def export_txt(segments: list[dict[str, Any]], output_path: str | Path) -> None:
    lines = [f"[{segment['start']:.2f} - {segment['end']:.2f}] {segment['text']}" for segment in segments]
    Path(output_path).write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def export_srt(segments: list[dict[str, Any]], output_path: str | Path) -> None:
    blocks: list[str] = []
    for index, segment in enumerate(segments, start=1):
        blocks.append(
            "\n".join(
                [
                    str(index),
                    f"{format_srt_timestamp(segment['start'])} --> {format_srt_timestamp(segment['end'])}",
                    segment["text"],
                ]
            )
        )
    Path(output_path).write_text("\n\n".join(blocks) + ("\n" if blocks else ""), encoding="utf-8")


def export_json(segments: list[dict[str, Any]], output_path: str | Path) -> None:
    Path(output_path).write_text(json.dumps(segments, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

