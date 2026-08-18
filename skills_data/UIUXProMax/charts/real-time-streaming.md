---
name: Chart Pattern: Real-Time Streaming
source: UIUXProMax
version: 1.0.0
description: Streaming Area Chart
tags: ["chart", "data-viz"]
triggers: ["Real-Time Streaming"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 23
**Data Type:** Real-Time Streaming
**Keywords:** streaming, real-time, ticker, live, velocity, pulse, monitoring
**Best Chart Type:** Streaming Area Chart
**Secondary Options:** Ticker Tape, Moving Gauge
**When to Use:** Live monitoring dashboards; IoT/ops data updating at ≥1 Hz; user needs current value at a glance
**When NOT to Use:** Update frequency < 1/min (use periodic-refresh line chart); flashing content without reduced-motion support
**Data Volume Threshold:** Canvas/WebGL required. Buffer last 60–300s of data. Downsample older data on scroll
**Color Guidance:** Current pulse: #00FF00 (dark theme) or #0080FF (light theme). History: fading opacity. Grid: dark background
**Accessibility Grade:** B
**Accessibility Notes:** Pause/resume control required. Current value as large visible text KPI. Respect prefers-reduced-motion.
**A11y Fallback:** Pause/resume button required; current value shown as large text KPI; prefers-reduced-motion: freeze animation
**Library Recommendation:** Smoothed D3.js, CanvasJS
**Interactive Level:** Real-time + Pause + Zoom
