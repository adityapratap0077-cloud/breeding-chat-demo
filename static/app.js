const chat = document.getElementById('chat');
const form = document.getElementById('form');
const input = document.getElementById('input');
const sendBtn = document.getElementById('send');

const EXAMPLES = [
  "Which varieties held yield above 4 t/ha under salinity in boro season?",
  "Compare Pokkali and FL478",
  "What is the Saltol QTL and which varieties carry it?",
  "Which aman-season varieties are salt tolerant, ranked by saline yield?",
  "What does dS/m measure?",
  "What wheat varieties tolerate salinity?"
];

const chipsBox = document.getElementById('chips');
EXAMPLES.forEach(function (q) {
  const b = document.createElement('button');
  b.type = 'button'; b.className = 'chip'; b.textContent = q;
  b.onclick = function () { input.value = q; form.requestSubmit(); };
  chipsBox.appendChild(b);
});

function addMsg(cls, html) {
  const d = document.createElement('div');
  d.className = 'msg ' + cls;
  d.innerHTML = html;
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
  return d;
}
function esc(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

form.addEventListener('submit', async function (e) {
  e.preventDefault();
  const q = input.value.trim();
  if (!q || sendBtn.disabled) return;
  input.value = '';
  addMsg('q', '<span>' + esc(q) + '</span>');
  const typing = addMsg('a', '<div class="who">Assistant</div><div class="typing">Looking up trial data…</div>');
  sendBtn.disabled = true;
  const ctrl = new AbortController();
  const timer = setTimeout(function () { ctrl.abort(); }, 30000);
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({question: q}),
      signal: ctrl.signal
    });
    clearTimeout(timer);
    if (!res.ok) throw new Error('http ' + res.status);
    const data = await res.json();
    if (!data.answer) throw new Error('bad response');
    let rowsHtml = '';
    if (data.rows_used && data.rows_used.length) {
      rowsHtml = '<div class="rows">' +
        data.rows_used.map(function (r) { return esc(r.variety); }).join(', ') +
        '</div>';
    }
    typing.innerHTML = '<div class="who">Assistant</div><div class="body">' +
      esc(data.answer).replace(/\n/g, '<br>') + '</div>' + rowsHtml;
  } catch (err) {
    clearTimeout(timer);
    const msg = (err && err.name === 'AbortError')
      ? 'The request timed out — the connection may be slow. Please try again.'
      : 'Sorry — the server did not respond. Please try again.';
    typing.innerHTML = '<div class="who">Assistant</div><div class="body">' + msg + '</div>';
  }
  sendBtn.disabled = false;
  chat.scrollTop = chat.scrollHeight;
});

addMsg('a', '<div class="who">Assistant</div><div class="body">Ask me about salt-tolerant rice varieties — for example, which ones hold yield under salinity, how Pokkali compares to FL478, or what the Saltol marker is.</div>');
