from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TranscriptionSegment:
    start: float
    end: float
    text: str

    def to_dict(self) -> dict[str, Any]:
        return {"start": self.start, "end": self.end, "text": self.text}


class Transcriber:
    def __init__(self, model_name: str, device: str, compute_type: str) -> None:
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:  # pragma: no cover - depends on environment
            raise RuntimeError("faster-whisper is not installed") from exc

        self.model = WhisperModel(model_name, device=device, compute_type=compute_type)

    def transcribe(self, input_path: str | Path, language: str = "ja") -> list[dict[str, Any]]:
        segments, _info = self.model.transcribe(str(input_path), language=language)
        results: list[dict[str, Any]] = []
        for segment in segments:
            results.append(
                TranscriptionSegment(
                    start=float(segment.start),
                    end=float(segment.end),
                    text=str(segment.text).strip(),
                ).to_dict()
            )
        return results
