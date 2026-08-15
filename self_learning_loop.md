# The self-learning loop

The repo generates touches. The *engine* is the loop that makes next week's touches
better than this week's, automatically. This is what turns "campaigns" into "a system."

## The data model

Every generated touch writes one row:

| field | example | why it matters |
|---|---|---|
| `attribution_id` | `lead_9f2a1c7b04` | joins the touch back to CRM outcomes |
| `icp` | `developer` | the routing hypothesis |
| `funnel_stage` | `activation` | where we thought they were |
| `channel` | `community` | where we reached them |
| `message_angle` | `proof / how-it-works` | the copy hypothesis |
| `sent_at` | `2026-08-15T09:00Z` | for time-to-outcome |

Outcomes (reply, meeting, opportunity, closed-won) are joined on `attribution_id`
from HubSpot / Salesforce.

## The loop

```
generate touch ──► log (icp × channel × angle) ──► CRM outcome joins back
      ▲                                                      │
      │                                                      ▼
   updated weights ◄──── aggregate reply / pipeline rate per (icp × channel × angle)
```

1. Aggregate reply and pipeline rate per **icp × channel × message_angle**.
2. Down-weight angles and channels that convert poorly for each ICP; up-weight winners.
3. Feed those weights back into the router and the prompt library, so the next batch is
   drawn from what actually converted, not from a static playbook.

## First experiments I'd run

| Experiment | Hypothesis | Metric | Scale / kill |
|---|---|---|---|
| Proof-led vs outcome-led for developers | Developers reply more to how-it-works than to ROI | reply rate (dev ICP) | kill outcome-led for devs if it trails 2 weeks |
| Community vs email for activation-stage devs | Community touches out-convert cold email | touch → docs return | move budget to the winner |
| Governance-led vs speed-led for enterprise | On-prem/compliance framing books more demos | touch → demo booked | scale the framing that books |

## Honest limits

- Attribution on a developer-led motion is messy: the dev who evaluates is rarely the
  buyer who signs. I'd model **account-level** conversion, not just lead-level, and treat
  the developer touch as an assist, not a last-click.
- Small sample sizes early on, so I'd hold decisions until each cell clears a minimum
  volume rather than chasing noise.
