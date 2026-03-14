# Builder Ledger

Builder Ledger is a secure, offline-first Electron desktop application specifically designed for construction project financial management. It replaces manual ledger notebooks with a role-based, local-first digital system.

## Key Features
- **100% Offline**: Runs entirely on the local machine without internet dependency.
- **Role-Based Access**: Specialized views and permissions for ADMIN, ACCOUNTANT, and REPORT_VIEWER.
- **Project & Shop Management**: Track expenses and payments across multiple active or closed construction projects and vendor shops.
- **Strict Audit Trail**: Immutable field-level change tracking for all ledger modifications.
- **Local Database**: Zero-configuration SQLite database with WAL mode for concurrent multi-user reading.

## Tech Stack
- **Framework**: Electron (Node.js + Chromium)
- **Database**: SQLite 3 (WAL mode enabled)
- **Frontend**: HTML5, Vanilla JavaScript, local Bootstrap 5.3
- **Security**: bcrypt for password hashing, strict IPC context isolation.
- **Packaging**: electron-builder (NSIS Windows installer)

## Project Structure & Prompt Files
This repository is carefully organized to separate architecture, UI mockups, AI rules, and code. Here is the complete breakdown of the project structure and its key files:

- **`.gitignore`**: Ensures that temporary files, SQLite database files (`*.db`, `*.db-wal`), logs, local environment variables, and compiled Electron output (`/dist`, `/out`) are securely ignored and never committed to version control.
- **`.github/`**: Houses GitHub configuration. Notably, it contains **`copilot-instructions.md`**, the **AI Coding Rulebook**. This file enforces strict, low-level technical guardrails (like "never write SQL in services" and "enforce WAL mode") that GitHub Copilot automatically reads to prevent bad code generation while developing.
- **`docs/`**: The true source of truth for the project. Contains the final architectural blueprints and engineering specifications (`01` through `07`).
  - **`docs/00-FINAL-ANTIGRAVITY-PROMPT.md`**: The **Master Architectural Prompt**. This single file dictates the entire business logic, constraints, and architecture of the application.
- **`mockups/`**: Contains the static HTML UI mockups for stakeholder review, completely separate from the actual application code. 
  - **`mockups/docs/FINAL-ANTIGRAVITY-UI-MOCKUP-PROMPT.md`**: The **UI Mockup Prompt**. This file dictates how the mockups should be built based on the database and architecture docs, ensuring the UI screens match the database columns exactly.
- **`src/`**: (To be generated) Will contain the application source code following the strict layered architecture defined in the `docs/`.

## Documentation Generation Workflow

This project uses a precise, AI-driven process for generating documentation and UI mockups. If you ever need to regenerate the project's documentation from scratch, follow this exact 3-step sequence:

### Step 1: Generate Architecture Documents
**Input File:** `docs/00-FINAL-ANTIGRAVITY-PROMPT.md`

Start by feeding the master prompt to an AI agent.
* **Prompt:** *"Read this prompt and generate the required production-ready documents exactly as specified."*
* **Output:** This generates files `01` through `07` in the `docs/` folder (Implementation Plan, HLD, LLD, Database Design, etc.).
* **Why:** This locks down your database schema, roles, and business rules first.

### Step 2: Generate UI Mockup Prompt
**Input Files:** Your newly generated Architecture Docs (specifically `02-high-level-design.md` and `04-database-design.md`).

Now that the backend is designed, tell the AI to create a prompt for the frontend.
* **Prompt:** *"Based on the database schema and architecture we just designed, write a Prompt File that I can give to a UI Designer to build static HTML fake screens. The screens must exactly match the roles and database fields you just invented."*
* **Output:** This generates `mockups/docs/FINAL-ANTIGRAVITY-UI-MOCKUP-PROMPT.md`.
* **Why:** This ensures the UI screens only contain fields that actually exist in your database.

### Step 3: Generate the UI Mockups
**Input File:** `mockups/docs/FINAL-ANTIGRAVITY-UI-MOCKUP-PROMPT.md`

Give the UI Mockup Prompt to an AI agent (or a human designer).
* **Prompt:** *"Follow this prompt strictly to build my static HTML mockup screens."*
* **Output:** This generates all the raw HTML files (`login.html`, `admin-dashboard.html`, etc.) in the `mockups/` folder.
* **Why:** This gives stakeholders a visual demo of the app that perfectly aligns with the backend engineering specs.

## Development & Setup
*(Source code implementation pending Phase 1 execution)*

```bash
# Install dependencies
npm install

# Run in development mode
npm run start

# Build production Windows installer
npm run build
```
