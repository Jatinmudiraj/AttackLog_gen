# import os
# from typing import List, Dict
# import yaml
# from flask import Flask, render_template, request, jsonify
# from flask import send_file, make_response
# from config import BASE_LOG_FOLDER, CONFIG_FOLDER
# from utils.llm_api import generate_logs_via_api
# # from utils.cleaner_utils import clean_openssh_file
# from utils.cleaner_utils import clean_log_file
# from utils.detector_utils import detect_mitre
# from utils.scenario_utils import load_scenarios
# import json

# SETTINGS_FILE = "app_settings.json"
# app = Flask(__name__)


# # =========================
# # Helper Functions
# # =========================

# def list_log_files(root: str) -> List[str]:
#     """
#     Recursively list all .txt and .log files under root.
#     Returned paths are relative to the project root.
#     """
#     paths: List[str] = []
#     if not os.path.exists(root):
#         return paths

#     for folder, dirs, files in os.walk(root):
#         for f in files:
#             if f.endswith(".txt") or f.endswith(".log"):
#                 rel = os.path.join(folder, f)
#                 paths.append(rel.replace("\\", "/"))
#     return sorted(paths)


# # =========================
# # Page Routes
# # =========================

# @app.route("/")
# def index():
#     # Your dashboard template; change name here if your file is different
#     return render_template("dashboard.html")





# @app.route("/mitre_yaml")
# def mitre_yaml():
#     try:
#         with open("configs/mitre_map.yaml", "r") as f:
#             content = f.read()

#         # Send YAML as text/plain so JS fetch() can parse it
#         response = make_response(content)
#         response.headers["Content-Type"] = "text/plain"
#         return response

#     except Exception as e:
#         return f"Error loading YAML: {e}", 500


# @app.route("/generator")
# def generator_page():
#     return render_template("generator.html")


# @app.route("/cleaner")
# def cleaner_page():
#     return render_template("cleaner.html")


# @app.route("/scenarios")
# def scenarios_page():
#     return render_template("scenarios.html")


# @app.route("/mitre")
# def mitre_page():
#     return render_template("mitre.html")


# @app.route("/timeline")
# def timeline_page():
#     return render_template("timeline.html")


# @app.route("/detector")
# def detector_page():
#     return render_template("detector.html")


# @app.route("/settings")
# def settings_page():
#     return render_template("settings.html")


# # =========================
# # API: List prompt files
# # Used by Generator dropdown
# # =========================

# @app.route("/api/list_prompt_files")
# def api_list_prompt_files():
#     files = list_log_files(BASE_LOG_FOLDER)
#     return jsonify(files)


# # =========================
# # API: Generate Logs
# # =========================

# @app.route("/api/generate_logs", methods=["POST"])
# def api_generate_logs():
#     data = request.json or {}

#     prompt_file = data.get("prompt_file", "").strip()
#     output_file = data.get("output_file", "").strip()

#     if not prompt_file:
#         return jsonify({"error": "prompt_file is required"}), 400

#     # Resolve prompt path
#     if not os.path.exists(prompt_file):
#         alt = os.path.join(BASE_LOG_FOLDER, prompt_file)
#         if os.path.exists(alt):
#             prompt_file = alt
#         else:
#             return jsonify({"error": f"Prompt file not found: {prompt_file}"}), 400

#     # Safe default output file if missing
#     if not output_file:
#         output_file = "generated_logs.txt"

#     # Ensure output directory exists
#     out_dir = os.path.dirname(output_file)
#     if out_dir and not os.path.exists(out_dir):
#         os.makedirs(out_dir, exist_ok=True)

#     # Read base prompt from file
#     with open(prompt_file, "r", encoding="utf-8", errors="ignore") as f:
#         base_prompt = f.read()

#     num_lines = int(data.get("num_lines", 100))
#     temperature = float(data.get("temperature", 0.7))
#     top_p = float(data.get("top_p", 0.95))
#     max_tokens = int(data.get("max_tokens", 400))
#     hostname = data.get("hostname", "LabHost")
#     log_type = data.get("log_type", "SSH")
#     ip_range = data.get("ip_range", "")
#     pid_range = data.get("pid_range", "")
#     date_range = data.get("date_range", "")
#     noise = str(data.get("noise", "0"))

#     lines = generate_logs_via_api(
#         prompt=base_prompt,
#         num_lines=num_lines,
#         temperature=temperature,
#         top_p=top_p,
#         max_tokens=max_tokens,
#         hostname=hostname,
#         log_type=log_type,
#         ip_range=ip_range,
#         pid_range=pid_range,
#         date_range=date_range,
#         noise=noise
#     )


#     # Save generated logs
#     with open(output_file, "w", encoding="utf-8") as f:
#         f.write("\n".join(lines))

#     return jsonify({"preview": lines})


# # =========================
# # API: Setting
# # =========================


# @app.route("/api/save_settings", methods=["POST"])
# def api_save_settings():
#     data = request.json or {}

#     with open(SETTINGS_FILE, "w") as f:
#         json.dump(data, f, indent=4)

#     return jsonify({"status": "ok"})

# # =========================
# # API: Clean Logs
# # =========================



# @app.route("/api/clean_logs", methods=["POST"])
# def api_clean_logs():
#     data = request.json or {}

#     inp = (data.get("input") or "").strip()
#     out = (data.get("output") or "").strip()
#     mode = (data.get("mode") or "sshd").strip()

#     if not inp:
#         return jsonify({"error": "input file is required"}), 400

#     # Resolve input path
#     if not os.path.exists(inp):
#         alt = os.path.join(BASE_LOG_FOLDER, inp)
#         if os.path.exists(alt):
#             inp = alt
#         else:
#             return jsonify({"error": f"Input file not found: {inp}"}), 400

#     if not out:
#         base, ext = os.path.splitext(inp)
#         out = base + "_cleaned" + ext

#     try:
#         preview = clean_log_file(inp, out, mode)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

#     return jsonify({"preview": preview})


# # @app.route("/api/clean_logs", methods=["POST"])
# # def api_clean_logs():
# #     data = request.json or {}

# #     inp = data.get("input", "").strip()
# #     out = data.get("output", "").strip()

# #     if not inp:
# #         return jsonify({"error": "input file is required"}), 400

# #     # Resolve input path
# #     if not os.path.exists(inp):
# #         alt = os.path.join(BASE_LOG_FOLDER, inp)
# #         if os.path.exists(alt):
# #             inp = alt
# #         else:
# #             return jsonify({"error": f"Input file not found: {inp}"}), 400

# #     # If output empty, we can put a default next to input
# #     if not out:
# #         base, ext = os.path.splitext(inp)
# #         out = base + "_cleaned" + ext

# #     try:
# #         preview = clean_openssh_file(inp, out)
# #     except FileNotFoundError as e:
# #         return jsonify({"error": str(e)}), 400

# #     return jsonify({"preview": preview})


# # =========================
# # API: Load Scenarios
# # =========================

# @app.route("/api/load_scenarios")
# def api_load_scenarios():
#     scenarios = load_scenarios()
#     return jsonify({"scenarios": scenarios})


# # =========================
# # API: Timeline
# # =========================

# @app.route("/api/timeline", methods=["POST"])
# def api_timeline():
#     data = request.json or {}
#     file_path = data.get("file", "").strip()

#     if not file_path:
#         return jsonify({"error": "file is required"}), 400

#     # 1. Direct path
#     if os.path.exists(file_path):
#         resolved = file_path
#     else:
#         # 2. Inside BASE_LOG_FOLDER
#         alt1 = os.path.join(BASE_LOG_FOLDER, file_path)
#         alt1 = alt1.replace("\\", "/")
#         if os.path.exists(alt1):
#             resolved = alt1
#         else:
#             # 3. If user only typed filename (OpenStack_gen.txt),
#             # search inside ALL system_logs subfolders
#             found = None
#             for root, dirs, files in os.walk(BASE_LOG_FOLDER):
#                 for f in files:
#                     if f == os.path.basename(file_path):
#                         found = os.path.join(root, f)
#                         break
#                 if found:
#                     break

#             if not found:
#                 return jsonify({"error": f"Timeline file not found: {file_path}"}), 400

#             resolved = found

#     # Read logs
#     with open(resolved, "r", encoding="utf-8", errors="ignore") as f:
#         lines = f.read().splitlines()

#     events = []
#     for i, line in enumerate(lines):
#         if line.strip():
#             events.append({"id": i + 1, "text": line})

#     return jsonify(events)


# # @app.route("/api/timeline", methods=["POST"])
# # def api_timeline():
# #     data = request.json or {}
# #     file_path = data.get("file", "").strip()

# #     if not file_path:
# #         return jsonify({"error": "file is required"}), 400

# #     # Resolve real path
# #     if not os.path.exists(file_path):
# #         alt = os.path.join(BASE_LOG_FOLDER, file_path)
# #         if os.path.exists(alt):
# #             file_path = alt
# #         else:
# #             return jsonify({"error": f"Timeline file not found: {file_path}"}), 400

# #     with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
# #         lines = f.read().splitlines()

# #     from utils.timeline_utils import compute_timeline
# #     events = compute_timeline(lines)

# #     return jsonify(events)



# # =========================
# # API: Detector (simple placeholder)
# # =========================

# @app.route("/api/detect", methods=["POST"])
# def api_detect():
#     data = request.json or {}

#     file = (data.get("file") or "").strip()
#     mode = (data.get("mode") or "rule").strip()
#     clf = (data.get("classifier") or "").strip()

#     if not file:
#         return jsonify({"error": "File is required"}), 400

#     # Resolve file path
#     if not os.path.exists(file):
#         alt = os.path.join(BASE_LOG_FOLDER, file)
#         if os.path.exists(alt):
#             file = alt
#         else:
#             return jsonify({"error": f"File not found: {file}"}), 400

#     with open(file, "r", encoding="utf-8", errors="ignore") as f:
#         lines = f.read().splitlines()

#     # Rule-based detection
#     if mode == "rule":
#         yaml_path = os.path.join(CONFIG_FOLDER, "mitre_map.yaml")
#         with open(yaml_path, "r") as y:
#             mitre = yaml.safe_load(y).get("techniques", {})

#         results = detect_mitre(lines, mitre)

#         return jsonify({"results": results})

#     # ML mode (future)
#     return jsonify({"results": []})

# @app.route("/api/mitre_map")
# def api_mitre_map():
#     yaml_path = os.path.join(CONFIG_FOLDER, "mitre_map.yaml")

#     if not os.path.exists(yaml_path):
#         return jsonify({"error": "mitre_map.yaml not found"}), 404

#     with open(yaml_path, "r", encoding="utf-8") as f:
#         data = yaml.safe_load(f)

#     return jsonify(data)



# @app.route("/api/list_yaml_files")
# def api_list_yaml_files():
#     yaml_files = []
#     cfg_dir = CONFIG_FOLDER

#     if os.path.exists(cfg_dir):
#         for f in os.listdir(cfg_dir):
#             if f.endswith(".yaml") or f.endswith(".yml"):
#                 yaml_files.append(f"{cfg_dir}/{f}")

#     return jsonify(yaml_files)


# # =========================
# # Main Entry
# # =========================

# if __name__ == "__main__":
#     # Bind to 0.0.0.0:8501 as in your logs
#     app.run(host="0.0.0.0", port=8501, debug=True)

import os
from typing import List, Dict
import yaml
from flask import Flask, render_template, request, jsonify
from flask import send_file, make_response
from config import BASE_LOG_FOLDER, CONFIG_FOLDER, PROMPT_TEMPLATE_FOLDER
from utils.llm_api import generate_logs_via_api
from utils.cleaner_utils import clean_log_file
from utils.detector_utils import detect_mitre
from utils.scenario_utils import load_scenarios
import json

SETTINGS_FILE = "app_settings.json"
app = Flask(__name__)


# =========================
# Helper Functions
# =========================

def list_log_files(root: str) -> List[str]:
    """
    Recursively list all .txt and .log files under root.
    Returned paths are relative to the project root.
    """
    paths: List[str] = []
    if not os.path.exists(root):
        return paths

    for folder, dirs, files in os.walk(root):
        for f in files:
            if f.endswith(".txt") or f.endswith(".log"):
                rel = os.path.join(folder, f)
                paths.append(rel.replace("\\", "/"))
    return sorted(paths)


# =========================
# Page Routes
# =========================

@app.route("/")
def index():
    # Your dashboard template; change name here if your file is different
    return render_template("dashboard.html")


@app.route("/mitre_yaml")
def mitre_yaml():
    try:
        with open("configs/mitre_map.yaml", "r") as f:
            content = f.read()

        # Send YAML as text/plain so JS fetch() can parse it
        response = make_response(content)
        response.headers["Content-Type"] = "text/plain"
        return response

    except Exception as e:
        return f"Error loading YAML: {e}", 500


@app.route("/generator")
def generator_page():
    return render_template("generator.html")


@app.route("/cleaner")
def cleaner_page():
    return render_template("cleaner.html")


@app.route("/scenarios")
def scenarios_page():
    return render_template("scenarios.html")


@app.route("/mitre")
def mitre_page():
    return render_template("mitre.html")


@app.route("/timeline")
def timeline_page():
    return render_template("timeline.html")


@app.route("/detector")
def detector_page():
    return render_template("detector.html")


@app.route("/settings")
def settings_page():
    return render_template("settings.html")


# =========================
# API: List prompt files (base logs)
# Used by Generator dropdown
# =========================

@app.route("/api/list_prompt_files")
def api_list_prompt_files():
    files = list_log_files(BASE_LOG_FOLDER)
    return jsonify(files)


# =========================
# API: List prompt templates (scenario/high-level prompts)
# =========================

@app.route("/api/list_prompt_templates")
def api_list_prompt_templates():
    files = list_log_files(PROMPT_TEMPLATE_FOLDER)
    return jsonify(files)


# =========================
# API: Generate Logs
# =========================


@app.route("/api/generate_logs", methods=["POST"])
def api_generate_logs():
    data = request.json or {}

    prompt_file = data.get("prompt_file", "").strip()
    output_file = data.get("output_file", "").strip()

    if not prompt_file:
        return jsonify({"error": "prompt_file is required"}), 400

    # Resolve prompt path
    if not os.path.exists(prompt_file):
        alt = os.path.join(BASE_LOG_FOLDER, prompt_file)
        if os.path.exists(alt):
            prompt_file = alt
        else:
            return jsonify({"error": f"Prompt file not found: {prompt_file}"}), 400

    # Safe default output file if missing
    if not output_file:
        output_file = "generated_logs.txt"

    # Ensure output directory exists
    out_dir = os.path.dirname(output_file)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # Read base prompt from file
    with open(prompt_file, "r", encoding="utf-8", errors="ignore") as f:
        base_prompt = f.read()

    num_lines = int(data.get("num_lines", 100))
    temperature = float(data.get("temperature", 0.7))
    top_p = float(data.get("top_p", 0.95))
    max_tokens = int(data.get("max_tokens", 400))
    hostname = data.get("hostname", "LabHost")
    log_type = data.get("log_type", "SSH")
    ip_range = data.get("ip_range", "")
    pid_range = data.get("pid_range", "")
    date_range = data.get("date_range", "")
    noise = str(data.get("noise", "0"))

    # Memory key: prefer explicit memory_id from client, else use output file path
    memory_id = (data.get("memory_id") or output_file or prompt_file).strip()

    lines = generate_logs_via_api(
        prompt=base_prompt,
        num_lines=num_lines,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        hostname=hostname,
        log_type=log_type,
        ip_range=ip_range,
        pid_range=pid_range,
        date_range=date_range,
        noise=noise,
        memory_id=memory_id,
    )

    # Save generated logs
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return jsonify({"preview": lines})



# @app.route("/api/generate_logs", methods=["POST"])
# def api_generate_logs():
#     data = request.json or {}

#     prompt_file = data.get("prompt_file", "").strip()
#     output_file = data.get("output_file", "").strip()
#     template_file = data.get("template_file", "").strip()

#     if not prompt_file:
#         return jsonify({"error": "prompt_file is required"}), 400

#     # Resolve prompt path (base logs for style)
#     if not os.path.exists(prompt_file):
#         alt = os.path.join(BASE_LOG_FOLDER, prompt_file)
#         if os.path.exists(alt):
#             prompt_file = alt
#         else:
#             return jsonify({"error": f"Prompt file not found: {prompt_file}"}), 400

#     # Safe default output file if missing
#     if not output_file:
#         output_file = "generated_logs.txt"

#     # Ensure output directory exists
#     out_dir = os.path.dirname(output_file)
#     if out_dir and not os.path.exists(out_dir):
#         os.makedirs(out_dir, exist_ok=True)

#     # Read base prompt (example logs) from file
#     with open(prompt_file, "r", encoding="utf-8", errors="ignore") as f:
#         base_prompt = f.read()

#     # Optional: scenario/high-level prompt template
#     scenario_text = ""
#     if template_file:
#         if not os.path.exists(template_file):
#             alt_tpl = os.path.join(PROMPT_TEMPLATE_FOLDER, template_file)
#             if os.path.exists(alt_tpl):
#                 template_file = alt_tpl
#             else:
#                 return jsonify(
#                     {"error": f"Template prompt file not found: {template_file}"}
#                 ), 400

#         with open(template_file, "r", encoding="utf-8", errors="ignore") as tf:
#             scenario_text = tf.read()

#     num_lines = int(data.get("num_lines", 100))
#     temperature = float(data.get("temperature", 0.7))
#     top_p = float(data.get("top_p", 0.95))
#     max_tokens = int(data.get("max_tokens", 400))
#     hostname = data.get("hostname", "LabHost")
#     log_type = data.get("log_type", "SSH")
#     ip_range = data.get("ip_range", "")
#     pid_range = data.get("pid_range", "")
#     date_range = data.get("date_range", "")
#     noise = str(data.get("noise", "0"))

#     lines = generate_logs_via_api(
#         prompt=base_prompt,
#         num_lines=num_lines,
#         temperature=temperature,
#         top_p=top_p,
#         max_tokens=max_tokens,
#         hostname=hostname,
#         log_type=log_type,
#         ip_range=ip_range,
#         pid_range=pid_range,
#         date_range=date_range,
#         noise=noise,
#         scenario_text=scenario_text,
#     )

#     # Save generated logs
#     with open(output_file, "w", encoding="utf-8") as f:
#         f.write("\n".join(lines))

#     return jsonify({"preview": lines})


# =========================
# API: Setting
# =========================

@app.route("/api/save_settings", methods=["POST"])
def api_save_settings():
    data = request.json or {}

    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return jsonify({"status": "ok"})


# =========================
# API: Clean Logs
# =========================

@app.route("/api/clean_logs", methods=["POST"])
def api_clean_logs():
    data = request.json or {}

    inp = (data.get("input") or "").strip()
    out = (data.get("output") or "").strip()
    mode = (data.get("mode") or "sshd").strip()

    if not inp:
        return jsonify({"error": "input file is required"}), 400

    # Resolve input path
    if not os.path.exists(inp):
        alt = os.path.join(BASE_LOG_FOLDER, inp)
        if os.path.exists(alt):
            inp = alt
        else:
            return jsonify({"error": f"Input file not found: {inp}"}), 400

    if not out:
        base, ext = os.path.splitext(inp)
        out = base + "_cleaned" + ext

    try:
        preview = clean_log_file(inp, out, mode)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"preview": preview})


# =========================
# API: Load Scenarios
# =========================

@app.route("/api/load_scenarios")
def api_load_scenarios():
    scenarios = load_scenarios()
    return jsonify({"scenarios": scenarios})


# =========================
# API: Timeline
# =========================

@app.route("/api/timeline", methods=["POST"])
def api_timeline():
    data = request.json or {}
    file_path = data.get("file", "").strip()

    if not file_path:
        return jsonify({"error": "file is required"}), 400

    # 1. Direct path
    if os.path.exists(file_path):
        resolved = file_path
    else:
        # 2. Inside BASE_LOG_FOLDER
        alt1 = os.path.join(BASE_LOG_FOLDER, file_path)
        alt1 = alt1.replace("\\", "/")
        if os.path.exists(alt1):
            resolved = alt1
        else:
            # 3. If user only typed filename (OpenStack_gen.txt),
            # search inside ALL system_logs subfolders
            found = None
            for root, dirs, files in os.walk(BASE_LOG_FOLDER):
                for f in files:
                    if f == os.path.basename(file_path):
                        found = os.path.join(root, f)
                        break
                if found:
                    break

            if not found:
                return jsonify(
                    {"error": f"Timeline file not found: {file_path}"}
                ), 400

            resolved = found

    # Read logs
    with open(resolved, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()

    events = []
    for i, line in enumerate(lines):
        if line.strip():
            events.append({"id": i + 1, "text": line})

    return jsonify(events)


# =========================
# API: Detector (simple placeholder)
# =========================

@app.route("/api/detect", methods=["POST"])
def api_detect():
    data = request.json or {}

    file = (data.get("file") or "").strip()
    mode = (data.get("mode") or "rule").strip()
    clf = (data.get("classifier") or "").strip()

    if not file:
        return jsonify({"error": "File is required"}), 400

    # Resolve file path
    if not os.path.exists(file):
        alt = os.path.join(BASE_LOG_FOLDER, file)
        if os.path.exists(alt):
            file = alt
        else:
            return jsonify({"error": f"File not found: {file}"}), 400

    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()

    # Rule-based detection
    if mode == "rule":
        yaml_path = os.path.join(CONFIG_FOLDER, "mitre_map.yaml")
        with open(yaml_path, "r") as y:
            mitre = yaml.safe_load(y).get("techniques", {})

        results = detect_mitre(lines, mitre)

        return jsonify({"results": results})

    # ML mode (future)
    return jsonify({"results": []})


@app.route("/api/mitre_map")
def api_mitre_map():
    yaml_path = os.path.join(CONFIG_FOLDER, "mitre_map.yaml")

    if not os.path.exists(yaml_path):
        return jsonify({"error": "mitre_map.yaml not found"}), 404

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return jsonify(data)


@app.route("/api/list_yaml_files")
def api_list_yaml_files():
    yaml_files = []
    cfg_dir = CONFIG_FOLDER

    if os.path.exists(cfg_dir):
        for f in os.listdir(cfg_dir):
            if f.endswith(".yaml") or f.endswith(".yml"):
                yaml_files.append(f"{cfg_dir}/{f}")

    return jsonify(yaml_files)


# =========================
# Main Entry
# =========================

if __name__ == "__main__":
    # Bind to 0.0.0.0:8501 as in your logs
    app.run(host="0.0.0.0", port=8501, debug=True)
