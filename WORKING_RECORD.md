# Working record

## 2026-10-20 — Coming-soon website and brand handoff

Jason approved Diamond Dog's brand direction and requested a coming-soon site, a separate branch, and a separate repository containing both the site and brand kit. The OrcaOS tool repository is outside this change's scope.

Implemented a buildless, responsive static page using the approved symmetrical logo, black mascot with diamond collar tag, warm paper/ink palette, acid and lilac accents, and locally bundled fonts. The primary line is “Delegate work, not your identity.” The page explains bounded work and records, distinguishes accepted requests from unknown delivery, and gives honest early-stage answers. No launch date, signup flow, shipped-product claim, or permission-centric language is invented.

The evidence card is an illustrative marketing scenario. Both evidence labels remain visible when selecting either explanation. It does not restyle the fixed inspector evaluation screens. The final GitHub link points to the existing tool repository under its current OrcaOS name.

Verification: local HTTP 200; JavaScript syntax check; desktop, 1024px tablet, 800px narrow tablet, 390px phone and 320px small-phone viewport inspection. Repaired a narrow-tablet illustration/copy overlap by switching to the stacked layout earlier. Checked Accepted/Unknown explanation changes and FAQ expansion. Checked small-screen document width for horizontal overflow and browser warnings/errors (none reported). The main landmark encompasses all page sections. Visible focus treatment, reduced-motion CSS, alternative text, and native disclosure controls are present. No formal assistive-technology audit was performed.

Review: author verification sufficient — static presentation, copy, and local illustrative interactions; no custom authentication, payments, external writes, or sensitive-data handling.

Delivery: new private repository `Orca-Solutions/diamond-dog-landing`; implementation branch `codex/diamond-dog-coming-soon`. No automatic GitHub deployment is configured. Merge remains Jason's action. The owner-private Sites deployment is tracked in the delivery receipt beside this record. Public launch/domain and source/brand licensing remain unresolved choices, not implementation blockers for private review.

## 2026-10-20 — Repository destination correction

Jason requested `Orca-Solutions/diamond-dog-landing` as the delivery destination. The repository was empty; seeded its base from the original README-only baseline, then pushed the existing implementation and this signed reference correction on the working branch. Website and brand assets are unchanged, so the prior browser verification and private deployment remain applicable. The prior repository is retained; its PR is superseded by the PR in the requested destination.

## 2026-10-21 — Public-domain launch preparation

Jason confirmed `diamonddog.orcasolutions.dev` and requested launch. PR #1 is
merged as `6a9166149fe3640a553c9766cce9f97294633986`; GitHub now reports the
repository public. Frontend/domain management prepared a separate Git-connected
Cloudflare Pages rollout serving only `site/`. No brand-kit publication through
the web root, backend, secret, storage, paid upgrade or OrcaOS tool change is
needed. The existing private Sites review remains a separate deployment mirror.

Updated the canonical URL and Open Graph image/URL to the public domain and
documented the intended Git production/preview setup and rollback. These are
metadata and hosting-documentation changes; page appearance and JavaScript are
unchanged, so the October 20 viewport and interaction evidence remains applicable.
Author checks cover JavaScript syntax, local asset references and whitespace.
Production activation and normal public-domain HTTPS acceptance are recorded
separately in the linked DevOps record; this source change does not prove launch.
