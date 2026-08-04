import streamlit as st
from store_quakes import get_all_quakes, init_database, save_earthquakes
from fetch_quakes import fetch_earthquakes
from validate_quakes import process_earthquakes

st.set_page_config(page_title="QuakeWatch", layout="wide")

# Make sure the database exists
init_database()

st.title("🌍 QuakeWatch")
st.subheader("Real-time earthquake data pipeline")

# Fetch Latest section
st.markdown("### Update Data")
if st.button("🔄 Fetch Latest Earthquakes"):
    with st.spinner("Fetching from USGS..."):
        raw_data = fetch_earthquakes()
        clean_quakes, stats = process_earthquakes(raw_data)
        saved, skipped = save_earthquakes(clean_quakes)
    st.success(f"Fetched {stats['total_received']} quakes — saved {saved} new, skipped {skipped} duplicates.")

# Get data (refreshed after fetch)
quakes = get_all_quakes()

# AI Summary section
st.markdown("### AI Summary")
if st.button("Generate Summary"):
    try:
        from summarize_quakes import summarize_earthquakes
        summary = summarize_earthquakes()
        st.info(summary)
    except Exception as e:
        st.error(f"Error generating summary: {e}")

# Show recent earthquakes
st.markdown("### Recent Earthquakes")

if quakes:
    data = []
    for mag, place, timestamp in quakes:
        data.append({
            "Magnitude": f"M{mag}",
            "Location": place,
            "Time": timestamp
        })
    
    st.dataframe(data, use_container_width=True)
    st.caption(f"Total in database: {len(quakes)}")
else:
    st.warning("No earthquakes recorded yet. Click 'Fetch Latest' to load some.")

# Stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Recorded", len(quakes))
with col2:
    if quakes:
        max_mag = max([q[0] for q in quakes])
        st.metric("Largest", f"M{max_mag}")
with col3:
    st.caption("Data from USGS")