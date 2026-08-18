---
name: recipe-draft-email-from-doc
source: GoogleWorkspaceCLI
version: 1.0.0
description: 'Read content from a Google Doc and use it as the body of a Gmail message.'
tags: ["google-workspace", "recipe"]
triggers: ["recipe draft email from doc"]
license: Apache-2.0
target_agent: file
category: file_management
---

# Draft a Gmail Message from a Google Doc

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-docs`, `gws-gmail`

Read content from a Google Doc and use it as the body of a Gmail message.

## Steps

1. Get the document content: `gws docs documents get --params '{"documentId": "DOC_ID"}'`
2. Copy the text from the body content
3. Send the email: `gws gmail +send --to recipient@example.com --subject 'Newsletter Update' --body 'CONTENT_FROM_DOC'`
