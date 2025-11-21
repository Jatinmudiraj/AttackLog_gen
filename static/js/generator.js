// // Load prompt files at page load
// window.onload = function () {
//     loadLogFiles("prompt_file");
//     loadPromptTemplates("scenario_prompt");

//     // Auto-fill output file when prompt changes
//     const pfSel = document.getElementById("prompt_file");
//     if (pfSel) {
//         pfSel.addEventListener("change", function () {
//             const pf = this.value;
//             if (pf) {
//                 const out = pf.replace("_org", "_gen");
//                 const outInput = document.getElementById("output_file");
//                 if (outInput) {
//                     outInput.value = out;
//                 }
//             }
//         });
//     }
// };


// // MAIN GENERATE FUNCTION WITH LOADER
// async function generate() {

//     // Validate prompt file (base logs)
//     const promptFile = requireFile("prompt_file");
//     const outputFile = document.getElementById("output_file").value.trim();

//     if (!outputFile) {
//         alert("Output file cannot be empty!");
//         return;
//     }

//     const scenarioSelect = document.getElementById("scenario_prompt");
//     const templateFile = scenarioSelect ? scenarioSelect.value.trim() : "";

//     // Prepare payload
//     const payload = {
//         prompt_file: promptFile,
//         output_file: outputFile,

//         template_file: templateFile,  // new: scenario/high-level prompt

//         log_type: document.getElementById("log_type").value,
//         hostname: document.getElementById("hostname").value,

//         temperature: parseFloat(document.getElementById("temp").value),
//         top_p: parseFloat(document.getElementById("top_p").value),
//         max_tokens: parseInt(document.getElementById("max_tok").value, 10),
//         num_lines: parseInt(document.getElementById("num_lines").value, 10),

//         noise: document.getElementById("noise").value,
//         seed: document.getElementById("seed").value,
//         ip_range: document.getElementById("ip_range").value,
//         pid_range: document.getElementById("pid_range").value,
//         date_range: document.getElementById("date_range").value
//     };

//     // Disable button + show loader
//     const btn = document.getElementById("generate_btn");
//     if (btn) {
//         btn.disabled = true;
//     }
//     showLoader("Generating Logs...");

//     try {
//         const res = await fetch("/api/generate_logs", {
//             method: "POST",
//             headers: {"Content-Type": "application/json"},
//             body: JSON.stringify(payload)
//         });

//         const out = await res.json();

//         // Handle backend errors
//         if (!res.ok || out.error) {
//             alert(out.error || "Log generation failed.");
//             return;
//         }

//         // Display logs
//         document.getElementById("preview").innerText = out.preview.join("\n");
//         document.getElementById("log_count").innerText =
//             out.preview.length + " lines";

//     } catch (err) {
//         console.error("Generation error:", err);
//         alert("Network or server error while generating logs.");
//     } finally {
//         // Re-enable button and hide loader
//         if (btn) {
//             btn.disabled = false;
//         }
//         hideLoader();
//     }
// }


// // BUTTON FUNCTIONS

// function clearLogs() {
//     document.getElementById("preview").innerText = "";
//     document.getElementById("log_count").innerText = "0 lines";
// }

// function copyLogs() {
//     navigator.clipboard.writeText(
//         document.getElementById("preview").innerText
//     );
// }

// function downloadLogs() {
//     const text = document.getElementById("preview").innerText;
//     const elem = document.createElement("a");
//     elem.setAttribute(
//         "href",
//         "data:text/plain;charset=utf-8," + encodeURIComponent(text)
//     );
//     elem.setAttribute("download", "generated_logs.txt");
//     elem.click();
// }



// static/js/generator.js

// Load prompt files and scenario templates at page load
window.onload = function () {
    // Base logs
    loadLogFiles("prompt_file");

    // Scenario / high-level prompt templates (e.g., from configs/prompt_templates)
    if (typeof loadPromptTemplates === "function") {
        loadPromptTemplates("scenario_prompt");
    }

    // Auto-fill output file when prompt changes
    const pfSel = document.getElementById("prompt_file");
    if (pfSel) {
        pfSel.addEventListener("change", function () {
            const pf = this.value;
            if (pf) {
                const out = pf.replace("_org", "_gen");
                const outInput = document.getElementById("output_file");
                if (outInput) {
                    outInput.value = out;
                }
            }
        });
    }
};


// MAIN GENERATE FUNCTION WITH LOADER + MEMORY
async function generate() {

    // Validate prompt file (base logs)
    const promptFile = requireFile("prompt_file");
    const outputFile = document.getElementById("output_file").value.trim();

    if (!outputFile) {
        alert("Output file cannot be empty!");
        return;
    }

    // Scenario / high-level prompt template
    const scenarioSelect = document.getElementById("scenario_prompt");
    const templateFile = scenarioSelect ? scenarioSelect.value.trim() : "";

    // Use output file as memory id so multiple runs for same file share context
    const memoryId = outputFile || promptFile;

    // Prepare payload
    const payload = {
        prompt_file: promptFile,
        output_file: outputFile,

        // NEW: scenario / high-level prompt template
        template_file: templateFile,

        log_type: document.getElementById("log_type").value,
        hostname: document.getElementById("hostname").value,

        temperature: parseFloat(document.getElementById("temp").value),
        top_p: parseFloat(document.getElementById("top_p").value),
        max_tokens: parseInt(document.getElementById("max_tok").value, 10),
        num_lines: parseInt(document.getElementById("num_lines").value, 10),

        noise: document.getElementById("noise").value,
        seed: document.getElementById("seed").value,
        ip_range: document.getElementById("ip_range").value,
        pid_range: document.getElementById("pid_range").value,
        date_range: document.getElementById("date_range").value,

        // NEW: memory id for LLM-side context
        memory_id: memoryId
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
        const previewEl = document.getElementById("preview");
        const countEl = document.getElementById("log_count");

        if (previewEl) {
            previewEl.innerText = out.preview.join("\n");
        }
        if (countEl) {
            countEl.innerText = out.preview.length + " lines";
        }

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
    const previewEl = document.getElementById("preview");
    const countEl = document.getElementById("log_count");

    if (previewEl) previewEl.innerText = "";
    if (countEl) countEl.innerText = "0 lines";
}

function copyLogs() {
    const previewEl = document.getElementById("preview");
    if (!previewEl) return;

    navigator.clipboard.writeText(previewEl.innerText);
}

function downloadLogs() {
    const previewEl = document.getElementById("preview");
    if (!previewEl) return;

    const text = previewEl.innerText;
    const elem = document.createElement("a");
    elem.setAttribute(
        "href",
        "data:text/plain;charset=utf-8," + encodeURIComponent(text)
    );
    elem.setAttribute("download", "generated_logs.txt");
    elem.click();
}

