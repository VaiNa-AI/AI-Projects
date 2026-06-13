# Cohort 5
Repository for Agentic AI Bootcamp - Cohort 5

# Windows - Anaconda Prompt
# Mac - Terminal

# Goto Folder which you have script

```
conda create --prefix ./env python=3.12 -y
conda activate ./env 
pip install -r requirements.txt

python main.py```

---

# Assignment.py — Controlled Support Agent (LangGraph)

`Assignment.py` builds a customer-support router as a **LangGraph state machine**: it identifies the customer, classifies the issue (LLM with a keyword fallback), and deterministically routes to one of four paths. Below are answers to the assignment questions, grounded in the code.

### 1. What capability did I give the agent?
The ability to **create and track support tickets** — a controlled side-effect on an external system. This is exposed through the `create_priority_ticket` tool, which generates a `TKT-xxxxx` ID, logs the event, and returns it. Everything else (identifying, classifying, routing) is reasoning that leads up to deciding *whether and how* to use that capability.

### 2. What tool did I create and when should it be used?
The tool is `create_priority_ticket(customer_id, issue_category, priority)`. Per its docstring, it should be used **whenever a support request needs to be tracked and assigned** — billing disputes, technical failures, or anything needing follow-up. It's invoked by three terminal nodes (`technical_path`, `premium_path`, `standard_path`), each passing a different `priority`. The `verify_path` deliberately does **not** call it — an unverified customer shouldn't generate a ticket.

### 3. What state fields did my graph track?
The `SupportState` TypedDict tracks seven fields:

| Field | Purpose |
|---|---|
| `user_message` | the raw input |
| `customer_id` | extracted ID (e.g. `CUST-001`) |
| `customer_tier` | `premium` / `standard` / `unknown` |
| `issue_category` | `billing` / `technical` / `general` |
| `route_taken` | which path executed (for traceability) |
| `ticket_id` | the created ticket, if any |
| `final_response` | the reply shown to the user |

`identify_customer` sets the first two, `classify_issue` sets `issue_category`, and the path node sets the last three.

### 4. What routing decision did my graph make?
A single conditional edge runs `route_request` after classification, with this priority order:

1. **`customer_tier == "unknown"`** → `verify_path` (can't help an unverified user — ask for ID first)
2. else **`issue_category == "technical"`** → `technical_path` (high-priority ticket regardless of tier)
3. else **`premium`** → `premium_path`, otherwise → `standard_path`

So tier-unknown short-circuits everything, technical issues are escalated next, and remaining cases split by tier.

### 5. Why is this more controlled than a simple agent?
A "simple agent" hands the LLM the tools and a loop, and *it* decides what to call, in what order, and when to stop — flexible but opaque and unpredictable. This graph is more controlled because:

- **The control flow is yours, not the LLM's.** Routing is deterministic Python in `route_request`. The same input always takes the same path. The LLM only does the one narrow job it's good at — classification — bounded to three valid labels with a keyword fallback if it misbehaves or is unavailable.
- **Guardrails are structural.** An unknown customer *cannot* reach a ticket-creating node — the graph topology prevents it, not a prompt asking the model nicely.
- **It's traceable and explainable.** `route_taken`, structured JSON logs, and the recorded state mean every decision is auditable after the fact.

In short: it trades the open-ended autonomy of a tool-calling agent for a **fixed, inspectable state machine** where the LLM is a constrained component rather than the decision-maker.
