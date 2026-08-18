---
name: recipe-batch-invite-to-event
source: GoogleWorkspaceCLI
version: 1.0.0
description: 'Add a list of attendees to an existing Google Calendar event and send notifications.'
tags: ["google-workspace", "recipe"]
triggers: ["recipe batch invite to event"]
license: Apache-2.0
target_agent: file
category: file_management
---

# Add Multiple Attendees to a Calendar Event

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-calendar`

Add a list of attendees to an existing Google Calendar event and send notifications.

## Steps

1. Get the event: `gws calendar events get --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'`
2. Add attendees: `gws calendar events patch --params '{"calendarId": "primary", "eventId": "EVENT_ID", "sendUpdates": "all"}' --json '{"attendees": [{"email": "alice@company.com"}, {"email": "bob@company.com"}, {"email": "carol@company.com"}]}'`
3. Verify attendees: `gws calendar events get --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'`
