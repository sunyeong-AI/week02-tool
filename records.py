import requests

def fetch_records():
    """Fetch weather records from the Open-Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.38&hourly=temperature_2m,precipitation&past_days=7&forecast_days=0&timezone=America/Toronto"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data

def main():
    """Run the weather data aggregation program."""

if __name__ == "__main__":
    main()
    data = fetch_records()
    print(data.keys())