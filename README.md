# Lodestar

A minimalist web app, that allows users to log astronomical observations to a database. Also includes a home page that surfaces selected astronomy related information.

**Code Institute Bootcamp Capstone Project. 2025.**

## Features

**Feature 1** - A user can utilize CRUD functionality for astronomical logs.
**Feature 2** - A user can read up-to-date astronomy information, through API integrations.
**Feature 3** - (Stretch): Pull real astronomical data from an Astronomy API into the users astronomical logs.

*Usage notes and feature screenshots for each feature.*

## Tech Stack

<p align="left">
  <img src="https://skillicons.dev/icons?i=html,css,js,django,postgres,heroku" />
</p>

## Software Development Approach

* *Methodology:* Agile approach, adapted for this specific projects scope and timeframe.
* *GitHub Projects board:* [Lodestar](https://github.com/users/curtisnlogan/projects/12/views/1)
* *Screenshots:*

## Design Rationale

### UI / UX

### Typography

* **Headings:** `Exo 2`, readability first with subtle sci-fi styling.
* **Body:** `Inter`, readability above all else for logging accuracy, modern styling.

### Color System 

| Role                   | Hex       | Notes                         |
| ---------------------- | --------- | ----------------------------- |
| **Primary Background** | `#000000` | Deep space dark like mode     |
| **Cards / Panels**     | `#001430` | Subtle nebula blue            |
| **Primary Text**       | `#F3F4F6` | High-contrast on dark bg      |
| **Secondary Text**     | `#C3D1E3` | Muted for helper text         |
| **Accents**            | `#398F9F` | Buttons, links                |
| **Highlights**         | `#FFD966` | Alerts, hover/focus           |

### Iconography & Imagery

* **Icons:** [Tabler Icons](https://tabler.io/icons) — thin, crisp outlines fit the theme and do not require intrusive attributions in page.
* **Images:** Curated astronomy shots from [Pexels](https://www.pexels.com/).

### Motion

* Subtle-interactions only for comfort: modest ease-in-out for hover/focus/expand.
* Respect `prefers-reduced-motion` accessibility feature as default. All users will benefit from this due to the nature of this web app.

### ERDs

> *screenshots.*

### Wireframes

> [Home Page - Logged Out](https://share.balsamiq.com/c/7bNH8SRv4DGu45XFubGoEr.jpg)
> [Home Page - Logged In](https://share.balsamiq.com/c/5W8FNdetQaXZaK1yHdnKoP.jpg)
> [My Observations Page](https://share.balsamiq.com/c/e1tdS3XZPHJzkwwG5rTtyP.jpg)
> [My Observations Page - Observation Form](https://share.balsamiq.com/c/wWf9BTFpRmpxfnmenumcJM.jpg)
> [My Observations Page - Observation Details](https://share.balsamiq.com/c/6z2jMcSR4W3uyZqSnRwRZw.jpg)
> [My Astronomy News](https://share.balsamiq.com/c/tPYprGczYJDAPKk2HX7RyM.jpg)

### Key Decisions and Plan Changes

* — **Theme**
  Settled on Astonomy, srong personal interest, good knowledge of the subject.

* — **UI/UX foundations**
  Dark UI, star-field feel without literal backgrounds for use during astronomical observations.

* — **MVP Scope**
  Focused on **Astronomical Log** to achieve CRUD functionality and **Astronomy Info** with APIs for UX. Everything else is backlog/stretch, including my more complex idea of integrating APIs with the log feature.

* — **Epics & User Stories**
  Used assessment criteria integrated into User Stories. No slices per story due to small scope; instead, each epic ships once associsated User Stories are completed. User Stories and their corrosponding acceptance criteria are the smallest deliverables in this project. Story slices considered overboard for project scope.

* — **Accessibility First**
  Ensured color choices meet contrast targets to strict WCAG standards.

* - **UX/Scope reduction**
  The New Observation form was integrated into the homepage instead of a separate page. This reduces clicks for the user, keeps data entry centralised, and allows the assessor to see a streamlined flow in      limited project time.

## Setup and Deployment

## Unit Tests

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

- Area: docs | Passing in the assignment criteria for the README section, I prompted AI to help me build a README skeleton.
- Area: UI/UX | Using my knowledge of space themed websites, I worked with AI to generate a suitable colour pallete for my website. It emphasised the importance of a dark mode themed pallete, which has made my web app more practical in the field.
- Area: agile | Passing in my curated version of the assignment criteria, I iterated Epics and User Stories with AI, ensuring a lean approach was taken given the small scope of this project.

## Credits

This project uses the following third-party resources:

- **Fonts**  
  - [Inter](https://github.com/rsms/inter) — Copyright 2016 The Inter Project Authors. Licensed under the [SIL Open Font License, Version 1.1](https://openfontlicense.org/).  
  - [Exo 2](https://fonts.google.com/specimen/Exo+2) — Copyright 2020 The Exo 2 Project Authors. Licensed under the [SIL Open Font License, Version 1.1](https://openfontlicense.org/).  

- **Icons**  
  - [Tabler Icons](https://tabler.io/icons) — Copyright 2020–present Paweł Kuna. Licensed under the [MIT License](https://github.com/tabler/tabler-icons/blob/master/LICENSE).  

- **Images**  
  - Images provided by [Pexels](https://www.pexels.com/) and used under the [Pexels License](https://www.pexels.com/license/).
