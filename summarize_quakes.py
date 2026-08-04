import os
from dotenv import load_dotenv
import anthropic
from store_quakes import get_all_quakes

# Load API key from .env
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# If running on Streamlit Cloud, get the key from Streamlit secrets
if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass

def summarize_earthquakes():
    """Use Claude to write a plain-English summary of recent earthquakes."""
    
    # Get all quakes from database
    quakes = get_all_quakes()
    
    if not quakes:
        return "No earthquakes recorded yet."
    
    # Format quakes into a list for Claude
    quake_list = "\n".join([
        f"- M{mag} near {place} at {timestamp}"
        for mag, place, timestamp in quakes
    ])
    
    # Create the prompt
    prompt = f"""Here are recent earthquake records:

{quake_list}

Write a 2-3 sentence plain-English summary. Include:
1. How many earthquakes
2. The largest magnitude and where
3. Any notable patterns

Keep it under 50 words. Be conversational."""
    
    # Call Claude
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=100,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

if __name__ == "__main__":
    print("Generating earthquake summary...\n")
    summary = summarize_earthquakes()
    print(f"Summary:\n{summary}")