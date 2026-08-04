import requests
from datetime import datetime

# Fetch earthquake data from USGS
def fetch_earthquakes():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an error if the request failed
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Print the data nicely
if __name__ == "__main__":
    print("Fetching earthquakes from USGS...")
    quakes = fetch_earthquakes()
    
    if quakes:
        features = quakes.get("features", [])
        print(f"\nFound {len(features)} earthquakes in the last hour:\n")
        
        for quake in features[:5]:  # Print first 5
            props = quake["properties"]
            mag = props.get("mag", "N/A")
            place = props.get("place", "Unknown")
            print(f"  M{mag} — {place}")
    else:
        print("Failed to fetch data.")