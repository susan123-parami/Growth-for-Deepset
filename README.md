# GTM Demand Engine

AI-assisted, self-learning demand workflow, built in **Haystack + Claude**.
A value artifact for deepset's Growth Marketing Manager role.

By May Thaw Tar · [maythawtar.com](https://www.maythawtar.com) · [LinkedIn](https://www.linkedin.com/in/may-thaw-tar-susan/)

---

## The problem it models

deepset sells one product to two ICPs that buy in opposite directions:

- **Developer** — arrives via Haystack (open source). Bottom-up, proof-led.
- **Enterprise** — buys the platform. Top-down, ROI-led, sales-assisted.

> One product, two journeys. Earn the developer's trust first; the enterprise deal follows.

## What it does

```
lead + signal ─► ICP router ─► message generator ─► CRM-ready record
                 dev / ent     copy · channel · stage   (HubSpot / SFDC)
```

**In**

```json
{ "company": "Northwind Robotics", "signal": "starred haystack; 3 engineers signed up for docs" }
```

**Out**

```json
{ "icp": "developer", "funnel_stage": "activation",
  "channel": "community + docs, not sales",
  "message": { "subject": "the 3-line haystack pipeline your team read", "body": "..." },
  "attribution_id": "lead_9f2a1c7b04" }
```

## Why the message changes (the point)

| ICP | Value story | Channel |
|---|---|---|
| **Developer** | "Build production RAG with control over retrieval, evaluation, deployment." | Haystack content · GitHub · community |
| **Enterprise** | "Move AI from experimentation to production without giving up control or sovereignty." | LinkedIn · outbound · case study |

Same capability, framed for how each ICP decides. That reframing, not the automation, is the work.

## Human in the loop

Not "AI runs GTM." **AI drafts, a human approves.**

```
signals → AI enrich → ICP classify → AI draft ─►  HUMAN APPROVAL  ─►  launch
                                                         ▲               │
                        new hypotheses ◄── AI analysis ◄── performance data
```

## The self-learning loop

- Aggregate reply and pipeline rate per **ICP × channel × message-angle**.
- Reweight: down the losers, up the winners. Feed back into router + prompts.
- Metric chain: **engagement → MQL → SQL → opportunity → pipeline.**

Data model, experiments, and attribution caveats: [`docs/self_learning_loop.md`](docs/self_learning_loop.md).

## Run

```bash
pip install -r requirements.txt
cp .env.example .env          # add ANTHROPIC_API_KEY
python demand_engine.py       # standalone (Anthropic SDK)
python haystack_pipeline.py   # same logic, Haystack pipeline
```

## Files

| File | What |
|---|---|
| `demand_engine.py` | Standalone version (Anthropic SDK). |
| `haystack_pipeline.py` | Same logic as a Haystack pipeline (deepset-platform version). |
| `data/leads.sample.json` | Synthetic leads, mixed developer / enterprise signals. |
| `docs/self_learning_loop.md` | Feedback loop, experiments, attribution notes. |

## How it maps to the role

| What JD asks for | What I do |
|---|---|
| Demand gen as a self-learning system | the feedback loop |
| Full-funnel, awareness → opportunity | `funnel_stage` + metric chain |
| AI-assisted workflows | LLM segmentation + messaging |
| APIs / automation / data workflows | Python, structured pipeline |
| ICP mapping + value-based messaging | dev vs enterprise routing + copy |
| Developer **and** enterprise audiences | both journeys, one engine |
| Haystack | built in it |
| Attribution to revenue | `attribution_id` → CRM |

## Notes

- Synthetic data, no private info. A prototype to show how I think, not production code.
- Imports and pipeline assembly verified against `haystack-ai` 3.0; the live model call needs your `ANTHROPIC_API_KEY`.
