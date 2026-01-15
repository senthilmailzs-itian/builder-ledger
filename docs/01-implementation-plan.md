# Builder Ledger - Detailed Implementation Plan

## Document Information
- **Version**: 1.1
- **Last Updated**: 2026-01-15
- **Status**: Production-Ready
- **Purpose**: Phase-wise development roadmap for Builder Ledger (development activities only)

---

## Executive Summary

This implementation plan outlines the **development-only** phases for Builder Ledger, an offline-first Electron desktop application for construction project financial management.

**Scope**: Development activities only (no separate testing/UAT/documentation phases)
**Approach**: Copilot-driven execution with clear feature sequencing
**Timeline**: 60-75 days (~2.5-3 months)

---

## Phase 1: Project Foundation

### Duration: 5-7 days

### Objectives
- Initialize Electron project structure
- Set up development environment
- Configure SQLite database with WAL mode

### Tasks
- [ ] Create project folder structure (`/src/main`, `/src/renderer`, `/src/services`, `/src/repositories`)
- [ ] Initialize `package.json` with Electron, SQLite3, bcrypt dependencies
- [ ] Download and configure local Bootstrap 5.3 assets (no CDN)
- [ ] Set up ESLint and Prettier
- [ ] Create database schema (users, projects, shops, categories, ledger_entries, ledger_audit_trail)
- [ ] Enable WAL mode and foreign key enforcement
- [ ] Create seed data (default admin user, payment/expense categories)

### Deliverables
- Working Electron boilerplate
- SQLite database with schema
- Local Bootstrap assets

---

## Phase 2: Core Architecture

### Duration: 10-12 days

### Objectives
- Implement layered architecture (UI → IPC → Services → Repositories → DB Adapter)
- Build database abstraction layer
- Implement repository pattern

### Tasks
- [ ] Create DB Adapter with connection management, transactions, parameterized queries
- [ ] Implement Base Repository with CRUD methods
- [ ] Create User Repository (authentication queries, soft delete)
- [ ] Create Project Repository (CRUD, lifecycle management)
- [ ] Create Shop Repository (CRUD, lifecycle management)
- [ ] Create Category Repository (CRUD)
- [ ] Create Ledger Repository (complex queries for balances, shop payables)
- [ ] Create Audit Repository (insert-only for ledger changes)

### Deliverables
- DB Adapter abstraction
- 6 repository classes
- No SQL in service layer

---

## Phase 3: Authentication & Security

### Duration: 4-5 days

### Objectives
- Implement local authentication with bcrypt
- Create in-memory session management
- Configure Electron security (context isolation)

### Tasks
- [ ] Implement bcrypt password hashing
- [ ] Create Auth Service (login/logout)
- [ ] Implement in-memory session manager (no persistence)
- [ ] Create session validation middleware
- [ ] Configure `contextIsolation = true`, `nodeIntegration = false`
- [ ] Create preload script with secure IPC bridge

### Deliverables
- Auth Service
- Session Manager
- Secure preload script

---

## Phase 4: Business Logic Layer

### Duration: 12-15 days

### Objectives
- Implement service layer with business rules
- Enforce authorization at service level
- Implement ledger entry logic with payment category rules

### Tasks
- [ ] Create User Service (user management, role assignment, authorization checks)
- [ ] Create Project Service (CRUD, open/close lifecycle, ADMIN-only enforcement)
- [ ] Create Shop Service (CRUD, open/close lifecycle, ADMIN-only enforcement)
- [ ] Create Category Service (CRUD)
- [ ] Create Ledger Service with:
  - Payment Received (shop = NULL)
  - Shop Payment (shop required, ACTIVE shop check)
  - Refund to Customer (shop = NULL, balance > 0 check)
  - Expense categories (shop optional)
- [ ] Implement balance calculation (derived, not stored)
- [ ] Implement shop payable calculation
- [ ] Create Audit Service (field-level change tracking)
- [ ] Create Attachment Service (file upload, validation: JPG/PNG/PDF, 5MB, max 5 files)
- [ ] Create Backup Service (auto weekly, on-demand)

### Deliverables
- 7 service classes with business logic
- Authorization enforcement
- Audit trail integration

---

## Phase 5: IPC Communication Layer

### Duration: 6-8 days

### Objectives
- Create IPC controllers for all entities
- Implement error handling and response formatting
- Expose secure APIs via preload

### Tasks
- [ ] Create Auth Controller (login, logout, session validation)
- [ ] Create User Controller (user CRUD, role management)
- [ ] Create Project Controller (CRUD, lifecycle operations)
- [ ] Create Shop Controller (CRUD, lifecycle operations)
- [ ] Create Category Controller (CRUD)
- [ ] Create Ledger Controller (entry CRUD, balance queries, shop payables)
- [ ] Create Audit Controller (audit trail queries)
- [ ] Create Backup Controller (backup operations)
- [ ] Update preload script with all IPC APIs
- [ ] Implement consistent error response format

### Deliverables
- 8 IPC controllers
- Complete preload API
- Error handling

---

## Phase 6: User Interface Development

### Duration: 18-22 days

### Objectives
- Build all UI screens for 3 roles (ADMIN, ACCOUNTANT, REPORT_VIEWER)
- Implement role-based navigation
- Create forms with validation

### Tasks

**Authentication UI** (2 days):
- [ ] Create login screen with username/password
- [ ] Implement client-side validation
- [ ] Add error message display
- [ ] Implement logout functionality

**ADMIN Screens** (8 days):
- [ ] User Management (list, add, edit, activate/deactivate, soft delete)
- [ ] Project Management (list, add, edit, open/close, soft delete, status filter)
- [ ] Shop Management (list, add, edit, open/close, soft delete, status filter)
- [ ] Category Management (list by type, add, edit, soft delete)
- [ ] View Project Ledger (read-only, project selector, date filter, balance display)
- [ ] View Shop Ledger (read-only, shop selector, outstanding payable)
- [ ] Audit Trail (date filter, user filter, action filter, field-level changes)
- [ ] Backup History (list backups, trigger on-demand backup with folder selection)

**ACCOUNTANT Screens** (8 days):
- [ ] Dashboard (view by Project/Shop toggle, status filter, summary cards)
- [ ] Project View (project selector, date filter, entry list, add/edit/delete, balance, attachments)
- [ ] Add/Edit Entry Modal (action date, category, shop, amount, description, payment details, attachments)
- [ ] Shop View (shop selector, project-wise breakdown, outstanding payable, make payment button)
- [ ] Make Shop Payment Modal (amount, date, mode, reference)
- [ ] Audit Trail (read-only)
- [ ] Backup History (read-only, no trigger button)

**REPORT_VIEWER Screens** (2 days):
- [ ] Reuse ACCOUNTANT screens with UI elements hidden (no add/edit/delete buttons)

### Deliverables
- Login screen
- 8 ADMIN screens
- 5 ACCOUNTANT screens
- 5 REPORT_VIEWER screens (read-only versions)

---

## Phase 7: System Features

### Duration: 5-6 days

### Objectives
- Implement automatic weekly backup
- Implement logging system
- Add timestamp generation (IST timezone)

### Tasks
- [ ] Implement startup backup check (last backup > 7 days)
- [ ] Create backup logic (close DB, copy file, reopen DB)
- [ ] Implement retention policy (keep last 8 backups)
- [ ] Add error handling (backup failure must not block app)
- [ ] Implement file-based logger (Winston)
- [ ] Configure daily log rotation (retain 30 days)
- [ ] Ensure no sensitive data logged
- [ ] Implement IST timestamp generation in application layer (no database-generated timestamps)

### Deliverables
- Backup Service with auto weekly + on-demand
- Logging system
- IST timestamp utilities

---

## Phase 8: Packaging & Deployment

### Duration: 4-5 days

### Objectives
- Configure electron-builder for Windows x64
- Create NSIS installer
- Set up file permissions for shared database

### Tasks
- [ ] Configure `electron-builder.json` for Windows x64 NSIS installer
- [ ] Set installation paths:
  - Binaries: `C:\Program Files\Builder Ledger\`
  - Data: `C:\ProgramData\BuilderLedger\`
- [ ] Configure file permissions for multi-user access
- [ ] Create desktop and start menu shortcuts
- [ ] Implement first-run detection and database initialization
- [ ] Create default admin user setup
- [ ] Build installer and test on clean Windows 10/11 machine

### Deliverables
- NSIS installer (.exe)
- Multi-user shared database access
- First-run setup

---

## Timeline Summary

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Foundation | 5-7 days | None |
| Phase 2: Core Architecture | 10-12 days | Phase 1 |
| Phase 3: Authentication | 4-5 days | Phase 2 |
| Phase 4: Business Logic | 12-15 days | Phase 3 |
| Phase 5: IPC Layer | 6-8 days | Phase 4 |
| Phase 6: UI Development | 18-22 days | Phase 5 |
| Phase 7: System Features | 5-6 days | Phase 6 |
| Phase 8: Packaging | 4-5 days | Phase 7 |

**Total Duration**: 64-80 days (~2.5-3 months)

---

## Feature Sequencing

### Critical Path
1. Database schema → Repositories → Services → IPC → UI
2. Authentication must be complete before any role-based features
3. Ledger Service must be complete before UI screens
4. Backup Service can be developed in parallel with UI

### Dependencies
- **UI depends on**: Complete IPC layer
- **IPC depends on**: Complete Service layer
- **Services depend on**: Complete Repository layer
- **Repositories depend on**: Database schema

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| SQLite file locking in multi-user scenario | Use WAL mode, test concurrent access early |
| File permission issues | Configure NSIS installer with proper ACLs, test on multiple Windows accounts |
| Timestamp timezone issues | Generate all timestamps in application layer with explicit IST timezone |
| Backup failure blocking app | Wrap backup in try-catch, log errors, continue app startup |

---

## Success Criteria

### Functional
- ✅ All 3 roles (ADMIN, ACCOUNTANT, REPORT_VIEWER) fully functional
- ✅ Ledger entry CRUD with payment category rules enforced
- ✅ Project/Shop lifecycle (ACTIVE/CLOSED) working
- ✅ Attachments upload/retrieval (5 files, 5MB each)
- ✅ Field-level audit trail for ledger entries
- ✅ Automatic weekly backup + on-demand backup
- ✅ Multi-user shared database access

### Non-Functional
- ✅ 100% offline operation (no internet at runtime)
- ✅ Secure authentication (bcrypt, in-memory sessions)
- ✅ Context isolation and secure IPC
- ✅ IST timestamps generated by application
- ✅ Responsive UI with local Bootstrap

---

## Out of Scope (V1)

The following are **explicitly excluded** from this implementation plan:

- ❌ Separate Testing phases (unit tests, integration tests, UAT)
- ❌ Testing frameworks or coverage mandates
- ❌ Documentation phases
- ❌ Release/deployment phases beyond installer creation
- ❌ User training or change management
- ❌ Data migration from manual ledgers
- ❌ Export to Excel/PDF
- ❌ Advanced reporting features
- ❌ Mobile companion app

---

## Post-V1 Considerations

### Future Enhancements (V1.2+)
- Export ledger to Excel/PDF
- Advanced reporting (profit/loss, project summaries)
- Bulk entry import from CSV
- Database migration to PostgreSQL (using repository abstraction)

---

**Document Status**: ✅ Production-Ready  
**Approved By**: [Pending]  
**Date**: 2026-01-15
