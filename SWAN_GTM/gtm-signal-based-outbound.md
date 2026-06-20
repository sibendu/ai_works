---
name: gtm-signal-based-outbound
skill: 05-07
description: Turn a buying signal into a personalized, timed outreach sequence.
---

# GTM Signal-Based Outbound

**When to use this skill:** Use this skill when a specific behavioral signal — a website visit, job change, funding round, hiring surge, or content engagement — triggers an outreach decision. This skill guides you to classify signal strength, research context, determine the right angle, write personalized messages, and sequence follow-ups. This is distinct from the Outreach Strategy skill, which handles planned outreach; this skill handles reactive, signal-driven outbound where timing is the competitive advantage.

**How to activate:** Paste this entire skill into your conversation with Claude, then provide the context requested in the Personalization Required section below. Claude will work through the methodology step by step.

---

## ⚠️ Personalization Required

This skill is a complete methodology, but it's missing the context that makes it effective for your situation. Before running this skill, provide:

- **What you sell** — product/service, ICP, key use cases
- **Your senders** — who is reaching out (name, role, tone)
- **Signal sources** — which signals you actually have access to (e.g., website visitor data, LinkedIn alerts, intent tools, news feeds)
- **Outreach channels** — email, LinkedIn, phone, or a combination
- **Message examples** — 2–3 examples of outreach that has worked in the past

Without this, the agent will produce structurally correct but generic outreach. With it, it will produce context-driven, personalized messages that convert.

---

## What This Skill Produces

A classified signal assessment, a research-backed angle, and a ready-to-send personalized message (or sequence) that references the signal without being creepy.

---

> **Data access — what each environment can do natively:**
> 
> - **Swan (agent.getswan.com):** All research steps in this skill run natively. Swan has built-in access to B2B data, waterfall enrichment, LinkedIn signals, funding data, job postings, tech stack intelligence, and CRM history. No manual data gathering required — Swan pulls, enriches, and synthesizes automatically when triggered.
> - **Claude (claude.ai) with web search enabled:** Claude can look up public information — company websites, news, LinkedIn profiles, recent funding announcements. Enable web search in settings. For proprietary data (CRM history, intent signals, tech stack), paste what you have.
> - **Claude Code:** Enable web search tools in your setup for public lookups. For everything else, provide the raw data directly — paste in company descriptions, recent news, contact details, or CRM exports.
> - **Claude Cowork:** Attach or paste your source data — CRM exports, company notes, prior call summaries — and Cowork will work through the methodology against what you provide.
> 
> If you are using Swan, you can instruct the agent to gather this data automatically. In all other environments, the more context you provide upfront, the better the output.


## Outbound Methodology

---

### Step 1 — Classify the Signal

Before doing anything, identify what type of signal this is. Signal type determines urgency, research depth, and angle.

**Tier 1 — High-intent (act within 24h)**
- Website visit to pricing, product, or demo pages
- Inbound form fill or demo request
- Direct reply to any prior outreach
- Review site activity (G2, Capterra, etc.)
- Re-engagement from a previously cold or lost account

**Tier 2 — Moderate-intent (act within 72h)**
- Job change — a known contact or ICP persona joined a new company
- New relevant hire at a target company (e.g., they hired a Head of RevOps)
- Funding round announced
- Company expansion into a new market or geography
- Former champion or customer moved to a new company

**Tier 3 — Weak-intent (act within 1 week, lower priority)**
- LinkedIn content engagement (likes, comments on relevant posts)
- News mention without clear buying signal
- Technology install or removal detected
- Hiring volume increase in a relevant department
- Conference or event attendance

> If the signal type is unclear, default to Tier 2 handling.

---

### Step 2 — Research Before Writing

Never write outreach before researching. The research determines whether to reach out at all and what angle to use.

**For the company:**
- What do they do, how big are they, what's their current moment (growth, transition, pressure)?
- Does this company fit the ICP? If not, stop.
- Is there an existing relationship (current customer, past deal, prior outreach)?

**For the signal:**
- What specifically happened? Get the details (not just "they got funding" — the amount, stage, stated use of funds)
- How recent is it? Signals older than 30 days lose relevance fast
- Is there a clear connection between this signal and what you sell?

**For the contact:**
- Who is the right person to reach out to given this signal? (Not always the person who triggered the signal)
- What is their role, seniority, likely priorities?
- Any shared context — mutual connections, past interaction, content they've published?

> If you cannot establish a clear connection between the signal and a specific pain or priority for this company, do not reach out. A weak hook is worse than no outreach.

---

### Step 3 — Determine the Angle

The signal is the reason you're reaching out. The angle is the insight or value you bring to the conversation. These are different things.

**Map signal type to angle:**

| Signal | Angle |
|--------|-------|
| Funding | They have budget and a mandate to move fast. Connect your solution to what they said they'd do with the money. |
| New hire | The new hire likely has a fresh mandate. Position yourself as a tool that helps them succeed in their new role early. |
| Hiring spree in a relevant team | They're scaling something. Identify the friction that comes with that scale and address it. |
| Website visit | They already know you exist. Remove friction, don't re-introduce yourself. Reference the specific area they looked at if possible. |
| Job change (contact moved) | Congratulate without being hollow. Reference what you achieved together or what you know about their situation. |
| Intent data / review site | They're evaluating. Be direct about it. Don't pretend you don't know. |

**Angle quality test** — finish this sentence honestly:

> *"I'm reaching out because [signal], which tells me you might be dealing with [specific problem], and we help with that specifically by [specific capability]."*

If the sentence feels forced or vague, rethink the angle.

---

### Step 4 — Write the Outreach

**Principles (channel-agnostic):**
- Lead with the signal, not with yourself
- One idea per message. No feature lists, no company overviews
- Make the ask small and specific (a reply, a quick call, a reaction — not "let me know if you want to chat")
- Subject lines for email: specific, not clever. Reflect the actual content
- LinkedIn messages: shorter than email. 3–5 sentences max
- Sequence length: 2–3 touches max per signal. If they don't respond, the signal wasn't strong enough — find a new one before reaching out again

**Message structure (adapt to channel):**

```Signal hook — what you noticed and why it matters (1 sentence)

Connection — why that's relevant to what you do (1–2 sentences)

Specific ask — one clear, low-friction next step (1 sentence)
```

**Personalization check before sending:**
- Does this message work if you remove the company name and contact name? If yes, it's not personalized enough.
- Would the recipient feel like you did your homework? If not, do more research or don't send.

---

### Step 5 — Sequence Logic

**Single-signal, single contact:**

| Touch | Purpose | Timing |
|-------|---------|--------|
| Touch 1 | Signal-driven message | Day 0–1 |
| Touch 2 | Value-add follow-up — share something relevant (article, insight, case study). Don't just bump. | Day 5–7 |
| Touch 3 | Break-up or pivot — acknowledge they're busy, offer a different framing or ask if it's not a priority | Day 12–14 |

**Multi-signal or high-priority account:**
- If multiple signals fire on the same account within 30 days, treat it as a high-priority account and consider multi-threaded outreach (different contacts, different angles)
- Do not send the same message to multiple contacts at the same company

**After 3 touches with no response:**
- Stop. Archive the sequence.
- Set a reminder to revisit if a new signal fires.
- Do not add them to a generic nurture without a fresh reason.

---

### Step 6 — Log and Learn

After outreach is sent, record the following:
- Which signal triggered it
- What angle was used
- Channel and sequence used
- Outcome (reply, meeting, no response, unsubscribe)

Over time, this data reveals which signals convert for your specific ICP and which are noise. Prune signals that consistently produce no replies after 20+ attempts.

**In Swan:** This is logged automatically. Swan tracks signal source, outreach angle, sequence performance, and reply rates natively — no manual recording required. Use Swan's analytics to identify which signals convert and which are noise across your full outbound motion.

**In Claude (claude.ai, Claude Code, Claude Cowork):** Claude does not retain memory across sessions. Log these outcomes in your CRM, a spreadsheet, or your sequencing tool manually. Treat this as a recurring calibration step — review monthly and update the skill's signal tier list based on what's actually converting.

---

## Quick Reference — Signal-to-Action Cheatsheet

| Signal | Tier | Angle | Channel | Timing |
|--------|------|-------|---------|--------|
| Pricing page visit | 1 | Remove friction, they already know you | Email or DM | Same day |
| Funding announced | 2 | Connect to stated use of funds | Email | Within 48h |
| ICP hire made | 2 | Help the new hire win early | LinkedIn first | Within 72h |
| Contact changed jobs | 2 | Build on prior relationship | LinkedIn + Email | Within 48h |
| Hiring surge | 3 | Scale-related pain | Email | Within 1 week |
| Content engagement | 3 | Extend the conversation they started | LinkedIn | Within 1 week |

---

## Relationship to Other Skills

gtm-signal-based-outbound →  reactive outreach triggered by a specific signal
gtm-outreach-strategy     →  planned outreach campaigns (not signal-triggered)
gtm-account-research      →  deeper research if the signal comes from a high-priority account
gtm-qualification-scoring →  confirm the account is worth acting on before building the sequence
