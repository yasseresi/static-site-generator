# Static Site Generator

A Python-based static site generator that converts Markdown content to HTML and serves it as a static website.

## 🚀 GitHub Pages Deployment

This site is automatically deployed to GitHub Pages using GitHub Actions. The workflow builds the static site and deploys it to the `docs/` directory.

### Live Site
Visit the live site at: https://yasseresi.github.io/static-site-generator/

## 🏗️ Local Development

### Prerequisites
- Python 3.11 or higher

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yasseresi/static-site-generator.git
   cd static-site-generator
   ```

2. Generate the static site:
   ```bash
   python3 src/main.py
   ```

3. The generated site will be in the `docs/` directory.

### Project Structure
```
├── content/          # Markdown content files
├── static/           # Static assets (CSS, images)
├── src/              # Python source code
├── docs/             # Generated static site (GitHub Pages serves from here)
├── template.html     # HTML template
└── .github/workflows/deploy.yml  # GitHub Actions workflow
```

### Running Tests
```bash
python3 -m unittest discover src/
```

## 📁 Content Management

- Add new pages by creating `.md` files in the `content/` directory
- Static assets go in the `static/` directory
- The site structure mirrors the `content/` directory structure

## 🔧 Build Scripts

- `build.sh` - Builds the static site
- `main.sh` - Builds and serves locally
- `test.sh` - Runs tests

## 🌐 Deployment

The site is automatically deployed to GitHub Pages when you push to the main branch. The GitHub Actions workflow:

1. Checks out the code
2. Sets up Python
3. Runs `python3 src/main.py` to generate the site
4. Deploys the `docs/` directory to GitHub Pages

No manual deployment needed!
