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

// Builders functionality
const loadBuildersBtn = document.getElementById('loadBuilders');
const buildersTableDiv = document.getElementById('buildersTable');
const builderSearchInput = document.getElementById('builderSearch');

let allBuilders = []; // Store all builders for filtering

function renderBuilders(builders) {
  if (!builders || builders.length === 0) {
    buildersTableDiv.innerHTML = '<p>No builders found.</p>';
    return;
  }
  
  // Build table
  let tableHTML = `
    <table class="builders-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>City</th>
          <th>State</th>
          <th>Website</th>
        </tr>
      </thead>
      <tbody>
  `;
  
  builders.forEach(builder => {
    const website = builder.Website ? 
      `<a href="${builder.Website}" target="_blank" rel="noopener noreferrer">${builder.Website}</a>` : 
      '';
    
    tableHTML += `
      <tr>
        <td>${builder.Name || ''}</td>
        <td>${builder.City || ''}</td>
        <td>${builder.State || ''}</td>
        <td>${website}</td>
      </tr>
    `;
  });
  
  tableHTML += `
      </tbody>
    </table>
    <p class="table-footer">Showing ${builders.length} of ${allBuilders.length} builders</p>
  `;
  
  buildersTableDiv.innerHTML = tableHTML;
}

async function loadBuilders() {
  buildersTableDiv.innerHTML = '<p>Loading builders...</p>';
  try {
    const res = await fetch('/api/sf/builders');
    const data = await res.json();
    
    if (!res.ok) throw new Error(typeof data === 'string' ? data : JSON.stringify(data));
    
    allBuilders = data.builders || [];
    renderBuilders(allBuilders);
  } catch (err) {
    buildersTableDiv.innerHTML = `<p class="error">Error: ${err.message}</p>`;
  }
}

function filterBuilders() {
  const searchTerm = builderSearchInput.value.toLowerCase().trim();
  
  if (!searchTerm) {
    renderBuilders(allBuilders);
    return;
  }
  
  const filtered = allBuilders.filter(builder => {
    const name = (builder.Name || '').toLowerCase();
    const city = (builder.City || '').toLowerCase();
    const state = (builder.State || '').toLowerCase();
    const website = (builder.Website || '').toLowerCase();
    
    return name.includes(searchTerm) ||
           city.includes(searchTerm) ||
           state.includes(searchTerm) ||
           website.includes(searchTerm);
  });
  
  renderBuilders(filtered);
}

loadBuildersBtn?.addEventListener('click', loadBuilders);
builderSearchInput?.addEventListener('input', filterBuilders);

// Navigation
const navItems = document.querySelectorAll('.nav-item');
const sections = {
  homes: document.getElementById('section-homes'),
  builders: document.getElementById('section-builders'),
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
    
    // Auto-load builders when Builders tab is clicked
    if (target === 'builders') {
      loadBuilders();
    }
  });
});

// SOQL Query functionality
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

// Auto-load builders on page load (since it's the default active tab)
if (sections.builders?.classList.contains('visible')) {
  loadBuilders();
}
