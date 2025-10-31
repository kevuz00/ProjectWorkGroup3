const accessLogsKey = "accessLogs";
let accessLogs = JSON.parse(localStorage.getItem(accessLogsKey)) || [];
let chartInstance = null;
let injectionChartInstance = null;

// NEW: aggregate accesses per day (using timestampISO when available)
function aggregateByDay() {
    const map = {};
    accessLogs.forEach(log => {
        const iso = log.timestampISO || log.timestamp; // fallback
        const d = new Date(iso);
        if (isNaN(d)) return;
        // use YYYY-MM-DD as key
        const key = d.toISOString().slice(0,10);
        map[key] = (map[key] || 0) + 1;
    });
    // return sorted arrays
    const keys = Object.keys(map).sort();
    const labels = keys;
    const data = keys.map(k => map[k]);
    return { labels, data };
}

function getChartColors() {
    const s = getComputedStyle(document.documentElement);
    return {
        line: s.getPropertyValue('--chart-line').trim() || 'rgba(167,139,250,0.95)',
        fillStart: s.getPropertyValue('--chart-fill-start').trim() || 'rgba(167,139,250,0.85)',
        fillEnd: s.getPropertyValue('--chart-fill-end').trim() || 'rgba(167,139,250,0.12)',
        injLine: s.getPropertyValue('--chart-inj-line').trim() || 'rgba(255,159,64,0.95)',
        injFillStart: s.getPropertyValue('--chart-inj-fill-start').trim() || 'rgba(255,159,64,0.85)',
        injFillEnd: s.getPropertyValue('--chart-inj-fill-end').trim() || 'rgba(255,159,64,0.12)',
        grid: s.getPropertyValue('--chart-grid').trim() || 'rgba(255,255,255,0.06)',
        tick: s.getPropertyValue('--chart-tick').trim() || 'rgba(255,255,255,0.92)'
    };
}

// helper: build vertical gradient using actual canvas height
function buildGradient(ctx, colorStart, colorEnd) {
    const h = Math.max(ctx.canvas.clientHeight || 120, 80);
    const grad = ctx.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, colorStart);
    grad.addColorStop(1, colorEnd);
    return grad;
}

function renderChart() {
    const canvas = document.getElementById('accessChart');
    const ctx = canvas.getContext('2d');
    const agg = aggregateByDay();
    const cols = getChartColors();

    const gradient = buildGradient(ctx, cols.fillStart, cols.fillEnd);

    const config = {
        type: 'line',
        data: {
            labels: agg.labels,
            datasets: [{
                label: 'Accessi',
                data: agg.data,
                fill: true,
                backgroundColor: gradient,
                borderColor: cols.line,
                borderWidth: 2.8,
                pointRadius: 3.5,
                pointHoverRadius: 6,
                pointBorderWidth: 1,
                tension: 0.36,
                cubicInterpolationMode: 'monotone'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 700, easing: 'easeOutQuart' },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(10,10,12,0.92)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgba(255,255,255,0.06)',
                    borderWidth: 1,
                    mode: 'index',
                    intersect: false,
                    padding: 8
                }
            },
            layout: { padding: { top: 6, bottom: 6, left: 4, right: 8 } },
            scales: {
                x: {
                    grid: { color: cols.grid },
                    ticks: { color: cols.tick, maxRotation: 0, autoSkip: true, maxTicksLimit: 6 }
                },
                y: {
                    beginAtZero: true,
                    grid: { color: cols.grid },
                    ticks: { color: cols.tick, precision: 0 }
                }
            },
            interaction: { mode: 'index', intersect: false },
            elements: {
                point: { backgroundColor: cols.line, hoverBackgroundColor: '#fff', hoverBorderColor: cols.line }
            }
        }
    };

    // destroy & recreate to guarantee correct sizing and gradients
    if (chartInstance) {
        try { chartInstance.destroy(); } catch (e) { /* ignore */ }
        chartInstance = null;
    }
    chartInstance = new Chart(ctx, config);
}

function escapeHtml(text) {
    if (!text) return '';
    return text.toString().replace(/[&<>"'`=\/]/g, function (s) {
        return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;','/':'&#x2F;','=':'&#x3D;','`':'&#x60;'})[s];
    });
}

function analyzeIPs() {
    const ipMap = {}; // ip -> { total, failed, success, lastSeen }
    accessLogs.forEach(log => {
        const ip = log.ip || 'unknown';
        ipMap[ip] = ipMap[ip] || { total:0, failed:0, success:0, lastSeen: null };
        ipMap[ip].total++;
        if (log.status === 'Failed') ipMap[ip].failed++;
        if (log.status === 'Success') ipMap[ip].success++;
        ipMap[ip].lastSeen = log.timestamp;
    });
    return ipMap;
}

function renderAnalysis() {
    const ipMap = analyzeIPs();
    const suspicious = [];
    for (const ip in ipMap) {
        const info = ipMap[ip];
        const failRate = info.total ? (info.failed / info.total) : 0;
        if (info.failed >= 3 || (info.total >=3 && failRate > 0.7)) {
            suspicious.push({ ip, ...info, failRate });
        }
    }
    suspicious.sort((a,b) => b.failed - a.failed);

    const suspiciousList = document.getElementById('suspiciousList');
    suspiciousList.innerHTML = suspicious.length ? suspicious.map(s => `
        <div class="ip-card">
            <div class="ip-address">${escapeHtml(s.ip)}</div>
            <div class="ip-meta">Tot: ${s.total} • Falliti: ${s.failed} • Ultimo: ${escapeHtml(s.lastSeen)}</div>
        </div>
    `).join('') : '<div class="muted">Nessun IP sospetto rilevato</div>';

    const total = accessLogs.length;
    const success = accessLogs.filter(l => l.status==='Success').length;
    const failed = accessLogs.filter(l => l.status==='Failed').length;
    const analysisBox = document.getElementById('analysisBox');
    analysisBox.innerHTML = `
        <div>Totale tentativi: <strong>${total}</strong></div>
        <div>Successi: <strong>${success}</strong> • Falliti: <strong>${failed}</strong></div>
        <div>Tasso di successo: <strong>${total?Math.round((success/total)*100):0}%</strong></div>
        <div class="mt-2">IP sospetti: <strong>${suspicious.length}</strong></div>
    `;
}

// --- injection detectors (if not present) ---
function detectInjectionTypes(text) {
    const t = (text||'').toString();
    const types = new Set();
    if (!t) return types;
    const lower = t.toLowerCase();

    // XSS: script tags, event handlers, javascript: URIs, encoded < signs
    if (/<\s*script|<\s*img|on\w+\s*=|javascript:|%3c|<\s*svg|<\s*iframe/i.test(t)) types.add('XSS');

    // SQLi: SQL keywords, comment sequences, ' or 1=1 patterns
    if (/\b(select|union|insert|update|delete|drop|alter|create|into)\b/i.test(t) ||
        /('|--|#|\/\*|\*\/|\bor\s+1=1\b)/i.test(t)) types.add('SQLi');

    // Command injection: shell meta-chars or common commands
    if (/[;&|`$()<>]/.test(t) ||
        /\b(wget|curl|nc|ncat|bash|sh|cmd|powershell|rm|cat)\b/i.test(t)) types.add('Command');

    // Directory traversal
    if (/\.\.\/|\.\.\\/.test(t)) types.add('Traversal');

    // LDAP-like suspicious characters (simple heuristic)
    if (/[()|&]/.test(t) && /[=*]/.test(t)) types.add('LDAP');

    return types;
}

function analyzeInjections() {
    const map = {}; // type -> { count, examples: Set }
    accessLogs.forEach(log => {
        // check username and userAgent (and ip) for suspicious payloads
        const fields = [log.username, log.ua, log.ip, log.timestamp, log.timestampISO];
        fields.forEach(f => {
            const types = detectInjectionTypes(f);
            types.forEach(type => {
                if (!map[type]) map[type] = { count:0, examples: new Set() };
                map[type].count++;
                map[type].examples.add((f||'').toString().slice(0,180));
            });
        });
    });
    // convert sets to arrays and ensure all expected types exist
    const expected = ['XSS','SQLi','Command','Traversal','LDAP'];
    expected.forEach(k => { if(!map[k]) map[k]={count:0,examples:new Set()}; });

    // transform examples to arrays
    for (const k in map) {
        map[k].examples = Array.from(map[k].examples).slice(0,5);
    }
    return map;
}

// aggregate injection events per day (for line chart)
function aggregateInjectionsByDay() {
    const map = {};
    accessLogs.forEach(log => {
        // if any injection detected in this log
        const combined = `${log.username||''} ${log.ua||''} ${log.ip||''}`;
        const types = detectInjectionTypes(combined);
        if (types.size === 0) return;
        const iso = log.timestampISO || log.timestamp;
        const d = new Date(iso);
        if (isNaN(d)) return;
        const key = d.toISOString().slice(0,10);
        map[key] = (map[key] || 0) + 1;
    });
    const keys = Object.keys(map).sort();
    return { labels: keys, data: keys.map(k => map[k]) };
}

// render injection chart as line chart (same style as access chart)
function renderInjectionChart() {
    const canvas = document.getElementById('injectionChart');
    const ctx = canvas.getContext('2d');
    const agg = aggregateInjectionsByDay();
    const cols = getChartColors();

    const gradient = buildGradient(ctx, cols.injFillStart, cols.injFillEnd);

    const config = {
        type: 'line',
        data: {
            labels: agg.labels,
            datasets: [{
                label: 'Injection events',
                data: agg.data,
                fill: true,
                backgroundColor: gradient,
                borderColor: cols.injLine,
                borderWidth: 2.6,
                pointRadius: 3.5,
                pointHoverRadius: 6,
                pointBorderWidth: 1,
                tension: 0.36,
                cubicInterpolationMode: 'monotone'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 700, easing: 'easeOutQuart' },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(10,10,12,0.92)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgba(255,255,255,0.06)',
                    borderWidth: 1,
                    mode: 'index',
                    intersect: false,
                    padding: 8
                }
            },
            layout: { padding: { top: 6, bottom: 6, left: 4, right: 8 } },
            scales: {
                x: { grid: { color: cols.grid }, ticks: { color: cols.tick, maxRotation: 0, autoSkip: true, maxTicksLimit: 5 } },
                y: { beginAtZero: true, grid: { color: cols.grid }, ticks: { color: cols.tick, precision: 0 } }
            },
            interaction: { mode: 'index', intersect: false },
            elements: { point: { backgroundColor: cols.injLine, hoverBackgroundColor: '#fff' } }
        }
    };

    if (injectionChartInstance) {
        try { injectionChartInstance.destroy(); } catch (e) { /* ignore */ }
        injectionChartInstance = null;
    }
    injectionChartInstance = new Chart(ctx, config);
}

// render full report (table-like list) with detected injection types per entry
function renderReport() {
    const container = document.getElementById('reportList');
    if (!container) return;
    if (!accessLogs || accessLogs.length === 0) {
        container.innerHTML = '<div class="muted">Nessun dato</div>';
        return;
    }
    const rows = accessLogs.slice().reverse().map(log => {
        const combined = `${log.username||''} ${log.ua||''} ${log.ip||''}`;
        const inj = Array.from(detectInjectionTypes(combined)).join(', ') || '-';
        const ts = escapeHtml(log.timestamp || '');
        return `<div class="report-row">
            <div class="report-row-header"><strong>${escapeHtml(log.username||'')}</strong> — ${escapeHtml(log.status||'')}</div>
            <div class="report-row-body">
                <div><small>${ts} • IP: ${escapeHtml(log.ip||'unknown')}</small></div>
                <div>UserAgent: <span class="muted">${escapeHtml(log.ua||'')}</span></div>
                <div>Tipi di injection: <strong>${escapeHtml(inj)}</strong></div>
            </div>
        </div>`;
    }).join('');
    container.innerHTML = `<div class="report-scroll">${rows}</div>`;
}

// basic detectors (heuristics)
function detectInjectionTypes(text) {
    const t = (text||'').toString();
    const types = new Set();

    if (!t) return types;
    const lower = t.toLowerCase();

    // XSS: script tags, event handlers, javascript: URIs, encoded < signs
    if (/<\s*script|<\s*img|on\w+\s*=|javascript:|%3c|<\s*svg|<\s*iframe/i.test(t)) types.add('XSS');

    // SQLi: SQL keywords, comment sequences, ' or 1=1 patterns
    if (/\b(select|union|insert|update|delete|drop|alter|create|into)\b/i.test(t) ||
        /('|--|#|\/\*|\*\/|\bor\s+1=1\b)/i.test(t)) types.add('SQLi');

    // Command injection: shell meta-chars or common commands
    if (/[;&|`$()<>]/.test(t) ||
        /\b(wget|curl|nc|ncat|bash|sh|cmd|powershell|rm|cat)\b/i.test(t)) types.add('Command');

    // Directory traversal
    if (/\.\.\/|\.\.\\/.test(t)) types.add('Traversal');

    // LDAP-like suspicious characters (simple heuristic)
    if (/[()|&]/.test(t) && /[=*]/.test(t)) types.add('LDAP');

    return types;
}

function analyzeInjections() {
    const map = {}; // type -> { count, examples: Set }
    accessLogs.forEach(log => {
        // check username and userAgent (and ip) for suspicious payloads
        const fields = [log.username, log.ua, log.ip, log.timestamp, log.timestampISO];
        fields.forEach(f => {
            const types = detectInjectionTypes(f);
            types.forEach(type => {
                if (!map[type]) map[type] = { count:0, examples: new Set() };
                map[type].count++;
                map[type].examples.add((f||'').toString().slice(0,180));
            });
        });
    });
    // convert sets to arrays and ensure all expected types exist
    const expected = ['XSS','SQLi','Command','Traversal','LDAP'];
    expected.forEach(k => { if(!map[k]) map[k]={count:0,examples:new Set()}; });

    // transform examples to arrays
    for (const k in map) {
        map[k].examples = Array.from(map[k].examples).slice(0,5);
    }
    return map;
}

// aggregate injection events per day (for line chart)
function aggregateInjectionsByDay() {
    const map = {};
    accessLogs.forEach(log => {
        // if any injection detected in this log
        const combined = `${log.username||''} ${log.ua||''} ${log.ip||''}`;
        const types = detectInjectionTypes(combined);
        if (types.size === 0) return;
        const iso = log.timestampISO || log.timestamp;
        const d = new Date(iso);
        if (isNaN(d)) return;
        const key = d.toISOString().slice(0,10);
        map[key] = (map[key] || 0) + 1;
    });
    const keys = Object.keys(map).sort();
    return { labels: keys, data: keys.map(k => map[k]) };
}

// render injection chart as line chart (same style as access chart)
function renderInjectionChart() {
    const canvas = document.getElementById('injectionChart');
    const ctx = canvas.getContext('2d');
    const agg = aggregateInjectionsByDay();
    const cols = getChartColors();

    const gradient = buildGradient(ctx, cols.injFillStart, cols.injFillEnd);

    const config = {
        type: 'line',
        data: {
            labels: agg.labels,
            datasets: [{
                label: 'Injection events',
                data: agg.data,
                fill: true,
                backgroundColor: gradient,
                borderColor: cols.injLine,
                borderWidth: 2.6,
                pointRadius: 3.5,
                pointHoverRadius: 6,
                pointBorderWidth: 1,
                tension: 0.36,
                cubicInterpolationMode: 'monotone'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 700, easing: 'easeOutQuart' },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(10,10,12,0.92)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgba(255,255,255,0.06)',
                    borderWidth: 1,
                    mode: 'index',
                    intersect: false,
                    padding: 8
                }
            },
            layout: { padding: { top: 6, bottom: 6, left: 4, right: 8 } },
            scales: {
                x: { grid: { color: cols.grid }, ticks: { color: cols.tick, maxRotation: 0, autoSkip: true, maxTicksLimit: 5 } },
                y: { beginAtZero: true, grid: { color: cols.grid }, ticks: { color: cols.tick, precision: 0 } }
            },
            interaction: { mode: 'index', intersect: false },
            elements: { point: { backgroundColor: cols.injLine, hoverBackgroundColor: '#fff' } }
        }
    };

    if (injectionChartInstance) {
        try { injectionChartInstance.destroy(); } catch (e) { /* ignore */ }
        injectionChartInstance = null;
    }
    injectionChartInstance = new Chart(ctx, config);
}

// render full report (table-like list) with detected injection types per entry
function renderReport() {
    const container = document.getElementById('reportList');
    if (!container) return;
    if (!accessLogs || accessLogs.length === 0) {
        container.innerHTML = '<div class="muted">Nessun dato</div>';
        return;
    }
    const rows = accessLogs.slice().reverse().map(log => {
        const combined = `${log.username||''} ${log.ua||''} ${log.ip||''}`;
        const inj = Array.from(detectInjectionTypes(combined)).join(', ') || '-';
        const ts = escapeHtml(log.timestamp || '');
        return `<div class="report-row">
            <div class="report-row-header"><strong>${escapeHtml(log.username||'')}</strong> — ${escapeHtml(log.status||'')}</div>
            <div class="report-row-body">
                <div><small>${ts} • IP: ${escapeHtml(log.ip||'unknown')}</small></div>
                <div>UserAgent: <span class="muted">${escapeHtml(log.ua||'')}</span></div>
                <div>Tipi di injection: <strong>${escapeHtml(inj)}</strong></div>
            </div>
        </div>`;
    }).join('');
    container.innerHTML = `<div class="report-scroll">${rows}</div>`;
}

// call renderInjection from renderLogs
/* ensure injection rendering updated */
function renderLogs() {
    accessLogs = JSON.parse(localStorage.getItem(accessLogsKey)) || [];
    const logsTable = document.getElementById("accessLogs");
    logsTable.innerHTML = "";

    accessLogs.slice().reverse().forEach(log => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td class="px-4 py-2">${escapeHtml(log.username)}</td>
            <td class="px-4 py-2">${escapeHtml(log.status)}</td>
            <td class="px-4 py-2">${escapeHtml(log.timestamp)}</td>
            <td class="px-4 py-2">${escapeHtml(log.ip || 'unknown')}</td>
            <td class="px-4 py-2">${escapeHtml((log.ua || '').slice(0,80))}</td>
        `;
        logsTable.appendChild(row);
    });

    renderChart();
    renderAnalysis();
    renderInjectionChart(); // now line chart like access chart
    renderInjection();      // update injection list + examples (if you keep that function)
    renderReport();         // full report
}

function exportCSV() {
    const rows = [
        ['nome_utente','stato','data_ora','ip','userAgent'],
        ...accessLogs.map(l => [l.username, l.status, l.timestamp, l.ip || '', (l.ua||'')])
    ];
    const csv = rows.map(r => r.map(cell => `"${(cell||'').toString().replace(/"/g,'""')}"`).join(',')).join('\r\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `report_accessi_${new Date().toISOString().slice(0,19).replace(/[:T]/g,'-')}.csv`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
}

document.getElementById('downloadBtn').addEventListener('click', exportCSV);
document.getElementById('clearBtn').addEventListener('click', () => {
    if (!confirm('Cancellare tutti i log?')) return;
    localStorage.removeItem(accessLogsKey);
    accessLogs = [];
    renderLogs();
});

// inizializza
renderLogs();
