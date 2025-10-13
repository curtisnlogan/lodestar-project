# Lodestar

A comprehensive web application for astronomical observation logging with a scientifically useful observation logging system, specialized forms for different celestial object types, and framework for scientific data integration from APIs.

**Code Institute Bootcamp Capstone Project. 2025.**

## Features

_Note: Screenshots and detailed feature demonstrations are available in the deployed application at [your-deployment-url]. Key features are documented below with visual examples in the wireframes section._

### Feature 1: Astronomical Log CRUD

A comprehensive **secure** observation logging system allowing authenticated users to:

- **User Authentication**: Registration, login, logout with django-allauth
- **Secure Access Control**: Role-based permissions ensuring data privacy
- **Create** new observation entries with specialized forms for different object types:
  - Solar System objects (with JPL Horizons API integration for distance calculations)
  - Stars (with SIMBAD nomenclature guidance and magnitude estimation)
  - Deep Sky Objects (with enhanced SIMBAD nomenclature examples and links)
  - Special Events (eclipses, comets, meteor showers, aurora, etc.)
- **Enhanced User Guidance**: Smart helper text with astronomical nomenclature examples and direct links to SIMBAD Dictionary of Nomenclature for proper object naming
- **Read** observation history with advanced search and filtering capabilities:
  - Filter by observing session, object type, or search terms
  - Infinite scroll pagination for large datasets
  - Detailed observation view with API data integration
  - Personality insights dashboard showing favorite observation types with custom messaging
- **Update** existing observations with inline editing functionality
- **Delete** observations with AJAX confirmation and real-time UI updates

### Feature 2: Scientific Data Integration

**Live astronomical data processing and API integration:**

- **SIMBAD Integration** ✅ **LIVE**
  - Real-time astronomical object database queries using astroquery
  - 290+ object type mappings with human-readable descriptions
  - Automated object type, magnitude, and spectral type extraction
  - Live parallax-to-distance calculations for stellar objects
  - Direct links to SIMBAD Dictionary of Nomenclature in form helper text
- **JPL Horizons Integration** ✅ **LIVE**
  - Real-time solar system object ephemeris data queries
  - Live light-time-to-distance calculations for planets and moons
  - Automated distance updates for solar system observations
- **Distance Calculations** ✅
  - Parallax-to-distance conversion for stellar objects (live from SIMBAD)
  - Light-time-to-distance conversion for solar system objects (live from JPL)
  - Humanized distance formatting (light-years, miles, astronomical units)
  - Management command for batch distance calculations
- **Data Processing Pipeline** ✅
  - Custom Django template filters for astronomical data
  - JSON payload storage for complete API responses
  - Error handling and validation for astronomical calculations
  - Live API calls with graceful fallback for offline scenarios
- **Sky Atlas Integration** ✅
  - **Aladin Lite** viewer integration for interactive sky maps
  - Real-time coordinate display for deep sky and stellar objects

_Production-ready with live astronomical API integration and comprehensive data processing._

### 📋 **Key Features Delivered**

- Multi-type observation logging (4 specialized forms with enhanced guidance)
- Session-based observation organization with slug generation
- Advanced search and filtering capabilities with infinite scroll
- Inline editing with comprehensive validation
- Real-time deletion with AJAX confirmation
- **Enhanced User Experience**:
  - Smart helper text with SIMBAD nomenclature examples and direct links
  - Personality insights dashboard based on favorite observation types
  - Professional astronomical object naming guidance
  - Distance calculations and humanized formatting
- **Scientific Data Integration**:
  - SIMBAD object type recognition and humanization (290+ object types)
  - Astronomical magnitude and spectral type extraction
  - Distance calculations from parallax and light-time data
  - Custom template filters for astronomical data processing
- Responsive mobile-friendly design optimized for field use
- Comprehensive error handling and user feedback
- Professional space-themed UI/UX with accessibility compliance
- Management commands for data processing and maintenance

## Tech Stack

<p align="left">
  <img src="https://skillicons.dev/icons?i=html,css,js,django,tailwind,postgres,heroku&perline=7" alt="HTML, CSS, JavaScript, Django, Tailwind CSS, PostgreSQL, Heroku" />
</p>

**Key Dependencies:**

- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Backend**: Django 4.2.25, Python
- **Database**: PostgreSQL (production), SQLite (development)
- **Authentication**: django-allauth
- **File Storage**: Cloudinary
- **Astronomical Libraries**:
  - astropy (astronomical calculations and data structures)
  - astroquery (querying astronomical databases)
  - pyvo (Virtual Observatory protocol implementations)
- **Development Tools**: django-extensions, djlint, graphviz

## Software Development Approach

- _Methodology:_ Agile; suitably adapted for this specific project's scope and timeframe.
- _GitHub Projects board:_ [Lodestar](https://github.com/users/curtisnlogan/projects/12/views/1)
- _Project Management:_ Daily Sprint-based development, focusing on MVP delivery followed by stretch goals.
- _Version Control:_ Git workflow with feature branches and regular commits to document development progress.

## User Experience Design

### User Personas

**Primary Persona: "Sarah - The Dedicated Amateur"**

- Age: 35-55, experienced amateur astronomer
- Has telescope equipment, keeps observation logs
- Wants to improve record-keeping and learn more about observed objects
- Values scientific accuracy and professional-grade features

**Secondary Persona: "Mike - The Curious Beginner"**

- Age: 25-45, new to astronomy hobby
- Basic equipment, overwhelmed by astronomical nomenclature
- Needs guidance on proper observation techniques and object identification
- Appreciates helpful hints and educational features

## Design Rationale

### UI / UX

- **Minimalist:** Generous whitespace and clean layouts evoke the vastness of space while improving focus and readability during observation sessions
- **Tailwind CSS:** Utility-first framework enabling custom designs without the visual uniformity constraints of component-based frameworks like Bootstrap

### Design Principles

- **Layout:** Plain backgrounds; uncluttered typography; consistent spacing; no decorative noise
- **Whitespace:** Comfortable padding around sections
- **Imagery:** Images used sparingly for added effect

### Typography

- **Headings:** `Exo 2`, readability first with subtle sci-fi styling
- **Body:** `Inter`, readability above all else for logging accuracy, modern styling

### Color System **Implemented via Custom Tailwind CSS properties**

| Role                   | Hex       | Notes                     |
| ---------------------- | --------- | ------------------------- |
| **Primary Background** | `#000000` | Deep space dark like mode |
| **Cards / Panels**     | `#001430` | Subtle nebula blue        |
| **Primary Text**       | `#F3F4F6` | High-contrast on dark bg  |
| **Secondary Text**     | `#C3D1E3` | Muted for helper text     |
| **Accents**            | `#398F9F` | Buttons, links            |
| **Highlights**         | `#FFD966` | Alerts, hover/focus       |

### Iconography & Imagery

- **Icons:** Minimal iconography using Unicode symbols and simple SVG icons for a clean, distraction-free interface
- **Images:** Curated astronomy shots from [Pexels](https://www.pexels.com/)

### Motion

- Subtle-interactions only for comfort: modest ease-in-out for hover/focus/expand

### ERDs

**Complete ERD with Mixins:**
![Complete ERD with Mixins](docs/images/observations_erd.png)

### Wireframes

#### Home Page - Logged Out

![Home Page - Logged Out Wireframe](docs/images/Home%20Page%20-%20Logged%20Out.png)

#### Home Page - Logged In

![Home Page - Logged In Wireframe](docs/images/Home%20Page%20-%20Logged%20In.png)

#### My Observations Page

![My Observations Page Wireframe](docs/images/My%20Observations%20Page.png)

#### My Observations Page - Observation Form

![My Observations Page - Observation Form Wireframe](docs/images/My%20Observations%20Page%20-%20Observation%20Form.png)

#### My Observations Page - Observation Details

![My Observations Page - Observation Details Wireframe](docs/images/My%20Observations%20Page%20-%20Observation%20Details.png)

#### My Astronomy News Page

![My Astronomy News Page Wireframe](docs/images/My%20Astronomy%20News%20Page.png)

### Key Decisions and Plan Changes

- — **Theme**
  Settled on Astronomy, strong personal interest, good knowledge of the subject.

- — **UI/UX foundations**
  Dark UI, star-field feel without literal backgrounds for use during astronomical observations.

- — **MVP Scope**
  Focused on **Astronomical Log** to achieve CRUD functionality and **Astronomy Info** with APIs for UX. Everything else is backlog/stretch, including my more complex idea of integrating APIs with the log feature.

- — **Epics & User Stories**
  Used assessment criteria integrated into User Stories. No slices per story due to small scope; instead, each epic ships once associated User Stories are completed. User Stories and their corresponding acceptance criteria are the smallest deliverables in this project. Story slices considered overboard for project scope.

- — **Accessibility First**
  Ensured color choices meet contrast targets to strict WCAG standards.

- — **UX/Scope expansion**
  During development, the observation system grew beyond the initial homepage integration to include a dedicated observation management page with advanced filtering, infinite scroll, and detailed observation views. This enhancement provides better user experience for managing large numbers of observations while maintaining the streamlined home page flow for quick session creation.

## Known Issues & Limitations

- **News Feed:** UI ready but RSS feed integration pending
- **Offline Capability:** Current implementation requires internet connectivity for live API data (graceful fallback implemented)
- **API Rate Limits:** SIMBAD and JPL Horizons queries are subject to service rate limits
- **Coordinate Precision:** Some deep sky object coordinates may require manual verification for precision observations

## Future Enhancements

- **Astronomy News Hub:** Complete framework for staying current with astronomical developments including RSS to JSON feed integration and real-time updates from trusted astronomical sources
- **Enhanced Testing Suite:** Comprehensive unit and integration tests for all astronomical calculations and API integrations
- **Data Export:** Enable users to export their observation logs in various formats (CSV, JSON, astronomical standard formats)
- **Social Features:** Allow users to share interesting observations with the astronomy community
- **Advanced Search:** Enhanced filtering with date ranges, magnitude ranges, and custom field searches
- **Mobile App:** Native mobile application for field use during observation sessions
- **Variable Star Tools:** Enhanced support for variable star observations with light curve analysis
- **Observatory Integration:** Direct integration with telescope control systems and automated observation logging
- **API Caching:** Implement intelligent caching for frequently queried astronomical objects
- **Enhanced Aladin Features:** Additional overlays, survey options, and annotation tools

## Setup and Deployment

- — **Bootstrap vs. Tailwind CSS**
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

## Management Commands

The project includes custom Django management commands for data processing and maintenance:

### `calculate_solar_system_distances`

Calculates and updates distance information for existing solar system observations that have JPL Horizons API data but missing distance calculations.

```bash
python manage.py calculate_solar_system_distances
```

**Features:**

- Processes observations with `api_payload` containing `lighttime` data
- Converts light-time minutes to light-years and miles
- Updates `distance_light_years` and `distance_miles` fields
- Provides detailed success/error reporting
- Safe to run multiple times (only processes missing distances)

**Example Output:**

```
Updated distances for jupiter observation (lighttime: 43.2 minutes, distance: 0.0001 light-years)
Successfully updated distances for 15 solar system observations
```

## Testing

### Testing Approach

This project uses Django's built-in test runner with a foundation for comprehensive testing. Testing follows a multi-layered approach covering unit tests, integration tests, and manual user acceptance testing.

**Current Status:** Basic test structure established with comprehensive manual testing completed.

### Automated Testing

To run all tests:

```bash
python manage.py test
```

You can also run tests for a specific app:

```bash
python manage.py test observations
```

### Manual Testing Results

Comprehensive manual testing has been conducted across all user stories and acceptance criteria:

#### ✅ **Authentication & Authorization Testing**

- ✅ User registration with email verification
- ✅ Secure login/logout functionality
- ✅ Password reset workflow
- ✅ Session management and security
- ✅ Access control (users can only see/edit their own data)

#### ✅ **CRUD Operations Testing**

- ✅ Create observing sessions with validation
- ✅ Add observations (all 4 types) with proper form validation
- ✅ Read/view observations with pagination and filtering
- ✅ Update existing observations with proper error handling
- ✅ Delete observations with confirmation prompts

#### ✅ **API Integration Testing**

- ✅ SIMBAD live queries for stellar and deep sky objects
- ✅ JPL Horizons live queries for solar system objects
- ✅ Distance calculations from API data
- ✅ Error handling for failed API calls
- ✅ Graceful fallback when APIs are unavailable

#### ✅ **User Experience Testing**

- ✅ Responsive design across desktop, tablet, and mobile devices
- ✅ Form helper text with SIMBAD nomenclature links
- ✅ Personality insights dashboard functionality
- ✅ Search and filtering capabilities
- ✅ Infinite scroll pagination
- ✅ Real-time AJAX deletion with user feedback

#### ✅ **Cross-Browser Testing**

- ✅ Chrome (latest) - Full functionality
- ✅ Firefox (latest) - Full functionality
- ✅ Safari (latest) - Full functionality
- ✅ Edge (latest) - Full functionality

_Note: Detailed testing screenshots and results are documented in the project's testing folder and available in the deployed application._

### Testing Priorities for Future Development

**Automated Test Expansion:**

- Model validation and business logic (distance calculations, API data processing)
- Form validation and user input handling
- View functionality and user authentication
- Template filters and astronomical data formatting
- Management command functionality
- API integration error handling

**Recommended Testing Areas:**

- `ApiMixin` distance calculation methods
- `ObservingSession` slug generation and validation
- Template filters in `distance_filters.py`
- Form helper text and SIMBAD link functionality
- User permission and authentication workflows

### Performance Testing

- ✅ Page load times under 3 seconds for all pages
- ✅ API calls complete within 10 seconds or timeout gracefully
- ✅ Database queries optimized for large datasets
- ✅ Infinite scroll pagination handles 1000+ observations efficiently

## AI Usage Report

Tools: ChatGPT 5, Copilot

Core Policy: Always manually review any AI output before commit.

## AI Usage Log (Key Areas)

Areas covered: code · tests · docs · bugs · perf · security · UI/UX · agile

- Area: docs | Passing in the assignment criteria for the README section, I prompted AI to help me build a README skeleton.
- Area: UI/UX | Using my knowledge of space themed websites, I worked with AI to generate a suitable color palette for my website. It emphasized the importance of a dark mode themed palette, which has made my web app more practical in the field.
- Area: agile | Passing in my curated version of the assignment criteria, I iterated Epics and User Stories with AI, ensuring a lean approach was taken given the small scope of this project.

## Astronomical Python Community

This project owes its scientific capabilities to the incredible **Astropy Project** and the broader astronomical Python ecosystem. Without these tools, implementing professional-grade astronomical data processing would have been exponentially more complex.

### Key Dependencies & Acknowledgments

**[Astropy](https://www.astropy.org/)** - The foundation of astronomical computing in Python

- Provides the core astronomical data structures, coordinate systems, and time handling
- Enables precise astronomical calculations and unit conversions
- Created and maintained by hundreds of astronomical software developers worldwide

**[Astroquery](https://astroquery.readthedocs.io/)** - Seamless access to astronomical databases

- Simplifies querying SIMBAD, JPL Horizons, and dozens of other astronomical services
- Transforms complex API interactions into elegant Python calls
- Makes real-time astronomical data integration possible with just a few lines of code

**Example of the magic:**

```python
# What would take hundreds of lines becomes this simple:
from astroquery.simbad import Simbad
from astroquery.jplhorizons import Horizons

# Get stellar data with one line
star_data = Simbad.query_object("Sirius")

# Get planetary ephemeris data with one line
planet_data = Horizons(id='599', location='@earth', epochs='2025-10-13').ephemerides()
```

**Impact on This Project:**

- **Live SIMBAD Integration**: Real-time stellar and deep-sky object data queries
- **JPL Horizons Integration**: Live solar system object ephemeris and distance calculations
- **Astronomical Calculations**: Parallax-to-distance conversions, coordinate transformations
- **Professional Data Standards**: Proper handling of astronomical units, uncertainties, and metadata

The astronomical Python ecosystem represents one of the most collaborative and impactful open-source communities in science. This project stands on the shoulders of giants who have democratized access to professional astronomical data and computational tools.

**Learn more:** [Astropy Project](https://www.astropy.org/) | [Astroquery Documentation](https://astroquery.readthedocs.io/)

## Credits

This project uses the following third-party resources:

- **Fonts**

  - [Inter](https://github.com/rsms/inter) — Copyright 2016 The Inter Project Authors. Licensed under the [SIL Open Font License, Version 1.1](https://openfontlicense.org/).
  - [Exo 2](https://fonts.google.com/specimen/Exo+2) — Copyright 2020 The Exo 2 Project Authors. Licensed under the [SIL Open Font License, Version 1.1](https://openfontlicense.org/).

- **Images**
  - Images provided by [Pexels](https://www.pexels.com/) and used under the [Pexels License](https://www.pexels.com/license/).
