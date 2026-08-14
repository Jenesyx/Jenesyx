# Jenesyx Terminal — Setup Guide

This template creates the green-black-blue terminal profile shown in this folder: a live contribution heatmap, self-typing ASCII portrait beside an animated ASCII name, and the original neofetch-style information card.

## Fastest setup

1. Create a public repository named exactly like your GitHub username.
2. Copy **the contents** of `Jenesyx` into it, excluding `.git` and `.venv` if they exist locally.
3. Edit the personal text in `scripts/make_info_card.py`, identity settings in `scripts/make_identity.py`, and contact links in `README.md`.
4. Replace `source-photo.jpg` and regenerate the portrait.
5. Push the repository and run **Update profile art** in GitHub Actions.

## Requirements

- A GitHub account
- Python 3.10 or newer
- Git, GitHub Desktop, or GitHub’s web uploader
- The included Python requirements files

No paid API or external stats-card service is required.

## 1. Create your profile repository

Create a **public** GitHub repository whose name exactly matches your username. GitHub displays its root `README.md` on your profile.

## 2. Copy the template

Copy the template files into the root of your profile repository:

```text
your-username/
├── .github/workflows/update-profile-art.yml
├── data/contributions.json
├── scripts/
├── avi-ascii.svg
├── contrib-heatmap.svg
├── identity.svg
├── info-card.svg
├── source-photo.jpg
├── source-prepped.png
├── whoami.svg
├── README.md
└── SETUP.md
```

Do **not** copy a nested `.git` folder or `.venv` environment. Make sure the hidden `.github` folder is copied.

## 3. Personalize the ASCII identity and information card

Open `scripts/make_identity.py` and edit the identity block near the top:

```python
WORDMARK = "ARTA"
USER = "arta"
HOST = "jenesyx"
```

The current generator contains the `A`, `R`, and `T` glyphs needed for `ARTA`. Add another glyph to `GLYPHS` before using a different letter.

Open `scripts/make_info_card.py` and edit only the section marked `EDIT ME`:

```python
USER = "your-terminal-name"
HOST = "your-github-username"
ROWS = [
    ("Now", "What you are currently building"),
    ("Stack", "Your main technologies"),
    ("Learning", "What you are learning"),
    ("Reach", "Your username and website"),
]
```

Keep values reasonably short; long text wraps and makes the card taller.

Regenerate the original right-side information card and the new identity image:

```bash
python scripts/make_info_card.py
python scripts/make_identity.py
```

## 4. Create your ASCII portrait

Replace `source-photo.jpg` with your portrait. A plain or removed background produces the best ASCII result.

### Basic method

Use this when your photo already has a simple background:

```bash
python -m pip install -r scripts/requirements-portrait-basic.txt
python scripts/prep_photo.py source-photo.jpg --no-rembg
python scripts/make_ascii_svg.py
python scripts/make_identity.py
```

### Automatic background-removal method

This installs larger machine-learning dependencies but can remove a complex background automatically:

```bash
python -m pip install -r scripts/requirements-portrait.txt
python scripts/prep_photo.py source-photo.jpg
python scripts/make_ascii_svg.py
python scripts/make_identity.py
```

If the portrait looks too bright, dark, or detailed, adjust `--clip`, `--gamma`, or the `--cols` value documented by the scripts, then regenerate it.

## 5. Update the README

In `README.md`:

- Replace `arta@github` in the terminal headings.
- Replace the website and social URLs.
- Replace badge labels and usernames.
- Remove contact buttons you do not need.

Do not rename `identity.svg`, `info-card.svg`, or `contrib-heatmap.svg` unless their paths are also updated in `README.md`.

## 6. Generate live contribution data locally

Install the lightweight daily dependencies:

```bash
python -m pip install -r scripts/requirements.txt
python scripts/fetch_contributions.py your-github-username
python scripts/render_heatmap_svg.py
```

This updates `data/contributions.json` and `contrib-heatmap.svg`. Internet access is required.

## 7. Preview the result

- Open `README.md` in VS Code and press `Ctrl+Shift+V`.
- Push the repository for the exact GitHub SVG rendering and animation behavior.

## 8. Enable automatic updates

Push the repository and open **Actions → Update profile art → Run workflow**. The workflow refreshes the contribution heatmap every day.

If the workflow cannot commit:

1. Open **Settings → Actions → General**.
2. Under **Workflow permissions**, select **Read and write permissions**.
3. Save and run the workflow again.

The portrait and information card change only when you regenerate and commit them; the daily workflow intentionally updates only contribution data.

## AI-assisted setup prompt

Place your source portrait in the repository, then copy this prompt into a coding assistant:

```text
Set up the Jenesyx Terminal GitHub profile template in this repository for me.

My details:
- GitHub username: [USERNAME]
- Terminal user name: [SHORT NAME]
- Full name: [NAME]
- Current work: [CURRENT WORK]
- Previous work: [PREVIOUS WORK]
- Technology stack: [STACK]
- Highlights: [HIGHLIGHTS]
- Currently learning: [LEARNING]
- Website and social links: [LINKS]
- Portrait image path: [PATH TO MY PHOTO]

Please inspect the existing repository and scripts first. Do not copy or modify nested .git or .venv folders. Update only the EDIT ME section in scripts/make_info_card.py, the identity settings in scripts/make_identity.py, and the personal headings, badges, and links in README.md. Prepare the portrait, generate avi-ascii.svg, identity.svg, and info-card.svg, fetch my live contribution data if internet access is available, render contrib-heatmap.svg, and validate all generated SVG files and local Markdown links. Preserve the green-black-blue terminal design, the animated ASCII name, and the original neofetch information panel. Keep the README order as contribution, ASCII identity, whoami information, then contact. Do not add a separate status --all panel. Verify that the workflow supports the default branch and is correctly placed. Do not change unrelated files, and do not commit or push unless I explicitly ask.
```

## Common problems

- **Portrait generation uses too much memory:** use the basic method with `--no-rembg`.
- **Portrait has a noisy background:** use a cut-out image or the full background-removal method.
- **The identity portrait is stale:** rerun `make_ascii_svg.py`, then `make_identity.py` last.
- **The ASCII name is wrong:** update `WORDMARK` and ensure every letter exists in `GLYPHS`.
- **Contribution data is wrong:** pass the exact username to `fetch_contributions.py` or run the Action in the correct profile repository.
