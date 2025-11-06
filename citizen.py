from collections import defaultdict
import datetime
import utils

load_json = utils.load_json
save_json = utils.save_json
find_by_id = utils.find_by_id
print_table = utils.print_table


def register_citizen():
    citizens = load_json("citizens")
    print("Register new citizen")
    name = input("Name: ").strip()
    age = input("Age: ").strip()
    location = input("Location / Region: ").strip()
    contact = input("Contact (email/phone): ").strip()
    n=name.split()
    nn="cit_"+n[0]
    citizen = {"citizen_id": nn, "name": name, "age": age, "location": location, "contact": contact}
    citizens.append(citizen)
    save_json("citizens", citizens)
    print("Registered. Your Citizen ID:", citizen["citizen_id"])


def citizen_login():
    citizens = load_json("citizens")
    cid = input("Enter Citizen ID: ").strip()
    c = find_by_id(citizens, "citizen_id", cid)
    if c:
        citizen_menu(c)
    else:
        print("Citizen not found. Please register.")


def citizen_menu(citizen):
    while True:
        print(f"--- Citizen Menu ({citizen['name']}) ---\n")
        print("1.View Current Air Quality (your region)\n")
        print("2.Search Historical AQI Data\n")
        print("3.View Pollution Trends (text)\n")
        print("4.Access Health Guidelines\n")
        print("5.Manage Profile\n")
        print("6.Logout\n")
        ch = input("Choice: ").strip()
        if ch == "1":
            view_current_aqi(citizen)
        elif ch == "2":
            search_historical_data()
        elif ch == "3":
            view_trends()
        elif ch == "4":
            access_guidelines()
        elif ch == "5":
            manage_profile(citizen)
        elif ch == "6":
            break
        else:
            print("Invalid choice.")


def view_current_aqi(citizen):
    region = citizen.get("location","")
    air = load_json("air")
    region_records = [r for r in air if r["region"].lower() == region.lower()]
    if not region_records:
        print(f"No AQI data for region: {region}")
        return
    region_records.sort(key=lambda r: r["date"], reverse=True)
    r = region_records[0]
    print_table([[r["date"], r["region"], r["AQI"], r.get("pollutants",{})]], headers=["Date","Region","AQI","Pollutants"])
    alerts = load_json("alerts")
    for a in alerts:
        if a["region"].lower() == region.lower() and a["status"] == "active":
            print(f"ALERT: {a['AQI_level']} issued on {a['issue_date']} (id {a['alert_id']})")


def search_historical_data():
    air = load_json("air")
    if not air:
        print("No air quality data available.")
        return
    print("Search by:1.Date\n2.Region\n3.Pollutant\n4.All Regions (latest AQI per region)\n5.Back")
    ch = input("Choice: ").strip()
    results = []
    if ch == "1":
        d = input("Date (YYYY-MM-DD): ").strip()
        results = [r for r in air if r["date"] == d]
    elif ch == "2":
        reg = input("Region: ").strip().lower()
        results = [r for r in air if r["region"].lower() == reg]
    elif ch == "3":
        pol = input("Pollutant name (e.g. PM2.5): ").strip()
        results = [r for r in air if pol in r.get("pollutants",{})]
    elif ch == "4":
        latest = {}
        for r in air:
            key = r["region"]
            if key not in latest or r["date"] > latest[key]["date"]:
                latest[key] = r
        results = list(latest.values())
    else:
        return
    if not results:
        print("No matches found.")
        return
    rows = [[r.get("record_id"), r.get("date"), r.get("region"), r.get("AQI"), r.get("pollutants",{})] for r in results]
    print_table(rows, headers=["ID","Date","Region","AQI","Pollutants"])


def view_trends():
    print("Trend view (text-only). Use Generate Reports to see aggregated stats.")


def access_guidelines():
    guides = load_json("guidelines")
    if not guides:
        print("No guidelines available.")
        return
    rows = [[g.get("guide_id"), g.get("AQI_range"), g.get("precautions")] for g in guides]
    print_table(rows, headers=["ID","AQI Range","Precautions"])


def manage_profile(citizen):
    citizens = load_json("citizens")
    found = find_by_id(citizens, "citizen_id", citizen["citizen_id"])
    if not found:
        print("Profile not found.")
        return
    found["name"] = input(f"Name [{found['name']}]: ").strip() or found["name"]
    age = input(f"Age [{found.get('age','')}]: ").strip()
    if age != "":
        found["age"] = age
    found["location"] = input(f"Location [{found.get('location','')}]: ").strip() or found.get("location")
    found["contact"] = input(f"Contact [{found.get('contact','')}]: ").strip() or found.get("contact")
    save_json("citizens", citizens)
    print("Profile updated.")
