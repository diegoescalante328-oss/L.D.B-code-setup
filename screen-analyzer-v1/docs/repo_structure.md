# Repo Structure

screen-analyzer-v1/
â”œâ”€â”€ README.md
â”œâ”€â”€ AGENTS.md
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ .env.example
â”œâ”€â”€ docs/
â”œâ”€â”€ config/
â”œâ”€â”€ schemas/
â”œâ”€â”€ prompts/
â”œâ”€â”€ app/
â”‚   â”œâ”€â”€ main.py
â”‚   â”œâ”€â”€ camera/
â”‚   â”œâ”€â”€ analysis/
â”‚   â”œâ”€â”€ ui/
â”‚   â””â”€â”€ storage/
â”œâ”€â”€ scripts/
â”œâ”€â”€ tests/
â””â”€â”€ legacy_notes/

## Important note
This repo is structured so Codex can read the docs first, then fill in the app modules cleanly.
