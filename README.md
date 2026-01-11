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
├── DATA_SOURCES.md        # Comprehensive data source documentation and verification
├── .streamlit/
│   └── config.toml        # Streamlit theme configuration
├── requirements.txt        # Python dependencies
├── packages.txt           # System packages (if needed)
└── README.md              # This file
```

## Data Model

The dashboard generates synthetic quarterly trade data for 8 major economic corridors based on verified values from authoritative sources:
- **Geographic Regions**: Each corridor defined by lat/lon boundaries
- **Quarterly Values**: Trade volumes calculated with growth trends and seasonal variation
- **Heat Map Points**: Generated dynamically based on trade intensity
- **Time Range**: Q1 2021 - Q4 2025 (20 quarters)
- **Data Sources**: See [DATA_SOURCES.md](DATA_SOURCES.md) for comprehensive source documentation

### Corridor Base Values (Annual Trade in Billions USD)

**Verified from Authoritative Sources (January 2026):**
- **South China Sea: $5,300B** ($5.3 Trillion) - CSIS, ASEAN Maritime Outlook, U.S. EIA
- **Malacca Strait: $3,500B** ($3.5 Trillion) - Maritime & Port Authority of Singapore
- **Strait of Hormuz: $1,400B** ($1.4 Trillion) - U.S. EIA, IEA, UNCTAD
- **English Channel: $1,400B** ($1.4 Trillion) - UK Office for National Statistics
- **Strait of Gibraltar: $1,200B** ($1.2 Trillion) - UNCTAD (10% of global trade)
- **Red Sea / Suez Canal: $700B** - Suez Canal Authority (2024, impacted by disruptions)
- **Bosphorus Strait: $400B** - Turkish Ministry of Transport
- **Panama Canal: $270B** - Panama Canal Authority

**Total Annual Trade:** ~$14.2 Trillion across all 8 chokepoints

### Data Quality & Sources

All base values are derived from official government sources, international organizations, and authoritative maritime institutions:
- **UNCTAD** (UN Conference on Trade and Development)
- **U.S. Energy Information Administration (EIA)**
- **International Energy Agency (IEA)**
- **Panama Canal Authority** (ACP)
- **Suez Canal Authority** (SCA)
- **Maritime and Port Authority of Singapore** (MPA)
- **UK Office for National Statistics** (ONS)
- **Turkish Ministry of Transport and Infrastructure**
- **Center for Strategic and International Studies** (CSIS)

For detailed source documentation, methodology, and verification dates, see [DATA_SOURCES.md](DATA_SOURCES.md).

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
