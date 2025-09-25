# Lodestar

A minimalist web app, that allows users to log astronomical observations to a database. Also includes a home page that surfaces selected space related news and information.

**Code Institute Bootcamp Capstone Project. 2025.**

## Features

**Epic 1** (MVP): A user can utilize CRUD functionality on their own astronomical logs.
**Epic 2** (MVP): A user can read up-to-date space/astronomy news, through NASA API integrations.
**Epic 3** (Stretch): Pull real astronomical data from an Astronomy API into the users astronomical log.

*Usage notes and feature screenshots for each feature.*

## Tech Stack

<p align="left">
  <img src="https://skillicons.dev/icons?i=html,css,js,django,postgres,heroku" />
</p>

Here’s a tightened, drop-in “Design” section you can paste into your README. I kept your choices, clarified intent, and filled gaps with practical guidance and copy-ready snippets.

---

# Design

## UI / UX

### Typography

* **Headings:** `Exo 2`, fallback `system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif`
* **Body:** `Inter`, same fallbacks as above

### Color System

| Role                   | Hex       | Notes                         |
| ---------------------- | --------- | ----------------------------- |
| **Primary Background** | `#000000` | Deep space backdrop           |
| **Cards / Panels**     | `#001430` | Subtle nebula blue            |
| **Primary Text**       | `#F3F4F6` | High-contrast on dark         |
| **Secondary Text**     | `#C3D1E3` | Muted for helper text         |
| **Accent**             | `#398F9F` | Buttons, links, active states |
| **Highlight**          | `#FFD966` | Alerts                        |

### Iconography & Imagery

* **Icons:** [Tabler Icons](https://tabler.io/icons) — thin, crisp outlines fit the theme.
* **Images:** Curated astronomy shots from [Pexels](https://www.pexels.com/). Favor wide crops with low visual noise behind text.

### Motion

* Micro-interactions only: 150–200ms ease-in-out for hover/focus/expand.
* Respect `prefers-reduced-motion`.

## ERDs

> *See: `/docs/erds/*` (notes & screenshots).*

## Wireframes

> *See: `/docs/wireframes/*` (notes & screenshots).*

**Primary views**

## Key Decisions

* — Theme: Astronomy**
  Strong personal interest, good knowledge of the subject. Dark UI, star-field feel without literal backgrounds for use during observations.

* — MVP Scope**
  Focused on **Astronomical Log** to achieve CRUD functionality and **Space News/Info** with NASA API for UX. Everything else is backlog/stretch.

* — Epics & User Stories**
  Used assessment criteria as baseline. No slices per story due to small scope; instead, each epic ships end-to-end:

* — Non-Goals & Trade-offs (v1)**
  No social features, comments, or real-time collaboration.

* — Tech & Content Choices**
  Tabler icons for consistency and license conditions; Pexels for royalty-free imagery.

* — Accessibility First**
  Ensured color choices meet contrast targets on dark surfaces; keyboard nav and focus styles are mandatory for observations.

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

## Agile

*Methodology:* Agile
*GitHub Projects board:* [Lodestar](https://github.com/users/curtisnlogan/projects/12/views/1)
*Screenshots:*

## Design Rationale & Plan Changes

**Initial Rationale (why these choices):** <!-- framework, auth, db, hosting -->
**Major Plan Changes (dated):**

* **YYYY-MM-DD:** <!-- change + reason + impact + link to issue/PR -->
* **YYYY-MM-DD:** <!-- … -->

## AI Usage Report

Tools: ChatGPT 5, Copilot  

Core Policy: Always review any AI output

## AI Usage Log (Key Areas)

Areas covered: code · tests · docs · bugs · perf · security · UI/UX · Agile

<!-- - Areas: code · tests · docs · bugs · perf · security · UX --> | <!-- what AI helped with (1 line) -->

- Areas: docs | Using the assignment criteria for the readme section, I prompted AI to help me build a README.md skeleton.
- Areas: UI/UX | Emphasing my readability first approach to fonts, I worked through possible selections with AI and tested them on Google Fonts.
- Areas: UI/UX | Using my knowledge on space themed websites, I worked with AI to come up with a suitable colour pallete for my website. It emphasised the importance of a dark like mode for individuals using this web app, whilst carrying out observations.
- Areas: Agile | Refreshed my knowledge on Agile approaches, which allowed me to streamline my implemntation of the epics/user stories etc. approach.

## Testing (Django)

```
python manage.py test
```

## Credits

This project uses the following third-party resources:

* <!-- Library/Repo/Article --> — **Author** — License: <!-- --> — Used for: <!-- -->\

- **Fonts**  
  - [Inter](https://github.com/rsms/inter) — Copyright 2016 The Inter Project Authors. Licensed under the [SIL Open Font License, Version 1.1](https://openfontlicense.org/).  
  - [Exo 2](https://fonts.google.com/specimen/Exo+2) — Copyright 2020 The Exo 2 Project Authors. Licensed under the [SIL Open Font License, Version 1.1](https://openfontlicense.org/).  

- **Icons**  
  - [Tabler Icons](https://tabler.io/icons) — Copyright 2020–present Paweł Kuna. Licensed under the [MIT License](https://github.com/tabler/tabler-icons/blob/master/LICENSE).  

- **Images**  
  - Images provided by [Pexels](https://www.pexels.com/) and used under the [Pexels License](https://www.pexels.com/license/).
