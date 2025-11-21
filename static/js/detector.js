// Load log files on page load
window.addEventListener("DOMContentLoaded", () => {
    loadLogFiles("det_file");
});

async function runDetection() {
    let file;
    try {
        file = requireFile("det_file"); // ensures not empty
    } catch {
        return; // already alerted
    }

    const mode = document.getElementById("det_mode").value;
    const clf = document.getElementById("clf_path").value.trim();

    const payload = {
        file,
        mode,
        classifier: clf
    };

    const btn = document.getElementById("detect_btn");
    if (btn) btn.disabled = true;

    showLoader("Running Detection...");

    try {
        const res = await fetch("/api/detect", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });

        const out = await res.json();

        if (!res.ok || out.error) {
            document.getElementById("det_results").innerText =
                out.error || "Detection failed.";
            hideLoader();
            if (btn) btn.disabled = false;
            return;
        }

        const results = out.results || [];

        if (results.length === 0) {
            document.getElementById("det_results").innerHTML =
                "<p>No techniques detected.</p>";
            hideLoader();
            if (btn) btn.disabled = false;
            return;
        }

        let html = `
            <table class="det-table">
                <tr>
                    <th>Line</th>
                    <th>Technique ID</th>
                    <th>Technique Name</th>
                </tr>
        `;

        results.forEach(r => {
            html += `
                <tr>
                    <td>${r.line}</td>
                    <td class="tech-id">${r.tech_id}</td>
                    <td>${r.name}</td>
                </tr>
            `;
        });

        html += "</table>";

        document.getElementById("det_results").innerHTML = html;

    } catch (err) {
        console.error("Detector error:", err);
        alert("Server or network error.");
    } finally {
        hideLoader();
        if (btn) btn.disabled = false;
    }
}
