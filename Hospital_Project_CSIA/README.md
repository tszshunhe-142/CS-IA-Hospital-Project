# Hospital Health Education Platform

The platform provides a Figma-inspired homepage, a MySQL-backed lecture library and lecture detail pages, keyword search, relevance ranking, combined lecture filters, and related-lecture recommendations. The example records are fictional. Accounts and administration remain reserved for later phases.

## Technology

- Python 3.10+ and Flask
- MySQL 8+ with `mysql-connector-python`
- HTML, CSS, and Flask templates
- HTML5 video for local lecture recordings

## Project structure

```text
app/
  __init__.py                  Flask routes for home, library, and details
  __main__.py                  Development entry point
  algorithms/search.py         Weighted scoring and manual Merge Sort
  algorithms/filtering.py      Department, category, and date filters
  algorithms/recommendations.py Weighted lecture similarity and top 3 selection
  data/__init__.py             MySQL lecture queries
  database/connection.py       Environment-based MySQL connection
  static/css/styles.css        Responsive page styles
  static/videos/               Place local lecture videos here
  templates/
    base.html                  Shared navigation and footer
    index.html                 Homepage
    lectures.html              Lecture library
    lecture_detail.html        Lecture player and information
    partials/lecture_card.html Shared lecture card
database/
  schema.sql                   Normalized MySQL schema
  sample_data.sql              Fictional lecture records, tags, and topics
tests/                         Search, recommendation, filter, and route tests
.env.example                   MySQL environment variable names
requirements.txt               Python dependencies
```

## Install and configure

1. Install Python 3.10+ and MySQL 8+.
2. Open PowerShell in this project folder and create a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

3. Initialize the database. In PowerShell, from the project folder:

   ```powershell
   Get-Content -Raw .\database\schema.sql | mysql -u root -p
   Get-Content -Raw .\database\sample_data.sql | mysql -u root -p
   ```

   The seed script is intended to be loaded once into a newly initialized schema because it inserts fixed sample IDs.

4. Copy `.env.example` to `.env` in the project root, then edit `.env` and enter the root password you created during MySQL setup. For example:

   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```

   The application loads `.env` from the project root, regardless of the current PowerShell directory. Values in this file take precedence over variables inherited from old PowerShell tabs. `.env` is ignored by Git; never share or commit it. The listed `DB_USER=root` is convenient for local development. A separate MySQL account with read access can be used instead.

## Run

With the virtual environment active, `.env` configured, and MySQL running, start one development server from the project folder:

```powershell
python -m app
```

Open http://127.0.0.1:5000. The homepage and lecture library read their records from MySQL. If MySQL settings are missing or the server is unavailable, pages show a setup message and the Flask terminal logs the specific connection error. A lecture detail page displays the video controls only when the referenced file exists under `app/static/`; otherwise it shows instructions for adding a local file. The example video paths do not have bundled video files.

## Existing pages and project scope

The navigation and page layout follow the supplied Figma screenshots. Search is available in the homepage and lecture library. Department, category, and date filters can be combined with search. Accounts and administrator functions are not implemented.

## Phase 3 search and filtering

The lecture library uses the weighted relevance scoring and manual Merge Sort described in [Phase 3 search documentation](docs/PHASE3_SEARCH.md). Filters are applied before relevance ranking. An empty keyword keeps the database's newest-first order, while an empty result set displays a message and a Clear all link.

Run the automated checks from the project root:

```powershell
python -m unittest discover -s tests -v
```

The suite covers search fields, relevance weights, descending and stable sorting, filters, recommendation similarity, top 3 ranking, and Flask routes. Route tests use fictional in-memory rows and do not replace the separate real MySQL connection check. Recommendation details are in [PHASE4_RECOMMENDATION.md](docs/PHASE4_RECOMMENDATION.md).
