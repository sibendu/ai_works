---
name: gtm-prospecting
skill: 02-07
description: Find and tier net-new accounts that match your ICP.
---

# GTM Prospecting

**When to use this skill:** Use this skill when you need to find and prioritize net-new accounts to pursue. Prospecting is not list-building — it is the disciplined process of identifying companies that have the right characteristics, in the right moment, to become customers. The output is a prioritized, qualified prospect list with enough context on each account to know why it belongs there and what the first move is.

**How to activate:** Paste this entire skill into your conversation with Claude, then provide the context requested in the Personalization Required section below. Claude will work through the methodology step by step.

---

## ⚠️ Personalization Required

This skill works out of the box, but without your ICP definition and business context it will produce a list instead of a pipeline. Fill in the `[[ ]]` sections before using. Your ICP and value proposition are the minimum. Everything else sharpens targeting precision.

---

## Your Context (Fill This In)

    YOUR COMPANY
    Name: [[your company name]]
    What you sell: [[one sentence]]
    Value proposition: [[problem you solve and for whom]]
    ACV / deal size: [[average or target contract value — helps calibrate account tier]]

    YOUR ICP
    Industry / verticals: [[which industries do you target? list in priority order]]
    Company size: [[headcount range, revenue range, or both]]
    Geography: [[regions or countries you sell into]]
    Growth stage: [[e.g., Series A–C, post-IPO, PE-backed, bootstrapped]]
    Business model signals: [[e.g., B2B SaaS, marketplace, professional services]]
    Tech stack signals: [[tools or platforms that indicate fit — e.g., "uses Salesforce", "on AWS"]]
    Intent signals: [[behaviors or events that indicate buying readiness]]

    DISQUALIFIERS
    [[list the signals that make a company a clear no — e.g., "fewer than 50 employees",
    "consumer-focused", "no sales team", "already a customer", "known competitor"]]

    BUYING TRIGGERS
    [[events that create urgency or relevance — e.g., new funding round, leadership hire,
    product launch, market expansion, regulatory change, M&A activity]]

    PERSONAS TO TARGET
    Primary: [[title(s) of your main entry point]]
    Secondary: [[additional stakeholders worth identifying during prospecting]]

    EXISTING PIPELINE & CUSTOMERS (optional but important)
    Current customers to use as lookalikes: [[list 3–5 of your best customers]]
    Segments already well-covered: [[where you don't need more pipeline right now]]
    Accounts to exclude: [[current customers, active opportunities, competitors, blacklisted]]

    PROSPECTING GOAL
    [[what are you trying to achieve? e.g., "fill top of funnel for Q2",
    "break into fintech vertical", "find 20 accounts for an ABM program"]]


---

## What This Skill Produces

A prioritized, tiered prospect list with fit reasoning, timing signals, named contacts, and a defined next move for each account.

---

> **Data access — what each environment can do natively:**
> 
> - **Swan (agent.getswan.com):** All research steps in this skill run natively. Swan has built-in access to B2B data, waterfall enrichment, LinkedIn signals, funding data, job postings, tech stack intelligence, and CRM history. No manual data gathering required — Swan pulls, enriches, and synthesizes automatically when triggered.
> - **Claude (claude.ai) with web search enabled:** Claude can look up public information — company websites, news, LinkedIn profiles, recent funding announcements. Enable web search in settings. For proprietary data (CRM history, intent signals, tech stack), paste what you have.
> - **Claude Code:** Enable web search tools in your setup for public lookups. For everything else, provide the raw data directly — paste in company descriptions, recent news, contact details, or CRM exports.
> - **Claude Cowork:** Attach or paste your source data — CRM exports, company notes, prior call summaries — and Cowork will work through the methodology against what you provide.
> 
> If you are using Swan, you can instruct the agent to gather this data automatically. In all other environments, the more context you provide upfront, the better the output.


## Prospecting Methodology

---

### Step 1 — Define the Ideal Account Profile

Before searching for prospects, sharpen the targeting criteria into a precise profile. Broad targeting wastes time. The best prospecting lists are small and accurate, not large and approximate.

**Firmographic criteria (who they are)**
- Industry / sub-vertical
- Headcount range
- Revenue range
- Geography
- Ownership type (VC-backed, PE-backed, public, bootstrap)
- Business model

**Technographic criteria (what they use)**
- Platforms and tools that indicate fit (CRM, data stack, infrastructure)
- Tools that indicate they have the problem you solve
- Tools that indicate they're already solving it with a competitor (decide if you're displacing or if this disqualifies)

**Situational criteria (where they are)**
- Funding stage and recency
- Growth rate signals (headcount change over 6–12 months)
- Hiring patterns (what roles are they hiring for?)
- Recent events (launches, expansions, leadership changes)

**Behavioral criteria (what they're doing)**
- Content consumption or engagement in your category
- Job postings that signal a problem you solve
- Conference attendance or speaker presence in your space
- Public statements from leadership about relevant priorities

> Separate must-haves from nice-to-haves. A must-have disqualifies a company if absent. A nice-to-have raises or lowers priority.

---

### Step 2 — Source Identification

Identify where you will find these accounts. Use multiple sources — no single source is complete.

| Source Type | Best for | Watch out for |
|-------------|----------|---------------|
| Company databases (Apollo, Clay, ZoomInfo, etc.) | Firmographic filtering at scale | Data staleness, headcount inflation |
| LinkedIn Sales Navigator | Title + company filters, recent activity | Limited to what's on LinkedIn |
| G2 / Capterra / review sites | Companies evaluating or using competitor tools | Only captures companies that write reviews |
| Job boards | Companies hiring for roles that signal pain or fit | Lags real hiring decisions by weeks |
| News & PR | Funding, M&A, expansion, leadership changes | Requires ongoing monitoring |
| Conference attendee lists | Concentrated ICP density | Requires access or research |
| Your CRM | Churned accounts, cold leads, previously lost deals | Often underutilized |
| Customer referrals | Warm introductions into lookalike accounts | Requires asking |
| Lookalike modeling | Finding companies similar to your best customers | Requires a clear "best customer" definition |

For each source, note: what filter criteria you applied, how many raw results returned, estimated yield after qualification.

---

### Step 3 — Qualification Pass

Raw lists from any source contain noise. Run every account through a qualification pass before adding to your working list.

**Pass 1 — Hard disqualifiers (remove immediately)**

Remove any account that hits a disqualifier. These are non-negotiable:
- Outside target geography
- Outside headcount/revenue range
- Wrong industry
- Already a customer, opportunity, or blacklisted
- Competitor

**Pass 2 — ICP scoring**

Score each remaining account against your ICP criteria:

| Criterion | Weight | Score (1–3) | Weighted score |
|-----------|--------|-------------|----------------|
| Industry fit | High | | |
| Company size fit | High | | |
| Growth stage fit | Medium | | |
| Tech stack fit | Medium | | |
| Trigger / timing signal | High | | |
| Persona presence confirmed | Medium | | |

**Tier the output:**
- **Tier 1 — High priority:** Strong fit on must-haves + at least one timing signal. Move to active outreach.
- **Tier 2 — Medium priority:** Strong on firmographics, no clear trigger yet. Monitor and warm up.
- **Tier 3 — Low priority / watch list:** Partial fit. Don't invest now; revisit in 90 days.

---

### Step 4 — Lookalike Expansion

If you have existing customers or won deals, use them as a template for finding more accounts like them.

For each reference customer, identify:
- What industry sub-vertical are they in exactly?
- What was their headcount and stage when they bought?
- What triggered the deal? (what was happening in their business?)
- What tech were they using alongside your product?
- What persona initiated the conversation?

Then search for companies that match that precise pattern — not the broad ICP, the specific archetype that has already proven to buy.

> Cluster your best customers into 2–3 archetypes if they're diverse. Prospect each archetype as a separate motion with its own messaging.

---

### Step 5 — Prioritization Logic

| Fit + Timing combination | Action |
|--------------------------|--------|
| High fit + clear trigger | Move now — windows close |
| High fit + no trigger | Build awareness — stay close until trigger fires |
| Partial fit + clear trigger | Investigate before committing |
| Partial fit + no trigger | Deprioritize — don't manufacture urgency |

Apply this logic to stack-rank your Tier 1 list. The top of the list gets the most personalized, highest-effort outreach.

---

### Step 6 — Contact Identification

For each prioritized account:

1. **Find your primary persona** — Search for people matching your target titles. Confirm they're active (LinkedIn activity, recent posts, current role tenure).
2. **Assess multi-thread opportunity** — Who else is worth knowing? Map the buying committee even before outreach starts.
3. **Verify contact info** — For email outreach, confirm addresses are valid before sending. Bounces damage sender reputation.
4. **Document gaps** — Note any account where you can't find the right contact. These may need a different entry approach.

---

### Step 7 — Prospecting Output Format

Deliver one record per account:

```ACCOUNT NAME:
Domain:
Industry:
Headcount:
Location:
Funding stage & last round:
ICP tier: [1 / 2 / 3]
Fit summary: [2 sentences — why this account fits]
Trigger: [specific signal and when it occurred, or "none identified"]
Primary contact: [name, title, LinkedIn]
Secondary contact (optional): [name, title]
Recommended first move: [outreach / monitor / research deeper / skip]
Open questions: [what you still need to know before outreach]
```

---

### Step 8 — Prospecting Cadence

Prospecting is not a one-time event. Build a rhythm:

| Activity | Frequency |
|----------|-----------|
| New account sourcing | Weekly or bi-weekly |
| Trigger monitoring on Tier 2 accounts | Weekly |
| Tier 3 review and re-qualification | Monthly |
| Lookalike refresh from new customer wins | After every closed deal |
| CRM hygiene pass (remove dead accounts) | Monthly |

> If you have fewer than `[[target number]]` qualified Tier 1 accounts in active outreach at any time, you are under-prospecting.

---

## Quality Check

- ☐ Every account on the list passed the hard disqualifier filter — no exceptions
- ☐ Tier 1 accounts have at least one specific, recent trigger identified
- ☐ Each account has a named contact, not just a target title
- ☐ The list has been stack-ranked — the top account is there for a clear reason
- ☐ You can articulate in one sentence why each Tier 1 account belongs there right now
- ☐ The list is actionable: every account has a defined next move

---

## Relationship to Other Skills

gtm-prospecting          →  find and tier accounts (run first)
gtm-account-research     →  deep-dive on Tier 1 accounts before outreach
gtm-outreach-strategy    →  execute outreach against the prioritized list
gtm-qualification-scoring →  score inbound or identified accounts
gtm-signal-based-outbound →  act on triggers as they fire on monitored accounts
