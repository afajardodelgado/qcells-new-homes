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
const divisionsPanel = document.getElementById('divisionsPanel');
const builderInfoDiv = document.getElementById('builderInfo');
const divisionsTableDiv = document.getElementById('divisionsTable');
const buildersLayout = document.getElementById('buildersLayout');

let allBuilders = []; // Store all builders for filtering
let selectedBuilderId = null;
let buildersSortColumn = null;
let buildersSortDirection = 'asc';

function renderBuilders(builders) {
  if (!builders || builders.length === 0) {
    buildersTableDiv.innerHTML = '<p>No builders found.</p>';
    return;
  }
  
  const getSortIcon = (column) => {
    if (buildersSortColumn !== column) return '';
    return buildersSortDirection === 'asc' ? ' ▲' : ' ▼';
  };
  
  // Build table with sortable headers
  let tableHTML = `
    <div style="flex: 1; overflow-y: auto; min-height: 0;">
      <table class="builders-table">
        <thead>
          <tr>
            <th onclick="sortBuilders('Name')" style="cursor: pointer;">Name${getSortIcon('Name')}</th>
            <th onclick="sortBuilders('City')" style="cursor: pointer;">City${getSortIcon('City')}</th>
            <th onclick="sortBuilders('State')" style="cursor: pointer;">State${getSortIcon('State')}</th>
            <th onclick="sortBuilders('Website')" style="cursor: pointer;">Website${getSortIcon('Website')}</th>
          </tr>
        </thead>
        <tbody>
  `;
  
  builders.forEach(builder => {
    const website = builder.Website ? 
      `<a href="${builder.Website}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()">${builder.Website}</a>` : 
      '';
    
    const selectedClass = builder.Id === selectedBuilderId ? 'selected' : '';
    
    tableHTML += `
      <tr class="${selectedClass}" data-builder-id="${builder.Id}" onclick="selectBuilder('${builder.Id}')">
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
    </div>
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
  
  let filtered;
  if (!searchTerm) {
    filtered = [...allBuilders];
  } else {
    filtered = allBuilders.filter(builder => {
      const name = (builder.Name || '').toLowerCase();
      const city = (builder.City || '').toLowerCase();
      const state = (builder.State || '').toLowerCase();
      const website = (builder.Website || '').toLowerCase();
      
      return name.includes(searchTerm) ||
             city.includes(searchTerm) ||
             state.includes(searchTerm) ||
             website.includes(searchTerm);
    });
  }
  
  // Apply current sort if active
  if (buildersSortColumn) {
    filtered.sort((a, b) => {
      const aVal = (a[buildersSortColumn] || '').toString().toLowerCase();
      const bVal = (b[buildersSortColumn] || '').toString().toLowerCase();
      
      if (aVal < bVal) return buildersSortDirection === 'asc' ? -1 : 1;
      if (aVal > bVal) return buildersSortDirection === 'asc' ? 1 : -1;
      return 0;
    });
  }
  
  renderBuilders(filtered);
}

function sortBuilders(column) {
  // Toggle direction if same column, otherwise default to ascending
  if (buildersSortColumn === column) {
    buildersSortDirection = buildersSortDirection === 'asc' ? 'desc' : 'asc';
  } else {
    buildersSortColumn = column;
    buildersSortDirection = 'asc';
  }
  
  // Get current filtered data
  const searchTerm = builderSearchInput.value.toLowerCase().trim();
  let dataToSort = searchTerm ? 
    allBuilders.filter(builder => {
      const name = (builder.Name || '').toLowerCase();
      const city = (builder.City || '').toLowerCase();
      const state = (builder.State || '').toLowerCase();
      const website = (builder.Website || '').toLowerCase();
      
      return name.includes(searchTerm) ||
             city.includes(searchTerm) ||
             state.includes(searchTerm) ||
             website.includes(searchTerm);
    }) : [...allBuilders];
  
  // Sort
  dataToSort.sort((a, b) => {
    const aVal = (a[column] || '').toString().toLowerCase();
    const bVal = (b[column] || '').toString().toLowerCase();
    
    if (aVal < bVal) return buildersSortDirection === 'asc' ? -1 : 1;
    if (aVal > bVal) return buildersSortDirection === 'asc' ? 1 : -1;
    return 0;
  });
  
  renderBuilders(dataToSort);
}

// Make sortBuilders available globally
window.sortBuilders = sortBuilders;

function closeBuilderDetails() {
  selectedBuilderId = null;
  buildersLayout.classList.remove('split-view');
  
  // Re-render to remove selected state
  if (buildersSortColumn) {
    sortBuilders(buildersSortColumn);
  } else {
    const searchTerm = builderSearchInput.value.toLowerCase().trim();
    if (searchTerm) {
      filterBuilders();
    } else {
      renderBuilders(allBuilders);
    }
  }
}

// Make closeBuilderDetails available globally
window.closeBuilderDetails = closeBuilderDetails;

async function selectBuilder(builderId) {
  selectedBuilderId = builderId;
  
  // Show split view with animation
  buildersLayout.classList.add('split-view');
  
  // Re-render to show selected state, maintaining current sort/filter
  if (buildersSortColumn) {
    sortBuilders(buildersSortColumn);
  } else {
    const searchTerm = builderSearchInput.value.toLowerCase().trim();
    if (searchTerm) {
      filterBuilders();
    } else {
      renderBuilders(allBuilders);
    }
  }
  
  // Load divisions
  builderInfoDiv.innerHTML = '<p>Loading builder info...</p>';
  divisionsTableDiv.innerHTML = '<p>Loading divisions...</p>';
  
  try {
    const res = await fetch(`/api/sf/divisions/${builderId}`);
    const data = await res.json();
    
    if (!res.ok) throw new Error(typeof data === 'string' ? data : JSON.stringify(data));
    
    // Display builder info
    if (data.builder_info) {
      const info = data.builder_info;
      builderInfoDiv.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
          <h3 style="margin: 0;">Builder Details</h3>
          <button onclick="closeBuilderDetails()" class="btn" style="padding: 4px 12px; font-size: 12px;">✕ Close</button>
        </div>
        <div class="info-section">
          <div class="info-section-title">Builder Information</div>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">Name</span>
              <span class="info-value">${info.Name || '—'}</span>
            </div>
            
            <div class="info-item">
              <span class="info-label">Builder ID</span>
              <span class="info-value">${info.Builder_ID_Code || '—'}</span>
            </div>
            
            <div class="info-item">
              <span class="info-label">Status</span>
              <span class="info-value">${info.National_Account_Status || '—'}</span>
            </div>
            
            <div class="info-item">
              <span class="info-label">HQ Location</span>
              <span class="info-value">${info.HQ_City || ''}${info.HQ_City && info.HQ_State ? ', ' : ''}${info.HQ_State || '—'}</span>
            </div>
            
            <div class="info-item">
              <span class="info-label">Account Manager</span>
              <span class="info-value">${info.Account_Manager_Name || '—'}</span>
            </div>
            
            <div class="info-item">
              <span class="info-label">Service Territories</span>
              <span class="info-value">${info.Service_Territories || '—'}</span>
            </div>
          </div>
        </div>
      `;
    } else {
      builderInfoDiv.innerHTML = '<p>No builder information available.</p>';
    }
    
    // Display divisions table
    if (data.divisions && data.divisions.length > 0) {
      let divisionsHTML = `
        <div class="info-section">
          <div class="info-section-title">Divisions (${data.totalSize})</div>
          <table class="divisions-table">
            <thead>
              <tr>
                <th>Division Name</th>
                <th>City</th>
                <th>State</th>
              </tr>
            </thead>
            <tbody>
      `;
      
      data.divisions.forEach(div => {
        divisionsHTML += `
          <tr>
            <td>${div.Division_Name || '—'}</td>
            <td>${div.Division_City || '—'}</td>
            <td>${div.Division_State || '—'}</td>
          </tr>
        `;
      });
      
      divisionsHTML += `
            </tbody>
          </table>
        </div>
      `;
      
      divisionsTableDiv.innerHTML = divisionsHTML;
    } else {
      divisionsTableDiv.innerHTML = `
        <div class="info-section">
          <div class="info-section-title">Divisions</div>
          <p style="color: var(--color-muted); margin-top: 12px;">No divisions found for this builder.</p>
        </div>
      `;
    }
  } catch (err) {
    builderInfoDiv.innerHTML = `<p class="error">Error loading builder info: ${err.message}</p>`;
    divisionsTableDiv.innerHTML = '';
  }
}

// Make selectBuilder available globally
window.selectBuilder = selectBuilder;

loadBuildersBtn?.addEventListener('click', loadBuilders);
builderSearchInput?.addEventListener('input', filterBuilders);

// Communities functionality
const loadCommunitiesBtn = document.getElementById('loadCommunities');
const communitiesTableDiv = document.getElementById('communitiesTable');
const communitySearchInput = document.getElementById('communitySearch');

let allCommunities = [];
let communitiesSortColumn = null;
let communitiesSortDirection = 'asc';

function renderCommunities(communities) {
  if (!communities || communities.length === 0) {
    communitiesTableDiv.innerHTML = '<p>No communities found.</p>';
    return;
  }
  
  const getSortIcon = (column) => {
    if (communitiesSortColumn !== column) return '';
    return communitiesSortDirection === 'asc' ? ' ▲' : ' ▼';
  };
  
  // Build table with sortable headers
  let tableHTML = `
    <div style="flex: 1; overflow-y: auto; min-height: 0;">
      <table class="builders-table">
        <thead>
          <tr>
            <th onclick="sortCommunities('Builder_Name')" style="cursor: pointer;">Builder Name${getSortIcon('Builder_Name')}</th>
            <th onclick="sortCommunities('Builder_ID_Code')" style="cursor: pointer;">Builder ID${getSortIcon('Builder_ID_Code')}</th>
            <th onclick="sortCommunities('National_Account_Status')" style="cursor: pointer;">Status${getSortIcon('National_Account_Status')}</th>
            <th onclick="sortCommunities('Service_Territories')" style="cursor: pointer;">Service Territories${getSortIcon('Service_Territories')}</th>
            <th onclick="sortCommunities('Account_Manager_Name')" style="cursor: pointer;">Account Manager${getSortIcon('Account_Manager_Name')}</th>
            <th onclick="sortCommunities('HQ_City')" style="cursor: pointer;">HQ City${getSortIcon('HQ_City')}</th>
            <th onclick="sortCommunities('HQ_State')" style="cursor: pointer;">HQ State${getSortIcon('HQ_State')}</th>
            <th onclick="sortCommunities('Division_Name')" style="cursor: pointer;">Division Name${getSortIcon('Division_Name')}</th>
            <th onclick="sortCommunities('Division_City')" style="cursor: pointer;">Division City${getSortIcon('Division_City')}</th>
            <th onclick="sortCommunities('Division_State')" style="cursor: pointer;">Division State${getSortIcon('Division_State')}</th>
          </tr>
        </thead>
        <tbody>
  `;
  
  communities.forEach(community => {
    tableHTML += `
      <tr>
        <td>${community.Builder_Name || '—'}</td>
        <td>${community.Builder_ID_Code || '—'}</td>
        <td>${community.National_Account_Status || '—'}</td>
        <td>${community.Service_Territories || '—'}</td>
        <td>${community.Account_Manager_Name || '—'}</td>
        <td>${community.HQ_City || '—'}</td>
        <td>${community.HQ_State || '—'}</td>
        <td>${community.Division_Name || '—'}</td>
        <td>${community.Division_City || '—'}</td>
        <td>${community.Division_State || '—'}</td>
      </tr>
    `;
  });
  
  tableHTML += `
        </tbody>
      </table>
    </div>
    <p class="table-footer">Showing ${communities.length} of ${allCommunities.length} communities</p>
  `;
  
  communitiesTableDiv.innerHTML = tableHTML;
}

async function loadCommunities() {
  communitiesTableDiv.innerHTML = '<p>Loading communities...</p>';
  try {
    const res = await fetch('/api/sf/communities');
    const data = await res.json();
    
    if (!res.ok) throw new Error(typeof data === 'string' ? data : JSON.stringify(data));
    
    allCommunities = data.communities || [];
    renderCommunities(allCommunities);
  } catch (err) {
    communitiesTableDiv.innerHTML = `<p class="error">Error: ${err.message}</p>`;
  }
}

function filterCommunities() {
  const searchTerm = communitySearchInput.value.toLowerCase().trim();
  
  let filtered;
  if (!searchTerm) {
    filtered = [...allCommunities];
  } else {
    filtered = allCommunities.filter(community => {
      const builderName = (community.Builder_Name || '').toLowerCase();
      const builderID = (community.Builder_ID_Code || '').toLowerCase();
      const status = (community.National_Account_Status || '').toLowerCase();
      const territories = (community.Service_Territories || '').toLowerCase();
      const accountMgr = (community.Account_Manager_Name || '').toLowerCase();
      const hqCity = (community.HQ_City || '').toLowerCase();
      const hqState = (community.HQ_State || '').toLowerCase();
      const divName = (community.Division_Name || '').toLowerCase();
      const divCity = (community.Division_City || '').toLowerCase();
      const divState = (community.Division_State || '').toLowerCase();
      
      return builderName.includes(searchTerm) ||
             builderID.includes(searchTerm) ||
             status.includes(searchTerm) ||
             territories.includes(searchTerm) ||
             accountMgr.includes(searchTerm) ||
             hqCity.includes(searchTerm) ||
             hqState.includes(searchTerm) ||
             divName.includes(searchTerm) ||
             divCity.includes(searchTerm) ||
             divState.includes(searchTerm);
    });
  }
  
  // Apply current sort if active
  if (communitiesSortColumn) {
    filtered.sort((a, b) => {
      const aVal = (a[communitiesSortColumn] || '').toString().toLowerCase();
      const bVal = (b[communitiesSortColumn] || '').toString().toLowerCase();
      
      if (aVal < bVal) return communitiesSortDirection === 'asc' ? -1 : 1;
      if (aVal > bVal) return communitiesSortDirection === 'asc' ? 1 : -1;
      return 0;
    });
  }
  
  renderCommunities(filtered);
}

function sortCommunities(column) {
  // Toggle direction if same column, otherwise default to ascending
  if (communitiesSortColumn === column) {
    communitiesSortDirection = communitiesSortDirection === 'asc' ? 'desc' : 'asc';
  } else {
    communitiesSortColumn = column;
    communitiesSortDirection = 'asc';
  }
  
  // Get current filtered data
  const searchTerm = communitySearchInput.value.toLowerCase().trim();
  let dataToSort = searchTerm ? 
    allCommunities.filter(community => {
      const builderName = (community.Builder_Name || '').toLowerCase();
      const builderID = (community.Builder_ID_Code || '').toLowerCase();
      const status = (community.National_Account_Status || '').toLowerCase();
      const territories = (community.Service_Territories || '').toLowerCase();
      const accountMgr = (community.Account_Manager_Name || '').toLowerCase();
      const hqCity = (community.HQ_City || '').toLowerCase();
      const hqState = (community.HQ_State || '').toLowerCase();
      const divName = (community.Division_Name || '').toLowerCase();
      const divCity = (community.Division_City || '').toLowerCase();
      const divState = (community.Division_State || '').toLowerCase();
      
      return builderName.includes(searchTerm) ||
             builderID.includes(searchTerm) ||
             status.includes(searchTerm) ||
             territories.includes(searchTerm) ||
             accountMgr.includes(searchTerm) ||
             hqCity.includes(searchTerm) ||
             hqState.includes(searchTerm) ||
             divName.includes(searchTerm) ||
             divCity.includes(searchTerm) ||
             divState.includes(searchTerm);
    }) : [...allCommunities];
  
  // Sort
  dataToSort.sort((a, b) => {
    const aVal = (a[column] || '').toString().toLowerCase();
    const bVal = (b[column] || '').toString().toLowerCase();
    
    if (aVal < bVal) return communitiesSortDirection === 'asc' ? -1 : 1;
    if (aVal > bVal) return communitiesSortDirection === 'asc' ? 1 : -1;
    return 0;
  });
  
  renderCommunities(dataToSort);
}

// Make sortCommunities available globally
window.sortCommunities = sortCommunities;

loadCommunitiesBtn?.addEventListener('click', loadCommunities);
communitySearchInput?.addEventListener('input', filterCommunities);

// Navigation
const navItems = document.querySelectorAll('.nav-item');
const sections = {
  builders: document.getElementById('section-builders'),
  communities: document.getElementById('section-communities'),
  'new-homes': document.getElementById('section-new-homes'),
  pricing: document.getElementById('section-pricing'),
  marketing: document.getElementById('section-marketing'),
  training: document.getElementById('section-training'),
  support: document.getElementById('section-support'),
  homes: document.getElementById('section-homes')
};

navItems.forEach(item => {
  item.addEventListener('click', () => {
    navItems.forEach(n => n.classList.remove('active'));
    item.classList.add('active');

    const target = item.getAttribute('data-section');
    Object.values(sections).forEach(s => s.classList.remove('visible'));
    sections[target]?.classList.add('visible');
    
    // Auto-load data when tabs are clicked
    if (target === 'builders') {
      loadBuilders();
    } else if (target === 'communities') {
      loadCommunities();
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
