# Xi Cao — Honors & Achievements

V1.0 preview (`1.0.0-preview.1`) · prepared 2 November 2026.

This folder is the complete static website. Upload **the contents of this folder**, including `.nojekyll`, to the repository root. Preparation does not publish anything.

## Structure

```text
index.html                  Entry page and unchanged page layout
assets/css/site.css         Approved navy / ivory styling
assets/js/content.js        Public award, project and research data; image map
assets/js/site.js           Rendering, filters, search, dialogs and subtle motion
assets/images/              Project figures and conceptual hero artwork
assets/evidence/            Certificate and acceptance-letter display images
assets/favicon.svg          Small browser-tab icon
ASSET_MANIFEST.json         Image dimensions, sizes and checksums
VERSION                     Preview version
scripts/validate_site.py    Optional local verification (Python standard library)
.nojekyll                   Serve this as ordinary static files
```

## Dependencies and local review

No React, Vite, npm packages, build command, server application, API keys or database are required. A modern browser runs the site. CSS, JavaScript and images use document-relative paths, supporting a GitHub project URL under a repository subdirectory.

For local review, run from this folder:

```sh
python3 scripts/validate_site.py
python3 -m http.server 8000
```

Then open `http://localhost:8000`. The entry page can also be opened locally; the HTTP preview is preferred for checking deployed-path behavior.

## Recommended GitHub Pages setup

1. Place this folder's contents in the repository's `main` branch, with `index.html` at the root.
2. In the repository, open **Settings → Pages**.
3. Choose **Deploy from a branch**, then `main` and `/(root)`.
4. Save when you are ready to publish, and use the URL GitHub returns.

No custom Actions workflow, domain configuration or framework build is needed for this preview. These are instructions for a later deployment; no repository, commit, push or publication was performed during preparation.

Reference: [GitHub's publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Fonts and public content

The approved system-font stack is retained: Bodoni 72 / Didot where installed, then Georgia / Times New Roman; Arial / Helvetica for sans-serif text. No licensed font binaries are redistributed, and no external font service is required. Exact serif rendering can vary by device.

The 14 recognition records, 15 award-certificate images, two research records and their letter images are retained. Research is counted separately. The hero is explicitly conceptual artwork.

Evidence is supplied as flattened public PNG display copies under `assets/evidence/public/`. Private email addresses, team/adviser names in documents, class/cohort details and document identifiers have been masked where applicable. Award wording and results are preserved; every copy is labelled. Original documents are not included. Public scholarly authorship credits and the owner's chosen footer contact address remain visible.

The three SenviX project images are omitted pending provenance and publication-permission confirmation. Conference status is limited to acceptance supported by the supplied letter; no abstract-inclusion, full-paper-publication or database-indexing claim is made. MathorCup 2025 is shown as Regional Third Prize, matching its certificate.

The deployment folder excludes private experience documents, CV files, raw document archives, original full-resolution evidence PDFs, internal audits, historical comparisons and machine-specific source metadata. Do not copy sibling handoff folders into this repository.

## Editing later

Edit display content and the asset map in `assets/js/content.js`; styling in `site.css`; interactions in `site.js`. Keep filenames and letter case exact. Run the validator after changes. Shared projects remain linked by `projectId`, and all totals are calculated from the records.

The conference abstract-source link may time out and does not establish inclusion. Its redacted local acceptance-letter viewer remains available. Acceptance does not establish full-paper publication or database indexing.
