# OpenGeo Documentation - Quick Reference

## 🌐 Live Site

**URL**: <https://pulakeshpradhan.github.io/opengeo/>

## 📁 Project Structure

```
OpenGeo/
├── docs/                           # Documentation source
│   ├── assets/                     # Images, CSS, icons
│   │   ├── logo.png               # OpenGeo logo
│   │   ├── favicon.ico            # Browser icon
│   │   └── extra.css              # Custom styling
│   ├── examples/                   # Jupyter notebooks
│   │   ├── intro.md               # Examples overview
│   │   └── *.ipynb                # Example notebooks
│   ├── api/                        # API reference
│   │   ├── index.md               # API overview
│   │   ├── image.md               # og.Image docs
│   │   ├── image_collection.md    # og.ImageCollection docs
│   │   ├── feature_collection.md  # og.FeatureCollection docs
│   │   ├── geometry.md            # og.Geometry docs
│   │   └── map.md                 # og.Map docs
│   ├── index.md                    # Home page
│   ├── installation.md             # Installation guide
│   └── usage.md                    # Usage guide
├── .github/workflows/
│   └── docs.yml                    # Auto-deploy workflow
├── mkdocs.yml                      # MkDocs configuration
└── create_logo.py                  # Logo generation script
```

## 🎨 Theme Configuration

### Colors

- **Primary**: Teal (#009688)
- **Accent**: Teal (#009688)
- **Scheme**: Light/Dark mode support

### Features Enabled

- ✅ Navigation tabs
- ✅ Navigation sections
- ✅ Navigation footer
- ✅ Search with suggestions
- ✅ Code copy buttons
- ✅ Content tabs
- ✅ TOC integration

## 📝 Adding New Content

### Add a New Page

1. Create a `.md` file in `docs/`
2. Add to `nav` section in `mkdocs.yml`:

   ```yaml
   nav:
     - New Page: new_page.md
   ```

### Add a New Example Notebook

1. Place `.ipynb` file in `docs/examples/`
2. Add to navigation in `mkdocs.yml`:

   ```yaml
   - Examples:
       - New Example: examples/new_example.ipynb
   ```

3. Add download link in `docs/examples/intro.md`:

   ```markdown
   *   **[New Example](new_example.ipynb)** [:material-download:](https://raw.githubusercontent.com/pulakeshpradhan/opengeo/main/docs/examples/new_example.ipynb){:download}
   ```

### Add API Documentation

1. Create `.md` file in `docs/api/`
2. Use mkdocstrings syntax:

   ```markdown
   # Module Name
   
   ::: opengeo.module.ClassName
   ```

## 🔧 Local Development

### Build Documentation Locally

```bash
mkdocs build
```

### Serve Documentation Locally

```bash
mkdocs serve
```

Then visit: <http://127.0.0.1:8000>

### Clean Build

```bash
mkdocs build --clean
```

## 🚀 Deployment

### Automatic Deployment

- Pushes to `main` branch trigger GitHub Actions
- Site automatically builds and deploys to GitHub Pages
- Workflow file: `.github/workflows/docs.yml`

### Manual Deployment

```bash
mkdocs gh-deploy --force
```

## 📦 Dependencies

### MkDocs Plugins

- `mkdocs-material` - Material theme
- `mkdocstrings[python]` - API documentation
- `mkdocs-jupyter` - Jupyter notebook support
- `mkdocs-git-revision-date-localized-plugin` - Last updated dates
- `mkdocs-minify-plugin` - HTML/CSS/JS minification

### Python Packages

See `requirements.txt` for full list

## 🎯 Key Features

### 1. Downloadable Notebooks

All notebooks have download links:

```markdown
[:material-download:](URL){:download}
```

### 2. Code Copy Buttons

Enabled via Material theme feature:

```yaml
features:
  - content.code.copy
```

### 3. Tabbed Content

Use for platform-specific instructions:

```markdown
=== "Windows"
    ```powershell
    command
    ```

=== "macOS/Linux"
    ```bash
    command
    ```
```

### 4. Admonitions

For tips, warnings, info:

```markdown
!!! tip "Title"
    Content here

!!! warning "Title"
    Content here

!!! info "Title"
    Content here
```

### 5. Custom Styling

Edit `docs/assets/extra.css` for custom styles

## 🔍 Troubleshooting

### Build Fails

- Check Python version (use 3.11)
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Clear cache: `mkdocs build --clean`

### Notebooks Not Rendering

- Ensure `mkdocs-jupyter` is installed
- Check notebook is in `docs/examples/`
- Verify notebook is in navigation

### Logo Not Showing

- Check file exists: `docs/assets/logo.png`
- Verify path in `mkdocs.yml`: `logo: assets/logo.png`

## 📊 Analytics (Optional)

To add Google Analytics, add to `mkdocs.yml`:

```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

## 🔗 Useful Links

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [mkdocstrings](https://mkdocstrings.github.io/)
- [mkdocs-jupyter](https://github.com/danielfrg/mkdocs-jupyter)

## 📄 License

Documentation is part of OpenGeo project under MIT License.
