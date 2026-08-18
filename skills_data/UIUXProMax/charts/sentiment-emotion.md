---
name: Chart Pattern: Sentiment / Emotion
source: UIUXProMax
version: 1.0.0
description: Word Cloud with Sentiment
tags: ["chart", "data-viz"]
triggers: ["Sentiment / Emotion"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 24
**Data Type:** Sentiment / Emotion
**Keywords:** sentiment, emotion, nlp, opinion, feeling, text-analysis
**Best Chart Type:** Word Cloud with Sentiment
**Secondary Options:** Sentiment Arc, Radar Chart
**When to Use:** NLP output visualization; exploratory analysis of text corpus sentiment; frequency-weighted keyword overview
**When NOT to Use:** Precise values matter (word size is inherently imprecise); screen-reader context; corpus < 50 items
**Data Volume Threshold:** 50–5000 terms optimal. Beyond 5000: apply top-N filtering before render. Avoid on mobile
**Color Guidance:** Positive: #22C55E. Negative: #EF4444. Neutral: #94A3B8. Word size maps to frequency
**Accessibility Grade:** C
**Accessibility Notes:** Word clouds fail screen readers. Never use as sole output of NLP analysis. Always pair with list view.
**A11y Fallback:** Sortable list view by frequency with sentiment label column; word cloud as supplementary only
**Library Recommendation:** D3-cloud, Highcharts, Nivo
**Interactive Level:** Hover + Filter
