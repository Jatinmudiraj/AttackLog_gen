function selectFile(inputId, outputId) {
    const picker = document.getElementById(inputId);
    const text = document.getElementById(outputId);

    if (picker.files.length > 0) {
        text.value = picker.files[0].path || picker.files[0].name;
    }
}

async function loadTimeline() {
    const file = document.getElementById("tl_file").value.trim();
    if (!file) return alert("Select a log file first!");

    const res = await fetch("/api/timeline", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ file })
    });

    let events = await res.json();

    if (events.error) {
        document.getElementById("timeline_box").innerHTML =
            `<p style="color:red">${events.error}</p>`;
        return;
    }

    renderTimeline(events);
}

function renderTimeline(events) {
    const box = document.getElementById("timeline_box");
    box.innerHTML = "";

    events.forEach(ev => {
        const severity = classifySeverity(ev.text);
        const dotClass = {
            info: "timeline-severity-info",
            warn: "timeline-severity-warn",
            critical: "timeline-severity-critical"
        }[severity];

        const div = document.createElement("div");
        div.className = "timeline-event";

        div.innerHTML = `
            <div class="timeline-dot ${dotClass}"></div>
            <div class="timeline-content">
                <div class="timeline-time">${extractTime(ev.text)}</div>
                <div class="timeline-text">${ev.text}</div>
            </div>
        `;

        box.appendChild(div);
    });
}

function extractTime(line) {
    const match = line.match(/^[A-Za-z]{3}\s+\d+\s+\d+:\d+:\d+/);
    return match ? match[0] : "Unknown Time";
}

function classifySeverity(line) {
    const lower = line.toLowerCase();

    if (lower.includes("failed password") ||
        lower.includes("permission denied") ||
        lower.includes("invalid user"))
        return "critical";

    if (lower.includes("sudo") ||
        lower.includes("session opened") ||
        lower.includes("accepted password"))
        return "warn";

    return "info";
}

function filterTimeline() {
    const query = document.getElementById("tl_search").value.toLowerCase();

    document.querySelectorAll(".timeline-event").forEach(ev => {
        const txt = ev.innerText.toLowerCase();
        const visible = txt.includes(query);

        ev.style.display = visible ? "flex" : "none";

        // Highlight matching text
        const content = ev.querySelector(".timeline-text");
        const raw = content.innerText;

        if (query && visible) {
            const regex = new RegExp(`(${query})`, "gi");
            content.innerHTML = raw.replace(regex, `<span class="highlight">$1</span>`);
        } else {
            content.innerText = raw;
        }
    });
}
