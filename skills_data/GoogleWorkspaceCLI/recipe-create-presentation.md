---
name: recipe-create-presentation
source: GoogleWorkspaceCLI
version: 1.0.0
description: 'Create a new Google Slides presentation and add initial slides.'
tags: ["google-workspace", "recipe"]
triggers: ["recipe create presentation"]
license: Apache-2.0
target_agent: file
category: file_management
---

# Create a Google Slides Presentation

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-slides`

Create a new Google Slides presentation and add initial slides.

## Steps

1. Create presentation: `gws slides presentations create --json '{"title": "Quarterly Review Q2"}'`
2. Get the presentation ID from the response
3. Share with team: `gws drive permissions create --params '{"fileId": "PRESENTATION_ID"}' --json '{"role": "writer", "type": "user", "emailAddress": "team@company.com"}'`
