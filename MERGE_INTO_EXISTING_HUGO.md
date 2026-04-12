# Guide: Merging Wiki into an Existing Hugo Site

You asked if there's no need to edit files since you already ran `cleanup_frontmatter.py`. The answer is: **you still need to edit the files one last time.**

Why? Because your original Wiki.js files use **absolute paths** for internal links and images (e.g., `[Solutions](/solutions)` and `![](/opendott/images/picture.png)`).
If you simply drop these files into `https://reuse.city/wiki`, an absolute link like `/solutions` will resolve to the root (`https://reuse.city/solutions`) instead of the correct path (`https://reuse.city/wiki/solutions`). Every single internal link and image will be broken.

To fix this, I have created a new python script: `fix_subdirectory_links.py`.

Here is exactly how to execute your new architecture:

---

## Part 1: Fix the Links and Merge the Content

1. **Run the new script** in your wiki fork/directory where your markdown files are currently sitting:
   ```bash
   python3 fix_subdirectory_links.py
   ```
   This will safely rewrite every absolute markdown link and HTML `src=` attribute in your files to prepend `/wiki/`.

2. **Move the content to your main website:**
   Assuming your main website repository is located at `../reuse.city-hugo`, copy the contents over:

   Move the wiki markdown pages into a `wiki/` folder in your main site's `content/` directory:
   ```bash
   cp -r content/* ../reuse.city-hugo/content/wiki/
   ```

   Move the images into a `wiki/` folder in your main site's `static/` directory:
   ```bash
   cp -r static/* ../reuse.city-hugo/static/wiki/
   ```

3. **Check the Home Page**
   Because you moved the wiki to a sub-folder, the wiki's homepage (which used to be `content/_index.md`) is now located at `content/wiki/_index.md`.
   Hugo will automatically build this at `https://reuse.city/wiki/`.

4. **Deploy**
   Commit the new files to your `reuse.city` repository and push to deploy your site.

---

## Part 2: Setting up NGINX 301 Redirects

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