
# from typing import List
# from openai import OpenAI
# import os
# import json

# from config import OPENAI_API_KEY


# SETTINGS_FILE = "app_settings.json"


# # ------------------------------
# # Load ChatGPT model from settings.json
# # ------------------------------
# def load_selected_model() -> str:
#     """
#     Reads the selected API model from app_settings.json.
#     Default = gpt-4o-mini.
#     """
#     if not os.path.exists(SETTINGS_FILE):
#         return "gpt-4o-mini"

#     try:
#         with open(SETTINGS_FILE, "r") as f:
#             data = json.load(f)
#             return data.get("api_model", "gpt-4o-mini")
#     except Exception:
#         return "gpt-4o-mini"


# # ------------------------------
# # Initialize OpenAI client
# # ------------------------------
# client = OpenAI(api_key=OPENAI_API_KEY)


# # ------------------------------
# # Build generation prompt (NEW SYNTHETIC LOGS)
# # ------------------------------
# def build_prompt(
#     base_prompt: str,
#     hostname: str,
#     log_type: str,
#     ip_range: str,
#     pid_range: str,
#     date_range: str,
#     noise: str,
#     num_lines: int,
#     scenario_text: str = "",
# ) -> str:
#     """
#     Build a synthetic log generation prompt.
#     Uses:
#       - base_prompt: example logs (STYLE only)
#       - scenario_text: high-level scenario (BEHAVIOR/content)
#     Ensures the model generates completely new logs (not repeated).
#     """

#     scenario_block = ""
#     if scenario_text and scenario_text.strip():
#         scenario_block = (
#             "\n\nSCENARIO REQUIREMENTS:\n"
#             + scenario_text.strip()
#             + "\n"
#         )

#     extra = f"""
# You are a high-fidelity Linux / system log generator.
# You are shown EXAMPLE logs ONLY to learn the style and formatting.

# YOU MUST NOT repeat, copy, or lightly modify the example logs.

# YOUR TASK:
# - Generate *{num_lines} new synthetic log lines*.
# - Log type: {log_type}
# - Hostname: {hostname}
# - IP range allowed: {ip_range}
# - PID range allowed: {pid_range}
# - Date/time allowed: {date_range}
# - Noise/variation level: {noise}%

# If SCENARIO REQUIREMENTS are given above, you MUST align the sequence and types of events with that scenario (attack path, host roles, techniques, timing pattern).

# STRICT OUTPUT RULES:
# - Output ONLY log lines, one per line.
# - No explanations, no English sentences.
# - Timestamps MUST follow real syslog format (e.g., "Jan 10 12:34:56").
# - Match spacing, host placement, PID style, and process formatting from the examples.
# - Use realistic randomness across users, PIDs, ports, IPs, and services.
# - ALL logs must be original and must never appear in the example section.
# """

#     final = (
#         "EXAMPLE LOGS (for STYLE only):\n"
#         f"{base_prompt}\n"
#         f"{scenario_block}\n"
#         "INSTRUCTIONS:\n"
#         f"{extra}"
#     )

#     return final


# # ------------------------------
# # Main API: Generate Logs
# # ------------------------------
# def generate_logs_via_api(
#     prompt: str,
#     num_lines: int,
#     temperature: float,
#     top_p: float,
#     max_tokens: int,
#     hostname: str,
#     log_type: str,
#     ip_range: str,
#     pid_range: str,
#     date_range: str,
#     noise: str,
#     scenario_text: str = "",
# ) -> List[str]:
#     """
#     Generate logs using:
#       - prompt: base example logs (style)
#       - scenario_text: optional high-level scenario/template
#     """

#     # Load selected ChatGPT model
#     model_name = load_selected_model()

#     # Build final prompt with instructions + scenario
#     final_prompt = build_prompt(
#         base_prompt=prompt,
#         hostname=hostname,
#         log_type=log_type,
#         ip_range=ip_range,
#         pid_range=pid_range,
#         date_range=date_range,
#         noise=noise,
#         num_lines=num_lines,
#         scenario_text=scenario_text,
#     )

#     # Ensure max_tokens is large enough
#     if max_tokens < 1024:
#         max_tokens = 2048

#     # Call OpenAI API
#     response = client.chat.completions.create(
#         model=model_name,
#         messages=[
#             {"role": "system", "content": "You generate realistic Linux/system log files."},
#             {"role": "user", "content": final_prompt},
#         ],
#         temperature=temperature,
#         top_p=top_p,
#         max_tokens=max_tokens,
#     )

#     # Extract response
#     raw = (response.choices[0].message.content or "").strip()

#     # Split into individual log lines
#     lines = [line for line in raw.splitlines() if line.strip()]

#     # If model outputs less lines, expand by re-randomization
#     if len(lines) < num_lines:
#         needed = num_lines - len(lines)

#         regen_prompt = final_prompt + f"\n\nNow generate {needed} MORE new unique log lines."
#         regen = client.chat.completions.create(
#             model=model_name,
#             messages=[
#                 {"role": "system", "content": "You generate realistic Linux/system log files."},
#                 {"role": "user", "content": regen_prompt},
#             ],
#             temperature=temperature,
#             top_p=top_p,
#             max_tokens=max_tokens,
#         )

#         extra_raw = regen.choices[0].message.content or ""
#         extra_lines = [x for x in extra_raw.splitlines() if x.strip()]
#         lines.extend(extra_lines)

#     # Trim exactly to requested lines
#     return lines[:num_lines]
# utils/llm_api.py
# from typing import List, Optional
# from openai import OpenAI
# import os
# import json

# from config import OPENAI_API_KEY
# from utils.memory_utils import get_history, add_turn

# SETTINGS_FILE = "app_settings.json"


# def load_selected_model() -> str:
#     """
#     Reads the selected API model from app_settings.json.
#     Default = gpt-4o-mini.
#     """
#     if not os.path.exists(SETTINGS_FILE):
#         return "gpt-4o-mini"

#     try:
#         with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             return data.get("api_model", "gpt-4o-mini")
#     except Exception:
#         return "gpt-4o-mini"


# # Initialize OpenAI client
# client = OpenAI(api_key=OPENAI_API_KEY)


# def build_prompt(
#     base_prompt: str,
#     hostname: str,
#     log_type: str,
#     ip_range: str,
#     pid_range: str,
#     date_range: str,
#     noise: str,
#     num_lines: int,
# ) -> str:
#     """
#     Build a synthetic log generation prompt.
#     Ensures the model generates completely new logs (not repeated).
#     """

#     extra = f"""
# You are a high-fidelity Linux / system log generator.
# You are shown EXAMPLE logs ONLY to learn the style.

# YOU MUST NOT repeat, copy, or lightly modify the example logs.

# YOUR TASK:
# - Generate *{num_lines} new synthetic log lines*.
# - Log type: {log_type}
# - Hostname: {hostname}
# - IP range allowed: {ip_range}
# - PID range allowed: {pid_range}
# - Date/time allowed: {date_range}
# - Noise/variation level: {noise}%

# STRICT OUTPUT RULES:
# - Output ONLY log lines, one per line.
# - No explanations, no English sentences.
# - Timestamp MUST follow real syslog format.
# - Match spacing, host placement, PID style, and process formatting.
# - USE realistic randomness across users, PIDs, ports, IPs, services.
# - ALL logs must be original and never appear in the example section.
# """

#     return f"EXAMPLE LOGS (for STYLE only):\n{base_prompt}\n\nINSTRUCTIONS:\n{extra}"


# def generate_logs_via_api(
#     prompt: str,
#     num_lines: int,
#     temperature: float,
#     top_p: float,
#     max_tokens: int,
#     hostname: str,
#     log_type: str,
#     ip_range: str,
#     pid_range: str,
#     date_range: str,
#     noise: str,
#     memory_id: Optional[str] = None,
# ) -> List[str]:
#     """
#     Main API to generate logs via OpenAI.

#     If memory_id is provided, we:
#       - load previous (user, assistant) turns from llm_memory.json
#       - prepend them to the messages list
#       - store this new turn after generation
#     """

#     model_name = load_selected_model()

#     # Build final prompt with instructions
#     final_prompt = build_prompt(
#         base_prompt=prompt,
#         hostname=hostname,
#         log_type=log_type,
#         ip_range=ip_range,
#         pid_range=pid_range,
#         date_range=date_range,
#         noise=noise,
#         num_lines=num_lines,
#     )

#     # Ensure max_tokens is large enough
#     if max_tokens < 1024:
#         max_tokens = 2048

#     # Build message list with optional memory
#     messages = [
#         {
#             "role": "system",
#             "content": "You generate realistic Linux/system log files.",
#         }
#     ]

#     if memory_id:
#         history = get_history(memory_id)
#         if history:
#             messages.extend(history)

#     # Current user request
#     messages.append({"role": "user", "content": final_prompt})

#     # Call OpenAI API
#     response = client.chat.completions.create(
#         model=model_name,
#         messages=messages,
#         temperature=temperature,
#         top_p=top_p,
#         max_tokens=max_tokens,
#     )

#     raw = (response.choices[0].message.content or "").strip()
#     lines = [line for line in raw.splitlines() if line.strip()]

#     # If not enough lines, try one small follow-up generation
#     if len(lines) < num_lines:
#         needed = num_lines - len(lines)
#         regen_prompt = final_prompt + f"\n\nNow generate {needed} MORE new unique log lines."

#         regen_messages = [
#             {
#                 "role": "system",
#                 "content": "You generate realistic Linux/system log files.",
#             }
#         ]

#         if memory_id:
#             history = get_history(memory_id)
#             if history:
#                 regen_messages.extend(history)

#         regen_messages.append({"role": "user", "content": regen_prompt})

#         regen = client.chat.completions.create(
#             model=model_name,
#             messages=regen_messages,
#             temperature=temperature,
#             top_p=top_p,
#             max_tokens=max_tokens,
#         )

#         extra_raw = regen.choices[0].message.content or ""
#         extra_lines = [x for x in extra_raw.splitlines() if x.strip()]
#         lines.extend(extra_lines)

#     # Trim exactly to requested lines
#     final_lines = lines[:num_lines]

#     # Store this turn in memory (prompt + generated text)
#     if memory_id:
#         add_turn(memory_id, final_prompt, "\n".join(final_lines))

#     return final_lines

from typing import List, Optional
import os
import json

from httpx import Client as HttpxClient
from openai import OpenAI    # IMPORTANT: Use this, not 'import openai'

from config import OPENAI_API_KEY
from utils.memory_utils import get_history, add_turn

SETTINGS_FILE = "app_settings.json"

# ------------------------------------------------------------
# 🔥 Render-safe OpenAI client
# ------------------------------------------------------------
# Render injects proxy config → OpenAI SDK breaks.
# We must disable proxies manually using httpx.
# ------------------------------------------------------------

# Disable all proxies completely
http_client = HttpxClient(proxies=None)

# Create OpenAI client with proxy-free HTTP backend
client = OpenAI(
    api_key=OPENAI_API_KEY,
    http_client=http_client,
)


def load_selected_model() -> str:
    """
    Reads the selected API model from app_settings.json.
    Default = gpt-4o-mini.
    """
    if not os.path.exists(SETTINGS_FILE):
        return "gpt-4o-mini"

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("api_model", "gpt-4o-mini")
    except Exception:
        return "gpt-4o-mini"


def build_prompt(
    base_prompt: str,
    hostname: str,
    log_type: str,
    ip_range: str,
    pid_range: str,
    date_range: str,
    noise: str,
    num_lines: int,
) -> str:
    """Build synthetic log generation prompt."""

    extra = f"""
You are a high-fidelity Linux / system log generator.
You are shown EXAMPLE logs ONLY to learn the style.

YOU MUST NOT repeat, copy, or lightly modify the example logs.

YOUR TASK:
- Generate *{num_lines} new synthetic log lines*.
- Log type: {log_type}
- Hostname: {hostname}
- IP range allowed: {ip_range}
- PID range allowed: {pid_range}
- Date/time allowed: {date_range}
- Noise/variation level: {noise}%

STRICT OUTPUT RULES:
- Output ONLY log lines, one per line.
- No explanations, no English sentences.
- Timestamp MUST follow real syslog format.
- Match spacing, host placement, PID style, and process formatting.
- USE realistic randomness across users, PIDs, ports, IPs, services.
- ALL logs must be original and never appear in the example section.
"""

    return f"EXAMPLE LOGS (for STYLE only):\n{base_prompt}\n\nINSTRUCTIONS:\n{extra}"


def generate_logs_via_api(
    prompt: str,
    num_lines: int,
    temperature: float,
    top_p: float,
    max_tokens: int,
    hostname: str,
    log_type: str,
    ip_range: str,
    pid_range: str,
    date_range: str,
    noise: str,
    memory_id: Optional[str] = None,
) -> List[str]:
    """
    Calls OpenAI API to generate logs.
    Now Render-safe due to proxy-free client.
    """

    model_name = load_selected_model()

    # Build final prompt
    final_prompt = build_prompt(
        base_prompt=prompt,
        hostname=hostname,
        log_type=log_type,
        ip_range=ip_range,
        pid_range=pid_range,
        date_range=date_range,
        noise=noise,
        num_lines=num_lines,
    )

    # Ensure sufficient token budget
    if max_tokens < 1024:
        max_tokens = 2048

    # Build message history
    messages = [
        {
            "role": "system",
            "content": "You generate realistic Linux/system log files.",
        }
    ]

    # Add memory if present
    if memory_id:
        history = get_history(memory_id)
        if history:
            messages.extend(history)

    messages.append({"role": "user", "content": final_prompt})

    # -------------------------------------------------
    # 🔥 MAIN API CALL (Render-safe)
    # -------------------------------------------------
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )

    raw = (response.choices[0].message.content or "").strip()
    lines = [line for line in raw.splitlines() if line.strip()]

    # -------------------------------------------------
    # If fewer than num_lines generated → ask for more
    # -------------------------------------------------
    if len(lines) < num_lines:
        needed = num_lines - len(lines)
        regen_prompt = (
            final_prompt
            + f"\n\nNow generate {needed} MORE completely new unique log lines."
        )

        regen_messages = [
            {
                "role": "system",
                "content": "You generate realistic Linux/system log files.",
            }
        ]

        if memory_id:
            history = get_history(memory_id)
            if history:
                regen_messages.extend(history)

        regen_messages.append({"role": "user", "content": regen_prompt})

        regen = client.chat.completions.create(
            model=model_name,
            messages=regen_messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        )

        extra_raw = regen.choices[0].message.content or ""
        extra_lines = [x for x in extra_raw.splitlines() if x.strip()]
        lines.extend(extra_lines)

    final_lines = lines[:num_lines]

    # Save conversation into memory
    if memory_id:
        add_turn(memory_id, final_prompt, "\n".join(final_lines))

    return final_lines
