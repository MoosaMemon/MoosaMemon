<h1 align="center">Moosa Memon</h1>

<p align="center">
  <b>AI automation engineer.</b> I build AI systems that survive production.
</p>

<p align="center">
  <a href="https://moosamemon.me"><img alt="Website" src="https://img.shields.io/badge/moosamemon.me-111111?style=flat-square"></a>
  <a href="https://www.linkedin.com/in/moosamemon/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white"></a>
  <a href="https://x.com/moosamemonn"><img alt="X" src="https://img.shields.io/badge/@moosamemonn-111111?style=flat-square&logo=x&logoColor=white"></a>
  <a href="mailto:notmoosamemon@gmail.com"><img alt="Email" src="https://img.shields.io/badge/Email-C14438?style=flat-square&logo=gmail&logoColor=white"></a>
  <a href="https://moosamemon.me/contact/"><img alt="Book a call" src="https://img.shields.io/badge/Book%20a%2020--min%20call-2F6F4E?style=flat-square&logo=caldotcom&logoColor=white"></a>
</p>

---

**AI Automation Engineer at UnitZero** since August 2025 · BS in Artificial Intelligence, FAST · Karachi, working US hours.

I build retrieval pipelines that answer from messy internal documents, agent workflows that do multi-step work without babysitting, and the automation infrastructure that connects both to the tools a business already runs on.

The day job stays private. Everything below I designed and shipped end to end on my own time.

<br>

## Selected systems

> Links go to the case studies rather than the repos — these are private builds, so the write-ups are the public record. Numbers appear only where they were actually measured.

| System | What it is | Measured result |
|---|---|---|
| **[A support agent that asks before it acts](https://moosamemon.me/work/customer-ops-agent/)** | Answers from a knowledge base and takes four real actions — ticket, CRM write, email, booking — every mutating one behind a human approval gate | 95.5% tool-selection accuracy, 100% argument validity, **0% false-action rate** on a 44-case golden set, enforced as a CI gate |
| **[A research agent for the PSX that shows its sources](https://moosamemon.me/work/fintex/)** | Four agents over documents, time-series and live exchange prices, fused into cited answers with an honest confidence score | Router at **20/20 with 0% wrong routes**, up from 13.6 and 32% before the rewrite; every ablation costs 3.4–4.0 points |
| **[Flagging invasive species a year before official detection](https://moosamemon.me/work/beachhead/)** | Fuses citizen-science sightings, climate suitability and introduction pathways into triaged field-survey recommendations | Retrospectively flagged **5 of 7** ground-truth European invasions **12–36 months early**; the other two had no citizen-science record at all |
| **[A price API that explains every rupee](https://moosamemon.me/work/autopricer/)** | A resale-price model wrapped in auth, caching, async batch scoring, drift monitoring and a champion/challenger retraining gate | R² **0.94**, 33% RMSE cut over baseline; Redis cache cut median latency **48% (730 → 380 ms)** at 20 concurrent users, 0 failures |
| **[An agent that can't touch an account it hasn't verified](https://moosamemon.me/work/verify-bridge/)** | Answers from internal docs and acts on customer accounts only after identity verification | Bypass the prompt, bypass n8n, hand-craft the webhook — sensitive routes still return **403** and write a denial to the audit log |
| **[An ops hub where the AI can't certify its own claims](https://moosamemon.me/work/ops-relay/)** | Calls, forwarded emails and notes in; deduplicated, confidence-tagged tasks out, behind a Slack approval gate | A fact is `verified` only if it matches a field the upstream platform actually sent — enforced in code, tested as a property |
| **[Answers from your PDFs, source highlighted on the page](https://moosamemon.me/work/doclens/)** | Hybrid retrieval and reranking, with a side-by-side viewer that highlights the exact cited page | Every answer carries filename, page and chunk; a grounding check declines instead of guessing |
| **[A WhatsApp booking agent that cannot double-book](https://moosamemon.me/work/converse-iq/)** | Answers from the business's own records, books appointments, and routes phone calls into the same agent | Any wrong-date booking fails the eval run outright; webhook redelivery and duplicate-message paths covered by 145 offline tests |

<br>

## The rest of the work

**45 systems** in the index, grouped by what they actually are:

| | |
|---|---|
| **Agents** · 13 | Approval gates, tool routing, multi-agent pipelines, escalation to humans |
| **Automation** · 10 | n8n backbones, Slack/Airtable/CRM glue, scheduled connectors, back-office reconciliation |
| **ML Systems** · 8 | Trained models with the serving, monitoring and retraining around them |
| **Environmental** · 6 | Satellite, acoustic and citizen-science pipelines that produce cited, reviewable evidence |
| **RAG** · 5 | Hybrid retrieval, multi-tenant isolation, grounding checks, evaluation harnesses |
| **LLM Infra** · 3 | Gateways, red-teaming, synthetic data and fine-tuning pipelines |

**[Browse all 45 →](https://moosamemon.me/work/)**

<br>

## How I work

**Right-sized tooling.** An n8n workflow when that's enough, a LangGraph backend when it isn't. The judgment about which one a problem deserves is the actual deliverable — not the most impressive architecture I could justify.

**Unhappy paths first.** Retries, fallbacks, evals and logging get built before the demo does. The difference between a demo and a system is everything that happens after the happy path.

**Nothing certifies itself.** Where a model can write to the real world, a human gates it and the gate lives in the backend, not the prompt. Where it makes a claim, the claim carries its provenance.

**Numbers or nothing.** Every project write-up quotes measurements where they exist and says plainly what isn't finished. No project here is described as working better than it does.

<br>

## Stack

<p align="center">
  <img alt="Stack" src="https://skillicons.dev/icons?i=py,fastapi,docker,postgres,supabase,redis,pytorch,sklearn,ts,react,tailwind,astro,nodejs,githubactions,grafana,prometheus,linux,git&theme=dark&perline=9">
</p>

| | |
|---|---|
| **Agents & orchestration** | LangGraph · LangChain · CrewAI · MCP · n8n · Dify |
| **Models** | Claude API · Gemini · Groq · Hugging Face · ONNX Runtime · PEFT/LoRA |
| **Retrieval** | Qdrant · ChromaDB · pgvector · Pinecone · Neo4j · BM25 hybrid + RRF |
| **Backend** | FastAPI · Django · Celery · Postgres · Supabase · Redis · SQLModel |
| **ML** | PyTorch · scikit-learn · LightGBM · SHAP |
| **Frontend** | React · TypeScript · Tailwind · Astro |
| **Ops** | Docker · GitHub Actions · Prometheus · Grafana · Langfuse |

<br>

---

<p align="center">
  <b>Bring me the problem, leave with how I'd build it.</b><br>
  20 minutes, no pitch.
</p>

<p align="center">
  <a href="https://moosamemon.me/contact/">Book a call</a> ·
  <a href="https://moosamemon.me/work/">See the work</a> ·
  <a href="mailto:notmoosamemon@gmail.com">notmoosamemon@gmail.com</a>
</p>
