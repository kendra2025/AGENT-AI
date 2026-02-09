"""CLI for MetaNewsX."""

import textwrap

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


@click.group()
def cli() -> None:
    """Run the MetaNewsX CLI."""


@cli.command()
def demo() -> None:
    """Print a sample Decision-Grade Brief."""
    click.echo(textwrap.dedent(DECISION_GRADE_BRIEF).strip())


if __name__ == "__main__":
    cli()
