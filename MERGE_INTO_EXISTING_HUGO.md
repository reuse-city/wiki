# Guide: Merging Wiki into an Existing Hugo Site

To merge the contents of this repository into your existing `reuse.city` Hugo website, **you still need to edit the exported markdown files one last time.**

Why? Because your original Wiki.js files use **absolute paths** for internal links and images (e.g., `[Solutions](/solutions)` and `![](/opendott/images/picture.png)`).
If you simply drop these files into `https://reuse.city/wiki`, an absolute link like `/solutions` will resolve to the root (`https://reuse.city/solutions`) instead of the correct path (`https://reuse.city/wiki/solutions`). Every single internal link and image will be broken. Furthermore, Wiki.js outputs YAML frontmatter and markdown tags that are invalid in standard Hugo.

To automate this, I have created two python scripts: `cleanup_frontmatter.py` and `fix_subdirectory_links.py`.

Here is exactly how to safely execute your new architecture using these scripts:

---

## Part 1: Clean and Fix the Markdown Files

1. **Run the Cleanup script** in your wiki fork/directory where your markdown files are currently sitting:
   ```bash
   python3 cleanup_frontmatter.py
   ```
   *What this does: Safely translates `published: true` to `draft: false`, double-quotes unquoted colons in `title:` fields to prevent YAML parsing crashes, and strips unsupported `{.align-right}` tags so they don't render as plain text.*

2. **Run the Path Fixer script**:
   ```bash
   python3 fix_subdirectory_links.py
   ```
   *What this does: Safely rewrites every absolute markdown link and HTML `src=`/`href=` attribute in your files to prepend `/wiki/`.*

## Part 2: Merge the Content to your Main Website

Assuming your main website repository is located at `../reuse.city-hugo`:

1. Copy the wiki markdown folders and files into a `wiki/` folder in your main site's `content/` directory:
   ```bash
   mkdir -p ../reuse.city-hugo/content/wiki
   cp -r opendott/ solutions/ projects/ drafts/ ../reuse.city-hugo/content/wiki/

   # Copy the root markdown files
   cp *.md ../reuse.city-hugo/content/wiki/

   # Remove the markdown files you don't need published
   rm ../reuse.city-hugo/content/wiki/README.md
   rm ../reuse.city-hugo/content/wiki/MERGE_INTO_EXISTING_HUGO.md
   rm ../reuse.city-hugo/content/wiki/MIGRATION_ANALYSIS.md
   ```

2. Copy the images into a `wiki/` folder in your main site's `static/` directory:
   ```bash
   mkdir -p ../reuse.city-hugo/static/wiki
   cp -r img/ ../reuse.city-hugo/static/wiki/

   # Copy root images
   cp *.png *.jpg ../reuse.city-hugo/static/wiki/

   # Copy any nested images
   mkdir -p ../reuse.city-hugo/static/wiki/opendott
   cp -r opendott/images ../reuse.city-hugo/static/wiki/opendott/
   ```

3. **Rename the Index Files**
   In Hugo, directories are served using `_index.md`. You must rename your root pages so Hugo builds them correctly:
   ```bash
   mv ../reuse.city-hugo/content/wiki/home.md ../reuse.city-hugo/content/wiki/_index.md
   mv ../reuse.city-hugo/content/wiki/opendott.md ../reuse.city-hugo/content/wiki/opendott/_index.md
   mv ../reuse.city-hugo/content/wiki/solutions.md ../reuse.city-hugo/content/wiki/solutions/_index.md
   mv ../reuse.city-hugo/content/wiki/projects.md ../reuse.city-hugo/content/wiki/projects/_index.md
   ```

4. **Deploy**
   Commit the new files to your `reuse.city` repository and push to deploy your site.

---

## Part 3: Setting up NGINX 301 Redirects

Now that your wiki is hosted at `https://reuse.city/wiki`, you need to handle your old domain: `wiki.reuse.city`.

You must set up a `301 Moved Permanently` redirect. This tells search engines (Google) to transfer your SEO rankings to the new domain, and ensures any old links shared on social media or in emails don't break.

Since you mentioned having a VPS with NGINX, here is the exact server block you should use.

1. Create a new NGINX config file (e.g., `/etc/nginx/sites-available/wiki.reuse.city.conf`):

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name wiki.reuse.city;

    # Optional: If you use Let's Encrypt for HTTPS, uncomment these lines and configure them
    # listen 443 ssl http2;
    # listen [::]:443 ssl http2;
    # ssl_certificate /etc/letsencrypt/live/wiki.reuse.city/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/wiki.reuse.city/privkey.pem;

    # 301 Redirect matching the exact URI path
    # e.g. wiki.reuse.city/solutions -> reuse.city/wiki/solutions
    return 301 https://reuse.city/wiki$request_uri;
}
```

2. Enable the configuration and test:
```bash
sudo ln -s /etc/nginx/sites-available/wiki.reuse.city.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Alternative: Cloudflare Page Rules
If your DNS for `reuse.city` is managed through Cloudflare, you don't even need the VPS.
1. In Cloudflare, ensure an `A` or `CNAME` record exists for `wiki` pointing anywhere (proxied/orange cloud).
2. Go to **Rules > Page Rules** and create a rule:
   - URL matches: `wiki.reuse.city/*`
   - Setting: **Forwarding URL**
   - Status Code: **301 - Permanent Redirect**
   - Destination URL: `https://reuse.city/wiki/$1`