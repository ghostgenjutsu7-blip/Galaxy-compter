---
name: recipe-schedule-recurring-event
source: GoogleWorkspaceCLI
version: 1.0.0
description: 'Create a recurring Google Calendar event with attendees.'
tags: ["google-workspace", "recipe"]
triggers: ["recipe schedule recurring event"]
license: Apache-2.0
target_agent: file
category: file_management
---

# Schedule a Recurring Meeting

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-calendar`

Create a recurring Google Calendar event with attendees.

## Steps

1. Create recurring event: `gws calendar events insert --params '{"calendarId": "primary"}' --json '{"summary": "Weekly Standup", "start": {"dateTime": "2024-03-18T09:00:00", "timeZone": "America/New_York"}, "end": {"dateTime": "2024-03-18T09:30:00", "timeZone": "America/New_York"}, "recurrence": ["RRULE:FREQ=WEEKLY;BYDAY=MO"], "attendees": [{"email": "team@company.com"}]}'`
2. Verify it was created: `gws calendar +agenda --days 14 --format table`
