# Builder Ledger - Low-Level Design (LLD)

## Document Information
- **Version**: 1.1
- **Last Updated**: 2026-01-15
- **Status**: Production-Ready
- **Purpose**: Component-level design specifications (design-only, no code)

---

## 1. Project Structure

### 1.1 Folder Organization

```
builder-ledger/
├── src/
│   ├── main/                      # Main process (Node.js)
│   │   ├── index.js               # Entry point
│   │   ├── database/              # Database layer
│   │   │   ├── db-adapter.js      # SQLite abstraction
│   │   │   └── schema.sql         # Database schema
│   │   ├── repositories/          # Data access layer
│   │   │   ├── base-repository.js
│   │   │   ├── user-repository.js
│   │   │   ├── project-repository.js
│   │   │   ├── shop-repository.js
│   │   │   ├── category-repository.js
│   │   │   ├── ledger-repository.js
│   │   │   └── audit-repository.js
│   │   ├── services/              # Business logic layer
│   │   │   ├── auth-service.js
│   │   │   ├── user-service.js
│   │   │   ├── project-service.js
│   │   │   ├── shop-service.js
│   │   │   ├── category-service.js
│   │   │   ├── ledger-service.js
│   │   │   ├── audit-service.js
│   │   │   ├── attachment-service.js
│   │   │   └── backup-service.js
│   │   ├── controllers/           # IPC handlers
│   │   │   ├── auth-controller.js
│   │   │   ├── user-controller.js
│   │   │   ├── project-controller.js
│   │   │   ├── shop-controller.js
│   │   │   ├── category-controller.js
│   │   │   ├── ledger-controller.js
│   │   │   ├── audit-controller.js
│   │   │   └── backup-controller.js
│   │   ├── utils/                 # Utilities
│   │   │   ├── session-manager.js
│   │   │   ├── logger.js
│   │   │   ├── validator.js
│   │   │   └── timestamp-util.js
│   │   └── preload.js             # Secure IPC bridge
│   └── renderer/                  # Renderer process (Browser)
│       ├── login.html
│       ├── login.js
│       ├── admin/                 # ADMIN screens
│       │   ├── user-management.html
│       │   ├── project-management.html
│       │   ├── shop-management.html
│       │   ├── category-management.html
│       │   ├── project-ledger-view.html
│       │   ├── shop-ledger-view.html
│       │   ├── audit-trail.html
│       │   └── backup-history.html
│       ├── accountant/            # ACCOUNTANT screens
│       │   ├── dashboard.html
│       │   ├── project-view.html
│       │   ├── shop-view.html
│       │   ├── audit-trail.html
│       │   └── backup-history.html
│       ├── report-viewer/         # REPORT_VIEWER screens
│       │   └── (same as accountant, read-only)
│       └── assets/
│           ├── css/
│           │   ├── bootstrap.min.css
│           │   └── app.css
│           └── js/
│               ├── bootstrap.bundle.min.js
│               └── common.js
├── package.json
├── electron-builder.json
└── README.md
```

---

## 2. Database Layer

### 2.1 DB Adapter Design

**Purpose**: Abstract SQLite operations, manage connections, provide transaction support

**Responsibilities**:
- Initialize database connection with WAL mode
- Enable foreign key enforcement
- Provide parameterized query methods (run, get, all)
- Transaction management (begin, commit, rollback)
- Connection lifecycle (open, close)

**Key Methods**:
- `initialize()`: Set up database, enable WAL, foreign keys
- `run(sql, params)`: Execute INSERT/UPDATE/DELETE
- `get(sql, params)`: Fetch single row
- `all(sql, params)`: Fetch multiple rows
- `executeInTransaction(callback)`: Run operations in transaction
- `close()`: Close database connection

---

### 2.2 Repository Pattern Design

**Base Repository**:
- Generic CRUD operations
- Soft delete implementation
- Common query patterns

**Concrete Repositories**:

**User Repository**:
- Find by username (for authentication)
- Find by role
- Activate/deactivate user
- Soft delete user

**Project Repository**:
- Find by status (ACTIVE/CLOSED)
- Update status (open/close)
- Find active projects
- Soft delete project

**Shop Repository**:
- Find by status (ACTIVE/CLOSED)
- Update status (open/close)
- Find active shops
- Soft delete shop

**Category Repository**:
- Find by type (PAYMENT/EXPENSE)
- Find all active categories
- Soft delete category

**Ledger Repository**:
- Find by project with filters (date range, category)
- Find by shop with filters
- Calculate project balance (derived)
- Calculate shop payables (derived)
- Complex queries with JOINs
- Soft delete entry

**Audit Repository**:
- Insert audit record (CREATE/UPDATE/DELETE)
- Find by ledger entry
- Find by date range
- Find by user
- **No update or delete** (immutable)

---

## 3. Service Layer

### 3.1 Service Design Principles

**All services must**:
- Enforce authorization (check role)
- Validate business rules
- Validate inputs
- Handle errors gracefully
- Delegate SQL to repositories
- Generate IST timestamps

### 3.2 Service Components

**Auth Service**:
- Login (validate credentials, create session)
- Logout (destroy session)
- Password hashing with bcrypt

**User Service**:
- Create user (ADMIN only, hash password)
- Update user (ADMIN only)
- Activate/deactivate (ADMIN only)
- Soft delete (ADMIN only)
- Get all users (ADMIN only)

**Project Service**:
- Create project (ADMIN only, status=ACTIVE)
- Update project name (ADMIN only)
- Open/close project (ADMIN only)
- Soft delete (ADMIN only)
- Get projects with status filter

**Shop Service**:
- Create shop (ADMIN only, status=ACTIVE)
- Update shop name (ADMIN only)
- Open/close shop (ADMIN only)
- Soft delete (ADMIN only)
- Get shops with status filter

**Category Service**:
- Create category (ADMIN only)
- Update category (ADMIN only)
- Soft delete (ADMIN only)
- Get categories by type

**Ledger Service**:
- Create entry (ACCOUNTANT only, validate payment rules)
  - Payment Received: shop=NULL
  - Shop Payment: shop required, shop ACTIVE
  - Refund: shop=NULL, balance > 0
  - Expense: shop optional
- Update entry (ACCOUNTANT only, project/shop ACTIVE)
- Soft delete entry (ACCOUNTANT only, project/shop ACTIVE)
- Get entries by project/shop
- Calculate balances (derived)
- Calculate shop payables (derived)
- Log audit trail on CREATE/UPDATE/DELETE

**Audit Service**:
- Log CREATE action
- Log UPDATE action (one record per field)
- Log DELETE action
- Query audit trail

**Attachment Service**:
- Upload files (validate format, size, count)
- Store in file system
- Return relative paths
- Retrieve attachments

**Backup Service**:
- Auto weekly backup (on startup if > 7 days)
- On-demand backup (ADMIN only)
- Retain last 8 backups
- Close DB before copy, reopen after

---

## 4. IPC Controller Layer

### 4.1 Controller Design Pattern

**All controllers must**:
- Register IPC handlers in constructor
- Validate session from event
- Call service methods
- Return consistent response format: `{success, data/error}`
- Wrap in try-catch

### 4.2 Controller Components

**Auth Controller**:
- Handle `auth:login`
- Handle `auth:logout`
- Handle `auth:validate-session`

**User Controller**:
- Handle `users:get-all`
- Handle `users:create`
- Handle `users:update`
- Handle `users:activate`
- Handle `users:delete`

**Project Controller**:
- Handle `projects:get-all`
- Handle `projects:create`
- Handle `projects:update`
- Handle `projects:open`
- Handle `projects:close`
- Handle `projects:delete`

**Shop Controller**:
- Handle `shops:get-all`
- Handle `shops:create`
- Handle `shops:update`
- Handle `shops:open`
- Handle `shops:close`
- Handle `shops:delete`

**Category Controller**:
- Handle `categories:get-all`
- Handle `categories:get-by-type`
- Handle `categories:create`
- Handle `categories:update`
- Handle `categories:delete`

**Ledger Controller**:
- Handle `ledger:get-by-project`
- Handle `ledger:get-by-shop`
- Handle `ledger:create`
- Handle `ledger:update`
- Handle `ledger:delete`
- Handle `ledger:get-balance`
- Handle `ledger:get-shop-payables`

**Audit Controller**:
- Handle `audit:get-by-entry`
- Handle `audit:get-by-date-range`
- Handle `audit:get-by-user`

**Backup Controller**:
- Handle `backup:get-history`
- Handle `backup:trigger` (ADMIN only)

---

## 5. Preload Script Design

### 5.1 Secure IPC Bridge

**Purpose**: Expose limited, secure API to renderer process

**Configuration**:
- Use `contextBridge.exposeInMainWorld`
- Namespace: `window.api`
- Use `ipcRenderer.invoke` (not `send`)

**API Structure**:
- `window.api.auth.*`
- `window.api.users.*`
- `window.api.projects.*`
- `window.api.shops.*`
- `window.api.categories.*`
- `window.api.ledger.*`
- `window.api.audit.*`
- `window.api.backup.*`

---

## 6. UI Layer Design

### 6.1 Common UI Patterns

**Navigation Bar**:
- Application title
- User info display (username, role)
- Logout button

**Sidebar Navigation**:
- Role-based menu items
- Active state highlighting
- Links to screens

**Data Tables**:
- Bootstrap table styling
- Sortable columns (client-side)
- Filter controls
- Action buttons (Edit, Delete, etc.)

**Forms**:
- Bootstrap form controls
- Client-side validation
- Error message display
- Submit/Cancel buttons

**Modals**:
- Bootstrap modal component
- Add/Edit forms
- Confirmation dialogs

### 6.2 Screen Designs

**Login Screen**:
- Username input
- Password input
- Login button
- Error message area
- Redirect based on role after login

**ADMIN Screens**:
1. **User Management**: List users, add/edit/activate/deactivate/delete
2. **Project Management**: List projects, add/edit/open/close/delete, status filter
3. **Shop Management**: List shops, add/edit/open/close/delete, status filter
4. **Category Management**: List by type, add/edit/delete
5. **View Project Ledger**: Read-only, project selector, date filter, balance display
6. **View Shop Ledger**: Read-only, shop selector, outstanding payable
7. **Audit Trail**: Date filter, user filter, action filter, field-level changes
8. **Backup History**: List backups, trigger on-demand backup

**ACCOUNTANT Screens**:
1. **Dashboard**: View by Project/Shop toggle, status filter, summary cards
2. **Project View**: Project selector, entry list, add/edit/delete, balance, attachments
3. **Shop View**: Shop selector, project-wise breakdown, outstanding payable, make payment
4. **Audit Trail**: Read-only
5. **Backup History**: Read-only

**REPORT_VIEWER Screens**:
- Same as ACCOUNTANT but all forms/buttons hidden (read-only)

---

## 7. Utility Components

### 7.1 Session Manager

**Purpose**: Manage in-memory user sessions

**Responsibilities**:
- Create session (store userId, role, sessionId)
- Validate session
- Destroy session
- Get session from IPC event
- **NO persistence** (sessions cleared on app restart)
- **NO sessionStorage usage**

**Data Structure**:
- In-memory Map: `sessionId → {userId, role, createdAt}`

### 7.2 Logger

**Purpose**: File-based application logging

**Responsibilities**:
- Log to daily file
- Rotate logs daily
- Retain last 30 days
- Log levels: INFO, WARN, ERROR
- **NO sensitive data** (passwords, hashes)

**Implementation**: Winston library

### 7.3 Validator

**Purpose**: Input validation utilities

**Responsibilities**:
- Validate username (alphanumeric, 3-50 chars)
- Validate password (min 8 chars)
- Validate amount (positive number)
- Validate date format
- Validate file format (JPG/PNG/PDF)
- Validate file size (max 5MB)

### 7.4 Timestamp Utility

**Purpose**: Generate IST timestamps

**Responsibilities**:
- Generate current IST timestamp
- Format: ISO-8601 with timezone offset
- Timezone: Asia/Kolkata
- **Application-layer generation only**
- **NO database-generated timestamps**

---

## 8. Main Process Entry Point

### 8.1 index.js Design

**Responsibilities**:
- Initialize Electron app
- Create main window
- Configure security (`contextIsolation=true`, `nodeIntegration=false`)
- Load preload script
- Initialize database
- Instantiate repositories
- Instantiate services
- Instantiate controllers
- Register IPC handlers
- Handle app lifecycle (ready, window-all-closed, activate)
- Trigger auto backup on startup

---

## 9. Database Schema Design

### 9.1 Table Definitions (Conceptual)

**users**:
- Primary key: `id`
- Unique constraint: `username`
- Foreign keys: `created_by`, `updated_by` → `users(id)`
- Soft delete: `is_deleted`
- Audit fields: `created_at`, `updated_at`

**projects**:
- Primary key: `id`
- Status: ACTIVE/CLOSED
- Foreign keys: `created_by`, `updated_by` → `users(id)`
- Soft delete: `is_deleted`
- Audit fields: `created_at`, `updated_at`

**shops**:
- Primary key: `id`
- Status: ACTIVE/CLOSED
- Foreign keys: `created_by`, `updated_by` → `users(id)`
- Soft delete: `is_deleted`
- Audit fields: `created_at`, `updated_at`

**categories**:
- Primary key: `id`
- Type: PAYMENT/EXPENSE
- Foreign keys: `created_by`, `updated_by` → `users(id)`
- Soft delete: `is_deleted`
- Audit fields: `created_at`, `updated_at`

**ledger_entries**:
- Primary key: `id`
- Foreign keys: `project_id`, `category_id`, `shop_id` (nullable), `created_by`, `updated_by` → respective tables
- Business date: `action_date`
- Soft delete: `is_deleted`
- Audit fields: `created_at`, `updated_at`
- Attachment paths: comma-separated relative paths

**ledger_audit_trail**:
- Primary key: `id`
- Foreign keys: `ledger_entry_id` → `ledger_entries(id)`, `changed_by` → `users(id)`
- Action type: CREATE/UPDATE/DELETE
- Field-level tracking: `field_name`, `old_value`, `new_value`
- Timestamp: `changed_at`
- **Immutable** (no updates or deletes)

### 9.2 Index Design (Conceptual)

**Performance Indexes**:
- `ledger_entries(project_id, action_date)` - Project ledger queries
- `ledger_entries(shop_id, action_date)` - Shop ledger queries
- `ledger_entries(category_id)` - Category filtering
- `ledger_entries(is_deleted)` - Soft delete filtering
- `ledger_audit_trail(ledger_entry_id)` - Audit trail lookup
- `users(username)` - Login queries

---

## 10. Error Handling Strategy

### 10.1 Error Propagation

**Repository Layer**:
- Throw database errors
- Log SQL errors

**Service Layer**:
- Catch repository errors
- Throw business logic errors with user-friendly messages
- Log errors

**Controller Layer**:
- Catch service errors
- Return `{success: false, error: message}`
- Log errors

**UI Layer**:
- Display error messages to user
- Log errors to console

### 10.2 Error Types

- **Authentication Errors**: Invalid credentials, session expired
- **Authorization Errors**: Insufficient permissions
- **Validation Errors**: Invalid input, business rule violations
- **Database Errors**: Connection failures, constraint violations
- **File System Errors**: Attachment upload failures, backup failures

---

## 11. Security Design

### 11.1 Password Security

- Hash with bcrypt (cost factor 10)
- Never log or expose password hashes
- Validate password strength (min 8 chars)

### 11.2 Session Security

- In-memory only (Map data structure)
- No persistence to disk
- **NO sessionStorage**
- **NO localStorage**
- **NO cookies**
- Cleared on app restart

### 11.3 SQL Injection Prevention

- Parameterized queries in all repositories
- Never concatenate user input into SQL
- Use `?` placeholders

### 11.4 Electron Security

- `contextIsolation = true`
- `nodeIntegration = false`
- Preload script as secure bridge
- No direct Node.js access from renderer

---

## 12. Backup & Recovery Design

### 12.1 Backup Strategy

**Auto Weekly Backup**:
- Trigger: On app startup
- Condition: Last backup > 7 days
- Process: Close DB → Copy file → Reopen DB
- Retention: Keep last 8 backups
- Error handling: Log error, continue app startup

**On-Demand Backup**:
- Trigger: ADMIN user action
- User selects destination folder
- Process: Close DB → Copy file → Reopen DB
- Confirmation: Display success/failure message

### 12.2 Recovery Process

**Manual Restore**:
- User closes app
- User replaces `builder-ledger.db` with backup file
- User restarts app

---

## 13. Attachment Handling Design

### 13.1 Upload Process

1. Validate file format (JPG/PNG/PDF)
2. Validate file size (max 5MB)
3. Validate file count (max 5 per entry)
4. Generate destination path: `{year}/{month}/{entry_id}/`
5. Copy file to destination
6. Store relative path in database (comma-separated)

### 13.2 Retrieval Process

1. Read `attachment_path` from database
2. Split by comma
3. Construct absolute paths
4. Return file paths to UI
5. UI displays/downloads files

---

## 14. Timestamp Generation Design

### 14.1 IST Timestamp Utility

**Purpose**: Generate all timestamps in application layer

**Requirements**:
- Timezone: Asia/Kolkata (IST)
- Format: ISO-8601 with timezone offset
- **NO database-generated timestamps**
- **NO triggers**

**Usage**:
- Generate `action_date` before inserting ledger entry
- Generate `created_at` before inserting any record
- Generate `updated_at` before updating any record
- Generate `changed_at` before inserting audit record

---

**Document Status**: ✅ Production-Ready  
**Approved By**: [Pending]  
**Date**: 2026-01-15
