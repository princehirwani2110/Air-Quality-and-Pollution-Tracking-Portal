Air Quality & Pollution Tracking Portal (CLI)

Overview
--------
This is a simple menu-driven command-line application for tracking air quality and pollutant data. It supports two user roles:
- Admin: manage air quality records, pollutants, alerts and generate reports.
- Citizen: register, view local AQI, search historical data, and access health guidelines.

Repository layout
-----------------
- `main.py` - Entry point. Delegates to `admin.py` and `citizen.py`. Ensures sample data exists on first run.
- `admin.py` - Admin functions (login, add/update/delete air records, manage pollutants, upload bulk data, reports, alerts).
- `citizen.py` - Citizen functions (register/login, view current AQI, search historical data, guidelines, profile management).
- `utils.py` - Shared helpers: data file paths, JSON load/save, ID generator, table printing, sample-data creation.
- `data/` - JSON files used by the app: `air_quality.json`, `citizens.json`, `pollutants.json`, `alerts.json`, `guidelines.json`.

The program is interactive. The main menu options are:
1. Admin Login
2. Citizen Login
3. Register as New Citizen
4. Exit

Admin credentials
-----------------
- Username: `admin`
- Password: `admin123`

Dependencies
------------
- Standard Python 3 (tested with Python 3.8+).
- Optional: `tabulate` package for nicer table output. If it's not installed the app falls back to plain text tables. To install it:

Detailed code explanation
------------------------

This section explains the implementation and structure of the code so contributors can quickly understand and modify the project.

1) main.py
	 - Purpose: Single entry point for the CLI. It bootstraps sample data and delegates role-specific flows to `admin.py` and `citizen.py`.
	 - Key functions:
		 - `main_menu()` — calls `utils.ensure_sample_data()` then presents the main menu with 4 options (Admin login, Citizen login, Register, Exit). Delegates to `admin.admin_login`, `admin.admin_menu`, `citizen.citizen_login`, and `citizen.register_citizen`.
	 - Behavior notes: `main.py` intentionally contains no business logic besides delegation. This keeps CLI wiring separate from implementation.

2) utils.py
	 - Purpose: Shared utilities used by admin and citizen modules.
	 - Key constants:
		 - `BASE_DIR`, `DATA_DIR` — paths used for storing JSON files in `data/`.
		 - `FILES` — mapping name→filename (`air`, `citizens`, `pollutants`, `alerts`, `guidelines`).
		 - `ADMIN_CREDENTIALS` — default admin username/password (`admin` / `admin123`).
	 - Key functions and contracts:
		 - `ensure_data_dir()`
				 - Inputs: none
				 - Outputs: creates `data/` and empty JSON files if missing
				 - Errors: none (filesystem errors will raise normally)
		 - `load_json(name)`
				 - Inputs: `name` (one of keys in FILES)
				 - Outputs: Python object loaded from JSON file (list or dict); returns [] on parse errors
		 - `save_json(name, data)`
				 - Inputs: `name`, `data` (serializable)
				 - Outputs: writes JSON to file (pretty-printed); uses `default=str` for fallback serialization
		 - `gen_id(prefix='id')` — returns a short UUID-like id string prefixed with `prefix_`.
		 - `print_table(rows, headers=None)` — prints rows using `tabulate` if available, otherwise a simple textual table.
		 - `safe_float(x, default=0.0)` — safe conversion to float.
		 - `find_by_id(list_obj, key_name, key_value)` — simple linear search in a list of dicts.
		 - `create_sample_data()` & `ensure_sample_data()` — generate a small dataset (pollutants, guidelines, some citizens, 20 cities × 15 days of AQI records, and a couple of alerts) and save to the JSON files. `ensure_sample_data()` calls `create_sample_data()` when `pollutants` is empty.

	 - Data format examples (JSON objects):
		 - Air record (list element of `air_quality.json`):
			 {
				 "record_id": "rec_ab12cd34",
				 "region": "Delhi",
				 "date": "2025-01-10",
				 "AQI": 211,
				 "pollutants": {"PM2.5": 120.5, "NO2": 40.2, ...},
				 "health_risk": ""
			 }
		 - Citizen: {"citizen_id":"cit_xxx","name":"Alice","age":30,"location":"Delhi","contact":"..."}
		 - Pollutant: {"pollutant_id":"pol_...","name":"PM2.5","description":"...","safe_limit":60}
		 - Alert: {"alert_id":"alert_xxx","region":"Delhi","AQI_level":"Very Unhealthy","status":"active","issue_date":"2025-01-10","expiry_date":"2025-01-12"}

3) admin.py
	 - Purpose: All administrative features — managing air records and pollutants, uploading bulk data, creating/withdrawing alerts, and generating reports.
	 - Exported functions used by `main.py`:
		 - `admin_login()` — interactive prompt for username/password; returns True on success.
		 - `admin_menu()` — interactive admin menu loop.
	 - Important internal functions (callable from admin menu):
		 - `add_air_quality_record()` — prompts for region/date/AQI/pollutants and appends to air JSON.
		 - `update_delete_aq_record()` — displays all records, lets admin pick record_id and update or delete.
		 - `manage_pollutants()` — add/update/delete pollutant definitions.
		 - `upload_bulk_data()` — imports `.json` (list of records) or `.csv` (CSV fields) into `air` file.
		 - `generate_reports()` — three report types: top polluted regions (average AQI), monthly trend for a region, alerts summary.
		 - `manage_alerts()` — issue or withdraw alerts.

	 - Notes & edge-cases:
		 - `upload_bulk_data` expects JSON to be a list of records; CSV parsing uses pollutant names as column headers.
		 - No concurrency control: simultaneous processes writing to the same JSON files may corrupt data. Consider migrating to a small DB (SQLite) if multiple concurrent writers are needed.

4) citizen.py
	 - Purpose: Citizen-facing features — registration, login by citizen_id, viewing current AQI for a citizen's location, searching historical data, viewing guidelines, and updating profile.
	 - Exported functions used by `main.py`:
		 - `register_citizen()` — interactive registration; adds a citizen and prints the new `citizen_id`.
		 - `citizen_login()` — prompts for citizen_id and, if found, starts `citizen_menu()`.
	 - Internal functions used in the menu:
		 - `view_current_aqi(citizen)` — shows the latest AQI record for citizen's `location` and prints any active alerts.
		 - `search_historical_data()` — supports search by date, region, pollutant, or latest AQI per region.
		 - `access_guidelines()` — prints the health guidelines loaded from `guidelines.json`.
		 - `manage_profile(citizen)` — update name/age/location/contact and save changes.

Quick examples (interactive flows)
---------------------------------
- Admin: run program, select Admin Login → use `admin` / `admin123`, then pick options from Admin Menu to add records or generate reports.
- Citizen: select Register as New Citizen to get a `citizen_id`, then choose Citizen Login and enter that id to see the citizen menu.

