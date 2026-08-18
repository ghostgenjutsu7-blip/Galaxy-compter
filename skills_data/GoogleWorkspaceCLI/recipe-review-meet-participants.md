---
name: recipe-review-meet-participants
source: GoogleWorkspaceCLI
version: 1.0.0
description: 'Review who attended a Google Meet conference and for how long.'
tags: ["google-workspace", "recipe"]
triggers: ["recipe review meet participants"]
license: Apache-2.0
target_agent: file
category: file_management
---

# Review Google Meet Attendance

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-meet`

Review who attended a Google Meet conference and for how long.

## Steps

1. List recent conferences: `gws meet conferenceRecords list --format table`
2. List participants: `gws meet conferenceRecords participants list --params '{"parent": "conferenceRecords/CONFERENCE_ID"}' --format table`
3. Get session details: `gws meet conferenceRecords participants participantSessions list --params '{"parent": "conferenceRecords/CONFERENCE_ID/participants/PARTICIPANT_ID"}' --format table`
