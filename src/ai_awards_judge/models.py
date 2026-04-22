from __future__ import annotations

from dataclasses import asdict, dataclass, field


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
    concise_summary: str = ""
    evidence_cited: list[str] = field(default_factory=list)
    judge_id: str = "heuristic"
    scoring_mode: str = "heuristic"

    @property
    def entry_key(self) -> str:
        return " | ".join(
            [
                self.entry.category.strip(),
                self.entry.entrant.strip(),
                self.entry.company.strip(),
                self.entry.product.strip(),
            ]
        )

    def to_dict(self) -> dict:
        return {
            "entry": self.entry.to_dict(),
            "scores": self.scores.to_dict(),
            "strengths": self.strengths,
            "concerns": self.concerns,
            "verdict": self.verdict,
            "confidence": self.confidence,
            "concise_summary": self.concise_summary,
            "evidence_cited": self.evidence_cited,
            "judge_id": self.judge_id,
            "scoring_mode": self.scoring_mode,
            "entry_key": self.entry_key,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "JudgedEntry":
        entry_data = data["entry"]
        score_data = data["scores"]
        score_data = {key: value for key, value in score_data.items() if key != "total"}
        return cls(
            entry=Entry(**entry_data),
            scores=ScoreBreakdown(**score_data),
            strengths=list(data.get("strengths", [])),
            concerns=list(data.get("concerns", [])),
            verdict=data.get("verdict", ""),
            confidence=data.get("confidence", "medium"),
            concise_summary=data.get("concise_summary", ""),
            evidence_cited=list(data.get("evidence_cited", [])),
            judge_id=data.get("judge_id", "unknown"),
            scoring_mode=data.get("scoring_mode", "heuristic"),
        )


@dataclass
class ReconciledEntry:
    entry_key: str
    category: str
    entrant: str
    company: str
    product: str
    judge_count: int
    scores: ScoreBreakdown
    judge_ids: list[str]
    verdict: str
    confidence: str
    summary: str
    evidence_cited: list[str]
    strengths: list[str]
    concerns: list[str]
    score_range: int = 0
    disagreement_level: str = "low"
    verdict_counts: dict[str, int] = field(default_factory=dict)
    confidence_counts: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["scores"] = self.scores.to_dict()
        return data
