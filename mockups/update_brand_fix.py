import os
import glob

MOCKUPS_DIR = r"c:\Users\senth\OneDrive\Documents\GitHub\builder-ledger\mockups"

old_brand = r'<img src="assets/images/logo.png" alt="Dream Builders Logo" height="30" class="d-inline-block align-text-top me-2 bg-white rounded p-1"> Dream Builders, Thiruvarur'
new_brand = r'<img src="assets/img/dream builders.png" alt="Dream Builders Logo" height="30" class="d-inline-block align-text-top me-2 bg-white rounded p-1"> 🏗️ Builder Ledger - Dream Builders, Thiruvarur'

html_files = glob.glob(os.path.join(MOCKUPS_DIR, "*.html"))
count = 0

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if old_brand in content:
        content = content.replace(old_brand, new_brand)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1

print(f"Fixed {count} HTML files.")
