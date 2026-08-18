---
name: recipe-find-large-files
source: GoogleWorkspaceCLI
version: 1.0.0
description: 'Identify large Google Drive files consuming storage quota.'
tags: ["google-workspace", "recipe"]
triggers: ["recipe find large files"]
license: Apache-2.0
target_agent: file
category: file_management
---

# Find Largest Files in Drive

> **PREREQUISITE:** Load the following skills to execute this recipe: `gws-drive`

Identify large Google Drive files consuming storage quota.

## Steps

1. List files sorted by size: `gws drive files list --params '{"orderBy": "quotaBytesUsed desc", "pageSize": 20, "fields": "files(id,name,size,mimeType,owners)"}' --format table`
2. Review the output and identify files to archive or move
