import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const workflow = readFileSync(new URL('../.github/workflows/preview-link.yml', import.meta.url), 'utf8');
const script = workflow.split('          script: |\n')[1]
  .split('\n').map(line => line.startsWith('            ') ? line.slice(12) : line).join('\n');
const repository = 'Orca-Solutions/diamond-dog-landing';
const sha = 'a'.repeat(40);
const nextSha = 'b'.repeat(40);
const deployment = '12345678-1234-1234-1234-123456789abc';
const preview = 'https://12345678.diamonddog-a17.pages.dev/';
const env = {
  CF_ACCOUNT: '10a1430d3ed1c6f0b8bafcd1170c3778',
  CF_PROJECT: 'diamonddog', CF_HOST: 'diamonddog-a17.pages.dev',
};
const pull = () => ({
  number: 9, state: 'open',
  head: { sha, repo: { full_name: repository } },
  base: { repo: { full_name: repository } },
});
const check = () => ({
  id: 100, head_sha: sha, status: 'completed', conclusion: 'success',
  app: { id: 85455, slug: 'cloudflare-workers-and-pages' },
  details_url: `https://dash.cloudflare.com/?to=/${env.CF_ACCOUNT}/pages/view/diamonddog/${deployment}`,
  output: { summary: `<a href='${preview}'>Preview</a>` },
});

async function reconcile(state) {
  state.writes ??= [];
  state.comments ??= [];
  const github = {
    rest: {
      pulls: {
        list: async () => ({ data: state.pulls ?? [pull()] }),
        get: async ({ pull_number }) => ({
          data: state.current ?? (state.pulls ?? [pull()]).find(p => p.number === pull_number),
        }),
      },
      checks: { listForRef: async ({ ref }) => ({ data: {
        check_runs: (state.checks ?? [check()]).filter(c => c.head_sha === ref),
      } }) },
      issues: {
        listComments: async ({ issue_number }) => ({
          data: state.comments.filter(c => c.issue_number === issue_number),
        }),
        createComment: async args => {
          state.writes.push({ action: 'create', ...args });
          state.comments.push({ ...args, id: state.comments.length + 1,
            user: { login: 'github-actions[bot]' } });
        },
        updateComment: async args => {
          state.writes.push({ action: 'update', ...args });
          Object.assign(state.comments.find(c => c.id === args.comment_id), { body: args.body });
        },
      },
    },
    paginate: async (method, args) => {
      const result = (await method(args)).data;
      return result.check_runs ?? result;
    },
  };
  await vm.runInNewContext(`(async () => { ${script}\n })()`, {
    github, context: { repo: { owner: 'Orca-Solutions', repo: 'diamond-dog-landing' } },
    process: { env }, URL,
  });
  return state;
}

test('a build completed before PR creation gets its verified preview link', async () => {
  const state = await reconcile({});
  assert.equal(state.writes.length, 1);
  assert.match(state.comments[0].body, /Open Cloudflare preview/);
  assert.ok(state.comments[0].body.includes(preview));
  assert.ok(state.comments[0].body.includes(sha));
});

test('existing current native comments are retained without a duplicate', async () => {
  const state = await reconcile({ comments: [{ id: 8, issue_number: 9,
    user: { login: 'cloudflare-workers-and-pages[bot]' },
    body: `Preview ${preview.slice(0, -1)} commit ${sha.slice(0, 7)}` }] });
  assert.equal(state.writes.length, 0);
});

test('repeated events are idempotent and a new head never retains the old link', async () => {
  const state = await reconcile({});
  await reconcile(state);
  assert.equal(state.writes.length, 1);
  state.pulls = [pull()];
  state.pulls[0].head.sha = nextSha;
  await reconcile(state);
  assert.match(state.comments[0].body, /Waiting for a successful/);
  assert.ok(!state.comments[0].body.includes(preview));
  assert.ok(state.comments[0].body.includes(nextSha));
  const newer = check(); newer.head_sha = nextSha;
  state.checks = [newer];
  await reconcile(state);
  assert.equal(state.comments.length, 1);
  assert.ok(state.comments[0].body.includes(preview));
});

test('failed builds replace an existing fallback success with failure status', async () => {
  const state = await reconcile({});
  state.checks = [check()]; state.checks[0].conclusion = 'failure';
  await reconcile(state);
  assert.match(state.comments[0].body, /did not succeed/);
  assert.ok(!state.comments[0].body.includes(preview));
});

test('wrong app, account, project, source and untrusted preview URLs cannot be published', async t => {
  const cases = {
    'different app id': c => { c.app.id = 1; },
    'different app slug': c => { c.app.slug = 'someone-else'; },
    'old source SHA': c => { c.head_sha = nextSha; },
    'different account': c => { c.details_url = c.details_url.replace(env.CF_ACCOUNT, '0'.repeat(32)); },
    'different project': c => { c.details_url = c.details_url.replace('/diamonddog/', '/other/'); },
    'lookalike host': c => { c.output.summary = `<a href='${preview.slice(0, -1)}.evil.example/'>Preview</a>`; },
    'different deployment': c => { c.output.summary = c.output.summary.replace('12345678.', '87654321.'); },
    'userinfo': c => { c.output.summary = c.output.summary.replace('https://', 'https://secret@'); },
    'insecure URL': c => { c.output.summary = c.output.summary.replace('https://', 'http://'); },
    'untrusted dashboard': c => { c.details_url = c.details_url.replace('dash.cloudflare.com', 'example.com'); },
  };
  for (const [name, mutate] of Object.entries(cases)) {
    await t.test(name, async () => {
      const c = check(); mutate(c);
      const state = await reconcile({ checks: [c] });
      assert.equal(state.writes.length, 0);
    });
  }
});

test('forks and closed PRs are excluded', async () => {
  const fork = pull(); fork.head.repo.full_name = 'outside/fork';
  const closed = pull(); closed.state = 'closed';
  const state = await reconcile({ pulls: [fork, closed] });
  assert.equal(state.writes.length, 0);
});

test('a PR changing while its check is read is not given a stale link', async () => {
  const current = pull(); current.head.sha = nextSha;
  const state = await reconcile({ current });
  assert.equal(state.writes.length, 0);
});

test('reconciliation covers every open same-repository PR after queued events', async () => {
  const second = pull(); second.number = 10;
  const state = await reconcile({ pulls: [pull(), second] });
  assert.deepEqual(state.writes.map(c => c.issue_number), [9, 10]);
});

test('workflow has no checkout, PR target event, deployment credentials or production rights', () => {
  assert.match(workflow, /pull_request:/);
  assert.match(workflow, /check_run:/);
  assert.match(workflow, /checks: read\n  pull-requests: write/);
  assert.doesNotMatch(workflow, /pull_request_target|secrets\.|checkout@|pages: write|id-token: write|contents: write/);
});
