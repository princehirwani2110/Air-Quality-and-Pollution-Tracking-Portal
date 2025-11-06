import os
import json
import datetime
import csv
from collections import defaultdict
import utils

load_json = utils.load_json
save_json = utils.save_json
gen_id = utils.gen_id
print_table = utils.print_table
safe_float = utils.safe_float
find_by_id = utils.find_by_id
ADMIN_CREDENTIALS = utils.ADMIN_CREDENTIALS


def admin_login():
    print("Admin login")
    u = input("Username: ").strip()
    p = input("Password: ").strip()
    if u == ADMIN_CREDENTIALS["username"] and p == ADMIN_CREDENTIALS["password"]:
        print("Logged in as admin.")
        return True
    print("Invalid credentials.")
    return False

def admin_menu():
    while True:
        print("--- Admin Menu ---")
        print("1. Add Air Quality Record")
        print("2. Update/Delete Air Record")
        print("3. Manage Pollutants")
        print("4. Upload Bulk Data (JSON/CSV)")
        print("5. Generate Reports")
        print("6. Manage Alerts")
        print("7. Back to Main Menu")
        ch = input("Choice: ").strip()
        if ch == "1":
            add_air_quality_record()
        elif ch == "2":
            update_delete_aq_record()
        elif ch == "3":
            manage_pollutants()
        elif ch == "4":
            upload_bulk_data()
        elif ch == "5":
            generate_reports()
        elif ch == "6":
            manage_alerts()
        elif ch == "7":
            break
        else:
            print("Invalid choice.")

def add_air_quality_record():
    air = load_json("air")
    pollutants_list = load_json("pollutants")
    print("Add Air Quality Record")
    region = input("Region / City: ").strip()
    date = input("Date (YYYY-MM-DD): ").strip()
    if date == "":
        date = str(datetime.date.today())
    aqi = safe_float(input("AQI (numeric): ").strip() or 0)
    pollutant_levels = {}
    print("Enter pollutant levels (blank to skip):")
    for p in pollutants_list:
        name = p.get("name")
        val = input(f"  {name}: ").strip()
        if val != "":
            pollutant_levels[name] = safe_float(val)
    rec = {
        "record_id": gen_id("rec"),
        "region": region,
        "date": date,
        "AQI": int(aqi),
        "pollutants": pollutant_levels,
        "health_risk": ""
    }
    air.append(rec)
    save_json("air", air)
    print("Record added.")


def update_delete_aq_record():
    air = load_json("air")
    if not air:
        print("No air quality records available.")
        return
    rows = [[r["record_id"], r["region"], r["date"], r["AQI"]] for r in air]
    print_table(rows, headers=["ID", "Region", "Date", "AQI"])
    rid = input("Enter record_id to update/delete (blank to cancel): ").strip()
    if not rid:
        return
    rec = find_by_id(air, "record_id", rid)
    if not rec:
        print("Record not found.")
        return
    action = input("Enter 'u' to update, 'd' to delete, anything else to cancel: ").strip().lower()
    if action == "d":
        air = [r for r in air if r["record_id"] != rid]
        save_json("air", air)
        print("Deleted.")
    elif action == "u":
        rec["region"] = input(f"Region [{rec['region']}]: ").strip() or rec['region']
        rec["date"] = input(f"Date [{rec['date']}]: ").strip() or rec['date']
        aqi_in = input(f"AQI [{rec['AQI']}]: ").strip()
        if aqi_in != "":
            rec["AQI"] = int(safe_float(aqi_in, rec["AQI"]))
        for k in list(rec.get("pollutants", {}).keys()):
            newv = input(f"{k} [{rec['pollutants'].get(k,'')}]: ").strip()
            if newv != "":
                rec['pollutants'][k] = safe_float(newv)
        save_json("air", air)
        print("Updated.")
    else:
        print("Cancelled.")


def manage_pollutants():
    while True:
        pollutants = load_json("pollutants")
        rows = [[p["pollutant_id"], p["name"], p.get("description",""), p.get("safe_limit","")] for p in pollutants]
        print_table(rows, headers=["ID", "Name", "Description", "Safe limit"])
        print("Options: 1.Add 2.Update 3.Delete 4.Back")
        ch = input("Choice: ").strip()
        if ch == "1":
            name = input("Name: ").strip()
            desc = input("Description: ").strip()
            sl = input("Safe limit (numeric): ").strip()
            pollutants.append({"pollutant_id": gen_id("pol"), "name": name, "description": desc, "safe_limit": safe_float(sl)})
            save_json("pollutants", pollutants)
            print("Pollutant added.")
        elif ch == "2":
            pid = input("Pollutant ID to update: ").strip()
            p = find_by_id(pollutants, "pollutant_id", pid)
            if not p:
                print("Not found.")
                continue
            p["name"] = input(f"Name [{p['name']}]: ").strip() or p["name"]
            p["description"] = input(f"Description [{p.get('description','')}]: ").strip() or p.get("description","")
            sl = input(f"Safe limit [{p.get('safe_limit','')}]: ").strip()
            if sl != "":
                p["safe_limit"] = safe_float(sl)
            save_json("pollutants", pollutants)
            print("Updated.")
        elif ch == "3":
            pid = input("Pollutant ID to delete: ").strip()
            pollutants = [x for x in pollutants if x["pollutant_id"] != pid]
            save_json("pollutants", pollutants)
            print("Deleted if existed.")
        elif ch == "4":
            break
        else:
            print("Invalid choice.")


def upload_bulk_data():
    path = input("Enter path to JSON or CSV file: ").strip()
    if not os.path.exists(path):
        print("File not found.")
        return
    ext = os.path.splitext(path)[1].lower()
    air = load_json("air")
    if ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            for rec in data:
                if "record_id" not in rec:
                    rec["record_id"] = gen_id("rec")
                air.append(rec)
            save_json("air", air)
            print(f"Imported {len(data)} records.")
        else:
            print("JSON must be a list of records.")
    elif ext == ".csv":
        pollutants = [p["name"] for p in load_json("pollutants")]
        with open(path, newline="", encoding="utf-8") as cf:
            reader = csv.DictReader(cf)
            added = 0
            for row in reader:
                rec = {
                    "record_id": gen_id("rec"),
                    "region": row.get("region", ""),
                    "date": row.get("date", str(datetime.date.today())),
                    "AQI": int(safe_float(row.get("AQI",0))),
                    "pollutants": {},
                    "health_risk": row.get("health_risk","")
                }
                for pn in pollutants:
                    if pn in row and row[pn] != "":
                        rec["pollutants"][pn] = safe_float(row[pn])
                air.append(rec)
                added += 1
            save_json("air", air)
            print(f"Imported {added} rows from CSV.")
    else:
        print("Unsupported file type. Use .json or .csv")


def generate_reports():
    air = load_json("air")
    if not air:
        print("No data available.")
        return
    print("Report options: 1.Top polluted regions (avg AQI) 2.Monthly trend for a region 3.Alerts summary 4.Back")
    ch = input("Choice: ").strip()
    if ch == "1":
        region_map = defaultdict(list)
        for r in air:
            region_map[r["region"]].append(r.get("AQI",0))
        rows = [[region, round(sum(vals)/len(vals),1), len(vals)] for region, vals in region_map.items()]
        rows.sort(key=lambda x: x[1], reverse=True)
        print_table(rows, headers=["Region", "Average AQI", "Records"])
    elif ch == "2":
        region = input("Region: ").strip()
        rows = [r for r in air if r["region"].lower() == region.lower()]
        if not rows:
            print("No data for that region.")
            return
        monthly = defaultdict(list)
        for r in rows:
            try:
                d = datetime.datetime.strptime(r["date"], "%Y-%m-%d")
                key = f"{d.year}-{d.month:02d}"
            except Exception:
                key = r["date"]
            monthly[key].append(r.get("AQI",0))
        data = sorted([(k, sum(v)/len(v)) for k,v in monthly.items()])
        print_table(data, headers=["Month", "Avg AQI"])
    elif ch == "3":
        alerts = load_json("alerts")
        if not alerts:
            print("No alerts.")
            return
        rows = [[a["alert_id"], a["region"], a["AQI_level"], a["status"], a["issue_date"]] for a in alerts]
        print_table(rows, headers=["ID","Region","AQI_level","Status","Issue date"])
    else:
        return


def manage_alerts():
    alerts = load_json("alerts")
    print("1.Issue alert 2.Withdraw alert 3.Back")
    ch = input("Choice: ").strip()
    if ch == "1":
        region = input("Region: ").strip()
        level = input("AQI level: ").strip()
        issue_date = str(datetime.date.today())
        expiry = input("Expiry date (YYYY-MM-DD) or blank: ").strip()
        alerts.append({"alert_id": gen_id("alert"), "region": region, "AQI_level": level, "status": "active", "issue_date": issue_date, "expiry_date": expiry})
        save_json("alerts", alerts)
        print("Alert issued.")
    elif ch == "2":
        aid = input("Alert ID to withdraw: ").strip()
        a = find_by_id(alerts, "alert_id", aid)
        if a:
            a["status"] = "withdrawn"
            save_json("alerts", alerts)
            print("Alert withdrawn.")
    else:
        return
