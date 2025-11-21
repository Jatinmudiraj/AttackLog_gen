// static/js/cleaner.js

// On page load: populate input dropdown, set up auto-fill for output path
window.addEventListener("DOMContentLoaded", () => {
    // Populate input file list
    loadLogFiles("input_file");

    // When input file changes, auto-fill output file path
    const inputSel = document.getElementById("input_file");
    const outInput = document.getElementById("output_file");

    if (inputSel && outInput) {
        inputSel.addEventListener("change", () => {
            const val = inputSel.value.trim();
            if (!val) {
                outInput.value = "";
                return;
            }

            // Keep same folder, add "_cleaned" before extension
            const dot = val.lastIndexOf(".");
            if (dot !== -1) {
                outInput.value = val.slice(0, dot) + "_cleaned" + val.slice(dot);
            } else {
                outInput.value = val + "_cleaned.txt";
            }
        });
    }
});

async function cleanFile() {
    let inputPath;
    try {
        inputPath = requireFile("input_file");
    } catch {
        return;
    }

    const outInput = document.getElementById("output_file");
    const modeSel = document.getElementById("clean_mode");

    const payload = {
        input: inputPath,
        output: outInput.value.trim(),
        mode: modeSel.value.trim(),
    };

    showLoader("Cleaning Logs...");

    try {
        const res = await fetch("/api/clean_logs", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const out = await res.json();

        if (!res.ok || out.error) {
            alert(out.error || "Cleaning failed.");
            return;
        }

        const lines = out.preview || [];
        document.getElementById("clean_preview").innerText = lines.join("\n");
        document.getElementById("clean_count").innerText = lines.length + " lines";
    } catch (e) {
        alert("Server or network error.");
    } finally {
        hideLoader();
    }
}


function copyClean() {
    const text = document.getElementById("clean_preview").innerText;
    if (!text) {
        alert("Nothing to copy.");
        return;
    }
    navigator.clipboard.writeText(text);
}

function downloadClean() {
    const text = document.getElementById("clean_preview").innerText;
    if (!text) {
        alert("Nothing to download.");
        return;
    }

    const elem = document.createElement("a");
    elem.setAttribute(
        "href",
        "data:text/plain;charset=utf-8," + encodeURIComponent(text)
    );
    elem.setAttribute("download", "cleaned_logs.txt");
    document.body.appendChild(elem);
    elem.click();
    document.body.removeChild(elem);
}

function clearClean() {
    document.getElementById("clean_preview").innerText = "";
    document.getElementById("clean_count").innerText = "0 lines";
}
