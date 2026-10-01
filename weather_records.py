import requests
import json
from pathlib import Path

def fetch_weather_records():
    """Fetch weather records from the Open-Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.38&hourly=temperature_2m,precipitation&past_days=7&forecast_days=0&timezone=America/Toronto"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    
    except requests.RequestException:
        print("Could not download the weather data.")
        return None

def calculate_daily_temperature(records):
    """Calculate daily minimum, maximum, and mean temperatures."""

    hourly_data = records["hourly"]
    times = hourly_data["time"]

    unique_dates = {time.split("T")[0] for time in times}

    temperatures = hourly_data["temperature_2m"]

    hourly_temp_records = zip(times, temperatures)
    daily_temperatures = {}

    for time, temperature in hourly_temp_records:

        try:
            temperature = float(temperature)
        except (TypeError, ValueError):
            continue

        date = time.split("T")[0]

        if date not in daily_temperatures:
            daily_temperatures[date] = []

        daily_temperatures[date].append(temperature)

    daily_temp_stats = {}

    for date, temperatures in daily_temperatures.items():
        minimum = min(temperatures)
        maximum = max(temperatures)
        mean = sum(temperatures) / len(temperatures)

        daily_temp_stats[date] = {
            "min": minimum,
            "max": maximum,
            "mean": mean
        }

    return daily_temp_stats, unique_dates

             
def calculate_daily_precipitation(records):
    """Calculate total precipitation for each day."""
    hourly_data = records["hourly"]
    times = hourly_data["time"]
    precipitations = hourly_data["precipitation"]
    hourly_precip_records = zip(times, precipitations)

    daily_precipitations = {}

    for time, precipitation in hourly_precip_records:

        try:
            precipitation = float(precipitation)
        except (TypeError, ValueError):
            continue

        if precipitation < 0:
            continue
        
        date = time.split("T")[0]

        if date not in daily_precipitations:
            daily_precipitations[date] = []

        daily_precipitations[date].append(precipitation)

    daily_precip_totals = {}

    for date, precipitations in daily_precipitations.items():
        total_precipitation = sum(precipitations)
        daily_precip_totals[date] = total_precipitation

    return daily_precip_totals

def build_summary(records, temperature_summary, precipitation_summary, unique_dates):
    """Build the final weather summary."""
    summary = {
        "source_url": "https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.38&hourly=temperature_2m,precipitation&past_days=7&forecast_days=0&timezone=America/Toronto",
        "record_count": len(records["hourly"]["time"]),
        "days_processed": len(unique_dates),
        "daily_temperature": temperature_summary,
        "daily_precipitation": precipitation_summary
    }

    return summary

def write_summary(summary):
    """Write the summary to a JSON file."""
    output_path = Path("summary.json")
    output_path.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8"
    )

def main():
    """Run the weather data aggregation program."""
    weather_data = fetch_weather_records()

    if weather_data is None:
        return
    
    temperature_summary, unique_dates = calculate_daily_temperature(weather_data)
    precipitation_summary = calculate_daily_precipitation(weather_data)
    summary = build_summary(weather_data, temperature_summary, precipitation_summary, unique_dates)
    write_summary(summary)

if __name__ == "__main__":
    main()
    
    