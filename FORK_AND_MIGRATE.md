# Step-by-Step Guide: Migrating Wiki.js to Hugo on GitHub Pages

Since the current repository acts as an automatically synced backup from Wiki.js, directly restructuring it would break the syncing mechanism and effectively overwrite your backup.

To prevent this, the safest and best approach is to **fork** this repository (or copy it to a new one) and perform the migration there. This way, your original backup remains untouched, while the new repository becomes the source code for your static GitHub Pages site.

Follow these step-by-step instructions to perform the migration perfectly:

---

## 1. Create a Fork or Duplicate Repository
Do not edit the original backup repository.
1. On GitHub, click **Fork** at the top right of this repository to create a new repository (e.g., `reuse-city/wiki-hugo-site`).
2. Clone this new repository to your local computer:
   ```bash
   git clone https://github.com/YOUR_USERNAME/wiki-hugo-site.git
   cd wiki-hugo-site
   ```

## 2. Install Hugo
Make sure you install the **Extended** version of Hugo (required by most themes to compile SCSS).
- **macOS (Homebrew)**: `brew install hugo`
- **Windows (Scoop)**: `scoop install hugo-extended`
- **Linux (Debian/Ubuntu)**: `sudo apt install hugo` (Check the version, otherwise download the `.deb` from the [Hugo Releases page](https://github.com/gohugoio/hugo/releases)).

## 3. Configure Hugo and the Theme
At the root of the repository, run the following commands:
1. **Initialize a Hugo theme (e.g., Hugo Book)**:
   ```bash
   git submodule add https://github.com/alex-shpak/hugo-book themes/hugo-book
   ```
2. **Create a `hugo.toml` file**:
   Create a file named `hugo.toml` in the root folder and paste the following:
   ```toml
   baseURL = 'https://wiki.reuse.city/'  # Your custom domain or GitHub Pages URL
   languageCode = 'en-us'
   title = 'Reuse City Wiki'
   theme = 'hugo-book'

   [params]
     BookTheme = 'auto'
     BookToC = true
   ```

## 4. Reorganize Content for Permalinks
To ensure your existing absolute links like `[Solutions](/solutions)` continue working, you must move the content into Hugo's required `content/` folder and rename a few files so they act as "Branch Bundles".

Run these commands in your terminal (macOS/Linux):

1. **Create the content directory:**
   ```bash
   mkdir -p content
   ```
2. **Move directories into `content/`:**
   ```bash
   mv opendott/ content/
   mv solutions/ content/
   mv projects/ content/
   ```
3. **Move and rename root files into "indexes" (`_index.md`):**
   ```bash
   mv home.md content/_index.md
   mv opendott.md content/opendott/_index.md
   mv solutions.md content/solutions/_index.md
   mv projects.md content/projects/_index.md
   mv structure.md content/structure.md
   mv drafts/ content/
   ```

## 5. Reorganize Images
Your markdown uses absolute paths for images (e.g., `![logo](/reuse-city-logo-branco.png)`). In Hugo, files stored in the `static/` directory are copied to the root of the site.

1. **Create the static directory:**
   ```bash
   mkdir -p static
   ```
2. **Move root images and the `img/` folder to `static/`:**
   ```bash
   mv *.png *.jpg static/
   mv img/ static/
   ```
3. **Important: Move nested images to `static/` so their absolute paths still work:**
   Wiki.js links to images as `/opendott/images/...`. Move this directory inside `static/`:
   ```bash
   mkdir -p static/opendott
   mv content/opendott/images/ static/opendott/
   ```

## 6. Test Your New Site Locally
You can now start the Hugo development server to see how it looks:
```bash
hugo server -D
```
Open your browser to `http://localhost:1313`. Click around to ensure all images load and internal links are working.

> *Note on Links: If some internal links are relative, they might require minor tweaking, but absolute links starting with `/` will work perfectly.*

## 7. Set Up GitHub Pages Deployment
To automatically build and publish your site using GitHub Actions:

1. Create a directory for the workflow:
   ```bash
   mkdir -p .github/workflows
   ```
2. Create a file named `.github/workflows/hugo.yaml` with the following content:
   ```yaml
   name: Deploy Hugo site to Pages

   on:
     push:
       branches: [ main ]
     workflow_dispatch:

   permissions:
     contents: read
     pages: write
     id-token: write

   concurrency:
     group: "pages"
     cancel-in-progress: false

   jobs:
     build:
       runs-on: ubuntu-latest
       env:
         HUGO_VERSION: 0.125.4
       steps:
         - uses: actions/checkout@v4
           with:
             submodules: recursive
         - name: Install Hugo CLI
           run: |
             wget -O ${{ runner.temp }}/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb \
             && sudo dpkg -i ${{ runner.temp }}/hugo.deb
         - name: Build with Hugo
           run: hugo --minify
         - name: Upload artifact
           uses: actions/upload-pages-artifact@v3
           with:
             path: ./public

     deploy:
       environment:
         name: github-pages
         url: ${{ steps.deployment.outputs.page_url }}
       runs-on: ubuntu-latest
       needs: build
       steps:
         - name: Deploy to GitHub Pages
           id: deployment
           uses: actions/deploy-pages@v4
   ```

## 8. Commit and Push
Finally, commit all your changes and push them back to your new GitHub repository.
```bash
git add .
git commit -m "Migrate Wiki.js content to Hugo"
git push origin main
```

## 9. Enable GitHub Pages
1. Go to your repository settings on GitHub.
2. Click on **Pages** in the left sidebar.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. GitHub Actions will now automatically build and publish your site to your GitHub Pages domain. Ensure you configure your custom domain (`wiki.reuse.city`) in the settings if you plan to use it!