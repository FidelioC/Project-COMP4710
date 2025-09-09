import pandas as pd

# --- Load data ---
weather_df = pd.read_csv("EPL_weather_2015_2023.csv")
stats_df = pd.read_csv("match_stats.csv")

# --- Normalize Date formats ---
weather_df["Date"] = pd.to_datetime(weather_df["Date"], dayfirst=True).dt.strftime("%Y-%m-%d")
stats_df["Date"] = pd.to_datetime(stats_df["Date"]).dt.strftime("%Y-%m-%d")

# --- Merge on Date, HomeTeam, AwayTeam ---
merged_df = pd.merge(
    stats_df,
    weather_df[["Date", "HomeTeam", "AwayTeam", "temperature_C", "precip_mm", "weathercode", "windspeed"]],
    on=["Date", "HomeTeam", "AwayTeam"],
    how="left"
)

# --- Weather code mapping (Open-Meteo standard) ---
weather_map = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

# --- Add description column ---
merged_df["weather_description"] = merged_df["weathercode"].map(weather_map)

# --- Save result ---
merged_df.to_csv("merged_match_stats_with_weather.csv", index=False)
print("✅ Saved merged_match_stats_with_weather.csv")
