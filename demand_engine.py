"""Route a lead into deepset's two ICPs (developer vs enterprise) and draft the
message, channel, and funnel stage tuned to how that ICP buys.

Standalone version (Anthropic SDK). See haystack_pipeline.py for the same logic
as a Haystack pipeline.
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

MODEL = "claude-3-5-sonnet-latest"
DATA_FILE = Path(__file__).parent / "data" / "leads.sample.json"
_JSON = re.compile(r"\{.*\}", re.DOTALL)

SYSTEM_PROMPT = """You route leads for deepset, which sells one product to two ICPs.

developer: arrives via Haystack (open source). bottom-up, evidence-led, distrusts
  marketing. win with proof, control, how-it-works, through community, not sales.
enterprise: economic buyer for the platform. top-down, ROI-led, sales-assisted.
  win with outcomes, governance, risk reduction, through LinkedIn and outbound.

Earn the technical evaluator first; the enterprise deal follows developer trust.

Given one lead, return ONLY this JSON:
{"icp":"developer|enterprise","why":"<one sentence from the signal>",
 "funnel_stage":"awareness|activation|consideration|sales_ready",
 "channel":"<best channel for this icp+stage>",
 "message":{"subject":"<lowercase, <=9 words>","body":"<=60 words, concrete>"}}"""


@dataclass(frozen=True)
class Lead:
    company: str
    domain: str
    signal: str


@dataclass(frozen=True)
class Touch:
    company: str
    icp: str
    why: str
    funnel_stage: str
    channel: str
    subject: str
    body: str
    attribution_id: str  # joins the touch back to CRM outcomes for the learning loop


def load_leads(path: Path = DATA_FILE) -> list[Lead]:
    return [Lead(**row) for row in json.loads(path.read_text())]


def extract_json(text: str) -> dict:
    match = _JSON.search(text)
    if not match:
        raise ValueError(f"no JSON object in reply: {text[:120]}")
    return json.loads(match.group())


def route(lead: Lead, client: Anthropic) -> Touch:
    reply = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": json.dumps(asdict(lead))}],
    )
    data = extract_json(reply.content[0].text)
    return Touch(
        company=lead.company,
        icp=data["icp"],
        why=data["why"],
        funnel_stage=data["funnel_stage"],
        channel=data["channel"],
        subject=data["message"]["subject"],
        body=data["message"]["body"],
        attribution_id=f"lead_{uuid.uuid4().hex[:10]}",
    )


def main() -> None:
    load_dotenv()
    client = Anthropic()
    for lead in load_leads():
        t = route(lead, client)
        print(f"\n{t.company}  ->  {t.icp.upper()}  ({t.funnel_stage})")
        print(f"  why     {t.why}")
        print(f"  channel {t.channel}")
        print(f"  subject {t.subject}")
        print(f"  body    {t.body}")


if __name__ == "__main__":
    main()
