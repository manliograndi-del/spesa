/* Shared site header. First row: Umberto Tozzi's sections and Gloria, always visible.
   A "Classifiche e altri artisti" button opens a second row with the general pages; it is open by itself on those pages.
   Sections that group more than one page get tabs under the header. */
(function () {
  const HAVE = ["album.html", "allora-oggi.html", "ascolti.html", "cover.html", "fanclub.html", "follower.html", "fonti.html", "fonti.html", "gloria.html", "gloria.html", "hpi-fimi.html", "index.html", "mondo-artisti.html", "mondo.html", "schermo.html", "singoli-fimi.html", "singoli.html", "tozzi-fonti.html", "tozzi-mondo.html", "tozzi-spotify.html", "vendite.html"]; /* filled in by build.py with the pages that exist */
  const TOZZI = [
    ["Su Spotify", [["tozzi-spotify.html", "Tozzi su Spotify"]]],
    ["Nel mondo", [["tozzi-mondo.html", "Le città che lo ascoltano"]]],
    ["In classifica", [["tozzi-fonti.html", "Tozzi, fonte per fonte"]]],
    ["Ascolti", [["ascolti.html", "Ascoltatori mensili"], ["follower.html", "Follower"]]],
    ["Le cover", [["cover.html", "Le cover"]]],
    ["Sullo schermo", [["schermo.html", "Sullo schermo"]]],
    ["Fan club", [["fanclub.html", "Fan club"]]],
  ];
  const MORE = [
    { label: "Classifiche", items: [
      ["Album", [["album.html", "Album per artista"]]],
      ["Singoli", [["singoli.html", "Singoli italiani"]]],
      ["FIMI", [["singoli-fimi.html", "Classifica FIMI"], ["hpi-fimi.html", "Hit Parade Italia contro FIMI"]]],
      ["Mondo", [["mondo.html", "Le canzoni"], ["mondo-artisti.html", "Gli artisti"]]],
    ]},
    { label: "Artisti '70–'80", items: [
      ["Allora e oggi", [["allora-oggi.html", "Allora contro oggi"]]],
      ["Vendite", [["vendite.html", "Certificazioni e dischi venduti"]]],
    ]},
    { label: "Ricerca", items: [
      ["Fonti", [["fonti.html", "Tutti i link della ricerca"]]],
    ]},
  ];
  const ok = p => !HAVE || HAVE.includes(p);
  const here = (location.pathname.split("/").pop() || "index.html").split("?")[0];
  const css = `
  #sitebar{position:sticky;top:0;z-index:50;background:linear-gradient(180deg,rgba(6,9,48,.96),rgba(10,14,70,.93));backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:2px solid #de0952;box-shadow:0 8px 24px rgba(0,0,20,.35);font-family:Montserrat,"Segoe UI",system-ui,sans-serif}
  #sitebar,#sitebar *{box-sizing:border-box}#sitebar a,#sitebar span,#sitebar b,#sitebar button{margin:0}
  #sitebar .sb-in{max-width:1240px;margin:0 auto;display:flex;align-items:center;gap:10px 22px;padding:10px max(16px,env(safe-area-inset-right,0px)) 10px max(16px,env(safe-area-inset-left,0px));padding-top:calc(10px + env(safe-area-inset-top,0px))}
  #sitebar .sb-logo{display:grid;line-height:1;text-decoration:none;flex:none}
  #sitebar .sb-logo b{font-family:Anton,Montserrat,sans-serif;font-weight:400;font-size:32px;letter-spacing:.05em;text-transform:uppercase;background:radial-gradient(circle,#fffdf2 0 .016em,rgba(255,244,200,.95) .03em,rgba(255,220,120,0) .055em) 0 0/.13em .13em,linear-gradient(180deg,#ffe066,#ffb21c 45%,#f0521a);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 6px rgba(255,160,40,.5))}
  #sitebar .sb-logo span{font-size:9.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#a9acd8;margin-top:3px}
  #sitebar .sb-scroll{flex:1;min-width:0;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}
  #sitebar .sb-scroll::-webkit-scrollbar,#sitebar .sb-tin::-webkit-scrollbar{display:none}
  #sitebar .sb-row{display:flex;gap:6px;align-items:center;width:max-content;margin-left:auto}
  #sitebar .sb-btn{font:inherit;font-size:12px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;color:#fff;background:#de0952;border:0;border-radius:3px;padding:9px 12px;text-decoration:none;white-space:nowrap;display:inline-flex;align-items:center;gap:6px;cursor:pointer}
  #sitebar .sb-btn:hover{background:#f42370}
  #sitebar .sb-btn.sb-cur{background:#fff;color:#b0063f}
  #sitebar .sb-btn.sb-cta{background:#fea607;color:#00001d}
  #sitebar .sb-btn.sb-cta:hover{background:#ffb72f}
  #sitebar .sb-btn.sb-cta.sb-cur{background:#fff;color:#00001d}
  #sitebar .sb-btn.sb-ghost{background:transparent;color:#e1e3f7;box-shadow:inset 0 0 0 1px #4a50a8}
  #sitebar .sb-btn.sb-ghost:hover{box-shadow:inset 0 0 0 1px #fea607;color:#fff}
  #sitebar .sb-btn.sb-ghost[aria-expanded="true"]{background:#1d2378;box-shadow:inset 0 0 0 1px #fea607}
  #sitebar .sb-btn svg{width:10px;height:10px;fill:currentColor;transition:transform .15s}
  #sitebar .sb-btn[aria-expanded="true"] svg{transform:rotate(180deg)}
  #sitebar .sb-more{display:none;border-top:1px solid rgba(255,255,255,.08);background:rgba(4,6,36,.5)}
  #sitebar.sb-open .sb-more{display:block}
  #sitebar .sb-more .sb-scroll{max-width:1240px;margin:0 auto;padding:9px max(16px,env(safe-area-inset-right,0px)) 10px max(16px,env(safe-area-inset-left,0px))}
  #sitebar .sb-more .sb-row{margin-left:0;gap:6px 18px;align-items:flex-end}
  #sitebar .sb-grp{display:grid;gap:4px}
  #sitebar .sb-lab{font-size:10px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#fea607}
  #sitebar .sb-grp > div{display:flex;gap:5px}
  #sitebar .sb-more .sb-btn{font-size:11.5px;padding:8px 11px}
  #sitebar .sb-tabs{border-top:1px solid rgba(255,255,255,.08)}
  #sitebar .sb-tin{max-width:1240px;margin:0 auto;display:flex;gap:4px;overflow-x:auto;padding:0 max(16px,env(safe-area-inset-right,0px)) 0 max(16px,env(safe-area-inset-left,0px));scrollbar-width:none}
  #sitebar .sb-tabs a{flex:none;padding:9px 12px 8px;font-size:13px;font-weight:600;color:#c9cbe4;text-decoration:none;border-bottom:3px solid transparent}
  #sitebar .sb-tabs a:hover{color:#fff}
  #sitebar .sb-tabs a.sb-cur{color:#fff;border-bottom-color:#fea607}
  #sitebar :focus-visible{outline:2px solid #fea607;outline-offset:2px}
  @media (max-width:1060px){
    #sitebar .sb-in{flex-wrap:wrap;gap:8px 12px;padding-bottom:8px}
    #sitebar .sb-logo{flex-direction:row}
    #sitebar .sb-in > .sb-scroll{flex-basis:100%;margin:0 calc(-1 * max(16px,env(safe-area-inset-left,0px)));padding:0 max(16px,env(safe-area-inset-left,0px))}
    #sitebar .sb-in .sb-row{margin-left:0}
  }
  #sitebar .sb-short{display:none}
  @media (max-width:640px){
    #sitebar{position:relative}
    #sitebar .sb-in > .sb-scroll{overflow:visible;margin:0;padding:0}
    #sitebar .sb-in .sb-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));width:auto;gap:6px}
    #sitebar .sb-in .sb-btn{justify-content:center;text-align:center;white-space:normal;line-height:1.15;min-height:42px;padding:8px 4px;font-size:11px;letter-spacing:.4px}
    #sitebar .sb-in .sb-btn svg{flex:none}
    #sitebar .sb-long{display:none}#sitebar .sb-short{display:inline}
    #sitebar .sb-more .sb-scroll{overflow:visible}
    #sitebar .sb-more .sb-row{flex-wrap:wrap;width:auto;gap:10px 14px}
    #sitebar .sb-grp > div{flex-wrap:wrap}
  }
  @media (prefers-reduced-motion:reduce){#sitebar .sb-btn svg{transition:none}}`;
  const st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
  let curTabs = null, inMore = false;
  const btn = ([t, tabs], extra = "") => {
    tabs = tabs.filter(x => ok(x[0]));
    if (!tabs.length) return "";
    const cur = tabs.some(x => x[0] === here);
    if (cur && tabs.length > 1) curTabs = tabs;
    return `<a class="sb-btn${extra}${cur ? " sb-cur" : ""}" href="${tabs[0][0]}"${cur ? ' aria-current="page"' : ""}>${t}</a>`;
  };
  const tozzi = TOZZI.map(i => btn(i)).join("") + btn(["Gloria", [["gloria.html", "Gloria"]]], " sb-cta");
  const more = MORE.map(g => {
    const h = g.items.map(i => btn(i)).join("");
    if (g.items.some(([, tabs]) => tabs.some(x => x[0] === here))) inMore = true;
    return h ? `<div class="sb-grp"><span class="sb-lab">${g.label}</span><div>${h}</div></div>` : "";
  }).join("");
  const chev = '<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4z"/></svg>';
  const bar = document.createElement("div");
  bar.id = "sitebar"; bar.setAttribute("role", "banner");
  bar.innerHTML = `<div class="sb-in"><a class="sb-logo" href="index.html"><b>Tozziade</b><span>Umberto Tozzi in numeri</span></a>
    <div class="sb-scroll"><div class="sb-row" role="navigation" aria-label="Umberto Tozzi">${tozzi}
    <button class="sb-btn sb-ghost" type="button" id="sb-more-btn" aria-expanded="false" aria-controls="sb-more"><span class="sb-long">Classifiche e altri artisti</span><span class="sb-short">Altri artisti</span>${chev}</button></div></div></div>
    <div class="sb-more" id="sb-more"><div class="sb-scroll"><div class="sb-row" role="navigation" aria-label="Classifiche e altri artisti">${more}</div></div></div>`;
  if (curTabs) {
    const t = document.createElement("div"); t.className = "sb-tabs";
    t.innerHTML = `<div class="sb-tin" role="tablist">${curTabs.map(([h, l]) => `<a href="${h}"${h === here ? ' class="sb-cur" aria-current="page"' : ""}>${l}</a>`).join("")}</div>`;
    bar.appendChild(t);
  }
  const mb = bar.querySelector("#sb-more-btn");
  const setOpen = o => { bar.classList.toggle("sb-open", o); mb.setAttribute("aria-expanded", o ? "true" : "false"); };
  setOpen(inMore);
  mb.addEventListener("click", () => setOpen(!bar.classList.contains("sb-open")));
  const body = document.body;
  const bs = getComputedStyle(body);
  bar.style.marginTop = `-${bs.paddingTop}`;
  bar.style.marginLeft = `-${bs.paddingLeft}`;
  bar.style.marginRight = `-${bs.paddingRight}`;
  bar.style.marginBottom = "22px";
  body.insertBefore(bar, body.firstChild);
  bar.querySelectorAll(".sb-btn.sb-cur").forEach(c => { const s = c.closest(".sb-scroll"); if (s && s.scrollWidth > s.clientWidth) s.scrollLeft = c.offsetLeft - s.clientWidth / 2 + c.offsetWidth / 2; });
})();
