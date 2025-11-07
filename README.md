# Air Quality & Pollution Tracking Portal (CLI)

A simple menu-driven command-line application to track air quality and pollutant data. The project provides two roles:

- **Admin** — manage air quality records, pollutants, alerts and generate reports.
- **Citizen** — register, view local AQI, search historical data and access health guidelines.

This repository is intentionally small and file-based (JSON files under `data/`) for learning and quick prototyping.

---

## Quick start

From the project root (where `main.py` is located) run:

```bash
python3 main.py
```

The program is interactive. Use the menu to login as Admin or Citizen, register a new citizen, or exit.

Admin credentials (default)

- Username: `admin`
- Password: `admin123`

Optional dependency

- `tabulate` — installs nicer table formatting. If not installed the app falls back to a plain text table.

```bash
pip install tabulate
```

---

## Project layout

- `main.py` — entry point. Calls `utils.ensure_sample_data()` and delegates role flows to `admin.py` and `citizen.py`.
- `admin.py` — all admin-facing functionality (login, add/update/delete records, manage pollutants, bulk upload, generate reports, manage alerts).
- `citizen.py` — citizen-facing functionality (register/login, view current AQI for citizen's location, search historical data, guidelines, profile management).
- `utils.py` — shared helpers: data path constants, JSON load/save, id generation, printing helpers, and sample-data generation.
- `data/` — contains JSON files used by the app:
  - `air_quality.json` — list of air/AQI records
  - `citizens.json` — registered citizen records
  - `pollutants.json` — pollutant definitions
  - `alerts.json` — active/withdrawn alerts
  - `guidelines.json` — health guidelines by AQI range

---

## Design & Implementation notes

### `main.py`
- Minimal logic: presents the main menu and calls into `admin` and `citizen` modules.
- Calls `utils.ensure_sample_data()` at startup to populate sample data on first run.

### `utils.py`
- Centralizes shared constants and helpers.
- Key helpers:
  - `ensure_data_dir()` — creates `data/` and empty JSON files if missing.
  - `load_json(name)` / `save_json(name, data)` — read/write to JSON files identified by keys in `FILES`.
  - `gen_id(prefix)` — creates short ids used across records (e.g., `rec_1234abcd`).
  - `print_table(rows, headers)` — pretty prints rows using `tabulate` when available.
  - `create_sample_data()` — generates sample pollutants, guidelines, citizens, 20 cities × 15 days of AQI, and a couple of alerts.

### `admin.py`
- Interactive admin menu with these main features:
  - Add air quality record
  - Update/delete an existing record
  - Manage pollutant definitions (add/update/delete)
  - Upload bulk data from JSON or CSV
  - Generate simple reports (top polluted regions by avg AQI, monthly trend, alerts summary)
  - Manage alerts (issue, withdraw)

Notes:
- Bulk CSV import depends on pollutant names as column headers for pollutant values.
- The module uses `utils` helpers to load/save JSON and print tables.

### `citizen.py`
- Citizen flows include:
  - Registering as a new citizen (returns a `citizen_id`)
  - Login by `citizen_id` which opens the citizen menu
  - View current AQI for the citizen's `location` (latest record for the region)
  - Search historical data (by date, region, pollutant, or latest per region)
  - Access health guidelines
  - Manage profile (update name/age/location/contact)

---

## Data formats / examples

### Air record (element in `air_quality.json`)

```json
{
  "record_id": "rec_ab12cd34",
  "region": "Delhi",
  "date": "2025-01-10",
  "AQI": 211,
  "pollutants": {"PM2.5": 120.5, "NO2": 40.2},
  "health_risk": ""
}
```

### Citizen (element in `citizens.json`)

```json
{"citizen_id":"cit_alice","name":"Alice","age":30,"location":"Delhi","contact":"alice@example.com"}
```

### Pollutant (element in `pollutants.json`)

```json
{"pollutant_id":"pol_pm25","name":"PM2.5","description":"Fine particulate matter (µg/m³)","safe_limit":60}
```

### Alert (element in `alerts.json`)

```json
{"alert_id":"alert_xxx","region":"Delhi","AQI_level":"Very Unhealthy","status":"active","issue_date":"2025-01-10","expiry_date":"2025-01-12"}
```

