# Builder Ledger - UI Mockups

## Overview

This directory contains **static HTML UI mockups** for the Builder Ledger application. These mockups are for **demo and user validation purposes only** and do not contain any application logic.

## Purpose

- Visual demonstration of UI screens
- Validate navigation flow and screen layouts
- Collect stakeholder feedback BEFORE development
- Can be deployed to GitLab Pages for remote review

## Technology Stack

- **HTML**: Static pages
- **Bootstrap 5.3**: Local files (required)
- **CSS**: Minimal custom styling for purple gradient theme
- **JavaScript**: Bootstrap bundle only (no application logic)

## File Structure

```
mockups/
├── assets/
│   ├── bootstrap/
│   │   ├── css/
│   │   │   └── bootstrap.min.css (REQUIRED - download separately)
│   │   └── js/
│   │       └── bootstrap.bundle.min.js (REQUIRED - download separately)
│   └── css/
│       └── (optional custom CSS)
├── index.html                          # Mockup Navigator (START HERE)
├── login.html                          # Login Screen
├── admin-dashboard.html                # ADMIN Dashboard
├── admin-user-management.html          # ADMIN User Management
├── admin-project-management.html       # ADMIN Project Management
├── admin-shop-management.html          # ADMIN Shop Management
├── admin-category-management.html      # ADMIN Category Management
├── admin-project-ledger.html           # ADMIN Project Ledger (Read-Only)
├── admin-shop-ledger.html              # ADMIN Shop Ledger (Read-Only)
├── admin-audit-trail.html              # ADMIN Audit Trail
├── admin-backup-history.html           # ADMIN Backup History
├── accountant-dashboard.html           # ACCOUNTANT Dashboard
├── accountant-project-ledger.html      # ACCOUNTANT Project Ledger (Add/Edit/Delete)
├── accountant-shop-view.html           # ACCOUNTANT Shop View (Make Payments)
├── accountant-ledger-entry-form.html   # ACCOUNTANT Ledger Entry Form
├── accountant-audit-trail.html         # ACCOUNTANT Audit Trail (Read-Only)
├── accountant-backup-history.html      # ACCOUNTANT Backup History (Read-Only)
├── viewer-dashboard.html               # REPORT_VIEWER Dashboard (Read-Only)
├── viewer-project-view.html            # REPORT_VIEWER Project View (Read-Only)
├── viewer-shop-view.html               # REPORT_VIEWER Shop View (Read-Only)
├── viewer-audit-trail.html             # REPORT_VIEWER Audit Trail (Read-Only)
└── viewer-backup-history.html          # REPORT_VIEWER Backup History (Read-Only)
```

## Setup Instructions

### Step 1: Download Bootstrap 5.3

1. Visit [https://getbootstrap.com/docs/5.3/getting-started/download/](https://getbootstrap.com/docs/5.3/getting-started/download/)
2. Download "Compiled CSS and JS"
3. Extract the files
4. Copy the following files to the mockups directory:
   - `bootstrap.min.css` → `mockups/assets/bootstrap/css/bootstrap.min.css`
   - `bootstrap.bundle.min.js` → `mockups/assets/bootstrap/js/bootstrap.bundle.min.js`

### Step 2: Open in Browser

1. Navigate to the `mockups/` directory
2. Open `index.html` in your web browser
3. Click on any screen link to navigate

## Design Features

### Theme
- **Primary Color**: #667eea (Purple)
- **Secondary Color**: #764ba2 (Dark Purple)
- **Gradient**: Linear gradient from primary to secondary
- **Layout**: Desktop-first, clean enterprise look

### Currency Formatting
- All amounts displayed in Indian Rupee (₹)
- Format: ₹12,50,000 (Indian numbering system)

### Navigation
- Sidebar navigation (role-specific)
- Header with app name and user info
- Logout link (visual only)
- Breadcrumbs where applicable

## Role-Based Screens

### ADMIN (9 screens)
- Dashboard with summary cards
- User Management (add/edit/deactivate users)
- Project Management (add/edit/close projects)
- Shop Management (add/edit/close shops)
- Category Management (payment & expense categories)
- Project Ledger View (read-only)
- Shop Ledger View (read-only)
- Audit Trail (field-level change tracking)
- Backup History (auto & manual backups)

### ACCOUNTANT (6 screens)
- Dashboard with project summary
- Project Ledger (add/edit/delete entries)
- Shop View (make shop payments)
- Ledger Entry Form (complete entry form)
- Audit Trail (read-only)
- Backup History (read-only)

### REPORT_VIEWER (5 screens)
- Dashboard (read-only summary)
- Project View (read-only ledger)
- Shop View (read-only payables)
- Audit Trail (read-only)
- Backup History (read-only)

## Important Notes

### Static Mockups Only
- **No real data**: All data is dummy/placeholder
- **No calculations**: Balances and totals are static
- **No validation**: Forms do not validate inputs
- **No persistence**: Nothing is saved
- **No authentication**: Login is visual only

### Navigation
- All navigation uses anchor links (`<a href="...">`)
- No JavaScript routing
- No state management
- Each page is independent

### Interactivity
- Buttons show alerts ("Static mockup - no data saved")
- Modals open/close (Bootstrap functionality)
- Dropdowns and date pickers work (HTML5 inputs)
- No actual CRUD operations

## Deployment to GitLab Pages

1. Ensure Bootstrap files are in place
2. Commit all files to Git repository
3. Push to GitLab
4. Enable GitLab Pages in repository settings
5. Access via: `https://your-username.gitlab.io/builder-ledger/mockups/`

## Feedback Collection

When sharing with stakeholders:

1. Start with `index.html` (Mockup Navigator)
2. Ask them to explore each role's screens
3. Collect feedback on:
   - Screen layouts
   - Navigation flow
   - Labels and terminology
   - Missing features
   - Usability issues

## Next Steps

After mockup validation:

1. Review feedback with stakeholders
2. Update mockups based on feedback
3. Freeze mockup design
4. Use as reference for actual implementation
5. Refer to engineering documentation in `docs/` folder

## Relationship to Engineering Docs

These mockups are **separate from** the engineering documentation:

- **Engineering Docs** (`docs/` folder): Technical specifications, architecture, database design
- **UI Mockups** (`mockups/` folder): Visual demonstration for user validation

Both should be aligned but serve different purposes.

---

**Status**: ✅ Complete  
**Total Screens**: 22 HTML files  
**Last Updated**: 2026-01-15
