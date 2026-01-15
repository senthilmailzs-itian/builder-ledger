YOU ARE A SENIOR UX ARCHITECT AND FRONTEND DESIGNER.

YOUR TASK IS TO GENERATE STATIC, FUNCTIONAL UI MOCKUP SCREENS
FOR A DESKTOP APPLICATION CALLED “BUILDER LEDGER”.

THIS PROMPT IS FOR DEMO AND USER VALIDATION PURPOSES ONLY.
THIS IS NOT AN IMPLEMENTATION CONTRACT.
DO NOT GENERATE APPLICATION LOGIC.

=================================================
PRIMARY PURPOSE
=================================================

- Create visual UI mockups for early user demonstration
- Validate navigation, screen flow, labels, and usability
- Deploy as STATIC PAGES on GitLab Pages
- Collect feedback BEFORE development starts

=================================================
CRITICAL SCOPE BOUNDARY
=================================================

THIS PROMPT IS STRICTLY UI-ONLY.

YOU MUST NOT:
- Mention Electron
- Mention IPC
- Mention SQLite or databases
- Mention services, repositories, or business logic
- Implement authentication logic
- Implement authorization logic
- Implement calculations
- Use JavaScript for logic
- Use APIs
- Use backend concepts

YOU MAY:
- Use static HTML
- Use Bootstrap components
- Use dummy/static data
- Use simple anchor-based navigation
- Use placeholder values

=================================================
TECHNOLOGY RULES (FINAL)
=================================================

- HTML ONLY
- Bootstrap 5.3 ONLY (LOCAL FILES, NOT CDN)
- Optional minimal CSS for styling
- NO JavaScript (except Bootstrap bundle if absolutely required)
- NO frameworks
- NO build tools

=================================================
DESIGN LANGUAGE
=================================================

- Desktop-first layout
- Clean enterprise look
- Purple gradient theme:
  - Primary: #667eea
  - Secondary: #764ba2
- Consistent header and sidebar layout
- Indian Rupee formatting in UI text:
  Example: ₹25,00,000

NOTE: Mobile responsiveness was added as an enhancement
beyond the original desktop-first specification.

=================================================
APPLICATION CONTEXT (FOR UI ONLY)
=================================================

Builder Ledger is a construction finance tracking application.

Conceptual entities:
- Projects
- Shops (vendors)
- Categories (Payment / Expense)
- Ledger Entries

These are ONLY for LABELING and SCREEN FLOW.
DO NOT IMPLEMENT RULES OR VALIDATIONS.

=================================================
ROLE-BASED SCREEN SET (UI ONLY)
=================================================

ROLE: ADMIN
- Login Screen (shared)
- Dashboard (summary cards – static)
- User Management
- Project Management
- Shop Management
- Category Management
- Project Ledger View (read-only)
- Shop Ledger View (read-only)
- Audit Trail (read-only)
- Backup History

ROLE: ACCOUNTANT
- Dashboard
- Project Ledger View
- Shop View
- Ledger Entry Form
- Audit Trail (read-only)
- Backup History (read-only)

ROLE: REPORT_VIEWER
- Dashboard (read-only)
- Project View (read-only)
- Shop View (read-only)
- Audit Trail (read-only)
- Backup History (read-only)

=================================================
LEDGER ENTRY FORM (UI MOCKUP ONLY)
=================================================

Include fields visually:
- Project (dropdown)
- Category (dropdown)
- Shop (dropdown)
- Amount (₹ input)
- Action Date (date picker)
- Description (textarea)
- Payment Mode (dropdown – visual only)
- Attachment upload (visual only)

NO VALIDATION LOGIC.
NO CONDITIONAL BEHAVIOR.
DISPLAY ONLY.

=================================================
NAVIGATION REQUIREMENTS
=================================================

- Sidebar navigation per role
- Header with application name
- Logout link (visual only)
- Breadcrumbs (optional)
- All navigation via anchor links

=================================================
MOCKUP NAVIGATOR (MANDATORY)
=================================================

Generate ONE index page that:
- Lists ALL screens
- Groups screens by role
- Provides links to each mockup page
- Acts as a demo hub for stakeholders

=================================================
FILE STRUCTURE (OUTPUT)
=================================================

Generate a flat, GitLab Pages–friendly structure:

/mockups
  /assets
    /css
    /bootstrap
  index.html        (Mockup Navigator)
  login.html
  admin-*.html
  accountant-*.html
  viewer-*.html

=================================================
IMPORTANT OUTPUT RULES
=================================================

- Static HTML ONLY
- Dummy data ONLY
- No calculations
- No real workflows
- Screens must be visually complete
- Labels and layout must be realistic
- Assume users will click and explore

=================================================
FINAL REMINDER
=================================================

THESE MOCKUPS ARE FOR DEMO PURPOSES ONLY.
THEY DO NOT DEFINE IMPLEMENTATION DETAILS.
THEY MUST NOT CONFLICT WITH THE FROZEN ENGINEERING PROMPT.

# END OF UI MOCKUP PROMPT