import requests
import pandas as pd
from datetime import datetime
import pytz
import time

# --- 1. Stadium coordinates (Premier League 2015–2023) ---
stadium_coords = {
    "Arsenal": (51.5549, -0.1084),
    "Aston Villa": (52.5090, -1.8847),
    "Bournemouth": (50.7352, -1.8383),
    "Brentford": (51.4907, -0.3020),
    "Brighton": (50.8609, -0.0837),
    "Burnley": (53.7890, -2.2300),
    "Chelsea": (51.4817, -0.1910),
    "Crystal Palace": (51.3983, -0.0856),
    "Everton": (53.4388, -2.9663),
    "Fulham": (51.4749, -0.2216),
    "Huddersfield": (53.6543, -1.7682),
    "Hull": (53.7461, -0.3665),
    "Leeds": (53.7778, -1.5733),
    "Leicester": (52.6204, -1.1422),
    "Liverpool": (53.4308, -2.9609),
    "Man City": (53.4831, -2.2004),
    "Man United": (53.4631, -2.2913),
    "Middlesbrough": (54.5780, -1.2170),
    "Newcastle": (54.9756, -1.6217),
    "Norwich": (52.6220, 1.3093),
    "Sheffield United": (53.3703, -1.4700),
    "Southampton": (50.9058, -1.3911),
    "Stoke": (52.9884, -2.1751),
    "Sunderland": (54.9144, -1.3883),
    "Swansea": (51.6422, -3.9340),
    "Tottenham": (51.6043, -0.0664),
    "Watford": (51.6498, -0.4016),
    "West Brom": (52.5090, -1.9635),
    "West Ham": (51.5386, -0.0165),
    "Wolves": (52.5903, -2.1304),
}

# --- 2. Helper: fetch weather from Open-Meteo ---
def get_weather(lat, lon, dt_utc):
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": dt_utc.strftime("%Y-%m-%d"),
        "end_date": dt_utc.strftime("%Y-%m-%d"),
        "hourly": "temperature_2m,precipitation,weathercode,windspeed_10m",
        "timezone": "UTC"
    }
    try:
        r = requests.get(base_url, params=params)
        r.raise_for_status()
        data = r.json()
        times = data["hourly"]["time"]
        idx = times.index(dt_utc.strftime("%Y-%m-%dT%H:00"))
        return {
            "temperature_C": data["hourly"]["temperature_2m"][idx],
            "precip_mm": data["hourly"]["precipitation"][idx],
            "weathercode": data["hourly"]["weathercode"][idx],
            "windspeed": data["hourly"]["windspeed_10m"][idx],
        }
    except Exception as e:
        print(f"Weather fetch failed for {dt_utc}: {e}")
        return None

# --- 3. Convert Date/Time to UTC (handle 2- or 4-digit years) ---
def parse_datetime(date_str, time_str):
    formats = ["%d/%m/%y %H:%M", "%d/%m/%Y %H:%M"]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str + " " + str(time_str), fmt)
            london = pytz.timezone("Europe/London")
            local_dt = london.localize(dt)
            return local_dt.astimezone(pytz.UTC)
        except ValueError:
            continue
    raise ValueError(f"Date format not recognized: {date_str} {time_str}")

# --- 4. Loop over all seasons 2015–16 to 2022–23 ---
all_data = []
# season_codes = ["1516","1617","1718","1819","1920","2021","2122","2223"]

# season_codes = ["1516","1617","1718","1819","1920","2021","2122"] # Training data
season_codes = ["2223"] # Prediction data 

for code in season_codes:
    url = f"https://www.football-data.co.uk/mmz4281/{code}/E0.csv"
    try:
        fixtures = pd.read_csv(url)
        # print(fixtures.columns)
    except Exception as e:
        print(f"Could not fetch season {code}: {e}")
        continue

    if not {"Date", "HomeTeam", "AwayTeam"}.issubset(fixtures.columns):
        print(f"Missing columns in season {code}, skipping")
        continue
    
    if "Time" not in fixtures.columns:
        fixtures["Time"] = "15:00"

    fixtures = fixtures[["Date", "Time", "HomeTeam", "AwayTeam"]]
    fixtures["KickoffUTC"] = fixtures.apply(lambda x: parse_datetime(str(x.Date), str(x.Time)), axis=1)
    fixtures["Season"] = code

    weather_data = []
    for i, row in fixtures.iterrows():
        team = row["HomeTeam"]
        if team not in stadium_coords:
            weather_data.append(None)
            continue
        lat, lon = stadium_coords[team]
        w = get_weather(lat, lon, row["KickoffUTC"])
        weather_data.append(w)
        time.sleep(1)  # avoid hammering API

    fixtures["Weather"] = weather_data
    all_data.append(fixtures)

# --- 5. Combine all seasons ---
all_fixtures = pd.concat(all_data, ignore_index=True)

# Expand weather dict into columns
weather_df = pd.json_normalize(all_fixtures["Weather"])
final = pd.concat([all_fixtures.drop(columns=["Weather"]), weather_df], axis=1)

# --- 6. Save CSV ---
final.to_csv("training_weather_2223.csv", index=False)
print("prediction_weather_2223.csv")
