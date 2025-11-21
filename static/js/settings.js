// Show/hide custom model input
document.getElementById("api_model").addEventListener("change", function () {
    const custom = document.getElementById("custom_model_block");
    if (this.value === "custom") {
        custom.style.display = "block";
    } else {
        custom.style.display = "none";
    }
});

// Load YAML files on page load
window.addEventListener("DOMContentLoaded", () => {
    loadYamlFiles();
});

// Fetch YAML files from backend
async function loadYamlFiles() {
    const sel = document.getElementById("topo_file");

    sel.innerHTML = `
        <option value="">-- Select YAML file from configs/ --</option>
    `;

    try {
        const res = await fetch("/api/list_yaml_files");
        const files = await res.json();

        files.forEach(path => {
            const opt = document.createElement("option");
            opt.value = path;
            opt.textContent = path;
            sel.appendChild(opt);
        });

    } catch (e) {
        console.error("YAML listing failed:", e);
    }
}

function saveSettings() {
    let model = document.getElementById("api_model").value;
    if (model === "custom") {
        model = document.getElementById("custom_model_name").value.trim();
        if (!model) {
            alert("Enter custom model name.");
            return;
        }
    }

    const payload = {
        api_model: model,
        base_folder: document.getElementById("base_folder").value,
        dataset_folder: document.getElementById("dataset_folder").value,
        config_folder: document.getElementById("config_folder").value,
        topo_file: document.getElementById("topo_file").value
    };

    fetch("/api/save_settings", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    }).then(() => {
        alert("Settings saved successfully.");
    });
}
