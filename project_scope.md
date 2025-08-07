# 📘 Investment Research Tool – Project Scope

## Summary

The **Investment Research Tool** is a modular, Python-based analytics project designed to identify and evaluate promising investment opportunities — starting with publicly traded stocks and ETFs. The tool supports data ingestion, performance benchmarking, fundamental and sector analysis, and research report generation. Future iterations will integrate LLMs (Large Language Models) to summarize and explain financial insights in natural language.

This project also serves as a platform to practice and document software engineering, data analytics, Git/GitHub workflows, and financial research methods.

---

## Goals

- Create a reusable framework for stock-level investment research
- Build modules for data ingestion, performance analysis, and reporting
- Integrate benchmark and sector comparisons
- Explore fundamentals and valuation techniques
- Generate research-ready reports (Markdown, PDF, HTML)
- (Future) Summarize insights using OpenAI/GPT or similar LLMs

---

## In Scope

| Category        | Included                                                                 |
|----------------|--------------------------------------------------------------------------|
| **Assets**     | US stocks and ETFs (e.g., AAPL, SPY, XLK)                                |
| **Data Sources** | Public APIs (e.g., `yfinance`, `yahooquery`, `fmp`), local CSVs           |
| **Metrics**    | Returns, volatility, Sharpe ratio, alpha/beta, technical indicators      |
| **Fundamentals** | PE, PEG, ROE, Debt/Equity, basic financial statements                    |
| **Valuation**  | Relative multiples and simple discounted cash flow (DCF)                 |
| **Sectors**    | Sector ETFs (e.g., XLK, XLF), peer group analysis                         |
| **Outputs**    | CSVs, plots, research reports (Markdown/PDF/HTML)                        |
| **Tech Stack** | Python (pandas, matplotlib, plotly, yfinance), Git, GitHub               |
| **Reporting**  | Modular reporting system per ticker or watchlist                         |
| **LLM Integration** | Phase 2 — GPT-generated summaries and Q&A over analysis                |

---

## Out of Scope (for Now)

| Category             | Not Included Yet                                                  |
|---------------------|--------------------------------------------------------------------|
| Real-time data streaming | No live data updates or trading signals                          |
| Options/futures/crypto  | Not prioritized in initial build                                 |
| Fundamental forecasting | No deep ML-based prediction modeling                             |
| Alternative data        | No social sentiment, web scraping, or NLP news feeds (yet)       |
| Deployment              | No Shiny or Streamlit front-end (can add later)                  |

---