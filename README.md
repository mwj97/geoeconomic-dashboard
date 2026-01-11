# 🛰️ Geoeconomic Intelligence Dashboard

A real-time defense & aerospace trade flow monitoring system built with Streamlit and PyDeck.

## Features

- **3D Globe Visualization**: Interactive 3D map with trade flow arcs
- **Risk-Based Intelligence**: Color-coded routes (Red=High, Yellow=Medium, Blue=Low)
- **Compliance Monitoring**: Automated detection of high-risk shipments on flags of convenience
- **Live Filtering**: Real-time risk level filtering with dynamic statistics
- **Professional UI**: Dark cyberpunk theme with neon accents

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
├── app.py                  # Main Streamlit application
├── data/
│   └── shipments.csv      # Trade route data (15 routes)
├── .streamlit/
│   └── config.toml        # Streamlit theme configuration
├── requirements.txt        # Python dependencies
├── packages.txt           # System packages (if needed)
└── README.md              # This file
```

## Data Schema

The `shipments.csv` contains:
- Origin/Destination cities with coordinates
- Risk level (High/Medium/Low)
- Shipment value in USD
- Vessel type (Container Ship, Oil Tanker, Bulk Carrier)
- Flag state (country of vessel registration)

## Key Technologies

- **Streamlit**: Web framework
- **PyDeck**: 3D map visualization
- **Pandas**: Data manipulation
- **NumPy**: Numerical operations

## Compliance Intelligence

The dashboard automatically flags high-risk shipments using flags of convenience:
- Panama
- Liberia
- Marshall Islands

Alerts are displayed in real-time below the map.

## License

MIT License

## Author

Generated with Claude Code
