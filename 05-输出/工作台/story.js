const params = new URLSearchParams(location.search);
const STORY_URL = `stories/${params.get('story') || 'ch01'}.json`;
const state = { data: null, current: null, path: [], lastAct: 0 };

async function load() {
  const res = await fetch(STORY_URL);
  if (!res.ok) throw new Error(`无法加载 ${STORY_URL}`);
  state.data = await res.json();
  state.current = state.data.start;
  document.getElementById('title').textContent = state.data.title;
  document.getElementById('subtitle').textContent = state.data.subtitle || '';
  render();
}

function render() {
  const scene = state.data.scenes[state.current];
  if (!scene) throw new Error(`场景不存在：${state.current}`);
  const sceneEl = document.getElementById('scene');
  sceneEl.innerHTML = '';

  if (scene.title) {
    const h2 = document.createElement('h2');
    h2.textContent = scene.title;
    sceneEl.appendChild(h2);
  }

  const text = document.createElement('p');
  text.className = 'text';
  text.textContent = scene.text;
  sceneEl.appendChild(text);

  if (scene.card) renderComparison(sceneEl);

  const choicesEl = document.getElementById('choices');
  choicesEl.innerHTML = '';

  if (scene.choices) {
    scene.choices.forEach(choice => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'choice';
      btn.textContent = choice.label;
      btn.addEventListener('click', () => go(choice.next, choice.label, scene.act));
      choicesEl.appendChild(btn);
    });
  } else if (scene.next) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'continue';
    btn.textContent = scene.title === '历史揭晓' ? '进入下一幕' : '继续';
    btn.addEventListener('click', () => go(scene.next));
    choicesEl.appendChild(btn);
  }

  if (scene.card) {
    const share = document.createElement('div');
    share.className = 'share';
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'share-btn';
    btn.textContent = '复制分享文案';
    btn.addEventListener('click', () => copyText(buildShareText()));
    share.appendChild(btn);
    choicesEl.appendChild(share);
  }

  if (scene.act) state.lastAct = scene.act;
  const progress = document.getElementById('progress');
  progress.textContent = scene.act
    ? `第 ${scene.act} 幕 / 3`
    : (scene.card ? '完成' : (state.lastAct ? `第 ${state.lastAct} 幕 / 3` : ''));
  const fill = document.getElementById('progress-fill');
  fill.style.width = `${(state.lastAct / 3) * 100}%`;

  const card = document.getElementById('card');
  if (scene.card) {
    card.textContent = `卡片：${scene.card} ${scene.cardTitle || ''}`;
    card.classList.add('visible');
  } else {
    card.textContent = '';
    card.classList.remove('visible');
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
  sceneEl.setAttribute('tabindex', '-1');
  sceneEl.focus({ preventScroll: true });
}

function renderComparison(root) {
  if (!state.path.length) return;
  const rows = [...state.path].sort((a, b) => a.act - b.act);
  const wrap = document.createElement('div');
  wrap.className = 'compare';
  const h3 = document.createElement('h3');
  h3.textContent = '你的选择 vs 历史';
  wrap.appendChild(h3);

  const table = document.createElement('table');
  const thead = document.createElement('thead');
  thead.innerHTML = '<tr><th>幕</th><th>你的选择</th><th>历史</th></tr>';
  table.appendChild(thead);

  const tbody = document.createElement('tbody');
  rows.forEach(item => {
    const history = state.data.history?.[String(item.act)] || '—';
    const match = item.label.trim().charAt(0) === history.trim().charAt(0);
    const tr = document.createElement('tr');
    const act = document.createElement('td');
    act.textContent = `第 ${item.act} 幕`;
    const user = document.createElement('td');
    user.textContent = item.label;
    const hist = document.createElement('td');
    hist.textContent = history;
    hist.className = match ? 'match' : 'differ';
    hist.title = match ? '与历史一致' : '与历史不同';
    tr.append(act, user, hist);
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
  wrap.appendChild(table);
  root.appendChild(wrap);
}

function buildShareText() {
  const lines = [`我在《${state.data.title}》做了三个选择：`];
  const rows = [...state.path].sort((a, b) => a.act - b.act);
  rows.forEach(item => {
    const history = state.data.history?.[String(item.act)] || '—';
    lines.push(`${item.act}. 我选 ${item.label}；历史选 ${history}`);
  });
  lines.push('');
  lines.push('最扎心的一句：最好的税，是让人感觉不到；最好的财政，是让人先赚到钱。');
  lines.push('https://justinjchen-cornell.github.io/Ledger-of-Empires/');
  return lines.join('\n');
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    showToast('已复制分享文案');
  } catch (error) {
    const area = document.createElement('textarea');
    area.value = text;
    area.style.position = 'fixed';
    area.style.opacity = '0';
    document.body.appendChild(area);
    area.select();
    document.execCommand('copy');
    area.remove();
    showToast('已复制分享文案');
  }
}

let toastTimer;
function showToast(message) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2000);
}

function go(next, label, act) {
  if (label) state.path.push({ from: state.current, act, label });
  state.current = next;
  render();
}

document.getElementById('restart').addEventListener('click', () => {
  state.current = state.data.start;
  state.path = [];
  state.lastAct = 0;
  render();
});

load().catch(error => {
  document.getElementById('scene').innerHTML = `<p class="error">${error.message}</p><p class="text">如果是本地打开，请用 <code>python -m http.server</code>，不要直接双击 HTML。</p>`;
});
