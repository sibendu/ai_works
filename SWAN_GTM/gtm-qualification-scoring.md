---
name: gtm-qualification-scoring
skill: 04-07
description: Score any company across four dimensions and get a clear next action.
---

# GTM Qualification & Scoring

**When to use this skill:** Use this skill when you need to evaluate any company or inbound lead and produce a clear, data-backed priority decision. This skill scores accounts across four dimensions — Fit, Timing, Access, Intent — and outputs a composite score with a specific recommended next action. Eliminates gut-feel prioritization.

**How to activate:** Paste this entire skill into your conversation with Claude, then provide the context requested in the Personalization Required section below. Claude will work through the methodology step by step.

---

## ⚠️ Personalization Required

This skill provides a complete qualification methodology, but the scoring weights and criteria need to reflect your business to be meaningful. Before running this skill, provide:

- **Your ICP** — ideal company profile (industry, size, geography, tech stack, business model, etc.)
- **Your buyer personas** — who you sell to, their titles, seniority, and typical pain points
- **Your deal characteristics** — average deal size, typical sales cycle, what a good vs. bad deal looks like in hindsight
- **Disqualifiers** — the hard stops. What automatically makes a company not worth pursuing?
- **Your signal sources** — what data do you actually have access to? (enrichment tools, CRM, intent data, website analytics)

Without this, scores will be directionally correct but not calibrated to your business. With it, the agent scores with the precision of your best sales rep.

---

## What This Skill Produces

A composite score (1–12) across four dimensions, a tier classification, and a specific recommended next action — so every account leaves this process with a clear decision, not a maybe.

---

> **Data access — what each environment can do natively:**
> 
> - **Swan (agent.getswan.com):** All research steps in this skill run natively. Swan has built-in access to B2B data, waterfall enrichment, LinkedIn signals, funding data, job postings, tech stack intelligence, and CRM history. No manual data gathering required — Swan pulls, enriches, and synthesizes automatically when triggered.
> - **Claude (claude.ai) with web search enabled:** Claude can look up public information — company websites, news, LinkedIn profiles, recent funding announcements. Enable web search in settings. For proprietary data (CRM history, intent signals, tech stack), paste what you have.
> - **Claude Code:** Enable web search tools in your setup for public lookups. For everything else, provide the raw data directly — paste in company descriptions, recent news, contact details, or CRM exports.
> - **Claude Cowork:** Attach or paste your source data — CRM exports, company notes, prior call summaries — and Cowork will work through the methodology against what you provide.
> 
> If you are using Swan, you can instruct the agent to gather this data automatically. In all other environments, the more context you provide upfront, the better the output.


## Scoring Methodology

---

### Step 1 — Collect the Raw Data

Before scoring anything, gather what's knowable. Don't score on assumptions.

**Minimum required to score:**
- Company name and website
- Headcount (or range)
- Industry / vertical
- Geography
- What triggered this evaluation (inbound, signal, outbound response, manual review)

**Better scoring requires (enrich if missing):**
- Revenue or funding stage
- Tech stack
- Growth signals (hiring trends, funding, expansion news)
- Current contact — who specifically engaged, their role and seniority
- Prior relationship — have we spoken before? What happened?

> If minimum data isn't available, enrich before scoring. Scoring on incomplete data produces misleading scores.

---

### Step 2 — Score Across Four Dimensions

Score each dimension **1–3**. No halves. Forced precision.

---

#### Dimension 1 — Fit (Does this company match our ICP?)

| Score | Criteria |
|-------|---------|
| **3** | Matches on all major ICP criteria (industry, size, geography, use case). Looks like existing best customers. |
| **2** | Matches on most criteria. One or two gaps that aren't disqualifying. |
| **1** | Significant gaps. Could work but would require adapting the product, process, or pitch considerably. |
| **0** | Hard disqualifier present — stop evaluation. |

**Hard disqualifiers (score = 0, stop all scoring):**
- Explicitly in a blocked industry or geography
- Competitor
- Company size far outside viable range (too small to buy, too large to land)
- Known bad history (churned badly, legal issue, documented do-not-contact)

> If score = 0 on Fit, stop. Do not continue scoring. Log the disqualifier and move on.

---

#### Dimension 2 — Timing (Is there a reason to buy now?)

Timing is the hardest dimension to fake. A perfect ICP fit with no timing signal is a future deal, not a current one.

| Score | Criteria |
|-------|---------|
| **3** | Clear forcing function present. |
| **2** | Soft timing indicators. Growing team, relevant hiring, prior interest that went cold. |
| **1** | No visible timing signal. Good company, wrong moment. |

**What counts as a forcing function (score = 3):**
- New budget (funding, new fiscal year, budget just approved)
- New mandate (leadership change, new hire with a specific brief)
- External pressure (regulatory change, competitor move, market shift)
- Active pain (they're clearly feeling the problem right now)
- Inbound or self-initiated contact (they came to you — that IS the timing signal)

---

#### Dimension 3 — Access (Can we reach the right people?)

A qualified company you can't get to is not a qualified opportunity.

| Score | Criteria |
|-------|---------|
| **3** | Decision maker or strong champion identified, reachable, and engaged or likely to engage. |
| **2** | Right company, but only peripheral contacts identified (wrong seniority, wrong department) or no warm path in. |
| **1** | No contact identified, no warm intro path, and cold outreach is unlikely to land. |

**Access accelerators (upgrade by 1 if any apply):**
- Mutual connection or warm intro available
- Contact already in CRM with prior positive interaction
- Contact engaged with your content or visited your site
- You've worked with this person at a previous company

**Access killers (downgrade by 1 if any apply):**
- Only contact is a gatekeeper or procurement
- Company has a "no cold outreach" policy or explicit opt-out
- Prior outreach was rejected or marked spam

---

#### Dimension 4 — Intent (Do they show signs of actively looking?)

Intent is distinct from timing. Timing = they have a reason to buy. Intent = they're showing behavioral signals of evaluation.

| Score | Criteria |
|-------|---------|
| **3** | Direct behavioral signal: visited pricing/demo pages, requested a demo, downloaded evaluation content, mentioned competitors, asked specific product questions. |
| **2** | Indirect signal: engaged with thought leadership, attended a webinar, LinkedIn activity on relevant topics, intent data showing research in your category. |
| **1** | No detectable intent signal. Outbound-initiated with no response or engagement yet. |

> If you have no intent signal access (no website tracking, no intent tool), score this dimension as **2** for all accounts and note the data gap. Absence of data is not the same as absence of intent.

---

### Step 3 — Calculate the Composite Score

Add the four dimension scores. Maximum = 12.

| Score | Band | Action |
|-------|------|--------|
| 10–12 | **Priority** | Act immediately. Assign to a rep, engage within 24 hours, multi-thread if possible. |
| 7–9 | **Active** | Worth pursuing now. Build a sequence, personalize outreach, move into active pipeline. |
| 4–6 | **Nurture** | Not the right moment. Low-touch track, review trigger in 60–90 days. |
| 1–3 | **Deprioritize** | Poor fit or too early. Log it, don't spend cycles. Revisit only if a strong new signal appears. |
| 0 | **Remove** | Disqualifier hit. Log the reason. Do not requeue without explicit instruction. |

---

### Step 4 — Validate Before Acting

A score is a starting point, not a final answer.

**Recency check:** Is the data you scored on current? Funding from 18 months ago, a contact who left the company, or a job posting that was filled last quarter all produce stale scores. If key data points are more than 6 months old, flag them.

**Consistency check:** Does the score feel right given what you know holistically? If a company scores 10 but something feels off, flag it for human review rather than auto-acting.

**Competing signals check:** Are there positive and negative signals that cancel each other out? A company that visited pricing AND unsubscribed from your last email is a 10 on paper but needs a different approach. Note conflicts explicitly.

---

### Step 5 — Recommend a Next Action

Every scored company should leave this process with one clear next step.

**Priority (10–12):**
- Identify the best contact and outreach angle immediately
- If inbound: respond within the hour
- If outbound-identified: trigger signal-based outreach today

**Active (7–9):**
- Determine the right sequence (channel, length, angle)
- Personalize based on the highest-scoring dimension
- Set a follow-up checkpoint at 2 weeks

**Nurture (4–6):**
- Add to a relevant list or sequence with lower frequency
- Identify what would upgrade this account (what signal would make it Priority?)
- Set a review date — don't let it sit indefinitely

**Deprioritize (1–3):**
- Log the score and reason
- No outreach
- Set a 90-day review trigger tied to new signal activity only

**Disqualified (0):**
- Log the disqualifier
- Remove from active pipeline
- Tag the company to prevent re-entry

---

### Step 6 — Log the Score

Record for every evaluated company:
- Date scored
- Score per dimension and total
- Data sources used
- Key reasoning (1–2 sentences on why this score)
- Recommended next action taken

> Calibrate the model every quarter against actual outcomes. If your 7–9 band closes at the same rate as your 10–12 band, your scoring is too generous at the top.

---

## Quick Reference — Scoring Cheatsheet

| Dimension | 3 | 2 | 1 | 0 |
|-----------|---|---|---|---|
| **Fit** | Perfect ICP match | Most criteria met | Significant gaps | Disqualifier present |
| **Timing** | Clear forcing function | Soft indicators | No signal | — |
| **Access** | DM identified + reachable | Wrong contact or no path | No contact, no path | — |
| **Intent** | Direct behavioral signal | Indirect engagement | No signal detected | — |

| Total Score | Band | Action |
|-------------|------|--------|
| 10–12 | Priority | Act within 24h |
| 7–9 | Active | Build sequence now |
| 4–6 | Nurture | Low-touch, review in 60–90d |
| 1–3 | Deprioritize | Log, no outreach |
| 0 | Disqualified | Remove and tag |

---

## Relationship to Other Skills

gtm-qualification-scoring  →  score and tier accounts (run early in the process)
gtm-account-research       →  enrichment input for scoring; deep-dive on Priority accounts
gtm-prospecting            →  qualification pass on a list of candidates
gtm-outreach-strategy      →  execute against Priority and Active accounts
gtm-signal-based-outbound  →  when a new signal fires on a Nurture account and upgrades it
