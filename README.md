# Investment Analyzer
A Python-based tool for analyzing and researching stocks, sectors, benchmarks, and fundamentals

## Feature
- Ingest stock and benchmark data (price, volume, fundamentals)
- Analyze performance and technical indicators
- Compare across sectors and industries
- Calculate key ratios and valuations
- Auto-generate stock research reports
- Future: Use LLMs to summarize insights and answer questions

## Project Structure
├── data/ # Raw and processed data

├── scripts/ # Core analysis modules (ingestion, indicators, etc.)

├── notebooks/ # Jupyter or RMarkdown analysis

├── reports/ # Auto-generated research reports

├── dashboards/ # (Optional) Interactive dashboards

├── tests/ # Unit tests

├── requirements.txt

└── README.md

## Getting Started
### 1. Clone the Repo
```bash
git clone https://github.com/dberle22/investment_analyzer
cd investment-research-tool
```

### 2. Create and Activate a Virtual Environment
python -m venv venv
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

## Modules (Planned)
scripts/ingest.py: Stock & fundamentals data ingestion
scripts/performance.py: Returns and technicals
scripts/compare.py: Benchmark and peer comparison
scripts/valuation.py: Ratio and valuation models
scripts/reporting.py: PDF/Markdown reports
scripts/llm_insights.py: (coming soon) GPT-powered summaries

## Author
Dan Berle