# 🛰️ Geoeconomic Intelligence Dashboard

A quarterly trade flow monitoring system for key global economic corridors built with Streamlit and PyDeck.

## Features

- **Heat Map Visualization**: Interactive 3D heat map showing trade intensity across major economic corridors
- **Time Series Analysis**: Slider control for 5 years of quarterly data (Q1 2021 - Q4 2025)
- **Economic Corridor Tracking**: Focus on critical global chokepoints including:
  - Strait of Hormuz
  - Red Sea / Suez Canal
  - Malacca Strait
  - South China Sea
  - Panama Canal
  - English Channel
  - Bosphorus Strait
  - Strait of Gibraltar
- **Trade Analytics**: Quarter-over-quarter comparison, corridor rankings, and historical trends
- **Live Filtering**: Real-time corridor selection with dynamic statistics
- **Professional UI**: Dark cyberpunk theme with heat map gradients

## Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/mwj97/geoeconomic-dashboard.git
cd geoeconomic-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository
5. Set main file path: `app.py`
6. Deploy!

## Project Structure

```
geoeconomics/
├── app.py                  # Main Streamlit application with corridor heat maps
├── data/
│   └── shipments.csv      # Legacy data (no longer used)
├── .streamlit/
│   └── config.toml        # Streamlit theme configuration
├── requirements.txt        # Python dependencies
├── packages.txt           # System packages (if needed)
└── README.md              # This file
```

## Data Model

The dashboard generates synthetic quarterly trade data for 8 major economic corridors:
- **Geographic Regions**: Each corridor defined by lat/lon boundaries
- **Quarterly Values**: Trade volumes calculated with growth trends and seasonal variation
- **Heat Map Points**: Generated dynamically based on trade intensity
- **Time Range**: Q1 2021 - Q4 2025 (20 quarters)

### Corridor Base Values (Annual Trade in Billions USD)
- South China Sea: $940B
- Strait of Hormuz: $850B
- Malacca Strait: $780B
- Red Sea / Suez Canal: $620B
- English Channel: $580B
- Strait of Gibraltar: $425B
- Panama Canal: $340B
- Bosphorus Strait: $285B

## Key Technologies

- **Streamlit**: Web framework
- **PyDeck**: 3D map visualization with HeatmapLayer
- **Pandas**: Data manipulation and time series analysis
- **NumPy**: Numerical operations and statistical modeling
- **Requests**: GeoJSON data fetching for country boundaries

## License

MIT License

## Author

Generated with Claude Code
