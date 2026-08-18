---
name: recipe-log-deal-update
source: GoogleWorkspaceCLI
version: 1.0.0
description: 'Append a deal status update to a Google Sheets sales tracking spreadsheet.'
tags: ["google-workspace", "recipe"]
triggers: ["recipe log deal update"]
license: Apache-2.0
target_agent: file
category: file_management
---

# Log Deal Update to Sheet

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-sheets`, `gws-drive`

Append a deal status update to a Google Sheets sales tracking spreadsheet.

## Steps

1. Find the tracking sheet: `gws drive files list --params '{"q": "name = '\''Sales Pipeline'\'' and mimeType = '\''application/vnd.google-apps.spreadsheet'\''"}'`
2. Read current data: `gws sheets +read --spreadsheet SHEET_ID --range "Pipeline!A1:F"`
3. Append new row: `gws sheets +append --spreadsheet SHEET_ID --range 'Pipeline' --values '["2024-03-15", "Acme Corp", "Proposal Sent", "$50,000", "Q2", "jdoe"]'`
