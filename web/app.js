// Simple SPA-like navigation and Salesforce query demo

// Global error handler - logs to backend
window.addEventListener('error', async (event) => {
  const errorData = {
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    stack: event.error?.stack || 'No stack trace',
    timestamp: new Date().toISOString(),
    userAgent: navigator.userAgent
  };

  try {
    await fetch('/api/log-error', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(errorData)
    });
  } catch (err) {
    console.error('Failed to log error to backend:', err);
  }
});

// Unhandled promise rejection handler
window.addEventListener('unhandledrejection', async (event) => {
  const errorData = {
    message: event.reason?.message || String(event.reason),
    stack: event.reason?.stack || 'No stack trace',
    timestamp: new Date().toISOString(),
    userAgent: navigator.userAgent,
    type: 'unhandledrejection'
  };

  try {
    await fetch('/api/log-error', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(errorData)
    });
  } catch (err) {
    console.error('Failed to log promise rejection to backend:', err);
  }
});

const navItems = document.querySelectorAll('.nav-item');
const sections = {
  homes: document.getElementById('section-homes'),
  pricing: document.getElementById('section-pricing'),
  marketing: document.getElementById('section-marketing'),
  training: document.getElementById('section-training'),
  support: document.getElementById('section-support')
};

navItems.forEach(item => {
  item.addEventListener('click', () => {
    navItems.forEach(n => n.classList.remove('active'));
    item.classList.add('active');

    const target = item.getAttribute('data-section');
    Object.values(sections).forEach(s => s.classList.remove('visible'));
    sections[target]?.classList.add('visible');
  });
});

const soqlInput = document.getElementById('soql');
const runBtn = document.getElementById('runQuery');
const output = document.getElementById('output');

async function runQuery() {
  const soql = soqlInput.value.trim();
  output.textContent = 'Running...';
  try {
    const res = await fetch('/api/sf/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ soql })
    });
    const text = await res.text();
    let data;
    try { data = JSON.parse(text); } catch { data = text; }
    if (!res.ok) throw new Error(typeof data === 'string' ? data : JSON.stringify(data, null, 2));
    output.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    output.textContent = `Error\n${err.message}`;
  }
}

runBtn?.addEventListener('click', runQuery);
