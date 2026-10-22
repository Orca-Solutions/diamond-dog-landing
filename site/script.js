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
