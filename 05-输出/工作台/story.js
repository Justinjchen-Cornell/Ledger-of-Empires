const params = new URLSearchParams(location.search);
const STORY_URL = `stories/${params.get('story') || 'ch01'}.json`;
const state = { data: null, current: null, path: [] };

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

  if (scene.card && state.path.length) {
    const recap = document.createElement('div');
    recap.className = 'recap';
    const title = document.createElement('strong');
    title.textContent = '你的选择';
    recap.appendChild(title);
    const ol = document.createElement('ol');
    state.path.forEach(item => {
      const li = document.createElement('li');
      li.textContent = item.label;
      ol.appendChild(li);
    });
    recap.appendChild(ol);
    sceneEl.appendChild(recap);
  }

  const choicesEl = document.getElementById('choices');
  choicesEl.innerHTML = '';

  if (scene.choices) {
    scene.choices.forEach(choice => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'choice';
      btn.textContent = choice.label;
      btn.addEventListener('click', () => go(choice.next, choice.label));
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

  const progress = document.getElementById('progress');
  progress.textContent = scene.act ? `第 ${scene.act} 幕 / 3` : '';

  const card = document.getElementById('card');
  if (scene.card) {
    card.textContent = `卡片：${scene.card} ${scene.cardTitle || ''}`;
    card.classList.add('visible');
  } else {
    card.textContent = '';
    card.classList.remove('visible');
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function go(next, label) {
  if (label) state.path.push({ from: state.current, label });
  state.current = next;
  render();
}

document.getElementById('restart').addEventListener('click', () => {
  state.current = state.data.start;
  state.path = [];
  render();
});

load().catch(error => {
  document.getElementById('scene').innerHTML = `<p class="error">${error.message}</p>`;
});
