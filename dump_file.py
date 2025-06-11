import os

# --- Config ---
SOURCE_DIR = "."  # Root directory to scan
OUTPUT_FILE = "project_dump.txt"

# Folders to exclude (by name)
EXCLUDE_DIRS = {'.git', '__pycache__', 'venv', 'node_modules','api test', 'Designs'}

# Specific files to skip (by exact name)
EXCLUDE_FILES = {'secrets.py', '.env',}

# Skip if filename contains any of these substrings
EXCLUDE_PATTERNS = {'dump', 'log'}

# Allowed file extensions to include
ALLOWED_EXTENSIONS = {'.py', '.html', '.css', '.js', '.txt'}


def should_include(file):
    name = os.path.basename(file)
    if name in EXCLUDE_FILES:
        return False
    if any(pattern in name for pattern in EXCLUDE_PATTERNS):
        return False
    return os.path.splitext(file)[1] in ALLOWED_EXTENSIONS


with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
    for root, dirs, files in os.walk(SOURCE_DIR):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            if should_include(file):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        out.write(f"\n\n--- FILE: {path} ---\n")
                        out.write(content)
                except Exception as e:
                    print(f"Skipping {path}: {e}")

print(f"\n✅ Dump complete. Contents written to '{OUTPUT_FILE}'")
