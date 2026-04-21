from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Entry:
    path: str
    category: str
    entrant: str
    company: str
    product: str
    summary: str
    evidence: list[str]
    notes: str
    raw_text: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ScoreBreakdown:
    innovation: int
    impact: int
    execution: int
    results: int

    @property
    def total(self) -> int:
        return self.innovation + self.impact + self.execution + self.results

    def to_dict(self) -> dict:
        data = asdict(self)
        data["total"] = self.total
        return data


@dataclass
class JudgedEntry:
    entry: Entry
    scores: ScoreBreakdown
    strengths: list[str]
    concerns: list[str]
    verdict: str
    confidence: str

    def to_dict(self) -> dict:
        return {
            "entry": self.entry.to_dict(),
            "scores": self.scores.to_dict(),
            "strengths": self.strengths,
            "concerns": self.concerns,
            "verdict": self.verdict,
            "confidence": self.confidence,
        }
