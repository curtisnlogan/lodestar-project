# Project Title

*Short one-line value prop. Bootcamp Capstone (Cohort/Year).*

---

## Features

* [ ] <!-- EPIC: Feature 1 -->
* [ ] <!-- EPIC: Feature 2 -->
* [ ] <!-- EPIC: Feature 3 -->
  *Usage notes and screenshots.*

---

## Tech Stack

**Frontend:** <!-- TODO --> · **Backend:** <!-- TODO --> · **DB:** <!-- TODO --> · **Infra/CI:** <!-- TODO -->

---

## System Design

> *Final implementation docs: ERD, routes/APIs, key decisions*

**ERD:** `docs/diagrams/erd.png`

**API/Routes (expand as you build):**

| Method | Route      | Purpose       | Auth             | Notes         |
| ------ | ---------- | ------------- | ---------------- | ------------- |
| GET    | `/api/...` | <!-- TODO --> | Public/Protected | <!-- TODO --> |

**Key Decisions:**

* 001 — <!-- TODO short title -->

---

## Setup

**Prereqs:** <!-- Node/Python version --> · <!-- DB -->
**Env:** copy `.env.example` → `.env` and fill:

* `DATABASE_URL=` <!-- TODO -->
* `JWT_SECRET=` <!-- TODO -->

**Install & Run Locally:**

```bash
git clone <repo> && cd <dir>
# install
npm i
# dev
npm run dev
# (optional) docker
# docker compose up --build
```

## Deployment

*Target (e.g., Render/Vercel/Netlify):* <!-- TODO -->
*Build cmd:* <!-- TODO --> · *Env in prod:* <!-- TODO -->
*Migrations:* <!-- TODO --> · *Monitoring/Logs:* <!-- TODO -->
*Rollback plan:* <!-- TODO one line -->

## Troubleshooting

| Symptom               | Likely Cause               | Fix                              |
| --------------------- | -------------------------- | -------------------------------- |
| DB connection refused | DB not running / URL wrong | Start DB / update `DATABASE_URL` |
| CORS error            | Origin not allowed         | Update server CORS allowlist     |
| <!-- add as found --> |                            |                                  |

---

## Wireframes

Store images in `docs/wireframes/` and link:

* `docs/wireframes/landing.png`
* `docs/wireframes/core-flow.png`
* Figma link: <!-- TODO -->

---

## Agile

*Methodology:* <!-- Scrum/Kanban; sprint length -->
*GitHub Projects board:* <!-- link -->
*Screenshots:* `docs/agile/board-week-01.png`, `docs/agile/burndown-sprint-02.png`

---

## Design Rationale & Plan Changes

**Initial Rationale (why these choices):** <!-- framework, auth, db, hosting -->
**Major Plan Changes (dated):**

* **YYYY-MM-DD:** <!-- change + reason + impact + link to issue/PR -->
* **YYYY-MM-DD:** <!-- … -->

---

## AI Usage Report

**Tools:** <!-- ChatGPT, Copilot, etc. -->
**Policy:** Human review; tests added; licenses respected; no secrets in prompts.

**Log (add rows as used):**

| Date       | Tool     | Area (code/tests/bugs/perf/UX) | Prompt/Goal (short) | Used? | Link (PR/commit) | Impact (notes/metrics)                   |
| ---------- | -------- | ------------------------------ | ------------------- | ----- | ---------------- | ---------------------------------------- |
| YYYY-MM-DD | <!-- --> | <!-- -->                       | <!-- -->            | ✅/❌   | #123             | <!-- time saved, defects fixed, etc. --> |

---

## Proofreading Log

| Date       | Scope (README / repo / board) | Issues Found | Fixed? | Reviewer |
| ---------- | ----------------------------- | ------------ | ------ | -------- |
| YYYY-MM-DD | README                        | <!-- -->     | ✅/❌    | <!-- --> |

---

## Testing (optional but recommended)

```bash
npm test        # unit
# npm run test:e2e  # if applicable
```

*Coverage report path:* `coverage/index.html` <!-- if applicable -->

---

## Credits

* <!-- Library/Repo/Article --> — **Author** — License: <!-- --> — Used for: <!-- -->
* Assets/icons/fonts: <!-- source & license -->
  *For substantial third-party code, include `THIRD_PARTY_NOTICES.md`.*
