# Alberta Market Entry — Footer & Schema Templates

Reusable templates for the FIXLIFY (Edmonton) and NEARY (Calgary) Alberta rollout.
A migration script will inject these into existing HTML pages keyed by region detection.

## Phase 1 Constraints (LOCKED)

- **NO phone numbers anywhere on Alberta pages** — booking form + email only.
- **No fake reviews / no `aggregateRating`** in schema.
- **No `LocalBusiness` schema** — using `ProfessionalService` (no GBP yet, no listed phone).
- **Pure SEO branding** — H1/title use city keyword phrasing; brand name only in meta + footer.
- **Per-location footer** — Edmonton pages get Edmonton footer; Calgary pages get Calgary footer.

## Files

| File | Purpose | Used by |
|------|---------|---------|
| `footer-edmonton.html` | Edmonton footer with Edmonton CMA service area, address, email CTA | All Edmonton-targeted pages on **fixlifyservices.com** |
| `footer-calgary.html` | Calgary footer with Calgary CMA service area, address, email CTA | All Calgary-targeted pages on **appliancerepairneary.com** |
| `footer-default.html` | Existing Toronto footer (centralized snapshot) | NIKA, NAR, and non-Alberta pages on FIXLIFY/NEARY |
| `schema-edmonton.json` | `ProfessionalService` JSON-LD template for Edmonton pages | All Edmonton pages |
| `schema-calgary.json` | `ProfessionalService` JSON-LD template for Calgary pages | All Calgary pages |

## Footer CSS Reuse

Each footer reuses the **existing site's** CSS classes — no new stylesheets are introduced.

- `footer-edmonton.html` → uses **FIXLIFY's** `.fx-footer`, `.fx-footer-inner`, `.fx-footer-cta-strip`, `.fx-footer-columns`, `.fx-footer-col`, `.fx-footer-list`, `.fx-footer-bottom` classes (already inlined in fixlifyservices.com `<style>` blocks).
- `footer-calgary.html` → uses **NEARY's** `.site-footer`, `.footer-inner`, `.footer-columns`, `.footer-col`, `.footer-links`, `.footer-bottom` classes (already inlined in appliancerepairneary.com `<style>` blocks).
- `footer-default.html` → uses **NIKA's** `.main-footer`, `.footer-content-seo`, `.footer-columns`, `.footer-col`, `.lz-trust-strip` classes.

This means: as long as the page already loads its own site's `<style>` blocks (which all current pages do), these footers will visually match seamlessly. **No additional CSS file needs to be loaded.**

## Schema Placeholder Variables

The two `schema-*.json` files contain Mustache-style placeholders the migration script must replace per-page:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{PAGE_URL}}` | Canonical URL of the page | `https://fixlifyservices.com/services/refrigerator-repair-edmonton/` |
| `{{BUSINESS_NAME}}` | SEO-optimized business name | `Edmonton Refrigerator Repair` or `Calgary Appliance Repair Near You` |
| `{{PAGE_DESCRIPTION}}` | 150-160 char meta description (use page's existing `<meta name="description">`) | `Same-day refrigerator repair in Edmonton...` |
| `{{HERO_IMAGE_URL}}` | Absolute URL to page hero image | `https://fixlifyservices.com/assets/images/refrigerator-repair-edmonton.jpg` |
| `{{SERVICE_TYPE_OR_APPLIANCE_REPAIR}}` | Service type — appliance-specific or generic `Appliance Repair` | `Refrigerator Repair` |

## What is intentionally NOT in the schema

- **No `telephone`** — phone field absent (Phase 1 policy)
- **No `aggregateRating`** — no fake reviews
- **No `LocalBusiness`** type — using `ProfessionalService` since no GBP exists yet
- **No `sameAs`** social links until brand presence is established

When Phase 2 starts (GBP listings live, real reviews), upgrade to `LocalBusiness` and add: `telephone`, `aggregateRating`, `review`, `sameAs`.

## Migration Script Contract

The migration script (separate file, not in this directory) should:

1. **Detect region** per page — scan filename/canonical/H1/breadcrumb for "edmonton", "calgary", or surrounding-city tokens (sherwood park, st-albert, airdrie, etc.).
2. **Pick footer** — Edmonton tokens → `footer-edmonton.html`; Calgary tokens → `footer-calgary.html`; otherwise → `footer-default.html`.
3. **Replace existing footer** — match `<footer ...>...</footer>` (greedy, single per page) and swap in the chosen template.
4. **Inject schema** — read `schema-edmonton.json` or `schema-calgary.json`, fill placeholders from the page's existing `<title>`, `<meta name="description">`, canonical link, and the largest `<img>` near `<h1>`. Wrap in `<script type="application/ld+json">...</script>` and insert before `</head>`. **Replace** any existing `ProfessionalService` / `LocalBusiness` JSON-LD on the same page (do not duplicate).
5. **Strip phone numbers** — as a safety net, the migration script should regex-strip any `(403)`, `(587)`, `(780)`, `(825)`, `(437)`, `(416)`, `(647)` phone tokens AND `tel:` links from Alberta pages before saving. This catches phones in body content (hero CTAs, sticky bars, mid-page CTAs) — the templates only cover the footer.

## Validation (run after migration)

```bash
# 1. Schema JSON validity
node -e "JSON.parse(require('fs').readFileSync('schema-edmonton.json','utf8'))"
node -e "JSON.parse(require('fs').readFileSync('schema-calgary.json','utf8'))"

# 2. No telephone field in Alberta schemas
grep -i "telephone" schema-edmonton.json schema-calgary.json   # must return nothing

# 3. No Toronto strings in Alberta footers/schemas
grep -iE "toronto|ontario|gta|\(437\)|\(416\)" footer-edmonton.html footer-calgary.html schema-edmonton.json schema-calgary.json   # must return nothing
```

## Future Phase 2 Upgrades

When ready to switch on phones, reviews, GBP:

- Replace `ProfessionalService` → `LocalBusiness`
- Add `telephone`, `aggregateRating`, `review`, `sameAs`
- Add phone CTAs to footers (preserve email + booking)
- Add `priceRange` precision (e.g. `$80-$300`)
