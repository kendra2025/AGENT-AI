"""CLI for MetaNewsX."""

from __future__ import annotations

import re
import textwrap
from typing import Iterable

import click


DECISION_GRADE_BRIEF = """
Decision-Grade Brief
====================

Topic: Accelerating Community AI Literacy Programs

Key Signal
- Public library systems adopting AI training cohorts have doubled attendance
  in the last 12 months across three pilot cities.

Why It Matters
- Upskilling residents improves employability and reduces local talent gaps.
- Libraries can become trusted distribution hubs for responsible AI guidance.

Risks & Watchouts
- Inconsistent funding cycles may disrupt instructor continuity.
- Programs must align with data privacy expectations for public institutions.

Recommended Actions (Next 30 Days)
1) Identify two library partners with existing digital literacy classes.
2) Secure a sponsor for an eight-week pilot cohort.
3) Publish a transparent syllabus and outcomes dashboard.
"""


def _split_sentences(text: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text.strip())
    if not cleaned:
        return []
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def _select_claims(sentences: Iterable[str]) -> list[str]:
    claims: list[str] = []
    for sentence in sentences:
        lower = sentence.lower()
        if any(token in lower for token in (" will ", " has ", " have ", " is ", " are ", " was ", " were ")):
            claims.append(sentence)
        elif re.search(r"\b\d+%?\b", sentence):
            claims.append(sentence)
        if len(claims) >= 5:
            break
    return claims


def _build_headline(sentences: list[str]) -> str:
    if not sentences:
        return "No topic detected from the provided text."
    first_sentence = sentences[0]
    return first_sentence if first_sentence.endswith((".", "!", "?")) else f"{first_sentence}."


def _confidence_note(sentences: list[str], claims: list[str]) -> str:
    if not sentences:
        return "No source text was provided, so reliability cannot be assessed."
    detail_score = sum(1 for sentence in sentences if re.search(r"\b\d+%?\b", sentence))
    clarity = "clear" if len(sentences) <= 6 else "mixed"
    if detail_score >= 2 and len(claims) >= 3:
        return (
            "The text is relatively clear and includes multiple concrete details, "
            "so the claims appear moderately reliable pending verification."
        )
    if detail_score == 0:
        return (
            "The text offers broad statements with few specifics, so reliability is uncertain "
            "and would benefit from corroborating sources."
        )
    return (
        f"The text has {clarity} structure with some factual indicators, suggesting partial reliability "
        "that should be checked against primary sources."
    )


def _watch_items(sentences: list[str]) -> list[str]:
    if not sentences:
        return ["Clarify the main topic and provide supporting facts."]
    watchlist = []
    if any("could" in sentence.lower() or "may" in sentence.lower() for sentence in sentences):
        watchlist.append("Verify conditional statements against confirmed reports.")
    if any(re.search(r"\b\d+%?\b", sentence) for sentence in sentences):
        watchlist.append("Confirm the quantitative figures with original data.")
    watchlist.append("Identify the primary sources behind the reported claims.")
    return watchlist[:3]


def _uncertainty_flags(sentences: list[str]) -> list[str]:
    if not sentences:
        return ["No input text provided to evaluate."]
    flags = []
    if any(len(sentence.split()) < 6 for sentence in sentences):
        flags.append("Some sentences are very short, which may omit important context.")
    if any(token in " ".join(sentences).lower() for token in ("some", "many", "various", "likely", "reportedly")):
        flags.append("Vague qualifiers suggest potential uncertainty or bias.")
    if not any(re.search(r"\b\d+%?\b", sentence) for sentence in sentences):
        flags.append("No numeric data was provided to anchor the claims.")
    return flags[:3]


@click.group()
def cli() -> None:
    """Run the MetaNewsX CLI."""


@cli.command()
def demo() -> None:
    """Print a sample Decision-Grade Brief."""
    click.echo(textwrap.dedent(DECISION_GRADE_BRIEF).strip())


@cli.command()
@click.argument("text")
def analyze(text: str) -> None:
    """Analyze raw article text and generate a Decision-Grade Brief."""
    sentences = _split_sentences(text)
    claims = _select_claims(sentences)
    headline = _build_headline(sentences)
    confidence = _confidence_note(sentences, claims)
    watch_items = _watch_items(sentences)
    flags = _uncertainty_flags(sentences)

    lines = [
        "Decision-Grade Brief",
        "====================",
        "",
        "HEADLINE",
        headline,
        "",
        "CLAIMS",
    ]
    if claims:
        lines.extend([f"- {claim}" for claim in claims])
    else:
        lines.append("- No clear factual claims detected from the text.")
    lines.extend(
        [
            "",
            "CONFIDENCE",
            confidence,
            "",
            "WHAT TO WATCH",
        ]
    )
    lines.extend([f"- {item}" for item in watch_items])
    lines.extend(["", "UNCERTAINTY FLAGS"])
    lines.extend([f"- {flag}" for flag in flags])

    click.echo("\n".join(lines))


if __name__ == "__main__":
    cli()
