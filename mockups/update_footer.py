import os
import glob
import re

MOCKUPS_DIR = r"c:\Users\senth\OneDrive\Documents\GitHub\builder-ledger\mockups"

new_footer = """<!-- Global Footer -->
    <footer class="mt-auto py-3 text-center text-muted small" style="background-color: #f8f9fa; border-top: 1px solid #dee2e6; width: 100%;">
        <div class="container d-flex flex-column align-items-center">
            <div class="mb-1 d-flex align-items-center justify-content-center flex-wrap">
                <span class="me-2 mb-1">&copy; 2026 Dream Builders, Thiruvarur. Software by</span>
                <img src="assets/img/Dheeran OneClick Logo.png" alt="Dheeran OneClick Logo" height="26" class="d-inline-block align-middle mb-1">
            </div>
            <p class="mb-0 fst-italic text-secondary" style="font-size: 0.85rem;">"Think Simple, Use Simple"</p>
        </div>
    </footer>"""

html_files = glob.glob(os.path.join(MOCKUPS_DIR, "*.html"))
count = 0

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Use regex to replace the existing Global Footer block
    pattern = r"<!-- Global Footer -->.*?</footer>"
    if re.search(pattern, content, flags=re.DOTALL):
        new_content = re.sub(pattern, new_footer, content, flags=re.DOTALL)
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1

print(f"Updated footer in {count} HTML files.")
