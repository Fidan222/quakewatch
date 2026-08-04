import json
from datetime import datetime

def validate_earthquake(quake):
    """
    Check if an earthquake record is valid.
    Returns: (is_valid, reason_if_invalid)
    """
    props = quake.get("properties", {})
    geometry = quake.get("geometry", {})
    
    # Check if magnitude exists and is reasonable
    mag = props.get("mag")
    if mag is None:
        return False, "Missing magnitude"
    if mag < -2 or mag > 10:
        return False, f"Unreasonable magnitude: {mag}"
    
    # Check if location exists
    if not geometry.get("coordinates"):
        return False, "Missing coordinates"
    
    coords = geometry["coordinates"]
    lon, lat = coords[0], coords[1]
    
    # Sanity check coordinates (lat -90 to 90, lon -180 to 180)
    if lat < -90 or lat > 90 or lon < -180 or lon > 180:
        return False, f"Invalid coordinates: {lon}, {lat}"
    
    # Check if time exists
    if not props.get("time"):
        return False, "Missing timestamp"
    
    return True, None

def process_earthquakes(raw_data):
    """
    Filter raw earthquake data and return clean records + stats.
    """
    if not raw_data:
        return [], {}
    
    features = raw_data.get("features", [])
    clean = []
    rejected = []
    seen_ids = set()  # Prevent duplicates
    
    for quake in features:
        quake_id = quake.get("id")
        
        # Check for duplicates
        if quake_id in seen_ids:
            rejected.append({"id": quake_id, "reason": "Duplicate event ID"})
            continue
        
        # Validate
        is_valid, reason = validate_earthquake(quake)
        if not is_valid:
            rejected.append({"id": quake_id, "reason": reason})
            continue
        
        # Good record
        seen_ids.add(quake_id)
        clean.append(quake)
    
    stats = {
        "total_received": len(features),
        "valid": len(clean),
        "rejected": len(rejected),
        "rejection_reasons": {}
    }
    
    # Count why records were rejected
    for item in rejected:
        reason = item["reason"]
        stats["rejection_reasons"][reason] = stats["rejection_reasons"].get(reason, 0) + 1
    
    return clean, stats

if __name__ == "__main__":
    # Test it with the fetch script
    from fetch_quakes import fetch_earthquakes
    
    print("Fetching and validating earthquakes...\n")
    raw_data = fetch_earthquakes()
    clean_quakes, stats = process_earthquakes(raw_data)
    
    print(f"Results:")
    print(f"  Total received: {stats['total_received']}")
    print(f"  Valid: {stats['valid']}")
    print(f"  Rejected: {stats['rejected']}")
    
    if stats['rejection_reasons']:
        print(f"\nRejection breakdown:")
        for reason, count in stats['rejection_reasons'].items():
            print(f"    {reason}: {count}")
    
    print(f"\nFirst 3 valid earthquakes:")
    for quake in clean_quakes[:3]:
        props = quake["properties"]
        mag = props.get("mag")
        place = props.get("place")
        print(f"  M{mag} — {place}")