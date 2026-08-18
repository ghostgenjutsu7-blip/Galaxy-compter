---
name: recipe-send-team-announcement
source: GoogleWorkspaceCLI
version: 1.0.0
description: 'Send a team announcement via both Gmail and a Google Chat space.'
tags: ["google-workspace", "recipe"]
triggers: ["recipe send team announcement"]
license: Apache-2.0
target_agent: file
category: file_management
---

# Announce via Gmail and Google Chat

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-gmail`, `gws-chat`

Send a team announcement via both Gmail and a Google Chat space.

## Steps

1. Send email: `gws gmail +send --to team@company.com --subject 'Important Update' --body 'Please review the attached policy changes.'`
2. Post in Chat: `gws chat +send --space spaces/TEAM_SPACE --text '📢 Important Update: Please check your email for policy changes.'`
