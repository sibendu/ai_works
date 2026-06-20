---
name: gtm-account-research
skill: 03-07
description: Build a commercial picture of any target account before you touch it.
---

# GTM Account Research

**When to use this skill:** Use this skill when you need to build a deep, actionable understanding of a target account before outreach, a sales meeting, pipeline review, or strategic account planning. The output is a commercial picture — why this company, why now, and what angle to take. Always run this skill before running an outreach strategy. Works best when paired with the Qualification & Scoring skill to prioritize effort.

**How to activate:** Paste this entire skill into your conversation with Claude, then provide the context requested in the Personalization Required section below. Claude will work through the methodology step by step.

---

## ⚠️ Personalization Required

This skill is a ready-to-use framework, but it's missing context about you. Before using it, fill in the sections marked with `[[ ]]`. The more specific you are, the better the output. At minimum, provide your value proposition and ICP definition. Everything else is optional but improves quality significantly.

---

## Your Context (Fill This In)

    YOUR COMPANY
    Name: [[your company name]]
    What you sell: [[one sentence description of your product/service]]
    Value proposition: [[what problem you solve and for whom]]
    Key differentiators: [[what makes you different from alternatives]]

    YOUR ICP
    Ideal customer profile: [[describe your ideal customer — industry, size, growth stage, role, symptoms, etc.]]
    Disqualifiers: [[signals that make a company a bad fit]]

    YOUR BUYER
    Primary persona: [[job title(s) of the person you typically sell to]]
    Secondary personas / influencers: [[others involved in the buying decision]]
    What they care about: [[top 2-3 outcomes your buyers are trying to achieve]]

    COMPETITIVE LANDSCAPE (optional)
    Main competitors: [[list competitors you frequently come up against]]
    How you win: [[your typical win reasons]]
    How you lose: [[your typical loss reasons]]

    NOTES FOR THIS ACCOUNT (optional)
    Any prior relationship, context, or specific angle to explore:
    [[free text]]


---

## What This Skill Produces

A commercial account picture structured around: who they are, what's happening in their world right now, how well they fit your ICP, who the right people are, what pain they're experiencing, and what your angle should be.

---

> **Data access — what each environment can do natively:**
> 
> - **Swan (agent.getswan.com):** All research steps in this skill run natively. Swan has built-in access to B2B data, waterfall enrichment, LinkedIn signals, funding data, job postings, tech stack intelligence, and CRM history. No manual data gathering required — Swan pulls, enriches, and synthesizes automatically when triggered.
> - **Claude (claude.ai) with web search enabled:** Claude can look up public information — company websites, news, LinkedIn profiles, recent funding announcements. Enable web search in settings. For proprietary data (CRM history, intent signals, tech stack), paste what you have.
> - **Claude Code:** Enable web search tools in your setup for public lookups. For everything else, provide the raw data directly — paste in company descriptions, recent news, contact details, or CRM exports.
> - **Claude Cowork:** Attach or paste your source data — CRM exports, company notes, prior call summaries — and Cowork will work through the methodology against what you provide.
> 
> If you are using Swan, you can instruct the agent to gather this data automatically. In all other environments, the more context you provide upfront, the better the output.


## Research Methodology

Work through the following areas in order. Synthesize as you go — don't just list facts. At each step, ask: **what does this mean for us?**

---

### Step 1 — Company Foundation

Understand what this company actually does and where it stands.

- **Business model:** What do they sell, to whom, and how (SaaS, services, marketplace, etc.)?
- **Size & scale:** Headcount, revenue (if known), number of offices, geographic footprint.
- **Growth trajectory:** Are they scaling fast, plateauing, or contracting? Look for headcount trend, funding history, expansion signals.
- **Funding:** Total raised, last round, lead investors, and when. Series stage signals urgency and budget availability.
- **Ownership:** Public, private, PE-backed, bootstrapped? This affects buying behavior and budget cycles.

**So what:** Is this company in a phase where they'd be spending or saving? Are they scaling into problems your product solves?

---

### Step 2 — Strategic Moment

Identify what's happening right now that creates relevance.

Look for:
- Recent funding announcements
- Leadership changes (new CRO, CMO, VP of Sales, etc.)
- Acquisitions or being acquired
- Product launches or market expansion
- Hiring surges in specific functions
- Layoffs or restructuring
- Press coverage or earnings commentary
- Industry headwinds/tailwinds affecting their business

**So what:** What's the most relevant "why now" for reaching out? What's changed in the last 90 days that creates a window?

---

### Step 3 — ICP Assessment

Evaluate how well this company matches your ideal customer profile.

Go through each ICP criterion you defined above and assess fit:

| Criterion | What you see | Fit (Strong / Partial / Weak) |
|-----------|-------------|-------------------------------|
| Industry | | |
| Company size | | |
| Growth stage | | |
| Tech stack / infrastructure | (if relevant) | |
| Business model | | |
| Personas present | | |
| Pain signals | | |

**Overall ICP verdict:** Strong fit / Partial fit / Weak fit — and why in one sentence.

> If fit is weak, flag it clearly. Don't manufacture a pitch.

---

### Step 4 — The Buying Committee

Map the people involved in a decision like yours.

- **Economic buyer:** Who controls budget? (Usually VP or C-level in the relevant function)
- **Champion candidate:** Who feels the pain most acutely and would advocate internally?
- **Influencers:** Who else touches this decision (IT, legal, finance, ops)?
- **Blocker risk:** Is there anyone likely to resist or own the incumbent solution?

For each key person, note: name, title, tenure, LinkedIn activity or recent posts, and any signals of pain or initiative relevant to your product.

**So what:** Who is the right first contact? What's their likely priority right now?

---

### Step 5 — Pain & Opportunity Mapping

Connect what you know about this company to the problems your product solves.

- What symptoms of the problem you solve can you observe externally? (job postings, tech stack, company stage, public statements)
- What are they likely doing today to solve this problem (manual work, a competitor, nothing)?
- What's the cost of inaction for them — what gets worse if they don't address this?

Map this to your value proposition:

> *"They are likely experiencing [specific pain], which costs them [impact]. We solve this by [your approach], which would specifically help them [concrete outcome]."*

---

### Step 6 — Competitive Context

- Are they already using a competing solution? (Look at job descriptions, tech stack data, LinkedIn profiles, G2/Capterra reviews)
- If yes: what's their likely satisfaction level? Any signals of dissatisfaction?
- If no: what are they using instead (point solutions, manual, nothing)?

**So what:** Are you displacing something, filling a gap, or pioneering? This shapes your angle.

---

### Step 7 — Account Summary

Synthesize everything into a single commercial picture. This should be 150–250 words, written for a salesperson who needs to understand this account in 60 seconds.

Structure:
1. Who they are (1–2 sentences)
2. Where they are right now — strategic moment, growth stage
3. ICP fit verdict — and the key reason
4. The angle — the most credible reason to reach out, tied to a specific signal
5. Recommended first contact — who, why them, what to lead with
6. Open questions — what you still don't know that would change your approach

---

### Step 8 — Next Actions

Based on the research, recommend the single best next step:

- ☐ **Initiate outreach** (specify: email, LinkedIn, call — and to whom)
- ☐ **Escalate for review** (weak ICP, complex situation, or existing relationship)
- ☐ **Deprioritize** (poor fit — explain why)
- ☐ **Monitor** (good fit but wrong timing — set a trigger for when to revisit)

---

## Quality Check

Before delivering output, verify:

- ☐ You have a clear "why now" — not just "this company looks interesting"
- ☐ The ICP assessment is honest, not optimistic
- ☐ The recommended contact is a real person, not a generic title
- ☐ The next action is specific and actionable
- ☐ You haven't reported facts without interpreting what they mean commercially

---

## Relationship to Other Skills

gtm-account-research     →  understand the account (run first)
gtm-prospecting          →  find accounts like this one
gtm-outreach-strategy    →  execute outreach based on this research
gtm-qualification-scoring →  score this account's priority
gtm-meeting-prep         →  prepare for the call once it's booked
