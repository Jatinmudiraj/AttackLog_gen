// let SCENARIOS = [];
// let CURRENT = null;

// // Load scenarios
// window.addEventListener("DOMContentLoaded", async () => {
//     try {
//         const res = await fetch("/api/load_scenarios");
//         const data = await res.json();
//         SCENARIOS = data.scenarios || [];

//         const listEl = document.getElementById("scenario_list");
//         listEl.innerHTML = "";

//         SCENARIOS.forEach((sc, idx) => {
//             const card = document.createElement("div");
//             card.className = "scenario-card";
//             card.onclick = () => selectScenario(idx);

//             card.innerHTML = `
//                 <h3>${sc.id}</h3>
//                 <p>${sc.name}</p>
//             `;
//             listEl.appendChild(card);
//         });

//     } catch (e) {
//         console.error("Error loading scenarios:", e);
//     }
// });

// function selectScenario(idx) {
//     CURRENT = SCENARIOS[idx];
//     if (!CURRENT) return;

//     document.querySelectorAll(".scenario-card").forEach((c, i) =>
//         c.classList.toggle("active", i === idx)
//     );

//     updateDetails();
//     drawGraph();
// }

// function updateDetails() {
//     const sc = CURRENT;

//     document.getElementById("scenario_title").innerText = `${sc.id} – ${sc.name}`;
//     document.getElementById("scenario_desc").innerText = sc.description;

//     document.getElementById("scenario_hosts").innerHTML =
//         `<strong>Hosts:</strong> ${sc.nodes.join(", ")}`;

//     document.getElementById("scenario_mitre").innerHTML =
//         `<strong>MITRE:</strong> ${sc.mitre.join(", ")}`;

//     const phasesEl = document.getElementById("scenario_phases");
//     phasesEl.innerHTML = "";
//     sc.phases.forEach(p => {
//         const li = document.createElement("li");
//         li.textContent = p;
//         phasesEl.appendChild(li);
//     });
// }

// function drawGraph() {
//     const sc = CURRENT;
//     const svg = document.getElementById("scenario_svg");

//     while (svg.firstChild) svg.removeChild(svg.firstChild);

//     const nodes = sc.nodes;
//     const edges = sc.edges;

//     const width = 900, height = 550;
//     const cx = width / 2, cy = height / 2;
//     const radius = 200;
//     const TWO_PI = Math.PI * 2;

//     // Arrow marker
//     const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
//     const marker = document.createElementNS("http://www.w3.org/2000/svg", "marker");
//     marker.setAttribute("id", "arrow");
//     marker.setAttribute("markerWidth", "10");
//     marker.setAttribute("markerHeight", "7");
//     marker.setAttribute("refX", "10");
//     marker.setAttribute("refY", "3.5");
//     marker.setAttribute("orient", "auto");

//     const mp = document.createElementNS("http://www.w3.org/2000/svg", "path");
//     mp.setAttribute("d", "M0,0 L10,3.5 L0,7Z");
//     mp.setAttribute("fill", "#00ff99");

//     marker.appendChild(mp);
//     defs.appendChild(marker);
//     svg.appendChild(defs);

//     // Compute radial node positions
//     const pos = {};
//     nodes.forEach((host, i) => {
//         const angle = i * TWO_PI / nodes.length;
//         pos[host] = {
//             x: cx + radius * Math.cos(angle),
//             y: cy + radius * Math.sin(angle)
//         };
//     });

//     // Draw edges
//     edges.forEach(edge => {
//         const src = pos[edge.src];
//         const dst = pos[edge.dst];
//         if (!src || !dst) return;

//         // MAIN ARROW LINE
//         const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
//         line.setAttribute("x1", src.x);
//         line.setAttribute("y1", src.y);
//         line.setAttribute("x2", dst.x);
//         line.setAttribute("y2", dst.y);
//         line.setAttribute("stroke", "#00ff99");
//         line.setAttribute("stroke-width", "2");
//         line.setAttribute("marker-end", "url(#arrow)");
//         svg.appendChild(line);

//         // LABEL OFFSET = perpendicular shift
//         const mx = (src.x + dst.x) / 2;
//         const my = (src.y + dst.y) / 2;

//         const lx = mx + (dst.y - src.y) * 0.15;  // rotate/offset
//         const ly = my - (dst.x - src.x) * 0.15;

//         const lbl = document.createElementNS("http://www.w3.org/2000/svg", "text");
//         lbl.setAttribute("x", lx);
//         lbl.setAttribute("y", ly);
//         lbl.setAttribute("fill", "#ddd");
//         lbl.setAttribute("font-size", "12");
//         lbl.setAttribute("text-anchor", "middle");
//         lbl.textContent = edge.label;
//         svg.appendChild(lbl);
//     });

//     // Draw nodes
//     nodes.forEach(host => {
//         const { x, y } = pos[host];

//         const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
//         circle.setAttribute("cx", x);
//         circle.setAttribute("cy", y);
//         circle.setAttribute("r", 28);
//         circle.setAttribute("fill", "#0d1117");
//         circle.setAttribute("stroke", "#00ff99");
//         circle.setAttribute("stroke-width", "2.5");
//         svg.appendChild(circle);

//         const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
//         text.setAttribute("x", x);
//         text.setAttribute("y", y + 5);
//         text.setAttribute("fill", "#fff");
//         text.setAttribute("font-size", "13");
//         text.setAttribute("text-anchor", "middle");
//         text.textContent = host;
//         svg.appendChild(text);
//     });
// }



let SCENARIOS = [];
let CURRENT = null;

// Load scenarios on page ready
window.addEventListener("DOMContentLoaded", async () => {
    try {
        const res = await fetch("/api/load_scenarios");
        const data = await res.json();
        SCENARIOS = data.scenarios || [];

        const listEl = document.getElementById("scenario_list");
        listEl.innerHTML = "";

        SCENARIOS.forEach((sc, idx) => {
            const card = document.createElement("div");
            card.className = "scenario-card";
            card.onclick = () => selectScenario(idx);

            card.innerHTML = `
                <h3>${sc.id}</h3>
                <p>${sc.name}</p>
            `;
            listEl.appendChild(card);
        });

    } catch (e) {
        console.error("Error loading scenarios:", e);
    }
});

function selectScenario(idx) {
    CURRENT = SCENARIOS[idx];
    if (!CURRENT) return;

    document.querySelectorAll(".scenario-card").forEach((c, i) =>
        c.classList.toggle("active", i === idx)
    );

    updateDetails();
    drawGraph();
}

function updateDetails() {
    const sc = CURRENT;

    document.getElementById("scenario_title").innerText = `${sc.id} – ${sc.name}`;
    document.getElementById("scenario_desc").innerText = sc.description;

    document.getElementById("scenario_hosts").innerHTML =
        `<strong>Hosts:</strong> ${sc.nodes.join(", ")}`;

    document.getElementById("scenario_mitre").innerHTML =
        `<strong>MITRE:</strong> ${sc.mitre.join(", ")}`;

    const phasesEl = document.getElementById("scenario_phases");
    phasesEl.innerHTML = "";
    sc.phases.forEach(p => {
        const li = document.createElement("li");
        li.textContent = p;
        phasesEl.appendChild(li);
    });

    // Reset selection box text
    const selBox = document.getElementById("scenario_selection");
    if (selBox) {
        selBox.innerHTML = "Click a node or edge in the graph to see details.";
    }
}

/* ---------- Selection helper ---------- */
function setSelectionHTML(html) {
    const selBox = document.getElementById("scenario_selection");
    if (selBox) {
        selBox.innerHTML = html;
    }
}

/* ---------- Node / Edge click handlers ---------- */
function onNodeClick(host) {
    if (!CURRENT) return;
    const sc = CURRENT;
    const svg = document.getElementById("scenario_svg");

    // Clear previous highlights
    svg.querySelectorAll(".scenario-node-group").forEach(g =>
        g.classList.remove("active-node")
    );
    svg.querySelectorAll(".scenario-edge").forEach(e =>
        e.classList.remove("active-edge")
    );

    // Highlight this node group
    const targetGroup = svg.querySelector(`.scenario-node-group[data-host="${host}"]`);
    if (targetGroup) {
        targetGroup.classList.add("active-node");
    }

    // Build info for this host
    const outgoing = sc.edges.filter(e => e.src === host);
    const incoming = sc.edges.filter(e => e.dst === host);

    let role = "Isolated";
    if (incoming.length === 0 && outgoing.length > 0) role = "Entry / Attack Source";
    else if (incoming.length > 0 && outgoing.length > 0) role = "Pivot / Lateral Hop";
    else if (incoming.length > 0 && outgoing.length === 0) role = "Final Target / Sink";

    let html = `<strong>Node:</strong> ${host}<br><strong>Role:</strong> ${role}<br><br>`;

    if (incoming.length) {
        html += `<strong>Incoming from:</strong><ul>`;
        incoming.forEach(e => {
            html += `<li>${e.src} → ${host} : ${e.label}</li>`;
        });
        html += `</ul>`;
    }

    if (outgoing.length) {
        html += `<strong>Outgoing to:</strong><ul>`;
        outgoing.forEach(e => {
            html += `<li>${host} → ${e.dst} : ${e.label}</li>`;
        });
        html += `</ul>`;
    }

    setSelectionHTML(html);
}

function onEdgeClick(edge) {
    if (!CURRENT) return;
    const svg = document.getElementById("scenario_svg");

    // Reset all highlights
    svg.querySelectorAll(".scenario-node-group").forEach(g =>
        g.classList.remove("active-node")
    );
    svg.querySelectorAll(".scenario-edge").forEach(e =>
        e.classList.remove("active-edge")
    );

    // Highlight matching edge line
    svg.querySelectorAll(".scenario-edge").forEach(e => {
        if (e.dataset.src === edge.src &&
            e.dataset.dst === edge.dst &&
            e.dataset.label === edge.label) {
            e.classList.add("active-edge");
        }
    });

    let html = `
        <strong>Edge:</strong> ${edge.src} → ${edge.dst}<br>
        <strong>Action:</strong> ${edge.label}
    `;
    setSelectionHTML(html);
}

/* ---------- Graph drawing with animation ---------- */
function drawGraph() {
    const sc = CURRENT;
    const svg = document.getElementById("scenario_svg");

    while (svg.firstChild) svg.removeChild(svg.firstChild);

    const nodes = sc.nodes;
    const edges = sc.edges;

    const width = 900, height = 550;
    const cx = width / 2, cy = height / 2;
    const radius = 200;
    const TWO_PI = Math.PI * 2;

    const svgNS = "http://www.w3.org/2000/svg";

    // Arrow marker
    const defs = document.createElementNS(svgNS, "defs");
    const marker = document.createElementNS(svgNS, "marker");
    marker.setAttribute("id", "arrow");
    marker.setAttribute("markerWidth", "10");
    marker.setAttribute("markerHeight", "7");
    marker.setAttribute("refX", "10");
    marker.setAttribute("refY", "3.5");
    marker.setAttribute("orient", "auto");

    const mp = document.createElementNS(svgNS, "path");
    mp.setAttribute("d", "M0,0 L10,3.5 L0,7Z");
    mp.setAttribute("fill", "#00ff99");

    marker.appendChild(mp);
    defs.appendChild(marker);
    svg.appendChild(defs);

    // Compute radial node positions
    const pos = {};
    nodes.forEach((host, i) => {
        const angle = i * TWO_PI / nodes.length;
        pos[host] = {
            x: cx + radius * Math.cos(angle),
            y: cy + radius * Math.sin(angle)
        };
    });

    // Draw edges (animated)
    edges.forEach(edge => {
        const src = pos[edge.src];
        const dst = pos[edge.dst];
        if (!src || !dst) return;

        // Main line
        const line = document.createElementNS(svgNS, "line");
        line.setAttribute("x1", src.x);
        line.setAttribute("y1", src.y);
        line.setAttribute("x2", dst.x);
        line.setAttribute("y2", dst.y);
        line.setAttribute("stroke", "#00ff99");
        line.setAttribute("stroke-width", "2");
        line.setAttribute("marker-end", "url(#arrow)");
        line.classList.add("scenario-edge");
        line.dataset.src = edge.src;
        line.dataset.dst = edge.dst;
        line.dataset.label = edge.label;
        line.style.cursor = "pointer";
        line.addEventListener("click", () => onEdgeClick(edge));
        svg.appendChild(line);

        // Label, slightly offset from the line
        const mx = (src.x + dst.x) / 2;
        const my = (src.y + dst.y) / 2;

        const lx = mx + (dst.y - src.y) * 0.15;
        const ly = my - (dst.x - src.x) * 0.15;

        const lbl = document.createElementNS(svgNS, "text");
        lbl.setAttribute("x", lx);
        lbl.setAttribute("y", ly);
        lbl.setAttribute("fill", "#ddd");
        lbl.setAttribute("font-size", "12");
        lbl.setAttribute("text-anchor", "middle");
        lbl.textContent = edge.label;
        lbl.style.cursor = "pointer";
        lbl.addEventListener("click", () => onEdgeClick(edge));
        svg.appendChild(lbl);
    });

    // Draw nodes (group = circle + text, animated)
    nodes.forEach(host => {
        const { x, y } = pos[host];

        const group = document.createElementNS(svgNS, "g");
        group.classList.add("scenario-node-group");
        group.dataset.host = host;
        group.style.cursor = "pointer";
        group.addEventListener("click", () => onNodeClick(host));

        const circle = document.createElementNS(svgNS, "circle");
        circle.setAttribute("cx", x);
        circle.setAttribute("cy", y);
        circle.setAttribute("r", 28);
        circle.setAttribute("fill", "#0d1117");
        circle.setAttribute("stroke", "#00ff99");
        circle.setAttribute("stroke-width", "2.5");
        circle.classList.add("scenario-node-circle");

        const text = document.createElementNS(svgNS, "text");
        text.setAttribute("x", x);
        text.setAttribute("y", y + 5);
        text.setAttribute("fill", "#fff");
        text.setAttribute("font-size", "13");
        text.setAttribute("text-anchor", "middle");
        text.textContent = host;

        group.appendChild(circle);
        group.appendChild(text);
        svg.appendChild(group);
    });
}
