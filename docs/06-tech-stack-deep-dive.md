# Builder Ledger - Tech Stack Deep Dive

## Document Information
- **Version**: 1.0
- **Last Updated**: 2026-03-14
- **Status**: Production-Ready
- **Purpose**: Complete technical overview and deep dive of the technology stack chosen for Builder Ledger

---

## 1. Technology Stack Overview

### 1.1 Stack Summary

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Runtime** | Electron | 28.x | Desktop app shell — wraps HTML/JS into a Windows `.exe` |
| **Backend Language** | Node.js | 18.x / 20.x LTS | Server-side logic running inside Electron's main process |
| **Database** | SQLite | 3.x | Embedded, single-file database — zero configuration |
| **UI Framework** | Bootstrap | 5.3 (local) | Pre-built responsive components (tables, forms, modals) |
| **Frontend Language** | Vanilla JavaScript | ES2020+ | Simple client-side logic for forms and API calls |
| **Password Security** | bcrypt | 5.x | Irreversible password hashing |
| **Logging** | Winston | 3.x | Daily rotating log files |
| **Packaging** | electron-builder | 24.x | Creates Windows NSIS installer (`.exe`) |

### 1.2 Architecture Layers

```
User clicks a button
    ↓
HTML/Bootstrap UI       → What the user sees (forms, tables, buttons)
    ↓
Client-side JavaScript  → Form validation, sends request via IPC
    ↓
Preload Script          → Secure bridge (only approved functions pass through)
    ↓
IPC Controller          → Routes the request to the correct service
    ↓
Service Layer           → Business rules + authorization checks (NO SQL)
    ↓
Repository Layer        → SQL queries — the ONLY place where SQL exists
    ↓
DB Adapter              → Manages SQLite connection, transactions
    ↓
SQLite Database         → The single .db file storing all data
```

Each layer only talks to the one directly below it. This makes the code organized, maintainable, and swappable.

---

## 2. Electron — The Application Shell

### 2.1 What It Is

Electron is a framework that lets you build desktop applications using web technologies (HTML, CSS, JavaScript). It bundles a Chromium browser + Node.js runtime into a single application.

### 2.2 Why It Was Chosen

- Builder Ledger needs to run as a **Windows desktop application** (not in a browser)
- Gives access to the **file system** (for attachments, backups, logs) — something a normal website can't do
- Widely proven — VS Code, WhatsApp Desktop, Slack are all built with Electron
- Uses web technologies the team already knows (HTML, CSS, JS)

### 2.3 How It Works

```
┌─────────────────────────────────────────┐
│         Electron Application            │
│                                         │
│  ┌───────────────┐  ┌────────────────┐  │
│  │ Main Process  │  │ Renderer       │  │
│  │ (Node.js)     │  │ (Browser/UI)   │  │
│  │               │  │                │  │
│  │ • DB access   │  │ • HTML pages   │  │
│  │ • File system │◄─┤ • Bootstrap UI │  │
│  │ • Business    │  │ • Forms        │  │
│  │   logic       │  │ • Tables       │  │
│  └───────────────┘  └────────────────┘  │
└─────────────────────────────────────────┘
```

- **Main Process** = the backend (handles database, files, security)
- **Renderer Process** = the frontend (what the user sees — HTML pages)
- They communicate via **IPC** (see Section 4)

### 2.4 Security Configuration

| Setting | Value | Purpose |
|---------|-------|---------|
| `contextIsolation` | `true` | Renderer cannot access Node.js APIs directly |
| `nodeIntegration` | `false` | No `require()` in HTML pages |
| Preload script | Required | Only approved functions exposed to UI |

---

## 3. SQLite — The Database

### 3.1 What It Is

SQLite is a lightweight, serverless database engine. The entire database is stored as a **single file** on disk — no database server to install, configure, or maintain.

### 3.2 Why It Was Chosen

- **100% offline** — no database server installation needed (unlike MySQL/PostgreSQL)
- **Zero configuration** — just a file: `builder-ledger.db`
- Perfect for a desktop app where data lives on the local machine
- Handles up to ~10 concurrent users with **WAL mode** (see Section 5)
- Extremely reliable — used in Firefox, Android, iOS, and countless apps

### 3.3 Database File Location

```
C:\ProgramData\BuilderLedger\
├── data\
│   └── builder-ledger.db          ← The entire database (single file)
├── backups\
│   ├── builder-ledger_2026-01-15.db
│   └── ...
├── logs\
│   └── app_2026-03-14.log
└── attachments\
    └── {year}\{month}\{entry_id}\
```

### 3.4 Key Database Settings

```sql
PRAGMA journal_mode = WAL;      -- Enable concurrent read/write (see Section 5)
PRAGMA foreign_keys = ON;       -- Enforce referential integrity
```

### 3.5 Future-Proofing

The code uses the **Repository Pattern** (see Section 6). All SQL queries live in 6 repository files only. If you ever want to switch from SQLite to PostgreSQL, you only change these 6 files — the rest of the application stays untouched.

---

## 4. IPC (Inter-Process Communication) — Deep Dive

### 4.1 The Problem

Electron runs your app in **two separate processes** that cannot directly talk to each other:

| Process | What It Does | Has Access To |
|---------|-------------|---------------|
| **Main Process** (Node.js) | Database, files, business logic | File system, SQLite, bcrypt — everything |
| **Renderer Process** (Browser) | Shows HTML pages, buttons, forms | Only the screen — **NO database, NO file system** |

This separation exists for **security**. If the renderer could directly access the file system or database, a malicious script injected into your HTML could steal or delete all your data.

**The problem**: User clicks "Save Entry" on the screen (renderer), but the database lives in the main process. How do they communicate?

**Answer**: **IPC** — a secure messaging system between the two processes.

### 4.2 How IPC Works

Think of it like a **bank counter with a glass window**:

```
Customer (Renderer)        Glass Window (Preload)       Bank Staff (Main Process)

"I want to add a           Passes the slip              Validates → saves to DB
 ledger entry"             through the slot              → returns confirmation
 [fills form, clicks       (only approved
  save button]              requests allowed)
```

### 4.3 Builder Ledger Example: Accountant Adds a Ledger Entry

**Step 1 — User clicks "Save" on the form (Renderer Process)**:
```javascript
// In project-view.js (browser side)
async function saveEntry() {
    const entryData = {
        project_id: 3,              // "Villa Construction" project
        category_id: 5,             // "Cement Purchase" category
        shop_id: 2,                 // "Sri Lakshmi Traders" shop
        amount: 45000,
        description: "50 bags cement @ Rs.900",
        action_date: "2026-03-14",
        payment_mode: "CASH"
    };

    // Calls the PRELOAD script — NOT the main process directly
    const result = await window.api.ledger.create(entryData);

    if (result.success) {
        alert("Entry saved!");
    } else {
        alert(result.error);  // e.g., "Shop is CLOSED, cannot add entry"
    }
}
```

**Step 2 — Preload script passes request through secure channel**:
```javascript
// In preload.js (the glass window)
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
    ledger: {
        // ONLY these specific functions are exposed — nothing else
        create: (data) => ipcRenderer.invoke('ledger:create', data),
        update: (id, data) => ipcRenderer.invoke('ledger:update', id, data),
        delete: (id) => ipcRenderer.invoke('ledger:delete', id),
        getByProject: (projectId) => ipcRenderer.invoke('ledger:get-by-project', projectId),
    }
});
// The renderer CANNOT access: fs, sqlite3, require(), process, or anything else
```

**Step 3 — Main process receives and handles request**:
```javascript
// In ledger-controller.js (main process)
ipcMain.handle('ledger:create', async (event, data) => {
    try {
        // 1. Validate session (is user logged in?)
        // 2. Call service layer (business rules)
        const entry = await ledgerService.createEntry(data, userId, role);
        return { success: true, data: entry };
    } catch (error) {
        return { success: false, error: error.message };
    }
});
```

### 4.4 Why Not Just Access the Database Directly?

Without IPC + Context Isolation:
```javascript
// ❌ DANGEROUS — if renderer had Node.js access
const fs = require('fs');
fs.unlinkSync('C:\\ProgramData\\BuilderLedger\\data\\builder-ledger.db');
// Deletes entire database!
```

With IPC + Context Isolation:
```javascript
// ✅ SAFE — renderer can only call approved functions
await window.api.ledger.create(data);  // Only this works
// window.require → undefined
// window.fs → undefined
```

### 4.5 Complete IPC Channel Map

| Channel | Direction | Purpose |
|---------|-----------|---------|
| `auth:login` | Renderer → Main | User login |
| `auth:logout` | Renderer → Main | User logout |
| `users:get-all` | Renderer → Main | List all users |
| `users:create` | Renderer → Main | Create new user |
| `projects:get-all` | Renderer → Main | List projects |
| `projects:create` | Renderer → Main | Create project |
| `projects:open` / `projects:close` | Renderer → Main | Change project lifecycle |
| `shops:get-all` | Renderer → Main | List shops |
| `shops:create` | Renderer → Main | Create shop |
| `categories:get-all` | Renderer → Main | List categories |
| `ledger:create` | Renderer → Main | Add ledger entry |
| `ledger:update` | Renderer → Main | Edit ledger entry |
| `ledger:delete` | Renderer → Main | Soft-delete entry |
| `ledger:get-by-project` | Renderer → Main | Fetch project ledger |
| `ledger:get-balance` | Renderer → Main | Calculate balance |
| `ledger:get-shop-payables` | Renderer → Main | Calculate shop outstanding |
| `audit:get-by-entry` | Renderer → Main | View change history |
| `backup:trigger` | Renderer → Main | Trigger on-demand backup |

---

## 5. WAL (Write-Ahead Logging) — Deep Dive

### 5.1 The Problem

Builder Ledger is used by **multiple Windows users on the same computer**:

- **Admin** (builder owner) is viewing the audit trail
- **Accountant** is entering expenses for a cement purchase
- **Report Viewer** (partner) is checking project balance

All three access the **same SQLite database file** at the same time.

**Without WAL mode**: SQLite locks the **entire file** when anyone writes. While the Accountant saves an entry, the Admin's screen would **freeze or show an error** — even though the Admin is only *reading* data.

### 5.2 How WAL Solves This

**Normal SQLite (without WAL)**:
```
Accountant writes entry → ENTIRE DATABASE LOCKED
Admin tries to read audit trail → ❌ "Database is locked" error
Report Viewer tries to view balance → ❌ "Database is locked" error
```

**SQLite with WAL mode**:
```
Accountant writes entry → Write goes to a separate WAL file
Admin reads audit trail → ✅ Reads from main DB (not blocked!)
Report Viewer reads balance → ✅ Reads from main DB (not blocked!)

After write completes → WAL file merges back into main DB (checkpoint)
```

### 5.3 Internal Architecture

```
Without WAL:
┌──────────────────────┐
│  builder-ledger.db   │ ← Both reads AND writes go here
│                      │ ← Only ONE operation at a time
└──────────────────────┘

With WAL:
┌──────────────────────┐    ┌──────────────────────────┐
│  builder-ledger.db   │    │  builder-ledger.db-wal   │
│  (main database)     │    │  (write-ahead log)       │
│                      │    │                          │
│  Readers read from   │    │  Writers write here      │
│  here (unblocked)    │    │  first (temporary)       │
└──────────────────────┘    └────────────┬─────────────┘
                                         │ merges back periodically
                                         ▼
                            ┌──────────────────────────┐
                            │  builder-ledger.db       │
                            │  (updated)               │
                            └──────────────────────────┘
```

### 5.4 Real Use Case: Month-End Simultaneous Access

| Time | Admin (User 1) | Accountant (User 2) | Report Viewer (User 3) |
|------|----------------|---------------------|------------------------|
| 10:00 AM | Opens Audit Trail | Opens Project View | Opens Dashboard |
| 10:01 AM | **Reads** audit records ✅ | **Writes** cement expense ₹45,000 ✅ | **Reads** project balance ✅ |
| 10:02 AM | **Reads** more records ✅ | **Writes** labor payment ₹12,000 ✅ | **Reads** shop payables ✅ |
| 10:03 AM | Closes shop (**Write**) | Waits briefly (Admin's write goes first) | **Reads** dashboard ✅ |

**Key rule**: Multiple reads happen simultaneously. Writes are queued one-by-one, but they **never block readers**.

### 5.5 How It's Enabled

```javascript
// In db-adapter.js — runs once at app startup
db.run("PRAGMA journal_mode = WAL");   // One line — enables concurrent access
db.run("PRAGMA foreign_keys = ON");    // Enforce foreign key constraints
```

### 5.6 Limitations

- Recommended for up to **~10 concurrent users** (sufficient for Builder Ledger)
- Write operations are **serialized** (one at a time) — but each write is fast (~200ms)
- WAL file must be on the **same disk** as the main database

---

## 6. Repository Pattern — Deep Dive

### 6.1 The Problem

Your app talks to the database constantly. If you write SQL queries everywhere, you end up with:

```javascript
// ❌ BAD: SQL scattered in the service layer
async function createEntry(data) {
    // Business logic mixed with SQL — messy!
    const project = await db.get(
        "SELECT * FROM projects WHERE id = ? AND is_deleted = 0",
        [data.project_id]
    );
    if (project.status !== 'ACTIVE') throw new Error("Project is closed");

    await db.run(
        "INSERT INTO ledger_entries (project_id, amount, ...) VALUES (?, ?, ...)",
        [...]
    );
}
```

**Problems**:
1. Same SQL gets copy-pasted in 10 places
2. Changing a column name means fixing every query everywhere
3. Switching from SQLite to PostgreSQL means rewriting **everything**
4. Can't test business logic without a real database

### 6.2 The Solution: Separate SQL from Business Logic

**Rule**: All SQL lives in **repository files only**. Services never see any SQL.

```
┌────────────────────────────────────────────────────────┐
│ Service Layer    (Business Logic — NO SQL here)        │
│                                                        │
│  "Is the project active? Is the user authorized?       │
│   Calculate the balance. Log the audit trail."         │
│                                                        │
│  Calls repository methods like:                        │
│    projectRepo.findById(3)                             │
│    ledgerRepo.insert(entry)                            │
│    auditRepo.insert(auditRecord)                       │
└───────────────────────┬────────────────────────────────┘
                        │ calls
┌───────────────────────▼────────────────────────────────┐
│ Repository Layer  (SQL Lives HERE — and ONLY here)     │
│                                                        │
│  projectRepo.findById(3)                               │
│    → SELECT * FROM projects WHERE id = 3               │
│                                                        │
│  ledgerRepo.insert(entry)                              │
│    → INSERT INTO ledger_entries (...)                   │
│                                                        │
│  auditRepo.insert(record)                              │
│    → INSERT INTO ledger_audit_trail (...)               │
└────────────────────────────────────────────────────────┘
```

### 6.3 Builder Ledger Repositories

| Repository | Table | Key Methods |
|------------|-------|-------------|
| **User Repository** | `users` | `findByUsername()`, `findByRole()`, `activate()`, `softDelete()` |
| **Project Repository** | `projects` | `findById()`, `findByStatus()`, `updateStatus()`, `softDelete()` |
| **Shop Repository** | `shops` | `findById()`, `findByStatus()`, `updateStatus()`, `softDelete()` |
| **Category Repository** | `categories` | `findByType()`, `findAllActive()`, `softDelete()` |
| **Ledger Repository** | `ledger_entries` | `insert()`, `findByProject()`, `getProjectBalance()`, `getShopPayables()` |
| **Audit Repository** | `ledger_audit_trail` | `insert()`, `findByEntry()`, `findByDateRange()` — **no update/delete (immutable)** |

### 6.4 Real Use Case: Accountant Creates a Cement Purchase

**Service layer** (business rules only — zero SQL):
```javascript
// In ledger-service.js
async createEntry(data, userId, role) {
    // 1. Authorization
    if (role !== 'ACCOUNTANT') throw new Error('Only ACCOUNTANT can create entries');

    // 2. Validate project is ACTIVE
    const project = await this.projectRepo.findById(data.project_id);
    if (project.status !== 'ACTIVE') throw new Error('Cannot add to CLOSED project');

    // 3. If shop is specified, validate shop is ACTIVE
    if (data.shop_id) {
        const shop = await this.shopRepo.findById(data.shop_id);
        if (shop.status !== 'ACTIVE') throw new Error('Shop is CLOSED');
    }

    // 4. Save entry (NO SQL here!)
    const entry = await this.ledgerRepo.insert({
        ...data,
        created_by: userId,
        created_at: TimestampUtil.nowIST()
    });

    // 5. Log audit trail (NO SQL here!)
    await this.auditRepo.insert({
        ledger_entry_id: entry.id,
        action_type: 'CREATE',
        changed_by: userId,
        changed_at: TimestampUtil.nowIST()
    });

    return entry;
}
```

**Repository layer** (SQL only — zero business logic):
```javascript
// In ledger-repository.js
async insert(entry) {
    const sql = `INSERT INTO ledger_entries
        (project_id, category_id, shop_id, amount, description,
         payment_mode, action_date, created_by, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`;

    const result = await this.db.run(sql, [
        entry.project_id, entry.category_id, entry.shop_id,
        entry.amount, entry.description, entry.payment_mode,
        entry.action_date, entry.created_by, entry.created_at
    ]);

    return { id: result.lastID, ...entry };
}

async getProjectBalance(projectId) {
    const sql = `SELECT
        COALESCE(SUM(CASE WHEN c.type = 'PAYMENT' THEN le.amount ELSE 0 END), 0) -
        COALESCE(SUM(CASE WHEN c.type = 'EXPENSE' THEN le.amount ELSE 0 END), 0)
            AS balance
        FROM ledger_entries le
        JOIN categories c ON le.category_id = c.id
        WHERE le.project_id = ? AND le.is_deleted = 0`;

    const result = await this.db.get(sql, [projectId]);
    return result.balance;
}
```

### 6.5 Future Database Migration Benefit

```
Without Repository Pattern:
  → Rewrite 50+ files with SQL scattered everywhere 😱

With Repository Pattern:
  → Rewrite only 6 repository files
  → Service layer, controllers, UI — ZERO changes ✅
```

---

## 7. bcrypt — Password Security Deep Dive

### 7.1 The Problem

Builder Ledger stores user credentials in SQLite. If someone copies the database file from `C:\ProgramData\BuilderLedger\`, they could see all passwords if stored as plain text:

```
❌ WITHOUT hashing:
| username | password    | role          |
|----------|-------------|---------------|
| admin    | admin123    | ADMIN         |  ← Anyone who copies the DB
| ramesh   | ramesh@456  | ACCOUNTANT    |    sees all passwords!
| suresh   | suresh789   | REPORT_VIEWER |
```

### 7.2 How bcrypt Solves This

bcrypt converts passwords into an **irreversible hash** — you cannot reverse-engineer the original password:

```
✅ WITH bcrypt:
| username | password_hash                                 | role          |
|----------|-----------------------------------------------|---------------|
| admin    | $2b$10$N9qo8uLOickgx2ZMRZoMyeYkMq2.6Wl4V/... | ADMIN         |
| ramesh   | $2b$10$3euPcmQFCib.m7TKhGH9pe8VZyFcNsmAy5... | ACCOUNTANT    |
| suresh   | $2b$10$YWVlZDExMjNhYmNkZWYxMj.kL9xjH5yGf3... | REPORT_VIEWER |
```

Even if someone steals the database file, they **cannot** figure out the original password from the hash.

### 7.3 How Login Works with bcrypt

```
Step 1: User types "admin123" on login screen

Step 2: bcrypt hashes "admin123" and COMPARES with stored hash
        bcrypt.compare("admin123", "$2b$10$N9qo8uLOickgx2ZMRZoMy...")
        → Result: true (match!) → Login success ✅

Step 3: If user types wrong password "admin456"
        bcrypt.compare("admin456", "$2b$10$N9qo8uLOickgx2ZMRZoMy...")
        → Result: false → Login failed ❌
```

### 7.4 Builder Ledger Example: Admin Creates a New User

```javascript
// What happens when Admin creates user "ramesh" with password "ramesh@456":

// 1. bcrypt hashes the password (cost factor 10 = ~100ms)
const passwordHash = await bcrypt.hash("ramesh@456", 10);
// passwordHash = "$2b$10$3euPcmQFCib..."

// 2. ONLY the hash is stored — original password is never saved
await userRepo.insert({
    username: "ramesh",
    password_hash: passwordHash,   // ← Only this is stored
    role: "ACCOUNTANT"
});
// The original password "ramesh@456" is thrown away
```

```javascript
// Next day — Ramesh logs in:

// 1. Fetch user record
const user = await userRepo.findByUsername("ramesh");

// 2. Compare entered password with stored hash
const isValid = await bcrypt.compare("ramesh@456", user.password_hash);
// bcrypt internally re-hashes and checks → isValid = true

// 3. Create session
if (isValid) {
    sessionManager.createSession(user.id, user.role);
}
```

### 7.5 Why Cost Factor 10?

The `10` in `bcrypt.hash(password, 10)` means bcrypt performs **2¹⁰ = 1,024 rounds** of hashing:

| Scenario | Time | Impact |
|----------|------|--------|
| Normal login | ~100ms | Invisible to user |
| Attacker tries 10,000 passwords | 10,000 × 100ms = **~16 minutes** | Slow and impractical |
| Dictionary attack (1M passwords) | 1,000,000 × 100ms = **~27 hours** | Effectively useless |

This **deliberate slowness** makes brute-force attacks impractical while being invisible to legitimate users.

---

## 8. Vanilla JavaScript — Why Not React/Angular/Vue?

### 8.1 SPA vs. Multi-Page App

| Feature | SPA (React/Vue/Angular) | Multi-Page (Vanilla JS) |
|---------|------------------------|------------------------|
| **How it works** | Loads ONE HTML page, JS rebuilds the screen dynamically | Each screen is a separate HTML file |
| **Navigation** | URL changes but page never reloads | User clicks link → new page loads |
| **Complexity** | High — state management, component lifecycle, build tools | Low — standard HTML + JS |
| **Best for** | Social media feeds, real-time chat, complex dashboards | Data entry apps, admin panels, ledger tools |

### 8.2 Why Builder Ledger is a CRUD App

Every operation in Builder Ledger is one of four things:

| Operation | What the User Does | Example |
|-----------|-------------------|---------|
| **C**reate | Fill a form → click save | Add project, add user, add ledger entry |
| **R**ead | Open a page → see a table/list | View ledger, view audit trail, view balance |
| **U**pdate | Click edit → modify form → save | Edit project name, edit ledger entry amount |
| **D**elete | Click delete → confirm | Soft-delete a shop, soft-delete a user |

There are no real-time updates, no drag-and-drop, no live-streaming data, no complex interactive visualizations. Each screen is **independent** — load a page, see data, fill a form, save, done.

### 8.3 Comparison: React vs. Vanilla JS for Project Management

**With React (SPA approach)**:
```
project-management/
├── components/
│   ├── ProjectList.jsx           ← Table component
│   ├── ProjectForm.jsx           ← Add/edit form component
│   ├── ProjectRow.jsx            ← Row component
│   ├── ProjectFilter.jsx         ← Filter component
│   ├── ProjectModal.jsx          ← Modal component
│   └── ProjectStatusBadge.jsx    ← Badge component
├── hooks/
│   ├── useProjects.js            ← Data fetching hook
│   └── useProjectForm.js         ← Form state hook
├── context/
│   └── ProjectContext.js         ← State management
└── store/
    └── projectSlice.js           ← Redux/Zustand state

→ 10+ files, requires React, JSX, Webpack/Vite, state management knowledge
```

**With Vanilla JS (Builder Ledger approach)**:
```
admin/
├── project-management.html       ← Complete page with table + form
└── project-management.js         ← Button clicks + API calls

→ 2 files, requires basic HTML + JS knowledge only
```

### 8.4 What the Code Actually Looks Like

```html
<!-- project-management.html -->
<table class="table table-striped">
  <thead>
    <tr>
      <th>Project Name</th>
      <th>Status</th>
      <th>Created Date</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody id="projectTableBody">
    <!-- JavaScript fills this -->
  </tbody>
</table>

<!-- Bootstrap Modal for Add/Edit -->
<div class="modal" id="projectModal">
  <input type="text" id="projectName" placeholder="Project Name">
  <button onclick="saveProject()">Save</button>
</div>
```

```javascript
// project-management.js — entire file is ~50 lines
async function loadProjects() {
    const result = await window.api.projects.getAll();
    const tbody = document.getElementById('projectTableBody');
    tbody.innerHTML = '';

    result.data.forEach(project => {
        tbody.innerHTML += `
            <tr>
                <td>${project.name}</td>
                <td><span class="badge bg-${project.status === 'ACTIVE' ? 'success' : 'secondary'}">
                    ${project.status}</span></td>
                <td>${project.created_at}</td>
                <td>
                    <button onclick="editProject(${project.id})">Edit</button>
                    <button onclick="deleteProject(${project.id})">Delete</button>
                </td>
            </tr>`;
    });
}

async function saveProject() {
    const name = document.getElementById('projectName').value;
    await window.api.projects.create({ name });
    loadProjects();  // Refresh the table
}
```

### 8.5 When Would You Need React/SPA?

You would need it if your app had:
- Real-time updates (like chat messages appearing live)
- Complex interactive dashboards with drag-and-drop
- Single-page navigation with animated transitions
- Hundreds of interactive components on one screen

Builder Ledger has **none of these**. Each screen is independent — simple forms + tables.

---

## 9. Bootstrap 5.3 — UI Framework

### 9.1 What It Is

A CSS/JS library providing pre-built UI components: buttons, forms, tables, modals, navigation bars, and responsive grid layouts.

### 9.2 Why It Was Chosen

- Professional-looking UI without writing CSS from scratch
- Pre-built components match the app's needs (data tables, form inputs, modals)
- Responsive — works at different screen sizes
- **Downloaded locally** — no CDN dependency since the app runs 100% offline

### 9.3 Local Asset Storage

```
src/renderer/assets/
├── css/
│   ├── bootstrap.min.css         ← Downloaded, not from CDN
│   └── app.css                   ← Custom styles
└── js/
    ├── bootstrap.bundle.min.js   ← Downloaded, not from CDN
    └── common.js                 ← Shared JS utilities
```

---

## 10. Winston — Logging Library

### 10.1 What It Is

A production logging library for Node.js that writes structured log messages to files.

### 10.2 Configuration in Builder Ledger

| Setting | Value | Purpose |
|---------|-------|---------|
| Log location | `C:\ProgramData\BuilderLedger\logs\` | Centralized log storage |
| Rotation | Daily | New file each day (`app_2026-03-14.log`) |
| Retention | 30 days | Auto-delete old logs |
| Levels | INFO, WARN, ERROR | Different severity levels |
| Sensitive data | **Never logged** | No passwords, hashes, or financial amounts |

---

## 11. electron-builder — Packaging & Installer

### 11.1 What It Is

A tool that packages the Electron app into a distributable Windows installer (`.exe`).

### 11.2 Builder Ledger Installer Configuration

| Setting | Value |
|---------|-------|
| App ID | `com.builderledger.app` |
| Product Name | `Builder Ledger` |
| Target | Windows x64 NSIS |
| Install Path | `C:\Program Files\Builder Ledger\` |
| Data Path | `C:\ProgramData\BuilderLedger\` |
| Shortcuts | Desktop + Start Menu |
| Default credentials | `admin` / `admin123` |

---

## 12. Security Stack Summary

| Layer | Technology | How It Protects |
|-------|-----------|-----------------|
| **Passwords** | bcrypt (cost 10) | Hashed irreversibly — safe even if DB is stolen |
| **Sessions** | In-memory Map | Lost on restart, no sessionStorage/localStorage/cookies |
| **Process Isolation** | Electron context isolation | UI cannot access Node.js, file system, or database directly |
| **SQL Protection** | Parameterized queries | Prevents SQL injection attacks |
| **Authorization** | Service-layer checks | Enforced in code, not just in UI (UI is defensive only) |
| **Change Tracking** | Immutable audit trail | Every ledger change recorded with old/new values |

---

## 13. Quick Reference Summary

| Concept | One-Line Summary | Builder Ledger Use Case |
|---------|------------------|------------------------|
| **Electron** | Web tech → desktop app | Wraps HTML/JS into a Windows `.exe` with file system access |
| **SQLite** | Database in a single file | No server needed, works 100% offline |
| **IPC** | Secure messaging between UI and backend | "Save Entry" button → secure channel → database |
| **WAL** | Multiple users read/write simultaneously | Admin reads while Accountant writes — no blocking |
| **Repository Pattern** | All SQL in one place | Switch from SQLite to PostgreSQL by changing only 6 files |
| **bcrypt** | Irreversible password hashing | "ramesh@456" → `$2b$10$3eu...` — impossible to reverse |
| **Vanilla JS** | Simple JS for form-based apps | 2 files per screen instead of 10+ React components |
| **Bootstrap** | Pre-built UI components (offline) | Tables, forms, modals — no CDN needed |
| **Winston** | Daily rotating log files | 30-day retention, no sensitive data logged |
| **electron-builder** | Creates Windows installer | NSIS `.exe` with shortcuts and proper file paths |

---

**Document Status**: ✅ Production-Ready
**Created**: 2026-03-14
