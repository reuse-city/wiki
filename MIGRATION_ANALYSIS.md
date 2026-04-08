# Migration Analysis: Wiki.js to Static Site Generator

Since you are the sole editor of this wiki and maintaining a full Docker VPS is unnecessary overhead, migrating to a Static Site Generator (SSG) hosted on GitHub Pages is an excellent idea.

The exported data in this repository is mostly standard Markdown with YAML front matter, which makes it highly compatible with modern SSGs. However, Wiki.js has certain specific conventions (e.g., absolute link paths, custom Markdown attributes) that need to be addressed during migration.

Here are the best alternatives to achieve an exact match for your structure and permalinks, along with the necessary considerations and potential downsides.

---

## 1. Alternatives for SSGs

### **A. Hugo** (Highly Recommended)
Hugo is a Go-based static site generator known for its incredible speed and flexibility.
- **Pros**:
  - **Permalinks**: Out of the box, Hugo handles URLs like `/solutions` perfectly (it generates `/solutions/index.html`).
  - **Images**: By moving your images into a `static/` directory (e.g., `static/reuse-city-logo-branco.png`), absolute image paths like `![logo](/reuse-city-logo-branco.png)` will resolve correctly.
  - **Markdown Attributes**: Hugo's Goldmark parser supports markdown attributes, so syntax like `{.align-right}` can be enabled to work natively.
  - **Ecosystem**: Easily deployed to GitHub Pages via GitHub Actions.
- **Cons**:
  - The templating language (Go templates) has a slight learning curve if you need to build a custom theme.

### **B. Eleventy (11ty)** (Great for JavaScript users)
Eleventy is a popular Node.js-based generator.
- **Pros**:
  - **Flexibility**: You can configure it to preserve your exact permalink structure very easily.
  - **Markdown**: It uses `markdown-it`, which is the same parser used by Wiki.js. You can install plugins (like `markdown-it-attrs`) to perfectly support `{.align-right}` and other Wiki.js extensions.
  - **Familiarity**: Since Wiki.js is JS-based, if you want to extend your site with scripts, you might feel more at home in Node.js.
- **Cons**:
  - Out of the box, it provides zero styling or structure—you have to build the layout and navigation yourself or find a starter template.

### **C. Jekyll** (The Classic GitHub Pages Option)
Jekyll is built in Ruby and has native, out-of-the-box support for GitHub Pages.
- **Pros**:
  - **Native GitHub Pages integration**: You don't even need a GitHub Action; just push the code.
  - **Front Matter**: Compatible with your existing YAML front matter.
- **Cons**:
  - **Markdown Attributes**: Jekyll uses Kramdown, which expects attributes in the format `{: .align-right}`. The Wiki.js format `{.align-right}` will render as plain text on the screen unless you pre-process the files or write a custom plugin.
  - Ruby environment can be frustrating to set up for local development on some operating systems.

### **D. MkDocs (Material for MkDocs)**
A Python-based SSG tailored specifically for wikis and documentation.
- **Pros**:
  - Looks and behaves like a wiki out of the box (especially with the `Material for MkDocs` theme).
  - Excellent built-in search.
- **Cons**:
  - **Internal Links**: MkDocs typically requires relative links ending in `.md` (e.g., `[Solutions](solutions.md)`). The absolute links in this repo (e.g., `[Solutions](/solutions)`) will likely break or require a plugin/script to convert them.

---

## 2. Considerations for the Migration

To preserve exactly the same structure, permalinks, and look, you must carefully handle the following aspects:

### **1. Absolute Links & Hosting Domain**
Your Markdown files use absolute paths for internal links and images:
- Internal Link: `[Solutions](/solutions)`
- Image: `![logo](/reuse-city-logo-branco.png)`

**Action Required**:
These absolute paths assume the website is hosted at the **root of a domain** (e.g., `https://wiki.reuse.city`). If you host the new site on a GitHub Pages subdirectory (e.g., `https://username.github.io/wiki/`), **all links and images will break**.
*Solution*: You must either configure a custom domain for your GitHub Pages, use a root-level User Page (`username.github.io`), or run a search-and-replace script to make all paths relative.

### **2. Directory Structure vs File Names**
In Wiki.js, creating a page at `/solutions/thingdata` usually means the path resolves without extensions.
SSGs handle this by turning files into folders. `solutions.md` becomes `solutions/index.html`.
Most SSGs (Hugo, Jekyll, Eleventy) do this natively, ensuring your permalinks remain completely unbroken.

### **3. Front Matter**
Your pages already have YAML front matter:
```yaml
title: Structure
description: Structure of this website
published: true
date: 2024-11-05T00:09:03.540Z
tags:
editor: markdown
dateCreated: 2023-07-07T10:10:34.988Z
```
SSGs will easily parse `title`, `date`, and `tags`. The `published: true` flag works perfectly in most SSGs. Properties like `editor` and `dateCreated` will simply be ignored unless you actively use them in your templates.

### **4. Search Functionality**
Wiki.js uses a backend database to perform searches. Since SSGs generate static HTML, you lose server-side search.
**Action Required**: You will need to implement client-side search. Tools like **Pagefind**, **Lunr.js**, or **Algolia** are standard solutions for SSGs and work remarkably well for wikis of this size.

---

## 3. Potential Downsides of Migration

1. **Loss of In-Browser WYSIWYG Editor**:
   You will have to edit Markdown files directly in your IDE or GitHub’s web interface. If you prefer a visual editor, you might want to look into setting up a headless CMS like **Decap CMS** (formerly Netlify CMS) on top of your Git repository.

2. **No Dynamic Features**:
   Features like user access control, commenting systems, or dynamic server-side rendering will no longer be available.

3. **Initial Setup Effort**:
   While the content is already in Markdown, porting the design/theme from Wiki.js to an SSG will require some HTML/CSS work. You will need to build the layout, navigation sidebar, and header manually, or adapt an existing SSG wiki theme.

4. **Image Management**:
   In Wiki.js, uploading an image handles placement and linking automatically. With an SSG, you will need to manually place the image file in the correct repository folder (e.g., `static/images/`) and write the correct Markdown path to it.

---

## Summary Recommendation

I recommend using **Hugo** or **Eleventy** for this migration.
- **Hugo** is easier if you want to find an existing Wiki theme (like `Hugo Book` or `Geekdoc`) and just drop your files in.
- **Eleventy** is ideal if you want to easily write a script to perfectly match Wiki.js's markdown parser (`markdown-it`) to handle your custom `{.align-right}` image tags without any changes to your content.

Whichever you choose, as long as you deploy to a custom domain (like `wiki.reuse.city`), your absolute permalinks will continue to function exactly as they did in Wiki.js.