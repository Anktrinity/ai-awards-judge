from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from collections import defaultdict

from ai_awards_judge.models import Entry, JudgedEntry, ScoreBreakdown


POSITIVE_INNOVATION = ["ai", "novel", "innovative", "distinct", "searchable", "cluster", "intelligence"]
POSITIVE_EXECUTION = ["deployed", "pilot", "workflow", "integration", "check-in", "production", "enterprise"]
RESULT_SIGNALS = ["reduced", "increase", "improved", "renewal", "%", "roi", "satisfaction", "adoption"]
RISK_TERMS = ["early-stage", "portfolio-level", "not feature-isolated", "pilot", "limited"]


class LLMScoringError(RuntimeError):
    pass


def _count_keywords(text: str, keywords: list[str]) -> int:
    lowered = text.lower()
    return sum(1 for keyword in keywords if keyword in lowered)


def _count_metrics(text: str) -> int:
    return len(re.findall(r"\b\d+(?:\.\d+)?%?\b", text))


def _judge_id_from_env() -> str:
    return os.getenv("AI_AWARDS_JUDGE_ID", "heuristic")


def score_entry(entry: Entry) -> JudgedEntry:
    joined = "\n".join([entry.summary, *entry.evidence, entry.notes, entry.raw_text])
    innovation = min(95, 60 + _count_keywords(joined, POSITIVE_INNOVATION) * 5 + min(_count_metrics(joined), 4))
    impact = min(95, 58 + _count_metrics(joined) * 4 + _count_keywords(joined, RESULT_SIGNALS) * 3)
    execution = min(95, 60 + _count_keywords(joined, POSITIVE_EXECUTION) * 5 + len(entry.evidence) * 2)
    results = min(95, 52 + _count_metrics(joined) * 5 + _count_keywords(joined, RESULT_SIGNALS) * 4)

    risk_hits = _count_keywords(joined, RISK_TERMS)
    if risk_hits:
        results = max(45, results - risk_hits * 4)
        impact = max(50, impact - max(0, risk_hits - 1) * 2)

    strengths: list[str] = []
    concerns: list[str] = []

    if _count_metrics(joined) >= 3:
        strengths.append("Includes multiple concrete metrics or evidence points.")
    if "pilot" in joined.lower() or "deployed" in joined.lower():
        strengths.append("Shows evidence of real-world rollout or testing.")
    if entry.category and entry.category.lower() in joined.lower():
        strengths.append("Strong category alignment in the submission framing.")

    if "early-stage" in joined.lower():
        concerns.append("Entry appears early-stage, so long-term proof is still limited.")
    if "portfolio-level" in joined.lower() or "not feature-isolated" in joined.lower():
        concerns.append("Some evidence may be broader than the single feature being judged.")
    if len(entry.evidence) < 2:
        concerns.append("Thin evidence set, which lowers confidence.")

    total = innovation + impact + execution + results
    if total >= 340:
        verdict = "Strong finalist"
    elif total >= 300:
        verdict = "Competitive shortlist contender"
    elif total >= 260:
        verdict = "Promising, but under the leaders"
    else:
        verdict = "Needs stronger evidence or positioning"

    confidence = "high" if len(entry.evidence) >= 3 and _count_metrics(joined) >= 3 else "medium"
    if len(entry.evidence) < 2:
        confidence = "low"

    return JudgedEntry(
        entry=entry,
        scores=ScoreBreakdown(
            innovation=innovation,
            impact=impact,
            execution=execution,
            results=results,
        ),
        strengths=strengths or ["Relevant use case with some judging potential."],
        concerns=concerns or ["No major concern captured from the current heuristic pass."],
        verdict=verdict,
        confidence=confidence,
        concise_summary=entry.summary.strip() or f"{entry.product} submitted by {entry.entrant}.",
        evidence_cited=entry.evidence[:5],
        judge_id=_judge_id_from_env(),
        scoring_mode="heuristic",
    )


def _extract_json_object(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise LLMScoringError("Model response did not contain a JSON object")
    return json.loads(match.group(0))


def _llm_endpoint() -> tuple[str, str, str]:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("AI_AWARDS_JUDGE_API_KEY")
    model = os.getenv("AI_AWARDS_JUDGE_MODEL", "gpt-4o-mini")
    base_url = os.getenv("AI_AWARDS_JUDGE_BASE_URL", "https://api.openai.com/v1")
    if not api_key:
        raise LLMScoringError("OPENAI_API_KEY or AI_AWARDS_JUDGE_API_KEY is required for llm scoring")
    return api_key, model, base_url.rstrip("/")


def score_entry_with_llm(entry: Entry, rubric: dict, prompts: dict) -> JudgedEntry:
    api_key, model, base_url = _llm_endpoint()
    dimensions = rubric.get("scale", {}).get("dimensions", [])
    dimension_labels = ", ".join(f"{item['key']} (0-{item['max_score']})" for item in dimensions)
    system_prompt = prompts.get("system_prompt", "You are an expert awards judge.")
    user_prompt = (
        "Return one JSON object only with keys: concise_summary, evidence_cited, strengths, concerns, "
        "innovation_score, impact_score, execution_score, results_score, verdict, confidence.\n"
        f"Use this rubric: {json.dumps(rubric)}\n"
        f"Scores must match: {dimension_labels}.\n"
        "Evidence cited must quote or closely paraphrase concrete evidence from the submission.\n"
        f"Submission:\n{entry.raw_text}"
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise LLMScoringError(f"LLM scoring request failed: {exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise LLMScoringError(f"LLM scoring request failed: {exc}") from exc

    content = body["choices"][0]["message"]["content"]
    parsed = _extract_json_object(content)
    scores = ScoreBreakdown(
        innovation=int(parsed["innovation_score"]),
        impact=int(parsed["impact_score"]),
        execution=int(parsed["execution_score"]),
        results=int(parsed["results_score"]),
    )
    return JudgedEntry(
        entry=entry,
        scores=scores,
        strengths=list(parsed.get("strengths", [])) or ["No strengths returned by model."],
        concerns=list(parsed.get("concerns", [])) or ["No concerns returned by model."],
        verdict=parsed.get("verdict", "Unspecified verdict"),
        confidence=parsed.get("confidence", "medium"),
        concise_summary=parsed.get("concise_summary", entry.summary.strip()),
        evidence_cited=list(parsed.get("evidence_cited", []))[:8],
        judge_id=os.getenv("AI_AWARDS_JUDGE_ID", model),
        scoring_mode="llm",
    )


def score_entry_auto(entry: Entry, rubric: dict | None = None, prompts: dict | None = None, scoring_mode: str = "heuristic") -> JudgedEntry:
    if scoring_mode == "heuristic":
        return score_entry(entry)
    if scoring_mode == "llm":
        if rubric is None or prompts is None:
            raise LLMScoringError("rubric and prompts are required for llm scoring")
        return score_entry_with_llm(entry, rubric, prompts)
    if scoring_mode == "auto":
        if rubric is not None and prompts is not None:
            try:
                return score_entry_with_llm(entry, rubric, prompts)
            except LLMScoringError:
                pass
        return score_entry(entry)
    raise ValueError(f"Unsupported scoring mode: {scoring_mode}")


def rank_by_category(entries: list[JudgedEntry]) -> dict[str, list[JudgedEntry]]:
    grouped: dict[str, list[JudgedEntry]] = defaultdict(list)
    for entry in entries:
        grouped[entry.entry.category].append(entry)
    for category, items in grouped.items():
        grouped[category] = sorted(items, key=lambda item: item.scores.total, reverse=True)
    return dict(grouped)
