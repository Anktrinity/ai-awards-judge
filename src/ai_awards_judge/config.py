from __future__ import annotations

from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_all_config() -> dict:
    return {
        "rubric": load_yaml(CONFIG_DIR / "rubric.yaml"),
        "categories": load_yaml(CONFIG_DIR / "categories.yaml"),
        "prompts": load_yaml(CONFIG_DIR / "prompts.yaml"),
        "outputs": load_yaml(CONFIG_DIR / "output_templates.yaml"),
    }
