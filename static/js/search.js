(() => {
  const input = document.getElementById('site-search');
  const results = document.getElementById('search-results');
  const status = document.getElementById('search-status');
  if (!input || !results || !status) return;
  const indexUrl = new URL('../search-index.json', document.currentScript.src);
  let entries = [];
  fetch(indexUrl).then(r => {
    if (!r.ok) throw new Error('index unavailable');
    return r.json();
  }).then(data => { entries = Array.isArray(data) ? data : []; })
    .catch(() => { status.textContent = 'Search is temporarily unavailable.'; });
  input.addEventListener('input', () => {
    const q = input.value.trim().toLocaleLowerCase();
    results.replaceChildren();
    if (!q) { status.textContent = ''; return; }
    const found = entries.filter(p => `${p.title} ${p.summary} ${p.content} ${(p.tags || []).join(' ')} ${(p.categories || []).join(' ')}`.toLocaleLowerCase().includes(q)).slice(0, 30);
    status.textContent = `${found.length} result${found.length === 1 ? '' : 's'}`;
    for (const p of found) {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = p.url;
      a.textContent = p.title;
      const summary = document.createElement('p');
      summary.textContent = p.summary || '';
      li.append(a, summary);
      results.append(li);
    }
  });
})();
