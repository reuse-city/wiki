#!/usr/bin/env python3
import os
import re

def process_frontmatter(content):
    # Check if file has frontmatter
    if not content.startswith('---'):
        return content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return content

    frontmatter = parts[1]

    # Fix the published flag which Hugo parses incorrectly as a date
    # In Wiki.js `published: true` means it's published.
    # In Hugo, we need `draft: false` to mean it's published.
    if 'published: true' in frontmatter:
        frontmatter = frontmatter.replace('published: true', 'draft: false')
    elif 'published: false' in frontmatter:
        frontmatter = frontmatter.replace('published: false', 'draft: true')

    # Fix unquoted titles and descriptions containing a colon (which breaks YAML parsers)
    # This regex looks for `title: Some text: more text` or `description:`
    # and wraps the value in double quotes to prevent Hugo build errors.
    def quote_field(match):
        field_name = match.group(1)
        field_val = match.group(2).strip()
        # If it's already quoted, leave it alone
        if field_val.startswith('"') and field_val.endswith('"'):
            return f"{field_name}: {field_val}"
        if field_val.startswith("'") and field_val.endswith("'"):
            return f"{field_name}: {field_val}"
        # Only quote if it contains a colon
        if ':' in field_val:
            # Escape existing double quotes
            field_val = field_val.replace('"', '\\"')
            return f'{field_name}: "{field_val}"'
        return match.group(0)

    frontmatter = re.sub(r'^(title|description):\s*(.+)$', quote_field, frontmatter, flags=re.MULTILINE)

    # Reassemble
    content_body = parts[2]

    # Fix Wiki.js image alignment attributes e.g. {.align-right} or {.align-center}
    # These are not natively supported by standard markdown/Hugo without custom CSS
    # so it's safest to simply strip them to prevent them rendering as text.
    content_body = re.sub(r'\{\.align-[^}]+\}', '', content_body)

    return f"---{frontmatter}---{content_body}"

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # We want to process the content directory (where the user moved the files)
    # But since we are providing this for the user to run *after* they move files,
    # let's just process all .md files we can find in content/ or current dir.

    target_dir = os.path.join(root_dir, 'content')
    if not os.path.exists(target_dir):
        # Fallback to processing all md files in root and subdirs
        # (useful for testing before the structure is moved)
        target_dir = root_dir

    count = 0
    for dirpath, _, filenames in os.walk(target_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                filepath = os.path.join(dirpath, filename)

                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                new_content = process_frontmatter(content)

                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed frontmatter in: {filepath}")
                    count += 1

    print(f"\nCleanup complete. Fixed {count} files.")

if __name__ == "__main__":
    main()
