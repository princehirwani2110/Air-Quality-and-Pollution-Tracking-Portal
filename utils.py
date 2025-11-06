import os
import json
import uuid
import random
import datetime
from collections import defaultdict

try:
    from tabulate import tabulate
except Exception:
    tabulate = None

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
FILES = {
    "air": "air_quality.json",
    "citizens": "citizens.json",
    "pollutants": "pollutants.json",
    "alerts": "alerts.json",
    "guidelines": "guidelines.json",
}

ADMIN_CREDENTIALS = {"username": "admin", "password": "admin123"}


def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    for fn in FILES.values():
        path = os.path.join(DATA_DIR, fn)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)


def load_json(name):
    ensure_data_dir()
    path = os.path.join(DATA_DIR, FILES[name])
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []


def save_json(name, data):
    ensure_data_dir()
    path = os.path.join(DATA_DIR, FILES[name])
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)


def gen_id(prefix="id"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def print_table(rows, headers=None):
    if tabulate:
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        if headers:
            print(" | ".join(headers))
            print("-" * max(40, len(headers) * 10))
        for r in rows:
            print(" | ".join(str(x) for x in r))


def safe_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default


def find_by_id(list_obj, key_name, key_value):
    for item in list_obj:
        if item.get(key_name) == key_value:
            return item
    return None

def create_sample_data():
    pollutants = [
        {"pollutant_id":"pol_pm25","name":"PM2.5","description":"Fine particulate matter (µg/m³)","safe_limit":60},
        {"pollutant_id":"pol_pm10","name":"PM10","description":"Coarse particulate matter (µg/m³)","safe_limit":100},
        {"pollutant_id":"pol_no2","name":"NO2","description":"Nitrogen dioxide (µg/m³)","safe_limit":80},
        {"pollutant_id":"pol_co","name":"CO","description":"Carbon monoxide (mg/m³)","safe_limit":10},
        {"pollutant_id":"pol_o3","name":"O3","description":"Ozone (µg/m³)","safe_limit":120},
        {"pollutant_id":"pol_so2","name":"SO2","description":"Sulfur dioxide (µg/m³)","safe_limit":80},
    ]
    save_json("pollutants", pollutants)

    guidelines = [
        {"guide_id":"g1","AQI_range":"0-50","precautions":"Good: No health impacts expected."},
        {"guide_id":"g2","AQI_range":"51-100","precautions":"Moderate: Unusually sensitive people should consider reducing prolonged outdoor exertion."},
        {"guide_id":"g3","AQI_range":"101-200","precautions":"Unhealthy: Sensitive groups should reduce prolonged outdoor exertion."},
        {"guide_id":"g4","AQI_range":"201-300","precautions":"Very Unhealthy: Avoid outdoor activities."},
        {"guide_id":"g5","AQI_range":"301-500","precautions":"Hazardous: Remain indoors and use protective measures."},
    ]
    save_json("guidelines", guidelines)

    citizens = [
        {"citizen_id":"cit_alice","name":"Alice","age":30,"location":"Delhi","contact":"alice@example.com"},
        {"citizen_id":"cit_bob","name":"Bob","age":40,"location":"Mumbai","contact":"bob@example.com"}
    ]
    save_json("citizens", citizens)

    cities = ["Delhi","Mumbai","Kolkata","Chennai","Bengaluru","Hyderabad","Ahmedabad","Pune","Lucknow","Jaipur",
              "Bhopal","Visakhapatnam","Surat","Kanpur","Nagpur","Indore","Thane","Agra","Vadodara","Nashik"]
    air = []
    random.seed(42)
    for city in cities:
        for day in range(1,16): 
            date = datetime.date(2025,1,day).isoformat()
            aqi = random.randint(50,400)
            pm25 = round(aqi * random.uniform(0.3,0.9),1)
            pm10 = round(aqi * random.uniform(0.4,1.0),1)
            no2 = round(aqi * random.uniform(0.05,0.25),1)
            co = round(random.uniform(0.2,5.0) * (aqi/100.0),2)
            o3 = round(random.uniform(10,150) * (aqi/200.0),1)
            so2 = round(random.uniform(5,80) * (aqi/200.0),1)
            rec = {"record_id": gen_id("rec"), "region": city, "date": date, "AQI": aqi,
                   "pollutants": {"PM2.5": pm25, "PM10": pm10, "NO2": no2, "CO": co, "O3": o3, "SO2": so2},
                   "health_risk": ""}
            air.append(rec)
    save_json("air", air)

    alerts = [
        {"alert_id": gen_id("alert"), "region": "Delhi", "AQI_level": "Very Unhealthy", "status": "active", "issue_date": "2025-01-10", "expiry_date": "2025-01-12"},
        {"alert_id": gen_id("alert"), "region": "Kanpur", "AQI_level": "Hazardous", "status": "active", "issue_date": "2025-01-08", "expiry_date": "2025-01-11"},
    ]
    save_json("alerts", alerts)
    print("Sample data created in data/")


def ensure_sample_data():
    ensure_data_dir()
    if not load_json("pollutants"):
        create_sample_data()
