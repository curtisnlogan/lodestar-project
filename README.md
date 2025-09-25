# Lodestar

A minimalist web app, that allows users to log personal astronomical observations to a database. Also includes a home page that surfaces selected space related news and information.

Code Institute Bootcamp Capstone Project. 2025.

## Features

- EPIC 1: User can utilize CRUD functionality on personal astromical observation logs.
- EPIC 2: User can read up-to-date space/astronomy news, through NASA API integrations.
- EPIC 3: Pull real astronomical data from an Astronomy API into the users astronmical log.
*Usage notes and screenshots.*

## Tech Stack

**Frontend:** HTML5, CSS3, JavaScript · **Backend:** Django Web Framework · **DB:** PostgresSQL· **Infra/CI:** Heroku

---

## System Design

> *Final implementation docs: ERD, routes/APIs, key decisions*

**ERD:** *screenshots*

**Public URL endpoints:**

| Method | Route      | Purpose       | Auth             |
| ------ | ---------- | ------------- | ---------------- |
| GET    | `/api/...` | <!-- TODO --> | Public/Protected |

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

## Wireframes

Store images in `docs/wireframes/` and link:

* `docs/wireframes/landing.png`

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
