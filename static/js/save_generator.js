// Load prompt files at page load
window.onload = function () {
    loadLogFiles("prompt_file");

    // Auto-fill output file when prompt changes
    document.getElementById("prompt_file").addEventListener("change", function () {
        const pf = this.value;
        if (pf) {
            const out = pf.replace("_org", "_gen");
            document.getElementById("output_file").value = out;
        }
    });
};


// MAIN GENERATE FUNCTION WITH LOADER
async function generate() {

    // Validate prompt file
    const promptFile = requireFile("prompt_file");
    const outputFile = document.getElementById("output_file").value.trim();

    if (!outputFile) {
        alert("Output file cannot be empty!");
        return;
    }

    // Prepare payload
    const payload = {
        prompt_file: promptFile,
        output_file: outputFile,

        log_type: document.getElementById("log_type").value,
        hostname: document.getElementById("hostname").value,

        temperature: parseFloat(document.getElementById("temp").value),
        top_p: parseFloat(document.getElementById("top_p").value),
        max_tokens: parseInt(document.getElementById("max_tok").value),
        num_lines: parseInt(document.getElementById("num_lines").value),

        noise: document.getElementById("noise").value,
        seed: document.getElementById("seed").value,
        ip_range: document.getElementById("ip_range").value,
        pid_range: document.getElementById("pid_range").value,
        date_range: document.getElementById("date_range").value
    };

    // Disable button + show loader
    const btn = document.getElementById("generate_btn");
    if (btn) {
        btn.disabled = true;
    }
    showLoader("Generating Logs...");

    try {
        const res = await fetch("/api/generate_logs", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });

        const out = await res.json();

        // Handle backend errors
        if (!res.ok || out.error) {
            alert(out.error || "Log generation failed.");
            return;
        }

        // Display logs
        document.getElementById("preview").innerText = out.preview.join("\n");
        document.getElementById("log_count").innerText =
            out.preview.length + " lines";

    } catch (err) {
        console.error("Generation error:", err);
        alert("Network or server error while generating logs.");
    } finally {
        // Re-enable button and hide loader
        if (btn) {
            btn.disabled = false;
        }
        hideLoader();
    }
}


// BUTTON FUNCTIONS

function clearLogs() {
    document.getElementById("preview").innerText = "";
    document.getElementById("log_count").innerText = "0 lines";
}

function copyLogs() {
    navigator.clipboard.writeText(
        document.getElementById("preview").innerText
    );
}

function downloadLogs() {
    const text = document.getElementById("preview").innerText;
    const elem = document.createElement("a");
    elem.setAttribute(
        "href",
        "data:text/plain;charset=utf-8," + encodeURIComponent(text)
    );
    elem.setAttribute("download", "generated_logs.txt");
    elem.click();
}
