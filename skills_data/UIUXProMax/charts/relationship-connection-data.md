---
name: Chart Pattern: Relationship / Connection Data
source: UIUXProMax
version: 1.0.0
description: Network Graph
tags: ["chart", "data-viz"]
triggers: ["Relationship / Connection Data"]
license: MIT
target_agent: design
category: data_viz
---

**No:** 16
**Data Type:** Relationship / Connection Data
**Keywords:** network, graph, nodes, edges, connections, relationships, force
**Best Chart Type:** Network Graph
**Secondary Options:** Hierarchical Tree, Adjacency Matrix
**When to Use:** Mapping connections between entities; network topology or social graph exploration context
**When NOT to Use:** Node count > 500 without clustering pre-applied; user needs precise connection counts; mobile context
**Data Volume Threshold:** ≤100 nodes: SVG; 101–500: Canvas; >500: must apply clustering/LOD before rendering
**Color Guidance:** Node types: categorical colors. Edges: #90A4AE at 60% opacity. Highlight path: #F59E0B
**Accessibility Grade:** D
**Accessibility Notes:** Fundamentally inaccessible without alternative. Never use as sole representation. Always provide list alternative.
**A11y Fallback:** Adjacency list table (Node A → Node B → Weight); hierarchical tree view when structure allows
**Library Recommendation:** D3.js (d3-force), Vis.js, Cytoscape.js
**Interactive Level:** Drilldown + Hover + Drag
