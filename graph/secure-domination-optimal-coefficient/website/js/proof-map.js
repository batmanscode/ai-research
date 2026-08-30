(() => {
  const svgNS = 'http://www.w3.org/2000/svg';
  const lineLayer = document.getElementById('proof-lines');
  const nodeLayer = document.getElementById('proof-nodes');
  const copy = document.getElementById('proof-copy');
  const tabs = [...document.querySelectorAll('[data-step]')];
  const play = document.getElementById('play-proof');

  const nodes = [
    {id:'root', x:410, y:42, w:230, h:62, label:['Connected + P₅-free'], sub:'α ≥ 3', reveal:0, current:[0]},
    {id:'path', x:175, y:154, w:176, h:66, label:['Dominating P₃'], sub:'path branch', reveal:1, solve:2, current:[1,2]},
    {id:'clique', x:590, y:154, w:186, h:66, label:['Dominating clique'], sub:'clique branch', reveal:1, solve:5, current:[1]},
    {id:'small', x:410, y:275, w:134, h:62, label:['1–2 hubs'], sub:'residual bound', reveal:3, solve:3, current:[3]},
    {id:'triangle', x:570, y:275, w:134, h:62, label:['3 hubs'], sub:'triangle theorem', reveal:3, solve:3, current:[3]},
    {id:'large', x:735, y:275, w:134, h:62, label:['4+ hubs'], sub:'private regions', reveal:3, solve:5, current:[3]},
    {id:'nocross', x:620, y:386, w:164, h:62, label:['No cross-edge'], sub:'private theorem', reveal:4, solve:4, current:[4]},
    {id:'cross', x:746, y:386, w:144, h:62, label:['Cross-edge'], sub:'forces a P₃', reveal:4, solve:5, current:[4], kind:'return'},
    {id:'result', x:275, y:416, w:222, h:70, label:['γₛ ≤ α + 1'], sub:'every branch closed', reveal:5, solve:5, current:[5]}
  ];

  const edges = [
    {from:'root', to:'path', reveal:1, solve:2},
    {from:'root', to:'clique', reveal:1, solve:5},
    {from:'clique', to:'small', reveal:3, solve:3},
    {from:'clique', to:'triangle', reveal:3, solve:3},
    {from:'clique', to:'large', reveal:3, solve:5},
    {from:'large', to:'nocross', reveal:4, solve:4},
    {from:'large', to:'cross', reveal:4, solve:5},
    {from:'path', to:'result', reveal:2, solve:5},
    {from:'small', to:'result', reveal:3, solve:5},
    {from:'triangle', to:'result', reveal:3, solve:5},
    {from:'nocross', to:'result', reveal:4, solve:5, curve:true},
    {from:'cross', to:'path', reveal:4, solve:5, return:true}
  ];

  const steps = [
    {
      title:'Start with one allowed network.',
      body:'The target is not to guess the guards directly. First expose a small set of vertices that already reaches—or dominates—everywhere else.',
      conclusion:'Goal: build a secure dominating set with at most α + 1 guards for every graph in the class.',
      link:'https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/structure/optimal-four-thirds-theorem.md',
      linkText:'Open the theorem statement ↗'
    },
    {
      title:'A structure theorem gives two doors.',
      body:'Bacsó and Tuza proved that every connected induced-P₅-free graph has either a dominating induced three-vertex path or a dominating clique. “Dominating” means every other vertex touches the core.',
      conclusion:'This split is exhaustive: solving both doors solves every graph in the stated class.',
      link:'https://doi.org/10.1007/BF02352694',
      linkText:'See the source structure theorem ↗'
    },
    {
      title:'The path door is already closed.',
      body:'The three vertices of the path are not claimed to be secure by themselves. A constructive exchange theorem uses that path to build a secure set of size at most α + 1.',
      conclusion:'Any dominating induced P₃ ⇒ γₛ ≤ α + 1.',
      link:'https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/structure/dominating-p3.md',
      linkText:'Read the dominating-path proof ↗'
    },
    {
      title:'Shrink the clique, then sort by size.',
      body:'Remove redundant hubs until the dominating clique is inclusion-minimal. One or two hubs follow from a general residual-completion bound. Three hubs require the separate dominating-triangle theorem. Only four or more hubs need the final geometry.',
      conclusion:'Clique size ≤ 3 is closed without claiming that the clique itself is a secure set.',
      link:'https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/structure/triangle-bad-m.md',
      linkText:'Read the triangle closure ↗'
    },
    {
      title:'The last large-clique case splits once.',
      body:'Every hub in a minimal clique has a private region. If distinct private regions have no edges between them, the pairwise-private theorem saves the needed guard. If a cross-edge x–y exists, one endpoint hub kᵢ makes kᵢ–x–y a dominating induced P₃.',
      conclusion:'The cross-edge branch folds back into the solved path door. Edges inside a single private region remain unrestricted.',
      link:'https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/structure/larger-clique-private-geometry.md',
      linkText:'Inspect the private-region lemmas ↗'
    },
    {
      title:'No cases remain.',
      body:'The path branch, small cliques, triangles, large cliques without cross-edges, and large cliques with cross-edges all reach the same additive bound.',
      conclusion:'γₛ ≤ α + 1 ≤ 4α/3 for α ≥ 3. The 12-vertex graph with (α, γₛ) = (3, 4) makes 4/3 exact.',
      link:'https://github.com/batmanscode/ai-research/blob/main/graph/secure-domination-optimal-coefficient/referees/optimal-four-thirds-audit-a.md',
      linkText:'Read an independent proof audit ↗'
    }
  ];

  const byId = new Map(nodes.map(node => [node.id, node]));
  let current = 0;
  let timer = null;

  function nodeClass(node, step) {
    if (step < node.reveal) return 'map-node pending';
    if (node.current.includes(step)) return `map-node current${node.kind ? ` ${node.kind}` : ''}`;
    if (node.solve !== undefined && step >= node.solve) return `map-node solved${node.kind ? ` ${node.kind}` : ''}`;
    return `map-node${node.kind ? ` ${node.kind}` : ''}`;
  }

  function makeNode(node, step) {
    const group = document.createElementNS(svgNS, 'g');
    group.setAttribute('class', nodeClass(node, step));
    group.setAttribute('transform', `translate(${node.x} ${node.y})`);
    const rect = document.createElementNS(svgNS, 'rect');
    rect.setAttribute('x', String(-node.w / 2)); rect.setAttribute('y', String(-node.h / 2));
    rect.setAttribute('width', String(node.w)); rect.setAttribute('height', String(node.h));
    const label = document.createElementNS(svgNS, 'text');
    label.setAttribute('y', '-4'); label.textContent = node.label[0];
    const sub = document.createElementNS(svgNS, 'text');
    sub.setAttribute('class', 'sub'); sub.setAttribute('y', '16'); sub.textContent = node.sub;
    group.append(rect, label, sub);
    return group;
  }

  function makeEdge(edge, step) {
    const a = byId.get(edge.from), b = byId.get(edge.to);
    const path = document.createElementNS(svgNS, 'path');
    let d;
    if (edge.return) {
      d = `M ${a.x - a.w / 2} ${a.y} C 520 448, 42 356, ${b.x - b.w / 2} ${b.y + 12}`;
      path.setAttribute('stroke-dasharray', '7 5');
    } else if (edge.curve) {
      d = `M ${a.x} ${a.y + a.h / 2} C ${a.x} 455, ${b.x + 90} 454, ${b.x + b.w / 2} ${b.y}`;
    } else {
      const down = b.y >= a.y;
      d = `M ${a.x} ${a.y + (down ? a.h / 2 : -a.h / 2)} L ${b.x} ${b.y - (down ? b.h / 2 : -b.h / 2)}`;
    }
    path.setAttribute('d', d);
    let cls = 'proof-line';
    if (step < edge.reveal) cls += ' hidden';
    else if (edge.solve !== undefined && step >= edge.solve) cls += ' solved';
    else cls += ' active';
    path.setAttribute('class', cls);
    return path;
  }

  function stop() {
    if (timer) window.clearInterval(timer);
    timer = null;
    play.textContent = '▶ Play proof';
  }

  function render(step) {
    current = step;
    lineLayer.replaceChildren(...edges.map(edge => makeEdge(edge, step)));
    nodeLayer.replaceChildren(...nodes.map(node => makeNode(node, step)));
    const item = steps[step];
    copy.innerHTML = `<h3>${item.title}</h3><p>${item.body}</p><p class="conclusion">${item.conclusion}</p><a class="formal-link" href="${item.link}">${item.linkText}</a>`;
    tabs.forEach((tab, index) => {
      const selected = index === step;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
    });
  }

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => { stop(); render(index); });
    tab.addEventListener('keydown', event => {
      let next = null;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === null) return;
      event.preventDefault(); stop(); render(next); tabs[next].focus();
    });
  });

  play.addEventListener('click', () => {
    if (timer) { stop(); return; }
    render(0); play.textContent = '■ Pause';
    timer = window.setInterval(() => {
      if (current === steps.length - 1) stop(); else render(current + 1);
    }, 3400);
  });

  render(0);
})();
