---
name: recipe-share-event-materials
source: GoogleWorkspaceCLI
version: 1.0.0
description: 'Share Google Drive files with all attendees of a Google Calendar event.'
tags: ["google-workspace", "recipe"]
triggers: ["recipe share event materials"]
license: Apache-2.0
target_agent: file
category: file_management
---

# Share Files with Meeting Attendees

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-calendar`, `gws-drive`

Share Google Drive files with all attendees of a Google Calendar event.

## Steps

1. Get event attendees: `gws calendar events get --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'`
2. Share file with each attendee: `gws drive permissions create --params '{"fileId": "FILE_ID"}' --json '{"role": "reader", "type": "user", "emailAddress": "attendee@company.com"}'`
3. Verify sharing: `gws drive permissions list --params '{"fileId": "FILE_ID"}' --format table`
