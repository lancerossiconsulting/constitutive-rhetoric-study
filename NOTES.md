# NOTES — Constitutive Rhetoric Study (build cache, do not re-fetch)

## Generator decision
- Pratt-study uses **Jekyll**, classic GitHub Pages branch deploy from `main` (root). Mirror it.
- No local Ruby available; rely on GitHub Pages server-side Jekyll build. Verify routing post-deploy via curl against live site.
- Repo: `lancerossiconsulting/constitutive-rhetoric-study`. Live base: `https://lancerossiconsulting.github.io/constitutive-rhetoric-study/`. `baseurl: /constitutive-rhetoric-study`.

## Pratt architecture (mirror)
- Wordmark: "Pratt Study" → ours "Constitutive Rhetoric Study".
- Slim 6-item nav: Home / Journal Article / Conference Paper / Substack / Literature Review / About. Rest surfaced via home cards.
- Home: H1 + tagline, intro paragraph, card grid, "About this project" note.
- Cards set: Journal Article, Conference Paper, Substack, Practice Brief, Literature Review, Podcast Outline, Infographics, Downloads.
- Footer: "© 2026 Lance Rossi" + GitHub | RSS | Contact (mailto) | Downloads. Working-draft note: "All writing on this site is the author's working draft and subject to revision."
- Lit review header line: "Annotated bibliography · N sources · Updated <date>"; grouped sections; each entry = citation + link + **bold one-line use note**; ordered by argument not alphabetical.
- Per-page head meta: canonical, description, og:title/description/url/type/site_name, viewport. og:type=article for content, website for home.
- Routing: permalink pretty → trailing-slash dirs (/literature-review/). feed.xml at root, 404.html, /downloads/ reserved.
- Skip link `#main` for a11y.

## Subject (authoritative, from project + M2 briefs)
Charland's *Constitutive Rhetoric: The Case of the Peuple Québécois* (QJS 1987) across three cases: Québec sovereignty, Alberta 2026 referendum (Oct 19 2026), US "true America"/No Kings framing.
Theory is the lens; **do not name CET on the page.**

### Verification gate (ROS-168) — load-bearing facts to source
- Alberta referendum Oct 19 2026 + 37-word question; "Alberta Sovereignty within a United Canada".
- May 13 2026 King's Bench duty-to-consult ruling.
- Numbered Treaties 6/7/8 predate the 1905 province.
- Québec 1980 + 1995 referendums; 1995 James Bay Cree counter-vote; 1998 SCC Secession Reference.
- US No Kings / 3.5% (Chenoweth) framing.
- Any polling split (Angus Reid / Leger).
Verify each before listing; omit or `[UNVERIFIED]` if unverifiable. Never fabricate.

## Editorial register (prose formats)
No em-dashes (load-bearing only), no "not X but Y", no leading affirmations, no summary conclusions. Verdicts earned. Label all content working draft.

## Decisions log
- D1: Jekyll classic deploy (matches Pratt), no Actions workflow needed.
- D2: 6-item nav mirrors Pratt; full format set via home cards + footer.
- D3: Switched deploy from legacy branch-build to GitHub Actions Jekyll workflow. Legacy "Page build failed" gave no diagnostics; Actions surfaced the real errors (custom `exclude:` had dropped Jekyll's default vendor/bundle exclusion; two unquoted YAML values contained colons). ROS-159 build spec explicitly allows "deploy via Actions", so this stays in spec. All fixed; build green, 0/30 internal links broken.
- D4: Official Alberta Oct 19 2026 question verified as a two-option procedural question (commence a legal process toward a future binding referendum), NOT a 37-word direct-separation question as the brief assumed. Used the verified wording; it strengthens the detachable-telos reading. King's Bench ruling cited Treaties 7 and 8 specifically.
