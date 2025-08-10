# scripts/ingest.py

import os
import pandas as pd
import yfinance as yf
from yahooquery import Ticker
from datetime import datetime

# --- SETTINGS ---
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
os.makedirs(DATA_DIR, exist_ok=True)