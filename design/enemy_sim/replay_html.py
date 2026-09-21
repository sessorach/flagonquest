"""
Renders a combat_sim.run_fight(..., trace=[]) trace as a single
self-contained HTML page - a battle-map grid plus a combat log per
round - so a fight can be looked at in a browser without needing
anything published anywhere. `narrate_fight.py --html out.html` is the
usual way to reach this; `render_html(trace, result, arena_size)` is
also importable directly if some other script wants to build the same
page from its own trace.

Kept as its own module (not folded into narrate_fight.py) so anything
else that wants this exact rendering - a future web view, say - can
import `render_html` without pulling in narrate_fight.py's CLI/argparse
machinery too.
"""
import json

_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Combat Replay</title>
<style>
:root{
  --bg:#0a0d15;
  --surface:#131826;
  --surface-2:#1a2135;
  --border:#2d3555;
  --border-soft:#232b44;
  --text:#e7e9f2;
  --text-dim:#8b93ab;
  --text-faint:#5b6480;
  --accent:#e8c46a;
  --party:#6fae5a;
  --party-dim:#3f6a38;
  --enemy:#e0645f;
  --heal:#5fc7c9;
  --miss:#5b6480;
}
*{box-sizing:border-box;}
body{
  margin:0;
  background:var(--bg);
  color:var(--text);
  font-family:Georgia,serif;
  padding:32px 16px 48px;
}
.wrap{max-width:980px;margin:0 auto;}
h1{
  font-size:clamp(26px,5vw,38px);
  color:var(--accent);
  margin:0 0 6px;
}
.subtitle{color:var(--text-dim);font-size:15px;margin:0 0 20px;line-height:1.5;}
.setup{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:18px;}
.turn-order{font-family:monospace;font-size:12px;color:var(--text-dim);margin:0 0 18px;line-height:1.6;}
.turn-order b{color:var(--text);}
.turn-order .party-name{color:var(--party);}
.turn-order .enemy-name{color:var(--enemy);}
.chip{
  font-family:monospace;
  font-size:12.5px;
  padding:5px 10px;
  border-radius:6px;
  background:var(--surface-2);
  border:1px solid var(--border-soft);
  color:var(--text-dim);
}
.chip b{color:var(--text);font-weight:600;}
.result-banner{
  font-size:18px;
  padding:12px 18px;
  border-radius:8px;
  margin-bottom:28px;
  background:linear-gradient(135deg,var(--party-dim),var(--surface));
  border:1px solid var(--party);
  color:#d8ecd0;
}
.legend{
  display:flex;flex-wrap:wrap;gap:16px;
  font-family:monospace;font-size:12px;color:var(--text-dim);
  background:var(--surface);border:1px solid var(--border-soft);border-radius:8px;
  padding:12px 16px;margin-bottom:32px;
}
.legend span{display:inline-flex;align-items:center;gap:6px;}
.dot{width:10px;height:10px;border-radius:50%;display:inline-block;flex:none;}
.dot.party{background:var(--party);}
.dot.enemy{background:var(--enemy);}
.swatch{width:10px;height:10px;border-radius:2px;display:inline-block;flex:none;}
.round{border:1px solid var(--border);border-radius:10px;background:var(--surface);margin-bottom:22px;overflow:hidden;}
.round-head{font-size:19px;color:var(--accent);padding:12px 18px;border-bottom:1px solid var(--border-soft);background:var(--surface-2);}
.round-body{display:grid;grid-template-columns:minmax(220px,340px) 1fr;}
@media (max-width:640px){.round-body{grid-template-columns:1fr;}}
.mapcol{padding:16px;display:flex;flex-direction:column;align-items:center;gap:10px;border-right:1px solid var(--border-soft);}
@media (max-width:640px){.mapcol{border-right:none;border-bottom:1px solid var(--border-soft);}}
.mapcol svg{width:100%;height:auto;max-width:300px;}
.roster{font-family:monospace;font-size:11.5px;color:var(--text-dim);width:100%;max-width:300px;display:flex;flex-direction:column;gap:2px;}
.roster .u{display:flex;justify-content:space-between;gap:8px;}
.roster .u b{color:var(--text);font-weight:600;}
.log{padding:14px 18px;font-family:monospace;font-size:13px;line-height:1.85;}
.line{padding:2px 0;}
.line .who{color:var(--text);font-weight:600;}
.line.hit .dmg{color:var(--accent);font-weight:600;}
.line.miss{color:var(--miss);}
.line.heal{color:var(--heal);}
.line.heal .who{color:var(--heal);}
.line.move{color:var(--text-faint);font-style:italic;}
.line .arrow{color:var(--text-dim);margin:0 4px;}
.line .breakdown{color:var(--text-faint);font-size:11.5px;}
.line .via{color:var(--text-dim);font-style:italic;}
footer{margin-top:36px;color:var(--text-dim);font-size:12px;font-family:monospace;border-top:1px solid var(--border-soft);padding-top:16px;}
footer code{color:var(--accent);}
</style>
</head>
<body>
<div class="wrap">
  <h1>Combat Replay</h1>
  <p class="subtitle">One seeded fight from FlagonQuest's enemy-encounter combat simulator, rendered round by round.</p>
  <div class="setup" id="setup"></div>
  <div class="turn-order" id="turnOrder"></div>
  <div class="result-banner" id="resultBanner"></div>
  <div class="legend">
    <span><span class="dot party"></span> Party</span>
    <span><span class="dot enemy"></span> Enemies</span>
    <span><span class="swatch" style="background:var(--accent)"></span> Hit / damage</span>
    <span><span class="swatch" style="background:var(--miss)"></span> Miss</span>
    <span><span class="swatch" style="background:var(--heal)"></span> Heal</span>
  </div>
  <div id="rounds"></div>
  <footer>Generated by design/enemy_sim/replay_html.py (narrate_fight.py --html) - see design/enemy_sim/README.md.</footer>
</div>
<script>
const FIGHT = __FIGHT_DATA__;
const ARENA = FIGHT.arena_size;
const trace = FIGHT.trace;
const result = FIGHT.result;

const initiative = trace.find(e => e.type === 'initiative');
const byRound = new Map();
for (const e of trace) {
  if (e.type === 'initiative') continue;
  if (!byRound.has(e.round)) byRound.set(e.round, []);
  byRound.get(e.round).push(e);
}

const firstRoundNum = Math.min(...byRound.keys());
const firstPositions = (byRound.get(firstRoundNum) || []).find(e => e.type === 'positions');
const labels = {};
if (firstPositions) {
  firstPositions.party.forEach((u, i) => labels[u.unit] = 'P' + (i + 1));
  firstPositions.enemies.forEach((u, i) => labels[u.unit] = 'E' + (i + 1));
}

function setupChips() {
  const el = document.getElementById('setup');
  const chips = [`<div class="chip">Rounds: <b>${result.rounds}</b></div>`,
                 `<div class="chip">Party HP remaining: <b>${Math.round(result.party_hp_pct * 100)}%</b></div>`];
  if (firstPositions) {
    const partyNames = firstPositions.party.map(u => u.unit.replace(/\\d+$/, ''));
    const enemyNames = [...new Set(firstPositions.enemies.map(u => u.unit.replace(/\\s?\\d+$/, '')))];
    chips.unshift(`<div class="chip">Party: <b>${partyNames.join(', ')}</b></div>`,
                   `<div class="chip">Enemies: <b>${enemyNames.join(', ')}</b> (${firstPositions.enemies.length} total)</div>`);
  }
  el.innerHTML = chips.join('');
  let banner = (result.winner === 'party' ? 'Party wins' : result.winner === 'enemies' ? 'Enemies win' : 'Draw') +
    ` after ${result.rounds} round${result.rounds === 1 ? '' : 's'}.`;
  if (result.vs_average) {
    const v = result.vs_average;
    banner += ` (average over ${v.trials} trials of this matchup: ${v.win_pct.toFixed(1)}% win, ` +
      `${v.avg_rounds.toFixed(1)} rounds, ${v.avg_hp_on_win.toFixed(1)}% HP on win - this replay is one sample, not the trend.)`;
  }
  document.getElementById('resultBanner').textContent = banner;
  if (initiative) {
    const names = initiative.order.map(o =>
      `<span class="${o.side === 'party' ? 'party-name' : 'enemy-name'}">${o.unit}</span>`);
    document.getElementById('turnOrder').innerHTML = `<b>Turn order:</b> ${names.join(' &rarr; ')}`;
  }
}

function svgMap(positions) {
  const pad = 20, scale = 18, size = ARENA * scale + pad * 2;
  const toX = x => pad + x * scale;
  const toY = y => pad + (ARENA - y) * scale;
  let grid = '';
  for (let i = 0; i <= ARENA; i += 5) {
    grid += `<line x1="${toX(i)}" y1="${toY(0)}" x2="${toX(i)}" y2="${toY(ARENA)}" stroke="var(--border-soft)" stroke-width="1"/>`;
    grid += `<line x1="${toX(0)}" y1="${toY(i)}" x2="${toX(ARENA)}" y2="${toY(i)}" stroke="var(--border-soft)" stroke-width="1"/>`;
  }
  const dots = [...positions.party.map(u => [u, 'party']), ...positions.enemies.map(u => [u, 'enemy'])]
    .map(([u, side]) => {
      const [x, y] = u.pos;
      const color = side === 'party' ? 'var(--party)' : 'var(--enemy)';
      return `<g><circle cx="${toX(x)}" cy="${toY(y)}" r="9" fill="${color}" stroke="var(--surface)" stroke-width="2"/>
        <text x="${toX(x)}" y="${toY(y)}" text-anchor="middle" dominant-baseline="central" font-family="monospace" font-size="9" font-weight="600" fill="var(--bg)">${labels[u.unit] || '?'}</text></g>`;
    }).join('');
  return `<svg viewBox="0 0 ${size} ${size}"><rect x="${pad}" y="${pad}" width="${ARENA*scale}" height="${ARENA*scale}" fill="var(--surface-2)" stroke="var(--border)" stroke-width="1.5"/>${grid}${dots}</svg>`;
}

function rosterList(positions) {
  const all = [...positions.party.map(u => ['party', u]), ...positions.enemies.map(u => ['enemy', u])];
  return `<div class="roster">${all.map(([side, u]) =>
    `<div class="u"><span><b style="color:var(--${side})">${labels[u.unit] || '?'}</b> ${u.unit}</span><span>${u.health} HP</span></div>`
  ).join('')}</div>`;
}

function logLine(e) {
  if (e.action === 'move') {
    const spaces = e.spaces != null ? ` <span class="via">(${e.spaces} space${e.spaces !== 1 ? 's' : ''})</span>` : '';
    return e.in_range
      ? `<div class="line move">${e.unit} moves${spaces} toward its target - now in range.</div>`
      : `<div class="line move">${e.unit} moves${spaces} toward its target - still out of range, no attack.</div>`;
  }
  if (e.action === 'attack') {
    const cls = e.hit ? 'hit' : 'miss';
    const via = e.via ? ` <span class="via">with ${e.via}</span>` : '';
    let verdict = 'misses';
    if (e.hit) {
      let breakdown = `${e.raw_dmg} raw &minus; ${e.resist} resist`;
      if (e.protected_absorbed) breakdown += ` &minus; ${e.protected_absorbed} Protected`;
      verdict = `<span class="dmg">HIT for ${e.dmg}</span> <span class="breakdown">(${breakdown})</span> &rarr; ${e.target_hp_after} HP`;
    }
    // Target's own Harried count right after this attack (glossary.md:
    // -1 Dodge/Parry per stack) - shown whenever it's nonzero, not just
    // on the attack that added the stack (it can carry over from an
    // earlier attack this same round).
    const harried = e.target_harried_after ? ` <span class="via">(target now Harried ${e.target_harried_after})</span>` : '';
    const turnShift = e.turn_shift ? ` <span class="via">[${e.turn_shift}]</span>` : '';
    return `<div class="line ${cls}"><span class="who">${e.unit}</span> attacks <b>${e.target}</b>${via} <span class="arrow">(${e.roll} vs ${e.defense})</span> ${verdict}${harried}${turnShift}</div>`;
  }
  if (e.action === 'heal') {
    const via = e.via ? ` <span class="via">with ${e.via}</span>` : '';
    return `<div class="line heal"><span class="who">${e.unit}</span> heals <b>${e.target}</b>${via} for ${e.amount} &rarr; ${e.target_hp_after} HP</div>`;
  }
  return '';
}

function render() {
  setupChips();
  const container = document.getElementById('rounds');
  const roundNums = [...byRound.keys()].sort((a, b) => a - b);
  for (const rnd of roundNums) {
    const events = byRound.get(rnd);
    const positions = events.find(e => e.type === 'positions');
    const logEvents = events.filter(e => e.action);
    const section = document.createElement('div');
    section.className = 'round';
    section.innerHTML = `
      <div class="round-head">Round ${rnd}</div>
      <div class="round-body">
        <div class="mapcol">${positions ? svgMap(positions) + rosterList(positions) : '<span style="color:var(--text-dim)">(static mode - no positions)</span>'}</div>
        <div class="log">${logEvents.map(logLine).join('') || '<span style="color:var(--text-dim)">(no actions this round)</span>'}</div>
      </div>`;
    container.appendChild(section);
  }
}
render();
</script>
</body>
</html>
"""


def render_html(trace, result, arena_size):
    """Returns the full page as a string - write it to a file yourself
    (see narrate_fight.py's --html option) or embed it however else you
    like."""
    data = json.dumps({"trace": trace, "result": result, "arena_size": arena_size})
    return _TEMPLATE.replace("__FIGHT_DATA__", data)
