# Hybrid Publishing Model

This project is structured for a hybrid release.

## Public repository

Publish these safely:
- source code
- rubric and configuration
- templates
- methodology and deployment docs
- sanitized sample inputs and outputs
- the reusable skill definition

## Private archive

Keep these private:
- entrant submission PDFs and DOCX files
- extracted text from real submissions
- internal score sheets tied to real entrants
- judge notes and feedback intended for internal review only
- organizer-only reports or calibration material that should not be public

## Why hybrid is the right choice

It lets others reuse the judging engine without exposing client, entrant, or program-sensitive material.

## Recommended GitHub setup

### Repo 1, public
`ai-awards-judge`

Contains reusable framework and documentation.

### Repo 2, private
`ai-awards-judge-private-data`

Contains original submissions, internal outputs, and any client-specific artifacts.

## Operational rule

Never commit private archive material to the public repo, even temporarily.
