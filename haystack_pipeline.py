"""GTM demand engine as a Haystack pipeline: the version that runs on deepset's own
platform. Same data layer and routing logic as demand_engine.py.
Assembly verified against haystack-ai 3.0 (ChatPromptBuilder + AnthropicChatGenerator).

    prompt (ChatPromptBuilder) -> llm (AnthropicChatGenerator)
"""

from __future__ import annotations

import uuid

from dotenv import load_dotenv
from haystack import Pipeline
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from haystack.utils import Secret
from haystack_integrations.components.generators.anthropic import AnthropicChatGenerator

from demand_engine import MODEL, Lead, Touch, extract_json, load_leads

TEMPLATE = """You route leads for deepset, which sells one product to two ICPs.

developer: arrives via Haystack (open source). bottom-up, evidence-led. win with
  proof, control, how-it-works, through community, not sales.
enterprise: economic buyer for the platform. top-down, ROI-led, sales-assisted.
  win with outcomes, governance, risk reduction, through LinkedIn and outbound.

Earn the technical evaluator first; the enterprise deal follows developer trust.

Lead: {{ lead }}

Return ONLY this JSON:
{"icp":"developer|enterprise","why":"<one sentence>","funnel_stage":"awareness|activation|consideration|sales_ready","channel":"<best channel>","message":{"subject":"<lowercase, <=9 words>","body":"<=60 words>"}}"""


def build_pipeline() -> Pipeline:
    pipe = Pipeline()
    pipe.add_component(
        "prompt",
        ChatPromptBuilder(template=[ChatMessage.from_user(TEMPLATE)], required_variables=["lead"]),
    )
    pipe.add_component(
        "llm",
        AnthropicChatGenerator(
            api_key=Secret.from_env_var("ANTHROPIC_API_KEY"),
            model=MODEL,
            generation_kwargs={"max_tokens": 600},
        ),
    )
    pipe.connect("prompt.prompt", "llm.messages")
    return pipe


def route(pipe: Pipeline, lead: Lead) -> Touch:
    lead_str = f"{lead.company} ({lead.domain}): {lead.signal}"
    result = pipe.run({"prompt": {"lead": lead_str}})
    data = extract_json(result["llm"]["replies"][0].text)
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
    pipe = build_pipeline()
    for lead in load_leads():
        t = route(pipe, lead)
        print(f"\n{t.company}  ->  {t.icp.upper()}  ({t.funnel_stage})")
        print(f"  channel {t.channel}")
        print(f"  subject {t.subject}")
        print(f"  body    {t.body}")


if __name__ == "__main__":
    main()
