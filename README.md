# mvxworld.art

> a personal universe. archived in transmissions. v0.1, expanding.

This is not a portfolio. It is the public-facing room of a multi-handle internet
native who treats design, code, and culture as one practice. The site grows
organically, page by page. Every new page is a room discovered, not a section
bolted on.

---

## status

**Phase 1** — shipping `index.html` (the main world) and `post.html` (the first transmission).

| | |
|---|---|
| Domain | `mvxworld.art` (registered + DNS at GoDaddy) |
| Stack | vanilla HTML + CSS + JS · no build step |
| Hosting | GitHub Pages (recommended) or Cloudflare Pages |
| Repo | [github.com/Trijbs/mvxworld](https://github.com/Trijbs/mvxworld) |
| Doc 001 | `mvxworld_plan_summary.txt` (the brief) |
| Doc 002 | `PLAN.md` (the thinking — read this) |

---

## file registry

```
mvxworld/
├── index.html        the main world         (dark, atmospheric, 5 rooms)
├── post.html         transmission 001       (light, narrow, the manifesto)
├── lore.html         the lore               (dark poster, 6 panels, scroll-driven)
├── tokens.css        design system tokens   (one source of truth)
├── PLAN.md           research + thinking    (read before iterating)
├── README.md         this file
├── CNAME             github pages custom domain → mvxworld.art
├── .nojekyll         tells github pages "don't process me — i'm static"
├── .gitignore
└── mvxworld_plan_summary.txt   doc 001 — the original brief
```

---

## room registry

| # | path | status | description |
|---|---|---|---|
| 00 | `index.html` | live | main world, dark archive |
| 01 | `post.html` | live | transmission 001 — the intersection |
| 02 | `lore.html` | live | the lore — manifesto as 6-panel poster |
| 03 | `work.html` | future | curated work, when work exists |
| 04 | `gallery.html` | future | image archive |
| 05 | `drop.html` | future | release pages for products / drops |
| 06 | `eyew/` | future | sub-brand sub-path |

---

## design system (short version — full version in PLAN.md)

```css
--ink-base    #0a0a09   /* dark archive base       */
--ink-surface #1a1a18   /* hover wells             */
--paper       #f5f3ee   /* off-white text on dark  */
--paper-deep  #ebe7dc   /* the post-page background*/
--acid        #c8ff00   /* primary accent          */
--burn        #ff4d1c   /* secondary, sparingly    */
--mute        #7a7870   /* metadata, captions      */
```

Type pairing: **Cormorant Garamond** italic serif × **IBM Plex Mono**.
The friction between warm italic serif and cold mono *is* the brand.
No third typeface.

---

## run locally

No build step. Just serve the folder:

```bash
# python (any version)
python3 -m http.server 8080

# or node
npx serve .

# or just open the file in a browser, but use a server for the fonts to load cleanly
```

Then open `http://localhost:8080`.

---

## deploy — first push

The repo lives at **`github.com/Trijbs/mvxworld`**. From this folder:

```bash
git init
git add .
git commit -m "doc 001 — the room is open"
git branch -M main
git remote add origin git@github.com:Trijbs/mvxworld.git
git push -u origin main
```

After this, every push to `main` redeploys.

---

## deploy — option A: GitHub Pages (recommended, fewest moving parts)

The `CNAME` file in the root already contains `mvxworld.art`, and `.nojekyll` is
included so GitHub serves the files as-is (no Jekyll processing, no skipped
underscored files).

**1 · Enable Pages on the repo:**
- GitHub → repo → Settings → Pages
- Source: `Deploy from a branch` · Branch: `main` · Folder: `/ (root)` · Save
- Once it builds, GitHub will show: *Your site is published at https://trijbs.github.io/mvxworld/*

**2 · Add the custom domain in Pages settings:**
- In the same Pages settings panel, set Custom domain → `mvxworld.art` → Save
- GitHub will start checking DNS. Wait until DNS is configured before checking "Enforce HTTPS".

**3 · Configure DNS at GoDaddy:**
- Log into GoDaddy → My Products → `mvxworld.art` → DNS
- Set these records (delete any existing A / CNAME entries that conflict):

  | Type  | Name | Value                  | TTL    |
  |-------|------|------------------------|--------|
  | A     | @    | `185.199.108.153`      | 1 hour |
  | A     | @    | `185.199.109.153`      | 1 hour |
  | A     | @    | `185.199.110.153`      | 1 hour |
  | A     | @    | `185.199.111.153`      | 1 hour |
  | CNAME | www  | `trijbs.github.io`     | 1 hour |

  *(GoDaddy uses `@` for the apex / root domain. Don't include the trailing dot.)*

**4 · Wait + verify:**
- DNS propagation: usually under an hour. Sometimes longer.
- Back in GitHub Pages settings, once the green check appears, tick **"Enforce HTTPS"**.
- Visit `https://mvxworld.art` — the room is open.

---

## deploy — option B: Cloudflare Pages (faster CDN, more features)

If you want Cloudflare's edge network, instant cache purges, and analytics:

**1 · Connect the repo:**
- Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git
- Pick `Trijbs/mvxworld` → Production branch: `main` → Build command: *(empty)* → Build output directory: `/`
- Deploy. You'll get a `mvxworld-xyz.pages.dev` URL.

**2 · Add the custom domain in Cloudflare Pages:**
- Project → Custom domains → Set up a domain → `mvxworld.art`
- Cloudflare will give you DNS records to set.

**3 · Configure DNS at GoDaddy** (keeping DNS at GoDaddy — easier path):
- In GoDaddy DNS, add a CNAME for `@` (or use ALIAS if available) pointing at `mvxworld-xyz.pages.dev`
- Add a CNAME for `www` pointing at the same target
- Some registrars don't allow CNAMEs at the apex; GoDaddy supports CNAME-flattening via "Forwarding" or you can switch to Cloudflare-managed DNS (option below).

**Or — full transfer, recommended for Cloudflare Pages:**
- Cloudflare → Add a Site → `mvxworld.art` → Free plan → it'll show you two nameservers
- In GoDaddy: Domain settings → Nameservers → Change → enter the two Cloudflare nameservers
- Once propagated (a few hours), Cloudflare manages DNS. Then add the custom domain in Pages and it auto-resolves.

---

## checklist before going live

- [ ] Repo pushed to `github.com/Trijbs/mvxworld`
- [ ] `index.html` and `post.html` open and render correctly locally
- [ ] `CNAME` file present at repo root (contains `mvxworld.art`)
- [ ] `.nojekyll` file present at repo root
- [ ] GitHub Pages enabled · custom domain set
- [ ] GoDaddy DNS records pointing at the chosen host
- [ ] HTTPS enforced
- [ ] First visit on `https://mvxworld.art` works · Counter shows `0` · MVX/TIME ticks

---

## the counter — how to "reset"

The `index.html` Counter ("days since last interesting idea") is driven by a
single `<time datetime>` attribute. To reset it, edit one line:

```html
<time id="reset-date" datetime="YYYY-MM-DD">YYYY · MM · DD</time>
```

Push. The site re-renders. Public commitment device.

---

## build-session prompt (for future expansions)

Use at the start of each session that adds a new room:

```
PROJECT:      mvxworld.art — personal identity hub
DOMAIN:       mvxworld.art
IDENTITY:     Gen Z, NL-based, creative systems builder, dark aesthete
AESTHETIC:    Dark archive (#0a0a09), acid green (#c8ff00),
              grain texture, Cormorant Garamond × IBM Plex Mono,
              slow reveal animations, custom cursor,
              one weird module per page.
BUILD:        [page name].html
MODULES:      [list what this page needs]
WEIRD MODULE: [which one — see PLAN.md §7]
REFERENCES:   [paste images, links, vibe]
OUTPUT:       single HTML file, embedded CSS + JS, production-ready,
              uses tokens.css for shared system variables
```

---

## the rule

> **Mostly follows the rules. Breaks one per section. The break is the accent.**

If a new room doesn't break one rule, it's not a room yet — it's a section.

— mvxworld · doc 003 · v0.1 · expanding
