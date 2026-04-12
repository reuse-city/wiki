#!/usr/bin/env python3
import os
import re

def process_links(content):
    # This script assumes you are moving everything to the /wiki/ subdirectory.
    # Therefore, absolute links like [Solutions](/solutions) must become [Solutions](/wiki/solutions)
    # and absolute images like ![](/opendott/images/a.png) must become ![](/wiki/opendott/images/a.png)

    # 1. Fix Markdown Image links: ![](/path) -> ![](/wiki/path)
    content = re.sub(r'!\[([^\]]*)\]\(/([^\)]+)\)', r'![\1](/wiki/\2)', content)

    # 2. Fix Markdown standard links: [](/path) -> [](/wiki/path)
    content = re.sub(r'(?<!!)\[([^\]]+)\]\(/([^\)]+)\)', r'[\1](/wiki/\2)', content)

    # 3. Fix raw HTML src attributes (images, videos, etc): src="/path" -> src="/wiki/path"
    content = re.sub(r'src=["\']/([^"\']+)["\']', r'src="/wiki/\1"', content)

    # 4. Fix raw HTML href attributes: href="/path" -> href="/wiki/path"
    content = re.sub(r'href=["\']/([^"\']+)["\']', r'href="/wiki/\1"', content)

    return content

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Search for files in content/ directory
    target_dir = os.path.join(root_dir, 'content')
    if not os.path.exists(target_dir):
        # Fallback to current directory for testing
        target_dir = root_dir

    count = 0
    for dirpath, _, filenames in os.walk(target_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                filepath = os.path.join(dirpath, filename)

                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                new_content = process_links(content)

                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed links in: {filepath}")
                    count += 1

    print(f"\nLink processing complete. Updated {count} files.")

if __name__ == "__main__":
    main()