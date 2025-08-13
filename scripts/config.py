"""
Configuration file for investment data ingestion scripts.

Edit the settings below to customize the data download parameters.
This file is shared between the prices and fundamentals scripts.
"""

from pathlib import Path
from datetime import datetime, timedelta

class Config:
    """Main configuration class"""
    
    # ---- Stock Selection ----
    TICKERS = [
        "AAPL",   # Apple Inc.
        "MSFT",   # Microsoft Corporation  
        "GOOGL",  # Alphabet Inc.
        # "TSLA",   # Tesla Inc.
        # "AMZN",   # Amazon.com Inc.
        # "NVDA",   # NVIDIA Corporation
        # "META",   # Meta Platforms Inc.
    ]
    
   
    
    # Alternative: Dynamic dates (uncomment to use)
    END_DATE = datetime.now().strftime("%Y-%m-%d")  # Today
    START_DATE = (datetime.now() - timedelta(days=1825)).strftime("%Y-%m-%d")  # 5 years ago
    
    # ---- Data Parameters ----
    INTERVAL = "1d"  # Options: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    
    # ---- File Options ----
    SAVE_INDIVIDUAL_FILES = True  # Save separate CSV for each ticker
    SAVE_COMBINED_FILES = True    # Save combined CSV with all tickers
    SAVE_PICKLE_FILES = True      # Save pickle files for faster loading
    
    # ---- Directory Structure ----
    # Auto-detect project structure
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent
    
    # Data directories
    DATA_DIR = PROJECT_ROOT / 'data' / 'raw'
    PRICES_DIR = DATA_DIR / 'prices'
    FUNDAMENTALS_DIR = DATA_DIR / 'fundamentals'
    
    # Output directories
    OUTPUT_DIR = PROJECT_ROOT / 'output'
    REPORTS_DIR = OUTPUT_DIR / 'reports'
    
    # ---- API Settings ----
    # Rate limiting (seconds between requests)
    REQUEST_DELAY = 0.1
    
    # Retry settings
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0
    
    # ---- Logging ----
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    LOG_TO_FILE = False
    LOG_DIR = PROJECT_ROOT / 'logs'
    
    @classmethod
    def create_directories(cls):
        """Create all necessary directories"""
        directories = [
            cls.DATA_DIR,
            cls.PRICES_DIR, 
            cls.FUNDAMENTALS_DIR,
            cls.OUTPUT_DIR,
            cls.REPORTS_DIR,
        ]
        
        if cls.LOG_TO_FILE:
            directories.append(cls.LOG_DIR)
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        errors = []
        
        # Check date format
        try:
            datetime.strptime(cls.START_DATE, "%Y-%m-%d")
            datetime.strptime(cls.END_DATE, "%Y-%m-%d")
        except ValueError:
            errors.append("Dates must be in YYYY-MM-DD format")
        
        # Check date order
        if cls.START_DATE >= cls.END_DATE:
            errors.append("START_DATE must be before END_DATE")
        
        # Check tickers
        if not cls.TICKERS:
            errors.append("TICKERS list cannot be empty")
        
        # Check interval
        valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
        if cls.INTERVAL not in valid_intervals:
            errors.append(f"INTERVAL must be one of: {valid_intervals}")
        
        if errors:
            raise ValueError(f"Configuration errors: {'; '.join(errors)}")
        
        return True
    
    @classmethod
    def summary(cls):
        """Print configuration summary"""
        print("⚙️  Configuration Summary")
        print("=" * 40)
        print(f"Tickers: {', '.join(cls.TICKERS)}")
        print(f"Date Range: {cls.START_DATE} to {cls.END_DATE}")
        print(f"Interval: {cls.INTERVAL}")
        print(f"Individual files: {cls.SAVE_INDIVIDUAL_FILES}")
        print(f"Combined files: {cls.SAVE_COMBINED_FILES}")
        print(f"Project Root: {cls.PROJECT_ROOT}")
        print(f"Data Directory: {cls.DATA_DIR}")
        print("")


# Environment-specific configurations (optional)
class DevConfig(Config):
    """Development environment settings"""
    TICKERS = ["AAPL"]  # Just one ticker for faster testing
    START_DATE = "2024-01-01"
    END_DATE = "2024-01-31"
    LOG_LEVEL = "DEBUG"


class ProdConfig(Config):
    """Production environment settings"""
    LOG_TO_FILE = True
    MAX_RETRIES = 5


# Choose which config to use (you can change this)
# Uncomment one of these lines:
# ActiveConfig = DevConfig    # For development/testing
ActiveConfig = Config         # For normal use
# ActiveConfig = ProdConfig   # For production


if __name__ == "__main__":
    # Test the configuration
    try:
        ActiveConfig.validate_config()
        ActiveConfig.summary()
        print("✅ Configuration is valid!")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")