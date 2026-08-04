import sqlite3
from datetime import datetime

def init_database():
    """Create the earthquakes table if it doesn't exist."""
    conn = sqlite3.connect("quakes.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS earthquakes (
            id TEXT PRIMARY KEY,
            magnitude REAL,
            place TEXT,
            latitude REAL,
            longitude REAL,
            depth REAL,
            time_ms INTEGER,
            timestamp TEXT,
            url TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_earthquakes(clean_quakes):
    """Save cleaned earthquakes to database. Skips duplicates."""
    conn = sqlite3.connect("quakes.db")
    cursor = conn.cursor()
    
    saved = 0
    skipped = 0
    
    for quake in clean_quakes:
        quake_id = quake.get("id")
        props = quake["properties"]
        geometry = quake["geometry"]
        
        mag = props.get("mag")
        place = props.get("place")
        coords = geometry["coordinates"]
        lon, lat = coords[0], coords[1]
        depth = coords[2] if len(coords) > 2 else None
        time_ms = props.get("time")
        url = props.get("url")
        
        # Convert milliseconds to readable timestamp
        timestamp = datetime.fromtimestamp(time_ms / 1000).isoformat() if time_ms else None
        
        try:
            cursor.execute("""
                INSERT INTO earthquakes 
                (id, magnitude, place, latitude, longitude, depth, time_ms, timestamp, url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (quake_id, mag, place, lat, lon, depth, time_ms, timestamp, url))
            saved += 1
        except sqlite3.IntegrityError:
            # Duplicate ID — already in database
            skipped += 1
    
    conn.commit()
    conn.close()
    
    return saved, skipped

def get_all_quakes():
    """Fetch all earthquakes from database."""
    conn = sqlite3.connect("quakes.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT magnitude, place, timestamp FROM earthquakes ORDER BY time_ms DESC")
    results = cursor.fetchall()
    conn.close()
    
    return results

if __name__ == "__main__":
    from fetch_quakes import fetch_earthquakes
    from validate_quakes import process_earthquakes
    
    print("Initializing database...")
    init_database()
    
    print("Fetching and validating earthquakes...\n")
    raw_data = fetch_earthquakes()
    clean_quakes, stats = process_earthquakes(raw_data)
    
    print(f"Saving {stats['valid']} valid earthquakes to database...")
    saved, skipped = save_earthquakes(clean_quakes)
    
    print(f"  Saved: {saved}")
    print(f"  Skipped (duplicates): {skipped}\n")
    
    print("All earthquakes in database:")
    all_quakes = get_all_quakes()
    for mag, place, timestamp in all_quakes[:5]:
        print(f"  M{mag} — {place} ({timestamp})")
    
    print(f"\nTotal in database: {len(all_quakes)}")