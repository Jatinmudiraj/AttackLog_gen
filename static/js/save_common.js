// static/js/common.js

// Populate a <select> with all log files from the server
async function loadLogFiles(selectId) {
    const sel = document.getElementById(selectId);
    if (!sel) return;

    // Clear old options
    sel.innerHTML = "";

    // Default option
    const def = document.createElement("option");
    def.value = "";
    def.textContent = "-- Select a log file --";
    sel.appendChild(def);

    try {
        const res = await fetch("/api/list_prompt_files");
        const files = await res.json();

        if (!Array.isArray(files)) return;

        files.forEach((path) => {
            const opt = document.createElement("option");
            opt.value = path;
            opt.textContent = path;
            sel.appendChild(opt);
        });
    } catch (err) {
        console.error("Error loading log files:", err);
        const opt = document.createElement("option");
        opt.value = "";
        opt.textContent = "Error loading files";
        sel.appendChild(opt);
    }
}

// Ensure a file is selected in a <select>, else alert + throw
function requireFile(selectId) {
    const sel = document.getElementById(selectId);
    if (!sel) {
        throw new Error(`Select element '${selectId}' not found`);
    }
    const val = sel.value.trim();
    if (!val) {
        alert("Please select a file first.");
        throw new Error("File not selected");
    }
    return val;
}
// GLOBAL LOADER CONTROL
function showLoader(text = "Processing...") {
    const overlay = document.getElementById("loading-overlay");
    const t = document.querySelector(".loader-text");
    if (t) t.innerText = text;
    overlay.style.display = "flex";
}

function hideLoader() {
    const overlay = document.getElementById("loading-overlay");
    overlay.style.display = "none";
}
