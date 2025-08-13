"""
Investment Data Ingestion Script

This script downloads price and fundamental data for specified stocks
and saves them as CSV files for further analysis.

Usage:
    python ingest_data.py
    
Configuration:
    Edit the TICKERS, START_DATE, END_DATE variables below
"""

import os
import sys
from datetime import datetime
import json
import pandas as pd
from yahooquery import Ticker
import yfinance as yf
from pathlib import Path
import argparse
from typing import List, Optional


# ---- Configuration ----
class Config:
    """Configuration class to hold all settings"""
    # Default settings
    TICKERS = ["AAPL", "MSFT", "GOOGL"]  # Edit these as needed
    START_DATE = "2020-01-01"
        # (datetime.now() - timedelta(days=1825)).strftime("%Y-%m-%d")  # 5 years ago
    END_DATE = datetime.now().strftime("%Y-%m-%d")  # Today
    INTERVAL = "1d"
    SAVE_INDIVIDUAL = True
    
    # Paths
    NB_CWD = Path.cwd()
    PROJECT_ROOT = NB_CWD.parent if NB_CWD.name != 'scripts' else NB_CWD.parent
    DATA_DIR = PROJECT_ROOT / 'data' / 'raw'
    PRICES_DIR = DATA_DIR / "prices"
    FUNDS_DIR = DATA_DIR / "fundamentals"



def setup_directories():
    """Create necessary directories"""
    for directory in (Config.DATA_DIR, Config.PRICES_DIR, Config.FUNDS_DIR):
        directory.mkdir(parents=True, exist_ok=True)
    
    print("📁 Directory structure:")
    print(f"   Data: {Config.DATA_DIR}")
    print(f"   Prices: {Config.PRICES_DIR}")
    print(f"   Fundamentals: {Config.FUNDS_DIR}")

# ---- Download Prices Function (yahooquery - RECOMMENDED) ----
def get_prices(tickers, start: str, end: str, interval: str = "1d", save: bool = True):
    """
    Download tidy daily OHLCV for a list of tickers using yahooquery.
    Returns one long/tidy DataFrame and (optionally) writes per-ticker CSVs.
    
    Args:
        tickers: List of ticker symbols or single ticker string
        start: Start date in YYYY-MM-DD format
        end: End date in YYYY-MM-DD format
        interval: Data interval (default "1d")
        save: Whether to save individual CSV files
    
    Returns:
        pd.DataFrame: Combined tidy DataFrame with all ticker data
    """
    if isinstance(tickers, str):
        tickers = [tickers]
    
    all_prices = []
    ordered_columns = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume", "ticker"]
    
    for tk in tickers:
        try:
            print(f"📈 Downloading {tk}...")
            
            ticker_obj = Ticker(tk)
            df = ticker_obj.history(start=start, end=end, interval=interval)
            
            if df.empty:
                print(f"⚠️  No data found for {tk}")
                continue
            
            # Reset index to get date as column
            df = df.reset_index()
            
            # Add ticker column
            df["ticker"] = tk
            
            # Rename columns to match standard format
            column_mapping = {
                'date': 'Date',
                'open': 'Open', 
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'adjclose': 'Adj Close',
                'volume': 'Volume'
            }
            df = df.rename(columns=column_mapping)
            
            # Keep only available columns
            available_columns = [c for c in ordered_columns if c in df.columns]
            df = df[available_columns]
            
            # Ensure Date is datetime
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')
            
            if save:
                clean_start = start.replace('-', '')
                clean_end = end.replace('-', '')
                filename = f"{tk.lower()}_{clean_start}_{clean_end}_{interval}.csv"
                filepath = Config.PRICES_DIR / filename
                df.to_csv(filepath, index=False)
                print(f"✅ Saved {len(df)} records for {tk} → {filename}")
            
            all_prices.append(df)
            
        except Exception as e:
            print(f"❌ Error downloading {tk}: {str(e)}")
            continue
    
    if all_prices:
        combined = pd.concat(all_prices, ignore_index=True)
        if 'Date' in combined.columns and 'ticker' in combined.columns:
            combined = combined.sort_values(['ticker', 'Date']).reset_index(drop=True)
        
        print(f"🎉 Successfully combined data for {len(combined['ticker'].unique())} tickers, {len(combined)} total records")
        return combined
    else:
        print("⚠️  No data was successfully downloaded")
        return pd.DataFrame()

# ---- Fallback using yfinance (if needed) ----
def get_prices_yfinance_fallback(tickers, start: str, end: str, interval: str = "1d", save: bool = True):
    """
    Fallback function using yfinance if yahooquery fails.
    """
    if isinstance(tickers, str):
        tickers = [tickers]
    
    all_prices = []
    ordered_columns = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume", "ticker"]
    
    for tk in tickers:
        try:
            print(f"📈 Downloading {tk} via yahooquery...")
            
            ticker_obj = Ticker(tk)
            df = ticker_obj.history(start=start, end=end, interval=interval)
            
            if df.empty:
                print(f"⚠️  No data found for {tk}")
                continue
            
            # Reset index to get date as column
            df = df.reset_index()
            
            # Add ticker column
            df["ticker"] = tk
            
            # Rename columns to match yfinance format
            column_mapping = {
                'date': 'Date',
                'open': 'Open', 
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'adjclose': 'Adj Close',
                'volume': 'Volume'
            }
            df = df.rename(columns=column_mapping)
            
            # Keep only available columns
            available_columns = [c for c in ordered_columns if c in df.columns]
            df = df[available_columns]
            
            # Ensure Date is datetime
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')
            
            if save:
                clean_start = start.replace('-', '')
                clean_end = end.replace('-', '')
                filename = f"{tk.lower()}_{clean_start}_{clean_end}_{interval}_yq.csv"
                filepath = Config.PRICES_DIR / filename
                df.to_csv(filepath, index=False)
                print(f"✅ Saved {len(df)} records for {tk} → {filename}")
            
            all_prices.append(df)
            
        except Exception as e:
            print(f"❌ Error downloading {tk}: {str(e)}")
            continue
    
    if all_prices:
        combined = pd.concat(all_prices, ignore_index=True)
        if 'Date' in combined.columns and 'ticker' in combined.columns:
            combined = combined.sort_values(['ticker', 'Date']).reset_index(drop=True)
        
        print(f"🎉 Successfully combined data for {len(combined['ticker'].unique())} tickers, {len(combined)} total records")
        return combined
    else:
        return pd.DataFrame()
    
def save_combined_prices(prices_df: pd.DataFrame, start_date: str, end_date: str) -> None:
    """Save combined price data to CSV"""
    if not prices_df.empty:
        clean_start = start_date.replace('-', '')
        clean_end = end_date.replace('-', '')
        
        combined_filename = f"combined_prices_{clean_start}_{clean_end}.csv"
        combined_filepath = Config.PRICES_DIR / combined_filename
        
        prices_df.to_csv(combined_filepath, index=False)
        print(f"✅ Saved combined data: {combined_filename}")
        print(f"📊 Total records: {len(prices_df)}")
        print(f"📈 Tickers: {', '.join(prices_df['ticker'].unique())}")
        
        # Optional: Save as pickle for faster loading
        pickle_filepath = Config.PRICES_DIR / f"combined_prices_{clean_start}_{clean_end}.pkl"
        prices_df.to_pickle(pickle_filepath)
        print(f"✅ Also saved as pickle: {pickle_filepath.name}")
        
        # Data summary
        print(f"\n📋 Data Summary:")
        print(f"Date range: {prices_df['Date'].min().date()} to {prices_df['Date'].max().date()}")
        print(f"Records per ticker:")
        for ticker in sorted(prices_df['ticker'].unique()):
            count = len(prices_df[prices_df['ticker'] == ticker])
            print(f"  {ticker}: {count} records")
    else:
        print("⚠️ No data to save - combined DataFrame is empty")

def main():
    """Main execution function"""
    print("🚀 Investment Data Ingestion Script")
    print("=" * 50)
    
    # Setup directories
    setup_directories()
    
    # Use config values directly
    tickers = Config.TICKERS
    start_date = Config.START_DATE
    end_date = Config.END_DATE
    interval = Config.INTERVAL
    save_individual = Config.SAVE_INDIVIDUAL
    
    # DEBUG: Print all paths
    print(f"\n🔍 DEBUG - File Paths:")
    print(f"   Current working directory: {Path.cwd()}")
    print(f"   Script directory: {Config.NB_CWD}")
    print(f"   Project root: {Config.PROJECT_ROOT}")
    print(f"   Data directory: {Config.DATA_DIR}")
    print(f"   Prices directory: {Config.PRICES_DIR}")
    print(f"   Prices dir exists: {Config.PRICES_DIR.exists()}")
    

    # Configuration summary
    print(f"\n⚙️  Configuration:")
    print(f"   Tickers: {tickers}")
    print(f"   Date range: {start_date} to {end_date}")
    print(f"   Interval: {interval}")
    print(f"   Save individual files: {save_individual}")
    print("")
    
    # Download price data
    print("📈 Starting price data download...")
    price_results = []
    
    for tk in tickers:
        try:
            dfp = get_prices([tk], start_date, end_date, interval, save=save_individual)
            if not dfp.empty:
                price_results.append(dfp)
        except Exception as e:
            print(f"❌ Price fetch failed for {tk}: {e}")
    
    # Combine and save price data
    prices_df = pd.concat(price_results, ignore_index=True) if price_results else pd.DataFrame()
    save_combined_prices(prices_df, start_date, end_date)
    
    print(f"\n✅ Script completed successfully!")
    return prices_df


if __name__ == "__main__":
    try:
        result = main()
    except KeyboardInterrupt:
        print("\n⚠️  Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Script failed with error: {e}")
        sys.exit(1)