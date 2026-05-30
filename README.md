# Pantelis Loupos Academic Website

This repository contains the Quarto source for the academic website at `www.loupos.org`. It is designed as a clean, static faculty website for GitHub Pages.

## Edit the Site

Main pages:

- `index.qmd` - home page
- `research.qmd` - research themes
- `publications.qmd` - publications and working papers
- `teaching.qmd` - courses
- `cv.qmd` - academic journey and CV link
- `contact.qmd` - contact and profile links

Shared configuration lives in `_quarto.yml`; custom styling lives in `styles.css`.

## Assets

- Profile and site images: `assets/img/`
- CV and paper PDFs: `assets/pdf/`
- Other downloadable files: `assets/files/`

The current CV PDF is stored at `assets/pdf/Loupos_CV.pdf` and linked from `cv.qmd`.

## Preview Locally

Install Quarto first:

```bash
# https://quarto.org/docs/get-started/
```

Preview the site:

```bash
quarto preview
```

Render the static site:

```bash
quarto render
```

The rendered website is written to `_site/`.

## Deploy to GitHub Pages

This repository includes `.github/workflows/publish.yml`, which uses the standard GitHub Pages artifact flow:

1. Check out the repository.
2. Install Quarto.
3. Configure GitHub Pages.
4. Render the Quarto site.
5. Upload `_site/` as the Pages artifact.
6. Deploy the artifact to GitHub Pages.

The rendered output directory is `_site/`, configured in `_quarto.yml`:

```yaml
project:
  type: website
  output-dir: _site
```

The workflow uploads that same directory:

```yaml
with:
  path: _site
```

## Custom Domain Setup

The repository includes a `CNAME` file with exactly:

```text
www.loupos.org
```

Because `_quarto.yml` includes `CNAME` under `resources`, Quarto copies this file into the published `_site/` output. GitHub Pages should use `www.loupos.org` as the custom domain. The root/apex domain `loupos.org` should also be configured in DNS so GitHub Pages can serve or redirect it to the `www` domain when GitHub supports that behavior for the repository.

The canonical site URL in `_quarto.yml` is:

```yaml
website:
  site-url: "https://www.loupos.org"
```

In GitHub, open **Settings -> Pages** and set:

- **Source:** GitHub Actions
- **Custom domain:** `www.loupos.org`
- **Enforce HTTPS:** enabled after GitHub makes the option available

## GitHub Pages Site Type

This site is intended to be published as a GitHub user site:

- Repository: `ploupos3.github.io`
- Default Pages URL: `https://ploupos3.github.io`

If you publish this source under any other repository name, it becomes a project site with default URL `https://ploupos3.github.io/<repo>`.

For DNS, the `www` CNAME should point to:

```text
ploupos3.github.io
```

Do not include a repository name in the DNS CNAME value.

## Wix DNS Records

For Wix DNS, preserve all existing MX, TXT, SPF, DKIM, and DMARC records used for Google Workspace email. Only replace website records.

For the apex/root domain `loupos.org`, add GitHub Pages `A` records:

```text
Type: A
Name: @
Value: 185.199.108.153

Type: A
Name: @
Value: 185.199.109.153

Type: A
Name: @
Value: 185.199.110.153

Type: A
Name: @
Value: 185.199.111.153
```

For `www.loupos.org`, add a CNAME record:

```text
Type: CNAME
Name: www
Value: ploupos3.github.io
```

Optional IPv6 records for the apex/root domain:

```text
Type: AAAA
Name: @
Value: 2606:50c0:8000::153

Type: AAAA
Name: @
Value: 2606:50c0:8001::153

Type: AAAA
Name: @
Value: 2606:50c0:8002::153

Type: AAAA
Name: @
Value: 2606:50c0:8003::153
```

Some DNS providers support `ALIAS`, `ANAME`, or CNAME flattening for apex domains. Those can point `loupos.org` to `ploupos3.github.io` instead of using `A` records, if the provider supports it.

## Commit and Push

If this folder has not been initialized as a git repository yet:

```bash
git init
git add .
git commit -m "Build Quarto academic website"
git branch -M main
git remote add origin https://github.com/ploupos3/ploupos3.github.io.git
git push -u origin main
```

If the repository already exists locally:

```bash
git add .
git commit -m "Prepare GitHub Pages custom domain"
git push
```

## Sources Used

- Local `Loupos_Resume.pdf` is the source of record for current appointments, paper statuses, teaching, service, and research interests.
- Current Wix website at `https://www.loupos.org/` was used for existing page structure and older publication/media links.
- GitHub Pages DNS guidance follows GitHub's documentation for custom domains.
