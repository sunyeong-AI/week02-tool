# Weather Records Aggregation

This program summarizes hourly temperature and precipitation records for Toronto into daily minimum, maximum, mean temperature, and total precipitation. This is useful because it makes the hourly weather data easier to understand and compare by day.

## Data Source

https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.38&hourly=temperature_2m,precipitation&past_days=7&forecast_days=0&timezone=America/Toronto

The program downloads hourly temperature and precipitation records for the past 7 days.

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run

Run the program from the project directory:

```bash
python weather_records.py
```

The program downloads the weather records, calculates daily temperature and precipitation summaries, and writes the results to summary.json.

## Example Output

After running the program, `summary.json` is created:

```json
{
  "record_count": 168,
  "days_processed": 7,
  "daily_temperature": {
    "2026-09-24": {
      "min": 10.1,
      "max": 18.8,
      "mean": 14.754166666666668
    }
  },
  "daily_precipitation": {
    "2026-09-24": 0.0
  }
}
```
## Data Quirks

The API provides hourly records, so the same date appears many times. I extracted the date from each timestamp and grouped the hourly records by date. I also used a set comprehension to remove duplicate dates and count the number of days processed.

## Design Choices

- To store the temperature and precipitation values for each day, I used lists. This allows me to calculate the minimum, maximum, mean, and total values.

- To make it easier to store and find the values for each day, I used dictionaries to group the weather records by date.

- To remove duplicate dates and keep only unique dates, I used a set with a set comprehension. This is useful because I only need to count each date once.

- To match each time with its corresponding temperature or precipitation value, I used `zip()`. This helps keep the related values together while processing the records.

- To make each function have one main job and make the program easier to understand, I used separate functions for fetching data, calculating temperature, calculating precipitation, building the summary, and writing the JSON file.

## Known Limitations

The program only analyzes the past 7 days of weather data. The analysis period cannot be selected by the user. With more time, I would allow users to specify a start date and an end date for the analysis.