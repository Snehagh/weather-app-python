# Python Weather App

A simple Streamlit-based weather application in pure Python.

## Features

- Enter a location (city name, ZIP code, etc.) to get current weather.
- Displays weather condition and temperature.
- Stores each lookup in a local SQLite database.
- Shows lookup history and allows deletion.

## Setup

1. **Unzip** the project folder.
2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set your `OPENWEATHER_API_KEY`.

5. **Run the app**:
   ```bash
   streamlit run main.py
   ```
6. **Open** the URL shown (usually http://localhost:8501) in your browser.

Enjoy!