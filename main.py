import os
import streamlit as st
import requests
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
if not API_KEY:
    st.error("Please set OPENWEATHER_API_KEY in your .env file.")
    st.stop()

# --- Database setup ---
DB_URL = "sqlite:///weather_history.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Lookup(Base):
    __tablename__ = 'lookups'
    id = Column(Integer, primary_key=True)
    location = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    data = Column(JSON, nullable=False)

Base.metadata.create_all(engine)

# --- Streamlit UI ---
st.title("🔆 Python Weather App")

location = st.text_input("Enter location (city, ZIP, etc.)")

if st.button("Get Weather"):
    if not location:
        st.warning("Please enter a location.")
    else:
        # Build ZIP-aware URL
        if location.isdigit() and len(location) == 5:
            api_url = (
                f"https://api.openweathermap.org/data/2.5/weather?"
                f"zip={location},us&units=metric&appid={API_KEY}"
            )
        else:
            api_url = (
                f"https://api.openweathermap.org/data/2.5/weather?"
                f"q={location}&units=metric&appid={API_KEY}"
            )

        # Debug: show the exact URL being requested
        st.write("📡 Requesting:", api_url)

        resp = requests.get(api_url)

        # Handle response
        if resp.status_code == 200:
            weather = resp.json()
            st.subheader(f"Current weather in {weather['name']}:")
            st.write(f"• Condition: {weather['weather'][0]['description'].title()}")
            st.write(f"• Temperature: {weather['main']['temp']}°C")
            # Save to database
            record = Lookup(location=location, data=weather)
            session.add(record)
            session.commit()
        else:
            # Show real API error message
            err = resp.json().get("message", resp.text)
            st.error(f"Error {resp.status_code}: {err}")

# Separator
st.markdown("---")

# --- Lookup history ---
st.subheader("📜 Lookup History")
lookups = session.query(Lookup).order_by(Lookup.timestamp.desc()).all()
for item in lookups:
    cols = st.columns([3, 1])
    cols[0].write(f"{item.id}. {item.location} at {item.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    if cols[1].button("Delete", key=f"del_{item.id}"):
        session.delete(item)
        session.commit()
        st.experimental_rerun()
