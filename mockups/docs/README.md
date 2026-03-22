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
│       └── mobile-responsive.css (mobile/tablet responsive styles)
├── index.html                          # Mockup Navigator (START HERE)
├── login.html                          # Login Screen
├── admin-dashboard.html                # ADMIN Dashboard
├── admin-user-management.html          # ADMIN User Management
├── admin-project-management.html       # ADMIN Project Management
├── admin-shop-management.html          # ADMIN Shop Management
├── admin-category-management.html      # ADMIN Category Management
├── admin-project-ledger.html           # ADMIN Project Ledger View (read-only)
├── admin-shop-ledger.html              # ADMIN Shop Ledger View (read-only)
├── admin-audit-trail.html              # ADMIN Audit Trail
├── admin-backup-history.html           # ADMIN Backup History
├── accountant-dashboard.html           # ACCOUNTANT Dashboard
├── accountant-project-ledger.html      # ACCOUNTANT Project Ledger (Add/Edit/Delete)
├── accountant-shop-view.html         # ACCOUNTANT Shop Ledger (Make Payments)
├── accountant-audit-trail.html         # ACCOUNTANT Audit Trail (read-only)
├── accountant-backup-history.html      # ACCOUNTANT Backup History (read-only)
├── viewer-dashboard.html               # REPORT_VIEWER Dashboard
├── viewer-project-view.html            # REPORT_VIEWER Project Ledger (read-only)
├── viewer-shop-view.html               # REPORT_VIEWER Shop Ledger (read-only)
├── viewer-audit-trail.html             # REPORT_VIEWER Audit Trail (read-only)
└── viewer-backup-history.html          # REPORT_VIEWER Backup History (read-only)
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

## Usage

1. Open `index.html` in your browser to see the mockup navigator
2. Click on any role section to navigate to specific screens
3. Use the sidebar navigation within each screen to explore different views
4. All buttons and forms are static (no backend functionality)

## Mobile Responsiveness

All mockup screens are now mobile-responsive with the following features:

- **Responsive Breakpoints**: Optimized for desktop (>768px), tablet (768px), and mobile (<576px)
- **Flexible Layouts**: Cards and content stack vertically on smaller screens
- **Scrollable Tables**: Tables become horizontally scrollable on mobile to preserve data visibility
- **Adjusted Typography**: Font sizes scale down appropriately for mobile devices
- **Touch-Friendly**: Buttons and interactive elements sized for touch targets
- **Sidebar Optimization**: Sidebar navigation adapts for mobile viewing

The responsive styles are defined in `assets/css/mobile-responsive.css` and automatically applied to all screens.

## Design Features

- **Purple Gradient Theme**: Uses a professional purple gradient (`#667eea` to `#764ba2`) throughout
- **Indian Rupee Formatting**: All currency values displayed with ₹ symbol and Indian number formatting (e.g., ₹25,00,000)
- **Role-Based Navigation**: Each role has a distinct sidebar with appropriate menu items
- **Consistent Layout**: Header with app name, user info, and logout; sidebar navigation; main content area
- **Bootstrap 5.3 Components**: Cards, tables, forms, modals, badges, and buttons
- **Dual Ledger Terminology**:
  - **Project Ledger**: Uses `RECEIPT` (money in / green badge) and `EXPENSE` (money out / warning badge)
  - **Shop Ledger**: Uses `PURCHASE` (material bought / warning badge) and `PAYMENT` (paid to shop / green badge)
- **3-Card Summary Rows**: Each ledger screen displays three gradient summary cards side by side:
  - *Project Ledger*: 🟢 Overall Receipt | 🟣 Current Project Balance | 🔴 Overall Expense
  - *Shop Ledger*: 🟢 Total Purchases | 🟣 Amount Paid | 🔴 Outstanding Payable
- **Shop Bill Support**: Shop PURCHASE entries use `Shop Bill` as Payment Mode with `BILL-YYYY-MMDD` reference and `bill_receipt.pdf` attachment
- **Advanced Tables**: Ledger tables include multi-select filters, sorting indicators (except Amount column), pagination, and a detailed "View Entry" pop-up modal
- **Context-Aware View Modal**: Project Ledger modal shows Labor/direct expenses (Cash, no shop, no attachment); Shop Ledger modal shows Shop Bill entries (bill number, bill_receipt.pdf)
- **Shop Ledger Modals & Actions**: `PURCHASE` rows have View/Pay buttons ("Pay for Purchase" modal pre-fills specific purchase amount). `PAYMENT` rows have View/Edit/Delete buttons. "Make Shop Payment" removes Project mapping, uses "Action Date", adds Comments/Attachments, and excludes "Shop Bill" from Payment Modes. Delete confirmations use a standard layout (red border, warning alert box).
- **Project Ledger Modals & Actions**: The "Add Entry" modal includes "Shop Bill" as a payment mode. The "Edit Entry" modal correctly disables the Project dropdown (to prevent moving entries between projects) and supports editing shop-linked expenses (demonstrating "Shop Bill", bill reference, and attachment).
- **Audit Columns**: Management tables (Users, Projects, Shops, Categories) display `Created By`, `Created Date`, `Updated By`, `Updated Date`
- **Dashboard Audit Widget**: Dashboards show a "Recent Ledger Activity" table with 9-column Audit Trail format (Last 5 Entries) and a "View Full Audit Trail" link
- **Unified Page Titles**: No "(Read-Only)" suffix in page headings — the role displayed in the navbar indicates the access level
- **Global Branding**: Navigation bars display the "Dream Builders, Thiruvarur" company name and logo (`assets/img/dream builders.png`). Every screen features a styled global flexbox footer stating `© 2026 Dream Builders, Thiruvarur. Software by` paired with the `assets/img/Dheeran OneClick Logo.png` image logo and the tagline `"Think Simple, Use Simple"`.
- **Backup Note Bar**: A styled yellow info bar below the table (not a top alert) for backup access notes
- **Static Data**: All screens contain realistic dummy data for demonstration purposes

## Role-Based Screens

### ADMIN (9 screens) ✅
- Dashboard with summary cards + Recent Ledger Activity widget
- User Management (add/edit/deactivate users)
- Project Management (add/edit/close projects)
- Shop Management (add/edit/close shops)
- Category Management (payment & expense categories)
- Project Ledger View (read-only, filters + sorting + pagination + View modal)
- Shop Ledger View (read-only, filters + sorting + pagination + View modal)
- Audit Trail (9-column field-level change tracking)
- Backup History (auto & manual backups, 8-week retention)

### ACCOUNTANT (5 screens) ✅
- Dashboard — ✅ same as Admin/Viewer (stat cards + Recent Ledger Activity widget + View Full Audit Trail link)
- Project Ledger (add/edit/delete entries) — ✅ 3-card summary + filters + table + Add/Edit Entry modals + View modal
- Shop Ledger (make shop payments) — ✅ 3-card summary + PURCHASE/PAYMENT types + Make Payment modal (Action Date, no project, updated delete confirm) + Pay for Purchase modal
- Audit Trail — ✅ same 9-column format, 4-filter bar (Date From, Date To, User, Action)
- Backup History — ✅ same layout; yellow bottom note bar (view-only, contact ADMIN); 8-week info card below title

### REPORT_VIEWER (5 screens) ✅
- Dashboard with summary cards + Recent Ledger Activity widget
- Project Ledger (read-only, filters + sorting + pagination + View modal)
- Shop Ledger (read-only, filters + sorting + pagination + View modal)
- Audit Trail (read-only, 9-column layout)
- Backup History (read-only, yellow note bar at bottom)

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

## How These Were Generated (The UI Mockup Prompt)

These mockups were generated using a strict, UI-only prompt file:  
`mockups/docs/FINAL-ANTIGRAVITY-UI-MOCKUP-PROMPT.md`

That prompt was written *after* the backend architecture and database schema were defined by the Master Prompt (`docs/00-FINAL-ANTIGRAVITY-PROMPT.md`). Because the UI prompt is based on the final database schema, it ensures that all forms and tables in these mockups have the exact correct fields (e.g., `amount`, `action_date`, `shop_id`).

## Relationship to Engineering Docs

These mockups are **completely separate from** the actual application engineering code:

- **Master Architectural Prompt** (`docs/00-FINAL-ANTIGRAVITY-PROMPT.md`): Dictates the backend rules, database schema, and IPC logic.
- **Engineering Docs** (`docs/01` to `07`): The actual technical specifications, architecture, and database design.
- **UI Mockups** (`mockups/` folder): Visual HTML/CSS demonstration for user validation only. No backend code.

---

**Status**: ✅ Admin (9/9) | ✅ Report Viewer (5/5) | ✅ Accountant (5/5 — All screens confirmed)  
**Total Screens**: 21 HTML files  
**Last Updated**: 2026-03-22
