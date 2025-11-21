let MITRE = {};
let CURRENT = null;

window.addEventListener("DOMContentLoaded", () => {
    loadMITRE();
});

/* ================= LOAD YAML ================= */
async function loadMITRE() {
    try {
        const res = await fetch("/mitre_yaml");
        const text = await res.text();

        const parsed = jsyaml.load(text);
        MITRE = parsed.techniques || {};

        renderTechniqueList();

    } catch (err) {
        console.error("MITRE load error:", err);
    }
}

/* ================= LIST VIEW ================= */
function renderTechniqueList() {
    const listEl = document.getElementById("mitre_list");
    listEl.innerHTML = "";

    Object.keys(MITRE).forEach(id => {
        const t = MITRE[id];

        const card = document.createElement("div");
        card.className = "mitre-card";
        card.onclick = () => showTechnique(id);

        card.innerHTML = `
            <div class="mitre-id">${id}</div>
            <div class="mitre-name">${t.name}</div>
            <div class="mitre-tactic">${t.tactic}</div>
        `;

        listEl.appendChild(card);
    });
}

/* ================= SEARCH ================= */
function filterTechniques() {
    const q = document.getElementById("mitre_search").value.toLowerCase();

    document.querySelectorAll(".mitre-card").forEach(card => {
        card.style.display = card.innerText.toLowerCase().includes(q)
            ? "block"
            : "none";
    });
}

/* ================= DETAILS PANEL ================= */
function showTechnique(id) {
    CURRENT = MITRE[id];
    highlightCard(id);
    updateDetails(id);
    drawGraph(id);
}

function highlightCard(id) {
    document.querySelectorAll(".mitre-card").forEach(card => {
        card.classList.toggle("active", card.innerText.includes(id));
    });
}

/* ================= DETAILS RENDER ================= */
function updateDetails(id) {
    const t = MITRE[id];

    document.getElementById("mitre_details").innerHTML = `
        <h2>${id} — ${t.name}</h2>
        <p>${t.description}</p>

        <h4>Tactic</h4>
        <p class="badge">${t.tactic}</p>

        <h4>Keywords</h4>
        <div class="keyword-box">${t.keywords.join(", ")}</div>

        <h4>Detection Logic</h4>
        <pre class="detect-box">${t.detection.logic}</pre>

        <h4>Examples</h4>
        <pre class="example-box">${t.examples.join("\n")}</pre>
    `;
}

/* ================= GRAPH RENDER ================= */
function drawGraph(id) {
    const svg = document.getElementById("mitre_svg");
    svg.innerHTML = "";

    const t = MITRE[id];
    const cx = 450, cy = 200;

    const nodes = [
        { label: t.tactic, y: cy - 100 },
        { label: id,       y: cy },
        { label: t.name,   y: cy + 100 }
    ];

    nodes.forEach(n => {
        drawNode(svg, cx, n.y, n.label);
    });

    drawArrow(svg, cx, cy - 60, cx, cy - 20);
    drawArrow(svg, cx, cy + 20, cx, cy + 60);
}

function drawNode(svg, x, y, text) {
    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", x - 150);
    rect.setAttribute("y", y - 20);
    rect.setAttribute("width", 300);
    rect.setAttribute("height", 40);
    rect.setAttribute("rx", 10);
    rect.setAttribute("fill", "#0d1117");
    rect.setAttribute("stroke", "#00ffaa");
    rect.setAttribute("stroke-width", "2");
    svg.appendChild(rect);

    const lbl = document.createElementNS("http://www.w3.org/2000/svg", "text");
    lbl.setAttribute("x", x);
    lbl.setAttribute("y", y + 5);
    lbl.setAttribute("fill", "white");
    lbl.setAttribute("text-anchor", "middle");
    lbl.textContent = text;
    svg.appendChild(lbl);
}

function drawArrow(svg, x1, y1, x2, y2) {
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", x1);
    line.setAttribute("y1", y1);
    line.setAttribute("x2", x2);
    line.setAttribute("y2", y2);
    line.setAttribute("stroke", "#00ffaa");
    line.setAttribute("stroke-width", "2");
    svg.appendChild(line);
}
