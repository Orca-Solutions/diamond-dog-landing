# Diamond Dog

**Delegate work, not your identity.**

The coming-soon website and first-edition brand kit for Diamond Dog, a delegation-first operating environment.

This repository is separate from [the OrcaOS tool](https://github.com/Orca-Solutions/OrcaOS). It contains no runtime implementation. The product is in early design, with a first experiment under way; nothing has shipped yet.

## Contents

- `site/` — portable static website, including local fonts and images.
- `brand-kit/` — 22-page brand book, SVG/PNG logos, mascot, font licenses, design tokens, applications, and voice guidance. Start with `brand-kit/START-HERE.txt`.
- `WORKING_RECORD.md` — decisions, verification, and current delivery state.

## Preview locally

From the repository root:

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory site
```

Open `http://127.0.0.1:4173`. There is no dependency installation or build step. The page is HTML/CSS with a small JavaScript interaction explaining evidence labels. FAQ sections use native HTML disclosure controls.

The page has no signup collection, analytics, cookies, backend, or account integration. The sample receipt is illustrative, not a product screenshot or a shipped workflow.

## Hosting

The current review deployment is owner-private on ChatGPT Sites:

https://diamond-dog-coming-soon.ninjasoforca.chatgpt.site

GitHub pushes do not deploy this repository. The review deployment uses a separate Sites-managed source mirror. Only `site/` is served; the brand kit is not placed in the web root. A public launch, custom domain, and production hosting configuration remain separate choices. The static folder is portable to a static host; update the absolute Open Graph image URL when changing domains.

To update the preview, copy the approved `site/` contents into the existing Sites project's static directory and publish through its supported workflow. To recover a prior appearance, restore `site/` from an approved earlier commit and redeploy that exact version. There is no database or user-submitted state to migrate.

## Brand and licensing

The selected logo has symmetrical ears. The black editorial dog has a narrow acid collar and a lilac diamond tag. The original reference photograph is excluded.

The brand book is the v1 design handoff; its landing-page concept is a historical concept, while `site/` is the implemented website. No changes are made to the tool's fixed inspector test screens.

Font license notices are included beside the font files. A brand-asset usage policy and a license for this website's source have not been selected. The tool's proposed software licenses do not automatically license these assets. The name and mark have not been cleared for public use. Allan Peters and Wharton did not participate in or endorse this work.
