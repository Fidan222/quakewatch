import streamlit as st
from store_quakes import get_all_quakes

st.set_page_config(page_title="QuakeWatch", layout="wide")

st.title("🌍 QuakeWatch")
st.subheader("Real-time earthquake data pipeline")

# Get data
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
    st.warning("No earthquakes recorded yet.")

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