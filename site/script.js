const explanations = {
  accepted: 'The service accepted the request. That tells us something useful. It does not establish delivery.',
  unknown: 'Delivery was not observed. That is neither a success nor an error. It is the limit of what this record can tell us.'
};

const evidenceButtons = document.querySelectorAll('[data-evidence]');
const explanation = document.getElementById('evidence-explanation');

for (const button of evidenceButtons) {
  button.addEventListener('click', () => {
    for (const candidate of evidenceButtons) {
      const selected = candidate === button;
      candidate.setAttribute('aria-pressed', String(selected));
      candidate.classList.toggle('selected', selected);
    }

    explanation.textContent = explanations[button.dataset.evidence];
  });
}

const header = document.querySelector('.header');
let scrolled = null;

function updateHeader() {
  const next = window.scrollY > 8;
  if (next !== scrolled) {
    scrolled = next;
    header.classList.toggle('is-scrolled', next);
  }
}

window.addEventListener('scroll', updateHeader, { passive: true });
updateHeader();

// Preview builds only (Cloudflare's branch and commit links): a switch for trying dim mode without
// changing the device's setting. It retargets the dim-mode rule, so the stylesheet stays the one
// source of truth. The live site never shows it.
if (location.hostname.endsWith('.diamonddog-a17.pages.dev')) {
  const dimRule = [...document.styleSheets]
    .flatMap(sheet => [...sheet.cssRules])
    .find(rule => rule.media && rule.media.mediaText.includes('prefers-color-scheme: dark'));
  const modes = { Auto: '(prefers-color-scheme: dark)', Light: 'not all', Dim: 'all' };
  const group = document.createElement('div');

  group.className = 'scheme-switch';
  group.setAttribute('role', 'group');
  group.setAttribute('aria-label', 'Preview colour scheme');
  group.innerHTML = '<span>Preview</span>';

  function choose(mode) {
    dimRule.media.mediaText = modes[mode];
    for (const button of group.querySelectorAll('button')) {
      button.setAttribute('aria-pressed', String(button.textContent === mode));
    }
    try { sessionStorage.setItem('preview-scheme', mode); } catch {}
  }

  for (const mode of Object.keys(modes)) {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = mode;
    button.addEventListener('click', () => choose(mode));
    group.append(button);
  }

  if (dimRule) {
    document.body.append(group);
    let saved = 'Auto';
    try { saved = sessionStorage.getItem('preview-scheme') || 'Auto'; } catch {}
    choose(modes[saved] ? saved : 'Auto');
  }
}
