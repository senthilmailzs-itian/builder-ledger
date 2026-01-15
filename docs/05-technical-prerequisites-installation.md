# Builder Ledger - Technical Prerequisites & Installation Guide

## Document Information
- **Version**: 1.1
- **Last Updated**: 2026-01-15
- **Status**: Production-Ready
- **Purpose**: Setup and installation guide for developers and end-users

---

## 1. System Requirements

### 1.1 End-User Requirements

**Operating System**:
- Windows 10 (64-bit) - Version 1809 or later
- Windows 11 (64-bit) - All versions

**Hardware**:
- **Processor**: Intel Core i3 or equivalent (2.0 GHz minimum)
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 500 MB free disk space
- **Display**: 1280x720 minimum resolution

**Permissions**:
- **Administrator rights** required ONLY for installation
- **Standard user rights** sufficient for running the application

**Additional Requirements**:
- **No internet connection required at runtime**
- Application works offline

---

### 1.2 Developer Requirements

**Operating System**:
- Windows 10/11 (64-bit) for development and testing
- macOS/Linux supported for development only (not for packaging)

**Development Tools**:
- **Node.js**: v18.x or v20.x LTS
- **npm**: v9.x or v10.x (comes with Node.js)
- **Git**: v2.40 or later
- **Code Editor**: VS Code recommended

**Internet Access**:
- **Required during development**: For downloading Node.js, Electron, npm packages
- **Required for Git/GitHub**: Version control and collaboration
- **Required for GitHub Copilot**: AI coding assistance (optional)
- **NOT required at runtime**: Application runs 100% offline

**Optional Tools**:
- **SQLite Browser**: For database inspection
- **DB Browser for SQLite**: GUI tool for viewing database

---

## 2. Developer Setup

### 2.1 Install Node.js

**Download**:
1. Visit [https://nodejs.org/](https://nodejs.org/)
2. Download **LTS version** (18.x or 20.x)
3. Run installer with default settings

**Verify Installation**:
```powershell
node --version
# Expected: v18.x.x or v20.x.x

npm --version
# Expected: v9.x.x or v10.x.x
```

---

### 2.2 Clone Repository

```powershell
# Navigate to your projects directory
cd C:\Users\<YourUsername>\Documents\GitHub

# Clone repository
git clone https://github.com/your-org/builder-ledger.git

# Navigate to project directory
cd builder-ledger
```

---

### 2.3 Install Dependencies

```powershell
# Install all npm dependencies
npm install

# Expected output: dependencies installed without errors
```

**Key Dependencies** (automatically installed):
- `electron`: ^28.0.0
- `sqlite3`: ^5.1.6
- `bcrypt`: ^5.1.1
- `winston`: ^3.11.0

**Local Assets** (included in repository):
- Bootstrap 5.3 (CSS and JS)
- No CDN dependencies

---

### 2.4 Download Local Bootstrap Assets

**If not already in repository**:

1. Visit [https://getbootstrap.com/docs/5.3/getting-started/download/](https://getbootstrap.com/docs/5.3/getting-started/download/)
2. Download "Compiled CSS and JS"
3. Extract to `src/renderer/assets/`
   - `bootstrap.min.css` → `src/renderer/assets/css/`
   - `bootstrap.bundle.min.js` → `src/renderer/assets/js/`

**Verify**: No CDN links in HTML files

---

### 2.5 Run Development Server

```powershell
# Start Electron in development mode
npm start

# Or with hot reload (if configured)
npm run dev
```

**Expected Behavior**:
- Electron window opens
- Login screen displays
- Default credentials: `admin` / `admin123`

---

## 3. Building for Production

### 3.1 Build Configuration

**electron-builder.json**:

Configuration for Windows x64 NSIS installer:
- App ID: `com.builderledger.app`
- Product Name: `Builder Ledger`
- Target: Windows x64 NSIS
- Installation directory: `C:\Program Files\Builder Ledger\`
- Data directory: `C:\ProgramData\BuilderLedger\`

---

### 3.2 Build Installer

```powershell
# Build Windows installer
npm run build

# Or with specific target
npm run build:win
```

**Output**:
- Installer: `dist/Builder Ledger Setup 1.1.0.exe`
- Unpacked files: `dist/win-unpacked/`

**Build Time**: ~2-5 minutes depending on machine

---

### 3.3 Test Installer

```powershell
# Navigate to dist folder
cd dist

# Run installer
.\Builder Ledger Setup 1.1.0.exe
```

**Installation Steps**:
1. Welcome screen → Next
2. Choose installation directory (default: `C:\Program Files\Builder Ledger`)
3. Select shortcuts (Desktop, Start Menu)
4. Install (requires admin rights)
5. Launch application

---

## 4. End-User Installation

### 4.1 Pre-Installation Checklist

- [ ] Windows 10/11 (64-bit)
- [ ] 500 MB free disk space
- [ ] Administrator rights available

---

### 4.2 Installation Steps

**Step 1: Download Installer**
- Obtain `Builder Ledger Setup 1.1.0.exe` from official source
- File size: ~150-200 MB

**Step 2: Run Installer**
- Right-click installer → "Run as administrator"
- If Windows SmartScreen appears: Click "More info" → "Run anyway"

**Step 3: Installation Wizard**

1. **Welcome Screen**: Click "Next"
2. **License Agreement**: Accept terms → "Next"
3. **Installation Directory**: 
   - Default: `C:\Program Files\Builder Ledger`
   - Change if needed → "Next"
4. **Shortcuts**: 
   - ✅ Create Desktop shortcut
   - ✅ Create Start Menu shortcut
   - Click "Next"
5. **Install**: Click "Install" (requires admin password if UAC enabled)
6. **Completion**: 
   - ✅ Launch Builder Ledger
   - Click "Finish"

---

### 4.3 First-Time Setup

**Step 1: Application Launch**
- Application opens to login screen
- Default credentials:
  - **Username**: `admin`
  - **Password**: `admin123`

**Step 2: Change Default Password** (CRITICAL)
1. Login with default credentials
2. Navigate to User Management
3. Edit admin user
4. Set strong password
5. Save changes

**Step 3: Create Users**
1. Navigate to User Management
2. Click "Add User"
3. Enter username, password, and role
4. Save

**Step 4: Create Master Data**
1. **Projects**: Add active construction projects
2. **Shops**: Add vendors/suppliers
3. **Categories**: Review and add custom expense categories if needed

---

### 4.4 File Locations

**Application Files**:
```
C:\Program Files\Builder Ledger\
├── Builder Ledger.exe
├── resources\
└── ...
```

**Application Data** (Shared across all Windows users):
```
C:\ProgramData\BuilderLedger\
├── data\
│   └── builder-ledger.db          # SQLite database
├── backups\
│   ├── builder-ledger_2026-01-15.db
│   └── ...
├── logs\
│   ├── app_2026-01-15.log
│   └── ...
└── attachments\
    └── {year}\{month}\{entry_id}\
```

---

## 5. Multi-User Setup

### 5.1 Shared Database Access

**How it works**:
- Single SQLite database shared by all Windows users on the machine
- Each user logs in with their own credentials
- Role-based access control enforced

**File Permissions** (set during installation):
```
C:\ProgramData\BuilderLedger\
├── data\                  # Read/Write for all users
├── backups\               # Read/Write for all users
├── logs\                  # Read/Write for all users
└── attachments\           # Read/Write for all users
```

---

### 5.2 Concurrent Access

**Supported**:
- Multiple users can access the application simultaneously
- SQLite WAL mode enables concurrent reads and writes

**Limitations**:
- Maximum ~10 concurrent users recommended
- Write operations are serialized (one at a time)

---

## 6. Uninstallation

### 6.1 Standard Uninstall

**Method 1: Control Panel**
1. Open Control Panel → Programs → Uninstall a program
2. Find "Builder Ledger"
3. Click "Uninstall"
4. Follow wizard

**Method 2: Settings App**
1. Open Settings → Apps → Installed apps
2. Find "Builder Ledger"
3. Click three dots → Uninstall

---

### 6.2 Complete Removal (Including Data)

**After uninstalling application**:

```powershell
# Remove application data (CAUTION: Deletes all data)
Remove-Item -Recurse -Force "C:\ProgramData\BuilderLedger"
```

**⚠️ WARNING**: This deletes all database, backups, logs, and attachments. **Backup first!**

---

## 7. Troubleshooting

### 7.1 Installation Issues

**Issue**: "Windows protected your PC" SmartScreen warning

**Solution**:
1. Click "More info"
2. Click "Run anyway"
3. Installer is not signed (expected for internal distribution)

---

**Issue**: "Access denied" during installation

**Solution**:
- Right-click installer → "Run as administrator"
- Ensure you have admin rights on the machine

---

**Issue**: Installation fails with "Error writing to directory"

**Solution**:
- Close any running instances of Builder Ledger
- Disable antivirus temporarily
- Retry installation

---

### 7.2 Runtime Issues

**Issue**: Application won't start / crashes on launch

**Solution**:
1. Check logs: `C:\ProgramData\BuilderLedger\logs\app_<date>.log`
2. Verify database exists: `C:\ProgramData\BuilderLedger\data\builder-ledger.db`
3. Reinstall application

---

**Issue**: "Database locked" error

**Solution**:
- Close all instances of Builder Ledger
- Check if another process is accessing the database
- Restart application

---

**Issue**: Login fails with correct credentials

**Solution**:
1. Verify database integrity using SQLite Browser
2. If corrupted, restore from backup
3. If no backup, reinitialize database (data loss)

---

**Issue**: Attachments not loading

**Solution**:
1. Verify attachments folder exists: `C:\ProgramData\BuilderLedger\attachments`
2. Check file permissions (all users should have read/write)
3. Check attachment paths in database

---

## 8. Backup & Recovery

### 8.1 Manual Backup

**Backup Database**:
```powershell
# Copy database file
Copy-Item "C:\ProgramData\BuilderLedger\data\builder-ledger.db" `
          "D:\Backups\builder-ledger_$(Get-Date -Format 'yyyy-MM-dd').db"
```

**Backup Attachments**:
```powershell
# Copy attachments folder
Copy-Item -Recurse "C:\ProgramData\BuilderLedger\attachments" `
                   "D:\Backups\attachments_$(Get-Date -Format 'yyyy-MM-dd')"
```

---

### 8.2 Restore from Backup

**Restore Database**:
1. Close Builder Ledger
2. Navigate to `C:\ProgramData\BuilderLedger\data\`
3. Rename `builder-ledger.db` to `builder-ledger.db.old`
4. Copy backup file to `builder-ledger.db`
5. Restart application

**Restore Attachments**:
1. Close Builder Ledger
2. Navigate to `C:\ProgramData\BuilderLedger\`
3. Rename `attachments` to `attachments.old`
4. Copy backup attachments folder
5. Restart application

---

### 8.3 Automatic Backup

**Configuration**:
- **Frequency**: Weekly (on app startup if last backup > 7 days)
- **Location**: `C:\ProgramData\BuilderLedger\backups\`
- **Retention**: Last 8 backups
- **Naming**: `builder-ledger_YYYY-MM-DDTHH-MM-SS.db`

**On-Demand Backup** (ADMIN only):
1. Login as ADMIN
2. Navigate to Backup History
3. Click "Backup Now"
4. Select destination folder
5. Backup created

---

## 9. Security Best Practices

### 9.1 Password Policy

**Recommendations**:
- Minimum 8 characters
- Mix of uppercase, lowercase, numbers, symbols
- Change default admin password immediately
- Unique passwords for each user

---

### 9.2 User Management

**Best Practices**:
- Create individual accounts (no shared credentials)
- Assign minimum required role (principle of least privilege)
- Deactivate users when they leave (don't delete for audit trail)
- Regularly review active users

---

### 9.3 Data Protection

**Recommendations**:
- Regular backups (weekly minimum)
- Store backups on separate drive/location
- Test restore procedure periodically

---

## 10. Maintenance Schedule

### 10.1 Daily
- Monitor application logs for errors
- Verify automatic backups are running

### 10.2 Weekly
- Review audit trail for suspicious activity
- Check database size and performance

### 10.3 Monthly
- Run database optimization (VACUUM, ANALYZE)
- Review and archive old backups
- Update application if new version available

### 10.4 Quarterly
- Test backup restore procedure
- Review user access and roles
- Clean up old log files (beyond 30-day retention)

---

## 11. Upgrade Procedure

### 11.1 Upgrade from Previous Version

**Pre-Upgrade**:
1. **Backup current database**:
   ```powershell
   Copy-Item "C:\ProgramData\BuilderLedger\data\builder-ledger.db" `
             "D:\Backups\pre-upgrade-backup.db"
   ```
2. **Note current version**: Help → About

**Upgrade Steps**:
1. Download new installer
2. Close Builder Ledger
3. Run new installer (will detect existing installation)
4. Choose "Upgrade" or "Overwrite"
5. Installer completes
6. Launch application
7. Verify data integrity

**Post-Upgrade**:
1. Login and verify all data is intact
2. Test critical workflows
3. Check version: Help → About

---

## 12. Developer Tools

### 12.1 Database Inspection

**Using SQLite CLI**:
```powershell
sqlite3 "C:\ProgramData\BuilderLedger\data\builder-ledger.db"

# List tables
.tables

# View schema
.schema ledger_entries

# Query data
SELECT * FROM ledger_entries WHERE project_id = 1;

# Exit
.quit
```

**Using DB Browser for SQLite** (GUI):
1. Download from [https://sqlitebrowser.org/](https://sqlitebrowser.org/)
2. Open database file
3. Browse tables, run queries, view schema

---

### 12.2 Viewing Logs

```powershell
# Navigate to logs directory
cd C:\ProgramData\BuilderLedger\logs

# View today's log
Get-Content "app_$(Get-Date -Format 'yyyy-MM-dd').log"

# Tail log (watch in real-time)
Get-Content "app_$(Get-Date -Format 'yyyy-MM-dd').log" -Wait
```

---

## 13. Appendix

### 13.1 Package.json Scripts

```json
{
  "scripts": {
    "start": "electron .",
    "dev": "electron . --dev",
    "build": "electron-builder",
    "build:win": "electron-builder --win --x64"
  }
}
```

---

### 13.2 Useful Commands

**Check SQLite Version**:
```powershell
sqlite3 --version
```

**Database Integrity Check**:
```powershell
sqlite3 "C:\ProgramData\BuilderLedger\data\builder-ledger.db" "PRAGMA integrity_check;"
```

**View Database Schema**:
```powershell
sqlite3 "C:\ProgramData\BuilderLedger\data\builder-ledger.db" ".schema"
```

---

**Document Status**: ✅ Production-Ready  
**Approved By**: [Pending]  
**Date**: 2026-01-15
