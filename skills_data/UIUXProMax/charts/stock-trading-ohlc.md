---
name: Chart Pattern: Stock / Trading OHLC
source: UIUXProMax
version: 1.0.0
description: Candlestick Chart
tags: ["chart", "data-viz"]
triggers: ["Stock / Trading OHLC"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 15
**Data Type:** Stock / Trading OHLC
**Keywords:** stock, trading, ohlc, candlestick, finance, price, volume
**Best Chart Type:** Candlestick Chart
**Secondary Options:** OHLC Bar, Heikin-Ashi
**When to Use:** Financial time-series with Open/High/Low/Close data; trading or investment product context only
**When NOT to Use:** Non-financial audience; no OHLC data available (use line chart); accessibility-first context
**Data Volume Threshold:** Real-time: Canvas required. Historical: paginate by time range. Max 500 candles visible at once
**Color Guidance:** Bullish: #26A69A. Bearish: #EF5350. Volume bars: 40% opacity below. Body fill vs hollow for OHLC style
**Accessibility Grade:** B
**Accessibility Notes:** Provide OHLC data table. Colorblind: use fill vs outline pattern (bullish = filled, bearish = hollow).
**A11y Fallback:** OHLC data table with sortable columns; numeric summary panel (daily change %)
**Library Recommendation:** Lightweight Charts (TradingView), ApexCharts
**Interactive Level:** Real-time + Hover + Zoom
