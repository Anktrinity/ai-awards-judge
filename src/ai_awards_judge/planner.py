from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json


@dataclass
class RunManifest:
    input_dir: str
    output_dir: str
    discovered_files: list[str]
    status: str = "planned"

    def to_dict(self) -> dict:
        return asdict(self)


def build_manifest(input_dir: Path, output_dir: Path) -> RunManifest:
    discovered = sorted(
        str(path.relative_to(input_dir))
        for path in input_dir.rglob("*")
        if path.is_file()
    )
    return RunManifest(
        input_dir=str(input_dir),
        output_dir=str(output_dir),
        discovered_files=discovered,
    )


def write_manifest(manifest: RunManifest, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest.to_dict(), indent=2), encoding="utf-8")
