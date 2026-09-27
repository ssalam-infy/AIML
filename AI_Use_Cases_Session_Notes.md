# Agentic AI for Automotive Enterprise IT: Session Notes

**Prepared for:** Sailaja Banu, IT Product Owner
**Date:** 27 September 2026
**Scope:** Everything discussed in this session, from AI use cases for an automotive company's internal IT (Mercedes-Benz as the reference) to a working Deck Builder prototype.

---

## Contents

1. [Trending agentic AI use cases in automotive enterprise IT](#1-trending-agentic-ai-use-cases-in-automotive-enterprise-it)
2. [Confluence as Markdown: compliance and governance with agentic AI](#2-confluence-as-markdown-compliance-and-governance-with-agentic-ai)
3. [Growing as an AI Product Owner: finding use cases and writing AI stories](#3-growing-as-an-ai-product-owner)
4. [AI knowledge assistant for Confluence (RAG)](#4-ai-knowledge-assistant-for-confluence-rag)
5. [Agentic live search: no index, the user's own permissions](#5-agentic-live-search-no-index-the-users-own-permissions)
6. [AI Deck Builder for delivery managers and scrum masters](#6-ai-deck-builder-for-delivery-managers-and-scrum-masters)
7. [Deck Builder prototype: what was built](#7-deck-builder-prototype-what-was-built)
8. [Sources](#8-sources)

---

## 1. Trending agentic AI use cases in automotive enterprise IT

### 1.1 Market context (2026)

- **From chatbots to agents working inside real processes.** A Databricks 2026 report found that industrial companies have moved past pilots and chatbots toward agentic systems that can reason, plan and act within business processes. It also saw a sharp rise in multi-agent solutions in manufacturing and automotive, and more focus on governance and agent evaluation.
- **Mercedes-Benz as the reference case:**
  - **March 2026:** began rolling out Microsoft 365 Copilot to all employees in administrative and production-related areas worldwide. The company says the use of AI agents will keep expanding and become more deeply embedded in core business processes.
  - **May 2026:** partnered with n8n on a global platform that lets employees design and deploy AI-powered workflows across R&D, production, sales, financial services, HR and IT. More than 1,500 people took part in a company-wide hackathon, and the best use cases are now being implemented.
  - **SAP and mainframe:** migrating its SAP landscape to AWS for RISE with SAP, and using agentic AI to speed up mainframe migration. Its large development hub in India increasingly uses AI-supported developer tools.
  - **Process intelligence (Celonis):** AI copilots forecast order-to-delivery timelines and optimise sequencing, process intelligence finds bottlenecks in service-parts logistics, and AI-driven anomaly detection catches quality deviations before they affect production.
  - **Mercedes-Benz Korea (Databricks):** building persona-based AI agents on a shared semantic layer, aiming for AI answers that match existing Power BI reports 100%.

**Consultant takeaway:** the foundation (copilots, an automation layer, cloud ERP) is in place. The value now comes from **domain-specific agents that take action across SAP, MES, PLM, CRM and ITSM**, not only answer questions.

### 1.2 Use case catalogue by function

#### A. Software engineering and QA (the IT organisation itself)

| Agent | What it does | Systems touched | KPI |
|---|---|---|---|
| Legacy modernisation agent | Reads COBOL/mainframe or old ABAP, documents business rules, proposes a target design, generates code and tests | Mainframe, SAP, Git | Migration cost and time, defect leakage |
| Requirement-to-test agent | Turns user stories and specs into test cases, test data and automation scripts; keeps traceability | Jira, ALM/Polarion, Xray | Test design effort, coverage |
| Test triage agent | Groups failures from nightly runs, separates flaky tests from real bugs, drafts defect tickets with logs attached | CI/CD, Jenkins, Jira | Triage hours, MTTR |
| Code review and compliance agent | Checks PRs against coding standards, security rules and licence policies | GitHub/GitLab, SonarQube | Review cycle time |
| Release readiness agent | Pulls test results, open defects and change risk into a go/no-go summary | ALM, ServiceNow Change | Failed changes |

For vehicle software, agents can generate and evaluate edge-case scenarios that scripted tests miss, cluster anomalies across large log volumes to find root causes sooner, and run checks aligned to ISO 26262, SOTIF and internal safety requirements.

#### B. Enterprise IT operations (ITSM / AIOps)

- **L1/L2 service desk agent:** resolves password resets, access requests and software installs end to end in ServiceNow, and escalates the rest with a diagnosis attached.
- **Incident commander agent:** correlates alerts, finds recent changes that could be the cause, suggests a rollback, and drafts the post-incident report.
- **Access governance agent:** runs quarterly access reviews, flags segregation-of-duties conflicts in SAP, and prepares audit evidence.
- **Cloud FinOps agent:** finds idle or over-provisioned resources and raises right-sizing tickets.

#### C. Procurement and supply chain

- **Supplier risk sentinel:** watches news, financial signals and delivery performance, and warns about at-risk suppliers of critical parts such as semiconductors or batteries.
- **Shortage resolution agent:** checks alternative suppliers, stock at other plants and the impact on the build plan, then proposes options to the buyer.
- **Contract and RFQ agent:** compares supplier quotes, checks terms against policy, and drafts negotiation points.
- **Order-to-delivery agent:** moves from forecasting to acting, re-sequencing and notifying, with human approval.

#### D. Manufacturing and quality

- **Quality deviation agent:** after anomaly detection flags a deviation, opens the 8D report, pulls similar past cases, and routes the issue to the right engineer.
- **Maintenance planning agent:** combines sensor data, maintenance history and the production schedule to plan downtime with the least disruption.
- **Shift handover agent:** summarises open issues, line stoppages and quality holds for the next shift.

#### E. R&D and engineering

- **Engineering knowledge agent:** searches PLM, specs, past test reports and regulations (homologation, UNECE R155/R156) and answers with sources.
- **Requirements consistency agent:** finds conflicts and gaps across thousands of requirements before they become defects.
- **Warranty and field-issue agent:** links warranty claims, workshop reports and vehicle telemetry to spot emerging problems early.

#### F. Sales, aftersales and dealer network

- **Dealer support agent:** answers dealer questions about orders, allocations, campaigns and technical bulletins.
- **Service status agent:** "Where is my car?" is a major driver of service calls. Agents can combine vehicle data, service schedules, parts availability and dealer systems to give real-time updates and notify customers of changes proactively.
- **Workshop diagnostic assistant:** guides technicians through fault diagnosis using repair manuals and past fixes.

#### G. Finance, HR and corporate functions

- **Invoice exception agent:** handles three-way-match failures in SAP by checking the PO, the goods receipt and the supplier, then resolves or routes the invoice.
- **Financial close agent:** runs reconciliations, explains variances and drafts commentary.
- **Self-service analytics agent:** answers KPI questions from a governed semantic layer (the Mercedes-Benz Korea pattern).
- **HR and policy agent:** handles onboarding, answers multilingual policy questions, and routes leave and travel requests.

### 1.3 Reference architecture

1. **Experience layer:** Teams, Copilot, dealer portals
2. **Orchestration layer:** multi-agent frameworks (LangGraph, n8n, Copilot Studio), with a supervisor agent routing work to specialist agents
3. **Tool layer:** MCP servers or APIs wrapping SAP, ServiceNow, Jira, PLM and MES, with read versus write permissions
4. **Knowledge layer:** RAG over documents plus a governed semantic layer for KPIs
5. **Trust layer:** human-in-the-loop approval for write actions, audit logs, evaluation suites, prompt-injection defences, EU AI Act and GDPR compliance

### 1.4 How to prioritise

Score each use case on **business value, data readiness, risk and time to value**. Start with internal, high-volume, reversible processes: test triage, IT service desk, invoice exceptions and engineering knowledge search. Move to safety-relevant or customer-facing automation only once evaluation and governance have proven themselves.

Given a testing background, section A is the strongest angle. Requirement-to-test generation, failure triage and release readiness show both domain depth and agentic design skills.

---

## 2. Confluence as Markdown: compliance and governance with agentic AI

**The VP's direction:** all Confluence pages should act as `.md` files, and agentic AI should be used to build solutions for the compliance and governance process.

**Why it works:** once pages are Markdown (ideally in Git), documentation becomes **compliance-as-code**. Agents can read it, diff it, test it, and propose changes through pull requests with a full audit trail.

### 2.1 Foundation: machine-readable pages

Each page becomes `.md` with a YAML frontmatter header:

```yaml
---
id: SEC-POL-014
title: Cloud Data Residency Policy
owner: jane.doe@company.com
classification: internal
status: approved
version: 3.2
last_reviewed: 2026-06-10
next_review: 2026-12-10
frameworks: [TISAX-5.2.1, ISO27001-A.5.23, GDPR-Art44]
applies_to: [cloud, data-platform]
supersedes: SEC-POL-009
---
```

Store the pages in Git, make every change a pull request, and optionally publish back to Confluence for readers. That gives versioning, approvals and diffs for free.

### 2.2 Eleven ideas to build

1. **Policy CI (automated tests for documents):** every PR checks the structure against templates, enforces language rules ("shall" versus "should"), detects contradictions between policies, and flags broken links or superseded references.
2. **Regulation change radar:** watches TISAX, ISO 27001, UNECE R155/R156, ISO 26262, ASPICE, GDPR and the EU AI Act. On a change, it finds affected pages through the frontmatter and opens a draft PR with an impact summary.
3. **Policy-versus-reality drift detector:** compares what the docs say with what systems actually do (branch protection, cloud regions, access review dates) and produces a drift report with evidence. *This is the most impressive demo.*
4. **Audit readiness and evidence-pack agent:** assembles evidence by control ID (policy versions, Git approval history, Jira tickets, test reports, training records) and lists controls with no evidence.
5. **Mock auditor agent:** one agent plays a strict TISAX or ASPICE auditor and writes findings; a second drafts the remediations.
6. **End-to-end traceability agent (ASPICE / ISO 26262):** walks requirement → design → implementation → test → evidence, and flags orphaned or untested requirements.
7. **"Ask the Policy" assistant:** answers practical questions with the exact policy section, version and owner. It escalates when unsure and logs questions to reveal unclear policies.
8. **Documentation hygiene agent:** finds overdue reviews, orphaned owners and duplicates, nudges owners, and proposes archiving.
9. **AI governance registry (EU AI Act ready):** each AI use case gets a `.md` record. The agent pre-classifies risk, generates a model card and risk assessment, and blocks deployment until the record is approved.
10. **Exceptions and waiver tracker:** waivers become records with expiry dates and compensating controls, with reminders and trend reports.
11. **Role-based policy training:** short role-specific quizzes generated from the relevant policies, with attestations recorded as audit evidence.

### 2.3 Architecture

1. **Ingestion:** Confluence API export → Markdown with frontmatter → Git
2. **Knowledge layer:** vector index plus a knowledge graph of policies, controls, systems and owners
3. **Tool layer:** MCP servers or APIs for Git, Jira, Confluence, IAM, cloud config and CI/CD
4. **Agent layer:** a supervisor agent routing to specialists (radar, drift, audit, Q&A, hygiene)
5. **Control layer:** agents only propose changes through PRs; humans approve and merge; everything is logged

### 2.4 Risks to raise with the VP

- **Conversion loss:** macros, Jira embeds, diagrams and attachments don't convert cleanly
- **Permissions:** restricted spaces must stay restricted for agents too
- **Source of truth:** decide whether Git or Confluence is the master; two-way sync gets messy
- **Accountability:** the agent never approves policy; a named human owner always does

### 2.5 Suggested MVP (6–8 weeks)

One framework (TISAX or ISO 27001) and about 50 key pages. Build the conversion pipeline with frontmatter, Policy CI, and the drift detector for 3–5 controls. The demo story: *"Here are 12 gaps we found automatically that would have been audit findings."*

---

## 3. Growing as an AI Product Owner

### 3.1 Reframing the challenge

Peers with AI/ML degrees bring ideas about **how** to build AI. The industry's biggest problem is **what** to build. MIT's NANDA research found that roughly 95% of enterprise generative AI pilots delivered no measurable P&L impact. As one analysis puts it, AI has made building cheaper but has not made judgment cheaper. Choosing the problem, the user, the value and the proof of success is the Product Owner's job.

### 3.2 Trending AI topics to know

| Topic | Plain meaning |
|---|---|
| Agentic AI | AI that plans and takes actions across systems, not only chats |
| Multi-agent systems | Specialist agents coordinated by a supervisor agent |
| RAG | AI answers from company documents, with citations |
| MCP / tool integration | Standard way to plug AI into Jira, Confluence, SAP, Git |
| AI evals | Systematic testing of AI quality: accuracy, hallucination rate, safety |
| AI governance | EU AI Act, risk classification, audit trails, human oversight |
| AI-assisted SDLC | AI for coding, testing, review, legacy modernisation |
| Knowledge-as-code | Docs in Markdown so agents can read and change them |
| Small / on-device models | Cheaper, private models for specific tasks |
| AI FinOps | Managing token cost and latency at scale |

### 3.3 The base: which tool fits which problem

- **Clear fixed rules** → no AI; use automation or a rules engine
- **Predict a number or category from history** → classic ML
- **Understand or produce unstructured content** (emails, docs, logs, specs, code) → generative AI
- **Multi-step work across systems that needs judgment** → agentic AI

**Strong at:** reading and summarising, classifying, drafting, finding patterns, translating between formats.
**Weak at:** guaranteed accuracy, exact arithmetic without tools, unknown facts, decisions where one error is catastrophic.

**Rule of thumb:** a good AI use case is one where being right 90% of the time, with a human checking, is still very valuable.

### 3.4 How to find use cases

Hunt for **pain**, then check whether AI fits. Signals:

1. High-volume, repetitive work
2. Reading-heavy work (logs, docs, specs, tickets)
3. Copy-paste across systems
4. Expert bottlenecks
5. "Search and assemble" tasks (audit evidence, release notes, status reports)
6. Judgment with patterns (triage, prioritisation, routing)

**Questions to ask stakeholders:**
- "What task do you do every week that you hate?"
- "Where do you spend time searching instead of deciding?"
- "What would you do with a smart junior assistant for 2 hours a day?"
- "Where do errors or delays usually come from?"
- "What do new joiners struggle to learn?"

Also sit with users and watch them work for an hour.

### 3.5 Use-case canvas (one page per idea)

1. **Problem:** who, how often, cost today
2. **Current process:** step by step
3. **AI role:** assist, augment or automate, and which step
4. **Data and access:** exists? clean? allowed?
5. **Risk:** impact when wrong, and who catches it
6. **Success metric:** baseline and target
7. **Why AI?** Could simple automation do it?

Score each idea on **Value × Feasibility ÷ Risk**.

### 3.6 Writing AI user stories

AI stories need **quality thresholds**, a **human-in-the-loop** step, **fallback behaviour** and a **feedback loop**.

> **As a** QA engineer, **I want** failed nightly test runs to be automatically grouped and analysed, **so that** I spend my morning fixing real defects instead of sorting through 300 failures.
>
> **Acceptance criteria:**
> - Groups failures by likely root cause; ≥85% of groupings match QA lead judgment on a 100-case test set
> - Labels each group *product defect*, *environment issue* or *flaky test*, with a confidence score
> - Below 70% confidence, marks it "needs human review"
> - Drafts a Jira defect with logs attached; a human approves before creation
> - One-click correction, with corrections logged for improvement
> - Cost per nightly run under an agreed budget; results ready by 8 AM
>
> **Success metric:** triage effort from about 3 hours to under 30 minutes per day

**Hidden advantage:** those acceptance criteria are really **AI evals**. A testing background is exactly the skill for defining "good enough to ship".

### 3.7 Knowledge checklist

LLM basics (tokens, context window, temperature, hallucinations) · prompting vs RAG vs fine-tuning · embeddings and vector search · agents (tools, planning, memory, guardrails) · evals (golden sets, LLM-as-judge, precision/recall) · cost and latency · privacy and security (PII, prompt injection, access control) · governance (EU AI Act risk tiers) · build versus buy.

### 3.8 90-day plan

- **Days 1–30, fluency:** use AI daily for real work; learn one concept a week and explain it to a colleague; keep a pain log.
- **Days 31–60, practice:** write canvases for the top 5 pain points; build one tiny prototype (n8n, Copilot Studio or a simple RAG demo); pair with an MTech peer (you bring the problem, they bring the approach).
- **Days 61–90, deliver:** pitch one use case with a canvas, stories and an eval plan; run a small pilot; share the results in a demo or write-up.
- **Weekly habits:** 30 minutes of reading, one use case written up, one user conversation.

### 3.9 Recommended resources

- *AI for Everyone*, Andrew Ng (Coursera)
- DeepLearning.AI short courses (RAG, agents, evals)
- *Building Effective Agents*, Anthropic engineering blog
- *AI Engineering*, Chip Huyen
- Google *People + AI Guidebook*

---

## 4. AI knowledge assistant for Confluence (RAG)

**Goal:** a user asks "How do I set up SonarQube for a new repo?" and gets a direct answer, source links and a confidence indicator, instead of a list of keyword matches.

### 4.1 How RAG works

1. **Index:** pages are chunked, embedded and stored with URL, space, owner, date and permissions
2. **Retrieve:** find the most relevant chunks by meaning
3. **Filter:** keep only pages the user can see
4. **Generate:** answer only from those chunks, with citations
5. **Display:** answer, sources, confidence and related pages

### 4.2 Delivery options

1. **Check what's already licensed:** Atlassian Rovo search respects existing permissions and gives summarised answers with sources. It is included with paid Atlassian Cloud plans but metered in credits. Data Center customers can use Rovo connectors that sync content to the cloud.
2. **Enterprise search platforms:** M365 Copilot with a Confluence connector, or Glean.
3. **Build your own RAG:** for custom confidence scoring, data residency or deep integration.

Present all three with a build-versus-buy comparison.

### 4.3 Confidence scoring done properly

Don't ask the LLM how confident it is. Calculate confidence from signals:

| Signal | Checks |
|---|---|
| Retrieval strength | Similarity and reranker scores |
| Source agreement | Do pages agree or contradict? |
| Grounding check | Is every sentence supported by a source? |
| Page quality | Approved vs draft, review date, owner |
| Coverage | Whole question answered, or only part? |

Show **High / Medium / Low with a reason**, not a false-precision percentage. When confidence is low, say so and point to the closest pages or a team.

### 4.4 Pros and cons

**Pros:** big time savings · search by meaning · fewer repeat questions to experts · faster onboarding · trust through sources · reveals documentation gaps · a foundation for the compliance agents.

**Cons and mitigations:**

| Risk | Mitigation |
|---|---|
| Outdated or conflicting pages | Rank approved and fresh pages higher; flag conflicts; clean up docs |
| Permission leaks | Enforce permissions at retrieval time; test explicitly |
| Hallucination | Answer only from sources; grounding check; "not found" when needed |
| Over-trust | Always show sources; add caution for security or production steps |
| Diagrams and attachments | Extract text; add alt text |
| Stale index | Incremental re-indexing |
| Cost | Caching, monitoring, budgets |
| Adoption | Put it in Teams, Confluence or the IDE |

### 4.5 Pilot

Pick 1–2 spaces (QA and DevOps) with about 100 pages, and a test set of 50 real questions with known answers. Measure accuracy, whether the correct source appears, time saved and user ratings.

---

## 5. Agentic live search: no index, the user's own permissions

**The concern raised:** with many processes, keeping a RAG index fresh and permission-synced is hard and risky. (Note: RAG doesn't need links collected by hand, because an indexer crawls the spaces through the API. The freshness and permission concerns are still valid.)

**The alternative:** an AI agent searches Confluence **live, at question time, signed in as the user**, the way an experienced colleague would.

### 5.1 How it works

1. **User signs in:** the agent acts on the user's behalf (SSO/OAuth), never as a super-admin
2. **Plans the search:** generates synonyms (SonarQube, Sonar, quality gate, static code analysis)
3. **Searches live:** Confluence returns only pages this user may see
4. **Reads and traces:** opens pages and follows links, parents, children and labels
5. **Decides if it has enough:** refines and repeats, within a step limit (for example 5 searches or 10 pages)
6. **Answers with a trace:**

> **Answer:** Request a SonarQube project through the DevOps portal, add `sonar-project.properties` to the repo root, and configure the pipeline step using the shared template. [1][2]
> **How I found this:** "SonarQube onboarding" → *Code Quality Standards* → *SonarQube Project Onboarding* (section 3) → *CI Template Guide*
> **Confidence: High.** Two approved pages agree; updated 2 months ago.

### 5.2 Why permissions are safe

Every call uses the user's own token, so the agent cannot see what the user can't see, and no content is copied elsewhere.

On Atlassian Cloud, the **Atlassian Rovo MCP Server** already provides this:
- secure, real-time access for AI tools to Jira and Confluence via OAuth 2.1 or API tokens
- access only to data the user already has permission to view, respecting space-level roles
- every tool call recorded in the organisation's audit log
- admin controls: revoke app access, domain allowlists, IP allowlisting

On Data Center, use the REST API with each user's personal access token or OAuth.

### 5.3 Architecture

Front end (Teams, Confluence sidebar, web page) → agent (LLM with search/read/trace/cite instructions) → tools (Confluence search and read page only, read-only scopes) → guardrails (step limits, mandatory citations, "not found" over guessing, logging).

### 5.4 Comparison

| | Classic RAG | Agentic live search | Hybrid |
|---|---|---|---|
| Setup effort | High | Low | Medium |
| Freshness | Last re-index | Always current | Current |
| Permissions | Copied and synced (risky) | Native | Native |
| Speed | 2–5 s | 10–40 s | Medium |
| Cost per question | Low | Higher | Medium |
| Vague questions | Good | Depends on search terms | Best |
| Traceability | Limited | Excellent | Good |

**Hybrid** = Rovo's semantic search as the agent's search tool, plus live tracing and reading. No index for your team to maintain.

### 5.5 Pros and cons

**Pros:** no index · always current · permissions enforced by Confluence · transparent trace · handles multi-page processes · quick to prototype.

**Cons and mitigations:** slower (show progress, cache answers) · higher cost (step limits, cheaper model for planning) · keyword search can miss pages (synonyms or Rovo semantic search) · API rate limits (per-user limits, caching) · poor titles and labels hurt results (the Markdown/metadata plan helps) · agent acts with user rights (keep it strictly read-only, least privilege).

### 5.6 Proof of concept

1. Ask the Atlassian admin whether the Rovo MCP server is enabled, and which authentication is allowed
2. Connect it to an approved AI assistant with read-only Confluence scopes
3. Prepare 30 real questions with known answers (SonarQube, Xray, CI, release process)
4. **Test with two users with different access levels** to prove restricted pages never appear for the user without access
5. Measure accuracy, time compared with manual search, and user feedback

---

## 6. AI Deck Builder for delivery managers and scrum masters

**Problem:** DMs and scrum masters lack Copilot skills or Copilot Studio build permission, depend on tech support, spend hours on decks, and the decks often still lack a clear message.

**Two layers:** tooling (visible) and storytelling (hidden). Fix both, or you just produce bad slides faster.

### 6.1 User journey

1. **Pick the deck type:** Sprint Review, Steering Committee, Monthly Status, Release Readiness, Escalation, Kickoff, Quarterly Review
2. **Answer 4–5 guided questions:** audience; the one message; the decision needed; status and why; anything sensitive
3. **Data collected automatically:** Jira, Confluence (RAID log, release plan), uploaded Excel, all with the user's own access
4. **Storyline approval before building:** a one-page outline the user can adjust
5. **Build:** editable `.pptx` in the corporate template, with charts and speaker notes
6. **Reviewer agent:** checks the deck against a rubric and gives 2–3 suggestions

### 6.2 Storytelling built into the templates

| Weak title | Impactful title |
|---|---|
| Sprint 14 Velocity | Velocity stabilised at 42 points; November release on track |
| Risks | Two supplier risks could delay testing by 2 weeks; decision needed |
| Defect Status | Critical defects down 60% since the new test automation |

- **Answer first:** the executive summary on slide 2
- **Steering structure:** summary (status, message, ask) → progress → value → risks → decisions → next steps → appendix

### 6.3 Delivery options

- **A. Quick win (1–2 weeks):** prompt and template pack for existing AI chat tools
- **B. Central agent in Teams (4–6 weeks):** built once by a team with Copilot Studio maker rights; DMs only need permission to *use* it (confirm licensing with the M365 admin)
- **C. Custom app (6–10 weeks):** approved LLM, Jira/Confluence APIs, python-pptx or pptxgenjs, corporate template; full control and no Copilot licensing dependency

Roadmap: **A now, then B or C as the product.**

### 6.4 Pros and cons

**Pros:** hours become a short guided session · no prompt skill or build permission · consistent, on-brand decks · data straight from Jira and Confluence · clearer asks for leadership · fewer tech-support requests.

**Cons and mitigations:** generic content (guided questions, outline approval) · wrong numbers (source and "as of" on charts, user confirms) · confidential data (approved tools, user permissions) · over-reliance (the DM owns the message) · template drift (central template library owned by the PMO).

### 6.5 Pitch

**Problem statement:** "Delivery managers and scrum masters spend hours per deck, depend on tech support, and still produce decks that don't drive decisions."

**Metrics:** time per deck (for example 3 hours down to 45 minutes) · support requests · DM satisfaction · "Was the ask clear?" feedback after steering meetings.

> **As a** delivery manager, **I want** to generate a steering committee deck from my Jira project by answering a few guided questions, **so that** I can present a clear status and decision request without spending hours formatting slides.
>
> **Acceptance criteria:** at least 5 deck types with predefined structures · pulls sprint, defect and risk data with the user's own permissions · editable outline approval before generation · editable .pptx in the corporate template with action titles and speaker notes · every chart shows its source and "as of" date · the reviewer flags slides without a clear message and confirms a "decisions needed" slide · a standard 8–10 slide deck in under 3 minutes

---

## 7. Deck Builder prototype: what was built

A working Node.js prototype (single script, one dependency: `pptxgenjs`) that turns a Jira CSV export plus a short deck brief into a 10-slide steering committee PowerPoint.

### 7.1 Files

| File | Purpose |
|---|---|
| `deck_builder.js` | The tool: interview, outline, build, reviewer |
| `sample_data/deck_brief.json` | The DM's answers plus sprint calendar and sensitive terms |
| `sample_data/jira_export.csv` | Fictional Jira export: 84 stories over Sprints 9–14 (with carry-over), 87 defects, 4 risks |
| `sample_data/milestones.csv` | 6 milestones with plan, forecast and actual dates |
| `output/ASB_Steering_Committee_2026-09-29.pptx` | Generated sample deck |
| `output/..._review.md`, `output/outline.md` | Review report and storyline |
| `README.md`, `package.json` | How to run and adapt it |

### 7.2 Commands

```bash
npm install pptxgenjs
node deck_builder.js interview --out my_brief.json   # guided questions, no prompt writing
node deck_builder.js outline                         # storyline for approval
node deck_builder.js build                           # deck + quality review
```

Options: `--brief`, `--jira`, `--milestones`, `--out`.

### 7.3 The 10 slides

1. Title with a RAG "status light"
2. Executive summary: status and reason, 3 key numbers (67% of scope done, forecast dev-complete 6 Nov, 2 open critical defects), "What we need from you"
3. Progress against plan: milestone timeline with a "Today" marker, delivery forecast, what is slipping and why
4. Delivery performance: committed vs completed per sprint (editable chart), 93% reliability, ~41 points per sprint, 110 points remaining
5. Value delivered: epic progress bars and business outcomes
6. Quality: found vs fixed per sprint, open critical trend (7 → 2), open defects by priority
7. Risks and issues: RAID table and blocked items
8. Decisions needed: why, options, recommendation, owner, date
9. Next steps: dated actions with owners, upcoming milestones
10. Appendix: data sources and how every number is calculated

### 7.4 Key design choices

- **Action titles computed from data:** numbers are never written by AI
- **Answer first:** the executive summary is always slide 2, with the ask
- **Sources and "as of" dates** on every slide
- **Sensitive terms masked** everywhere (the sample hides the payment vendor's name)
- **Adaptable:** `JIRA_COLUMNS`, `DONE_STATUSES`, `PRIORITY_GROUPS`, `THEME` and `FONTS` at the top of the script; `slide_order` in the brief

### 7.5 Quality reviewer rubric

- Executive summary on slide 2, with status and the ask
- Action titles, not topic labels
- RAG status consistent with the data
- A clear ask when AMBER or RED; decisions have a recommendation, owner and date
- Risks have owners and mitigations
- Outcomes are measurable; next steps have owners and dates
- Data at most 7 days old at meeting time
- Main story at most 9 slides

Warnings are also copied into each slide's speaker notes as a **PREP CHECK**.

### 7.6 Test results

- **Sample deck:** 1 FIX (a risk with no mitigation) and 1 WARN (the vague outcome "Improved dealer experience"). Both were planted in the sample data on purpose.
- **Weak brief test:** the reviewer flagged the topic-label title "Project status", a GREEN status contradicted by slipping milestones, an AMBER status with no ask, and missing next steps and outcomes.
- **Checks:** the file validation passed, every slide was inspected visually, and the zip was re-run from a fresh copy.

### 7.7 Limitations

- Sample data is fictional
- Runs offline on exported files; no live Jira connection and no AI model yet
- Only the Steering Committee deck type is implemented; the others show as "coming next"
- Corporate colours, fonts and Jira field names need configuring

### 7.8 Where an LLM fits next

1. Run the guided conversation in Teams
2. Polish titles and notes for tone. `numbersPreserved()` rejects any rewrite that adds a number not in the computed original.
3. Summarise Confluence pages (release plan, RAID log) into the brief

### 7.9 Suggested VP demo

Run the interview live → show the outline → build the deck → open the review report → re-run with a weak brief so the room sees the reviewer push back.

**Next step:** swap in the company template and a real, anonymised Jira export from one project.

---

## 8. Sources

**Mercedes-Benz and automotive AI**
- [Mercedes-Benz: AI at the digital workplace](https://group.mercedes-benz.com/technology/digitalisation/artificial-intelligence/ai-digital-workplace.html)
- [Mercedes-Benz: global n8n rollout](https://group.mercedes-benz.com/technology/digitalisation/artificial-intelligence/ai-automation.html)
- [AWS case study: Mercedes-Benz, RISE with SAP and agentic AI](https://aws.amazon.com/solutions/case-studies/mercedes-benz-transform-case-study/)
- [PEX Network: Mercedes-Benz AI-driven transformation](https://www.processexcellencenetwork.com/ai/news/mercedes-benz-accelerates-ai-driven-transformation)
- [StartupHub.ai: Mercedes-Benz Korea's AI agents](https://www.startuphub.ai/ai-news/technology/2026/mercedes-benz-korea-s-ai-agents)
- [Supply Chain Movement: AI agents in manufacturing and automotive](https://www.supplychainmovement.com/ai-agents-are-gaining-ground-in-manufacturing-and-automotive/)
- [N-iX: Agentic AI in automotive](https://www.n-ix.com/agentic-ai-in-automotive/)
- [Concentrix: Agentic AI use cases in automotive](https://www.concentrix.com/insights/blog/top-5-agentic-ai-use-cases-in-automotive-industry/)

**Product management and AI**
- [Metis Strategy: Product management in 2026](https://www.metisstrategy.com/product-management-ai-value-measurement/)
- [Userpilot: Product management trends 2026](https://userpilot.com/blog/product-management-trends/)
- [Field Guide: How AI is changing product management in 2026](https://muhammadusmanmustafa.info/blog/how-ai-is-changing-product-management-2026)

**Atlassian Rovo and MCP**
- [Atlassian: Rovo Search improvements](https://www.atlassian.com/blog/rovo/rovo-search-improvements)
- [Atlassian: Rovo search in Jira launch notes](https://jirareleases.atlassian.com/announcements/rovo-search-is-now-in-jira)
- [Atlassian: Rovo overview](https://www.atlassian.com/software/rovo)
- [Slite: Atlassian Rovo AI review](https://slite.com/learn/atlassian-rovo-ai-review)
- [The AI Agent Index: Atlassian Rovo review](https://theaiagentindex.com/agents/atlassian-rovo)
- [GitHub: Atlassian MCP Server](https://github.com/atlassian/atlassian-mcp-server)
- [GitHub MCP registry: Atlassian Rovo MCP Server](https://github.com/mcp/com.atlassian/atlassian-mcp-server)
- [Atlassian Support: Configure OAuth 2.1 for the Rovo MCP server](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/configuring-oauth-2-1/)
- [Microsoft Tech Community: Rovo MCP server in Azure SRE Agent](https://techcommunity.microsoft.com/blog/appsonazureblog/get-started-with-atlassian-rovo-mcp-server-in-azure-sre-agent/4497122)
