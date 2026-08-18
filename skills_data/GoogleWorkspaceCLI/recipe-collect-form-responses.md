---
name: recipe-collect-form-responses
source: GoogleWorkspaceCLI
version: 1.0.0
description: 'Retrieve and review responses from a Google Form.'
tags: ["google-workspace", "recipe"]
triggers: ["recipe collect form responses"]
license: Apache-2.0
target_agent: file
category: file_management
---

# Check Form Responses

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-forms`

Retrieve and review responses from a Google Form.

## Steps

1. List forms: `gws forms forms list` (if you don't have the form ID)
2. Get form details: `gws forms forms get --params '{"formId": "FORM_ID"}'`
3. Get responses: `gws forms forms responses list --params '{"formId": "FORM_ID"}' --format table`
