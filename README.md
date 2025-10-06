# Lodestar

A minimalist web app that allows users to log astronomical observations to a database, where scientific data from SIMBAD and Aladin APIs will be added.

**Code Institute Bootcamp Capstone Project. 2025.**

## Features

### Feature 1: Astronomical Log CRUD

A comprehensive **secure** observation logging system allowing authenticated users to:

-   **User Authentication**: Registration, login, logout with django-allauth
-   **Secure Access Control**: Role-based permissions ensuring data privacy
-   **Create** new observation entries with date, time, location, and celestial object details (In Development)
-   **Read** observation history with search and filtering capabilities (In Development)
-   **Update** existing observations with additional notes, corrections, or enhanced data (In Development)
-   **Delete** unwanted or duplicate entries to maintain clean records (In Development)

### Feature 2: Scientific Data Integration

Real-time integration with astronomical databases:

-   Pull verified scientific data from **SIMBAD** (astronomical object database)
-   Integrate **Aladin** sky atlas data for visual context
-   Automatically enhance user observations with professional astronomical data
-   Provide context and validation for user-logged observations

### Feature 3: Astronomy News Hub (Stretch Goal)

Stay current with astronomical developments:

-   Curated astronomy news feed via RSS to JSON feature
-   Real-time updates from trusted astronomical sources

_Screenshots and detailed usage notes will be added as features are completed._

## Authentication System

**Status: In Progress**

Lodestar uses **Django Allauth** for user authentication:

-   Secure user registration and login
-   Session management with clear status indicators

## Tech Stack

<p align="left">
  <img src="https://skillicons.dev/icons?i=html,css,js,django,tailwind,postgres,heroku&perline=7" alt="HTML, CSS, JavaScript, Django, Tailwind CSS, PostgreSQL, Heroku" />
</p>

## Software Development Approach

-   _Methodology:_ Agile; suitably adapted for this specific project's scope and timeframe.
-   _GitHub Projects board:_ [Lodestar](https://github.com/users/curtisnlogan/projects/12/views/1)
-   _Project Management:_ Daily Sprint-based development, focusing on MVP delivery first followed by stretch goals.
-   _Version Control:_ Git workflow with feature branches and regular commits to document development progress.

## Design Rationale

### UI / UX

-   **Minimalist:** Generous whitespace and clean layouts evoke the vastness of space while improving focus and readability during observation sessions
-   **Tailwind CSS:** Utility-first framework enabling custom designs without the visual uniformity constraints of component-based frameworks like Bootstrap

### Typography

-   **Headings:** `Exo 2`, readability first with subtle sci-fi styling.
-   **Body:** `Inter`, readability above all else for logging accuracy, modern styling.

### Color System

| Role                   | Hex       | Notes                     |
| ---------------------- | --------- | ------------------------- |
| **Primary Background** | `#000000` | Deep space dark like mode |
| **Cards / Panels**     | `#001430` | Subtle nebula blue        |
| **Primary Text**       | `#F3F4F6` | High-contrast on dark bg  |
| **Secondary Text**     | `#C3D1E3` | Muted for helper text     |
| **Accents**            | `#398F9F` | Buttons, links            |
| **Highlights**         | `#FFD966` | Alerts, hover/focus       |

### Iconography & Imagery

-   **Icons:** [Tabler Icons](https://tabler.io/icons) — thin, crisp outlines fit the theme and do not require intrusive attributions in page.
-   **Images:** Curated astronomy shots from [Pexels](https://www.pexels.com/).

### Motion

-   Subtle-interactions only for comfort: modest ease-in-out for hover/focus/expand.
-   Respect `prefers-reduced-motion` accessibility feature as default. All users will benefit from this due to the nature of this web app.

### ERDs

**Complete ERD with Mixins:**
![Complete ERD with Mixins](docs/images/observations_erd.png)

### Wireframes

-   [Home Page - Logged Out](https://share.balsamiq.com/c/7bNH8SRv4DGu45XFubGoEr.jpg)
-   [Home Page - Logged In](https://share.balsamiq.com/c/5W8FNdetQaXZaK1yHdnKoP.jpg)
-   [My Observations Page](https://share.balsamiq.com/c/e1tdS3XZPHJzkwwG5rTtyP.jpg)
-   [My Observations Page - Observation Form](https://share.balsamiq.com/c/wWf9BTFpRmpxfnmenumcJM.jpg)
-   [My Observations Page - Observation Details](https://share.balsamiq.com/c/6z2jMcSR4W3uyZqSnRwRZw.jpg)
-   [My Astronomy News](https://share.balsamiq.com/c/tPYprGczYJDAPKk2HX7RyM.jpg)

### Key Decisions and Plan Changes

-   — **Theme**
    Settled on Astronomy, strong personal interest, good knowledge of the subject.

-   — **UI/UX foundations**
    Dark UI, star-field feel without literal backgrounds for use during astronomical observations.

-   — **MVP Scope**
    Focused on **Astronomical Log** to achieve CRUD functionality and **Astronomy Info** with APIs for UX. Everything else is backlog/stretch, including my more complex idea of integrating APIs with the log feature.

-   — **Epics & User Stories**
    Used assessment criteria integrated into User Stories. No slices per story due to small scope; instead, each epic ships once associated User Stories are completed. User Stories and their corresponding acceptance criteria are the smallest deliverables in this project. Story slices considered overboard for project scope.

-   — **Accessibility First**
    Ensured color choices meet contrast targets to strict WCAG standards.

-   — **UX/Scope reduction**
    The New Observation form was integrated into the homepage instead of a separate page. This reduces clicks for the user, keeps data entry centralized, and allows the assessor to see a streamlined flow in limited project time.

## Known Issues & Limitations

-   **Mobile Responsiveness:** Initial focus on desktop experience; mobile optimization scheduled for future iterations.
-   **Offline Capability:** Current implementation requires internet connectivity for full functionality.

## Future Enhancements

-   **Advanced Search:** Implement complex filtering options for observation history.
-   **Data Export:** Enable users to export their observation logs in various formats.
-   **Social Features:** Allow users to share interesting observations with the astronomy community.
-   **Advanced API Integration:** Deeper integration with professional astronomy databases for enhanced data validation.

## Setup and Deployment

-   — **Bootstrap vs. Tailwind CSS**
    Settled on Tailwind CSS over Bootstrap despite the additional implementation time required. Early in the course, I noted my preference for Tailwind's utility-first approach over Bootstrap's overly constrained templating system. While this choice demanded more development time, I was confident it was feasible within the project timeframe and would deliver a more immersive, custom UI/UX that better serves the astronomy theme.

## Setup and Deployment

### Environment Variables

This project requires the following environment variables to be set:

| Variable         | Description                                 | Required | Default | Example                                                                          |
| ---------------- | ------------------------------------------- | -------- | ------- | -------------------------------------------------------------------------------- |
| `SECRET_KEY`     | Django secret key for cryptographic signing | ✅       | None    | `your-secret-key-here`                                                           |
| `DEBUG`          | Enable/disable debug mode                   | ❌       | `False` | `True` (development), `False` (production)                                       |
| `DATABASE_URL`   | Database connection string                  | ✅       | None    | `sqlite:///db.sqlite3` (local), `postgres://user:pass@host:port/db` (production) |
| `CLOUDINARY_URL` | Cloudinary configuration for image uploads  | ✅       | None    | `cloudinary://api_key:api_secret@cloud_name`                                     |

#### Local Development Setup

1. Create a `.env` file in the project root:

```bash
# .env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CLOUDINARY_URL=cloudinary://your-api-key:your-api-secret@your-cloud-name
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python src/manage.py migrate
```

4. Start the development server:

```bash
python src/manage.py runserver
```

#### Production Deployment

Ensure all environment variables are properly configured in your hosting environment (e.g., Heroku Config Vars).

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

-   Area: docs | Passing in the assignment criteria for the README section, I prompted AI to help me build a README skeleton.
-   Area: UI/UX | Using my knowledge of space themed websites, I worked with AI to generate a suitable color palette for my website. It emphasized the importance of a dark mode themed palette, which has made my web app more practical in the field.
-   Area: agile | Passing in my curated version of the assignment criteria, I iterated Epics and User Stories with AI, ensuring a lean approach was taken given the small scope of this project.

## Credits

This project uses the following third-party resources:

-   **Fonts**

    -   [Inter](https://github.com/rsms/inter) — Copyright 2016 The Inter Project Authors. Licensed under the [SIL Open Font License, Version 1.1](https://openfontlicense.org/).
    -   [Exo 2](https://fonts.google.com/specimen/Exo+2) — Copyright 2020 The Exo 2 Project Authors. Licensed under the [SIL Open Font License, Version 1.1](https://openfontlicense.org/).

-   **Icons**

    -   [Tabler Icons](https://tabler.io/icons) — Copyright 2020–present Paweł Kuna. Licensed under the [MIT License](https://github.com/tabler/tabler-icons/blob/master/LICENSE).

-   **Images**
    -   Images provided by [Pexels](https://www.pexels.com/) and used under the [Pexels License](https://www.pexels.com/license/).
