# mvxworld.art — research, thinking, and the start

> Document 002 — companion to `mvxworld_plan_summary.txt` (doc 001)
> Date: 2026-04-27 · Phase: 0.1 → 0.2

This is the thinking behind the build. The plan summary defined *what*. This decodes *why* and pins down the *how* tightly enough that the site can grow without losing the thread.

---

## 1. The diagnosis (one paragraph)

You are not a designer with code skills, not a coder with taste, not an entrepreneur with a Behance. You are a creative systems builder — the person who builds the world, the interface, the lore, the monetization, and the marketing as one continuous gesture. That gesture has a native language: media design and graphic design as the way you naturally externalize ideas. mvxworld.art exists to make that gesture legible to other people without translating it into a CV. Translation is loss; what we want is transmission.

This site is the transmission.

---

## 2. Decoding the references

Not "what do they look like" — *what do they actually do*, and which part of that you are inheriting.

### strml.net — site as performance
The page assembles itself with code visibly running. The CSS rules type themselves out and the page reformats live. You watch the writer think.
**What you take:** the principle that *loading is not a chore, it is content*. A staggered reveal where headline arrives last is a small, free version of this. Phase 2: page transitions. Phase 4: a `lore.html` where text actually types itself.
**What you do not take:** the whole "developer talking to developers" frame. You are not flexing your dotfiles.

### alienheadshitkid.neocities.org — the personal room
Openly unfinished. Pixel art, broken-on-purpose elements, a clear voice in the typography. Not trying to convert anyone.
**What you take:** *permission to leave seams*. A "currently:" status that's clearly hand-edited. A counter that means nothing. A page that says it is being built. The room metaphor — pages as rooms discovered, not sections in a navbar.
**What you do not take:** the random GIF/glitter chaos. The MVX equivalent of openly unfinished is *quiet, intentional roughness*. Grain texture, not Comic Sans. One break per section, not chaos.

### trijbsworld.nl — your prototype
Same DNA as MVX but a chapter behind. It already knows how to do typographic restraint and a confident dark palette.
**What you take:** confidence with serifs on dark. Trust in big type and a lot of negative space.
**What you do not take:** the about-page framing. mvxworld.art doesn't have an /about. It has a manifesto and a counter.

### Instagram across @mvdhs.x · @eye.w8 · @trijbsworld · @r.tjbz — four frequencies
Reading these as a set: there is a moody documentary side, a street/visual-language side, a process/in-the-studio side, and a personal/living side. They co-exist without merging. **The site's job is to honor that multiplicity without flattening it.** Don't pick one tone — let the *frequencies* model show up structurally on the page.

### Pinterest @closesz — the latent moodboard
Pinterest boards aren't just inspiration; they're a record of taste convergence. Treat them as ground truth for the moodboard, not the outputs themselves. Reference them privately when designing each new room.

### Minecraft handles (TriButer · eyew · hyptc · KrustyKrabs · cwel12 · yvij · qPathetic) — the inhabitants
These aren't sock-puppet accounts. They're characters. **The site's lore is that mvxworld is inhabited.** Every handle has a frequency: TriButer = origin/lore, eyew = visual, hyptc = technical underground, qPathetic = post-ironic alter ego, MVX = the world itself, tjbz = the writer. The other handles (KrustyKrabs / cwel / yvij) are inhabitants we don't fully meet yet.

### GitHub @Trijbs — the workshop
Public, technical, shows you work. Linked from day 1 because it is the most "credentialed" surface that still feels yours. It's the side door to the site, not the front door.

### Steam — the trace
Doesn't get linked. It's a private record that exists. Mentioning it in a memory file is enough; the user doesn't need every account exposed.

---

## 3. Positioning, in one sentence

> mvxworld.art is the public-facing room of a multi-handle internet native who treats design, code, and culture as one practice — a slow archive that grows organically, not a portfolio that asks to be hired.

Audience priority, in order:

1. **Future you.** This site has to feel right to you in 18 months. That kills 80% of the conversion-funnel temptations.
2. **Internet-literate peers** — other Gen Z creatives, designers, builders who recognize the references without explanation.
3. **A small pool of people who might collaborate or commission you** — they should be able to figure out you're for hire if they care enough to look. They should never be the design center of gravity.

Audience anti-priority: recruiters skimming for "key skills." If a recruiter doesn't get it, the site is doing its job.

---

## 4. Voice

**Lexicon to use, freely:**
archive · transmission · frequency · room · world · inhabitant · signal · koordinaten · lore · drop · field · static

**Lexicon to avoid:**
welcome · about me · portfolio · services · let's work together · hire me · clients · case study · skills · achievements · journey · passionate

**Sentence shape:**
Short. Cold. Sometimes one word. Then a long sentence that earns it. Lowercase preferred for UI labels, uppercase for system chrome ("MVX/TIME", "TRANSMISSIE 001").

**Language:** English mostly, with sparse Dutch/coded words for texture (`koordinaten`, `transmissie`, `de wereld`). One Dutch word per page is enough.

**The two voices on the site:**
- *Index voice* — sparse, declarative, fragment-heavy. The hallway.
- *Manifesto/post voice* — slower, sentence-paragraphs, italic serif. The room you sit down in.

The shift between them is the point. A reader who only sees the index gets atmosphere. A reader who clicks through gets you.

---

## 5. Design system (refined)

### Color tokens
| Token | Value | Use |
|---|---|---|
| `--ink-base` | `#0a0a09` | Index background, post chrome |
| `--ink-surface` | `#1a1a18` | Subtle panels, hover wells |
| `--paper` | `#f5f3ee` | Index foreground text, post background |
| `--paper-deep` | `#ebe7dc` | Post page surface (slightly cooler than #f5f3ee for contrast variation) |
| `--acid` | `#c8ff00` | Primary accent — selection, counter, hover, signal dot |
| `--burn` | `#ff4d1c` | Secondary accent — used max once per page |
| `--mute` | `#7a7870` | Metadata, inactive labels, captions |

**Contrast notes (WCAG AA target):**
- `--paper` on `--ink-base` ≈ 16.5:1 ✓
- `--mute` on `--ink-base` ≈ 5.2:1 ✓ (large text only at smaller sizes)
- `--acid` on `--ink-base` ≈ 14.8:1 ✓ (legible even though it looks "neon")
- `--ink-base` on `--acid` selection ≈ 14.8:1 ✓
- Body text on post page: `--ink-base` on `--paper-deep` ≈ 15.1:1 ✓

### Type
- **Display:** Cormorant Garamond — italic 500/700. Reserved for headlines, manifesto, declarations. *Italic is the default*; upright Cormorant rarely appears.
- **UI/body:** IBM Plex Mono — 400/500. Labels, navigation, metadata, the counter, the timer.
- **Post body:** Cormorant Garamond regular (not italic), 18–20px, 1.55 line-height. Reading-optimized, not stylized.

The friction between *italic warm serif* and *cold mono* is the personality. No third typeface. Ever.

### Type scale (modular, 1.25 ratio, tuned for 16px base)
- 12px — meta/status (mono)
- 14px — body labels (mono)
- 16px — base (mono)
- 20px — small display (serif)
- 28px — section heads (mono caps)
- 48–72px — hero sub (serif italic)
- 96–160px — hero declaration (serif italic, fluid `clamp()`)

### Spacing & rhythm
8px base unit. Page gutter: clamp(20px, 5vw, 64px). Vertical rhythm between sections: 96px desktop / 64px mobile. The page should breathe — empty space is content.

### Grid behavior
12-column on desktop with generous side gutters. **One element per section breaks the grid** (overhanging into the gutter, rotated, vertical, off-baseline). The break is the accent — without it the site feels like a magazine.

### Texture: grain
A fixed-position SVG noise overlay at ~6% opacity, `mix-blend-mode: overlay`, `pointer-events: none`. Scales to viewport. This is the single most identity-defining visual element after the type pairing — without it, dark archive becomes generic dark portfolio.

### Cursor
Custom on pointer devices only (`@media (hover: hover) and (pointer: fine)`). Two states: a 6px dot (default) and a 28px outline circle on hover targets. Acid green. Disabled on touch.

### Selection
`::selection` → `--acid` background, `--ink-base` text. Tiny detail, huge personality multiplier. People notice the second time they highlight something.

---

## 6. Information architecture

### Phase 1 — what ships now
```
mvxworld.art/
├── index.html        ← the main world
├── post.html         ← the manifesto (first transmission)
├── tokens.css        ← shared design system variables
├── README.md         ← build prompt + room registry
└── PLAN.md           ← this document
```

Two pages, two distinct atmospheres. The index is dark, sparse, atmospheric. The post is light, narrow, readable. The transition between them is *intentional rupture* — you click through and land somewhere fundamentally different. That's the room metaphor working: the hallway and the library are not styled the same.

### Phase 2 — when there's a second post
- Add `posts/` directory, second post lives there
- Promote `lore.html` (full manifesto poster experience)
- Add page-transition fade-to-black

### Phase 3 — when work exists to show
- `work.html` (curated, opinionated — not "everything I made")
- `gallery.html` (image archive)
- Newsletter or Discord (whichever you'll actually maintain — pick one)

### Phase 4 — sub-brands and drops
- `drop.html` for product / creative releases
- `eyew/` as visual sub-brand sub-path
- A 3D module (Three.js) on a single page — *not the homepage*

### Naming convention for new rooms
Single noun. Lowercase. No camelCase, no hyphens. `lore`, `gallery`, `drop`, `archive`, `signal`. If a room needs two words, the room isn't ready.

---

## 7. Modules on the index

In reading order down the page:

**1 · Hero (full viewport)**
A single italic serif declaration — `mvxworld` — with a small `/v0.1` mono tag and a `MVX/TIME` clock. Empty otherwise. The hero is a held breath.

**2 · Frequencies (the cryptic identity strip)**
A horizontal mono band listing the inhabitants:
`MVX · tjbz · eyew · hyptc · TriButer · qPathetic`
Two of these are linked in phase 1: tjbz → github.com/Trijbs, eyew → instagram.com/mvdhs.x. The rest are dimmed (`--mute`) — visible but not yet meeting the visitor. Hovering a dimmed one shows a one-line whisper ("not yet · 404 by design").

**3 · Status / "currently"**
Three mono lines: building / listening / thinking. Hand-edited HTML — feels alive precisely because it's clearly not.

**4 · The Counter (weird module)**
> *days since last interesting idea: 0*
The counter is a `<time datetime>` element. JS reads the datetime and computes days. The "reset" date is a constant in the source — change it manually when an interesting idea actually occurs. Public commitment device disguised as a joke. This is the module visitors will spend 20 seconds trying to decode.

**5 · Manifesto teaser**
Three italic serif lines from the manifesto, then an `→ read transmission 001` link in mono. The teaser does not preview the conclusion. It pulls the reader through.

**6 · Latest transmission card**
Title + date + frequency tag. Single card, no list. When there's a second post, this becomes a card list.

**7 · Koordinaten (footer)**
Amsterdam coordinates `52.3676° N · 4.9041° E`, the MVX/TIME clock, the version tag `mvxworld · v0.1 · expanding`. No copyright. No "made with love". Just the location of the room.

---

## 8. Interaction principles

| Principle | Concrete behavior |
|---|---|
| Slow reveal | Page load: staggered fade-in over ~1.4s. Hero text arrives last, at 1.0–1.4s. Things wake up. |
| Hover with weight | Links: letter-spacing widens 2–4px + color shift to `--acid` over 240ms. Never just a color flip. |
| Selection as identity | `::selection` is acid green. |
| Cursor as focus | Custom dot/circle, acid. Grows on links. |
| Scroll | Native. `IntersectionObserver` fades each section in once. No smooth-scroll library. |
| Touch | Cursor disabled. Grain stays. Modules unchanged. Hovers become tap states. |
| Reduced motion | `@media (prefers-reduced-motion)` removes all reveals + cursor effects. |
| Page transitions | Phase 1: none. Phase 2: 300ms fade-to-black both ways. |

---

## 9. Accessibility — the floor we don't go under

- All interactive targets ≥ 40×40px on mobile.
- Color contrast meets WCAG AA on every text/background pair (verified in §5).
- Acid green is the brand color but is *never* the only signal. Hover always combines color + letter-spacing. Counter combines color + literal text label.
- Focus states visible (acid outline, 2px, 4px offset). No `outline: none` without replacement.
- Custom cursor never disables the system cursor on touch / pointer-coarse devices.
- Grain overlay is `aria-hidden` and `pointer-events: none`.
- Manifesto post: 18–20px body, 1.55 line-height, max ~640px column width.
- Reduced-motion users get a static, complete site immediately.
- Semantic HTML — `<header>`, `<main>`, `<article>`, `<nav>`, `<footer>`, `<time>`. The site should make sense to a screen reader.

---

## 10. Performance budget

Hard targets, phase 1:
- Total page weight under 200KB on the index. No images yet means this is easy if we don't bloat fonts.
- Two font families, weights actually used: Cormorant 500i + 700i, Plex Mono 400 + 500. ~4 weights total. Use `&display=swap` and `text=` subsetting if it grows.
- Zero JS frameworks. Two ≤2KB inline scripts (cursor + counter + reveal observer).
- LCP < 1.5s on a typical connection. The hero is text — it's basically free.
- No analytics in phase 1. When you want them: Cloudflare Web Analytics (cookieless, free, ships with Pages).

---

## 11. The first five posts (writing roadmap)

So the site has a future after the manifesto:

1. **Transmission 001 — `the intersection`** (the manifesto, ships at launch)
2. **Transmission 002 — `the unfair advantage`** — why "internet-native" is a design discipline, not a generation.
3. **Transmission 003 — `naming things`** — short post on the etymology of MVX / tjbz / eyew. Lore as content.
4. **Transmission 004 — `the room metaphor`** — why the site grows page-by-page instead of being launched complete.
5. **Transmission 005 — `from forts to worlds`** — biographical, the throughline. Probably the post that becomes the about-page-without-being-an-about-page.

Posting cadence target: one transmission per 4–6 weeks. Slower is fine — the counter forgives infrequency, in fact it's the joke.

---

## 12. Risks and how we counter them

| Risk | Counter |
|---|---|
| Site feels generic-dark-portfolio | Grain + acid selection + counter + cryptic frequencies. The four cheapest, hardest-to-fake details. |
| Site feels too cool to engage with | Manifesto post is warm and direct. The serif on cream is the welcome mat the index refuses to be. |
| Site stagnates after launch | Counter forces honesty; status line forces small updates; transmission roadmap pre-loads writing momentum. |
| Cluttered identity layer | Phase 1 limits public links to two (Trijbs + mvdhs.x). The rest are visible-but-dim. |
| Recruiter-thinks-it's-amateur | The hidden "professional" layer is the GitHub link. Anyone who needs to verify can; the homepage doesn't have to do that work. |
| Mobile experience as afterthought | Cursor scoped to pointer-fine. Type uses `clamp()`. Counter and frequencies stack vertically below 720px. Tested early. |

---

## 13. Definition of done — phase 1

- [ ] `index.html` renders alone, no external CSS file required if we want to ship it standalone (we use `tokens.css` as a shared scaffold instead — see §6)
- [ ] `post.html` renders the manifesto on a light background, narrow column
- [ ] Both pages pass HTML validation
- [ ] Both pages work on mobile down to 360px
- [ ] Color contrast verified for every text/background pair
- [ ] No horizontal scroll on any breakpoint
- [ ] `prefers-reduced-motion` users get a complete static site
- [ ] Grain overlay on index, not on post
- [ ] Acid-green selection on index, default selection on post (intentional difference — the post is the calm room)
- [ ] Pushed to `github.com/Trijbs/mvxworld`
- [ ] Deployed via GitHub Pages (recommended) or Cloudflare Pages (see README §deploy)
- [ ] GoDaddy DNS records updated · CNAME file present in repo root · HTTPS enforced

---

## 14. Next steps after phase 1 ships

In strict order:
1. Live on the domain. Don't iterate before it's public. Living-on-the-domain is itself part of the design.
2. Tell three people. Not a launch — a soft pass. See where they get confused, where they linger.
3. Write transmission 002 within two weeks. The site needs proof of pulse.
4. Add a `lore.html` poster page once the manifesto has lived as a post for a while.
5. Decide on Discord vs newsletter — pick the one you'd actually maintain. Then add it.

---

*This plan expands as the world grows. Edit it. Don't precious it.*
*— mvxworld · doc 002 · v0.1*
