# Lodestar

A minimalist web app, that allows users to log astronomical observations to a database. Also includes a home page that surfaces selected space related news and information.

**Code Institute Bootcamp Capstone Project. 2025.**

## Features

**Feature 1** A user can utilize CRUD functionality on their astronomical logs.
**Feature 2** A user can read up-to-date space/astronomy news, through NASA API integrations.
**Feature 3** (Stretch): Pull real astronomical data from an Astronomy API into the users astronomical logs.

*Usage notes and feature screenshots for each feature.*

## Tech Stack

<p align="left">
  <img src="https://skillicons.dev/icons?i=html,css,js,django,postgres,heroku" />
</p>

## Software Development Approach

* *Methodology:* Agile adapted for this specific projects scope
* *GitHub Projects board:* [Lodestar](https://github.com/users/curtisnlogan/projects/12/views/1)
* *Screenshots:*

# Design Rationale

## UI / UX

### Typography

* **Headings:** `Exo 2`, readability first with some sci-fi styling.
* **Body:** `Inter`, readability above all else, modern styling.

### Color System

| Role                   | Hex       | Notes                         |
| ---------------------- | --------- | ----------------------------- |
| **Primary Background** | `#000000` | Deep space dark like mode     |
| **Cards / Panels**     | `#001430` | Subtle nebula blue            |
| **Primary Text**       | `#F3F4F6` | High-contrast on dark bg      |
| **Secondary Text**     | `#C3D1E3` | Muted for helper text         |
| **Accent**             | `#398F9F` | Buttons, links                |
| **Highlight**          | `#FFD966` | Alerts, hover/focus           |

### Iconography & Imagery

* **Icons:** [Tabler Icons](https://tabler.io/icons) — thin, crisp outlines fit the theme and do not require intrusive attribution on page.
* **Images:** Curated astronomy shots from [Pexels](https://www.pexels.com/).

### Motion

* Subtle-interactions only for minimalism: modest ease-in-out for hover/focus/expand.
* Respect `prefers-reduced-motion` as default. All users will benefit from this due to the nature of the web app.

## ERDs

> *See: `/docs/erds/*` (notes & screenshots).*

## Wireframes

> *See: `/docs/wireframes/*` (notes & screenshots).*

## Key Decisions and Major Plan Changes

* — Theme: Astronomy**
  Strong personal interest, good knowledge of the subject.

* — UI/UX foundations**
  Dark UI, star-field feel without literal backgrounds for use during astronomical observations.

* — MVP Scope**
  Focused on **Astronomical Log** to achieve CRUD functionality and **Space News/Info** with NASA API for UX. Everything else is backlog/stretch, including my more complex idea of integrating APIs with the log feature.

* — Epics & User Stories**
  Used assessment criteria as baseline. No slices per story due to small scope; instead, each epic ships once associsated User Stories are completed. User Stories and their corrosponding acceptance criteria are the smallest deliverables in this project.

* — Accessibility First**
  Ensured color choices meet contrast targets on dark surfaces, using AI to check against strict WSAG tests.

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

## Unit Tests (Django)

This project uses Django's built-in test runner.

To run all tests:

```bash
python manage.py test
```

You can also run tests for a specific app:

```bash
python manage.py test myapp
```

## AI Usage Report

Tools: ChatGPT 5, Copilot  

Core Policy: Always manually review any AI output.

## AI Usage Log (Key Areas)

Areas covered: code · tests · docs · bugs · perf · security · UI/UX · agile

- Area: docs | Passing in the assignment criteria for the README section, I prompted AI to help me build a skeleton.
- Area: UI/UX | Using my knowledge on space themed websites, I worked with AI to come up with a suitable colour pallete for my website. It emphasised the importance of a dark mode centered pallete.
- Area: agile | Refreshed my knowledge on Agile approaches, allowing me to streamline my implemntation of the epics/user stories etc. approach.
- - Area: agile | Passing in my curated version of the assignment criteria and my epics, I iterated with AI over User Stories, ensuring a sensible approach was taken given small project scope/timeframe.

## Credits

This project uses the following third-party resources:

- **Fonts**  
  - [Inter](https://github.com/rsms/inter) — Copyright 2016 The Inter Project Authors. Licensed under the [SIL Open Font License, Version 1.1](https://openfontlicense.org/).  
  - [Exo 2](https://fonts.google.com/specimen/Exo+2) — Copyright 2020 The Exo 2 Project Authors. Licensed under the [SIL Open Font License, Version 1.1](https://openfontlicense.org/).  

- **Icons**  
  - [Tabler Icons](https://tabler.io/icons) — Copyright 2020–present Paweł Kuna. Licensed under the [MIT License](https://github.com/tabler/tabler-icons/blob/master/LICENSE).  

- **Images**  
  - Images provided by [Pexels](https://www.pexels.com/) and used under the [Pexels License](https://www.pexels.com/license/).
