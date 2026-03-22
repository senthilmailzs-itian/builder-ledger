import os
import glob

MOCKUPS_DIR = r"c:\Users\senth\OneDrive\Documents\GitHub\builder-ledger\mockups"

new_brand = r'<img src="assets/images/logo.png" alt="Dream Builders Logo" height="30" class="d-inline-block align-text-top me-2 bg-white rounded p-1"> Dream Builders, Thiruvarur'

footer_html = """
    <!-- Global Footer -->
    <footer class="mt-auto py-4 text-center text-muted small" style="background-color: #f8f9fa; border-top: 1px solid #dee2e6; width: 100%;">
        <div class="container">
            <p class="mb-1">&copy; 2026 Dream Builders, Thiruvarur. Software by <strong>Dheeran OneClick</strong>.</p>
            <p class="mb-0 fst-italic">Think Simple, Use Simple</p>
        </div>
    </footer>
"""

html_files = glob.glob(os.path.join(MOCKUPS_DIR, "*.html"))
count = 0

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    # Replace navbar and titles
    content = content.replace("🏗️ Builder Ledger", new_brand)
    
    # Inject footer right before bootstrap JS.
    if "Global Footer" not in content and '<script src="assets/bootstrap/js/bootstrap.bundle.min.js"></script>' in content:
        content = content.replace('<script src="assets/bootstrap/js/bootstrap.bundle.min.js"></script>', 
                                  footer_html + '\n    <script src="assets/bootstrap/js/bootstrap.bundle.min.js"></script>')

    # Write back if changed
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1

print(f"Updated {count} HTML files.")
