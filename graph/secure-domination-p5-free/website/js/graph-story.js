(() => {
  const G_EDGES = [[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[1,7],[1,8],[1,9],[1,10],[1,11],[2,3],[2,4],[2,8],[2,9],[2,11],[3,5],[3,7],[3,10],[3,11],[4,6],[4,7],[4,8],[4,10],[5,6],[5,8],[5,9],[5,10],[6,7],[6,9],[6,11],[7,8],[7,9],[8,11],[9,10],[10,11]];
  const MATCHING = new Set(['0-1','2-9','3-7','4-10','5-8','6-11']);
  const allPairs = [];
  for (let u = 0; u < 12; u += 1) for (let v = u + 1; v < 12; v += 1) allPairs.push([u,v]);
  const gSet = new Set(G_EDGES.map(([u,v]) => `${u}-${v}`));
  const I_EDGES = allPairs.filter(([u,v]) => !gSet.has(`${u}-${v}`));

  const center = {x:250, y:250};
  const points = [{x:250,y:48}];
  for (let k = 0; k < 5; k += 1) {
    const a = -Math.PI/2 + k*2*Math.PI/5;
    points.push({x:center.x+142*Math.cos(a), y:center.y-68+142*Math.sin(a)});
  }
  for (let k = 0; k < 5; k += 1) {
    const a = -Math.PI/2 + Math.PI/5 + k*2*Math.PI/5;
    points.push({x:center.x+142*Math.cos(a), y:center.y+68+142*Math.sin(a)});
  }
  points.push({x:250,y:452});

  const steps = [
    {
      label:'01 · Start with the icosahedron', edges:I_EDGES, edgeCount:30,
      title:'A familiar solid, flattened.',
      body:'The ordinary icosahedral graph connects the corners joined by an edge of the solid. It has 12 vertices, 30 edges, and 120 symmetries.',
      callout:'The counterexample uses exactly the opposite adjacency relation.',
      legend:[['#3f4942','vertex'],['#747c76','icosahedral edge']]
    },
    {
      label:'02 · Take the complement', edges:G_EDGES, edgeCount:36,
      title:'Keep every missing edge instead.',
      body:'In the complement, two vertices are adjacent precisely when they were not adjacent in the icosahedron. The new graph has 36 edges; the six coral edges are dominating pairs.',
      callout:'It is connected and has no induced five-point path (P₅).', matching:true,
      legend:[['#3f4942','vertex'],['#747c76','complement edge'],['#9e3a2b','dominating edge']]
    },
    {
      label:'03 · Try three guards', edges:G_EDGES, edgeCount:36,
      title:'Every triple fails.',
      body:'Here guards 0, 1, and 2 cover the graph. But if vertex 7 is attacked and guard 1 moves to defend it, vertex 10 becomes exposed. Exhaustive verification finds a failure for all 220 triples.',
      callout:'120 triples fail to dominate at all; the other 100 dominate but fail the security exchange.', guards:[0,1,2], attack:7, exposed:10, arrow:[1,7], dim:true,
      legend:[['#2a5438','guard'],['#9e3a2b','attacked vertex'],['#65569c','newly exposed']]
    },
    {
      label:'04 · Four guards suffice', edges:G_EDGES, edgeCount:36,
      title:'The fourth guard closes the gap.',
      body:'The set {0, 1, 2, 3} is secure. For example, if vertex 10 is attacked, guard 1 can move there and the exchanged set still dominates every vertex.',
      callout:'No secure triple exists and a secure four-set does, so the secure domination number is exactly 4.', guards:[0,1,2,3], attack:10, arrow:[1,10],
      legend:[['#2a5438','guard'],['#9e3a2b','attack answered safely']]
    }
  ];

  const svgNS = 'http://www.w3.org/2000/svg';
  const edgeLayer = document.getElementById('edge-layer');
  const nodeLayer = document.getElementById('node-layer');
  const annotationLayer = document.getElementById('annotation-layer');
  const copy = document.getElementById('step-copy');
  const label = document.getElementById('stage-label');
  const legend = document.getElementById('stage-legend');
  const count = document.getElementById('edge-count');
  const tabs = [...document.querySelectorAll('[data-step]')];
  const play = document.getElementById('play-story');
  let current = 0;
  let timer = null;

  function line([u,v], step) {
    const el = document.createElementNS(svgNS,'line');
    el.setAttribute('x1',points[u].x); el.setAttribute('y1',points[u].y);
    el.setAttribute('x2',points[v].x); el.setAttribute('y2',points[v].y);
    el.setAttribute('class',`graph-edge${step.matching && MATCHING.has(`${Math.min(u,v)}-${Math.max(u,v)}`) ? ' matching' : ''}${step.dim ? ' dim' : ''}`);
    return el;
  }

  function node(id, step) {
    const el = document.createElementNS(svgNS,'g');
    let cls = 'node';
    if ((step.guards || []).includes(id)) cls += ' guard';
    if (step.attack === id) cls += ' attack';
    if (step.exposed === id) cls += ' exposed';
    el.setAttribute('class', cls);
    el.setAttribute('transform',`translate(${points[id].x} ${points[id].y})`);
    const c = document.createElementNS(svgNS,'circle'); c.setAttribute('r','15');
    const t = document.createElementNS(svgNS,'text'); t.setAttribute('text-anchor','middle'); t.setAttribute('dy','.36em'); t.textContent=id;
    el.append(c,t); return el;
  }

  function arrow([u,v]) {
    const a = document.createElementNS(svgNS,'path');
    const p = points[u], q = points[v];
    const dx=q.x-p.x, dy=q.y-p.y, len=Math.hypot(dx,dy), ux=dx/len, uy=dy/len;
    a.setAttribute('d',`M ${p.x+22*ux} ${p.y+22*uy} L ${q.x-24*ux} ${q.y-24*uy}`);
    a.setAttribute('class','story-arrow'); return a;
  }

  function render(index) {
    current = index;
    const step = steps[index];
    edgeLayer.replaceChildren(...step.edges.map(e => line(e,step)));
    annotationLayer.replaceChildren(...(step.arrow ? [arrow(step.arrow)] : []));
    nodeLayer.replaceChildren(...points.map((_,i) => node(i,step)));
    copy.innerHTML = `<h3>${step.title}</h3><p>${step.body}</p><p class="callout">${step.callout}</p>`;
    label.textContent = step.label; count.textContent = step.edgeCount;
    legend.innerHTML = step.legend.map(([color,text]) => `<span class="legend-dot" style="--dot:${color}">${text}</span>`).join('');
    tabs.forEach((tab,i) => {
      const selected = i === index;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
    });
  }

  tabs.forEach((tab, index) => {
    tab.addEventListener('click',() => { stop(); render(Number(tab.dataset.step)); });
    tab.addEventListener('keydown', event => {
      let next = null;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === null) return;
      event.preventDefault();
      stop();
      render(next);
      tabs[next].focus();
    });
  });
  function stop() { if (timer) window.clearInterval(timer); timer=null; play.textContent='▶ Play story'; }
  play.addEventListener('click',() => {
    if (timer) { stop(); return; }
    play.textContent='■ Pause'; render(0);
    timer=window.setInterval(() => { if (current===3) stop(); else render(current+1); }, 3200);
  });
  render(0);
})();
